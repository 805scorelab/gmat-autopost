"""Carousel 2026-11-22-c2, Critical Reasoning Breakdown: bike lanes. Original argument written for 805 Score Lab.

Argument: last year Darnell added bike lanes on Main Street; since then the number of cyclists counted on Main Street
has doubled. Conclusion: adding bike lanes to other streets will double cycling on those streets too.
Assumption: the doubling on Main Street came from new cycling caused by the lanes, not from riders moving over.
Answer B: most new Main Street cyclists switched from nearby streets without lanes. The doubling was redistribution,
so lanes everywhere would not double cycling on every street. Weakens.
(A) Cyclists feel safer in lanes: if anything supports the plan. (C) Cost: irrelevant to cycling numbers.
(D) Plans for five more streets: restates the plan, says nothing about the effect. (E) Fewer accidents: a benefit,
not evidence about how many people ride. Only B attacks the link from lanes to more cycling.
Trap: A, because it is about the lanes and sounds important, but it pushes the argument the wrong way.
Difficulty: our estimate, medium.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import Deck, check, check_html
import parts

ID = "2026-11-22-c2"
CH = {"A": "Many cyclists say they feel safer riding in bike lanes.",
      "B": "Most new cyclists on Main Street switched from nearby streets without bike lanes.",
      "C": "The Main Street lanes cost less than expected to build.",
      "D": "The council plans bike lanes on five more streets next year.",
      "E": "Accidents involving cyclists on Main Street fell after the lanes opened."}
d = Deck("Critical Reasoning Breakdown", ground="paper")
d.add(parts.cover("Double the bikes?<br>Not so fast.", "Verbal · our estimate: medium"), ground="forest")
d.add(parts.stake("Weaken questions reward one move.", "Find the gap between the evidence and the conclusion, "
                  "then pick the choice that widens it."))
d.add('<div style="margin-top:60px"><p style="font-size:38px;line-height:1.4">Last year, the city of Darnell added '
      'bike lanes on Main Street. Since then, the number of cyclists counted on Main Street has doubled. So adding '
      'bike lanes to other streets will double cycling on those streets too.</p>'
      '<p style="margin-top:26px;font-size:38px"><b>Which choice most weakens the conclusion?</b></p>'
      '<p style="margin-top:20px;font-size:32px;line-height:1.45">'
      + "<br>".join(f"({k}) {v}" for k, v in CH.items()) + "</p></div>")
d.add(parts.solve("Map the argument.", ["Evidence: Main St riders doubled", "Conclusion: lanes elsewhere",
                                         "will double riding there too"], "The gap: were those riders new?"))
d.add(parts.solve("Spot the assumption.", ["The lanes created new riders,", "not just moved them."],
                  "If riders only moved over, lanes everywhere can't double every street."))
d.add(parts.answer("The answer is B.", "B", "Riders switched from nearby streets. The doubling was a shift, "
                   "not growth, so the plan can't repeat it everywhere."))
d.add(parts.trap("A", "A pushes the wrong way.", "Feeling safer is a reason more people might ride. That "
                 "supports the plan. C, D and E don't touch rider numbers at all."))
d.add(parts.recap("Weaken: attack the gap", "Ask what else could explain the evidence.",
                  "More riders on one street<br>→ new riders, or moved riders?"))
d.add(parts.cta("Save it.", "Run the gap check on your next weaken question. New question every day."))

if __name__ == "__main__":
    for i in range(len(d.slides)):
        assert not check_html(d.html(i)), i
    paths = d.render(pathlib.Path(__file__).resolve().parents[1] / "out" / ID, stem=ID)
    print("check:", check(paths, len(d.slides)) or "PASS")
