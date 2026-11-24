"""What is the remainder when 5,738 is divided by 9?
Hand solution: a number leaves the same remainder mod 9 as its digit sum. 5 + 7 + 3 + 8 = 23, 2 + 3 = 5 (C).
Check: 9 x 637 = 5,733, and 5,738 - 5,733 = 5. Trap: E (8), the last digit, which is the remainder for 10, not 9.
A (2) and B (3) are the digits of 23; D (7) is a digit of the number."""
ITEM = dict(kind="PS", choices={"A": 2, "B": 3, "C": 5, "D": 7, "E": 8}, answer="C", compute=lambda: 5738 % 9)
