"""Data Sufficiency. What is the value of x + y? (x and y are real numbers.)
(1) 2x + 2y = 14: divide both sides by 2, x + y = 7. One value. Sufficient.
(2) x - y = 1: x = 1, y = 0 gives 1; x = 5, y = 4 gives 9. Many values. Not sufficient.
Answer A. Trap: C, believing you must solve for x and y separately (two equations) before you know x + y."""
from fractions import Fraction as F
ITEM = dict(kind="DS", answer="A",
            worlds=lambda: ((F(a, 2), F(b, 2)) for a in range(-40, 41) for b in range(-40, 41)),
            target=lambda c: c[0] + c[1],
            s1=lambda c: 2 * c[0] + 2 * c[1] == 14,
            s2=lambda c: c[0] - c[1] == 1)
