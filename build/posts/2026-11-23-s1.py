"""Story 2026-11-23-s1. Top: yesterday's Story answer (2026-11-22-s1, D: 6x = 30). Question: which is largest?
Original, verified in items/2026-11-23-s1.py. Answer E (4^3 = 64)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from story import make_story

ID = "2026-11-23-s1"
if __name__ == "__main__":
    p = make_story(ID, yesterday=("D", "3x = 15, so 6x = 2 × 15 = 30. No need to find x."),
                   question="Which is the largest?",
                   choices={"A": "2<sup>5</sup>", "B": "3<sup>3</sup>", "C": "5<sup>2</sup>", "D": "6<sup>2</sup>",
                            "E": "4<sup>3</sup>"},
                   out_dir=pathlib.Path(__file__).resolve().parents[1] / "out" / ID)
    print(p, "check: PASS")
