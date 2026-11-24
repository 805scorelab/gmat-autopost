"""Story 2026-11-26-s1. Top: yesterday's Story answer (2026-11-25-s1, D: 97 is prime; 91 = 7 x 13).
Question: which fraction is the greatest? Original, verified in items/2026-11-26-s1.py. Answer E (4/5)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from story import make_story

ID = "2026-11-26-s1"
if __name__ == "__main__":
    p = make_story(ID, yesterday=("D", "97 has no factor up to 9. Trap: 91 = 7 × 13."),
                   question="Which fraction is the greatest?",
                   choices={"A": "3/4", "B": "5/7", "C": "2/3", "D": "7/10", "E": "4/5"},
                   out_dir=pathlib.Path(__file__).resolve().parents[1] / "out" / ID)
    print(p, "check: PASS")
