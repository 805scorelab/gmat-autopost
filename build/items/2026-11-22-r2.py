"""The average of 4 numbers is 10, so they sum to 40. Add a fifth number and the average becomes 12, so the five
sum to 60. The new number is 60 - 40 = 20 (C). Trap: A (12), taking the new average as the new number; B (14) adds
the 2-point rise to 12 once; D (22) and E (2) come from mixing the sums."""
ITEM = dict(kind="PS", choices={"A": 12, "B": 14, "C": 20, "D": 22, "E": 2}, answer="C",
            compute=lambda: [n for n in range(-100, 101) if (40 + n) == 12 * 5][0])
