"""Carousel 2026-11-24-c2, GMAT Strategy: Quant pacing checkpoints. Original question for 805 Score Lab.

Weekly strategy slot. Facts used (docs/exam-facts.md): Quant is 21 questions in 45 minutes; you may review and change
up to 3 answers per section. "Even pace" is our arithmetic from the official count and time, not a GMAC recommendation.
Question: 20 minutes into GMAT Quant, you have just finished question 7. Compared with an even pace, where are you?
(A) Ahead by 5 min (B) On pace (C) Behind by about 3 min (D) Behind by 5 min (E) Behind by 6 min.
Answer D, verified in build/items/2026-11-24-c2.py: 45/21 = 15/7 min per question; 7 x 15/7 = 15 min; 20 - 15 = 5.
Wrong choices: A flips the sign; B ignores the clock; C counts question 8 as done (8 x 15/7 = about 17.1, trap);
E rounds the pace down to 2 minutes (7 x 2 = 14).
Checkpoints: 7 done at 15 min, 14 at 30, 21 at 45 (exact, since 21 = 3 x 7).
No claim about scores, outcomes or what most test takers do.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from brand import Deck, check, check_html
import parts

ID = "2026-11-24-c2"
d = Deck("GMAT Strategy", ground="paper")
d.add(parts.cover("20 minutes in.<br>Behind or not?", "Strategy · GMAT Quant pacing"), ground="mint")
d.add(parts.stake("Pacing is just arithmetic.", "Quant is 21 questions in 45 minutes. That one fact gives you "
                  "3 checkpoints you can hold in your head."))
d.add(parts.question(["You are <b>20 minutes</b> into GMAT Quant and have just finished <b>question 7</b>.",
                      "Compared with an even pace, where are you?"],
                     {"A": "Ahead by 5 min", "B": "On pace", "C": "Behind by about 3 min",
                      "D": "Behind by 5 min", "E": "Behind by 6 min"}))
d.add(parts.solve("Find the even pace.", ["45 min ÷ 21 questions", "= 15/7 min each", "≈ 2 min 8 s each"]))
d.add(parts.solve("Price 7 questions.", ["7 × 15/7 = <span class=acc>15 min</span>", "You used 20 min",
                                         "20 − 15 = 5 min behind"]))
d.add(parts.answer("The answer is D.", "D", "5 minutes behind an even pace, with 14 questions left."))
d.add(parts.trap("C", "Count only what you finished.", "Question 8 is open, not done. Counting it gives "
                 "8 × 15/7 ≈ 17 min and makes the gap look like 3. E comes from rounding the pace to 2 min."))
d.add(parts.solve("Your 3 checkpoints.", ["7 done → 15 min", "14 done → 30 min", "21 done → 45 min"],
                  "21 splits into 3 blocks of 7, so the checkpoints land on round numbers."))
d.add(parts.recap("Quant pacing: blocks of 7", "Check the clock after questions 7 and 14.",
                  "7 → 15 min · 14 → 30 min<br>21 → <span class=acc>45 min</span>"))
d.add(parts.cta("Save it.", "Practice with the 7, 14, 21 checkpoints on your next timed set. New post every day."))

if __name__ == "__main__":
    for i in range(len(d.slides)):
        assert not check_html(d.html(i)), i
    paths = d.render(pathlib.Path(__file__).resolve().parents[1] / "out" / ID, stem=ID)
    print("check:", check(paths, len(d.slides)) or "PASS")
