"""Reel 2026-11-30-r1, series Trap Answer: multiples of 3 or 5 from 1 to 100 (overlap counted once). Quant.
Voiced, score v1, v2 style.

Original question for 805 Score Lab: how many integers from 1 to 100, inclusive, are multiples of 3 or 5?
(A) 41 (B) 47 (C) 53 (D) 59 (E) 67. Answer B, verified in build/items/2026-11-30-r1.py.
Solve: 33 multiples of 3, 20 multiples of 5, 6 multiples of both (15, 30, 45, 60, 75, 90): 33 + 20 - 6 = 47.
Trap: C (53), adding 33 + 20 and counting the six shared numbers twice.
Difficulty: our estimate, medium.
Quality-log next step applied (29-r1 row: think_scene question text small next to big choices): choices sit in a
two-column grid so the question text can be 56 px. The 1 to 100 grid fills the zone width and is on screen at frame 0.
Usage: python3 posts/2026-11-30-r1.py
"""
import json
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import bubbles
from reel import Beat, build
from reelkit import MINT, RED, choice_list, cover, follow_card, strike, think_scene

ID = "2026-11-30-r1"
CHOICES = [("A", "41"), ("B", "47"), ("C", "53"), ("D", "59"), ("E", "67")]
GOLD = "#ffd166"
BLUE = "#7aa7ff"
M3 = [n for n in range(1, 101) if n % 3 == 0]
M5 = [n for n in range(1, 101) if n % 5 == 0]
BOTH = [n for n in range(1, 101) if n % 15 == 0]
assert (len(M3), len(M5), len(BOTH)) == (33, 20, 6) and 33 + 20 - 6 == 47 == len(set(M3) | set(M5))


def grid(lit=None, pulse=(), cell=80, gap=6, sweep=False):
    """The numbers 1 to 100 in a 10 x 10 grid. lit: {n: (colour, delay)} cells that fill one by one (fixed dark text
    when lit). pulse: cells that keep pulsing (the double-counted ones). sweep: a soft highlight sweeping the rows
    (frame-0 motion for the hook)."""
    lit = lit or {}
    css = ('<style>@keyframes pz{0%,100%{transform:scale(1)}50%{transform:scale(1.18)}}'
           '@keyframes sw{0%{top:0%}100%{top:88%}}</style>')
    cells = ""
    for n in range(1, 101):
        if n in lit:
            col, d = lit[n]
            pz = f",pz .9s {d + 0.4:.2f}s ease-in-out infinite" if n in pulse else ""
            cells += (f'<div class=a style="position:relative;width:{cell}px;height:{cell}px;border-radius:14px;'
                      f'background:{col};color:#111;display:flex;align-items:center;justify-content:center;'
                      f'font:800 34px Montserrat;animation:pop .3s {d:.2f}s both{pz}">{n}</div>')
        else:
            cells += (f'<div style="width:{cell}px;height:{cell}px;border-radius:14px;background:#232323;color:#bbb;'
                      f'display:flex;align-items:center;justify-content:center;font:700 32px Inter">{n}</div>')
    sw = ('<div class=a style="position:absolute;left:0;right:0;height:12%;border-radius:20px;'
          'background:rgba(191,251,209,.18);animation:sw 3s linear infinite both"></div>') if sweep else ""
    return (css + f'<div style="position:relative;overflow:hidden;display:grid;grid-template-columns:repeat(10,{cell}px);gap:{gap}px">'
            f'{cells}{sw}</div>')


def staged(nums, col, start, step):
    return {n: (col, start + i * step) for i, n in enumerate(nums)}


def counter(vals, start, step, color=MINT, size=110, label=""):
    spans = ""
    for i, v in enumerate(vals):
        last = i == len(vals) - 1
        anim = (f"animation:show {step:.2f}s {start + i * step:.2f}s both" if not last
                else f"animation:pop .35s {start + i * step:.2f}s both")
        spans += f'<span class=a style="position:absolute;left:0;{anim}">{v}</span>'
    return ('<style>@keyframes show{0%{opacity:0}1%,99%{opacity:1}100%{opacity:0}}</style>'
            f'<div style="display:flex;align-items:baseline;gap:22px;font:800 {size}px Montserrat">'
            f'<span style="color:#999;font-size:56px">{label}</span>'
            f'<span style="position:relative;display:inline-block;width:200px;height:{size + 10}px;color:{color}">'
            f'{spans}</span></div>')


def two_col(choices, font="800 64px Montserrat"):
    cells = "".join(f'<div style="font:{font}">({k}) {v}</div>' for k, v in choices)
    return f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px 60px;margin-top:22px">{cells}</div>'


HOOK = ('<div class=big style="font-size:84px">1 to 100.<br>Multiples of<br><span class=mint>3</span> or '
        f'<span style="color:{BLUE}">5</span>?</div>'
        '<div style="margin-top:36px">' + grid(cell=70, gap=6, sweep=True) + '</div>')

QUESTION = ('<div style="font:700 56px/1.3 Inter">How many integers from 1 to 100, inclusive, are multiples of '
            '<b>3 or 5</b>?</div>' + two_col(CHOICES))

all3 = staged(M3, MINT, 1.0, 0.05)
all35 = dict(all3)
all35.update(staged(M5, BLUE, 0.6, 0.08))
for n in BOTH:
    all35[n] = (GOLD, all35[n][1])
both_only = {n: ((GOLD if n in BOTH else MINT if n % 3 == 0 else BLUE), 0.0) for n in set(M3) | set(M5)}

beats = [
    Beat("From one to one hundred, how many whole numbers divide evenly by three or by five?", HOOK,
         sfx=[("pop", 0.3)]),
    Beat("Pick one.", '<div class="mid a" style="animation:in .4s both">Pick one</div>'
         + choice_list(CHOICES, font="800 92px Montserrat", gap=24),
         sfx=[("pop", t) for t in (0, .18, .36, .54, .72)], min_len=2.0),
    Beat("You have twenty seconds. Go.", think_scene(QUESTION, 20, delay=1.6), think=20),
    Beat("Count the threes first. One hundred divided by three gives thirty-three.",
         '<div style="display:flex;justify-content:space-between;align-items:baseline">'
         '<div class=mid style="font-size:64px">Multiples of <span class=mint>3</span></div>'
         + counter([3, 9, 15, 21, 27, 33], 1.0, 0.3, label="") + '</div>'
         '<div style="margin-top:20px">' + grid(all3, cell=78) + '</div>',
         sfx=[("pop", 1.0), ("ding", 2.5)]),
    Beat("Now count the fives. That is twenty more.",
         '<div style="display:flex;justify-content:space-between;align-items:baseline">'
         f'<div class=mid style="font-size:64px">+ multiples of <span style="color:{BLUE}">5</span></div>'
         + counter([4, 8, 12, 16, 20], 0.6, 0.32, color=BLUE, label="") + '</div>'
         '<div style="margin-top:20px">' + grid({**{n: (MINT, 0.0) for n in M3}, **staged(M5, BLUE, 0.6, 0.08),
                                                 **{n: (GOLD, 0.6 + M5.index(n) * 0.08) for n in BOTH}}, cell=78)
         + '</div>', sfx=[("pop", 0.6), ("ding", 2.2)]),
    Beat("But the gold ones, like fifteen and thirty, were counted twice. There are six of them.",
         f'<div class=mid style="font-size:64px"><span style="color:{GOLD}">Counted twice</span>: 6</div>'
         '<div style="margin-top:20px">' + grid(both_only, pulse=BOTH, cell=78) + '</div>'
         '<div style="display:flex;gap:18px;margin-top:22px">'
         + "".join(f'<span class=a style="font:800 56px Montserrat;color:{GOLD};animation:pop .35s {1.2 + i * 0.3:.2f}s '
                   f'both">{n}</span>' for i, n in enumerate(BOTH)) + '</div>',
         sfx=[("pop", 1.2 + i * 0.3) for i in range(6)]),
    Beat("Thirty-three plus twenty, minus six, is forty-seven. So it is answer B.",
         '<div class="big a" style="font-size:112px;animation:in .4s both">'
         '<span class=mint>33</span> + <span style="color:#7aa7ff">20</span></div>'
         f'<div class="big a" style="font-size:112px;margin-top:20px;animation:in .4s 1.0s both">− <span style="color:{GOLD}">6</span>'
         ' = <span class=mint>47</span></div>'
         '<div class=a style="margin-top:60px;animation:in .4s 2.0s both">' + bubbles("B") + '</div>',
         sfx=[("pop", 1.0), ("ding", 2.0)]),
    Beat("The trap is answer C. Fifty-three counts the gold ones twice.",
         '<div class="big a" style="font-size:104px;animation:in .4s both">Trap: <span class=mint>C</span></div>'
         '<div style="font:800 120px Montserrat;margin-top:60px"><span style="position:relative">33 + 20 = 53'
         + strike(1.4, 12) + '</span></div>'
         f'<p class=a style="margin-top:40px;font-size:58px;animation:in .4s 1.8s both">15, 30, 45 ... sit in '
         f'<span style="color:{GOLD}">both</span> lists.</p>', sfx=[("thump", 1.4)]),
    Beat("Shortcut. When two groups overlap, add both, then take the overlap away once.",
         '<div class="mid a" style="animation:in .4s both">Shortcut</div>'
         '<svg width="760" height="420" viewBox="0 0 760 420" style="margin-top:30px">'
         f'<circle class=a cx="280" cy="210" r="190" fill="{MINT}" fill-opacity=".35" stroke="{MINT}" stroke-width="8" '
         'style="animation:pop .5s .3s both;transform-origin:280px 210px"/>'
         f'<circle class=a cx="480" cy="210" r="190" fill="{BLUE}" fill-opacity=".35" stroke="{BLUE}" stroke-width="8" '
         'style="animation:pop .5s .9s both;transform-origin:480px 210px"/>'
         f'<text x="170" y="230" font-family="Montserrat" font-weight="800" font-size="72" fill="#fff">33</text>'
         f'<text x="520" y="230" font-family="Montserrat" font-weight="800" font-size="72" fill="#fff">20</text>'
         f'<text class=a x="352" y="230" font-family="Montserrat" font-weight="800" font-size="72" fill="{GOLD}" '
         'style="animation:pop .4s 1.8s both;transform-origin:380px 210px">6</text></svg>'
         '<div class="mid a" style="font-size:64px;margin-top:30px;animation:in .4s 2.4s both">'
         'A + B − <span style="color:#ffd166">both</span></div>',
         sfx=[("pop", 0.3), ("pop", 0.9), ("ding", 1.8)]),
    Beat("Follow for a new question every day.", follow_card("B"), sfx=[("pop", 0.6), ("ding", 2.3)],
         pad_after=1.2),
]

COVER = cover("paper", "Trap Answer", "1 to 100.<br>Multiples of<br>3 or 5?", 116)

if __name__ == "__main__":
    res = build(ID, beats, COVER, voiced=True, seed=149)
    print(json.dumps({k: v for k, v in res["measures"].items() if k != "takes"}, default=float))
