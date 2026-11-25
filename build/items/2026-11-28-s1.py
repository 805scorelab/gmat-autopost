"""If 3/x = 0.75, what is x? 0.75 = 3/4, so 3/x = 3/4 and x = 4 (D). Check: 3 / 4 = 0.75.
Trap: A (2.25), multiplying 3 x 0.75 instead of dividing 3 by 0.75. B (0.25) is 1 - 0.75; C (3.75) is 3 + 0.75;
E (4.5) is 3 x 1.5."""
from fractions import Fraction as F
CHOICES = {"A": F(225, 100), "B": F(25, 100), "C": F(375, 100), "D": F(4), "E": F(45, 10)}
def _brute():
    # independent check: search every choice-sized value in steps of 0.01 for 3/x = 0.75
    sols = [F(k, 100) for k in range(1, 1001) if F(3) / F(k, 100) == F(3, 4)]
    assert len(sols) == 1
    return sols[0]
ITEM = dict(kind="PS", choices=CHOICES, answer="D", compute=_brute)
