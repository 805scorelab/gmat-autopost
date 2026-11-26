"""After a 20% discount, a jacket costs $80. What was the price before the discount?
Hand solution: the sale price is 80% of the original, so 0.8p = 80 and p = 100 (D). Check: 20% of 100 is 20,
100 - 20 = 80.
Wrong choices: C (96) adds 20% of the sale price, 80 + 16 (trap: the 20% is of the original, not of 80);
A (64) takes another 20% off; B (88) adds 10%; E (120) is 80 + 40."""
from fractions import Fraction as F
def _brute():
    # independent check: every price in cents from $0.01 to $500 that becomes $80 after 20% off
    sols = [F(c, 100) for c in range(1, 50001) if F(c, 100) * F(80, 100) == 80]
    assert len(sols) == 1
    return sols[0]
ITEM = dict(kind="PS", choices={"A": 64, "B": 88, "C": 96, "D": 100, "E": 120}, answer="D", compute=_brute)
