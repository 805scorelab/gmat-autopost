"""Carousel 2026-11-23-c1, Problem of the Day: ratio after 6 boys join. Original question for 805 Score Lab.

In a class, boys to girls is 3 : 5. After 6 more boys join, boys to girls is 3 : 4. How many girls are in the class?
(A) 24 (B) 30 (C) 32 (D) 40 (E) 48. Answer D, verified in build/items/2026-11-23-c1.py.
Hand solution: boys 3k, girls 5k; (3k + 6) : 5k = 3 : 4 gives 12k + 24 = 15k, k = 8, girls 40.
Wrong choices: A (24) is the boys at the start (trap: answering the wrong quantity); B (30) the boys after;
C (32) is 4 x 8, reading the new ratio's 4 as girls x k; E (48) is 6 x 8.
Difficulty: our estimate, medium.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import Deck, check, check_html
import parts

ID = "2026-11-23-c1"
d = Deck("Problem of the Day", ground="paper")
d.add(parts.cover("6 boys join.<br>Count the girls.", "Quant · our estimate: medium"), ground="mint")
d.add(parts.stake("Ratios hide the real numbers.", "A ratio gives you parts, not people. One unknown, the size "
                  "of a part, turns both ratios into one equation."))
d.add(parts.question(["In a class, the ratio of boys to girls is <b>3 : 5</b>. After 6 more boys join, the ratio "
                      "is <b>3 : 4</b>.", "How many girls are in the class?"],
                     {"A": 24, "B": 30, "C": 32, "D": 40, "E": 48}))
d.add(parts.solve("Name one part k.", ["Boys = 3k", "Girls = 5k", "The girls never change."],
                  "So 5k is the number we want."))
d.add(parts.solve("Use the new ratio.", ["(3k + 6) : 5k = 3 : 4", "4(3k + 6) = 3(5k)", "12k + 24 = 15k",
                                         "k = <span class=acc>8</span>"]))
d.add(parts.solve("Check it.", ["Girls = 5 × 8 = 40", "Boys: 24, then 30", "30 : 40 = 3 : 4 ✓"],
                  "Both ratios hold."))
d.add(parts.answer("The answer is D.", "D", "40 girls. The 6 new boys are what moved the ratio from 3 : 5 to 3 : 4."))
d.add(parts.trap("A", "24 answers the wrong question.", "24 is the number of boys at the start. "
                 "Once you find k, reread what's asked: girls, so 5k."))
d.add(parts.recap("Ratio + change", "Write each group as parts × k. Keep the group that doesn't change.",
                  "3k : 5k → (3k + 6) : 5k = 3 : 4<br>k = 8, girls = <span class=acc>40</span>"))
d.add(parts.cta("Save it.", "Use the parts × k move on your next ratio question. New question every day."))

if __name__ == "__main__":
    for i in range(len(d.slides)):
        assert not check_html(d.html(i)), i
    paths = d.render(pathlib.Path(__file__).resolve().parents[1] / "out" / ID, stem=ID)
    print("check:", check(paths, len(d.slides)) or "PASS")
