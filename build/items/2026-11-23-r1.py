"""Drive 120 miles at 60 mph, return the same 120 miles at 40 mph. Average speed for the round trip?
Hand solution: out 120/60 = 2 h, back 120/40 = 3 h. Total 240 miles in 5 h = 48 mph (B).
Shortcut: equal distances, average speed = 2ab/(a + b) = 2 x 60 x 40 / 100 = 48.
Trap: C (50), averaging the two speeds; you spend longer at the slower speed."""
from fractions import Fraction as F
def _avg():
    # simulate minute by minute: distance covered over total time
    d, t = F(0), F(0)
    for speed, dist in ((60, 120), (40, 120)):
        step = F(speed, 60)                       # miles per minute
        covered = F(0)
        while covered < dist:
            covered += step
            t += F(1, 60)
        d += covered
    return d / t
ITEM = dict(kind="PS", choices={"A": 45, "B": 48, "C": 50, "D": 52, "E": 55}, answer="B", compute=_avg)
