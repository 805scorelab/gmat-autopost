"""Carousel 2026-11-28-c1, Problem of the Day: age word problem. Original question for 805 Score Lab.

In 5 years, Ana will be twice as old as she was 7 years ago. How old is Ana now?
(A) 12 (B) 14 (C) 17 (D) 19 (E) 24. Answer D, verified in build/items/2026-11-28-c1.py.
Hand solution: a + 5 = 2(a - 7) = 2a - 14, so a = 19. Check: 24 = 2 x 12.
Wrong choices: A (12) solves a + 5 = 2a - 7, doubling only a (trap; it is also her age 7 years ago); B (14) is 2 x 7;
C (17) is 12 + 5; E (24) is her age in 5 years.
Difficulty: our estimate, easy to medium.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import Deck, check, check_html
import parts

ID = "2026-11-28-c1"
d = Deck("Problem of the Day", ground="paper")
d.add(parts.cover("Twice as old.<br>How old now?", "Quant · our estimate: easy to medium"), ground="paper")
d.add(parts.stake("Age problems hide one bracket.", "“Twice what she was” doubles her whole past age. "
                  "Drop the bracket and you land on a choice that is waiting for you."))
d.add(parts.question(["In <b>5 years</b>, Ana will be <b>twice</b> as old as she was <b>7 years ago</b>.",
                      "How old is Ana <b>now</b>?"],
                     {"A": 12, "B": 14, "C": 17, "D": 19, "E": 24}))
d.add(parts.solve("Name today's age.", ["Ana now: <span class=acc>a</span>", "In 5 years: a + 5",
                                        "7 years ago: a − 7"]))
d.add(parts.solve("Double the whole past age.", ["a + 5 = 2(a − 7)", "a + 5 = 2a − 14"],
                  "The 2 multiplies the 7 too."))
d.add(parts.solve("Solve for a.", ["5 + 14 = 2a − a", "a = <span class=acc>19</span>"]))
d.add(parts.solve("Check both ages.", ["In 5 years: 24", "7 years ago: 12", "24 = 2 × 12 ✓"]))
d.add(parts.answer("The answer is D.", "D", "Ana is 19 now: 24 in 5 years, which is twice her age of 12, "
                   "7 years ago."))
d.add(parts.trap("A", "12 doubles only a.", "a + 5 = 2a − 7 forgets to double the 7 and gives 12. "
                 "That is her age 7 years ago, not today."))
d.add(parts.recap("Ages: write each time as today ± years", "Then put brackets around every age you multiply.",
                  "a + 5 = 2(a − 7) → a = <span class=acc>19</span>"))
d.add(parts.cta("Save it.", "Bracket every age on your next word problem. New question every day."))

if __name__ == "__main__":
    for i in range(len(d.slides)):
        assert not check_html(d.html(i)), i
    paths = d.render(pathlib.Path(__file__).resolve().parents[1] / "out" / ID, stem=ID)
    print("check:", check(paths, len(d.slides)) or "PASS")
