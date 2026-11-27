"""What is 2^10? Double ten times: 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, so 2^10 = 1024 (D).
Trap: A (20), multiplying 2 x 10. B (512) is 2^9, one doubling short; C (1000) is the rounded "about a thousand";
E (2048) is 2^11."""
def _brute():
    v = 1
    for _ in range(10):
        v += v          # doubling by addition, independent of the ** operator
    return v
ITEM = dict(kind="PS", choices={"A": 20, "B": 512, "C": 1000, "D": 1024, "E": 2048}, answer="D", compute=_brute)
