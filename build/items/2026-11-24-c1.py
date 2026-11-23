"""Machine A alone makes a batch of labels in 6 hours. Machines A and B together make the same batch in 4 hours.
At its own constant rate, how many hours does machine B alone take to make the batch?
Hand solution: rates in batches per hour. A = 1/6, together = 1/4, so B = 1/4 - 1/6 = 3/12 - 2/12 = 1/12. B takes 12 hours (D).
Check: in 12 hours A makes 2 batches and B makes 1, so 3 batches in 12 hours, 1 batch in 4 hours.
Trap: A (2), subtracting the times (6 - 4) instead of the rates. B (5) is the plain average of 6 and 4.
C (10) adds the times. E (24) is 6 x 4."""
from fractions import Fraction as F
ITEM = dict(kind="PS", choices={"A": 2, "B": 5, "C": 10, "D": 12, "E": 24}, answer="D",
            # independent check: simulate whole minutes; B's time t (in minutes, up to 100 hours) must make
            # A and B together finish exactly one batch in 240 minutes.
            compute=lambda: [F(t, 60) for t in range(1, 6001)
                             if F(240, 360) + F(240, t) == 1][0])
