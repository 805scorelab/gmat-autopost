"""Reel 2026-11-29-r2, series Meme: Data Sufficiency, expectation vs reality. Voiced, score v1, v2 style.

Weekly plan (docs/daily/daily-run.md 0.5): Sunday 21:00 Reel = meme. Replaces the earlier DS Reel queued in this slot
(percent increase), which was built before the v2 standard and the weekly plan.
Original meme format drawn by us (split panel, chat bubbles, simple shape faces). No meme images, no real people,
no characters, no logos. Nobody is mocked for a score.
Takeaway (useful and true): Data Sufficiency asks whether the value CAN be found, not what it is. Example on screen:
(1) x + y = 10 and (2) 2x + 2y = 20 are the same equation, so (2) adds nothing (checked below).
Quality-log next step applied (29-r2 row: motion 0.19, trim the hook line): every scene has a looping element
(spinning clock hand, scribble lines, typing dots), and the hook line is 6 words.
Usage: python3 posts/2026-11-29-r2.py
"""
import json
import sys
import pathlib
from fractions import Fraction
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from reel import Beat, build
from reelkit import MINT, RED, cover, follow_card, strike

ID = "2026-11-29-r2"
GOLD = "#ffd166"
BLUE = "#7aa7ff"

# (2) is (1) doubled: every (x, y) on one line is on the other, so (2) adds no information.
assert all((2 * x + 2 * y == 20) == (x + y == 10) for x in range(-30, 31) for y in range(-30, 31))
assert Fraction(20, 2) == 10

CSS = ('<style>@keyframes spinh{from{transform:rotate(0)}to{transform:rotate(360deg)}}'
       '@keyframes scrib{from{stroke-dashoffset:900}to{stroke-dashoffset:0}}'
       '@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-14px)}}'
       '@keyframes sweat{0%{transform:translateY(0);opacity:1}100%{transform:translateY(60px);opacity:0}}'
       '@keyframes dots{0%,100%{opacity:.25}50%{opacity:1}}</style>')


def face(calm=True, size=230, delay=0.0):
    """Our own simple face: calm (smile) or stressed (wavy mouth, sweat drop)."""
    mouth = ('<path d="M70 135 q30 26 60 0" stroke="#111" stroke-width="9" fill="none" stroke-linecap="round"/>'
             if calm else
             '<path d="M62 140 q12 -14 24 0 t24 0 t24 0" stroke="#111" stroke-width="9" fill="none" '
             'stroke-linecap="round"/>')
    drop = ('' if calm else
            f'<path class=a d="M160 40 q12 20 0 30 q-12 -10 0 -30z" fill="{BLUE}" '
            f'style="animation:sweat 1.2s {delay:.2f}s linear infinite both"/>')
    col = MINT if calm else GOLD
    return (f'<svg class=a width="{size}" height="{size}" viewBox="0 0 200 200" '
            f'style="animation:bob 2s {delay:.2f}s ease-in-out infinite both">'
            f'<circle cx="100" cy="100" r="90" fill="{col}"/><circle cx="70" cy="85" r="10" fill="#111"/>'
            f'<circle cx="130" cy="85" r="10" fill="#111"/>{mouth}{drop}</svg>')


def clock(seconds_label, fast=False, size=230, delay=0.0):
    speed = "0.6s" if fast else "6s"
    return (f'<div style="display:flex;align-items:center;gap:24px">'
            f'<svg width="{size}" height="{size}" viewBox="0 0 200 200"><circle cx="100" cy="100" r="86" '
            f'stroke="#fff" stroke-width="12" fill="none"/>'
            f'<g class=a style="transform-origin:100px 100px;animation:spinh {speed} {delay:.2f}s linear infinite both">'
            f'<line x1="100" y1="100" x2="100" y2="34" stroke="{RED if fast else MINT}" stroke-width="12" '
            f'stroke-linecap="round"/></g></svg>'
            f'<span style="font:800 120px Montserrat;color:{RED if fast else MINT}">{seconds_label}</span></div>')


def scribbles(delay=0.4, rows=5):
    paths = "".join(
        f'<path class=a d="M10 {30 + i * 60} q40 -30 80 0 t80 0 t80 0 t80 0 t80 0 t80 0 t80 0 t80 0" stroke="#bbb" '
        f'stroke-width="7" fill="none" stroke-dasharray="900" '
        f'style="animation:scrib 1s {delay + i * 0.35:.2f}s linear both"/>' for i in range(rows))
    return f'<svg width="760" height="{40 + rows * 60}" viewBox="0 0 860 {40 + rows * 60}">{paths}</svg>'


def panel(title, body, col, delay=0.0):
    return (f'<div class=a style="border:4px solid {col};border-radius:30px;padding:26px 30px;margin-top:24px;'
            f'animation:in .4s {delay:.2f}s both"><div style="font:800 70px Montserrat;color:{col}">{title}</div>'
            f'{body}</div>')


def bubble(who, text, side, delay, col="#262626", tcol="#fff"):
    al = "flex-start" if side == "l" else "flex-end"
    return (f'<div class=a style="display:flex;flex-direction:column;align-items:{al};margin-top:40px;'
            f'animation:in .4s {delay:.2f}s both"><div style="font:700 44px Inter;color:#999;margin:0 18px 8px">{who}'
            f'</div><div style="background:{col};color:{tcol};border-radius:34px;padding:24px 36px;'
            f'font:800 84px Montserrat">{text}</div></div>')


HOOK = (CSS + '<span class=chip style="font-size:40px">Meme · Data Sufficiency</span>'
        '<div class=big style="font-size:104px;margin-top:26px">Expectation<br>vs <span style="color:#ff6b6b">'
        'reality</span></div>'
        '<div style="display:flex;justify-content:space-around;align-items:center;margin-top:70px">'
        + face(True, 330) + '<span style="font:800 90px Montserrat;color:#666">vs</span>'
        + face(False, 330, 0.3) + '</div>')

EXPECT = (CSS + panel("Expectation", '<div style="display:flex;align-items:center;gap:30px;margin-top:20px">'
                      + face(True, 250) + '<div style="font:700 60px/1.3 Inter">"Is it enough?<br>Yes. Next."</div>'
                      '</div><div style="margin-top:24px">' + clock("0:30") + '</div>', MINT))

REALITY = (CSS + panel("Reality", '<div style="display:flex;align-items:center;gap:30px;margin-top:20px">'
                       + face(False, 250) + '<div style="font:700 56px/1.3 Inter">"Let me just find<br>x to 4 decimals."'
                       '</div></div>' + scribbles(0.5, 4)
                       + '<div style="margin-top:10px">' + clock("3:00", fast=True, delay=0.2) + '</div>', RED))

CHAT = (CSS + '<div class="mid a" style="animation:in .4s both">Meanwhile, the statements:</div>'
        + bubble("Statement (1)", "x + y = 10", "l", 0.5)
        + bubble("Statement (2)", "2x + 2y = 20", "r", 1.6, GOLD, "#111")
        + '<div class=a style="margin-top:30px;font:800 64px Montserrat;color:#ff6b6b;font-size:80px;animation:pop .4s 3.0s both">'
          'Same line.<br>Zero new info.</div>'
        + '<div style="display:flex;gap:14px;margin-top:30px">' + "".join(
            f'<span class=a style="width:26px;height:26px;border-radius:50%;background:#999;'
            f'animation:dots 1s {i * 0.2:.1f}s infinite both"></span>' for i in range(3)) + '</div>')

TAKEAWAY = (CSS + '<div class="big a" style="font-size:96px;animation:in .4s both">DS asks:</div>'
            '<div class=a style="margin-top:40px;font:800 100px Montserrat;animation:pop .4s .8s both">'
            '<span class=mint>Can</span> it be<br>found?</div>'
            '<div style="margin-top:40px;font:800 100px Montserrat;color:#888"><span class=a style="position:relative;'
            'animation:in .4s 1.8s both">What is it?' + strike(2.4, 12) + '</span></div>'
            '<div class=a style="margin-top:60px;animation:in .4s 3.2s both">' + clock("Stop early", delay=3.2)
            + '</div>')

beats = [
    Beat("Data Sufficiency. What you expect, and what really happens.", HOOK, sfx=[("pop", 0.3)], min_len=2.4),
    Beat("Expectation: you check if the information is enough, then move on.", EXPECT,
         sfx=[("pop", 0.2)]),
    Beat("Reality: you solve the whole thing, down to the last decimal, and lose a lot of time.", REALITY,
         sfx=[("pop", 0.2), ("thump", 2.6)]),
    Beat("Meanwhile, statement two is just statement one, doubled. Same line, no new information.", CHAT,
         sfx=[("pop", 0.5), ("pop", 1.6), ("thump", 3.0)]),
    Beat("The fix: Data Sufficiency asks if the value can be found, not what it is. Stop the moment you know.",
         TAKEAWAY, sfx=[("pop", 0.8), ("thump", 2.4), ("ding", 3.2)]),
    Beat("Follow for a new question every day.", follow_card(), sfx=[("pop", 0.6), ("ding", 2.3)], pad_after=1.2),
]

COVER = cover("mint", "Meme", "DS: expectation<br>vs reality", 116)

if __name__ == "__main__":
    res = build(ID, beats, COVER, voiced=True, seed=139)
    print(json.dumps({k: v for k, v in res["measures"].items() if k != "takes"}, default=float))
