"""Carousel 2026-11-21-c1, Problem of the Day: remainder of 2n.

Question (original, written for 805 Score Lab): when the positive integer n is divided by 6 the remainder is 4.
What is the remainder when 2n is divided by 6?  (A) 0 (B) 2 (C) 3 (D) 4 (E) 5

Hand solution: n = 6k + 4, so 2n = 12k + 8 = 6(2k + 1) + 2. Remainder 2, answer B.
Shortcut: multiply the remainder by 2 and reduce: 2 x 4 = 8, 8 - 6 = 2.
Wrong choices: A (0) would need 2n to be a multiple of 6; C (3) and E (5) are odd, but 2n is even and so is 6(2k+1),
so the remainder must be even; D (4) is the trap, assuming the remainder survives doubling.
Verified in code: build/items/2026-11-21-c1.py (brute force over n < 10000).
Difficulty: our estimate, easy.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import Deck, check, check_html
import parts

ID = "2026-11-21-c1"
d = Deck("Problem of the Day", ground="paper")
d.add(parts.cover("Double it.<br>What's left?", "Quant · our estimate: easy"), ground="forest")
d.add(parts.stake("Remainders are pure GMAT Quant.", "No calculator, 5 choices, about 2 minutes a question. "
                  "This one takes 30 seconds once you see the rule."))
d.add(parts.question(["When the positive integer <b>n</b> is divided by 6, the remainder is 4.",
                      "What is the remainder when <b>2n</b> is divided by 6?"],
                     {"A": 0, "B": 2, "C": 3, "D": 4, "E": 5}))
d.add(parts.solve("Try the smallest n.", ["n = 4 &nbsp;(4 ÷ 6 leaves 4)", "2n = 8", "8 = 6 + <span class=acc>2</span>"],
                  "So the remainder is 2. Does that hold for every n?"))
d.add(parts.solve("Now prove it for all n.", ["n = 6k + 4", "2n = 12k + 8", "2n = 6(2k + 1) + <span class=acc>2</span>"],
                  "Every n gives a remainder of 2."))
d.add(parts.answer("The answer is B.", "B", "Fast method: double the remainder, then take away 6 if you can. "
                   "2 × 4 = 8, and 8 − 6 = 2."))
d.add(parts.trap("D", "The remainder doesn't survive doubling.", "Picking 4 assumes n and 2n leave the same "
                 "remainder. Doubling n doubles the remainder too, and 8 is bigger than 6, so you trim it."))
d.add(parts.recap("Remainder of a multiple", "Multiply the remainder, then reduce by the divisor.",
                  "n ÷ 6 leaves 4<br>2n ÷ 6 leaves 2 × 4 = 8 → <span class=acc>2</span>"))
d.add(parts.cta("Save it.", "You'll want this rule the next time a remainder question costs you 3 minutes. "
                "New question every day."))

if __name__ == "__main__":
    for i in range(len(d.slides)):
        problems = check_html(d.html(i))
        assert not problems, (i, problems)
    out = pathlib.Path(__file__).resolve().parents[1] / "out" / ID
    paths = d.render(out, stem=ID)
    problems = check(paths, len(d.slides))
    print("\n".join(paths))
    print("check:", problems or "PASS")
