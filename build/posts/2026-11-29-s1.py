"""Story 2026-11-29-s1. Top: yesterday's Story answer (2026-11-28-s1, D: 0.75 = 3/4, so 3 / x = 3/4 and x = 4).
Question: 15% of 80 = ? Original, verified in items/2026-11-29-s1.py. Answer C (12)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from story import make_story

ID = "2026-11-29-s1"
if __name__ == "__main__":
    p = make_story(ID, yesterday=("D", "0.75 is 3/4, so 3 ÷ x = 3/4 and x = 4."),
                   question="15% of 80 = ?",
                   choices={"A": "8", "B": "10", "C": "12", "D": "15", "E": "68"},
                   out_dir=pathlib.Path(__file__).resolve().parents[1] / "out" / ID)
    print(p, "check: PASS")
