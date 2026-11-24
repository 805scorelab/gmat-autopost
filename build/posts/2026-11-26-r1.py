"""Reel 2026-11-26-r1, series Shortcut: units digit of 7^23. Quant. Voiced, score v1.

Original question for 805 Score Lab: what is the units digit of 7^23? (A) 1 (B) 3 (C) 7 (D) 9 (E) 0.
Answer B, verified in build/items/2026-11-26-r1.py. Units digits of powers of 7 cycle 7, 9, 3, 1 (length 4);
23 = 4 x 5 + 3, so 7^23 ends like 7^3 = 343: 3. Trap: C, assuming every power of 7 ends in 7.
Difficulty: our estimate, easy to medium.
Quality-log improvement applied (last row: "show the picture's first state at frame 0"): every beat's main picture is
on screen at its first frame (the hook's power and bubbles, the first power row, the empty 4-column grid); only the
later parts animate in.
Usage: python3 posts/2026-11-26-r1.py
"""
import json
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import bubbles
from reel import Beat, build
from reelkit import COUNTDOWN, MINT, RED, choice_list, cover, save_beat_scene

ID = "2026-11-26-r1"
CHOICES = [("A", "1"), ("B", "3"), ("C", "7"), ("D", "9"), ("E", "0")]
CYCLE = [7, 9, 3, 1]
assert [pow(7, k) % 10 for k in range(1, 9)] == CYCLE * 2 and 23 % 4 == 3 and pow(7, 23) % 10 == 3

HOOK = ('<div class=big style="font-size:240px">7<sup style="font-size:120px">23</sup></div>'
        '<div class=mid style="margin-top:30px">ends in what digit?</div>'
        '<div class="mid a" style="margin-top:30px;color:#999;font-size:60px;animation:in .4s 2.2s both">'
        'No calculator.</div>'
        f'<div style="margin-top:70px">{bubbles()}</div>')


def powers():
    """7^1..7^5 with their last digit lit; row 1 is there at frame 0, the rest drop in."""
    rows = ""
    for k in range(1, 6):
        v = str(pow(7, k))
        d = 0 if k == 1 else 0.3 + (k - 1) * 0.75
        anim = "" if k == 1 else f"animation:in .35s {d:.2f}s both"
        col = MINT if k < 5 else "#ffd166"
        rows += (f'<div class=a style="display:flex;justify-content:space-between;margin-top:18px;{anim}">'
                 f'<span>7<sup style="font-size:50px">{k}</sup></span>'
                 f'<span>{v[:-1]}<span style="color:{col}">{v[-1]}</span></span></div>')
    return ('<div class="mid">Watch the last digit.</div>'
            f'<div style="font:800 100px Montserrat;margin-top:30px">{rows}</div>'
            '<p class=a style="margin-top:40px;font-size:56px;color:#ffd166;animation:in .4s 3.8s both">'
            '7 again: the cycle repeats.</p>')


def grid():
    """Four columns labelled 7 9 3 1; 23 cells fill row by row; the 23rd lands under the 3."""
    w, gap = 170, 22
    head = "".join(f'<div style="width:{w}px;text-align:center;font:800 90px Montserrat;color:{MINT}">{c}</div>'
                   for c in CYCLE)
    cells = ""
    for i in range(23):
        last = i == 22
        bg = "#ffd166" if last else "#2a2a2a"
        d = 0.3 + i * 0.09
        cells += (f'<div class=a style="width:{w}px;height:70px;border-radius:14px;background:{bg};'
                  f'display:flex;align-items:center;justify-content:center;font:800 40px Montserrat;color:#000;'
                  f'animation:pop .25s {d:.2f}s both">{"23rd" if last else ""}</div>')
    return ('<div class=mid style="font-size:68px">Cycle of 4 · 23 ÷ 4</div>'
            f'<div style="display:flex;gap:{gap}px;margin-top:40px">{head}</div>'
            f'<div style="display:grid;grid-template-columns:repeat(4,{w}px);gap:{gap}px;margin-top:20px">{cells}</div>'
            '<p class=a style="margin-top:40px;font-size:58px;animation:in .4s 2.7s both">'
            '23 = 4 × 5 + <span class=mint>3</span> → 3 steps in</p>')


beats = [
    Beat("What is the last digit of seven to the power twenty-three? No calculator.", HOOK, sfx=[("pop", 2.2)]),
    Beat("Pick one.", '<div class="mid a" style="animation:in .4s both">Pick one</div>'
         + choice_list(CHOICES, font="800 80px Montserrat", gap=26),
         sfx=[("pop", t) for t in (0, .18, .36, .54, .72)], min_len=2.0),
    Beat("Three seconds.", COUNTDOWN, sfx=[("tick", 0.0), ("tick", 1.0), ("tick", 2.0)], min_len=3.2),
    Beat("Don't multiply it out. Watch the last digit. Seven, nine, three, one. Then seven again.",
         powers(), sfx=[("pop", 1.05), ("pop", 1.8), ("pop", 2.55), ("thump", 3.3)], min_len=4.4),
    Beat("The cycle is four long. Twenty-three divided by four leaves three. So go three steps into the cycle.",
         grid(), sfx=[("pop", 0.3), ("ding", 2.3)], min_len=4.0),
    Beat("Three steps in lands on three. Seven to the power twenty-three ends in three. Pick B.",
         '<div class="big a" style="font-size:104px;animation:in .4s both">Answer: <span class=mint>B</span></div>'
         + choice_list(CHOICES, highlight="B", animate=False, font="800 80px Montserrat", gap=26),
         sfx=[("ding", 1.8)]),
    Beat("The trap is C. Seven comes back as the last digit only once every four powers.",
         '<div class="big a" style="font-size:104px;animation:in .4s both">Trap: <span class=mint>C</span></div>'
         '<div style="display:flex;gap:26px;margin-top:60px;font:800 110px Montserrat">'
         + "".join(f'<span class=a style="color:{"#fff" if c == 7 else "#555"};animation:pop .35s {0.5 + i * .3:.2f}s both">'
                   f'{c}</span>' for i, c in enumerate(CYCLE * 2))
         + '</div><p class=a style="margin-top:50px;animation:in .4s 3.0s both">7 shows up at powers 1, 5, 9, 13 …'
         ' never at 23.</p>', sfx=[("thump", 0.5)]),
    Beat("Save this for your next last digit question.", save_beat_scene("B"), sfx=[("pop", 0.1)], pad_after=0.6),
]

COVER = cover("forest", "Shortcut", "7<sup style=\"font-size:70px\">23</sup> ends in?<br>No calculator.", 124)

if __name__ == "__main__":
    res = build(ID, beats, COVER, voiced=True, seed=83)
    print(json.dumps({k: v for k, v in res["measures"].items() if k != "takes"}, default=float))
