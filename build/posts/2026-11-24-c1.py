"""Carousel 2026-11-24-c1, Problem of the Day: work rates (machine B alone). Original question for 805 Score Lab.

Machine A alone makes a batch of labels in 6 hours. Machines A and B together make the same batch in 4 hours.
At its constant rate, how many hours does machine B alone take?
(A) 2 (B) 5 (C) 10 (D) 12 (E) 24. Answer D, verified in build/items/2026-11-24-c1.py.
Hand solution: work in batches per hour. B = 1/4 - 1/6 = 1/12, so 12 hours.
Wrong choices: A (2) subtracts the times instead of the rates (trap); B (5) averages 6 and 4; C (10) adds them;
E (24) multiplies them.
Difficulty: our estimate, medium.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import Deck, check, check_html
import parts

ID = "2026-11-24-c1"
d = Deck("Problem of the Day", ground="paper")
d.add(parts.cover("Both: 4 hours.<br>B alone?", "Quant · our estimate: medium"), ground="forest")
d.add(parts.stake("Times don't add. Rates do.", "Hours per job can't be added or subtracted. Jobs per hour can. "
                  "Flip each time into a rate first."))
d.add(parts.question(["Machine A alone makes a batch of labels in <b>6 hours</b>. Machines A and B together "
                      "make the same batch in <b>4 hours</b>.",
                      "At its constant rate, how many hours does machine B alone take?"],
                     {"A": 2, "B": 5, "C": 10, "D": 12, "E": 24}))
d.add(parts.solve("Turn times into rates.", ["A: 1 batch in 6 h → 1/6 per hour", "A + B: 1 batch in 4 h → 1/4 per hour"],
                  "Rates are what you can subtract."))
d.add(parts.solve("Subtract the rates.", ["B = 1/4 − 1/6", "B = 3/12 − 2/12", "B = <span class=acc>1/12</span> per hour"],
                  "1/12 of a batch each hour means 12 hours for the whole batch."))
d.add(parts.solve("Check it.", ["In 12 hours: A makes 2 batches", "B makes 1 batch", "3 batches in 12 h = 1 in 4 h ✓"]))
d.add(parts.answer("The answer is D.", "D", "Machine B alone takes 12 hours. It is the slower machine, "
                   "so its time has to be longer than 6."))
d.add(parts.trap("A", "6 − 4 = 2 subtracts the wrong thing.", "Subtracting hours gives 2, which would make B "
                 "3 times faster than A. Then together they would beat 4 hours easily."))
d.add(parts.recap("Work rate: flip, then add", "Rate = 1 ÷ time. Rates add when machines work together.",
                  "1/A + 1/B = 1/together<br>1/6 + 1/B = 1/4 → B = <span class=acc>12</span>"))
d.add(parts.cta("Save it.", "Flip times into rates on your next work question. New question every day."))

if __name__ == "__main__":
    for i in range(len(d.slides)):
        assert not check_html(d.html(i)), i
    paths = d.render(pathlib.Path(__file__).resolve().parents[1] / "out" / ID, stem=ID)
    print("check:", check(paths, len(d.slides)) or "PASS")
