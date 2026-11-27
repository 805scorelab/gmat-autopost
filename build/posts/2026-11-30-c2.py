"""Carousel 2026-11-30-c2, Critical Reasoning Breakdown: café loyalty app (weaken). Original argument for
805 Score Lab.

Stimulus: In March, Fernhill Café launched a loyalty app. From March to May, the average amount a customer spent per
visit was 15% higher than from December to February. The café's manager concludes that the app led customers to
spend more on each visit.
Question: which of the following, if true, most seriously weakens the manager's conclusion?
Answer C (in early March, Fernhill raised the prices of most of its drinks by about 15%): the same spending rise
has another cause that needs no change in what customers buy, so the app may have changed nothing.
(A) Some customers who use the app turn off its notifications: says nothing about spending; at most a few
    customers see fewer reminders.
(B) Fernhill's app is similar to apps used by other cafés: irrelevant to whether it changed spending here.
(D) Customers who use the app visit Fernhill more often than those who do not: about visits, not spending per
    visit; if anything it fits the app working.
(E) Most of Fernhill's customers downloaded the app in its first month: the trap. Wide adoption makes an app
    effect more possible, so it does not weaken; it slightly supports.
Only C gives an alternative cause for the same numbers, so no second choice is defensible.
The 15% figures are part of the fictional stimulus, not a real statistic.
Difficulty: our estimate, easy to medium.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import Deck, check, check_html
import parts

ID = "2026-11-30-c2"
CH = {"A": "Some customers who use the app have turned off its notifications.",
      "B": "Fernhill's app is similar to loyalty apps used by many other cafés.",
      "C": "In early March, Fernhill raised the prices of most of its drinks by about 15%.",
      "D": "Customers who use the app visit Fernhill more often than customers who do not.",
      "E": "Most of Fernhill's regular customers downloaded the app in its first month."}
d = Deck("Critical Reasoning Breakdown", ground="mint")
d.add(parts.cover("New app.<br>Bigger bills?", "Verbal · our estimate: easy to medium"), ground="mint")
d.add(parts.stake("Weaken = find another cause.", "When a change follows a new thing, ask what else changed "
                  "at the same time."))
d.add('<div style="margin-top:50px"><p style="font-size:35px;line-height:1.4">In March, Fernhill Café launched a '
      'loyalty app. From March to May, the average amount a customer spent per visit was 15% higher than from '
      'December to February. The café\'s manager concludes that the app led customers to spend more on each '
      'visit.</p>'
      '<p style="margin-top:22px;font-size:35px"><b>Which of the following, if true, most seriously weakens the '
      'manager\'s conclusion?</b></p>'
      '<p style="margin-top:16px;font-size:30px;line-height:1.4">'
      + "<br>".join(f"({k}) {v}" for k, v in CH.items()) + "</p></div>")
d.add(parts.solve("Split it in two.", ["Fact: spend per visit +15%", "Claim: the app caused it",
                                       "Gap: anything else in March?"],
                  "Cause-and-effect conclusions are weak where another cause fits."))
d.add(parts.solve("Test choice C.", ["Prices up about 15%", "→ same orders cost 15% more",
                                     "→ app <span class=acc>not needed</span>"],
                  "The numbers rise even if no one buys anything extra."))
d.add(parts.solve("Clear the rest.", ["A: notifications, not spending", "B: other cafés don't matter",
                                      "D: visits, not spend per visit"]))
d.add(parts.answer("The answer is C.", "C", "A price rise of about 15% explains the higher spending "
                   "without the app, so the manager's cause is in doubt."))
d.add(parts.trap("E", "Downloads don't prove spending.", "Lots of downloads makes an app effect more "
                 "possible. That points toward the conclusion, not against it."))
d.add(parts.recap("Weaken a cause: offer a rival cause", "Look for something else that changed at the same "
                  "time and explains the same numbers.", "Price ↑ 15% → <span class=acc>spend ↑ 15%</span>"))
d.add(parts.cta("Save it.", "Hunt for the rival cause on your next weaken question. New question every day."))

if __name__ == "__main__":
    for i in range(len(d.slides)):
        assert not check_html(d.html(i)), i
    paths = d.render(pathlib.Path(__file__).resolve().parents[1] / "out" / ID, stem=ID)
    print("check:", check(paths, len(d.slides)) or "PASS")
