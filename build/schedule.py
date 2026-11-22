"""Queue a built post into posts.json. Times are given in US Eastern and converted to UTC per date (DST-safe).

    cd build
    python3 schedule.py 2026-11-23-c1 carousel "2026-11-23 08:00" --series "Problem of the Day" --ground mint --pos 6
    python3 schedule.py 2026-11-23-r1 reel "2026-11-23 12:30" --series Shortcut --ground forest --pos 7
    python3 schedule.py 2026-11-23-s1 story "2026-11-23 07:30" --answer D

carousel: copies build/out/<id>/*.jpg to media/<id>/.  story: copies build/out/<id>/<id>.jpg.
reel: pushes build/out/<id>/<id>.mp4 and <id>-cover.jpg to the temporary branch media/<id> (never to main).
The caption must be build/captions/<id>.clean.txt with a PASS lint (stories have none). An entry with the same id is
replaced only if it has not been published. The manifest stays sorted.
"""
import argparse
import json
import pathlib
import shutil
import subprocess
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
EASTERN = ZoneInfo("America/New_York")


def git(*args, **kw):
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True, **kw).stdout.strip()


def push_reel_branch(post_id):
    out = BUILD / "out" / post_id
    blobs = []
    for name in (f"{post_id}.mp4", f"{post_id}-cover.jpg"):
        blobs.append((git("hash-object", "-w", str(out / name)), name))
    tree = git("mktree", input="".join(f"100644 blob {b}\t{n}\n" for b, n in blobs))
    commit = git("-c", "user.name=805scorelab", "-c", "user.email=805scorelab@users.noreply.github.com",
                 "commit-tree", tree, "-m", f"Reel media {post_id} (temporary branch, deleted once posted)")
    git("push", "-q", "-f", "origin", f"{commit}:refs/heads/media/{post_id}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("type", choices=["carousel", "reel", "story"])
    ap.add_argument("eastern", help='"YYYY-MM-DD HH:MM" US Eastern')
    ap.add_argument("--series", default="")
    ap.add_argument("--ground", default=None)
    ap.add_argument("--pos", type=int, default=None, help="grid position (feed posts)")
    ap.add_argument("--answer", default=None, help="the correct letter (stories: shown in the next story)")
    ap.add_argument("--silent", action="store_true", help="reel without narration (retired 21 Nov; voiced is standard)")
    a = ap.parse_args()

    local = datetime.strptime(a.eastern, "%Y-%m-%d %H:%M").replace(tzinfo=EASTERN)
    when = local.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    entry = dict(id=a.id, type=a.type, series=a.series, scheduled_utc=when)
    if a.answer:
        entry["answer"] = a.answer
    out = BUILD / "out" / a.id
    if a.type == "carousel":
        files = sorted(out.glob(f"{a.id}-*.jpg"))
        assert files, f"no slides in {out}"
        dest = ROOT / "media" / a.id
        dest.mkdir(parents=True, exist_ok=True)
        for f in files:
            shutil.copy(f, dest / f.name)
        entry["media"] = [f"{a.id}/{f.name}" for f in files]
    elif a.type == "story":
        dest = ROOT / "media" / a.id
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copy(out / f"{a.id}.jpg", dest / f"{a.id}.jpg")
        entry["media"] = [f"{a.id}/{a.id}.jpg"]
    else:
        push_reel_branch(a.id)
        entry.update(media_branch=f"media/{a.id}", video=f"{a.id}.mp4", cover=f"{a.id}-cover.jpg",
                     audio="silent" if a.silent else "voiced")
    if a.type != "story":
        cap = BUILD / "captions" / f"{a.id}.clean.txt"
        lint = BUILD / "captions" / f"{a.id}.lint.txt"
        assert cap.exists() and lint.exists() and lint.read_text().startswith("PASS"), f"caption for {a.id} not PASS"
        entry["caption_file"] = f"build/captions/{a.id}.clean.txt"
        entry.update(ground=a.ground, grid_position=a.pos)
    entry.update(ai_generated=(a.type == "reel" and not a.silent), published_id=None, attempts=0, last_error=None)

    manifest = json.loads((ROOT / "posts.json").read_text())
    for p in manifest["posts"]:
        if p["id"] == a.id and p.get("published_id"):
            raise SystemExit(f"{a.id} is already published ({p['published_id']}); refusing to replace it")
    manifest["posts"] = [p for p in manifest["posts"] if p["id"] != a.id] + [entry]
    manifest["posts"].sort(key=lambda p: p["scheduled_utc"])
    (ROOT / "posts.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(f"queued {a.id} {a.type} at {local:%a %d %b %H:%M} ET = {when}")


if __name__ == "__main__":
    main()
