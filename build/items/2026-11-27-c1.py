"""Of 50 students in a class, 28 take French, 20 take Spanish and 9 take both. How many take neither?
Hand solution: at least one = 28 + 20 - 9 = 39. Neither = 50 - 39 = 11 (C).
Wrong choices: A (2) is 50 - 48, forgetting the 9 counted twice (trap); B (9) is the both group; D (19) is French
only; E (39) is the number taking at least one."""
def _brute():
    # independent check: build the class student by student and count who is in neither set
    students = [("F", "S")] * 9 + [("F",)] * (28 - 9) + [("S",)] * (20 - 9)
    students += [()] * (50 - len(students))
    assert sum("F" in s for s in students) == 28 and sum("S" in s for s in students) == 20
    return sum(1 for s in students if not s)
ITEM = dict(kind="PS", choices={"A": 2, "B": 9, "C": 11, "D": 19, "E": 39}, answer="C", compute=_brute)
