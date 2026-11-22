"""Carousel 2026-11-22-c1, Data Sufficiency Drill: is x > y? Original question; verified in items/2026-11-22-c1.py.
(1) x - y > -1 and (2) x != y, x and y integers. Answer C. Trap A. Difficulty: our estimate, medium."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import Deck, check, check_html
import parts

ID = "2026-11-22-c1"
DS_KEY = ("(A) Statement 1 alone is enough<br>(B) Statement 2 alone is enough<br>(C) Only both together<br>"
          "(D) Each one alone is enough<br>(E) Not even both together")
d = Deck("Data Sufficiency Drill", ground="paper")
d.add(parts.cover("Is x bigger?<br>Two clues.", "Data Insights · our estimate: medium"), ground="paper")
d.add(parts.stake("Data Sufficiency lives in Data Insights.", "You don't solve for x. You decide whether the "
                  "clues are enough to answer. Test cases do the work."))
d.add('<div style="margin-top:70px"><p><b>x</b> and <b>y</b> are integers. Is <b>x &gt; y</b>?</p>'
      '<p style="margin-top:30px">(1) x − y &gt; −1<br>(2) x ≠ y</p>'
      f'<p style="margin-top:36px;font-size:34px;line-height:1.5">{DS_KEY}</p>'
      '<p style="margin-top:26px;font-size:32px;opacity:.75">Pick one before you swipe.</p></div>')
d.add(parts.solve("Test statement 1.", ["x − y &gt; −1 means x − y ≥ 0", "x = 4, y = 3 → yes",
                                         "x = 3, y = 3 → <span class=acc>no</span>"], "Two answers. Not enough."))
d.add(parts.solve("Test statement 2.", ["x = 5, y = 2 → yes", "x = 2, y = 5 → <span class=acc>no</span>"],
                  "Two answers again. Not enough."))
d.add(parts.solve("Now use both.", ["(1): x ≥ y", "(2): x ≠ y", "So x &gt; y, every time"],
                  "One answer. Together they're enough."))
d.add(parts.answer("The answer is C.", "C", "Neither clue works alone. Together they rule out the tie."))
d.add(parts.trap("A", "Statement 1 allows a tie.", "Integers with x − y &gt; −1 can still have x − y = 0. "
                 "Always test the edge case where both sides are equal."))
d.add(parts.recap("DS: break the statement", "Find one case that says yes and one that says no.",
                  "Yes and no → not sufficient<br>Always the same → sufficient"))
d.add(parts.cta("Save it.", "Use the tie test on your next inequality question. New question every day."))

if __name__ == "__main__":
    for i in range(len(d.slides)):
        assert not check_html(d.html(i)), i
    paths = d.render(pathlib.Path(__file__).resolve().parents[1] / "out" / ID, stem=ID)
    print("check:", check(paths, len(d.slides)) or "PASS")
