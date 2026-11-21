"""Caption lint: five checks scored 0 to 100. Ships only on PASS: overall 70+, no check under 55, no hard rule broken.

    python3 build/caption_lint.py build/captions/<id>.clean.txt     (writes <id>.lint.txt next to it)

Checks
  slop         AI-cliche vocabulary ("delve", "unlock", "game-changer", ...)
  characters   em/en dashes, invisible characters, curly-quote mixes
  specificity  digits and proper nouns per sentence ("3 steps", not "three steps"; "20 times", not "20x")
  burstiness   variation in sentence length (re-lint after every edit: evening lengths drops this)
  structure    formulaic patterns ("Here's the thing", "Let's dive in", emoji bullets, "In conclusion")
Hard rules (any one fails the caption): line 1 within 125 characters and not a greeting/hashtag/emoji; at most 5
hashtags and none of #viral #fyp #explorepage; no link; no engagement bait; no score guarantees; no em dash;
the non-affiliation line present; at most one ask.
"""
import re
import statistics
import sys

SLOP = ["delve", "unlock", "unleash", "game-changer", "game changer", "elevate", "embark", "journey", "realm",
        "tapestry", "navigate the", "in today's", "fast-paced", "seamless", "leverage", "supercharge", "boost your",
        "master the art", "crucial", "essential to note", "it's important to note", "dive into", "deep dive",
        "transformative", "empower", "testament", "landscape", "ever-evolving", "skyrocket", "next level",
        "level up", "secret sauce", "mind-blowing", "hack"]
FORMULAIC = [r"here'?s the thing", r"let'?s dive", r"in conclusion", r"buckle up", r"ready to", r"^\s*[-*•✅🔥👉]",
             r"not only .* but also", r"whether you'?re", r"look no further", r"the best part\??"]
BAIT = [r"tag a friend", r"follow for more", r"like and share", r"comment below if", r"smash", r"link in bio"]
GUARANTEE = [r"\b(7\d\d|8\d\d)\+", r"guarantee", r"in \d+ days", r"boost your score by"]
BANNED_TAGS = {"#viral", "#fyp", "#explorepage", "#foryou", "#foryoupage"}
ASKS = [r"\bsave (it|this)\b", r"\bcomment (your|the) (answer|letter)", r"\bshare (it|this)\b", r"\bfollow\b"]


def sentences(text):
    body = "\n".join(l for l in text.splitlines() if not l.strip().startswith("#"))
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", body) if len(s.strip()) > 2]


def lint(text):
    hard, scores = [], {}
    lines = [l for l in text.splitlines()]
    first = lines[0] if lines else ""
    if len(first) > 125:
        hard.append(f"line 1 is {len(first)} characters (max 125): {first[:125]!r}")
    if re.match(r"^\s*(hi|hello|hey|#|[\U0001F300-\U0001FAFF])", first, re.I):
        hard.append("line 1 starts with a greeting, hashtag or emoji")
    tags = re.findall(r"#\w+", text)
    if len(tags) > 5:
        hard.append(f"{len(tags)} hashtags (max 5)")
    if BANNED_TAGS & {t.lower() for t in tags}:
        hard.append("banned hashtag")
    if re.search(r"https?://|www\.", text):
        hard.append("link in caption")
    for pattern in BAIT:
        if re.search(pattern, text, re.I):
            hard.append(f"engagement bait: {pattern}")
    for pattern in GUARANTEE:
        if re.search(pattern, text, re.I):
            hard.append(f"score guarantee: {pattern}")
    if "Not affiliated with GMAC" not in text:
        hard.append("missing 'Independent. Not affiliated with GMAC.'")
    asks = sum(bool(re.search(p, text, re.I)) for p in ASKS)
    if asks > 1:
        hard.append(f"{asks} different asks (max 1)")

    low = text.lower()
    hits = [w for w in SLOP if w in low]
    scores["slop"] = max(0, 100 - 25 * len(hits))
    bad_chars = re.findall(r"[—–​‌‍⁠﻿]", text)
    if any(c in "—–" for c in bad_chars):
        hard.append("em or en dash")
    scores["characters"] = max(0, 100 - 30 * len(bad_chars))
    sents = sentences(text)
    specific = sum(bool(re.search(r"\d|\b[A-Z][a-z]+\b(?<!^)", s[1:])) for s in sents)
    if re.search(r"\b\d+x\b", text):
        hard.append("write '20 times', not '20x'")
    scores["specificity"] = min(100, round(100 * specific / max(len(sents), 1) * 1.4))
    lengths = [len(s.split()) for s in sents]
    if len(lengths) >= 3:
        cv = statistics.pstdev(lengths) / max(statistics.mean(lengths), 1)
        scores["burstiness"] = min(100, round(cv * 160))
    else:
        scores["burstiness"] = 50
    form = sum(bool(re.search(p, text, re.I | re.M)) for p in FORMULAIC)
    scores["structure"] = max(0, 100 - 30 * form)
    overall = round(sum(scores.values()) / len(scores))
    ok = not hard and overall >= 70 and min(scores.values()) >= 55
    return ok, overall, scores, hard, hits


if __name__ == "__main__":
    path = sys.argv[1]
    text = open(path, encoding="utf-8").read().strip()
    ok, overall, scores, hard, hits = lint(text)
    report = [f"{'PASS' if ok else 'FAIL'} overall {overall}", f"line 1 (125): {text.splitlines()[0][:125]!r}"]
    report += [f"  {k}: {v}" for k, v in scores.items()]
    report += [f"  HARD: {h}" for h in hard] + ([f"  slop words: {hits}"] if hits else [])
    print("\n".join(report))
    out = re.sub(r"\.clean\.txt$|\.txt$", "", path) + ".lint.txt"
    open(out, "w").write("\n".join(report) + "\n")
    sys.exit(0 if ok else 1)
