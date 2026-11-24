"""Carousel 2026-11-26-c2, Critical Reasoning Breakdown: brighter streetlights (strengthen). Original argument for
805 Score Lab.

Argument: Last year the town of Marlow replaced the streetlights in its Ward 4 with brighter LED lights. Over the
following year, nighttime car accidents in Ward 4 fell by a third. The council concludes that the brighter lights
caused the drop.
Question: which choice most strengthens the conclusion?
Answer D (in nearby wards that kept the old lights, nighttime accidents did not fall over the same year). It rules out
a town-wide cause such as weather, fuel prices or policing: the drop showed up only where the lights changed.
(A) LED lights cost less to run: about money, not accidents. Irrelevant.
(B) Daytime accidents in Ward 4 fell by a similar share: suggests a cause that works day and night, so it weakens.
(C) Many Ward 4 residents say the streets feel safer at night: a feeling, not accidents. Trap: it sounds like support
    for the lights but says nothing about crashes.
(E) Ward 4 lowered its speed limit that year: another cause. Weakens.
Only D removes an alternative explanation, so no second choice is defensible.
Difficulty: our estimate, easy to medium.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import Deck, check, check_html
import parts

ID = "2026-11-26-c2"
CH = {"A": "The new LED lights cost less to run than the old ones.",
      "B": "Daytime car accidents in Ward 4 fell by a similar share that year.",
      "C": "Many Ward 4 residents say the streets feel safer at night.",
      "D": "In nearby wards that kept the old lights, nighttime accidents did not fall that year.",
      "E": "Ward 4 also lowered its speed limit that year."}
d = Deck("Critical Reasoning Breakdown", ground="paper")
d.add(parts.cover("Brighter lights.<br>Fewer crashes?", "Verbal · our estimate: easy to medium"), ground="paper")
d.add(parts.stake("Strengthen = rule out other causes.", "A before-and-after change is only a clue. "
                  "The best support shows the drop happened where the lights changed and nowhere else."))
d.add('<div style="margin-top:50px"><p style="font-size:37px;line-height:1.4">Last year, the town of Marlow put '
      'brighter LED streetlights in its Ward 4. Over the following year, nighttime car accidents in Ward 4 fell by '
      'a third. The council concludes that the brighter lights caused the drop.</p>'
      '<p style="margin-top:22px;font-size:37px"><b>Which of the following most strengthens the conclusion?</b></p>'
      '<p style="margin-top:16px;font-size:31px;line-height:1.42">'
      + "<br>".join(f"({k}) {v}" for k, v in CH.items()) + "</p></div>")
d.add(parts.solve("Find the gap.", ["Lights changed", "Accidents fell", "Was it the lights, or something else?"],
                  "Anything town-wide could explain the drop."))
d.add(parts.solve("Test each choice.", ["A, C: not about crashes", "B, E: point to another cause",
                                        "D: <span class=acc>no drop without new lights</span>"],
                  "Only D compares with wards that kept the old lights."))
d.add(parts.answer("The answer is D.", "D", "Wards with the old lights saw no drop. That makes a town-wide "
                   "cause less likely and points back at the lights."))
d.add(parts.trap("C", "Feeling safer is not crashing less.", "C sounds like praise for the lights. "
                 "The conclusion is about accidents, and a feeling says nothing about them."))
d.add(parts.recap("Strengthen a cause: add a comparison", "Show the effect is missing where the cause is missing.",
                  "New lights → fewer crashes<br>Old lights → <span class=acc>no change</span>"))
d.add(parts.cta("Save it.", "Look for the comparison group on your next strengthen question. New question every day."))

if __name__ == "__main__":
    for i in range(len(d.slides)):
        assert not check_html(d.html(i)), i
    paths = d.render(pathlib.Path(__file__).resolve().parents[1] / "out" / ID, stem=ID)
    print("check:", check(paths, len(d.slides)) or "PASS")
