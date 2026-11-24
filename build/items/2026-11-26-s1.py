"""Which fraction is the greatest? 3/4, 5/7, 2/3, 7/10, 4/5.
Distance from 1: 1/4, 2/7, 1/3, 3/10, 1/5. The smallest gap is 1/5, so 4/5 is greatest: E.
Trap: A (3/4), the most familiar fraction; it trails 4/5 by 1/20."""
from fractions import Fraction as F
CHOICES = {"A": F(3, 4), "B": F(5, 7), "C": F(2, 3), "D": F(7, 10), "E": F(4, 5)}
ITEM = dict(kind="PS", choices=CHOICES, answer="E", compute=lambda: max(CHOICES.values()))
