"""Carousel 2026-11-23-c2, Critical Reasoning Breakdown: calorie labels (assumption). Original argument for 805 Score Lab.

Argument: Larkfield Bread put calorie counts on its menu boards in March. In the six months since, sales of its
high-calorie pastries fell by a third, while customer visits stayed the same. Conclusion: the labels caused customers
to buy fewer high-calorie pastries.
Answer B (no other change at Larkfield since March, such as higher pastry prices, accounts for the drop). Negate it:
another change explains the drop, and the conclusion loses its support. Required.
(A) Most customers read the boards: not required; the drop could come from a minority who read them. Trap.
(C) Other chains: outside the argument, which is only about Larkfield. (D) What customers bought instead: the
conclusion is about pastries, not substitutes. (E) Profitability: says nothing about why sales fell.
Difficulty: our estimate, medium.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import Deck, check, check_html
import parts

ID = "2026-11-23-c2"
CH = {"A": "Most Larkfield customers read the menu boards before ordering.",
      "B": "No other change at Larkfield since March, such as higher pastry prices, accounts for the drop.",
      "C": "Calorie labels would cut pastry sales at other bakery chains too.",
      "D": "Customers who skipped pastries bought lower-calorie items instead.",
      "E": "High-calorie pastries were Larkfield's most profitable products."}
d = Deck("Critical Reasoning Breakdown", ground="paper")
d.add(parts.cover("Did the labels<br>do it?", "Verbal · our estimate: medium"), ground="paper")
d.add(parts.stake("Assumption questions have a test.", "Negate the choice. If the argument falls apart, "
                  "the argument needed it."))
d.add('<div style="margin-top:50px"><p style="font-size:37px;line-height:1.4">In March, the bakery chain Larkfield Bread '
      'began showing calorie counts on its menu boards. In the six months since, sales of its high-calorie pastries '
      'fell by a third, while customer visits stayed the same. So the labels caused customers to buy fewer '
      'high-calorie pastries.</p>'
      '<p style="margin-top:22px;font-size:37px"><b>The argument depends on which assumption?</b></p>'
      '<p style="margin-top:16px;font-size:31px;line-height:1.42">'
      + "<br>".join(f"({k}) {v}" for k, v in CH.items()) + "</p></div>")
d.add(parts.solve("Map the argument.", ["Evidence: labels went up,", "pastry sales fell by 1/3", "Conclusion: labels caused it"],
                  "The gap: did anything else change?"))
d.add(parts.solve("Negate B.", ["Some other change, like", "higher prices, explains", "the drop."],
                  "Then the labels may have done nothing. The argument collapses."))
d.add(parts.answer("The answer is B.", "B", "The argument needs the labels to be the only explanation left standing."))
d.add(parts.trap("A", "\"Most\" is more than it needs.", "Negate A: most customers don't read the boards. "
                 "The ones who do could still cut a third of pastry sales. C, D and E sit outside the argument."))
d.add(parts.recap("Assumption: negate it", "If the negated choice breaks the argument, it's the answer.",
                  "Cause claimed → assume<br>no other cause"))
d.add(parts.cta("Save it.", "Run the negation test on your next assumption question. New question every day."))

if __name__ == "__main__":
    for i in range(len(d.slides)):
        assert not check_html(d.html(i)), i
    paths = d.render(pathlib.Path(__file__).resolve().parents[1] / "out" / ID, stem=ID)
    print("check:", check(paths, len(d.slides)) or "PASS")
