"""Which one is prime? 51, 91, 57, 97, 87.
51 = 3 x 17, 91 = 7 x 13, 57 = 3 x 19, 87 = 3 x 29. Only 97 has no factor up to 9 (sqrt 97 < 10): D.
Trap: B (91), it looks prime but 91 = 7 x 13."""
CHOICES = {"A": 51, "B": 91, "C": 57, "D": 97, "E": 87}


def _only_prime():
    primes = [n for n in CHOICES.values() if n > 1 and all(n % d for d in range(2, n))]
    assert len(primes) == 1, primes
    return primes[0]


ITEM = dict(kind="PS", choices=CHOICES, answer="D", compute=_only_prime)
