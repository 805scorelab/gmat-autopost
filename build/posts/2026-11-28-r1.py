"""Reel 2026-11-28-r1, series Trap Answer: which number was removed from an average? Quant. Voiced, score v1.

Original question for 805 Score Lab: the average of 5 numbers is 12. One number is removed and the average of the
other 4 is 10. Which number was removed? (A) 2 (B) 10 (C) 12 (D) 20 (E) 22.
Answer D, verified in build/items/2026-11-28-r1.py. Sum of 5 = 5 x 12 = 60, sum of 4 = 4 x 10 = 40, removed = 20.
Trap: A (2), the drop in the average.
Difficulty: our estimate, easy to medium.
Quality-log improvements applied (previous rows: longest static 1.17 s in the check beat; frame-0 picture small):
tiles fill the full width at frame 0, and the answer beat has a total bar that shrinks from 60 to 40 while the gap
counts up, so no beat holds still.
v2 upgrade (27 Nov, owner standard of 26 Nov): 20 s solving beat with think_scene replaces the 3 s countdown,
follow_card ends the Reel, lit tiles use fixed dark text instead of mix-blend (quality-log next step).
Usage: python3 posts/2026-11-28-r1.py
"""
import json
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import bubbles
from reel import Beat, build
from reelkit import MINT, RED, choice_list, cover, follow_card, strike, think_scene

ID = "2026-11-28-r1"
CHOICES = [("A", "2"), ("B", "10"), ("C", "12"), ("D", "20"), ("E", "22")]
assert 5 * 12 - 4 * 10 == 20 and 12 - 10 == 2
GOLD = "#ffd166"


def tiles(values, start=None, step=0.45, lift=None, col=MINT, size=150):
    """A full-width row of number tiles on screen at frame 0; each lights in turn from `start`. `lift`: index of a
    tile that floats up and fades to a question mark."""
    out = ""
    for i, v in enumerate(values):
        light = ""
        if start is not None:
            light = (f'<div class=a style="position:absolute;inset:0;border-radius:24px;background:{col};'
                     f'animation:pop .3s {start + i * step:.2f}s both"></div>')
        anim = f"animation:liftq .8s {lift[1]:.2f}s both;" if lift and i == lift[0] else ""
        out += (f'<div class=a style="position:relative;width:{size}px;height:{int(size * 1.2)}px;border-radius:24px;'
                f'background:#222;display:flex;align-items:center;justify-content:center;font:800 84px Montserrat;'
                f'{anim}">{light}<span class=a style="position:relative;color:#fff;{f"animation:darktxt .3s {start + i * step:.2f}s both" if start is not None else ""}">{v}</span></div>')
    return ('<style>@keyframes darktxt{from{color:#fff}to{color:#06142B}}@keyframes liftq{from{transform:none}to{transform:translateY(-70px);'
            'box-shadow:0 0 0 8px #ffd166}}</style>'
            f'<div style="display:flex;gap:22px;margin-top:40px">{out}</div>')


def counter(vals, start, step, color=MINT, size=130, label=""):
    """A number that counts through vals, one value per step, ending on the last."""
    spans = ""
    for i, v in enumerate(vals):
        d = start + i * step
        last = i == len(vals) - 1
        anim = f"animation:show {step:.2f}s {d:.2f}s both" if not last else f"animation:pop .35s {d:.2f}s both"
        spans += f'<span class=a style="position:absolute;left:0;{anim}">{v}</span>'
    return ('<style>@keyframes show{0%{opacity:0}1%,99%{opacity:1}100%{opacity:0}}</style>'
            f'<div style="display:flex;align-items:baseline;gap:26px;margin-top:50px;font:800 {size}px Montserrat">'
            f'<span style="color:#999;font-size:70px">{label}</span>'
            f'<span style="position:relative;display:inline-block;width:300px;height:{size + 10}px;color:{color}">'
            f'{spans}</span></div>')


HOOK = ('<div class=big style="font-size:96px">5 numbers.<br>Average <span class=mint>12</span>.</div>'
        + tiles(["?"] * 5, lift=(4, 3.2))
        + '<div class="mid a" style="margin-top:50px;font-size:66px;animation:in .4s 3.2s both">Remove 1.<br>'
          'The other 4 average <span style="color:#ffd166">10</span>.</div>'
        + '<div class="mid a" style="margin-top:30px;font-size:66px;animation:in .4s 5.6s both">Which one left?</div>'
        + f'<div style="margin-top:40px">{bubbles()}</div>')

QUESTION_SMALL = (
    '<div style="font:700 46px/1.3 Inter">Average of 5 numbers: <span class=mint>12</span>.<br>'
    'Remove 1. Average of the other 4: <span style="color:#ffd166">10</span>.<br>'
    '<b>Which number was removed?</b></div>'
    + choice_list(CHOICES, animate=False, font="800 52px Montserrat", gap=2))

beats = [
    Beat("Five numbers average twelve. Remove one, and the other four average ten. Which number did you remove?",
         HOOK, sfx=[("pop", 3.2), ("pop", 5.6)]),
    Beat("Pick one.", '<div class="mid a" style="animation:in .4s both">Pick one</div>'
         + choice_list(CHOICES, font="800 80px Montserrat", gap=26),
         sfx=[("pop", t) for t in (0, .18, .36, .54, .72)], min_len=2.0),
    Beat("You have twenty seconds. Go.", think_scene(QUESTION_SMALL, 20, delay=1.6), think=20),
    Beat("An average hides a total. Five numbers at twelve each make sixty.",
         '<div class=mid>Turn the average into a total.</div>' + tiles([12] * 5, start=1.4, step=0.4)
         + counter([12, 24, 36, 48, 60], 1.55, 0.4, label="total"),
         sfx=[("pop", 1.4 + 0.4 * i) for i in range(5)], min_len=4.0),
    Beat("Four numbers at ten each make forty.",
         '<div class=mid>Same for the 4 left.</div>' + tiles([10] * 4, start=0.6, step=0.4, col=GOLD)
         + counter([10, 20, 30, 40], 0.75, 0.4, color=GOLD, label="total"),
         sfx=[("pop", 0.6 + 0.4 * i) for i in range(4)], min_len=2.8),
    Beat("Sixty minus forty leaves twenty. That is the number you removed. So pick D.",
         '<style>@keyframes shrink{from{width:840px}to{width:560px}}</style>'
         '<div class=mid>The gap is the number.</div>'
         '<div style="position:relative;width:840px;height:130px;margin-top:50px;border-radius:20px;background:#2a2a2a">'
         f'<div class=a style="position:absolute;left:0;top:0;bottom:0;border-radius:20px;background:{GOLD};'
         'animation:shrink 1.6s .4s both"></div>'
         '<span style="position:absolute;left:30px;top:30px;font:800 70px/1 Montserrat;color:#000">40</span>'
         '<span class=a style="position:absolute;right:40px;top:30px;font:800 70px/1 Montserrat;color:#BFFBD1;'
         'animation:pop .4s 2.0s both">20</span></div>'
         '<div style="font:700 50px Inter;color:#999;margin-top:16px">total of 5 = 60</div>'
         '<div class="big a" style="font-size:100px;margin-top:50px;animation:pop .45s 2.6s both">'
         '60 − 40 = <span class=mint>20</span></div>'
         '<div class=a style="margin-top:50px;animation:in .4s 3.6s both">'
         + bubbles("D") + '</div>',
         sfx=[("pop", 2.0), ("ding", 2.6)]),
    Beat("The trap is answer A. Two is how far the average dropped, not the number you removed.",
         '<div class="big a" style="font-size:104px;animation:in .4s both">Trap: <span class=mint>A</span></div>'
         '<div style="font:800 130px Montserrat;margin-top:60px"><span style="position:relative">12 − 10 = 2'
         + strike(1.4, 12) + '</span></div>'
         '<p class=a style="margin-top:40px;font-size:58px;animation:in .4s 1.0s both">That is the drop in the average.</p>'
         '<p class=a style="margin-top:14px;font-size:58px;animation:in .4s 2.6s both">Compare <span class=mint>totals'
         '</span>, not averages.</p>', sfx=[("thump", 1.4)]),
    Beat("Follow for a new question every day.", follow_card("D"), sfx=[("pop", 0.6), ("ding", 2.3)],
         pad_after=1.2),
]

COVER = cover("mint", "Trap Answer", "Average 12.<br>Remove 1.<br>Which one?", 118)

if __name__ == "__main__":
    res = build(ID, beats, COVER, voiced=True, seed=103)
    print(json.dumps({k: v for k, v in res["measures"].items() if k != "takes"}, default=float))
