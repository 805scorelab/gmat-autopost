"""3x + 5 = 20, so 3x = 15 and 6x = 2(3x) = 30 (D). No need to find x. Trap: B (15), stopping at 3x."""
ITEM = dict(kind="PS", choices={"A": 10, "B": 15, "C": 25, "D": 30, "E": 45}, answer="D",
            compute=lambda: [6 * x for x in range(-100, 100) if 3 * x + 5 == 20][0])
