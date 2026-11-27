"""Sample Reel for the v2 style (owner feedback, 26 Nov): more animation, 20 s to read and solve, follow invite.
Original question: class A has 20 students averaging 70, class B has 30 students averaging 80. Average of all 50?
(A) 74 (B) 75 (C) 76 (D) 77 (E) 78. Answer C, verified in items/sample-weighted-avg.py. Trap B (plain average).
Usage: python3 posts/sample-v2-weighted.py"""
import json
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import bubbles
from reel import Beat, build
from reelkit import MINT, RED, choice_list, cover, follow_card, strike, think_scene

ID = "sample-v2-weighted"
CH = [("A", "74"), ("B", "75"), ("C", "76"), ("D", "77"), ("E", "78")]
GOLD = "#ffd166"


def people(n, colour, delay=0.0, step=0.03, cols=10, size=58):
    """n little person icons popping in one by one (our own SVG)."""
    icon = (f'<svg width="{size}" height="{size}" viewBox="0 0 40 40"><circle cx="20" cy="12" r="8" fill="{colour}"/>'
            f'<path d="M6 38c0-9 6-15 14-15s14 6 14 15z" fill="{colour}"/></svg>')
    cells = "".join(f'<div class=a style="animation:pop .3s {delay + i * step:.2f}s both">{icon}</div>' for i in range(n))
    return (f'<div style="display:grid;grid-template-columns:repeat({cols},{size}px);gap:10px">{cells}</div>')


def group(label, n, avg, colour, delay):
    return (f'<div style="margin-top:24px"><div style="display:flex;align-items:baseline;gap:22px;margin-bottom:16px">'
            f'<span class=mid style="font-size:64px;color:{colour}">{label}</span>'
            f'<span style="font:700 46px Inter">{n} students · avg <b style="font:800 54px Montserrat">{avg}</b></span>'
            f'</div>{people(n, colour, delay)}</div>')


def counter(values, start, step, size=150, colour=MINT):
    spans = "".join(
        f'<span class=a style="position:absolute;left:0;animation:{"cnt" if i < len(values) - 1 else "pop"} '
        f'{step if i < len(values) - 1 else .35:.2f}s {start + i * step:.2f}s both">{v}</span>'
        for i, v in enumerate(values))
    return ('<style>@keyframes cnt{0%{opacity:0}1%,99%{opacity:1}100%{opacity:0}}</style>'
            f'<span style="position:relative;display:inline-block;min-width:{size * 2.6:.0f}px;height:{size * 1.1:.0f}px;'
            f'font:800 {size}px Montserrat;color:{colour}">{spans}</span>')


def number_line(marker_to, delay=0.6, show_mid=True):
    """70 to 80 on a line; a marker slides from the middle (75) to the weighted point, weights hang on each end."""
    pct = (marker_to - 70) / 10 * 100
    mid = ('<div style="position:absolute;left:50%;top:-70px;transform:translateX(-50%);font:700 40px Inter;'
           'color:#ff6b6b">75?</div>') if show_mid else ""
    return (f'<style>@keyframes slide{{from{{left:50%}}to{{left:{pct:.1f}%}}}}'
            f'@keyframes sag{{from{{transform:rotate(0)}}to{{transform:rotate(4deg)}}}}</style>'
            f'<div class=a style="position:relative;margin:150px 30px 0;height:14px;background:#444;border-radius:7px;'
            f'transform-origin:{pct:.1f}% 50%;animation:sag 1.2s {delay:.2f}s both">'
            f'<div style="position:absolute;left:-30px;top:40px;font:800 64px Montserrat">70</div>'
            f'<div style="position:absolute;right:-30px;top:40px;font:800 64px Montserrat">80</div>'
            f'<div style="position:absolute;left:-10px;top:-120px;width:110px;height:110px;border-radius:20px;'
            f'background:#7aa7ff;display:flex;align-items:center;justify-content:center;font:800 50px Montserrat;'
            f'color:#111">20</div>'
            f'<div style="position:absolute;right:-30px;top:-160px;width:150px;height:150px;border-radius:24px;'
            f'background:{GOLD};display:flex;align-items:center;justify-content:center;font:800 64px Montserrat;'
            f'color:#111">30</div>{mid}'
            f'<div class=a style="position:absolute;top:-30px;width:0;height:0;border-left:34px solid transparent;'
            f'border-right:34px solid transparent;border-bottom:60px solid {MINT};transform:translate(-34px,44px);'
            f'animation:slide 1.4s {delay:.2f}s both"></div></div>')


QUESTION_SMALL = (
    '<div style="font:700 48px/1.3 Inter"><span style="color:#7aa7ff">Class A</span>: 20 students, avg 70<br>'
    f'<span style="color:{GOLD}">Class B</span>: 30 students, avg 80<br><b>Average of all 50?</b></div>'
    + choice_list(CH, animate=False, font="800 60px Montserrat", gap=10))

HOOK = ('<div class=big style="font-size:96px">Average of<br>all 50 students?</div>'
        + group("A", 20, 70, "#7aa7ff", 0.2) + group("B", 30, 80, GOLD, 0.9))

beats = [
    Beat("One class of twenty scores seventy on average. Another class of thirty scores eighty. "
         "What is the average for all fifty?", HOOK, sfx=[("pop", 0.2), ("pop", 0.9)]),
    Beat("Pick one.", '<div class="mid a" style="animation:in .4s both">Pick one</div>'
         + choice_list(CH, font="800 96px Montserrat", gap=26), sfx=[("pop", t) for t in (0, .18, .36, .54, .72)],
         min_len=1.8),
    Beat("You have twenty seconds. Go.", think_scene(QUESTION_SMALL, 20, delay=1.6), think=20),
    Beat("Seventy-five is the trap. That treats both classes as the same size.",
         '<div class="big a" style="animation:in .4s both"><span style="position:relative">75' + strike(0.8, 14)
         + '</span> is the trap</div><div style="display:flex;align-items:flex-end;gap:40px;margin-top:80px">'
         '<div class=a style="width:300px;height:220px;background:#7aa7ff;border-radius:24px;transform-origin:bottom;'
         'animation:grow2 .8s 1.4s both"></div><div class=a style="width:300px;height:330px;background:#ffd166;'
         'border-radius:24px;transform-origin:bottom;animation:grow2 .8s 1.8s both"></div></div>'
         '<div style="display:flex;gap:40px;margin-top:18px;font:800 56px Montserrat"><span style="width:300px;'
         'text-align:center">20</span><span style="width:300px;text-align:center">30</span></div>'
         '<style>@keyframes grow2{from{transform:scaleY(0)}to{transform:scaleY(1)}}</style>',
         sfx=[("thump", 0.8), ("pop", 1.4), ("pop", 1.8)]),
    Beat("Use totals. Twenty times seventy is one thousand four hundred. Thirty times eighty is two thousand four hundred.",
         '<div class="mid mint a" style="animation:in .4s both">Use totals</div>'
         '<div style="margin-top:40px;font:700 60px Inter;color:#7aa7ff">20 × 70 =</div>'
         + counter([200, 600, 1000, 1400], 0.8, 0.35, 130, "#7aa7ff")
         + f'<div style="margin-top:30px;font:700 60px Inter;color:{GOLD}">30 × 80 =</div>'
         + counter([400, 1200, 2000, 2400], 3.4, 0.35, 130, GOLD),
         sfx=[("pop", 1.85), ("pop", 4.45)]),
    Beat("Together that's three thousand eight hundred, divided by fifty. Seventy-six. So it is answer C.",
         '<div style="font:700 60px Inter">1400 + 2400</div><div style="font:700 60px Inter;margin-top:10px">'
         '= 3800 ÷ 50</div><div style="margin-top:30px">' + counter([70, 72, 74, 76], 2.4, 0.3, 220) + '</div>'
         + f'<div style="margin-top:30px">{bubbles("C")}</div>', sfx=[("ding", 3.4)]),
    Beat("Shortcut. The bigger class pulls the average toward eighty. Three fifths of the way. Seventy-six.",
         '<div class="mid mint a" style="animation:in .4s both">Shortcut: it tips</div>' + number_line(76, 0.8)
         + '<div class="big a" style="margin-top:170px;animation:pop .4s 2.6s both">3/5 of the way → '
           '<span class=mint>76</span></div>', sfx=[("pop", 0.8), ("ding", 2.6)]),
    Beat("Follow for a new question every day.", follow_card("C"), sfx=[("pop", 0.6), ("ding", 2.3)],
         pad_after=1.2),
]

COVER = cover("forest", "Trap Answer", "20 at 70.<br>30 at 80.<br>Not 75.", 118)

if __name__ == "__main__":
    res = build(ID, beats, COVER, voiced=True, seed=131)
    print(json.dumps({k: v for k, v in res["measures"].items() if k != "takes"}, default=float))
