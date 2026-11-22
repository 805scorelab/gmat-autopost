"""Reel 2026-11-22-r2, Trap Answer: the fifth number. Silent variant (option b) for the A/B test against voiced Reels.
Original question: the average of 4 numbers is 10. A fifth number is added and the average becomes 12. What is the
fifth number? (A) 12 (B) 14 (C) 20 (D) 22 (E) 2. Answer C, verified in items/2026-11-22-r2.py. Trap A.
Usage: python3 posts/2026-11-22-r2.py [silent|voiced]"""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import base_css, bubbles
from reel import Beat, build

ID = "2026-11-22-r2"
CH = [("A", "12"), ("B", "14"), ("C", "20"), ("D", "22"), ("E", "2")]


def choices(on=None, cross=None):
    out = ""
    for i, (l, v) in enumerate(CH):
        x = ('<span class=a style="position:absolute;left:-6px;right:-6px;top:50%;height:8px;background:#ff6b6b;'
             'transform-origin:left;animation:grow .4s .3s both"></span>') if l == cross else ""
        out += (f'<div style="display:flex;align-items:center;gap:34px;margin-top:24px">'
                f'<div class="bubble{" on" if l == on else ""} a" style="animation:pop .35s {i * .15:.2f}s both">{l}</div>'
                f'<span class=mid style="position:relative">{v}{x}</span></div>')
    return out


def boxes(values, highlight_last=False, label=""):
    cells = "".join(f'<div class=a style="flex:1;height:170px;border-radius:18px;display:flex;align-items:center;'
                    f'justify-content:center;font:800 64px Montserrat;animation:pop .35s {i * .2:.1f}s both;'
                    f'background:{"#BFFBD1" if highlight_last and i == len(values) - 1 else "#1c1c1c"};'
                    f'color:{"#06142B" if highlight_last and i == len(values) - 1 else "#fff"}">{v}</div>'
                    for i, v in enumerate(values))
    return f'<div style="display:flex;gap:18px;margin-top:50px">{cells}</div><p style="margin-top:30px">{label}</p>'


beats = [
    Beat("Four numbers average ten. Add one number and the average jumps to twelve. What did you add?",
         '<div class="big">4 numbers.<br>Average 10.</div><div class="mid mint" style="margin-top:36px">'
         'Add one. Average 12.<br>What did you add?</div>' + f'<div style="margin-top:60px">{bubbles()}</div>',
         sfx=[("pop", 0.1)], caption="Can you get it in 10 seconds?"),
    Beat("Pick one.", '<div class="mid a" style="animation:in .4s both">Pick one</div>' + choices(),
         sfx=[("pop", 0), ("pop", .15), ("pop", .3), ("pop", .45), ("pop", .6)], min_len=2.0,
         caption="Lock in your answer."),
    Beat("Twelve is the trap.", '<div class="big a" style="animation:in .4s both">12 is<br>the trap.</div>'
         + choices(cross="A"), sfx=[("thump", 0.6)], caption="12 is the new average, not the new number."),
    Beat("Work with totals, not averages. Four numbers averaging ten add up to forty.",
         '<div class="mid mint a" style="animation:in .4s both">Totals, not averages</div>'
         + boxes(["10", "10", "10", "10"], label="4 × 10 = <b>40</b>"), sfx=[("pop", 0), ("pop", .8)],
         caption="Use totals: 4 × 10 = 40."),
    Beat("Five numbers averaging twelve add up to sixty.",
         '<div class="mid mint a" style="animation:in .4s both">After adding one</div>'
         + boxes(["12", "12", "12", "12", "12"], label="5 × 12 = <b>60</b>"), sfx=[("pop", 1.0)],
         caption="5 × 12 = 60."),
    Beat("The new number is sixty minus forty. Twenty. The answer is C.",
         '<div class="big a" style="animation:in .4s both">60 − 40 = <span class=mint>20</span></div>'
         + boxes(["10", "10", "10", "10", "20"], highlight_last=True, label="The answer is C.") ,
         sfx=[("ding", 1.0)], caption="60 − 40 = 20. Answer: C."),
    Beat("Shortcut. The new number covers its own twelve, plus two extra for each of the other four.",
         '<div class="mid mint a" style="animation:in .4s both">Shortcut</div>'
         '<div class="big a" style="margin-top:30px;animation:in .4s .4s both">12 + 4 × 2<br>= <span class=mint>20</span></div>',
         sfx=[("pop", .4), ("ding", 1.6)], caption="Shortcut: 12 + 4 × 2 = 20."),
    Beat("Save this for your next averages question.",
         '<div class="big a" style="animation:in .5s both">Save it.</div>'
         '<div class="mid a" style="margin-top:40px;animation:in .5s .4s both">@805scorelab</div>'
         f'<div style="margin-top:70px">{bubbles("C")}</div>', sfx=[("pop", .1)], pad_after=0.8,
         caption="Save this for your next averages question."),
]

COVER = f"""<style>{base_css('paper', height=1920)}.c{{position:absolute;top:440px;left:90px;right:90px}}</style>
<div class=frame><div class=c><span class=chip>Trap Answer</span><h1 style="margin-top:40px;font-size:124px">
Add one number.<br>Average jumps.<br>Find it.</h1><div style="margin-top:70px">{bubbles()}</div></div></div>"""

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "silent"
    res = build(ID, beats, COVER, voiced=(mode == "voiced"), seed=12)
    print(json.dumps({k: v for k, v in res["measures"].items() if k != "takes"}, default=float))
