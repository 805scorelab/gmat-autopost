"""Verify the queue before pushing. Prints problems and exits 1 if there are any.

Checks: at most 2 carousels, 2 reels, 1 story and 5 posts per Eastern day; every media file exists (reels: on their
branch, checked by git ls-remote); every caption is lint PASS; every voiced reel has ai_generated true; no {{ }}
placeholder or em dash in any queued caption; no two unpublished posts share a caption opening (duplicate guard);
grid positions of feed posts follow the forest, paper, mint cycle in publish order.
"""
import json
import pathlib
import subprocess
import sys
from collections import Counter
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parents[1]
EASTERN = ZoneInfo("America/New_York")
CAP = {"carousel": 2, "reel": 2, "story": 1}
CYCLE = ("forest", "paper", "mint")


def main():
    m = json.loads((ROOT / "posts.json").read_text())
    problems, per_day, heads = [], Counter(), {}
    branches = subprocess.run(["git", "-C", str(ROOT), "ls-remote", "--heads", "origin", "media/*"],
                              capture_output=True, text=True).stdout
    for p in m["posts"]:
        day = datetime.fromisoformat(p["scheduled_utc"].replace("Z", "+00:00")).astimezone(EASTERN).date()
        per_day[(day, p["type"])] += 1
        per_day[(day, "all")] += 1
        if p.get("published_id"):
            continue
        if p["type"] in ("carousel", "story"):
            for f in p["media"]:
                if not (ROOT / "media" / f).exists():
                    problems.append(f"{p['id']}: missing media/{f}")
        else:
            if f"refs/heads/{p['media_branch']}" not in branches:
                problems.append(f"{p['id']}: branch {p['media_branch']} not on origin")
            if p.get("audio") != "silent" and not p.get("ai_generated"):
                problems.append(f"{p['id']}: voiced reel without ai_generated")
        if p["type"] != "story":
            cap = (ROOT / p["caption_file"]).read_text()
            lint = ROOT / p["caption_file"].replace(".clean.txt", ".lint.txt")
            if not lint.exists() or not lint.read_text().startswith("PASS"):
                problems.append(f"{p['id']}: caption lint not PASS")
            if "{{" in cap or "—" in cap or "–" in cap:
                problems.append(f"{p['id']}: placeholder or dash in caption")
            head = cap.strip()[:90]
            if head in heads:
                problems.append(f"{p['id']}: same caption opening as {heads[head]} (duplicate)")
            heads[head] = p["id"]
    for (day, kind), n in per_day.items():
        limit = 5 if kind == "all" else CAP[kind]
        if n > limit:
            problems.append(f"{day}: {n} {kind} posts (max {limit})")
    feed = [p for p in m["posts"] if p["type"] != "story" and p.get("grid_position")]
    for p in feed:
        want = CYCLE[(p["grid_position"] - 1) % 3]
        if p.get("ground") != want:
            problems.append(f"{p['id']}: grid position {p['grid_position']} needs {want}, has {p.get('ground')}")
    positions = [p["grid_position"] for p in sorted(feed, key=lambda p: p["scheduled_utc"])]
    if positions != sorted(positions) or len(set(positions)) != len(positions):
        problems.append(f"grid positions out of order: {positions}")
    print("\n".join(problems) if problems else "manifest OK")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
