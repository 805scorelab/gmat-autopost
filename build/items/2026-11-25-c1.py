"""A tank holds 40 liters of a solution that is 25% acid. How many liters of pure water must be added so that the
solution is 20% acid?
Hand solution: acid stays the same, 25% of 40 = 10 liters. After adding w liters of water, 10 / (40 + w) = 1/5, so
40 + w = 50 and w = 10 (C).
Check: 10 liters of acid in 50 liters is 20%.
Trap: E (50) is the new total volume, not the water added. A (2) is 5% of 40 (the drop in percent applied to the
old volume). B (8) is 20% of 40. D (12) is 10 + 2, mixing the acid amount with the trap step."""
from fractions import Fraction as F
ITEM = dict(kind="PS", choices={"A": 2, "B": 8, "C": 10, "D": 12, "E": 50}, answer="C",
            # independent check: try water amounts in steps of 1/10 liter up to 200 liters and keep the one that
            # makes the acid share exactly 20%.
            compute=lambda: [F(k, 10) for k in range(0, 2001)
                             if F(25, 100) * 40 / (40 + F(k, 10)) == F(20, 100)][0])
