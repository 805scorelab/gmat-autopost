"""Reel 2026-11-28-r2, series Trap Answer: is n odd? Data Sufficiency (Data Insights). Voiced, score v1.

Original question for 805 Score Lab: n is an integer. Is n odd? (1) 3n is odd. (2) n + n is even.
Answer A, verified in build/items/2026-11-28-r2.py. (1): 3 x even is even, 3 x odd is odd, so 3n odd forces n odd:
sufficient. (2): n + n = 2n is even for every integer, so it says nothing: not sufficient. Trap: D, treating (2) as
information.
Spoken lines say "the number" instead of the letter n (single letters mid-line fail the word check).
Difficulty: our estimate, easy to medium.
Quality-log improvements applied: frame-0 picture fills the width (integer tiles 1 to 6), every explanation beat
builds tile by tile.
Usage: python3 posts/2026-11-28-r2.py
"""
import json
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import bubbles
from reel import Beat, build
from reelkit import COUNTDOWN, MINT, RED, ds_key, cover, save_beat_scene, strike

ID = "2026-11-28-r2"
assert all((3 * n) % 2 == n % 2 for n in range(-50, 51)) and all((n + n) % 2 == 0 for n in range(-50, 51))
GOLD = "#ffd166"


def int_tiles(nums, start=None, step=0.25, size=124):
    """Integer tiles on screen at frame 0; from `start` the odd ones light mint and the even ones gold."""
    out = ""
    for i, n in enumerate(nums):
        col = MINT if n % 2 else GOLD
        light = ""
        if start is not None:
            light = (f'<div class=a style="position:absolute;inset:0;border-radius:20px;background:{col};'
                     f'animation:pop .3s {start + i * step:.2f}s both"></div>')
        out += (f'<div style="position:relative;width:{size}px;height:{int(size * 1.2)}px;border-radius:20px;'
                f'background:#222;display:flex;align-items:center;justify-content:center;font:800 74px Montserrat">'
                f'{light}<span style="position:relative;mix-blend-mode:difference">{n}</span></div>')
    return f'<div style="display:flex;gap:18px;margin-top:30px">{out}</div>'


def row(text, result, d, ok):
    col = MINT if ok else GOLD
    return (f'<div class=a style="display:flex;align-items:center;gap:30px;margin-top:30px;font:800 82px Montserrat;'
            f'animation:in .35s {d:.2f}s both"><span>{text}</span>'
            f'<span class=a style="padding:6px 26px;border-radius:18px;background:{col};color:#000;font-size:60px;'
            f'animation:pop .35s {d + 0.5:.2f}s both">{result}</span></div>')


HOOK = ('<div class=big style="font-size:120px">Is n odd?</div>'
        '<div class=mid style="font-size:54px;color:#bbb;margin-top:14px">n is an integer.</div>'
        + int_tiles([1, 2, 3, 4, 5, 6], start=0.4, step=0.2)
        + '<div class="mid a" style="margin-top:50px;font-size:70px;animation:in .4s 2.6s both">(1) 3n is odd.</div>'
        '<div class="mid a" style="margin-top:16px;font-size:70px;animation:in .4s 4.4s both">(2) n + n is even.</div>'
        f'<div style="margin-top:50px">{bubbles()}</div>')

beats = [
    Beat("Is the number odd? It is a whole number. Statement one: three times the number is odd. "
         "Statement two: the number plus itself is even.",
         HOOK, sfx=[("pop", 2.6), ("pop", 4.4)]),
    Beat("Which statements are enough?",
         '<div class="mid a" style="animation:in .4s both">Enough to answer?</div>' + ds_key(),
         sfx=[("pop", t) for t in (0, .18, .36, .54, .72)], min_len=2.0),
    Beat("Three seconds.", COUNTDOWN, sfx=[("tick", 0.0), ("tick", 1.0), ("tick", 2.0)], min_len=3.2),
    Beat("Statement one. Three times an even number is even. Three times an odd number is odd. "
         "So an odd result means the number is odd. Enough.",
         '<div class=mid style="font-size:66px">(1) 3n is odd</div>'
         + row("3 × 4 = 12", "even", 0.6, False) + row("3 × 5 = 15", "odd", 2.4, True)
         + '<p class=a style="margin-top:50px;font-size:60px;color:#BFFBD1;animation:in .4s 4.4s both">'
         'Odd result → n odd. Sufficient.</p>',
         sfx=[("pop", 1.1), ("pop", 2.9), ("ding", 4.4)]),
    Beat("Statement two. The number plus itself is twice the number. That is always even, odd number or not. "
         "Not enough.",
         '<div class=mid style="font-size:66px">(2) n + n is even</div>'
         + row("4 + 4 = 8", "even", 0.6, False) + row("5 + 5 = 10", "even", 2.0, False)
         + '<p class=a style="margin-top:50px;font-size:60px;color:#ff6b6b;animation:in .4s 3.6s both">'
         'Always even. Not sufficient.</p>',
         sfx=[("pop", 1.1), ("pop", 2.5), ("thump", 3.6)]),
    Beat("Statement one works alone. Statement two never does. So it is answer A.",
         '<div class="big a" style="font-size:110px;animation:pop .45s .2s both">(1) alone: '
         '<span class=mint>A</span></div><div style="margin-top:30px">' + ds_key(highlight="A") + '</div>',
         sfx=[("ding", 0.2)]),
    Beat("The trap is answer D. Statement two is true for every whole number, so it tells you nothing.",
         '<div class="big a" style="animation:in .4s both">Trap: <span class=mint>D</span></div>'
         '<div style="font:800 110px Montserrat;margin-top:50px"><span style="position:relative">n + n = 2n'
         '</span></div>'
         + int_tiles([1, 2, 3, 4, 5, 6], start=0.8, step=0.2)
         + '<p class=a style="margin-top:40px;font-size:58px;animation:in .4s 2.2s both">Every n passes (2).</p>'
         '<p class=a style="margin-top:14px;font-size:58px;animation:in .4s 3.2s both">A statement that is '
         '<span class=mint>always true</span> rules nothing out.</p>', sfx=[("thump", 2.2)]),
    Beat("Save this for your next data sufficiency question.", save_beat_scene("A"), sfx=[("pop", 0.1)],
         pad_after=0.6),
]

COVER = cover("paper", "Trap Answer", "Is n odd?<br>2 clues.", 124)

if __name__ == "__main__":
    res = build(ID, beats, COVER, voiced=True, seed=107)
    print(json.dumps({k: v for k, v in res["measures"].items() if k != "takes"}, default=float))
