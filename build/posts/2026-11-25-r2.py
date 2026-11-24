"""Reel 2026-11-25-r2, series 60-Second Challenge: Critical Reasoning flaw, biased sample. Verbal. Voiced, score v1.

Original question for 805 Score Lab:
  A gym asked members at its 6 a.m. classes when they like to train. Almost all said mornings. The manager concludes
  that most of the gym's members prefer mornings. Which is the flaw?
  (A) It generalizes from members who were all at morning classes.  (B) It ignores that morning classes may cost
  more.  (C) It treats "almost all" as if it meant "all".  (D) It relies on the manager's view, not members' answers.
  (E) It assumes morning fans never train at night.
Answer A. Everyone asked was already at a 6 a.m. class, so the sample is drawn from the people most likely to like
mornings; members who train later were never asked, yet the conclusion is about all members.
Why each wrong choice fails:
  B: price is never mentioned and has nothing to do with whether the sample represents all members.
  C: the trap. The conclusion only says "most", and "almost all" of the sample does give "most" of the sample; the
     argument never needs "all". The step that fails is sample to population, not the quantity word.
  D: the conclusion rests on the members' own answers, not on the manager's opinion.
  E: preferring mornings does not require never training at night, and the argument needs no such assumption.
Only A names the gap the conclusion depends on, so no second choice is defensible. The quantity step behind C is
checked below. Difficulty: our estimate, easy to medium.
Quality-log improvement applied (last row: "give the stimulus beat a moving picture"): the stimulus beat draws the
gym's members as a grid of dots and rings the 6 a.m. group as it is described; the explanation reuses the picture.
Usage: python3 posts/2026-11-25-r2.py
"""
import json
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import base_css, bubbles
from reel import Beat, build

ID = "2026-11-25-r2"
RED = "#ff6b6b"

# C fails: "almost all" (read as at least 90%) of a group is always "most" (over 50%) of that same group.
assert all(n * 9 // 10 > n / 2 for n in range(2, 1000) if n * 9 % 10 == 0), "almost all must give most"

CHOICES = [("A", "It generalizes from members who were all at morning classes."),
           ("B", "It ignores that morning classes may cost more."),
           ("C", "It treats “almost all” as if it meant “all”."),
           ("D", "It relies on the manager's view, not members' answers."),
           ("E", "It assumes morning fans never train at night.")]


def choice_list(highlight=None, cross=None, animate=True):
    rows = []
    for i, (l, v) in enumerate(CHOICES):
        on = " on" if l == highlight else ""
        anim = f"animation:pop .35s {i * .18:.2f}s both" if animate else ""
        dim = "opacity:.45;" if highlight and l != highlight else ""
        x = (f'<span class=a style="position:absolute;left:-6px;right:-6px;top:50%;height:7px;background:{RED};'
             'transform-origin:left;animation:grow .4s .5s both"></span>') if l == cross else ""
        rows.append(f'<div style="display:flex;align-items:center;gap:30px;margin-top:24px;{dim}">'
                    f'<div class="bubble{on} a" style="flex:none;{anim}">{l}</div>'
                    f'<span style="position:relative;font:600 44px/1.2 Inter">{v}{x}</span></div>')
    return "".join(rows)


def gym(ring_at=1.0, rest_at=None, height=520):
    """The gym's members as an 8 x 5 grid of dots. The first two columns are the 6 a.m. group: they light mint and a
    ring is drawn round them at ring_at. If rest_at is set, the other dots dim and get a 'never asked' label."""
    cols, rows, gx, gy = 8, 5, 104, 92
    dots = ""
    for c in range(cols):
        for r in range(rows):
            x, y = 60 + c * gx, 120 + r * gy
            d = 0.05 * (c + r)
            morning = c < 2
            fill = "#BFFBD1" if morning else "#ffffff"
            anim = f"animation:pop .35s {d:.2f}s both"
            op = ""
            if rest_at is not None and not morning:
                op = f';opacity:1;animation:pop .35s {d:.2f}s both, fadeq .5s {rest_at + 0.02 * c:.2f}s both'
                anim = ""
            dots += (f'<circle class=a cx="{x}" cy="{y}" r="30" fill="{fill}" '
                     f'style="transform-box:fill-box;transform-origin:center;{anim}{op}"/>')
    ring = (f'<rect class=a x="12" y="66" width="200" height="{rows * gy + 16}" rx="40" fill="none" stroke="#BFFBD1" '
            f'stroke-width="10" stroke-dasharray="1400" style="animation:dr 1s {ring_at:.2f}s both"/>'
            f'<text class=a x="112" y="44" text-anchor="middle" font-family="Montserrat" font-weight="800" '
            f'font-size="40" fill="#BFFBD1" style="animation:in .4s {ring_at + .5:.2f}s both">asked</text>')
    sun = (f'<g class=a style="animation:pop .4s {ring_at + .8:.2f}s both;transform-box:fill-box;transform-origin:center">'
           f'<circle cx="112" cy="{120 + rows * gy + 30}" r="20" fill="#ffd166"/></g>'
           f'<text class=a x="150" y="{120 + rows * gy + 44}" font-family="Inter" font-weight="700" font-size="40" '
           f'fill="#ffd166" style="animation:in .4s {ring_at + .9:.2f}s both">6 a.m.</text>')
    rest = ""
    if rest_at is not None:
        rest = (f'<rect class=a x="232" y="66" width="{cols * gx - 2 * gx + 20}" height="{rows * gy + 16}" rx="40" '
                f'fill="none" stroke="{RED}" stroke-width="10" stroke-dasharray="20 18" '
                f'style="animation:in .5s {rest_at + .4:.2f}s both"/>'
                f'<text class=a x="{232 + (cols - 2) * gx / 2 + 10}" y="44" text-anchor="middle" font-family="Montserrat" '
                f'font-weight="800" font-size="40" fill="{RED}" style="animation:in .4s {rest_at + .6:.2f}s both">'
                f'never asked</text>')
    return (f'<svg width="868" height="{height}" viewBox="0 0 868 {height}" style="margin-top:40px">'
            '<style>@keyframes dr{from{stroke-dashoffset:1400}to{stroke-dashoffset:0}}'
            '@keyframes fadeq{from{opacity:1}to{opacity:.25}}</style>'
            f'{dots}{ring}{sun}{rest}</svg>')


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

STIM = ('<div class=big style="font-size:92px;margin-bottom:30px">Find the flaw.</div>'
        '<div class=mid style="font-size:56px;line-height:1.22">A gym asks members at its <span class=mint>6&nbsp;a.m.'
        '</span> classes when they like to train.</div>'
        '<div class="mid a" style="font-size:56px;line-height:1.22;margin-top:24px;animation:in .4s 3.2s both">'
        'Almost all say mornings. So <span class=mint>most members</span> prefer mornings.</div>'
        + gym(ring_at=1.2, height=640))

BAR = (f'<div style="position:relative;margin-top:70px;height:120px;border-radius:24px;background:#1c1c1c">'
       f'<div class=a style="position:absolute;left:0;top:0;bottom:0;width:92%;border-radius:24px;background:#BFFBD1;'
       f'transform-origin:left;animation:grow 1.2s .6s both"></div>'
       f'<div class=a style="position:absolute;left:50%;top:-30px;bottom:-30px;width:8px;background:#fff;'
       f'animation:in .3s 1.8s both"></div></div>'
       f'<div style="position:relative;height:90px;font:800 48px Montserrat">'
       f'<span class=a style="position:absolute;left:50%;transform:translateX(-50%);top:40px;animation:in .3s 1.9s both">'
       f'most</span><span class="a mint" style="position:absolute;right:0;top:40px;animation:in .3s 1.2s both">'
       f'almost all</span></div>')

beats = [
    Beat("A gym asked members at its early morning classes when they like to train. Almost all said mornings. "
         "So most members prefer mornings. What is the flaw?", STIM,
         sfx=[("pop", 1.2), ("pop", 3.2)]),
    Beat("Pick one.", '<div class="mid a" style="animation:in .4s both">Pick one</div>' + choice_list(),
         sfx=[("pop", t) for t in (0, .18, .36, .54, .72)], min_len=3.0),
    Beat("Three seconds.", COUNTDOWN, sfx=[("tick", 0.0), ("tick", 1.0), ("tick", 2.0)], min_len=3.2),
    Beat("Everyone asked was already at a morning class. The night crowd was never asked.",
         '<div class="mid a" style="animation:in .4s both">Who was asked?</div>' + gym(ring_at=0.2, rest_at=2.4),
         sfx=[("pop", 0.2), ("thump", 2.8)], min_len=4.4),
    Beat("So the answers can't speak for every member. Pick A.",
         '<div class="big a" style="font-size:104px;animation:in .4s both">Answer: <span class=mint>A</span></div>'
         + choice_list(highlight="A", animate=False), sfx=[("ding", 2.2)]),
    Beat("C is the trap. Almost all is more than most, so that step is fine.",
         '<div class="big a" style="font-size:104px;animation:in .4s both">Trap: <span class=mint>C</span></div>'
         + BAR + '<p class=a style="margin-top:40px;animation:in .4s 2.6s both">The leap is from the 6&nbsp;a.m. group to '
         'everyone.</p>', sfx=[("pop", 0.6), ("thump", 1.8)]),
    Beat("Save this for your next critical reasoning question.",
         '<div class="big a" style="animation:in .5s both">Save it.</div>'
         '<div class="mid a" style="margin-top:40px;animation:in .5s .4s both">@805scorelab</div>'
         f'<div style="margin-top:80px">{bubbles("A")}</div>', sfx=[("pop", 0.1)], pad_after=0.6),
]

COVER = f"""<style>{base_css('paper', height=1920)}
 .c{{position:absolute;top:420px;left:90px;right:90px}}</style><div class=frame><div class=c>
 <span class=chip>60-Second Challenge</span><h1 style="margin-top:40px;font-size:118px">Who did<br>the gym ask?</h1>
 <div style="margin-top:70px">{bubbles()}</div></div></div>"""

if __name__ == "__main__":
    res = build(ID, beats, COVER, voiced=True, seed=79)
    print(json.dumps({k: v for k, v in res["measures"].items() if k != "takes"}, default=float))
