"""Story 2026-11-25-s1. Top: yesterday's Story answer (2026-11-24-s1, C: 1/2 + 1/3 + 1/6 = 6/6 = 1).
Question: which one is prime? Original, verified in items/2026-11-25-s1.py. Answer D (97)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from story import make_story

ID = "2026-11-25-s1"
if __name__ == "__main__":
    p = make_story(ID, yesterday=("C", "Use sixths: 3/6 + 2/6 + 1/6 = 6/6 = 1. Never add tops and bottoms."),
                   question="Which one is prime?",
                   choices={"A": "51", "B": "91", "C": "57", "D": "97", "E": "87"},
                   out_dir=pathlib.Path(__file__).resolve().parents[1] / "out" / ID)
    print(p, "check: PASS")
