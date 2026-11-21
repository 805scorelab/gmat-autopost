"""Is xy even? x, y positive integers. (1) x + y is odd: one is even, so xy is even. Sufficient.
(2) y is odd: x odd gives no, x even gives yes. Not sufficient. Answer A."""
ITEM = dict(kind="DS", answer="A",
            worlds=lambda: ((x, y) for x in range(1, 30) for y in range(1, 30)),
            target=lambda c: c[0] * c[1] % 2 == 0,
            s1=lambda c: (c[0] + c[1]) % 2 == 1,
            s2=lambda c: c[1] % 2 == 1)
