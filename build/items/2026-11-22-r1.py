"""Start at 100. Up 20%: 100 x 1.2 = 120. Down 20%: 120 x 0.8 = 96. Net change -4% (B).
Shortcut: (1 + p)(1 - p) = 1 - p^2, so up then down by p% always loses p^2/100 percent: 400/100 = 4.
Trap: A (0%), assuming the two 20% moves cancel; the second 20% is taken from 120, not 100."""
from fractions import Fraction as F
ITEM = dict(kind="PS", choices={"A": 0, "B": -4, "C": 4, "D": -2, "E": 2}, answer="B",
            compute=lambda: (F(100) * F(120, 100) * F(80, 100) - 100) / 100 * 100)
