"""n = 6k + 4, so 2n = 12k + 8 = 6(2k + 1) + 2. The remainder is 2 (B).
Trap: D (4), copying the original remainder; doubling to 8 and forgetting to reduce gives no listed choice."""
ITEM = dict(kind="PS", choices={"A": 0, "B": 2, "C": 3, "D": 4, "E": 5}, answer="B",
            compute=lambda: {(2 * n) % 6 for n in range(1, 10000) if n % 6 == 4}.pop())
