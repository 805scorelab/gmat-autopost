"""Reel 2026-11-26-r2, series Trap Answer: how many pens? Data Sufficiency (Data Insights). Voiced, score v1.

Original question for 805 Score Lab: pens cost $2 each and books $5 each. Ana bought only pens and books, at
least one of each. How many pens did she buy? (1) She spent $19 in total. (2) She bought 5 items.
Answer C, verified in build/items/2026-11-26-r2.py. (1): 7 pens + 1 book or 2 pens + 3 books, not sufficient.
(2): any split of 5, not sufficient. Together only 2 pens + 3 books (5 items, $19). Trap: A, believing the
whole-number limit leaves only one way to make $19.
Difficulty: our estimate, medium.
Quality-log improvement applied (previous row: motion 0.18, "more motion inside each beat"): every explanation beat
builds its picture item by item (pen and book tiles slide in one at a time, dollar totals count up).
Usage: python3 posts/2026-11-26-r2.py
"""
import json
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import bubbles
from reel import Beat, build
from reelkit import COUNTDOWN, MINT, RED, ds_key, cover, save_beat_scene, strike

ID = "2026-11-26-r2"
SPLITS_19 = [(p, n) for p in range(1, 10) for n in range(1, 4) if 2 * p + 5 * n == 19]
assert SPLITS_19 == [(2, 3), (7, 1)]
assert [(p, n) for p, n in SPLITS_19 if p + n == 5] == [(2, 3)]

PEN = '#BFFBD1'
BOOK = '#ffd166'


def tile(kind, d, size=78):
    col, lab = (PEN, "$2") if kind == "p" else (BOOK, "$5")
    w = size if kind == "p" else int(size * 1.5)
    return (f'<div class=a style="width:{w}px;height:{size + 30}px;border-radius:14px;background:{col};color:#000;'
            f'display:flex;align-items:center;justify-content:center;font:800 30px Montserrat;'
            + (f'animation:in .3s {d:.2f}s both' if d is not None else '') + f'">{lab}</div>')


def basket(p, n, start, step=0.18, total=True, cross=False, ok=False):
    tiles = "".join(tile("p", start + i * step) for i in range(p))
    tiles += "".join(tile("n", start + (p + i) * step) for i in range(n))
    end = start + (p + n) * step + 0.1
    tag = ""
    if total:
        tag = (f'<div class=a style="font:800 66px Montserrat;margin-left:auto;animation:pop .35s {end:.2f}s both">'
               f'${2 * p + 5 * n}</div>')
    mark = ""
    if cross:
        mark = strike(end + 0.8, 10)
    if ok:
        mark = (f'<span class=a style="position:absolute;left:-14px;right:-14px;top:-14px;bottom:-14px;'
                f'border:8px solid {MINT};border-radius:24px;animation:pop .4s {end + 0.8:.2f}s both"></span>')
    return (f'<div style="position:relative;display:flex;align-items:center;gap:12px;margin-top:34px">'
            f'{tiles}{tag}{mark}</div>'
            f'<div class=a style="font:700 44px Inter;color:#bbb;margin-top:10px;animation:in .3s {end:.2f}s both">'
            f'{p} pen{"s" if p > 1 else ""} + {n} book{"s" if n > 1 else ""} = {p + n} items</div>')


HOOK = ('<div style="display:flex;gap:40px;align-items:center">' + tile("p", None, 110) + '<span class=mid>pen</span>'
        + tile("n", None, 110) + '<span class=mid>book</span></div>'
        '<div class=big style="font-size:104px;margin-top:40px">How many pens?</div>'
        '<div class=mid style="font-size:56px;color:#bbb;margin-top:16px">At least 1 of each.</div>'
        '<div class="mid a" style="margin-top:40px;font-size:64px;animation:in .4s 3.6s both">(1) You spend $19.</div>'
        '<div class="mid a" style="margin-top:14px;font-size:64px;animation:in .4s 5.4s both">(2) You buy 5 items.</div>'
        f'<div style="margin-top:50px">{bubbles()}</div>')

beats = [
    Beat("A pen costs two dollars. A book costs five dollars. You buy at least one of each. How many pens? "
         "Statement one: you spend nineteen dollars. Statement two: you buy five items.",
         HOOK, sfx=[("pop", 3.6), ("pop", 5.4)]),
    Beat("Which statements are enough?",
         '<div class="mid a" style="animation:in .4s both">Enough to answer?</div>' + ds_key(),
         sfx=[("pop", t) for t in (0, .18, .36, .54, .72)], min_len=2.0),
    Beat("Three seconds.", COUNTDOWN, sfx=[("tick", 0.0), ("tick", 1.0), ("tick", 2.0)], min_len=3.2),
    Beat("Statement one. Seven pens plus one book make nineteen dollars. Two pens plus three books cost the same. "
         "Not enough.",
         '<div class="mid" style="font-size:66px">(1) $19</div>' + basket(7, 1, 0.3) + basket(2, 3, 3.4)
         + '<p class=a style="margin-top:40px;font-size:58px;color:#ff6b6b;animation:in .4s 5.4s both">'
         '7 pens or 2 pens. Not sufficient.</p>',
         sfx=[("pop", 1.9), ("pop", 4.5), ("thump", 5.4)]),
    Beat("Statement two. Five items can split many ways. Not enough.",
         '<div class="mid" style="font-size:66px">(2) 5 items</div>' + basket(1, 4, 0.3, total=False)
         + basket(4, 1, 1.4, total=False)
         + '<p class=a style="margin-top:40px;font-size:58px;color:#ff6b6b;animation:in .4s 2.6s both">'
         'Any split works. Not sufficient.</p>', sfx=[("pop", 1.2), ("pop", 2.3), ("thump", 2.6)]),
    Beat("Together. Seven pens and a book is eight items. Only two pens fit both. So pick C.",
         '<div class="mid" style="font-size:66px">Both: $19 and 5 items</div>'
         + basket(7, 1, 0.2, step=0.06, cross=True) + basket(2, 3, 0.8, step=0.06, ok=True)
         + '<div class="big a" style="font-size:110px;margin-top:40px;animation:pop .45s 3.2s both">'
         '2 pens: <span class=mint>C</span></div>', sfx=[("thump", 1.5), ("ding", 3.2)]),
    Beat("The trap is answer A. Whole numbers can still leave two answers.",
         '<div class="big a" style="animation:in .4s both">Trap: <span class=mint>A</span></div>'
         '<p class=a style="margin-top:40px;animation:in .4s .4s both">“Only whole numbers” does not mean only one way.'
         '</p>' + ds_key(cross="A", animate=False), sfx=[("thump", 0.5)]),
    Beat("Save this for your next data sufficiency question.", save_beat_scene("C"), sfx=[("pop", 0.1)],
         pad_after=0.6),
]

COVER = cover("mint", "Trap Answer", "$19 spent.<br>How many pens?", 118)

if __name__ == "__main__":
    res = build(ID, beats, COVER, voiced=True, seed=89)
    print(json.dumps({k: v for k, v in res["measures"].items() if k != "takes"}, default=float))
