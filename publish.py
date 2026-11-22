"""
Publish scheduled Instagram posts for @805scorelab through Meta's Content Publishing API.

Run by GitHub Actions on a cron. Reads posts.json, finds entries whose scheduled time has passed and that have no
published_id, publishes them (carousel, reel or story), and writes the media id back into the manifest. Ported from
pietrocappellaro31-art/ib-autopost (the sister page), with every trap that page hit kept as a guard.

Environment (repository secrets):
    IG_ACCESS_TOKEN   system-user token with instagram_content_publish (never printed)
    IG_USER_ID        optional; otherwise discovered from the token's Pages

Modes:
    python publish.py                  publish anything due (cron default)
    python publish.py --selftest       create one image container, publish nothing, print PASS
    python publish.py --reel-selftest <branch> <file>   upload a Reel container, publish nothing
    python publish.py --insights       record recent post performance into docs/daily/performance.*

Invariants:
    - A post with a published_id is never touched again (the only guard against a double publish).
    - Containers are created at publish time only; they expire after 24 hours.
    - At most 2 carousels, 2 reels and 1 story per Eastern day; at most 1 overdue post per format per run.
    - The token is stripped from every error body before printing (the repo and its logs are public).
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, time as clock, timedelta, timezone
from zoneinfo import ZoneInfo

EASTERN = ZoneInfo("America/New_York")
ROOT = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(ROOT, "posts.json")
REPO = os.environ.get("GITHUB_REPOSITORY", "805scorelab/gmat-autopost")

DAILY_CAP = {"carousel": 2, "reel": 2, "story": 1}          # per Eastern day, all from the manifest
MAX_ATTEMPTS = 3                                              # a post that failed 3 times waits for a person
LATE_HOURS = 6                                                # later than this, a post moves to its slot's next turn
PROBE_HOURS = 6                                               # while Meta blocks the app, probe once every 6 hours
BLOCK_MARKERS = ("API access blocked", "2207042", "temporarily blocked", "unusual activity", "\"code\":368",
                 "\"code\":4,", "\"code\":17,", "\"code\":32,", "\"code\":613")

GRAPH_VERSION = "v21.0"
GRAPH_ROOT = f"https://graph.facebook.com/{GRAPH_VERSION}"
POLL_SECONDS = 10
POLL_ATTEMPTS = 30            # images: 5 minutes
VIDEO_POLL_ATTEMPTS = 60      # video transcoding: 10 minutes


# --------------------------------------------------------------------------------------------------- Graph API
def _token():
    return os.environ["IG_ACCESS_TOKEN"]


def _scrub(text):
    token = os.environ.get("IG_ACCESS_TOKEN", "")
    return text.replace(token, "<token>") if token else text


def call_graph(path, params, method="GET"):
    """Send one request to the Graph API and return the decoded JSON."""
    params = dict(params, access_token=_token())
    url = f"{GRAPH_ROOT}/{path}"
    data = urllib.parse.urlencode(params).encode()
    request = (urllib.request.Request(f"{url}?{data.decode()}") if method == "GET"
               else urllib.request.Request(url, data=data, method="POST"))
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as error:
        body = _scrub(error.read().decode(errors="replace"))
        raise RuntimeError(f"Graph API {error.code} on {path}: {body}") from None
    except urllib.error.URLError as error:
        raise RuntimeError(_scrub(f"Network error on {path}: {error}")) from None


def wait_until_ready(container_id, attempts=POLL_ATTEMPTS):
    for _ in range(attempts):
        status = call_graph(container_id, {"fields": "status_code,status"})
        code = status.get("status_code")
        if code == "FINISHED":
            return
        if code in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"Container {container_id} ended as {code}: {status}")
        time.sleep(POLL_SECONDS)
    raise RuntimeError(f"Container {container_id} never finished processing")


def publish_container(ig_user_id, container_id):
    return call_graph(f"{ig_user_id}/media_publish", {"creation_id": container_id}, method="POST")["id"]


def remaining_quota(ig_user_id):
    """Trust the live number: Meta's docs disagree on the cap (50 vs 100 per 24h)."""
    result = call_graph(f"{ig_user_id}/content_publishing_limit", {"fields": "quota_usage,config"})
    entry = (result.get("data") or [{}])[0]
    return entry.get("config", {}).get("quota_total", 50) - entry.get("quota_usage", 0)


def is_block_error(error):
    return any(marker in str(error) for marker in BLOCK_MARKERS)


def resolve_ig_user_id():
    explicit = os.environ.get("IG_USER_ID", "").strip()
    if explicit:
        return explicit
    result = call_graph("me/accounts", {"fields": "name,instagram_business_account{id,username}"})
    found = [(p.get("name"), p["instagram_business_account"]["id"], p["instagram_business_account"].get("username"))
             for p in result.get("data", []) if p.get("instagram_business_account")]
    if not found:
        raise RuntimeError("No Instagram professional account is reachable from this token. Check that the Page is "
                           "assigned to the system user and that the Instagram account is connected to that Page.")
    if len(found) > 1:
        raise RuntimeError("Several Instagram accounts reachable: "
                           + ", ".join(f"{u} ({i})" for _, i, u in found) + ". Set IG_USER_ID.")
    page, ig_id, username = found[0]
    print(f"Resolved @{username} ({ig_id}) via Page '{page}'")
    return ig_id


# --------------------------------------------------------------------------------------------------- media URLs
def media_url(manifest, name):
    return name if name.startswith("http") else manifest["media_base"] + urllib.parse.quote(name)


def branch_url(branch, name):
    """Reels wait on a temporary media/<slug> branch so MP4s never enter main's history."""
    return (f"https://raw.githubusercontent.com/{REPO}/refs/heads/{urllib.parse.quote(branch)}/"
            f"{urllib.parse.quote(name)}")


def video_location(manifest, post, key):
    name = post.get(key)
    if not name:
        return None
    return branch_url(post["media_branch"], name) if post.get("media_branch") else media_url(manifest, name)


def caption_of(post):
    if post.get("caption") is not None:
        return post["caption"]
    with open(os.path.join(ROOT, post["caption_file"]), encoding="utf-8") as handle:
        return handle.read().strip()


# --------------------------------------------------------------------------------------------------- publishers
def publish_carousel(ig_user_id, post, manifest):
    children = []
    for name in post["media"]:
        params = {"image_url": media_url(manifest, name), "is_carousel_item": "true"}
        children.append(call_graph(f"{ig_user_id}/media", params, method="POST")["id"])
    print(f"  {len(children)} item containers")
    parent = call_graph(f"{ig_user_id}/media", {"media_type": "CAROUSEL", "children": ",".join(children),
                                                 "caption": caption_of(post)}, method="POST")["id"]
    wait_until_ready(parent)
    return publish_container(ig_user_id, parent)


def reel_container(ig_user_id, post, manifest):
    """Meta fetches video_url itself. On the sister page the resumable binary upload refused every Reel of 40 s or
    more (ProcessingFailedError) while video_url from the branch worked, so video_url is the default."""
    params = {"media_type": "REELS", "video_url": video_location(manifest, post, "video"),
              "caption": caption_of(post), "share_to_feed": "true"}
    if post.get("ai_generated"):
        params["is_ai_generated"] = "true"        # only accepted at container creation
    cover = video_location(manifest, post, "cover")
    if cover:
        params["cover_url"] = cover
    elif post.get("thumb_offset_ms") is not None:
        params["thumb_offset"] = str(int(post["thumb_offset_ms"]))
    return call_graph(f"{ig_user_id}/media", params, method="POST")["id"]


def publish_reel(ig_user_id, post, manifest, publish=True):
    container = reel_container(ig_user_id, post, manifest)
    print(f"  reel container {container}")
    wait_until_ready(container, attempts=VIDEO_POLL_ATTEMPTS)
    if not publish:
        return container
    media_id = publish_container(ig_user_id, container)
    if post.get("media_branch"):
        delete_branch(post["media_branch"])
    return media_id


def publish_story(ig_user_id, post, manifest):
    """Stories take no caption, and the API cannot add stickers (polls, quizzes, links)."""
    name = post["media"][0]
    params = {"media_type": "STORIES"}
    if name.lower().endswith(".mp4"):
        params["video_url"] = video_location(manifest, {**post, "v": name}, "v")
    else:
        params["image_url"] = media_url(manifest, name)
    if post.get("ai_generated"):
        params["is_ai_generated"] = "true"
    container = call_graph(f"{ig_user_id}/media", params, method="POST")["id"]
    wait_until_ready(container, attempts=VIDEO_POLL_ATTEMPTS if "video_url" in params else POLL_ATTEMPTS)
    return publish_container(ig_user_id, container)


def already_on_instagram(ig_user_id, post, manifest):
    """Last guard against a double publish (21 Nov: a queued run started from a stale checkout and posted the same
    carousel twice). Before publishing, look at the account's recent media: a feed post or Reel whose caption starts
    the same way, posted in the last 48 hours, means this entry is already live. Stories carry no caption and expire,
    so they are matched by the time window only through the manifest."""
    if post["type"] == "story":
        return None
    head = caption_of(post).strip()[:90]
    res = call_graph(f"{ig_user_id}/media", {"fields": "id,caption,timestamp", "limit": "25"})
    for m in res.get("data", []):
        age_h = (datetime.now(timezone.utc) - utc(m["timestamp"].replace("+0000", "+00:00"))).total_seconds() / 3600
        if age_h <= 48 and (m.get("caption") or "").strip()[:90] == head:
            return m["id"]
    return None


PUBLISHERS = {"carousel": publish_carousel, "reel": publish_reel, "story": publish_story}


def delete_branch(branch):
    token = os.environ.get("GITHUB_TOKEN")
    if not token or not branch.startswith("media/"):
        return
    request = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/git/refs/heads/{urllib.parse.quote(branch)}", method="DELETE",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"})
    try:
        urllib.request.urlopen(request, timeout=30)
        print(f"  deleted branch {branch}")
    except Exception as error:
        print(f"  branch {branch} not deleted: {error}", file=sys.stderr)


# --------------------------------------------------------------------------------------------------- scheduling
def utc(stamp):
    parsed = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def load_manifest():
    with open(MANIFEST, encoding="utf-8") as handle:
        return json.load(handle)


def save_manifest(manifest):
    with open(MANIFEST, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def next_slot_time(post, now):
    """The next time this post's Eastern wall-clock slot comes round, converted per date (DST-safe)."""
    slot_et = utc(post["scheduled_utc"]).astimezone(EASTERN).time()
    day = now.astimezone(EASTERN).date()
    candidate = datetime.combine(day, clock(slot_et.hour, slot_et.minute), EASTERN)
    if candidate.astimezone(timezone.utc) <= now:
        candidate = datetime.combine(day + timedelta(days=1), clock(slot_et.hour, slot_et.minute), EASTERN)
    return candidate.astimezone(timezone.utc)


def select_due(manifest, now):
    """Pick what to publish this run.

    Rules: unpublished and scheduled in the past; fewer than MAX_ATTEMPTS failures; a post more than LATE_HOURS late
    moves to its slot's next turn instead of going out at an odd hour; per format, at most the day's remaining cap
    and at most ONE post per run, so a recovered account never dumps a backlog in one scroll.
    """
    today = now.astimezone(EASTERN).date()
    published_today = {kind: 0 for kind in DAILY_CAP}
    for post in manifest["posts"]:
        if post.get("published_id") and post.get("published_at_utc"):
            if utc(post["published_at_utc"]).astimezone(EASTERN).date() == today:
                published_today[post["type"]] = published_today.get(post["type"], 0) + 1

    chosen, seen = [], set()
    for post in sorted(manifest["posts"], key=lambda p: p["scheduled_utc"]):
        if post.get("published_id"):
            continue
        kind = post["type"]
        if post.get("attempts", 0) >= MAX_ATTEMPTS:
            print(f"Skipping {post['id']}: failed {post['attempts']} times ({(post.get('last_error') or '')[:120]})")
            continue
        scheduled = utc(post["scheduled_utc"])
        if scheduled > now:
            continue
        if (now - scheduled).total_seconds() > LATE_HOURS * 3600:
            moved = next_slot_time(post, now)
            post["scheduled_utc"] = moved.strftime("%Y-%m-%dT%H:%M:%SZ")
            post.setdefault("moved_log", []).append(f"{now:%Y-%m-%d %H:%M}Z missed slot, moved to {post['scheduled_utc']}")
            print(f"{post['id']} missed its slot by more than {LATE_HOURS} h; moved to {post['scheduled_utc']}")
            continue
        if kind in seen:
            continue
        if published_today.get(kind, 0) >= DAILY_CAP.get(kind, 0):
            print(f"Daily cap reached for {kind} ({DAILY_CAP.get(kind)}); holding {post['id']}")
            continue
        seen.add(kind)
        chosen.append(post)
    return chosen


# --------------------------------------------------------------------------------------------------- modes
def selftest(ig_user_id, manifest):
    image_url = media_url(manifest, manifest.get("selftest_image", "selftest.jpg"))
    print(f"Self-test against {image_url}")
    print(f"  remaining quota in this 24h window: {remaining_quota(ig_user_id)}")
    container = call_graph(f"{ig_user_id}/media", {"image_url": image_url, "is_carousel_item": "true"},
                           method="POST")["id"]
    wait_until_ready(container)
    print(f"  container {container} reached FINISHED")
    print("PASS - credentials, media hosting and the publishing API all work. Nothing was posted.")
    return 0


def reel_selftest(ig_user_id, manifest, branch, name):
    post = dict(caption="Self-test, not published.", media_branch=branch, video=name, ai_generated=True)
    container = publish_reel(ig_user_id, post, manifest, publish=False)
    print(f"  container {container} FINISHED (nothing published)")
    print("PASS - the Reel upload path works. Nothing was posted.")
    return 0


PERF_JSON = os.path.join(ROOT, "docs", "daily", "performance.json")
PERF_MD = os.path.join(ROOT, "docs", "daily", "performance.md")
METRICS = {"reel": ("reach", "views", "saved", "shares", "total_interactions", "likes", "comments",
                    "ig_reels_avg_watch_time", "follows"),
           "feed": ("reach", "views", "saved", "shares", "total_interactions", "likes", "comments", "follows")}


def collect_insights(ig_user_id, limit=40):
    res = call_graph(f"{ig_user_id}/media", {"fields": "id,caption,media_product_type,media_type,timestamp,permalink",
                                              "limit": str(limit)})
    rows, unavailable, accepted = [], set(), {}
    for media in res.get("data", []):
        kind = "reel" if media.get("media_product_type") == "REELS" else "feed"
        names = accepted.get(kind, METRICS[kind])
        got = {}
        for name in names:
            try:
                data = call_graph(f"{media['id']}/insights", {"metric": name}).get("data", [])
                for m in data:
                    got[m["name"]] = (m.get("values") or [{}])[0].get("value", m.get("total_value", {}).get("value"))
            except Exception:
                unavailable.add(f"{kind} {name}")
        accepted.setdefault(kind, [n for n in names if f"{kind} {n}" not in unavailable])
        when = utc(media["timestamp"].replace("+0000", "+00:00"))
        rows.append(dict(id=media["id"], kind=kind if kind == "reel" else media.get("media_type", "").lower(),
                         permalink=media.get("permalink"),
                         posted_et=when.astimezone(EASTERN).strftime("%Y-%m-%d %a %H:%M"),
                         hours_live=round((datetime.now(timezone.utc) - when).total_seconds() / 3600, 1),
                         caption=(media.get("caption") or "").split("\n")[0][:90], **got))
    return dict(updated_utc=datetime.now(timezone.utc).isoformat(timespec="seconds"), media=rows,
                unavailable=sorted(unavailable))


def write_performance(perf):
    os.makedirs(os.path.dirname(PERF_JSON), exist_ok=True)
    with open(PERF_JSON, "w", encoding="utf-8") as handle:
        json.dump(perf, handle, indent=1, ensure_ascii=False)
        handle.write("\n")
    rows = sorted([r for r in perf["media"] if r["hours_live"] >= 24], key=lambda r: -(r.get("reach") or 0))
    lines = ["# Performance (written by publish.py; do not edit by hand)", "",
             f"Updated {perf['updated_utc']} UTC. Posts live 24 hours or more, best reach first.", "",
             "| Posted (ET) | Kind | Reach | Views | Saves | Shares | Comments | Follows | Avg watch ms | Line 1 |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['posted_et']} | {r['kind']} | {r.get('reach', '')} | {r.get('views', '')} | "
                     f"{r.get('saved', '')} | {r.get('shares', '')} | {r.get('comments', '')} | {r.get('follows', '')} | "
                     f"{r.get('ig_reels_avg_watch_time', '')} | {r['caption'].replace('|', '/')} |")
    if perf.get("unavailable"):
        lines += ["", "Not readable with the current token: " + ", ".join(perf["unavailable"])]
    with open(PERF_MD, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def insights_if_stale(ig_user_id, max_age_hours=20):
    try:
        with open(PERF_JSON, encoding="utf-8") as handle:
            age = (datetime.now(timezone.utc) - utc(json.load(handle)["updated_utc"])).total_seconds() / 3600
    except Exception:
        age = 1e9
    if age >= max_age_hours:
        write_performance(collect_insights(ig_user_id))
        print("  performance recorded")


RECORD_KEYS = ("published_id", "published_at_utc", "attempts", "last_error", "note", "moved_log", "scheduled_utc")


def export_records(path):
    """Write this run's publish records (by post id) so they can be re-applied onto a newer main."""
    m = load_manifest()
    records = {p["id"]: {k: p[k] for k in RECORD_KEYS if k in p} for p in m["posts"]}
    with open(path, "w") as handle:
        json.dump(dict(records=records, api_block=m.get("api_block")), handle)


def apply_records(path):
    """Merge exported records into the current posts.json. A published_id is never removed or replaced."""
    data = json.load(open(path))
    m = load_manifest()
    for p in m["posts"]:
        rec = data["records"].get(p["id"])
        if not rec:
            continue
        if p.get("published_id") and rec.get("published_id") and p["published_id"] != rec["published_id"]:
            p.setdefault("duplicate_published_ids", []).append(rec["published_id"])
            continue
        for k, v in rec.items():
            if k == "published_id" and p.get("published_id"):
                continue
            p[k] = v
    if data.get("api_block"):
        m["api_block"] = data["api_block"]
    save_manifest(m)


def main():
    now = datetime.now(timezone.utc)
    if "--export-records" in sys.argv:
        export_records(sys.argv[sys.argv.index("--export-records") + 1])
        return 0
    if "--apply-records" in sys.argv:
        apply_records(sys.argv[sys.argv.index("--apply-records") + 1])
        return 0
    manifest = load_manifest()

    if "{{" in manifest["media_base"] or "OWNER" in manifest["media_base"]:
        print("media_base still contains a placeholder. Nothing was called.", file=sys.stderr)
        return 1

    if "--selftest" in sys.argv:
        return selftest(resolve_ig_user_id(), manifest)
    if "--reel-selftest" in sys.argv:
        i = sys.argv.index("--reel-selftest")
        return reel_selftest(resolve_ig_user_id(), manifest, sys.argv[i + 1], sys.argv[i + 2])
    if "--insights" in sys.argv:
        write_performance(collect_insights(resolve_ig_user_id()))
        print("performance recorded")
        return 0

    if "--wait" in sys.argv:
        # GitHub drops many cron runs on quiet repos (21 Nov: the */10 window around 23:30 UTC never fired and the
        # 18:30 ET carousel went out 12 minutes late by hand). The hourly run is the one that does fire, so it waits
        # here for the next post due within the hour and publishes it on time.
        limit = float(sys.argv[sys.argv.index("--wait") + 1]) * 60
        upcoming = sorted(utc(p["scheduled_utc"]) for p in manifest["posts"]
                          if not p.get("published_id") and 0 < (utc(p["scheduled_utc"]) - now).total_seconds() <= limit)
        if upcoming:
            pause = (upcoming[0] - now).total_seconds() + 5
            print(f"Next post due at {upcoming[0]:%H:%M} UTC; waiting {pause / 60:.1f} min")
            time.sleep(pause)
            now = datetime.now(timezone.utc)

    before = json.dumps(manifest, sort_keys=True)
    due = select_due(manifest, now)
    if json.dumps(manifest, sort_keys=True) != before:
        save_manifest(manifest)                      # moved slots are recorded even when nothing is due

    block = manifest.get("api_block")
    if due and block:
        last = utc(block.get("last_probe_utc") or block["since_utc"])
        if (now - last).total_seconds() < PROBE_HOURS * 3600:
            print(f"API BLOCKED since {block['since_utc']} ({block.get('error', '')[:120]}). {len(due)} post(s) "
                  f"waiting; next probe after {PROBE_HOURS} h. The owner must clear Meta's checkpoint.",
                  file=sys.stderr)
            return 1

    if not due:
        print("Nothing due.")                         # no network call has been made
        return 0

    try:
        ig_user_id = resolve_ig_user_id()
        quota = remaining_quota(ig_user_id)
    except Exception as error:
        if is_block_error(error):
            manifest["api_block"] = dict(since_utc=(block or {}).get("since_utc") or now.isoformat(timespec="seconds"),
                                         last_probe_utc=now.isoformat(timespec="seconds"), error=str(error)[:300])
            save_manifest(manifest)
            print(f"API BLOCKED: {error}. Recorded; no more calls for {PROBE_HOURS} h.", file=sys.stderr)
            return 1
        raise
    if block:
        manifest.pop("api_block", None)
        save_manifest(manifest)
        print(f"API access is back (blocked since {block['since_utc']}).")

    print(f"{len(due)} post(s) due, {quota} remaining in the 24h window")
    if quota <= len(due) + 2:                          # keep a margin under the live cap
        due = due[:max(quota - 2, 0)]
        print(f"Quota close to the cap; publishing {len(due)}.")

    failures = 0
    for post in due:
        print(f"Publishing {post['id']} ({post['type']}, scheduled {post['scheduled_utc']})")
        try:
            live = already_on_instagram(ig_user_id, post, manifest)
            if live:
                post["published_id"] = live
                post["published_at_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
                post["note"] = "found already live on Instagram; not published again"
                save_manifest(manifest)
                print(f"  already live as {live}; recorded, NOT published again")
                continue
            post["published_id"] = PUBLISHERS[post["type"]](ig_user_id, post, manifest)
            post["published_at_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
            post["last_error"] = None
            save_manifest(manifest)                    # written immediately; the workflow commits it
            print(f"  published as {post['published_id']}")
        except Exception as error:
            failures += 1
            post["last_error"] = _scrub(str(error))[:300]
            post["attempts"] = post.get("attempts", 0) + 1
            save_manifest(manifest)
            print(f"  FAILED: {post['last_error']}", file=sys.stderr)
            if is_block_error(error):
                if "access blocked" in str(error).lower():
                    manifest["api_block"] = dict(since_utc=now.isoformat(timespec="seconds"),
                                                 last_probe_utc=now.isoformat(timespec="seconds"),
                                                 error=str(error)[:300])
                    save_manifest(manifest)
                print("STOPPING: the error looks like a block or a rate limit.", file=sys.stderr)
                break

    try:
        insights_if_stale(ig_user_id)
    except Exception as error:
        print(f"  insights not refreshed: {_scrub(str(error))[:200]}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
