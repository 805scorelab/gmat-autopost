"""Carousel 2026-11-29-c1, Problem of the Day: two buses leaving together (LCM, counting endpoints). Original question
for 805 Score Lab.

Bus A leaves the station every 12 minutes and bus B every 18 minutes. Both leave together at 8:00 a.m. How many times
do they leave together from 8:00 a.m. to 11:00 a.m., counting both 8:00 and 11:00?
(A) 4 (B) 5 (C) 6 (D) 10 (E) 15. Answer C, verified in build/items/2026-11-29-c1.py.
Hand solution: LCM(12, 18) = 36 minutes; 180 / 36 = 5 gaps; 5 + 1 = 6 departures together.
Wrong choices: B (5) counts gaps, not departures (trap); A (4) counts only times strictly between; D (10) is
180 / 18; E (15) is 180 / 12.
Difficulty: our estimate, medium.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import Deck, check, check_html
import parts

ID = "2026-11-29-c1"
assert 180 // 36 + 1 == 6 and 36 % 12 == 0 and 36 % 18 == 0
d = Deck("Problem of the Day", ground="mint")
d.add(parts.cover("Two buses.<br>Same minute?", "Quant · our estimate: medium"), ground="mint")
d.add(parts.stake("Count the stops, not the gaps.", "Repeating events meet on a fixed beat. "
                  "The last step, counting them, is where the points go."))
d.add(parts.question(["Bus A leaves every <b>12 min</b>, bus B every <b>18 min</b>. "
                      "Both leave at <b>8:00 a.m.</b>",
                      "How many times do they leave together from 8:00 to 11:00 a.m., ends included?"],
                     {"A": 4, "B": 5, "C": 6, "D": 10, "E": 15}))
d.add(parts.solve("Find the shared beat.", ["12: 12, 24, <span class=acc>36</span>", "18: 18, <span class=acc>36</span>",
                                            "LCM = 36 minutes"], "They meet every 36 minutes."))
d.add(parts.solve("Measure the window.", ["8:00 to 11:00", "= 180 minutes", "180 ÷ 36 = 5 gaps"]))
d.add(parts.solve("Gaps + 1 = stops.", ["5 gaps join 6 points", "8:00 · 8:36 · 9:12", "9:48 · 10:24 · 11:00"],
                  "Like 5 fence gaps between 6 posts."))
d.add(parts.answer("The answer is C.", "C", "They leave together 6 times: every 36 minutes from 8:00 through "
                   "11:00, both ends counted."))
d.add(parts.trap("B", "5 counts the gaps.", "180 ÷ 36 = 5 is the number of 36-minute gaps. "
                 "The 8:00 departure starts the first gap, so add 1."))
d.add(parts.recap("Repeating events: LCM, then count", "Meetings = window ÷ LCM, plus 1 when both ends count.",
                  "180 ÷ 36 + 1 = <span class=acc>6</span>"))
d.add(parts.cta("Save it.", "Count posts, not gaps, on your next timing question. New question every day."))

if __name__ == "__main__":
    for i in range(len(d.slides)):
        assert not check_html(d.html(i)), i
    paths = d.render(pathlib.Path(__file__).resolve().parents[1] / "out" / ID, stem=ID)
    print("check:", check(paths, len(d.slides)) or "PASS")
