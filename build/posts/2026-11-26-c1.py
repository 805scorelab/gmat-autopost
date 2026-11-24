"""Carousel 2026-11-26-c1, Problem of the Day: consecutive integers. Original question for 805 Score Lab.

The sum of 5 consecutive integers is 85. What is the largest of the 5 integers?
(A) 15 (B) 17 (C) 19 (D) 20 (E) 21. Answer C, verified in build/items/2026-11-26-c1.py.
Hand solution: for an odd count of consecutive integers the middle one is the average: 85 / 5 = 17. The list is
15, 16, 17, 18, 19, so the largest is 19.
Wrong choices: B (17) is the middle (trap: stopping at the average); A (15) is the smallest; D (20) and E (21) add 3
and 4 to the middle instead of 2.
Difficulty: our estimate, easy.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import Deck, check, check_html
import parts

ID = "2026-11-26-c1"
d = Deck("Problem of the Day", ground="mint")
d.add(parts.cover("5 in a row.<br>Sum is 85.", "Quant · our estimate: easy"), ground="mint")
d.add(parts.stake("The average sits in the middle.", "Consecutive integers are evenly spaced. "
                  "With an odd count, the middle number is the average. Start there."))
d.add(parts.question(["The sum of <b>5 consecutive integers</b> is <b>85</b>.",
                      "What is the <b>largest</b> of the 5 integers?"],
                     {"A": 15, "B": 17, "C": 19, "D": 20, "E": 21}))
d.add(parts.solve("Find the average.", ["85 ÷ 5 = <span class=acc>17</span>",
                                        "Evenly spaced: average = middle"],
                  "17 is the 3rd of the 5 numbers."))
d.add(parts.solve("Build out from the middle.", ["15, 16, <span class=acc>17</span>, 18, 19",
                                                 "2 below, 2 above"],
                  "No algebra needed."))
d.add(parts.solve("Check the sum.", ["15 + 16 + 17 + 18 + 19 = 85 ✓", "Largest = <span class=acc>19</span>"]))
d.add(parts.answer("The answer is C.", "C", "The middle is 17, and the largest sits 2 steps above it: 19."))
d.add(parts.trap("B", "17 is the middle, not the top.", "Finding the average is the right first step. "
                 "The question asks for the largest, so count 2 more steps up."))
d.add(parts.recap("Consecutive sums: start in the middle", "Average = middle term when the count is odd.",
                  "85 ÷ 5 = 17 → 15 … <span class=acc>19</span>"))
d.add(parts.cta("Save it.", "Start from the middle on your next consecutive-integer question. New question every day."))

if __name__ == "__main__":
    for i in range(len(d.slides)):
        assert not check_html(d.html(i)), i
    paths = d.render(pathlib.Path(__file__).resolve().parents[1] / "out" / ID, stem=ID)
    print("check:", check(paths, len(d.slides)) or "PASS")
