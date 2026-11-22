"""Reel 2026-11-23-r1, series Trap Answer: average speed on a round trip. Voiced, score v1.

Original question for 805 Score Lab: you drive 120 miles at 60 mph, then the same 120 miles back at 40 mph. What is
your average speed for the round trip? (A) 45 (B) 48 (C) 50 (D) 52 (E) 55 mph. Answer B, verified in
build/items/2026-11-23-r1.py. Hand solution: 2 h out, 3 h back, 240 miles / 5 h = 48 mph.
Trap: C (50), averaging the speeds; more time is spent at 40. Difficulty: our estimate, medium.
Quality-log improvement applied: drawn diagrams filling the frame (a road with the car driving it, a time bar).
Usage: python3 posts/2026-11-23-r1.py
"""
import json
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import base_css, bubbles
from reel import Beat, build

ID = "2026-11-23-r1"
CHOICES = [("A", "45 mph"), ("B", "48 mph"), ("C", "50 mph"), ("D", "52 mph"), ("E", "55 mph")]


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


def road(direction, seconds, speed_label, time_label, colour="#BFFBD1"):
    """A drawn road from HOME to CITY filling the frame width; the car drives it in `seconds`."""
    x0, x1 = (60, 800) if direction == "out" else (800, 60)
    return f"""<style>@keyframes car{direction}{{from{{transform:translateX({x0}px)}}to{{transform:translateX({x1}px)}}}}
      @keyframes trail{direction}{{from{{stroke-dashoffset:740}}to{{stroke-dashoffset:0}}}}
      @keyframes lab{{0%,70%{{opacity:0}}100%{{opacity:1}}}}</style>
      <svg width="868" height="430" viewBox="0 0 868 430" style="margin-top:50px">
        <rect x="20" y="170" width="828" height="110" rx="20" fill="#151a17"/>
        <line x1="60" y1="225" x2="808" y2="225" stroke="#333" stroke-width="6" stroke-dasharray="30 24"/>
        <line class=a x1="{x0 + 10}" y1="225" x2="{x1 + 10}" y2="225" stroke="{colour}" stroke-width="10"
              stroke-dasharray="740" style="animation:trail{direction} {seconds}s .2s linear both"/>
        <circle cx="70" cy="225" r="22" fill="#fff"/><circle cx="798" cy="225" r="22" fill="#fff"/>
        <text x="70" y="140" text-anchor="middle" font-family="Inter" font-weight="700" font-size="38" fill="#fff">Home</text>
        <text x="798" y="140" text-anchor="middle" font-family="Inter" font-weight="700" font-size="38" fill="#fff">City</text>
        <text x="434" y="350" text-anchor="middle" font-family="Inter" font-weight="600" font-size="40" fill="#aaa">120 miles</text>
        <g class=a style="animation:car{direction} {seconds}s .2s linear both">
          <rect x="-34" y="196" width="88" height="46" rx="14" fill="{colour}"/>
          <circle cx="-14" cy="246" r="11" fill="#fff"/><circle cx="34" cy="246" r="11" fill="#fff"/></g>
      </svg>
      <div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:30px">
        <span class=mid>{speed_label}</span>
        <span class="big mint a" style="animation:lab {seconds + .4:.1f}s both">{time_label}</span></div>"""


def timebar(show_marker=True):
    """Five hours as five blocks: 2 at 60 mph, 3 at 40 mph. A marker slides to 48 on a 40 to 60 scale."""
    blocks = "".join(f'<div class=a style="flex:1;height:150px;border-radius:14px;background:{c};'
                     f'animation:pop .35s {i * .25:.2f}s both;display:flex;align-items:center;justify-content:center;'
                     f'font:800 44px Montserrat;color:{ink}">{t}</div>'
                     for i, (c, ink, t) in enumerate([("#BFFBD1", "#06142B", "60")] * 2 + [("#ffffff", "#000", "40")] * 3))
    marker = """<style>@keyframes mk{from{left:50%}to{left:40%}}</style>
      <div style="position:relative;margin-top:220px;height:12px;background:#333;border-radius:6px">
        <div class=a style="position:absolute;top:-34px;width:6px;height:80px;background:#BFFBD1;animation:mk 1.6s 1.4s both">
          <div class=big style="position:absolute;top:-130px;left:-60px;font-size:84px;color:#BFFBD1">48</div></div>
        <span class=mid style="position:absolute;left:0;top:50px;font-size:44px">40</span>
        <span class=mid style="position:absolute;left:46%;top:50px;font-size:44px;opacity:.5">50</span>
        <span class=mid style="position:absolute;right:0;top:50px;font-size:44px">60</span></div>""" if show_marker else ""
    return (f'<div class=mid style="font-size:56px">5 hours of driving</div>'
            f'<div style="display:flex;gap:14px;margin-top:36px">{blocks}</div>'
            f'<p style="margin-top:22px;opacity:.75">2 hours at 60, 3 hours at 40</p>{marker}')


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
    Beat("You drive one hundred twenty miles at sixty miles an hour, then drive back at forty. "
         "What is your average speed?",
         '<div class="big" style="font-size:112px">60 mph out.<br>40 mph back.</div>'
         '<div class="mid mint" style="margin-top:40px">Average speed?</div>'
         f'<div style="margin-top:70px">{bubbles()}</div>', sfx=[("pop", 0.1), ("pop", 1.6)]),
    Beat("Pick one.", '<div class="mid a" style="animation:in .4s both">Pick one</div>' + choice_list(),
         sfx=[("pop", t) for t in (0, .18, .36, .54, .72)], min_len=1.8),
    Beat("Three seconds.", COUNTDOWN, sfx=[("tick", 0.0), ("tick", 1.0), ("tick", 2.0)], min_len=3.2),
    Beat("Fifty feels right. But fifty is the trap.",
         '<div class="big a" style="font-size:96px;animation:in .4s both">(60 + 40) ÷ 2 = 50?</div>'
         + choice_list(cross="C", animate=False), sfx=[("thump", 1.2)]),
    Beat("Going out at sixty takes two hours.", road("out", 1.8, "60 mph", "2 hours"), sfx=[("pop", 2.1)]),
    Beat("Coming back at forty takes three hours.", road("back", 2.4, "40 mph", "3 hours", colour="#ffffff"),
         sfx=[("pop", 2.7)]),
    Beat("Two hundred forty miles in five hours is forty eight miles an hour. The answer is B.",
         '<div class="big a" style="animation:in .4s both">240 ÷ 5 = <span class=mint>48</span></div>'
         + choice_list(highlight="B", animate=False), sfx=[("ding", 2.6)]),
    Beat("You spend more time at the slower speed, so the average leans toward forty.", timebar(),
         sfx=[("pop", t) for t in (0, .25, .5, .75, 1.0)] + [("ding", 3.0)], min_len=3.4),
    Beat("Save this for your next rate question.",
         '<div class="big a" style="animation:in .5s both">Save it.</div>'
         '<div class="mid a" style="margin-top:40px;animation:in .5s .4s both">@805scorelab</div>'
         f'<div style="margin-top:80px">{bubbles("B")}</div>', sfx=[("pop", 0.1)], pad_after=0.6),
]

COVER = f"""<style>{base_css('forest', height=1920)}
 .c{{position:absolute;top:420px;left:90px;right:90px}}</style><div class=frame><div class=c>
 <span class=chip>Trap Answer</span><h1 style="margin-top:40px;font-size:124px">60 out.<br>40 back.<br>Not 50.</h1>
 <div style="margin-top:70px">{bubbles()}</div></div></div>"""

if __name__ == "__main__":
    res = build(ID, beats, COVER, voiced=True, seed=23)
    print(json.dumps(res["measures"], indent=1, default=float)[:1500])
