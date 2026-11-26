"""Bus A leaves the station every 12 minutes and bus B every 18 minutes. Both leave together at 8:00 a.m. How many
times do they leave together from 8:00 a.m. to 11:00 a.m., counting both 8:00 and 11:00?
Hand solution: they meet every LCM(12, 18) = 36 minutes. 180 / 36 = 5 gaps, so 5 + 1 = 6 departures together:
8:00, 8:36, 9:12, 9:48, 10:24, 11:00 (C).
Wrong choices: B (5) counts gaps, not departures, and forgets 8:00 (trap); A (4) counts only the times strictly
between 8:00 and 11:00; D (10) is 180 / 18; E (15) is 180 / 12."""
def _brute():
    a = {t for t in range(0, 181) if t % 12 == 0}
    b = {t for t in range(0, 181) if t % 18 == 0}
    return len(a & b)
ITEM = dict(kind="PS", choices={"A": 4, "B": 5, "C": 6, "D": 10, "E": 15}, answer="C", compute=_brute)
