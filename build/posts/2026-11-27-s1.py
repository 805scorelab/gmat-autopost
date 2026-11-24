"""Story 2026-11-27-s1. Top: yesterday's Story answer (2026-11-26-s1, E: 4/5 is only 1/5 short of 1, the smallest gap).
Question: 0.2 x 0.3 = ? Original, verified in items/2026-11-27-s1.py. Answer B (0.06)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from story import make_story

ID = "2026-11-27-s1"
if __name__ == "__main__":
    p = make_story(ID, yesterday=("E", "Check the gap to 1: 4/5 is only 1/5 short, the smallest gap."),
                   question="0.2 × 0.3 = ?",
                   choices={"A": "0.6", "B": "0.06", "C": "0.006", "D": "6", "E": "0.5"},
                   out_dir=pathlib.Path(__file__).resolve().parents[1] / "out" / ID)
    print(p, "check: PASS")
