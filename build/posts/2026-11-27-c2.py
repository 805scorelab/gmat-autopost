"""Carousel 2026-11-27-c2, Critical Reasoning Breakdown: bakery boxes (evaluate the argument). Original argument for
805 Score Lab.

Argument: In March, Pelling Bakery switched from plastic boxes to paper boxes. Its sales from April through June were
higher than in the same months last year. The owner concludes that the paper boxes drew in more customers.
Question: which would be most useful to know in evaluating the argument?
Answer B (whether other bakeries in town also had higher sales from April through June than a year earlier). If yes,
a town-wide cause (more visitors, a new office nearby) could explain the rise and the argument weakens; if no, the
switch is a better explanation and the argument strengthens. Either answer changes the argument.
(A) Whether paper boxes cost more: cost does not tell us whether the boxes drew customers.
(C) Whether the owner prefers paper boxes: the owner's taste says nothing about customers.
(D) Whether the bakery plans to switch its bags to paper too: a future plan cannot explain past sales.
(E) Whether April to June sales beat January to March sales: the trap. The argument already compares the same months
    a year apart, which removes the season; a spring vs winter comparison mixes the season back in.
Only B has an answer either way that moves the argument, so no second choice is defensible.
Difficulty: our estimate, medium.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import Deck, check, check_html
import parts

ID = "2026-11-27-c2"
CH = {"A": "Whether the paper boxes cost more than the plastic ones",
      "B": "Whether other bakeries in town also had higher sales from April to June than a year earlier",
      "C": "Whether the owner personally prefers paper boxes",
      "D": "Whether the bakery plans to switch its bags to paper too",
      "E": "Whether the bakery's April to June sales were higher than its January to March sales"}
d = Deck("Critical Reasoning Breakdown", ground="mint")
d.add(parts.cover("New boxes.<br>More sales?", "Verbal · our estimate: medium"), ground="mint")
d.add(parts.stake("Evaluate = ask a question that cuts both ways.", "The right question has a yes that hurts "
                  "the argument and a no that helps it. If neither answer matters, skip it."))
d.add('<div style="margin-top:50px"><p style="font-size:37px;line-height:1.4">In March, Pelling Bakery switched from '
      'plastic boxes to paper boxes. Its sales from April to June were higher than in the same months last year. '
      'The owner concludes that the paper boxes drew in more customers.</p>'
      '<p style="margin-top:22px;font-size:37px"><b>Which would be most useful to know in evaluating the argument?'
      '</b></p><p style="margin-top:16px;font-size:31px;line-height:1.42">'
      + "<br>".join(f"({k}) {v}" for k, v in CH.items()) + "</p></div>")
d.add(parts.solve("Find the gap.", ["Boxes changed", "Sales rose", "The boxes, or something town-wide?"],
                  "A busier town would lift every bakery."))
d.add(parts.solve("Run yes and no.", ["B yes: all rose → <span class=acc>weaker</span>",
                                      "B no: only Pelling → <span class=acc>stronger</span>",
                                      "A, C, D: no swing either way"],
                  "Only B can move the argument both ways."))
d.add(parts.answer("The answer is B.", "B", "Other bakeries' sales tell us whether the rise came from the boxes "
                   "or from something that lifted the whole town."))
d.add(parts.trap("E", "The season is already handled.", "The argument compares April to June with the same months "
                 "last year. Spring vs winter brings the season back in and tests nothing about the boxes."))
d.add(parts.recap("Evaluate: test the yes and the no", "Pick the question whose answer can swing the argument.",
                  "Yes → weaker · No → stronger<br>→ <span class=acc>useful to know</span>"))
d.add(parts.cta("Save it.", "Run yes and no on your next evaluate question. New question every day."))

if __name__ == "__main__":
    for i in range(len(d.slides)):
        assert not check_html(d.html(i)), i
    paths = d.render(pathlib.Path(__file__).resolve().parents[1] / "out" / ID, stem=ID)
    print("check:", check(paths, len(d.slides)) or "PASS")
