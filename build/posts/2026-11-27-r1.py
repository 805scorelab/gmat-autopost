"""Reel 2026-11-27-r1, series Shortcut: remainder of 5,738 divided by 9 (digit sum). Quant. Voiced, score v1.

Original question for 805 Score Lab: what is the remainder when 5,738 is divided by 9? (A) 2 (B) 3 (C) 5 (D) 7 (E) 8.
Answer C, verified in build/items/2026-11-27-r1.py. A number leaves the same remainder on division by 9 as its digit
sum: 5 + 7 + 3 + 8 = 23, 2 + 3 = 5. Check: 9 x 637 = 5,733 and 5,738 - 5,733 = 5. Trap: E (8), the last digit, which
is the remainder on division by 10.
Difficulty: our estimate, easy to medium.
Quality-log improvement applied (previous row: keep motion up and the first state on screen at frame 0): digit
tiles are on screen at frame 0 and then fly into the running sum, the sum counts up digit by digit.
Usage: python3 posts/2026-11-27-r1.py
"""
import json
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import bubbles
from reel import Beat, build
from reelkit import COUNTDOWN, MINT, RED, choice_list, cover, save_beat_scene, strike

ID = "2026-11-27-r1"
CHOICES = [("A", "2"), ("B", "3"), ("C", "5"), ("D", "7"), ("E", "8")]
assert 5738 % 9 == 5 and sum(map(int, "5738")) == 23 and 23 % 9 == 5 and 9 * 637 == 5733

HOOK = ('<div class=big style="font-size:170px;white-space:nowrap">5,738 ÷ 9</div>'
        '<div class=mid style="margin-top:30px">remainder?</div>'
        '<div class="mid a" style="margin-top:30px;color:#999;font-size:60px;animation:in .4s 2.6s both">'
        'No long division.</div>'
        f'<div style="margin-top:70px">{bubbles()}</div>')


def digit_tiles(digits, start=0.6, step=0.7, final=None):
    """Digit tiles shown at frame 0; each one lights mint in turn while a running total underneath counts up."""
    tiles = ""
    for i, ch in enumerate(digits):
        d = start + i * step
        tiles += (f'<div style="position:relative;width:170px;height:200px;border-radius:24px;background:#222;'
                  f'display:flex;align-items:center;justify-content:center;font:800 130px Montserrat">'
                  f'<div class=a style="position:absolute;inset:0;border-radius:24px;background:{MINT};'
                  f'animation:pop .3s {d:.2f}s both"></div>'
                  f'<span style="position:relative;mix-blend-mode:difference">{ch}</span></div>')
    totals, run = "", 0
    for i, ch in enumerate(digits):
        run += int(ch)
        d = start + i * step + 0.15
        nxt = start + (i + 1) * step + 0.15
        last = i == len(digits) - 1
        anim = (f"animation:show {nxt - d:.2f}s {d:.2f}s both" if not last else f"animation:pop .35s {d:.2f}s both")
        totals += (f'<span class=a style="position:absolute;left:0;{anim}">{run}</span>')
    end = start + len(digits) * step
    out = (f'<style>@keyframes show{{0%{{opacity:0}}1%,99%{{opacity:1}}100%{{opacity:0}}}}</style>'
           f'<div style="display:flex;gap:24px;margin-top:40px">{tiles}</div>'
           f'<div style="display:flex;align-items:baseline;gap:30px;margin-top:60px;font:800 150px Montserrat">'
           f'<span style="color:#999;font-size:80px">sum</span>'
           f'<span style="position:relative;display:inline-block;width:240px;height:160px;color:{MINT}">{totals}</span>'
           f'</div>')
    if final:
        out += f'<p class=a style="margin-top:30px;font-size:60px;animation:in .4s {end + .3:.2f}s both">{final}</p>'
    return out


beats = [
    Beat("What is the remainder when five thousand seven hundred thirty-eight is divided by nine?", HOOK,
         sfx=[("pop", 2.6)]),
    Beat("Pick one.", '<div class="mid a" style="animation:in .4s both">Pick one</div>'
         + choice_list(CHOICES, font="800 80px Montserrat", gap=26),
         sfx=[("pop", t) for t in (0, .18, .36, .54, .72)], min_len=2.0),
    Beat("Three seconds.", COUNTDOWN, sfx=[("tick", 0.0), ("tick", 1.0), ("tick", 2.0)], min_len=3.2),
    Beat("Skip long division. Add each digit instead. Five plus seven plus three plus eight equals twenty-three.",
         '<div class=mid>Add the digits.</div>' + digit_tiles("5738", start=1.6, step=0.75),
         sfx=[("pop", 1.6), ("pop", 2.35), ("pop", 3.1), ("pop", 3.85)], min_len=4.6),
    Beat("Still more than nine? Add again. Two plus three is five. That is the remainder.",
         '<div class=mid>Add again.</div>' + digit_tiles("23", start=1.2, step=0.8,
                                                        final="Same remainder as 5,738 ÷ 9"),
         sfx=[("pop", 1.2), ("ding", 2.0)], min_len=3.6),
    Beat("Check it. Nine goes into five thousand seven hundred thirty-three. Five is left over. So pick C.",
         '<div class="big a" style="font-size:104px;animation:in .4s both">Answer: <span class=mint>C</span></div>'
         '<div style="font:800 80px Montserrat;margin-top:50px">'
         '<div class=a style="animation:in .35s .6s both">9 × 637 = 5,733</div>'
         '<div class=a style="margin-top:20px;animation:in .35s 2.2s both">5,738 − 5,733 = '
         '<span class=mint>5</span></div></div>'
         + '<div class=a style="margin-top:50px;animation:in .4s 3.4s both">'
         + choice_list(CHOICES, highlight="C", animate=False, font="800 60px Montserrat", gap=12) + '</div>',
         sfx=[("pop", 0.6), ("pop", 2.2), ("ding", 3.4)]),
    Beat("The trap is answer E. The last digit gives the remainder for ten, not for nine.",
         '<div class="big a" style="font-size:104px;animation:in .4s both">Trap: <span class=mint>E</span></div>'
         '<div style="font:800 140px Montserrat;margin-top:60px">5,73<span style="position:relative;color:#ffd166">8'
         + strike(1.6, 12) + '</span></div>'
         '<p class=a style="margin-top:40px;animation:in .4s .9s both">Last digit → remainder for 10.</p>'
         '<p class=a style="margin-top:14px;animation:in .4s 2.4s both"><span class=mint>Digit sum</span> → '
         'remainder for 9.</p>', sfx=[("thump", 1.6)]),
    Beat("Save this for your next remainder question.", save_beat_scene("C"), sfx=[("pop", 0.1)], pad_after=0.6),
]

COVER = cover("paper", "Shortcut", "5,738 ÷ 9.<br>Remainder?", 124)

if __name__ == "__main__":
    res = build(ID, beats, COVER, voiced=True, seed=97)
    print(json.dumps({k: v for k, v in res["measures"].items() if k != "takes"}, default=float))
