"""Reel 2026-11-22-r1, series Shortcut: up 20%, then down 20%.

Original question for 805 Score Lab: a price rises 20% and then falls 20%. What is the net percent change?
(A) 0% (B) -4% (C) +4% (D) -2% (E) +2%.  Answer B, verified in build/items/2026-11-22-r1.py.
Hand solution: 100 -> 120 -> 96. Shortcut: up p% then down p% loses p^2/100 percent: 20 x 20 / 100 = 4.
Trap: A, assuming the moves cancel. Difficulty: our estimate, easy.
Usage: python3 posts/2026-11-22-r1.py [voiced|silent]
"""
import json
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import base_css, bubbles
from reel import Beat, build

ID = "2026-11-22-r1"
CHOICES = [("A", "0%"), ("B", "−4%"), ("C", "+4%"), ("D", "−2%"), ("E", "+2%")]


def choice_list(highlight=None, cross=None, delay=0.0):
    rows = []
    for i, (l, v) in enumerate(CHOICES):
        on = " on" if l == highlight else ""
        anim = f"animation:pop .35s {delay + i * .18:.2f}s both" if delay is not None else ""
        x = '<span style="position:absolute;left:-6px;right:-6px;top:50%;height:8px;background:#ff6b6b;' \
            'transform-origin:left;animation:grow .4s .3s both" class=a></span>' if l == cross else ""
        rows.append(f'<div style="display:flex;align-items:center;gap:34px;margin-top:26px;position:relative">'
                    f'<div class="bubble{on} a" style="{anim}">{l}</div>'
                    f'<span class=mid style="position:relative">{v}{x}</span></div>')
    return "".join(rows)


def bar(from_pct, to_pct, label_from, label_to, colour="#BFFBD1"):
    """A horizontal bar that grows or shrinks from one value to another (max 130 maps to the full width)."""
    w0, w1 = from_pct / 130 * 100, to_pct / 130 * 100
    return f"""<style>@keyframes b{int(from_pct)}{int(to_pct)}{{from{{width:{w0}%}}to{{width:{w1}%}}}}
      @keyframes lab{{0%,60%{{opacity:0}}100%{{opacity:1}}}}</style>
      <div style="margin-top:80px;height:220px;background:#151a17;border-radius:20px;overflow:hidden">
        <div class=a style="height:100%;background:{colour};border-radius:20px;
             animation:b{int(from_pct)}{int(to_pct)} 1.1s .2s both cubic-bezier(.3,.8,.2,1)"></div></div>
      <div style="display:flex;justify-content:space-between;margin-top:26px">
        <span class=mid style="opacity:.6">{label_from}</span>
        <span class="big mint a" style="animation:lab 1.4s both">{label_to}</span></div>"""


beats = [
    Beat("A price goes up twenty percent, then down twenty percent. Where does it end up?",
         '<div class="big" style="font-size:150px">Up 20%.<br>Down 20%.</div>'
         '<div class="mid mint" style="margin-top:40px">Where does it end up?</div>'
         f'<div style="margin-top:80px">{bubbles()}</div>',
         sfx=[("pop", 0.1), ("pop", 0.6)], caption="Up 20%, then down 20%. Where does it end up?"),
    Beat("Pick one.", '<div class="mid a" style="animation:in .4s both">Pick one</div>' + choice_list(),
         sfx=[("pop", 0.0), ("pop", .18), ("pop", .36), ("pop", .54), ("pop", .72)], min_len=1.8),
    Beat("Three seconds.",
         """<style>@keyframes ring{from{stroke-dashoffset:0}to{stroke-dashoffset:1100}}</style>
         <div style="margin-top:0;display:flex;justify-content:center"><svg width="620" height="620" viewBox="0 0 420 420">
         <circle cx="210" cy="210" r="175" stroke="#222" stroke-width="26" fill="none"/>
         <circle class=a cx="210" cy="210" r="175" stroke="#BFFBD1" stroke-width="26" fill="none" stroke-dasharray="1100"
           transform="rotate(-90 210 210)" style="animation:ring 3s linear both"/>
         <style>@keyframes s3{0%,33%{opacity:1}33.1%,100%{opacity:0}}@keyframes s2{0%,33%{opacity:0}33.1%,66%{opacity:1}66.1%,100%{opacity:0}}@keyframes s1{0%,66%{opacity:0}66.1%,100%{opacity:1}}</style>
         <text class=a x="210" y="250" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="130" fill="#fff" style="animation:s3 3s linear both">3</text>
         <text class=a x="210" y="250" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="130" fill="#fff" style="animation:s2 3s linear both">2</text>
         <text class=a x="210" y="250" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="130" fill="#fff" style="animation:s1 3s linear both">1</text>
         </svg></div><div class="mid a" style="text-align:center;margin-top:50px;animation:in .4s both">Think.</div>""",
         sfx=[("tick", 0.0), ("tick", 1.0), ("tick", 2.0)], min_len=3.2, caption="3 seconds. Think."),
    Beat("Start with one hundred dollars.", '<div class="big a" style="margin-top:0;animation:in .4s both">Start: $100</div>'
         + bar(0, 100, "", "$100"), sfx=[("pop", 0.3)]),
    Beat("Up twenty percent is twenty dollars more. Now it's one hundred twenty dollars.",
         '<div class="big a" style="margin-top:0;animation:in .4s both">Up 20%</div>' + bar(100, 120, "$100", "$120"),
         sfx=[("pop", 1.2)], caption="Up 20% is $20 more. Now it's $120."),
    Beat("Down twenty percent of one hundred twenty is twenty four dollars. That leaves ninety six dollars.",
         '<div class="big a" style="margin-top:0;animation:in .4s both">Down 20% of $120</div>'
         + bar(120, 96, "−$24", "$96", colour="#ffffff"), sfx=[("pop", 1.2)]),
    Beat("So you're down four percent. The answer is B.",
         '<div class="big a" style="margin-top:0;animation:in .4s both">$96 = <span class=mint>−4%</span></div>'
         + choice_list(highlight="B", delay=None), sfx=[("ding", 0.6)]),
    Beat("Zero is the trap. The second twenty percent comes off a bigger number.",
         '<div class="big a" style="margin-top:0;animation:in .4s both">Trap: <span class=mint>0%</span></div>'
         '<p class=a style="margin-top:50px;animation:in .4s .4s both">20% of $120 is more than 20% of $100.</p>'
         + choice_list(cross="A", delay=None), sfx=[("pop", 0.3)]),
    Beat("Shortcut. Twenty times twenty is four hundred. Divide by one hundred. You lose four percent.",
         '<div class="mid mint a" style="margin-top:0;animation:in .4s both">Shortcut</div>'
         '<div class="big a" style="margin-top:40px;animation:in .4s .3s both">20 × 20 = 400</div>'
         '<div class="big a" style="margin-top:20px;animation:in .4s 1.4s both">400 ÷ 100 = <span class=mint>4%</span></div>'
         '<p class=a style="margin-top:50px;animation:in .4s 2.4s both">Up then down by the same %: you always lose.</p>',
         sfx=[("pop", 0.3), ("pop", 1.4), ("ding", 2.4)]),
    Beat("Save this for your next percent question.",
         '<div class="big a" style="margin-top:0;animation:in .5s both">Save it.</div>'
         '<div class="mid a" style="margin-top:40px;animation:in .5s .4s both">@805scorelab</div>'
         f'<div style="margin-top:80px">{bubbles("B")}</div>', sfx=[("pop", 0.1)], pad_after=0.6),
]

COVER = f"""<style>{base_css('paper', height=1920)}
 .c{{position:absolute;top:420px;left:90px;right:90px}}</style><div class=frame><div class=c>
 <span class=chip>Shortcut</span><h1 style="margin-top:40px;font-size:124px">Up 20%.<br>Down 20%.<br>Where are you?</h1>
 <div style="margin-top:70px">{bubbles()}</div></div></div>"""

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "voiced"
    rid = ID if mode == "voiced" else ID + "-silent"
    res = build(rid, beats, COVER, voiced=(mode == "voiced"), seed=7)
    print(json.dumps(res, indent=1, default=float))
