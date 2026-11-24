"""The sum of 5 consecutive integers is 85. What is the largest of the 5 integers?
Hand solution: the middle integer is the average, 85 / 5 = 17. The list is 15, 16, 17, 18, 19, so the largest is 19 (C).
Wrong choices: A (15) is the smallest; B (17) is the middle (trap: stopping at the average); D (20) adds 3 to the
middle; E (21) adds 4 to the middle."""
ITEM = dict(kind="PS", choices={"A": 15, "B": 17, "C": 19, "D": 20, "E": 21}, answer="C",
            # independent check: scan every starting integer and keep the run of 5 that sums to 85
            compute=lambda: [n + 4 for n in range(-200, 200) if sum(range(n, n + 5)) == 85][0])
