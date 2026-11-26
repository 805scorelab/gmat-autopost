"""Data Sufficiency. The price of a lamp went up. By what percent did it go up?
(1) The price went up by $12. Old price unknown (12 on 60 is 20%, 12 on 40 is 30%). Not sufficient.
(2) The new price is $72. Old price unknown. Not sufficient.
Together: old price = 72 - 12 = 60, percent = 12 / 60 = 20%. Sufficient. Answer C.
Trap: E, thinking the old price is needed as a stated fact; it follows from new minus increase."""
from fractions import Fraction as F
ITEM = dict(kind="DS", answer="C",
            worlds=lambda: ((old, new) for old in range(1, 201) for new in range(old + 1, 301)),
            target=lambda c: F(c[1] - c[0], c[0]) * 100,
            s1=lambda c: c[1] - c[0] == 12,
            s2=lambda c: c[1] == 72)
