"""Reel 2026-11-28-r2, series Grad School: guess Stanford GSB's average GMAT Focus score. Voiced, score v1, v2 style.

Weekly plan (docs/daily/daily-run.md 0.5): Saturday 21:00 Reel = grad school. Replaces the earlier DS Reel queued in
this slot (is n odd), which was built before the v2 standard and the weekly plan.

Facts, checked on 27 Nov 2026 on the school's own page (gsb.stanford.edu, MBA Entering Class Profile, "Class Profile
data is as of 17 September 2026"), Stanford MBA Class of 2028:
- 436 students
- GMAT (Focus) average 695, range 535 to 805
- GMAT average 743, range 650 to 780 (the older GMAT version)
Guess options A 655, B 695, C 745, D 785 are guesses, not facts; only B is presented as a fact.
Takeaway (no invented numbers): the same class has two different averages for the two GMAT versions, so compare a
Focus score with Focus figures.
Quality-log next step applied (29-r2 row: hook small, motion low, trim the hook line): the frame-0 picture is a
full-width score scale with a moving marker, and every beat has a moving element.
Narrator: the TTS/ASR pair drops "Stanford" in every position tried, so the school is named on screen, in the
caption and in the source line, and the spoken hook says "a famous business school on the West Coast".
Usage: python3 posts/2026-11-28-r2.py
"""
import json
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import bubbles
from reel import Beat, build
from reelkit import MINT, RED, choice_list, cover, follow_card, strike, think_scene

ID = "2026-11-28-r2"
GOLD = "#ffd166"
BLUE = "#7aa7ff"
GUESS = [("A", "655"), ("B", "695"), ("C", "745"), ("D", "785")]
LO, HI = 205, 805                       # GMAT Focus total score scale
FACT = {"focus_avg": 695, "focus_lo": 535, "focus_hi": 805, "classic_avg": 743, "size": 436}


def pct(v):
    return (v - LO) / (HI - LO) * 100


def scale(marker=None, delay=0.4, sweep=False, band=None, ticks=(205, 505, 805)):
    """A full-width score scale 205 to 805. marker: a value a pointer slides to (from the left end, or sweeping back
    and forth when sweep=True). band: (lo, hi, delay) a mint band that grows across that range."""
    css = ('<style>@keyframes mk{from{left:0%}to{left:var(--to)}}'
           '@keyframes swp{0%{left:10%}50%{left:90%}100%{left:10%}}'
           '@keyframes bandg{from{transform:scaleX(0)}to{transform:scaleX(1)}}</style>')
    t = "".join(f'<div style="position:absolute;left:{pct(v):.1f}%;top:46px;transform:translateX(-50%);'
                f'font:700 40px Inter;color:#999">{v}</div>' for v in ticks)
    b = ""
    if band:
        b = (f'<div class=a style="position:absolute;left:{pct(band[0]):.1f}%;width:{pct(band[1]) - pct(band[0]):.1f}%;'
             f'top:-6px;height:36px;border-radius:18px;background:{MINT};opacity:.55;transform-origin:left;'
             f'animation:bandg 1.2s {band[2]:.2f}s both"></div>')
    m = ""
    if marker is not None or sweep:
        anim = (f"animation:swp 4s {delay:.2f}s ease-in-out infinite both" if sweep
                else f"--to:{pct(marker):.1f}%;animation:mk 1.6s {delay:.2f}s cubic-bezier(.2,.8,.2,1) both")
        m = (f'<div class=a style="position:absolute;top:-70px;width:0;height:0;border-left:30px solid transparent;'
             f'border-right:30px solid transparent;border-top:52px solid {GOLD};transform:translateX(-30px);{anim}">'
             f'</div>')
    return (css + '<div style="position:relative;margin:110px 40px 90px;height:24px;border-radius:12px;'
            f'background:#2a2a2a">{b}{t}{m}</div>')


def counter(vals, start, step, color=MINT, size=200):
    spans = ""
    for i, v in enumerate(vals):
        last = i == len(vals) - 1
        anim = (f"animation:show {step:.2f}s {start + i * step:.2f}s both" if not last
                else f"animation:pop .4s {start + i * step:.2f}s both")
        spans += f'<span class=a style="position:absolute;left:0;{anim}">{v}</span>'
    return ('<style>@keyframes show{0%{opacity:0}1%,99%{opacity:1}100%{opacity:0}}</style>'
            f'<span style="position:relative;display:inline-block;width:{size * 2.2:.0f}px;height:{size * 1.1:.0f}px;'
            f'font:800 {size}px Montserrat;color:{color}">{spans}</span>')


def bars(delay=0.6):
    """Two bars, same class: older GMAT average 743 vs GMAT Focus average 695 (heights scaled on 205 to 805)."""
    def bar(label, v, col, d):
        h = int(560 * (v - LO) / (HI - LO))
        return (f'<div style="display:flex;flex-direction:column;align-items:center;width:340px">'
                f'<div class=a style="font:800 84px Montserrat;color:{col};animation:pop .4s {d + 0.8:.2f}s both">{v}'
                f'</div><div class=a style="width:260px;height:{h}px;border-radius:24px 24px 8px 8px;background:{col};'
                f'transform-origin:bottom;animation:grow2 1s {d:.2f}s both"></div>'
                f'<div style="font:700 44px Inter;margin-top:16px;text-align:center">{label}</div></div>')
    return ('<style>@keyframes grow2{from{transform:scaleY(0)}to{transform:scaleY(1)}}</style>'
            '<div style="display:flex;justify-content:center;gap:60px;align-items:flex-end;margin-top:40px">'
            + bar("older GMAT", FACT["classic_avg"], BLUE, delay) + bar("GMAT Focus", FACT["focus_avg"], MINT, delay + 1.2)
            + '</div>')


SRC = ('<div style="position:absolute;left:0;right:0;bottom:0;font:600 34px Inter;color:#999">'
       'Source: Stanford GSB class profile, Class of 2028 (as of 17 Sep 2026)</div>')

HOOK = ('<span class=chip style="font-size:40px">Grad school · guess first</span>'
        '<div class=big style="font-size:100px;margin-top:30px">Stanford MBA.<br>Average GMAT<br>'
        '<span class=mint>Focus</span> score?</div>'
        + scale(sweep=True, delay=0.0)
        + '<div class=mid style="font-size:56px;color:#bbb">Class of 2028 · 436 students</div>' + SRC)

QUESTION = ('<div style="font:700 52px/1.3 Inter">Stanford MBA, Class of 2028.<br><b>Average GMAT Focus score?</b></div>'
            + scale(sweep=True, delay=0.0) + choice_list(GUESS, animate=False, font="800 54px Montserrat", gap=2))

assert FACT["focus_avg"] == int(GUESS[1][1]) and FACT["classic_avg"] - FACT["focus_avg"] == 48

beats = [
    Beat("A famous business school on the West Coast. Its newest class. Guess the average GMAT Focus score.", HOOK, sfx=[("pop", 0.3)]),
    Beat("Pick one.", '<div class="mid a" style="animation:in .4s both">Pick one</div>'
         + choice_list(GUESS, font="800 104px Montserrat", gap=30), sfx=[("pop", t) for t in (0, .18, .36, .54)],
         min_len=1.8),
    Beat("You have ten seconds. Guess.", think_scene(QUESTION, 10, delay=1.4, note="Lock in your guess."), think=10),
    Beat("The average is six hundred ninety-five.",
         '<div class="mid a" style="animation:in .4s both">Class average, GMAT Focus</div>'
         '<div style="margin-top:30px">' + counter([605, 635, 655, 675, 695], 0.5, 0.28) + '</div>'
         + scale(marker=695, delay=0.5) + f'<div class=a style="animation:in .4s 1.9s both">{bubbles("B", "ABCD")}</div>' + SRC,
         sfx=[("ding", 1.62)]),
    Beat("The same class had an average of seven hundred forty-three on the older version of the test.",
         '<div class="mid a" style="animation:in .4s both">Same class. Two tests.</div>' + bars(0.6) + SRC,
         sfx=[("pop", 1.4), ("pop", 2.6)]),
    Beat("And their Focus scores ranged from five hundred thirty-five to eight hundred five.",
         '<div class="mid a" style="animation:in .4s both">GMAT Focus range</div>'
         + scale(band=(535, 805, 0.6), ticks=(205, 535, 805))
         + '<div style="display:flex;justify-content:space-between;margin:0 40px">'
           '<span class=a style="font:800 110px Montserrat;color:#fff;animation:pop .4s 1.0s both">535</span>'
           '<span class=a style="font:800 110px Montserrat;color:#BFFBD1;animation:pop .4s 1.8s both">805</span></div>'
         + SRC, sfx=[("pop", 1.0), ("pop", 1.8)]),
    Beat("So compare your Focus score with Focus numbers, not with old test numbers.",
         '<div class="big a" style="font-size:96px;animation:in .4s both">Compare<br><span class=mint>Focus</span> '
         'to <span class=mint>Focus</span></div>'
         '<div style="display:flex;gap:40px;margin-top:80px;font:800 110px Montserrat">'
         f'<span class=a style="position:relative;color:{BLUE};animation:pop .4s .9s both">743{strike(1.6, 12)}</span>'
         '<span class=a style="color:#BFFBD1;animation:pop .4s 2.2s both">695 ✓</span></div>'
         '<p class=a style="margin-top:50px;font-size:56px;animation:in .4s 3.0s both">Different test, different scale.'
         '</p>', sfx=[("pop", 0.9), ("thump", 1.6), ("ding", 2.2)]),
    Beat("Follow for a new question every day.", follow_card(), sfx=[("pop", 0.6), ("ding", 2.3)],
         pad_after=1.2),
]

COVER = cover("paper", "Grad School", "Stanford MBA.<br>Average<br>GMAT Focus?", 116)

if __name__ == "__main__":
    res = build(ID, beats, COVER, voiced=True, seed=137)
    print(json.dumps({k: v for k, v in res["measures"].items() if k != "takes"}, default=float))
