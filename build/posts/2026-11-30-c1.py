"""Carousel 2026-11-30-c1, Problem of the Day: exponents with a hidden base (9 = 3^2). Original question for
805 Score Lab.

If 3^x · 9^y = 3^12 and x − y = 3, what is the value of x?
(A) 3 (B) 4.5 (C) 6 (D) 7.5 (E) 9. Answer C, verified in build/items/2026-11-30-c1.py.
Hand solution: 9^y = 3^(2y), so x + 2y = 12; with x − y = 3, 3y = 9, y = 3, x = 6.
Wrong choices: D (7.5) treats 9^y as 3^y (trap); B (4.5) is y in that trap system; A (3) is y; E (9) is x + y.
Difficulty: our estimate, medium.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import Deck, check, check_html
import parts

ID = "2026-11-30-c1"
assert 3 ** 6 * 9 ** 3 == 3 ** 12 and 6 - 3 == 3
d = Deck("Problem of the Day", ground="forest")
d.add(parts.cover("Two bases.<br>One hides.", "Quant · our estimate: medium"), ground="forest")
d.add(parts.stake("Same base first, then compare.", "Exponent equations only line up when both sides use the "
                  "same base. Rewrite before you solve."))
d.add(parts.question(["If <b>3<sup>x</sup> · 9<sup>y</sup> = 3<sup>12</sup></b> and <b>x − y = 3</b>,",
                      "what is the value of x?"],
                     {"A": "3", "B": "4.5", "C": "6", "D": "7.5", "E": "9"}))
d.add(parts.solve("Rewrite 9 as a power of 3.", ["9 = 3<sup>2</sup>", "9<sup>y</sup> = 3<sup>2y</sup>",
                                                  "3<sup>x</sup> · 3<sup>2y</sup> = 3<sup>x + 2y</sup>"],
                  "Now every term has base 3."))
d.add(parts.solve("Match the exponents.", ["3<sup>x + 2y</sup> = 3<sup>12</sup>", "x + 2y = 12", "x − y = 3"]))
d.add(parts.solve("Subtract the equations.", ["(x + 2y) − (x − y) = 12 − 3", "3y = 9 → y = 3",
                                              "x = 3 + 3 = <span class=acc>6</span>"],
                  "Check: 3<sup>6</sup> · 9<sup>3</sup> = 729 · 729 = 3<sup>12</sup>."))
d.add(parts.answer("The answer is C.", "C", "With 9 written as 3², the exponents give x + 2y = 12 and "
                   "x − y = 3, so x = 6."))
d.add(parts.trap("D", "7.5 forgets that 9 = 3².", "Reading 9<sup>y</sup> as 3<sup>y</sup> gives x + y = 12, "
                 "so x = 7.5. The base 9 doubles the exponent."))
d.add(parts.recap("Exponents: one base, then equate", "Rewrite 4, 8, 9, 25, 27 as powers of 2, 3 or 5 first.",
                  "9<sup>y</sup> = 3<sup><span class=acc>2y</span></sup>"))
d.add(parts.cta("Save it.", "Rewrite to one base on your next exponent question. New question every day."))

if __name__ == "__main__":
    for i in range(len(d.slides)):
        assert not check_html(d.html(i)), i
    paths = d.render(pathlib.Path(__file__).resolve().parents[1] / "out" / ID, stem=ID)
    print("check:", check(paths, len(d.slides)) or "PASS")
