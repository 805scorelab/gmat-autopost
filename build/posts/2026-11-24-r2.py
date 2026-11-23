"""Reel 2026-11-24-r2, series Trap Answer: Critical Reasoning inference, reversed rule. Verbal. Voiced, score v1.

Original question for 805 Score Lab:
  At one firm, every intern who finishes the training is offered a job. Sam, an intern there, got no offer.
  Which must be true?
  (A) Sam did not finish the training.  (B) Sam's work was rated poorly.  (C) Every intern with an offer finished
  the training.  (D) Most interns finish the training.  (E) Sam did not want an offer.
Answer A. Rule: finish -> offer. Its contrapositive is no offer -> not finished; Sam has no offer, so Sam did not finish.
Why each wrong choice fails:
  B: no ratings are mentioned; the stimulus gives no reason beyond the training rule.
  C: the trap; it reverses the rule (offer -> finished). The rule allows an intern to get an offer without finishing.
  D: nothing says how many interns finish; it could be none or all but Sam.
  E: Sam's wishes are never mentioned; an offer is made by the firm, not chosen by Sam.
Only A is forced, so no second choice is defensible. Logic also checked below by enumerating every world.
Difficulty: our estimate, easy to medium. Quality-log improvement applied: big drawn arrow diagrams that fill the frame
width, with motion on every beat.
Usage: python3 posts/2026-11-24-r2.py
"""
import itertools
import json
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import base_css, bubbles
from reel import Beat, build

ID = "2026-11-24-r2"


def _must_be_true():
    """Worlds: Sam finished?, Sam offered?, plus one other intern (finished?, offered?). Keep worlds where the rule
    holds for everyone and Sam has no offer; a choice must be true in every kept world (B, D, E are about facts the
    worlds leave free, so they are not forced: checked by construction)."""
    worlds = [w for w in itertools.product([0, 1], repeat=4)
              if all((not f) or o for f, o in ((w[0], w[1]), (w[2], w[3]))) and not w[1]]
    a = all(not w[0] for w in worlds)
    c = all((not o) or f for w in worlds for f, o in ((w[0], w[1]), (w[2], w[3])))
    return a, c


assert _must_be_true() == (True, False), "A must be forced and C must not be"

CHOICES = [("A", "Sam did not finish the training."), ("B", "Sam's work was rated poorly."),
           ("C", "Every intern with an offer finished the training."), ("D", "Most interns finish the training."),
           ("E", "Sam did not want an offer.")]


def choice_list(highlight=None, cross=None, animate=True):
    rows = []
    for i, (l, v) in enumerate(CHOICES):
        on = " on" if l == highlight else ""
        anim = f"animation:pop .35s {i * .18:.2f}s both" if animate else ""
        dim = "opacity:.45;" if highlight and l != highlight else ""
        x = ('<span class=a style="position:absolute;left:-6px;right:-6px;top:50%;height:7px;background:#ff6b6b;'
             'transform-origin:left;animation:grow .4s .3s both"></span>') if l == cross else ""
        rows.append(f'<div style="display:flex;align-items:center;gap:30px;margin-top:26px;{dim}">'
                    f'<div class="bubble{on} a" style="flex:none;{anim}">{l}</div>'
                    f'<span style="position:relative;font:600 46px/1.2 Inter">{v}{x}</span></div>')
    return "".join(rows)


def arrow(left, right, delay=0.3, colour="#BFFBD1", ink="#06142B", cross_left=False, cross_right=False,
          cross_arrow=False):
    """Two big boxes joined by a drawn arrow, filling the frame width."""
    def box(text, d, crossed):
        x = (f'<svg class=a style="position:absolute;inset:0;animation:in .3s {d + .6:.2f}s both" viewBox="0 0 330 330">'
             '<line x1="40" y1="40" x2="290" y2="290" stroke="#ff6b6b" stroke-width="18"/>'
             '<line x1="290" y1="40" x2="40" y2="290" stroke="#ff6b6b" stroke-width="18"/></svg>') if crossed else ""
        return (f'<div class=a style="position:relative;width:330px;height:330px;border-radius:34px;background:{colour};'
                f'color:{ink};display:flex;align-items:center;justify-content:center;text-align:center;'
                f'font:800 54px/1.1 Montserrat;padding:20px;box-sizing:border-box;animation:pop .45s {d:.2f}s both">'
                f'{text}{x}</div>')
    cross = ('<line x1="40" y1="30" x2="150" y2="130" stroke="#ff6b6b" stroke-width="14"/>'
             '<line x1="150" y1="30" x2="40" y2="130" stroke="#ff6b6b" stroke-width="14"/>') if cross_arrow else ""
    line = (f'<svg width="190" height="160" viewBox="0 0 190 160"><style>@keyframes dr{{from{{stroke-dashoffset:150}}'
            f'to{{stroke-dashoffset:0}}}}</style>'
            f'<line class=a x1="10" y1="80" x2="160" y2="80" stroke="#fff" stroke-width="14" stroke-dasharray="150" '
            f'style="animation:dr .5s {delay + .45:.2f}s both"/>'
            f'<polygon class=a points="150,50 185,80 150,110" fill="#fff" style="animation:in .2s {delay + .9:.2f}s both"/>'
            f'<g class=a style="animation:in .3s {delay + 1.2:.2f}s both">{cross}</g></svg>')
    return (f'<div style="display:flex;align-items:center;justify-content:space-between;margin-top:70px">'
            f'{box(left, delay, cross_left)}{line}{box(right, delay + 1.0, cross_right)}</div>')


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

STIM = ('<div class=mid style="font-size:66px;line-height:1.22">Every intern who <span class=mint>finishes the '
        'training</span> is offered a <span class=mint>job</span>.</div>'
        '<div class="mid a" style="font-size:66px;line-height:1.22;margin-top:40px;animation:in .4s .2s both">'
        'Sam, an intern there, got <span class=mint>no offer</span>.</div>'
        '<div class="big a" style="font-size:96px;margin-top:60px;animation:in .4s .4s both">What must be true?</div>')

beats = [
    Beat("At one firm, any intern finishing the training is offered a job. Sam is an intern there. Sam got no offer. "
         "What must be true?", STIM, sfx=[("pop", 0.2), ("pop", 0.4)]),
    Beat("Pick one.", '<div class="mid a" style="animation:in .4s both">Pick one</div>' + choice_list(),
         sfx=[("pop", t) for t in (0, .18, .36, .54, .72)], min_len=3.0),
    Beat("Three seconds.", COUNTDOWN, sfx=[("tick", 0.0), ("tick", 1.0), ("tick", 2.0)], min_len=3.2),
    Beat("Draw the rule as an arrow. Finish the training, get an offer.",
         '<div class="mid a" style="animation:in .4s both">The rule</div>' + arrow("Finished training", "Job offer", .8),
         sfx=[("pop", 0.8), ("pop", 1.8)]),
    Beat("Sam has no offer. So Sam can't have finished, or the offer would be there.",
         '<div class="mid a" style="animation:in .4s both">Sam: <span class=mint>no offer</span></div>'
         + arrow("No job offer", "Not finished", .3, colour="#fff", ink="#000")
         + '<p class=a style="margin-top:50px;animation:in .4s 2.6s both">No offer, so the training was not finished.</p>',
         sfx=[("thump", 0.9), ("thump", 1.9)]),
    Beat("So Sam did not finish the training. Pick A.",
         '<div class="big a" style="font-size:104px;animation:in .4s both">Answer: <span class=mint>A</span></div>'
         + choice_list(highlight="A", animate=False), sfx=[("ding", 0.6)]),
    Beat("C is the trap. It flips the arrow. The rule never says an offer needs the training.",
         '<div class="big a" style="font-size:104px;animation:in .4s both">Trap: <span class=mint>C</span></div>'
         + arrow("Job offer", "Finished training", 1.4, colour="#fff", ink="#000", cross_arrow=True)
         + '<p class=a style="margin-top:50px;animation:in .4s 3.4s both">An offer can come without the training.</p>',
         sfx=[("pop", 1.4), ("thump", 2.6)]),
    Beat("Save this for your next critical reasoning question.",
         '<div class="big a" style="animation:in .5s both">Save it.</div>'
         '<div class="mid a" style="margin-top:40px;animation:in .5s .4s both">@805scorelab</div>'
         f'<div style="margin-top:80px">{bubbles("A")}</div>', sfx=[("pop", 0.1)], pad_after=0.6),
]

COVER = f"""<style>{base_css('forest', height=1920)}
 .c{{position:absolute;top:420px;left:90px;right:90px}}</style><div class=frame><div class=c>
 <span class=chip>Trap Answer</span><h1 style="margin-top:40px;font-size:118px">Don't flip<br>the arrow.</h1>
 <div style="margin-top:70px">{bubbles()}</div></div></div>"""

if __name__ == "__main__":
    res = build(ID, beats, COVER, voiced=True, seed=67)
    print(json.dumps({k: v for k, v in res["measures"].items() if k != "takes"}, default=float))
