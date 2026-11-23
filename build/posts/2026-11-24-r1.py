"""Reel 2026-11-24-r1, series Shortcut: swap the percent. Quant PS. Voiced, score v1.

Original question for 805 Score Lab: what is 28% of 75? (A) 19.6 (B) 21 (C) 22.4 (D) 24 (E) 28. Answer B, verified
in build/items/2026-11-24-r1.py. Shortcut: x% of y = y% of x (both are xy/100), so 75% of 28 = three quarters of 28 = 21.
Second example on screen: 8% of 50 = 50% of 8 = 4 (checked in the item run below). Difficulty: our estimate, easy to medium.
Quality-log improvement applied: bigger diagrams (tiles and bar fill the frame width) and motion between beats
(swapping tiles, a slow drift on every hold).
Usage: python3 posts/2026-11-24-r1.py
"""
import json
import sys
import pathlib
from fractions import Fraction as F
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import base_css, bubbles
from reel import Beat, build

ID = "2026-11-24-r1"
CHOICES = [("A", "19.6"), ("B", "21"), ("C", "22.4"), ("D", "24"), ("E", "28")]
assert F(8, 100) * 50 == F(50, 100) * 8 == 4 and F(28, 100) * 75 == F(75, 100) * 28 == 21


def choice_list(highlight=None, cross=None, animate=True):
    rows = []
    for i, (l, v) in enumerate(CHOICES):
        on = " on" if l == highlight else ""
        anim = f"animation:pop .35s {i * .18:.2f}s both" if animate else ""
        x = ('<span class=a style="position:absolute;left:-6px;right:-6px;top:50%;height:8px;background:#ff6b6b;'
             'transform-origin:left;animation:grow .4s .3s both"></span>') if l == cross else ""
        rows.append(f'<div style="display:flex;align-items:center;gap:34px;margin-top:24px">'
                    f'<div class="bubble{on} a" style="{anim}">{l}</div>'
                    f'<span class=mid style="position:relative">{v}{x}</span></div>')
    return "".join(rows)


def tiles(swap=False, delay=0.5):
    """Two big tiles in two slots: "__ % of __". The % belongs to the left slot, so when the numbers trade
    places the slot keeps its %: 28% of 75 becomes 75% of 28."""
    css = """<style>@keyframes toR{0%{transform:none}50%{transform:translate(244px,-100px)}100%{transform:translateX(488px)}}
      @keyframes toL{0%{transform:none}50%{transform:translate(-244px,100px)}100%{transform:translateX(-488px)}}
      .tile{width:380px;height:300px;border-radius:36px;display:flex;align-items:center;justify-content:center;
        font:800 150px Montserrat;letter-spacing:-.03em;background:#fff;color:#000;position:relative;z-index:3}
      .pct{position:absolute;left:280px;top:-120px;width:110px;height:110px;border-radius:50%;background:#BFFBD1;
        color:#06142B;display:flex;align-items:center;justify-content:center;font:800 70px Montserrat;z-index:1}</style>"""
    a_anim = f"animation:toR 1.1s {delay}s both" if swap else "animation:pop .4s both"
    b_anim = f"animation:toL 1.1s {delay}s both" if swap else "animation:pop .4s .3s both"
    return (css + '<div style="position:relative;display:flex;justify-content:space-between;align-items:center;'
            'margin-top:170px">'
            f'<div class="tile a" style="{a_anim}">28</div>'
            '<div class=pct>%</div>'
            '<div class="mid" style="position:absolute;left:50%;transform:translateX(-50%);font-size:60px">of</div>'
            f'<div class="tile a" style="{b_anim}">75</div></div>'
            f'<div class="mid mint a" style="margin-top:90px;animation:in .4s {delay + 1.2:.1f}s both">75% of 28</div>')


def bar(filled=0, labels=True, delay=0.4):
    """28 as one long bar cut into four 7s; `filled` quarters light up one by one."""
    cells = ""
    for i in range(4):
        on = i < filled
        cells += (f'<div class=a style="flex:1;height:260px;border-radius:22px;display:flex;align-items:center;'
                  f'justify-content:center;font:800 96px Montserrat;'
                  f'background:{"#BFFBD1" if on else "#1d1d1d"};color:{"#06142B" if on else "#fff"};'
                  f'border:6px solid {"#BFFBD1" if on else "#444"};'
                  f'animation:{"fill" if on else "pop"} .45s {delay + i * .45:.2f}s both">7</div>')
    brace = ('<div style="display:flex;justify-content:space-between;margin-top:26px">'
             '<span class=mid style="font-size:56px">28</span>'
             f'<span class="mid mint a" style="font-size:56px;animation:in .4s {delay + 1.6:.1f}s both">'
             f'{"3 of 4 = 21" if filled == 3 else "4 equal parts"}</span></div>') if labels else ""
    return f'<div style="display:flex;gap:16px;margin-top:60px">{cells}</div>{brace}'


COUNTDOWN = """<style>@keyframes ring{from{stroke-dashoffset:0}to{stroke-dashoffset:1100}}
 @keyframes s3{0%,33%{opacity:1}33.1%,100%{opacity:0}}@keyframes s2{0%,33%{opacity:0}33.1%,66%{opacity:1}66.1%,100%{opacity:0}}
 @keyframes s1{0%,66%{opacity:0}66.1%,100%{opacity:1}}</style>
 <div style="display:flex;justify-content:center"><svg width="620" height="620" viewBox="0 0 420 420">
 <circle cx="210" cy="210" r="175" stroke="#222" stroke-width="26" fill="none"/>
 <circle class=a cx="210" cy="210" r="175" stroke="#BFFBD1" stroke-width="26" fill="none" stroke-dasharray="1100"
   transform="rotate(-90 210 210)" style="animation:ring 3s linear both"/>""" + "".join(
    f'<text class=a x="210" y="250" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="130" '
    f'fill="#fff" style="animation:s{n} 3s linear both">{n}</text>' for n in (3, 2, 1)) + \
    """</svg></div><div class="mid a" style="text-align:center;margin-top:50px;animation:in .4s both">Think.</div>"""

beats = [
    Beat("What is twenty eight percent of seventy five? No calculator.",
         '<div class="big" style="font-size:150px">28% of 75</div>'
         '<div class="mid mint a" style="margin-top:40px;animation:in .4s 1.2s both">= ?</div>'
         f'<div style="margin-top:80px">{bubbles()}</div>', sfx=[("pop", 0.1), ("pop", 1.2)]),
    Beat("Pick one.", '<div class="mid a" style="animation:in .4s both">Pick one</div>' + choice_list(),
         sfx=[("pop", t) for t in (0, .18, .36, .54, .72)], min_len=1.8),
    Beat("Three seconds.", COUNTDOWN, sfx=[("tick", 0.0), ("tick", 1.0), ("tick", 2.0)], min_len=3.2),
    Beat("Don't multiply. Swap the numbers.",
         '<div class="mid a" style="animation:in .4s both">Swap them.</div>' + tiles(swap=True, delay=0.6),
         sfx=[("pop", 0.6), ("pop", 1.7)], min_len=2.8),
    Beat("Twenty eight percent of seventy five is seventy five percent of twenty eight. "
         "It's the same multiplication, so it's the same answer.",
         '<div class="big a" style="font-size:104px;animation:in .4s both">28% of 75<br>'
         '<span class=mint>= 75% of 28</span></div>'
         '<div class="mid a" style="margin-top:70px;font-size:68px;animation:in .4s 3.0s both">both = 28 × 75 ÷ 100</div>',
         sfx=[("pop", 1.6), ("pop", 3.0)]),
    Beat("Seventy five percent is three quarters. Cut twenty eight into four sevens.",
         '<div class="mid a" style="animation:in .4s both">75% = <span class=mint>¾</span></div>' + bar(0, delay=1.6),
         sfx=[("pop", 1.6 + i * .45) for i in range(4)]),
    Beat("Three of them make twenty one. The answer is B.",
         '<div class="mid a" style="animation:in .4s both">Take 3 of the 4</div>' + bar(3, delay=0.2)
         + f'<div style="margin-top:60px">{bubbles("B")}</div>',
         sfx=[("pop", 0.2), ("pop", 0.65), ("pop", 1.1), ("ding", 2.4)]),
    Beat("It works on any percent. Eight percent of fifty is fifty percent of eight, which is four.",
         '<div class="big a" style="font-size:112px;animation:in .4s both">8% of 50</div>'
         '<div class="big mint a" style="font-size:112px;margin-top:30px;animation:in .4s 2.0s both">= 50% of 8</div>'
         '<div class="big a" style="font-size:150px;margin-top:40px;animation:pop .45s 3.6s both">= 4</div>',
         sfx=[("pop", 2.0), ("ding", 3.6)]),
    Beat("Save this for your next percent question.",
         '<div class="big a" style="animation:in .5s both">Save it.</div>'
         '<div class="mid a" style="margin-top:40px;animation:in .5s .4s both">@805scorelab</div>'
         f'<div style="margin-top:80px">{bubbles("B")}</div>', sfx=[("pop", 0.1)], pad_after=0.6),
]

COVER = f"""<style>{base_css('paper', height=1920)}
 .c{{position:absolute;top:420px;left:90px;right:90px}}</style><div class=frame><div class=c>
 <span class=chip>Shortcut</span><h1 style="margin-top:40px;font-size:124px">28% of 75<br>in 5 seconds.</h1>
 <div style="margin-top:70px">{bubbles()}</div></div></div>"""

if __name__ == "__main__":
    res = build(ID, beats, COVER, voiced=True, seed=59)
    print(json.dumps({k: v for k, v in res["measures"].items() if k != "takes"}, default=float))
