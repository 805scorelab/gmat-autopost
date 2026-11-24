"""Reel 2026-11-25-r1, series Trap Answer: what is x + y? Data Sufficiency (Data Insights). Voiced, score v1.

Original question for 805 Score Lab: what is the value of x + y? (1) 2x + 2y = 14 (2) x - y = 1. Answer A, verified
in build/items/2026-11-25-r1.py. (1) halves to x + y = 7; (2) allows (5, 4), (1, 0) and every other pair one apart,
so the sum changes. Trap: C, solving for x and y separately when only the sum is asked.
Difficulty: our estimate, easy to medium. Quality-log improvement applied (from the last Reel row): no beat is text
only; every statement beat has a moving picture (halving equation, sliding pairs that keep or change the sum).
Usage: python3 posts/2026-11-25-r1.py
"""
import json
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import base_css, bubbles
from reel import Beat, build

ID = "2026-11-25-r1"
KEY = [("A", "(1) alone"), ("B", "(2) alone"), ("C", "Both together"), ("D", "Each alone"), ("E", "Not even both")]
RED = "#ff6b6b"


def key_list(highlight=None, cross=None, animate=True):
    rows = []
    for i, (l, v) in enumerate(KEY):
        on = " on" if l == highlight else ""
        anim = f"animation:pop .35s {i * .18:.2f}s both" if animate else ""
        dim = "opacity:.45;" if highlight and l != highlight else ""
        x = (f'<span class=a style="position:absolute;left:-6px;right:-6px;top:50%;height:8px;background:{RED};'
             'transform-origin:left;animation:grow .4s .5s both"></span>') if l == cross else ""
        rows.append(f'<div style="display:flex;align-items:center;gap:34px;margin-top:22px;{dim}">'
                    f'<div class="bubble{on} a" style="{anim}">{l}</div>'
                    f'<span class=mid style="position:relative;font-size:62px">{v}{x}</span></div>')
    return "".join(rows)


def halving():
    """2x + 2y = 14: the 2s get struck, a /2 badge drops in, and x + y = 7 rises below."""
    def two(d):
        return (f'<span style="position:relative;display:inline-block">2<span class=a style="position:absolute;'
                f'left:-4px;right:-4px;top:52%;height:9px;background:{RED};transform-origin:left;'
                f'animation:grow .35s {d:.2f}s both"></span></span>')
    return (f'<div class=big style="font-size:120px;margin-top:40px">{two(1.6)}x + {two(1.8)}y = '
            f'<span style="position:relative;display:inline-block">14<span class=a style="position:absolute;left:-4px;'
            f'right:-4px;top:52%;height:9px;background:{RED};transform-origin:left;animation:grow .35s 2.0s both">'
            '</span></span></div>'
            '<div class=a style="display:inline-block;align-self:flex-start;margin-top:40px;padding:16px 44px;'
            'border-radius:60px;background:#fff;color:#000;font:800 72px Montserrat;animation:pop .45s .9s both">'
            '÷ 2</div>'
            '<div class="big a" style="font-size:150px;margin-top:50px;animation:pop .5s 2.4s both">'
            '<span class=mint>x + y = 7</span></div>')


def pairs(rows, verdict, good):
    """Rows of (x, y) pairs popping in one after another, each with its sum; then a verdict."""
    out = ('<div style="display:grid;grid-template-columns:1fr 1fr 1.2fr;row-gap:28px;margin-top:40px;'
           'font:800 84px Montserrat">'
           '<div style="color:#999;font-size:52px">x</div><div style="color:#999;font-size:52px">y</div>'
           '<div style="color:#999;font-size:52px">x + y</div>')
    for i, (x, y) in enumerate(rows):
        d = 0.5 + i * 0.9
        s = x + y
        col = "#BFFBD1" if good else ("#BFFBD1" if i == 0 else RED)
        f = lambda v: ("−" if v < 0 else "") + str(abs(v))
        out += (f'<div class=a style="animation:in .35s {d:.2f}s both">{f(x)}</div>'
                f'<div class=a style="animation:in .35s {d + .1:.2f}s both">{f(y)}</div>'
                f'<div class=a style="color:{col};animation:pop .4s {d + .3:.2f}s both">{f(s)}</div>')
    out += "</div>"
    d = 0.5 + len(rows) * 0.9 + 0.3
    return out + f'<p class=a style="margin-top:50px;font-size:58px;animation:in .4s {d:.2f}s both">{verdict}</p>'


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

QUESTION = ('<div class="big">x + y = ?</div>'
            '<div class="mid a" style="margin-top:50px;animation:in .4s 1.4s both">(1) 2x + 2y = 14</div>'
            '<div class="mid a" style="margin-top:20px;animation:in .4s 4.0s both">(2) x − y = 1</div>')

beats = [
    Beat("What is x plus y? Statement one: two x plus two y equals fourteen. Statement two: x minus y equals one.",
         QUESTION + f'<div style="margin-top:70px">{bubbles()}</div>', sfx=[("pop", 1.4), ("pop", 4.0)]),
    Beat("Which statements are enough?",
         '<div class="mid a" style="animation:in .4s both">Enough to answer?</div>' + key_list(),
         sfx=[("pop", t) for t in (0, .18, .36, .54, .72)], min_len=2.0),
    Beat("Three seconds.", COUNTDOWN, sfx=[("tick", 0.0), ("tick", 1.0), ("tick", 2.0)], min_len=3.2),
    Beat("Statement one. Every term has a two. Divide both sides by two.",
         '<div class="mid a" style="animation:in .4s both">(1) 2x + 2y = 14</div>' + halving(),
         sfx=[("pop", 0.9), ("thump", 1.6), ("pop", 2.4)], min_len=3.2),
    Beat("So x plus y is seven. x and y can change, but the sum stays seven. Enough.",
         '<div class="mid a" style="animation:in .4s both">(1) x + y = <span class=mint>7</span></div>'
         + pairs([(3, 4), (10, -3), (0, 7)], "Every pair adds to 7. Sufficient.", True),
         sfx=[("pop", 0.8), ("pop", 1.7), ("pop", 2.6)]),
    Beat("Statement two. Five and four work. So do one and zero. The sum keeps changing. Not enough.",
         '<div class="mid a" style="animation:in .4s both">(2) x − y = 1</div>'
         + pairs([(5, 4), (1, 0), (10, 9)], "Three sums. Not sufficient.", False),
         sfx=[("pop", 0.8), ("thump", 1.7), ("thump", 2.6)]),
    Beat("Statement one alone answers it. Pick A.",
         '<div class="big a" style="font-size:96px;animation:in .4s both">(1) alone: <span class=mint>A</span></div>'
         + key_list(highlight="A", animate=False), sfx=[("ding", 1.6)]),
    Beat("C is the trap. You never needed x and y. You only needed their sum.",
         '<div class="big a" style="animation:in .4s both">Trap: <span class=mint>C</span></div>'
         '<p class=a style="margin-top:40px;animation:in .4s .4s both">Solve for what is asked, not for every letter.</p>'
         + key_list(cross="C", animate=False), sfx=[("thump", 0.5)]),
    Beat("Save this for your next data sufficiency question.",
         '<div class="big a" style="animation:in .5s both">Save it.</div>'
         '<div class="mid a" style="margin-top:40px;animation:in .5s .4s both">@805scorelab</div>'
         f'<div style="margin-top:80px">{bubbles("A")}</div>', sfx=[("pop", 0.1)], pad_after=0.6),
]

COVER = f"""<style>{base_css('mint', height=1920)}
 .c{{position:absolute;top:420px;left:90px;right:90px}}</style><div class=frame><div class=c>
 <span class=chip>Trap Answer</span><h1 style="margin-top:40px;font-size:124px">x + y = ?<br>Two equations?</h1>
 <div style="margin-top:70px">{bubbles()}</div></div></div>"""

if __name__ == "__main__":
    res = build(ID, beats, COVER, voiced=True, seed=73)
    print(json.dumps({k: v for k, v in res["measures"].items() if k != "takes"}, default=float))
