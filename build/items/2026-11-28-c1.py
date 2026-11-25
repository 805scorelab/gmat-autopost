"""In 5 years, Ana will be twice as old as she was 7 years ago. How old is Ana now?
Hand solution: a + 5 = 2(a - 7) = 2a - 14, so a = 19 (D). Check: in 5 years 24; 7 years ago 12; 24 = 2 x 12.
Wrong choices: A (12) solves a + 5 = 2a - 7, doubling only a and not a - 7 (trap; it is also her age 7 years ago);
B (14) is 2 x 7; C (17) is 12 + 5; E (24) is her age in 5 years."""
def _brute():
    ages = [a for a in range(7, 120) if a + 5 == 2 * (a - 7)]
    assert len(ages) == 1
    return ages[0]
ITEM = dict(kind="PS", choices={"A": 12, "B": 14, "C": 17, "D": 19, "E": 24}, answer="D", compute=_brute)
