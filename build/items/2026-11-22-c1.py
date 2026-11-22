"""Data Sufficiency. x and y are integers. Is x > y?
(1) x - y > -1: for integers this means x - y >= 0, so x >= y. x = y = 3 gives no; x = 4, y = 3 gives yes. Not sufficient.
(2) x != y: x = 2, y = 5 gives no; x = 5, y = 2 gives yes. Not sufficient.
Together: x >= y and x != y, so x > y. Sufficient. Answer C.
Trap: A, reading (1) as "x is bigger" and forgetting that x - y = 0 is allowed."""
ITEM = dict(kind="DS", answer="C",
            worlds=lambda: ((x, y) for x in range(-12, 13) for y in range(-12, 13)),
            target=lambda c: c[0] > c[1],
            s1=lambda c: c[0] - c[1] > -1,
            s2=lambda c: c[0] != c[1])
