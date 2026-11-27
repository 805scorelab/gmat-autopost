"""Reel 2026-11-30-r2, series Grad School: guess the average years of work experience in Wharton's newest MBA class.
Voiced, score v1, v2 style.

Weekly plan (docs/daily/daily-run.md 0.5): Monday 21:00 Reel = grad school.

Facts, checked on 27 Nov 2026 on the school's own page (mba.wharton.upenn.edu/class-profile, "Class of 2028",
"*Note: Profile as of November 9, 2026"):
- "Incoming Wharton MBA students bring an average of five years of work experience, with experience levels ranging
  from 1 to 15 years."
- "There is no minimum GMAT or GRE score requirement to apply to the Wharton MBA program, and we don't have a
  preference for one test over another."
The page's numeric counters (class size, GMAT average and so on) did not load in our text fetch, so none of them is
used. Guess options A 2, B 5, C 8, D 11 years are guesses, not facts; only B is presented as a fact.
Takeaway (no invented numbers, no admissions promise): an average is a middle, not a cutoff.
Quality-log next steps applied (28-r2: source line close to the subtitles, move it to the top under the progress
bar; 29-r2: scenes use only the top half of the zone, scale panels to fill the height): the source line sits at the
top of each fact scene, and the timeline scale and people row fill the zone width and height.
Usage: python3 posts/2026-11-30-r2.py
"""
import json
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import bubbles
from reel import Beat, build
from reelkit import MINT, RED, choice_list, cover, follow_card, strike, think_scene

ID = "2026-11-30-r2"
GOLD = "#ffd166"
BLUE = "#7aa7ff"
GUESS = [("A", "2 years"), ("B", "5 years"), ("C", "8 years"), ("D", "11 years")]
LO, HI = 0, 16                         # timeline in years of work experience
FACT = {"avg": 5, "lo": 1, "hi": 15}
assert int(GUESS[1][1].split()[0]) == FACT["avg"]


def pct(v):
    return (v - LO) / (HI - LO) * 100


def scale(marker=None, delay=0.4, sweep=False, band=None, ticks=(0, 5, 10, 15)):
    """A full-width timeline 0 to 16 years. marker: a pointer slides to that value; sweep: pointer swings back and
    forth; band: (lo, hi, delay) a mint band grows across that range."""
    css = ('<style>@keyframes mk{from{left:0%}to{left:var(--to)}}'
           '@keyframes swp{0%{left:8%}50%{left:92%}100%{left:8%}}'
           '@keyframes bandg{from{transform:scaleX(0)}to{transform:scaleX(1)}}</style>')
    t = "".join(f'<div style="position:absolute;left:{pct(v):.1f}%;top:46px;transform:translateX(-50%);'
                f'font:700 40px Inter;color:#999">{v}</div>' for v in ticks)
    b = ""
    if band:
        b = (f'<div class=a style="position:absolute;left:{pct(band[0]):.1f}%;width:{pct(band[1]) - pct(band[0]):.1f}%;'
             f'top:-6px;height:36px;border-radius:18px;background:{MINT};opacity:.6;transform-origin:left;'
             f'animation:bandg 1.4s {band[2]:.2f}s both"></div>')
    m = ""
    if marker is not None or sweep:
        anim = (f"animation:swp 4s {delay:.2f}s ease-in-out infinite both" if sweep
                else f"--to:{pct(marker):.1f}%;animation:mk 1.6s {delay:.2f}s cubic-bezier(.2,.8,.2,1) both")
        m = (f'<div class=a style="position:absolute;top:-70px;width:0;height:0;border-left:30px solid transparent;'
             f'border-right:30px solid transparent;border-top:52px solid {GOLD};transform:translateX(-30px);{anim}">'
             f'</div>')
    return (css + '<div style="position:relative;margin:110px 30px 100px;height:24px;border-radius:12px;'
            f'background:#2a2a2a">{b}{t}{m}</div>')


def counter(vals, start, step, color=MINT, size=220, unit=""):
    spans = ""
    for i, v in enumerate(vals):
        last = i == len(vals) - 1
        anim = (f"animation:show {step:.2f}s {start + i * step:.2f}s both" if not last
                else f"animation:pop .4s {start + i * step:.2f}s both")
        spans += f'<span class=a style="position:absolute;left:0;{anim}">{v}</span>'
    return ('<style>@keyframes show{0%{opacity:0}1%,99%{opacity:1}100%{opacity:0}}</style>'
            '<div style="display:flex;align-items:baseline;gap:24px">'
            f'<span style="position:relative;display:inline-block;width:{size * 0.75:.0f}px;height:{size * 1.05:.0f}px;'
            f'font:800 {size}px Montserrat;color:{color}">{spans}</span>'
            f'<span style="font:800 90px Montserrat">{unit}</span></div>')


def briefcases(n, start=0.3, step=0.12, col=MINT, per_row=8):
    """n small briefcase icons (one per year) that pop in one after another, wrapping rows to fill the width."""
    out = ""
    for i in range(n):
        out += (f'<svg class=a width="92" height="80" viewBox="0 0 92 80" style="animation:pop .3s {start + i * step:.2f}s both">'
                f'<rect x="30" y="4" width="32" height="16" rx="6" fill="none" stroke="{col}" stroke-width="7"/>'
                f'<rect x="4" y="18" width="84" height="56" rx="12" fill="{col}"/>'
                f'<rect x="38" y="38" width="16" height="10" rx="3" fill="#111"/></svg>')
    return f'<div style="display:grid;grid-template-columns:repeat({per_row},92px);gap:14px 12px">{out}</div>'


SRC = ('<div style="font:600 34px Inter;color:#999;margin-bottom:24px">'
       'Source: Wharton MBA class profile, Class of 2028 (as of 9 Nov 2026)</div>')

HOOK = ('<span class=chip style="font-size:40px">Grad school · guess first</span>'
        '<div class=big style="font-size:96px;margin-top:30px">Wharton MBA.<br>Average years of<br>'
        '<span class=mint>work experience</span>?</div>'
        + scale(sweep=True, delay=0.0)
        + briefcases(16, start=0.0, step=0.0, col="#2f2f2f"))

QUESTION = ('<div style="font:700 56px/1.3 Inter">Wharton MBA, Class of 2028.<br><b>Average years of work experience?'
            '</b></div>' + scale(sweep=True, delay=0.0)
            + '<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px 50px">'
            + "".join(f'<div style="font:800 64px Montserrat">({k}) {v}</div>' for k, v in GUESS) + '</div>')

beats = [
    Beat("A famous business school in Philadelphia. Its newest class. Guess the average years of work experience.",
         HOOK, sfx=[("pop", 0.3)]),
    Beat("Pick one.", '<div class="mid a" style="animation:in .4s both">Pick one</div>'
         + choice_list(GUESS, font="800 104px Montserrat", gap=30), sfx=[("pop", t) for t in (0, .18, .36, .54)],
         min_len=1.8),
    Beat("You have ten seconds. Guess.", think_scene(QUESTION, 10, delay=1.4, note="Lock in your guess."), think=10),
    Beat("The average is five years.",
         SRC + '<div class="mid a" style="animation:in .4s both">Class average</div>'
         + counter([1, 2, 3, 4, 5], 0.4, 0.3, unit="years") + scale(marker=5, delay=0.4)
         + briefcases(5, start=0.4, step=0.3)
         + f'<div class=a style="margin-top:40px;animation:in .4s 2.0s both">{bubbles("B", "ABCD")}</div>',
         sfx=[("pop", 0.4 + 0.3 * i) for i in range(5)] + [("ding", 2.0)], min_len=3.4),
    Beat("But the class runs from one year all the way to fifteen.",
         SRC + '<div class="mid a" style="animation:in .4s both">Range in the same class</div>'
         + scale(band=(1, 15, 0.5), ticks=(1, 5, 10, 15))
         + '<div style="display:flex;justify-content:space-between;align-items:flex-end;margin:0 20px">'
           '<div><div class=a style="font:800 120px Montserrat;color:#fff;animation:pop .4s .9s both">1</div>'
         + briefcases(1, start=0.9, per_row=1) + '</div>'
           '<div><div class=a style="font:800 120px Montserrat;color:#BFFBD1;text-align:right;animation:pop .4s 1.9s both">15</div>'
         + briefcases(15, start=1.9, step=0.07, per_row=5) + '</div></div>',
         sfx=[("pop", 0.9), ("pop", 1.9)], min_len=3.6),
    Beat("The school also says there is no minimum test score to apply.",
         SRC + '<div class="big a" style="font-size:100px;animation:in .4s both">Minimum<br>GMAT or GRE?</div>'
         '<div style="display:flex;gap:40px;margin-top:70px;font:800 130px Montserrat;padding-left:20px">'
         '<span class=a style="position:relative;color:#999;animation:pop .4s .8s both">GMAT' + strike(1.5, 14) + '</span>'
         '<span class=a style="position:relative;color:#999;animation:pop .4s 1.1s both">GRE' + strike(1.8, 14) + '</span></div>'
         '<div class="mid a" style="margin:60px 0 0 30px;color:#BFFBD1;animation:pop .4s 2.4s both">None ✓</div>',
         sfx=[("pop", 0.8), ("pop", 1.1), ("thump", 1.5), ("ding", 2.4)], min_len=3.4),
    Beat("So an average is a middle, not a cutoff.",
         '<div class="big a" style="font-size:110px;animation:in .4s both">Average =<br><span class=mint>middle</span></div>'
         '<div class="big a" style="font-size:110px;margin-top:40px;position:relative;display:inline-block;color:#999;'
         'animation:in .4s .9s both"><span style="position:relative">cutoff' + strike(1.6, 14) + '</span></div>'
         + scale(marker=5, delay=0.2, band=(1, 15, 0.2), ticks=(1, 5, 15)),
         sfx=[("pop", 0.9), ("thump", 1.6)], min_len=2.8),
    Beat("Follow for a new question every day.", follow_card(), sfx=[("pop", 0.6), ("ding", 2.3)],
         pad_after=1.2),
]

COVER = cover("forest", "Grad School", "Wharton MBA.<br>Average years<br>of experience?", 112)

if __name__ == "__main__":
    res = build(ID, beats, COVER, voiced=True, seed=151)
    print(json.dumps({k: v for k, v in res["measures"].items() if k != "takes"}, default=float))
