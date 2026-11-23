"""Pacing (strategy). GMAT Quant has 21 questions in 45 minutes. 20 minutes in, you have just finished question 7
and are starting question 8. Compared with an even pace (45 minutes spread equally over 21 questions), where are you?
Hand solution: even pace = 45/21 = 15/7 minutes (about 2 min 8 s) per question. 7 questions at even pace = 15 minutes.
20 - 15 = 5 minutes behind (D). Value = minutes behind (negative means ahead).
Wrong choices: A (ahead by 5) flips the sign. B (on pace) ignores the clock. C (behind by about 3) counts question 8
as done: 8 x 15/7 = about 17.1 minutes, so about 2.9 behind (trap). E (behind by 6) rounds the pace down to 2 minutes:
7 x 2 = 14, 20 - 14 = 6."""
from fractions import Fraction as F
ITEM = dict(kind="PS", choices={"A": -5, "B": 0, "C": 3, "D": 5, "E": 6}, answer="D",
            # independent: add the even-pace time question by question, in seconds, then convert to minutes
            compute=lambda: (20 * 60 - sum(F(45 * 60, 21) for _ in range(7))) / 60)
