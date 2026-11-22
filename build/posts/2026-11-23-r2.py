"""Reel 2026-11-23-r2, series Trap Answer: is x positive? Data Sufficiency (Data Insights). Voiced, score v1.

Original question for 805 Score Lab: is x positive? (1) x^2 = 9 (2) x^3 = 27. Answer B, verified in
build/items/2026-11-23-r2.py. (1) allows 3 and -3; (2) allows only 3. Trap: D, forgetting -3 in statement 1.
Difficulty: our estimate, easy. Quality-log improvement applied: a drawn number line filling the frame.
Usage: python3 posts/2026-11-23-r2.py
"""
import json
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import base_css, bubbles
from reel import Beat, build

ID = "2026-11-23-r2"
KEY = [("A", "(1) alone"), ("B", "(2) alone"), ("C", "Both together"), ("D", "Each alone"), ("E", "Not even both")]


def key_list(highlight=None, cross=None, animate=True):
    rows = []
    for i, (l, v) in enumerate(KEY):
        on = " on" if l == highlight else ""
        anim = f"animation:pop .35s {i * .18:.2f}s both" if animate else ""
        x = ('<span class=a style="position:absolute;left:-6px;right:-6px;top:50%;height:8px;background:#ff6b6b;'
             'transform-origin:left;animation:grow .4s .3s both"></span>') if l == cross else ""
        rows.append(f'<div style="display:flex;align-items:center;gap:34px;margin-top:22px">'
                    f'<div class="bubble{on} a" style="{anim}">{l}</div>'
                    f'<span class=mid style="position:relative;font-size:62px">{v}{x}</span></div>')
    return "".join(rows)


def number_line(points, cross=(), note=""):
    """A number line from -5 to 5 filling the frame width; points = [(value, label, colour, delay)]."""
    def px(v):
        return 60 + (v + 5) * 74.8
    ticks = "".join(f'<line x1="{px(v)}" y1="190" x2="{px(v)}" y2="{230 if v else 250}" stroke="#666" stroke-width="5"/>'
                    f'<text x="{px(v)}" y="300" text-anchor="middle" font-family="Inter" font-weight="600" '
                    f'font-size="36" fill="#999">{"−" if v < 0 else ""}{abs(v)}</text>' for v in range(-5, 6))
    dots = ""
    for v, label, colour, delay in points:
        dots += (f'<g class=a style="transform-origin:{px(v)}px 210px;animation:pop .45s {delay}s both">'
                 f'<circle cx="{px(v)}" cy="210" r="30" fill="{colour}"/>'
                 f'<text x="{px(v)}" y="130" text-anchor="middle" font-family="Montserrat" font-weight="800" '
                 f'font-size="52" fill="{colour}">{label}</text></g>')
        if v in cross:
            dots += (f'<g class=a style="animation:in .3s {delay + .9}s both">'
                     f'<line x1="{px(v) - 50}" y1="160" x2="{px(v) + 50}" y2="260" stroke="#ff6b6b" stroke-width="12"/>'
                     f'<line x1="{px(v) + 50}" y1="160" x2="{px(v) - 50}" y2="260" stroke="#ff6b6b" stroke-width="12"/></g>')
    return (f'<svg width="868" height="330" viewBox="0 0 868 330" style="margin-top:60px">'
            f'<line x1="30" y1="210" x2="838" y2="210" stroke="#fff" stroke-width="6"/>'
            f'<rect x="{px(0)}" y="200" width="{px(5) - px(0) + 30}" height="20" fill="#BFFBD1" opacity=".18"/>'
            f'{ticks}{dots}</svg>'
            + (f'<p class=a style="margin-top:40px;animation:in .4s 1.2s both">{note}</p>' if note else ""))


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

QUESTION = ('<div class="big">Is x &gt; 0?</div>'
            '<div class="mid a" style="margin-top:50px;animation:in .4s .8s both">(1) x² = 9</div>'
            '<div class="mid a" style="margin-top:20px;animation:in .4s 2.2s both">(2) x³ = 27</div>')

beats = [
    Beat("Is x positive? Statement one: x squared is nine. Statement two: x cubed is twenty seven.",
         QUESTION + f'<div style="margin-top:70px">{bubbles()}</div>', sfx=[("pop", 0.8), ("pop", 2.2)]),
    Beat("Which statements are enough?",
         '<div class="mid a" style="animation:in .4s both">Enough to answer?</div>' + key_list(),
         sfx=[("pop", t) for t in (0, .18, .36, .54, .72)], min_len=2.0),
    Beat("Three seconds.", COUNTDOWN, sfx=[("tick", 0.0), ("tick", 1.0), ("tick", 2.0)], min_len=3.2),
    Beat("Statement one. Three squared is nine. But negative three squared is nine too.",
         '<div class="mid a" style="animation:in .4s both">(1) x² = 9</div>'
         + number_line([(3, "3", "#BFFBD1", .6), (-3, "−3", "#ffffff", 2.4)]),
         sfx=[("pop", 0.6), ("pop", 2.4)]),
    Beat("One answer is yes, one is no. Not enough.",
         '<div class="mid a" style="animation:in .4s both">(1) x² = 9</div>'
         + number_line([(3, "yes", "#BFFBD1", 0), (-3, "no", "#ffffff", 0)], note="Two answers. Not sufficient."),
         sfx=[("thump", 1.2)]),
    Beat("Statement two. Negative three cubed is negative twenty seven. Only three works.",
         '<div class="mid a" style="animation:in .4s both">(2) x³ = 27</div>'
         + number_line([(-3, "−3", "#ffffff", .4), (3, "3", "#BFFBD1", 2.6)], cross=(-3,)),
         sfx=[("pop", 0.4), ("thump", 1.3), ("pop", 2.6)]),
    Beat("A cube keeps the sign. So x is positive, and statement two alone is enough. The answer is B.",
         '<div class="big a" style="font-size:96px;animation:in .4s both">(2) alone: <span class=mint>B</span></div>'
         + key_list(highlight="B", animate=False), sfx=[("ding", 4.2)]),
    Beat("D is the trap. A square has two roots, so check the negative.",
         '<div class="big a" style="animation:in .4s both">Trap: <span class=mint>D</span></div>'
         '<p class=a style="margin-top:40px;animation:in .4s .4s both">x² = 9 means x = 3 <b>or</b> x = −3.</p>'
         + key_list(cross="D", animate=False), sfx=[("pop", 0.3)]),
    Beat("Save this for your next data sufficiency question.",
         '<div class="big a" style="animation:in .5s both">Save it.</div>'
         '<div class="mid a" style="margin-top:40px;animation:in .5s .4s both">@805scorelab</div>'
         f'<div style="margin-top:80px">{bubbles("B")}</div>', sfx=[("pop", 0.1)], pad_after=0.6),
]

COVER = f"""<style>{base_css('mint', height=1920)}
 .c{{position:absolute;top:420px;left:90px;right:90px}}</style><div class=frame><div class=c>
 <span class=chip>Trap Answer</span><h1 style="margin-top:40px;font-size:124px">x² = 9.<br>Is x<br>positive?</h1>
 <div style="margin-top:70px">{bubbles()}</div></div></div>"""

if __name__ == "__main__":
    res = build(ID, beats, COVER, voiced=True, seed=41)
    print(json.dumps({k: v for k, v in res["measures"].items() if k != "takes"}, default=float))
