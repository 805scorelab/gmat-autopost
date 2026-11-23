"""1/2 + 1/3 + 1/6 = ? Common denominator 6: 3/6 + 2/6 + 1/6 = 6/6 = 1 (C).
Trap: D (3/11), adding the tops and the bottoms separately."""
from fractions import Fraction as F
ITEM = dict(kind="PS", choices={"A": F(1, 2), "B": F(5, 6), "C": F(1), "D": F(3, 11), "E": F(7, 6)}, answer="C",
            compute=lambda: F(1, 2) + F(1, 3) + F(1, 6))
