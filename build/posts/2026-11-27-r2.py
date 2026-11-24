"""Reel 2026-11-27-r2, series 60-Second Challenge: Critical Reasoning weaken, phone ban. Verbal. Voiced, score v1.

Original question for 805 Score Lab:
  This fall, a school banned phones in class. By winter, test scores had risen. The principal concludes that the ban
  raised the scores. Which choice most weakens the conclusion?
  (A) Students say they miss having their phones.  (B) This fall, the school also began daily tutoring in every
  class.  (C) Scores rose more in math than in reading.  (D) Several other schools have similar phone rules.
  (E) Some students still used phones at lunch.
Answer B. Daily tutoring started at the same time and could have raised the scores, so the rise no longer points to
the ban alone.
Why each wrong choice fails:
  A: how students feel about the ban says nothing about what raised the scores.
  C: both subjects still rose; a different size of rise does not offer another cause.
  D: other schools' rules say nothing about why this school's scores rose.
  E: the trap. The ban covers class time; phone use at lunch does not touch class time and gives no other cause.
Only B gives an alternative cause, so no second choice is defensible. Difficulty: our estimate, easy.
Quality-log improvement applied: the stimulus picture (crossed-out phone and score bars) is complete at frame 0;
only the last bar's rise and the arrow animate. The explanation reuses the same cause-arrow picture.
Usage: python3 posts/2026-11-27-r2.py
"""
import json
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from reel import Beat, build
from reelkit import COUNTDOWN, MINT, RED, choice_list, cover, save_beat_scene

ID = "2026-11-27-r2"
CHOICES = [("A", "Students say they miss having their phones."),
           ("B", "This fall the school also began daily tutoring in every class."),
           ("C", "Scores rose more in math than in reading."),
           ("D", "Several other schools have similar phone rules."),
           ("E", "Some students still used phones at lunch.")]

PHONE = (f'<svg width="200" height="260" viewBox="0 0 200 260"><rect x="40" y="20" width="120" height="220" rx="22" '
         f'fill="none" stroke="#fff" stroke-width="12"/><circle cx="100" cy="210" r="10" fill="#fff"/>'
         f'<line x1="10" y1="250" x2="190" y2="10" stroke="{RED}" stroke-width="16" stroke-linecap="round"/></svg>')


def bars(rise_at=0.6):
    """Score bars: two before-ban bars, then the after bar rises."""
    out = '<div style="display:flex;align-items:flex-end;gap:30px;height:260px">'
    for h, lab in ((120, "spring"), (130, "summer")):
        out += (f'<div style="text-align:center"><div style="width:120px;height:{h}px;background:#555;'
                f'border-radius:12px 12px 0 0"></div><div style="font:700 34px Inter;color:#999;margin-top:8px">{lab}'
                f'</div></div>')
    out += (f'<div style="text-align:center"><div style="position:relative;width:120px;height:220px">'
            f'<div class=a style="position:absolute;bottom:0;width:120px;height:220px;background:{MINT};'
            f'border-radius:12px 12px 0 0;transform-origin:bottom;animation:rise 1s {rise_at:.2f}s both"></div></div>'
            f'<div style="font:700 34px Inter;color:{MINT};margin-top:8px">winter</div></div></div>'
            '<style>@keyframes rise{from{transform:scaleY(.55)}to{transform:scaleY(1)}}</style>')
    return out


def box(text, color, anim=""):
    return (f'<div class=a style="padding:24px 34px;border:7px solid {color};border-radius:26px;'
            f'font:800 58px Montserrat;color:{color};{anim}">{text}</div>')


def arrow(color, anim=""):
    return (f'<div class=a style="font:800 90px Montserrat;color:{color};margin:6px 0 6px 60px;{anim}">↓</div>')


STIM = ('<div class=big style="font-size:92px;margin-bottom:30px">Weaken it.</div>'
        f'<div style="display:flex;align-items:flex-end;gap:50px">{PHONE}{bars(1.0)}</div>'
        '<div class=mid style="font-size:56px;line-height:1.22;margin-top:40px">A school bans phones in class. '
        'Scores rise.</div>'
        '<div class="mid a" style="font-size:56px;line-height:1.22;margin-top:20px;animation:in .4s 3.4s both">'
        'Principal: <span class=mint>the ban raised scores.</span></div>')

ONE_CAUSE = (box("Phone ban", "#fff") + arrow("#fff") + box("Scores up", MINT)
             + '<div class=a style="display:flex;gap:30px;align-items:center;margin-top:60px;animation:in .4s 2.4s both">'
             + box("?", "#ffd166", "animation:shake .5s 2.8s both") + '<span class=mid style="font-size:60px">'
             'another cause?</span></div>')

TWO_CAUSES = ('<div style="display:flex;gap:30px">'
              + box("Phone ban", "#fff", "animation:fadeb .6s 1.6s both")
              + box("Tutoring", "#ffd166", "animation:in .45s .3s both") + '</div>'
              '<div style="display:flex;gap:220px">' + arrow("#fff", "animation:fadeb .6s 1.6s both")
              + arrow("#ffd166", "animation:in .4s .8s both") + '</div>'
              + box("Scores up", MINT)
              + '<p class=a style="margin-top:50px;animation:in .4s 2.4s both">Now the rise has '
              '<span class=mint>another explanation</span>.</p>'
              '<style>@keyframes fadeb{from{opacity:1}to{opacity:.3}}</style>')

TRAP = ('<div class="big a" style="font-size:104px;animation:in .4s both">Trap: <span class=mint>E</span></div>'
        '<div style="display:flex;gap:30px;margin-top:50px">'
        + box("Class: no phones", MINT, "animation:in .4s .4s both")
        + box("Lunch", "#999", "animation:in .4s 1.2s both") + '</div>'
        '<p class=a style="margin-top:50px;animation:in .4s 2.2s both">Lunch is outside the rule. '
        'It gives no other cause.</p>')

beats = [
    Beat("A school bans phones in class this fall. By winter, test scores rise. The principal says the ban raised "
         "the scores. Which choice weakens that?", STIM, sfx=[("pop", 1.0), ("pop", 3.4)]),
    Beat("Pick one.", '<div class="mid a" style="animation:in .4s both">Pick one</div>' + choice_list(CHOICES),
         sfx=[("pop", t) for t in (0, .18, .36, .54, .72)], min_len=3.0),
    Beat("Three seconds.", COUNTDOWN, sfx=[("tick", 0.0), ("tick", 1.0), ("tick", 2.0)], min_len=3.2),
    Beat("The argument gives one cause for the rise: the ban. To weaken it, find another cause.",
         ONE_CAUSE, sfx=[("pop", 2.4), ("thump", 2.8)], min_len=3.6),
    Beat("Daily tutoring started at the same time. That could explain the rise just as well.",
         TWO_CAUSES, sfx=[("pop", 0.3), ("thump", 1.6)], min_len=3.4),
    Beat("So the ban may not be the reason. So pick B.",
         '<div class="big a" style="font-size:104px;animation:in .4s both">Answer: <span class=mint>B</span></div>'
         + choice_list(CHOICES, highlight="B", animate=False), sfx=[("ding", 1.6)]),
    Beat("The trap is answer E. The ban covers class time. Phones at lunch give no other cause.", TRAP,
         sfx=[("pop", 0.4), ("thump", 1.2)]),
    Beat("Save this for your next critical reasoning question.", save_beat_scene("B"), sfx=[("pop", 0.1)],
         pad_after=0.6),
]

COVER = cover("forest", "60-Second Challenge", "No phones.<br>Higher scores?", 118)

if __name__ == "__main__":
    res = build(ID, beats, COVER, voiced=True, seed=101)
    print(json.dumps({k: v for k, v in res["measures"].items() if k != "takes"}, default=float))
