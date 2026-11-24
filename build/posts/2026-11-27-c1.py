"""Carousel 2026-11-27-c1, Problem of the Day: overlapping sets (two groups). Original question for 805 Score Lab.

Of 50 students in a class, 28 take French, 20 take Spanish, and 9 take both. How many take neither?
(A) 2 (B) 9 (C) 11 (D) 19 (E) 39. Answer C, verified in build/items/2026-11-27-c1.py.
Hand solution: at least one language = 28 + 20 - 9 = 39 (the 9 were counted twice). Neither = 50 - 39 = 11.
Wrong choices: A (2) is 50 - 48, forgetting to remove the double count (trap); B (9) is the both group; D (19) is
French only; E (39) is the number taking at least one.
Difficulty: our estimate, easy to medium.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import Deck, check, check_html
import parts

ID = "2026-11-27-c1"
d = Deck("Problem of the Day", ground="forest")
d.add(parts.cover("28 French.<br>20 Spanish.<br>Neither?", "Quant · our estimate: easy to medium"), ground="forest")
d.add(parts.stake("Some students sit in both groups.", "Add the two groups and the overlap gets counted twice. "
                  "Remove it once, then compare with the class."))
d.add(parts.question(["Of <b>50 students</b> in a class, <b>28</b> take French, <b>20</b> take Spanish, "
                      "and <b>9</b> take both.",
                      "How many students take <b>neither</b> language?"],
                     {"A": 2, "B": 9, "C": 11, "D": 19, "E": 39}))
d.add(parts.solve("Add the groups.", ["28 + 20 = 48", "The 9 in both are in each count"],
                  "48 counts those 9 students twice."))
d.add(parts.solve("Remove the double count.", ["48 − 9 = <span class=acc>39</span>",
                                               "39 take at least 1 language"]))
d.add(parts.solve("Subtract from the class.", ["50 − 39 = <span class=acc>11</span> take neither",
                                               "Check: 19 + 9 + 11 + 11 = 50 ✓"],
                  "French only 19, both 9, Spanish only 11, neither 11."))
d.add(parts.answer("The answer is C.", "C", "39 students take at least 1 language, so 11 of the 50 take neither."))
d.add(parts.trap("A", "2 counts the overlap twice.", "50 − 48 = 2 treats the 9 students in both groups as 18 "
                 "people. Subtract the overlap once before you compare with 50."))
d.add(parts.recap("Two groups: total = A + B − both + neither", "Every student lands in exactly 1 region.",
                  "50 = 28 + 20 − 9 + <span class=acc>11</span>"))
d.add(parts.cta("Save it.", "Use the 2-group formula on your next overlapping-sets question. New question every day."))

if __name__ == "__main__":
    for i in range(len(d.slides)):
        assert not check_html(d.html(i)), i
    paths = d.render(pathlib.Path(__file__).resolve().parents[1] / "out" / ID, stem=ID)
    print("check:", check(paths, len(d.slides)) or "PASS")
