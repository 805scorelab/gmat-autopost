"""Data Sufficiency. Pens cost $2 each and books cost $5 each. Ana bought only pens and books, at least one
of each. How many pens did she buy?
(1) She spent $19 in total. 2p + 5n = 19 with p, n >= 1: (p, n) = (7, 1) or (2, 3). Not sufficient.
(2) She bought 5 items. p + n = 5: many splits. Not sufficient.
Together: 2p + 5(5 - p) = 19, 25 - 3p = 19, p = 2. Sufficient. Answer C.
Trap: A, assuming the whole-number limit leaves only one way to make $19."""
ITEM = dict(kind="DS", answer="C",
            worlds=lambda: ((p, n) for p in range(1, 40) for n in range(1, 40)),
            target=lambda c: c[0],
            s1=lambda c: 2 * c[0] + 5 * c[1] == 19,
            s2=lambda c: c[0] + c[1] == 5)
