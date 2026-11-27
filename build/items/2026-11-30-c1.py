"""If 3^x * 9^y = 3^12 and x - y = 3, what is the value of x?
Hand solution: 9^y = (3^2)^y = 3^(2y), so 3^(x + 2y) = 3^12 and x + 2y = 12. With x - y = 3, subtract:
3y = 9, y = 3, x = 6 (C). Check: 3^6 * 9^3 = 729 * 729 = 531441 = 3^12.
Wrong choices: D (7.5) treats 9^y as 3^y, giving x + y = 12 and x - y = 3 (trap); A (3) is y; B (4.5) is y in that same
trap system ((12 - 3) / 2); E (9) is x + y."""
from fractions import Fraction as F
def _brute():
    # search rational x, y in steps of 1/2 over -20..20 for exact equality of 3^x * 9^y with 3^12 (compare squares
    # to stay in integers: (3^x * 9^y)^2 = 3^(2x) * 81^y)
    sols = set()
    for a in range(-40, 41):
        for b in range(-40, 41):
            x, y = F(a, 2), F(b, 2)
            if x - y != 3:
                continue
            ex = 2 * x + 4 * y            # exponent of 3 in (3^x * 9^y)^2
            if ex == 24:
                sols.add(x)
    assert len(sols) == 1
    return sols.pop()
ITEM = dict(kind="PS", choices={"A": 3, "B": F(9, 2), "C": 6, "D": F(15, 2), "E": 9}, answer="C", compute=_brute)
