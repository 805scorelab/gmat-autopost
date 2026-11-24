"""What is 0.2 x 0.3? 2 x 3 = 6 and the factors have 2 decimal places in total, so 0.06: B.
Trap: A (0.6), counting only 1 decimal place."""
from fractions import Fraction as F
CHOICES = {"A": F(6, 10), "B": F(6, 100), "C": F(6, 1000), "D": F(6), "E": F(5, 10)}
ITEM = dict(kind="PS", choices=CHOICES, answer="B", compute=lambda: F(2, 10) * F(3, 10))
