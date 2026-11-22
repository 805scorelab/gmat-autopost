"""Which is largest? 2^5 = 32, 3^3 = 27, 5^2 = 25, 6^2 = 36, 4^3 = 64. The largest is 4^3 = 64 (E).
Trap: D (6^2), picking the biggest base; or A (2^5), picking the biggest exponent."""
ITEM = dict(kind="PS", choices={"A": 32, "B": 27, "C": 25, "D": 36, "E": 64}, answer="E",
            compute=lambda: max([2 ** 5, 3 ** 3, 5 ** 2, 6 ** 2, 4 ** 3]))
