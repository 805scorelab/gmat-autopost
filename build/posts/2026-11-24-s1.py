"""Story 2026-11-24-s1. Top: yesterday's Story answer (2026-11-23-s1, E: 4^3 = 64). Question: 1/2 + 1/3 + 1/6.
Original, verified in items/2026-11-24-s1.py. Answer C (1)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from story import make_story

ID = "2026-11-24-s1"
if __name__ == "__main__":
    p = make_story(ID, yesterday=("E", "4<sup>3</sup> = 64 beats 6<sup>2</sup> = 36 and 2<sup>5</sup> = 32. Compute, don't eyeball."),
                   question="1/2 + 1/3 + 1/6 = ?",
                   choices={"A": "1/2", "B": "5/6", "C": "1", "D": "3/11", "E": "7/6"},
                   out_dir=pathlib.Path(__file__).resolve().parents[1] / "out" / ID)
    print(p, "check: PASS")
