"""Reel 2026-11-29-r1, series Trap Answer: price before a 20% discount. Quant. Voiced, score v1.

Original question for 805 Score Lab: after a 20% discount, a jacket costs $80. What was the price before the
discount? (A) $64 (B) $88 (C) $96 (D) $100 (E) $120.
Answer D, verified in build/items/2026-11-29-r1.py. $80 is 80% of the old price: four 20% blocks are $80, so each
block is $20 and five blocks are $100.
Trap: C ($96), adding 20% of the sale price (80 + 16) instead of working from the old price.
Difficulty: our estimate, easy to medium.
Quality-log improvements applied (previous rows: lit tiles with mix-blend text read blue; 43.7 s too long): lit
blocks use a fixed dark text colour, and the script is kept short (target about 35 s).
Usage: python3 posts/2026-11-29-r1.py
"""
import json
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import bubbles
from reel import Beat, build
from reelkit import COUNTDOWN, MINT, RED, choice_list, cover, save_beat_scene, strike

ID = "2026-11-29-r1"
CHOICES = [("A", "$64"), ("B", "$88"), ("C", "$96"), ("D", "$100"), ("E", "$120")]
assert 100 * 0.8 == 80 and 80 + 0.2 * 80 == 96
GOLD = "#ffd166"


def blocks(labels, light=(), start=None, step=0.4, col=MINT, cross=None, extra=None, size=158):
    """Five full-width price blocks (each 20% of the old price), on screen at frame 0. Blocks in `light` fill with
    `col` one by one from `start`; their text switches to a fixed dark colour. `cross`: index struck out in red.
    `extra`: (index, delay) of a block that pops in last."""
    out = ""
    for i, lab in enumerate(labels):
        lit = i in light
        d = (start or 0) + list(light).index(i) * step if lit else 0
        fill = (f'<div class=a style="position:absolute;inset:0;border-radius:22px;background:{col};'
                f'animation:pop .3s {d:.2f}s both"></div>') if lit else ""
        txt = (f'<span class=a style="position:relative;color:#111;animation:pop .3s {d:.2f}s both">{lab}</span>'
               if lit else f'<span style="position:relative;color:#fff">{lab}</span>')
        x = (f'<div class=a style="position:absolute;left:-8px;right:-8px;top:50%;height:12px;background:{RED};'
             f'transform-origin:left;animation:grow .4s {cross[1]:.2f}s both"></div>') if cross and cross[0] == i else ""
        pop = f"animation:pop .4s {extra[1]:.2f}s both;" if extra and extra[0] == i else ""
        out += (f'<div class=a style="position:relative;width:{size}px;height:{int(size * 1.05)}px;border-radius:22px;'
                f'background:#262626;display:flex;align-items:center;justify-content:center;'
                f'font:800 54px Montserrat;{pop}">{fill}{txt}{x}</div>')
    return f'<div style="display:flex;gap:14px;margin-top:40px">{out}</div>'


def counter(vals, start, step, color=MINT, size=120, label=""):
    spans = ""
    for i, v in enumerate(vals):
        d = start + i * step
        last = i == len(vals) - 1
        anim = f"animation:show {step:.2f}s {d:.2f}s both" if not last else f"animation:pop .35s {d:.2f}s both"
        spans += f'<span class=a style="position:absolute;left:0;{anim}">{v}</span>'
    return ('<style>@keyframes show{0%{opacity:0}1%,99%{opacity:1}100%{opacity:0}}</style>'
            f'<div style="display:flex;align-items:baseline;gap:26px;margin-top:50px;font:800 {size}px Montserrat">'
            f'<span style="color:#999;font-size:64px">{label}</span>'
            f'<span style="position:relative;display:inline-block;width:360px;height:{size + 10}px;color:{color}">'
            f'{spans}</span></div>')


TAG = ('<div style="display:flex;align-items:center;gap:30px">'
       '<div style="padding:18px 40px;border-radius:26px;background:#fff;color:#111;font:800 130px Montserrat">$80</div>'
       '<div class=a style="padding:12px 28px;border-radius:20px;background:#ff6b6b;color:#111;'
       'font:800 76px Montserrat;animation:pop .4s .6s both">−20%</div></div>')

HOOK = ('<div class=big style="font-size:92px">After 20% off,<br>a jacket is:</div>'
        f'<div style="margin-top:40px">{TAG}</div>'
        + blocks(["?"] * 5)
        + '<div class="mid a" style="margin-top:50px;font-size:72px;animation:in .4s 3.0s both">'
          'Price <span style="color:#ffd166">before</span>?</div>'
        + f'<div style="margin-top:40px">{bubbles()}</div>')

beats = [
    Beat("A jacket is on sale for twenty percent off. It now costs eighty dollars. What was the price before the discount?",
         HOOK, sfx=[("pop", 0.6), ("pop", 3.0)]),
    Beat("Pick one.", '<div class="mid a" style="animation:in .4s both">Pick one</div>'
         + choice_list(CHOICES, font="800 80px Montserrat", gap=26),
         sfx=[("pop", t) for t in (0, .18, .36, .54, .72)], min_len=2.0),
    Beat("Three seconds.", COUNTDOWN, sfx=[("tick", 0.0), ("tick", 1.0), ("tick", 2.0)], min_len=3.2),
    Beat("Cut the old price into five equal blocks. The discount takes one block away. You pay for the other four.",
         '<div class=mid>Old price = 5 blocks of 20%.</div>'
         + blocks(["20%"] * 5, light=(0, 1, 2, 3), start=1.2, step=0.35, cross=(4, 2.8))
         + '<div class="mid a" style="margin-top:40px;font-size:66px;animation:in .4s 3.2s both">'
           'You pay <span class=mint>4 blocks</span> = $80</div>',
         sfx=[("pop", 1.2 + 0.35 * i) for i in range(4)] + [("thump", 2.8)]),
    Beat("Four blocks are eighty dollars, so each block is twenty dollars.",
         '<div class=mid>$80 ÷ 4 blocks</div>'
         + blocks(["$20"] * 4 + ["?"], light=(0, 1, 2, 3), start=0.5, step=0.4)
         + counter(["$20", "$40", "$60", "$80"], 0.6, 0.4, label="paid"),
         sfx=[("pop", 0.5 + 0.4 * i) for i in range(4)]),
    Beat("Five blocks make one hundred dollars. So it is answer D.",
         '<div class=mid>Put the 5th block back.</div>'
         + blocks(["$20"] * 5, light=(0, 1, 2, 3, 4), start=0.0, step=0.15, col=GOLD, extra=(4, 0.9))
         + '<div class="big a" style="font-size:120px;margin-top:50px;animation:pop .45s 1.4s both">'
           '5 × 20 = <span class=mint>$100</span></div>'
           '<div class=a style="margin-top:30px;animation:in .4s 2.2s both">'
         + choice_list(CHOICES, highlight="D", animate=False, font="800 54px Montserrat", gap=8) + '</div>',
         sfx=[("pop", 0.9), ("ding", 1.4)]),
    Beat("The trap is answer C. Ninety-six adds twenty percent of eighty, but the discount came off the old price.",
         '<div class="big a" style="font-size:104px;animation:in .4s both">Trap: <span class=mint>C</span></div>'
         '<div style="font:800 120px Montserrat;margin-top:60px"><span style="position:relative">80 + 16 = 96'
         + strike(1.6, 12) + '</span></div>'
         '<p class=a style="margin-top:40px;font-size:58px;animation:in .4s 1.0s both">16 is 20% of the wrong price.</p>'
         '<p class=a style="margin-top:14px;font-size:58px;animation:in .4s 2.6s both">Take 20% of the '
         '<span class=mint>old</span> price: 100 − 20 = 80 ✓</p>', sfx=[("thump", 1.6)]),
    Beat("Save this for your next percent question.", save_beat_scene("D"), sfx=[("pop", 0.1)], pad_after=0.6),
]

COVER = cover("forest", "Trap Answer", "$80 after<br>20% off.<br>Price before?", 118)

if __name__ == "__main__":
    res = build(ID, beats, COVER, voiced=True, seed=109)
    print(json.dumps({k: v for k, v in res["measures"].items() if k != "takes"}, default=float))
