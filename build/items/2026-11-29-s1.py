"""What is 15% of 80? 10% of 80 is 8 and 5% is half of that, 4, so 15% is 8 + 4 = 12 (C). Check: 0.15 x 80 = 12.
Trap: A (8), stopping at 10%. B (10) is 80 / 8; D (15) repeats the percent; E (68) is 80 - 12."""
from fractions import Fraction as F
def _brute():
    # independent check: the number y with y / 80 = 15 / 100, searched over 0..80 in steps of 0.5
    sols = [F(k, 2) for k in range(0, 161) if F(k, 2) * 100 == 15 * 80]
    assert len(sols) == 1
    return sols[0]
ITEM = dict(kind="PS", choices={"A": 8, "B": 10, "C": 12, "D": 15, "E": 68}, answer="C", compute=_brute)
