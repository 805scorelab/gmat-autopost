"""What is the units digit of 7^23?
Hand solution: units digits of 7^1..7^4 are 7, 9, 3, 1 and then repeat every 4. 23 = 4 x 5 + 3, so 7^23 ends like
7^3: 3 (B). Trap: C (7), assuming any power of 7 ends in 7. A (1) is the cycle's end, D (9) is 7^2, E (0) impossible."""
ITEM = dict(kind="PS", choices={"A": 1, "B": 3, "C": 7, "D": 9, "E": 0}, answer="B",
            compute=lambda: pow(7, 23) % 10)
