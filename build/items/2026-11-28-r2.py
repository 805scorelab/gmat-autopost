"""Data Sufficiency. n is an integer. Is n odd?
(1) 3n is odd. An odd product needs every factor odd, so n is odd. Sufficient.
(2) n + n is even. 2n is even for every integer n. Not sufficient.
Answer A. Trap: D, reading (2) as telling us something about n."""
ITEM = dict(kind="DS", answer="A",
            worlds=lambda: range(-200, 201),
            target=lambda n: n % 2 == 1,
            s1=lambda n: (3 * n) % 2 == 1,
            s2=lambda n: (n + n) % 2 == 0)
