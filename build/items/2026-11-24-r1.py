"""What is 28% of 75?
Hand solution: x% of y = y% of x, because both equal x * y / 100. So 28% of 75 = 75% of 28 = three quarters of 28 = 21 (B).
Trap: C (22.4), a slip that takes 80% of 28 instead of 75%. Choices D (24) and E (28) come from rough rounding.
Difficulty: our estimate, easy to medium without a calculator."""
from fractions import Fraction as F


def _pct():
    # independent method: count 28 hundredths of 75, one hundredth at a time
    total = F(0)
    for _ in range(28):
        total += F(75, 100)
    return total


ITEM = dict(kind="PS", choices={"A": F(98, 5), "B": 21, "C": F(112, 5), "D": 24, "E": 28}, answer="B", compute=_pct)
