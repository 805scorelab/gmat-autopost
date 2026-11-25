"""The average of 5 numbers is 12. One number is removed and the average of the other 4 is 10. Which number was
removed? Hand solution: sum of 5 = 60, sum of 4 = 40, removed = 20 (D).
Trap: A (2), the drop in the average. B (10) and C (12) are the averages; E (22) is 12 + 10."""
from itertools import product
def _brute():
    # independent check: every list of 5 whole numbers 0..30 with sum 60 whose 4 others average 10
    removed = set()
    for rest in product(range(0, 31), repeat=3):
        for x in range(0, 31):
            four = sum(rest) + x
            if four == 40:
                y = 60 - four
                nums = list(rest) + [x, y]
                if sum(nums) / 5 == 12 and sum(nums[:4]) / 4 == 10:
                    removed.add(y)
    assert removed == {20}
    return 20
ITEM = dict(kind="PS", choices={"A": 2, "B": 10, "C": 12, "D": 20, "E": 22}, answer="D", compute=_brute)
