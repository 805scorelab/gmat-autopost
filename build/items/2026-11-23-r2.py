"""Data Sufficiency. Is x positive? (x is a real number.)
(1) x^2 = 9: x = 3 or x = -3. Yes or no. Not sufficient.
(2) x^3 = 27: only x = 3 (a cube keeps the sign). Yes. Sufficient. Answer B.
Trap: D, reading x^2 = 9 as x = 3 and forgetting -3."""
from fractions import Fraction as F
ITEM = dict(kind="DS", answer="B",
            worlds=lambda: (F(n, 8) for n in range(-200, 201)),
            target=lambda x: x > 0,
            s1=lambda x: x * x == 9,
            s2=lambda x: x ** 3 == 27)
