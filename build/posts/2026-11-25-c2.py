"""Carousel 2026-11-25-c2, Critical Reasoning Breakdown: library hours (resolve the paradox). Original argument
for 805 Score Lab.

Situation: Last year, Tovin Public Library kept its doors open until 9 p.m. on weekdays instead of 6 p.m. Yet over
the year, the number of print books borrowed on weekdays fell slightly.
Question: which choice most helps explain the drop?
Answer E (the library also began lending e-books through an app, and many regular borrowers switched to them). That
gives a reason print borrowing could fall even with more open hours: the borrowing moved to a format the count leaves
out.
(A) Weekend print borrowing also fell: describes a wider drop but gives no cause. It deepens the puzzle.
(B) Most evening visitors came for study rooms: explains why the longer hours added little, but not why borrowing
fell. Trap.
(C) 300 new print titles: should raise borrowing, so it makes the drop harder to explain.
(D) Residents preferred the longer hours: a preference says nothing about borrowing.
Difficulty: our estimate, medium.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import Deck, check, check_html
import parts

ID = "2026-11-25-c2"
CH = {"A": "Weekend borrowing of print books also fell slightly last year.",
      "B": "Most people who came in the new evening hours used the study rooms rather than borrowing books.",
      "C": "The library added 300 new print titles to its shelves during the year.",
      "D": "Many residents told the library they preferred the longer weekday hours.",
      "E": "Last year the library also began lending e-books through an app, and many regular borrowers switched to them."}
d = Deck("Critical Reasoning Breakdown", ground="paper")
d.add(parts.cover("Longer hours.<br>Fewer books?", "Verbal · our estimate: medium"), ground="forest")
d.add(parts.stake("Paradox questions want a cause.", "Both facts are true. The right choice gives a reason "
                  "they can both be true at once."))
d.add('<div style="margin-top:50px"><p style="font-size:37px;line-height:1.4">Last year, Tovin Public Library stayed '
      'open until 9 p.m. on weekdays instead of 6 p.m. Yet over the year, the number of print books borrowed on '
      'weekdays fell slightly.</p>'
      '<p style="margin-top:22px;font-size:37px"><b>Which of the following most helps explain the drop?</b></p>'
      '<p style="margin-top:16px;font-size:31px;line-height:1.42">'
      + "<br>".join(f"({k}) {v}" for k, v in CH.items()) + "</p></div>")
d.add(parts.solve("Name the tension.", ["More hours to borrow", "Fewer print books borrowed", "Expected: up. Got: down."],
                  "We need a force pulling borrowing down."))
d.add(parts.solve("Test each choice.", ["A, C, D: no force down", "B: why no rise, not why a fall",
                                        "E: borrowers <span class=acc>moved to e-books</span>"],
                  "Only E pushes the print count down."))
d.add(parts.answer("The answer is E.", "E", "Borrowing shifted to e-books. Print loans can fall even while "
                   "the doors stay open longer."))
d.add(parts.trap("B", "It explains \"flat\", not \"down\".", "Study-room visitors show why the extra hours "
                 "added few loans. Nothing in B takes loans away. The puzzle asks for a fall."))
d.add(parts.recap("Paradox: explain the gap", "The answer makes both facts true together.",
                  "Fact 1 says up, fact 2 says down<br>→ find the force behind fact 2"))
d.add(parts.cta("Save it.", "Ask \"what pushes it down?\" on your next paradox question. New question every day."))

if __name__ == "__main__":
    for i in range(len(d.slides)):
        assert not check_html(d.html(i)), i
    paths = d.render(pathlib.Path(__file__).resolve().parents[1] / "out" / ID, stem=ID)
    print("check:", check(paths, len(d.slides)) or "PASS")
