"""Story 2026-11-30-s1. Top: yesterday's Story answer (2026-11-29-s1, C: 10% of 80 is 8, 5% is 4, so 15% is 12).
Question: 2^10 = ? Original, verified in items/2026-11-30-s1.py. Answer D (1024)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from story import make_story

ID = "2026-11-30-s1"
if __name__ == "__main__":
    p = make_story(ID, yesterday=("C", "10% of 80 is 8 and 5% is 4, so 15% is 8 + 4 = 12."),
                   question="2<sup>10</sup> = ?",
                   choices={"A": "20", "B": "512", "C": "1,000", "D": "1,024", "E": "2,048"},
                   out_dir=pathlib.Path(__file__).resolve().parents[1] / "out" / ID)
    print(p, "check: PASS")
