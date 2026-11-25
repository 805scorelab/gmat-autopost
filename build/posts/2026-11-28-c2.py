"""Carousel 2026-11-28-c2, Critical Reasoning Breakdown: city pools (most strongly supported / inference). Original
argument for 805 Score Lab.

Stimulus: Last summer, Dalby's two public pools charged the same entry fee. The Riverside pool lowered its fee by half
and its number of visits rose by 40 percent. The Hill Street pool kept its old fee and its number of visits did not
change. Riverside's fee income for the summer was lower than the summer before.
Question: which is most strongly supported by the statements above?
Answer C (Riverside's fee income fell because the larger number of visits did not make up for the lower fee). Visits
x 1.4 at half the fee gives 0.7 of last summer's income, matching the stated fall; nothing beyond the statements is
needed. (Verified: 1.4 x 0.5 = 0.7 < 1.)
(A) Lower fees always raise pool visits: "always" goes far beyond one pool in one summer.
(B) Hill Street's visitors care less about price: nothing in the stimulus tells us why their visits held steady.
(D) Riverside earned more than Hill Street this summer: we know neither pool's size or visit count, so no comparison.
(E) Dalby should lower fees at both pools: the trap. It is a recommendation; the statements show income fell, which
    if anything argues against it, and say nothing about the city's goals.
Only C follows from the statements alone, so no second choice is defensible.
Difficulty: our estimate, medium.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import Deck, check, check_html
import parts

ID = "2026-11-28-c2"
assert 1.4 * 0.5 < 1
CH = {"A": "Lowering the entry fee at a public pool always increases the number of visits.",
      "B": "Visitors to the Hill Street pool care less about price than visitors to Riverside.",
      "C": "At Riverside, the rise in visits was not large enough to make up for the lower fee.",
      "D": "Riverside earned more in fees this summer than the Hill Street pool did.",
      "E": "Dalby should lower the entry fee at both of its public pools."}
d = Deck("Critical Reasoning Breakdown", ground="forest")
d.add(parts.cover("Half price.<br>Less money?", "Verbal · our estimate: medium"), ground="forest")
d.add(parts.stake("Supported = nothing new allowed.", "The right choice must follow from the statements alone. "
                  "Anything that adds a cause, a rule or a plan is outside the box."))
d.add('<div style="margin-top:50px"><p style="font-size:35px;line-height:1.4">Last summer, Dalby\'s two public pools '
      'charged the same entry fee. This summer, the Riverside pool cut its fee in half, and its visits rose by '
      '40 percent. The Hill Street pool kept its fee, and its visits did not change. Riverside\'s fee income this '
      'summer was lower than last summer.</p>'
      '<p style="margin-top:22px;font-size:35px"><b>Which is most strongly supported by the statements above?</b></p>'
      '<p style="margin-top:16px;font-size:30px;line-height:1.4">'
      + "<br>".join(f"({k}) {v}" for k, v in CH.items()) + "</p></div>")
d.add(parts.solve("List the facts.", ["Fee: half", "Visits: +40%", "Income: down"],
                  "Three facts about Riverside. Stay inside them."))
d.add(parts.solve("Put them together.", ["Income = fee × visits", "0.5 × 1.4 = <span class=acc>0.7</span>",
                                         "More visits, still less money"],
                  "That is exactly what choice C says."))
d.add(parts.solve("Test the rest.", ["A: “always” is too big", "B: no reason is given",
                                     "D: no sizes to compare"]))
d.add(parts.answer("The answer is C.", "C", "Half the fee with 40% more visits brings in less money, which "
                   "matches the stated fall in income."))
d.add(parts.trap("E", "A plan is not a fact.", "“Should” brings in a goal the statements never give. "
                 "The facts even show the cut lost Riverside money."))
d.add(parts.recap("Supported: stay inside the box", "Combine the facts; reject any new rule, cause or plan.",
                  "Fee × visits → <span class=acc>income down</span>"))
d.add(parts.cta("Save it.", "Combine the facts on your next inference question. New question every day."))

if __name__ == "__main__":
    for i in range(len(d.slides)):
        assert not check_html(d.html(i)), i
    paths = d.render(pathlib.Path(__file__).resolve().parents[1] / "out" / ID, stem=ID)
    print("check:", check(paths, len(d.slides)) or "PASS")
