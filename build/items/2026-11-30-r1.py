"""How many integers from 1 to 100, inclusive, are multiples of 3 or 5 (or both)?
Hand solution: multiples of 3: 33; multiples of 5: 20; multiples of both (of 15): 6. 33 + 20 - 6 = 47 (B).
Wrong choices: C (53) adds 33 + 20 and forgets the 6 counted twice (trap); A (41) subtracts the overlap twice;
D (59) adds the overlap instead of subtracting it; E (67) is 100 - 33, the numbers that are not multiples of 3.
Note: 53 is also the count of multiples of neither (100 - 47); the question asks for "3 or 5", so C is wrong."""
def _brute():
    return sum(1 for n in range(1, 101) if n % 3 == 0 or n % 5 == 0)
ITEM = dict(kind="PS", choices={"A": 41, "B": 47, "C": 53, "D": 59, "E": 67}, answer="B", compute=_brute)
