"""Story 2026-11-28-s1. Top: yesterday's Story answer (2026-11-27-s1, B: 2 x 3 = 6 with 2 decimal places, 0.06).
Question: 3/x = 0.75, x = ? Original, verified in items/2026-11-28-s1.py. Answer D (4)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from story import make_story

ID = "2026-11-28-s1"
if __name__ == "__main__":
    p = make_story(ID, yesterday=("B", "2 × 3 = 6, and the factors carry 2 decimal places: 0.06."),
                   question="3 ÷ x = 0.75<br>x = ?",
                   choices={"A": "2.25", "B": "0.25", "C": "3.75", "D": "4", "E": "4.5"},
                   out_dir=pathlib.Path(__file__).resolve().parents[1] / "out" / ID)
    print(p, "check: PASS")
