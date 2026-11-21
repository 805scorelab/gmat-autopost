"""Solve every Quant and Data Insights item in code. An item ships only if this returns no problems.

An item is a Python module in build/items/ that defines ITEM (a dict). Two kinds:

Problem Solving ("PS")
    ITEM = dict(kind="PS", choices={"A": 0, "B": 2, ...}, answer="B", compute=<function returning the true value>)
    The hand solution lives in the module docstring. compute() must be an independent method (brute force where
    possible). Checks: the computed value equals the keyed choice, and every other choice differs from it.

Data Sufficiency ("DS")
    ITEM = dict(kind="DS", answer="C", worlds=<function yielding candidate cases>, target=<case -> answer of the
                question>, s1=<case -> bool>, s2=<case -> bool>)
    A statement is sufficient when every case consistent with it gives the same target value. The answer letter is
    derived (A: 1 alone; B: 2 alone; C: together only; D: each alone; E: not even together) and must equal the key.
    The cases that settle each verdict are reported, so counterexamples can go on the slides.

Usage:  python3 build/verify_math.py build/items/<id>.py [...]   (exit 1 on any problem)
"""

import importlib.util
import math
import sys
from fractions import Fraction

DS_KEY = {
    "A": "Statement (1) ALONE is sufficient, but statement (2) alone is not sufficient.",
    "B": "Statement (2) ALONE is sufficient, but statement (1) alone is not sufficient.",
    "C": "BOTH statements TOGETHER are sufficient, but NEITHER statement ALONE is sufficient.",
    "D": "EACH statement ALONE is sufficient.",
    "E": "Statements (1) and (2) TOGETHER are NOT sufficient.",
}


def same(a, b):
    if isinstance(a, float) or isinstance(b, float):
        return math.isclose(float(a), float(b), rel_tol=1e-9, abs_tol=1e-12)
    return Fraction(a) == Fraction(b) if all(isinstance(x, (int, Fraction)) for x in (a, b)) else a == b


def check_ps(item):
    problems = []
    truth = item["compute"]()
    choices, key = item["choices"], item["answer"]
    if len(choices) != 5 or sorted(choices) != list("ABCDE"):
        problems.append("PS needs exactly five choices A to E")
    if not same(choices[key], truth):
        problems.append(f"keyed {key}={choices[key]!r} but computed {truth!r}")
    for letter, value in choices.items():
        if letter != key and same(value, truth):
            problems.append(f"choice {letter} also equals the answer {truth!r}")
    values = list(choices.values())
    if len({str(v) for v in values}) != len(values):
        problems.append("duplicate choices")
    return problems, {"computed": truth}


def sufficiency(cases, target):
    answers = {}
    for case in cases:
        answers.setdefault(repr(target(case)), case)
    return len(answers) == 1 and bool(answers), answers


def check_ds(item):
    cases = list(item["worlds"]())
    target, s1, s2 = item["target"], item["s1"], item["s2"]
    c1 = [c for c in cases if s1(c)]
    c2 = [c for c in cases if s2(c)]
    c12 = [c for c in cases if s1(c) and s2(c)]
    problems = []
    if not c12:
        problems.append("the two statements contradict each other on this domain")
    suf1, w1 = sufficiency(c1, target)
    suf2, w2 = sufficiency(c2, target)
    suf12, w12 = sufficiency(c12, target)
    derived = ("D" if suf1 and suf2 else "A" if suf1 else "B" if suf2 else "C" if suf12 else "E")
    if derived != item["answer"]:
        problems.append(f"keyed {item['answer']} but derived {derived}")
    evidence = {"(1)": w1, "(2)": w2, "(1)+(2)": w12, "derived": derived}
    return problems, evidence


def verify(path):
    spec = importlib.util.spec_from_file_location("item", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    item = module.ITEM
    if not (module.__doc__ or "").strip():
        return ["no hand solution in the module docstring"], {}
    return {"PS": check_ps, "DS": check_ds}[item["kind"]](item)


if __name__ == "__main__":
    bad = 0
    for path in sys.argv[1:]:
        problems, evidence = verify(path)
        status = "PASS" if not problems else "FAIL"
        bad += bool(problems)
        print(f"{status} {path}")
        for p in problems:
            print(f"   - {p}")
        for k, v in evidence.items():
            if isinstance(v, dict):
                print(f"   {k}: " + ", ".join(f"{ans} e.g. {case}" for ans, case in list(v.items())[:3]))
            else:
                print(f"   {k}: {v}")
    sys.exit(1 if bad else 0)
