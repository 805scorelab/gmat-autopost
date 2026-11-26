"""Carousel 2026-11-29-c2, Critical Reasoning Breakdown: bookshop delivery plan (assumption). Original argument for
805 Score Lab.

Stimulus: Over the past year, many regular customers of Marlow Books, an online bookshop, began buying from other
shops instead. Marlow's books take five days to arrive. To win those customers back, Marlow plans to cut its delivery
time to two days.
Question: the plan depends on which assumption?
Answer B (at least some of the customers who left did so partly because of Marlow's delivery time). Negation test:
if none of them left because of delivery time, faster delivery gives them no reason to return, and the plan fails.
(A) Most online shoppers want books in one day: "most" and "one day" go beyond what the plan needs.
(C) Marlow's prices are lower than its rivals': the plan is about delivery; prices can be anything.
(D) Faster delivery will not raise Marlow's costs: the trap. The goal is winning customers back, not profit; the
    plan can win them back even if costs rise. Negated, the plan's goal still stands.
(E) Rival shops deliver in two days or less: not needed; the plan can work whatever rivals do.
Only B survives the negation test, so no second choice is defensible.
Difficulty: our estimate, medium.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import Deck, check, check_html
import parts

ID = "2026-11-29-c2"
CH = {"A": "Most people who buy books online want them to arrive within one day.",
      "B": "At least some of the customers who left did so partly because of Marlow's delivery time.",
      "C": "Marlow's prices are lower than those of the shops its customers switched to.",
      "D": "Cutting delivery time to two days will not raise Marlow's costs.",
      "E": "The shops Marlow's customers switched to deliver in two days or less."}
d = Deck("Critical Reasoning Breakdown", ground="paper")
d.add(parts.cover("Faster books.<br>Will they return?", "Verbal · our estimate: medium"), ground="paper")
d.add(parts.stake("An assumption is what the plan needs.", "Flip each choice into its opposite. "
                  "The one whose opposite breaks the plan is the assumption."))
d.add('<div style="margin-top:50px"><p style="font-size:35px;line-height:1.4">Over the past year, many regular '
      'customers of Marlow Books, an online bookshop, began buying from other shops instead. Marlow\'s books take '
      'five days to arrive. To win those customers back, Marlow plans to cut its delivery time to two days.</p>'
      '<p style="margin-top:22px;font-size:35px"><b>The plan depends on which of the following assumptions?</b></p>'
      '<p style="margin-top:16px;font-size:30px;line-height:1.4">'
      + "<br>".join(f"({k}) {v}" for k, v in CH.items()) + "</p></div>")
d.add(parts.solve("Name the goal.", ["Problem: customers left", "Fix: 2-day delivery", "Goal: win them back"],
                  "The plan only helps if delivery had something to do with why they left."))
d.add(parts.solve("Flip choice B.", ["“None left because of delivery”", "→ faster books change nothing",
                                     "→ plan <span class=acc>fails</span>"],
                  "Its opposite breaks the plan, so B is needed."))
d.add(parts.solve("Flip the rest.", ["A: “most”, “one day”: too big", "C: prices are another story",
                                     "E: rivals can be any speed"]))
d.add(parts.answer("The answer is B.", "B", "If no one left over slow delivery, cutting delivery time gives "
                   "them no reason to come back."))
d.add(parts.trap("D", "Costs are not the goal.", "The plan aims to win customers back. Even if costs rise, "
                 "that goal can still be met, so D is not needed."))
d.add(parts.recap("Assumption: negate and check", "The right choice, flipped, makes the plan fall apart.",
                  "No delivery reason → <span class=acc>no return</span>"))
d.add(parts.cta("Save it.", "Negate each choice on your next assumption question. New question every day."))

if __name__ == "__main__":
    for i in range(len(d.slides)):
        assert not check_html(d.html(i)), i
    paths = d.render(pathlib.Path(__file__).resolve().parents[1] / "out" / ID, stem=ID)
    print("check:", check(paths, len(d.slides)) or "PASS")
