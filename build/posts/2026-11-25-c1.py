"""Carousel 2026-11-25-c1, Problem of the Day: mixture dilution (add water). Original question for 805 Score Lab.

A tank holds 40 liters of a solution that is 25% acid. How many liters of pure water must be added so that the
solution is 20% acid?
(A) 2 (B) 8 (C) 10 (D) 12 (E) 50. Answer C, verified in build/items/2026-11-25-c1.py.
Hand solution: the acid never changes. 25% of 40 = 10 liters of acid. 10 / (40 + w) = 20%, so 40 + w = 50, w = 10.
Wrong choices: E (50) is the new total, not the water added (trap); A (2) takes 5% of 40; B (8) takes 20% of 40;
D (12) adds the 2 from choice A to the acid.
Difficulty: our estimate, medium.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import Deck, check, check_html
import parts

ID = "2026-11-25-c1"
d = Deck("Problem of the Day", ground="paper")
d.add(parts.cover("25% acid.<br>Make it 20%.", "Quant · our estimate: medium"), ground="paper")
d.add(parts.stake("Find what never changes.", "Adding water changes the total and the percent. "
                  "The amount of acid stays fixed. Build the equation around it."))
d.add(parts.question(["A tank holds <b>40 liters</b> of a solution that is <b>25% acid</b>.",
                      "How many liters of pure water must be added so that the solution is <b>20% acid</b>?"],
                     {"A": 2, "B": 8, "C": 10, "D": 12, "E": 50}))
d.add(parts.solve("Lock the acid.", ["25% of 40 = <span class=acc>10 liters</span> of acid",
                                     "Water adds liquid, never acid"],
                  "Those 10 liters stay in the tank."))
d.add(parts.solve("Set the new percent.", ["10 ÷ (40 + w) = 20%", "10 is 20% of the new total",
                                           "New total = 10 ÷ 0.2 = 50"],
                  "The tank must hold 50 liters at the end."))
d.add(parts.solve("Subtract what was there.", ["50 − 40 = <span class=acc>10 liters</span> of water",
                                                "Check: 10 ÷ 50 = 20% ✓"]))
d.add(parts.answer("The answer is C.", "C", "Add 10 liters of water. The acid stays at 10 liters, "
                   "and 10 out of 50 is 20%."))
d.add(parts.trap("E", "50 is the total, not the water.", "Solving for the new total is the right middle step. "
                 "Stopping there answers a different question. Subtract the 40 you started with."))
d.add(parts.recap("Dilution: fix the solute", "The part that doesn't change sets the equation.",
                  "acid ÷ new total = new %<br>10 ÷ 50 = 20% → add <span class=acc>10</span>"))
d.add(parts.cta("Save it.", "Lock the unchanged amount on your next mixture question. New question every day."))

if __name__ == "__main__":
    for i in range(len(d.slides)):
        assert not check_html(d.html(i)), i
    paths = d.render(pathlib.Path(__file__).resolve().parents[1] / "out" / ID, stem=ID)
    print("check:", check(paths, len(d.slides)) or "PASS")
