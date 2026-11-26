"""Reel 2026-11-29-r2, series Trap Answer: by what percent did the price go up? Data Sufficiency (Data Insights).
Voiced, score v1.

Original question for 805 Score Lab: the price of a lamp went up. By what percent did it go up?
(1) The price went up by $12. (2) The new price is $72.
Answer C, verified in build/items/2026-11-29-r2.py. (1): $12 on $60 is 20%, on $40 is 30%: not sufficient.
(2): the old price could be anything below $72: not sufficient. Together: old = 72 - 12 = 60, 12 / 60 = 20%.
Trap: E, waiting for the old price to be stated when it follows from new minus increase.
Difficulty: our estimate, easy to medium.
Quality-log improvements applied (previous rows: 43.7 s too long; lit tiles with mix-blend text read blue): short
script aimed at about 35 s, lit price bars use fixed dark text.
Usage: python3 posts/2026-11-29-r2.py
"""
import json
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import bubbles
from reel import Beat, build
from reelkit import COUNTDOWN, MINT, RED, ds_key, cover, save_beat_scene, strike

ID = "2026-11-29-r2"
assert 12 / 60 == 0.2 and 12 / 40 == 0.3 and 72 - 12 == 60
GOLD = "#ffd166"


def bar(old, inc, d, old_label=None, inc_label=None, pct=None, ok=True, scale=8.0, still=False):
    """A price bar: old part (grey) then the increase (gold) growing in at delay d; a percent chip pops after."""
    w_old, w_inc = int(old * scale), int(inc * scale)
    chip = ""
    if pct:
        col = MINT if ok else GOLD
        chip = (f'<span class=a style="margin-left:20px;padding:4px 20px;border-radius:16px;background:{col};'
                f'color:#111;font:800 52px Montserrat;animation:pop .35s {d + 0.7:.2f}s both">{pct}</span>')
    return ('<style>@keyframes growx{from{transform:scaleX(0)}to{transform:none}}</style>'
            f'<div class=a style="display:flex;align-items:center;margin-top:34px;'
            f'{"" if still else f"animation:in .3s {d:.2f}s both"}">'
            f'<div style="width:{w_old}px;height:110px;border-radius:18px 0 0 18px;background:#3a3a3a;display:flex;'
            f'align-items:center;justify-content:center;font:800 50px Montserrat;color:#fff">{old_label or ""}</div>'
            f'<div class=a style="width:{w_inc}px;height:110px;border-radius:0 18px 18px 0;background:{GOLD};'
            f'transform-origin:left;display:flex;align-items:center;justify-content:center;font:800 44px Montserrat;'
            f'color:#111;{"" if still else f"animation:growx .4s {d + 0.3:.2f}s both"}">{inc_label or ""}</div>{chip}</div>')


HOOK = ('<div class=big style="font-size:100px">Price went up.<br>By what <span class=mint>%</span>?</div>'
        + bar(60, 12, 0.0, "old ?", "+?", scale=11.0, still=True)
        + '<div class="mid a" style="margin-top:50px;font-size:70px;animation:in .4s 2.2s both">(1) Up by $12.</div>'
        '<div class="mid a" style="margin-top:16px;font-size:70px;animation:in .4s 3.6s both">(2) New price $72.</div>'
        f'<div style="margin-top:50px">{bubbles()}</div>')

beats = [
    Beat("A price went up. By what percent? Statement one: it went up by twelve dollars. "
         "Statement two: the new price is seventy-two dollars.",
         HOOK, sfx=[("pop", 2.2), ("pop", 3.6)]),
    Beat("Which statements are enough?",
         '<div class="mid a" style="animation:in .4s both">Enough to answer?</div>' + ds_key(),
         sfx=[("pop", t) for t in (0, .18, .36, .54, .72)], min_len=2.0),
    Beat("Three seconds.", COUNTDOWN, sfx=[("tick", 0.0), ("tick", 1.0), ("tick", 2.0)], min_len=3.2),
    Beat("Each statement alone leaves the old price open. If the old price was sixty dollars, that is twenty "
         "percent. If it was forty dollars, it is thirty percent.",
         '<div class=mid style="font-size:66px">(1) alone: +$12</div>'
         + bar(60, 12, 0.4, "$60", "+12", "20%", True)
         + bar(40, 12, 2.6, "$40", "+12", "30%", False)
         + '<p class=a style="margin-top:50px;font-size:60px;color:#ff6b6b;animation:in .4s 4.2s both">'
           'Two answers. Not sufficient. Same for (2).</p>',
         sfx=[("pop", 1.1), ("pop", 3.3), ("thump", 4.2)]),
    Beat("Together, the old price is seventy-two minus twelve, which is sixty. Twelve out of sixty is twenty percent. "
         "So it is answer C.",
         '<div class=mid style="font-size:66px">Together</div>'
         '<div class="big a" style="font-size:96px;margin-top:30px;animation:pop .4s .4s both">72 − 12 = '
         '<span class=mint>60</span></div>'
         + bar(60, 12, 1.6, "$60", "+12", "20%", True)
         + '<div class=a style="margin-top:30px;animation:in .4s 3.4s both">' + ds_key(highlight="C", animate=False)
         + '</div>',
         sfx=[("pop", 0.4), ("ding", 2.3)]),
    Beat("The trap is answer E. You never get the old price, but new minus increase gives it.",
         '<div class="big a" style="animation:in .4s both">Trap: <span class=mint>E</span></div>'
         '<div style="font:800 96px Montserrat;margin-top:50px"><span style="position:relative">“No old price”'
         + strike(1.2, 12) + '</span></div>'
         '<p class=a style="margin-top:40px;font-size:60px;animation:in .4s 1.8s both">old = new − increase</p>'
         '<p class=a style="margin-top:14px;font-size:60px;animation:in .4s 2.6s both">Combine before you give up.</p>',
         sfx=[("thump", 1.2)]),
    Beat("Save this for your next data sufficiency question.", save_beat_scene("C"), sfx=[("pop", 0.1)],
         pad_after=0.6),
]

COVER = cover("mint", "Trap Answer", "Price went up.<br>By what %?<br>2 clues.", 118)

if __name__ == "__main__":
    res = build(ID, beats, COVER, voiced=True, seed=113)
    print(json.dumps({k: v for k, v in res["measures"].items() if k != "takes"}, default=float))
