"""20 students average 70 (total 1400); 30 average 80 (total 2400). All 50: 3800 / 50 = 76 (C).
Shortcut: the class of 30 has weight 30/50 = 3/5, so the average sits 3/5 of the way from 70 to 80: 76.
Trap: B (75), the plain average of 70 and 80, as if the classes were the same size."""
from fractions import Fraction as F
ITEM = dict(kind="PS", choices={"A": 74, "B": 75, "C": 76, "D": 77, "E": 78}, answer="C",
            compute=lambda: F(sum([70] * 20 + [80] * 30), 50))
