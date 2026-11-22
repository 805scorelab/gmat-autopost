"""Boys to girls is 3 : 5. After 6 boys join, boys to girls is 3 : 4. How many girls?
Hand solution: boys 3k, girls 5k. (3k + 6) / 5k = 3/4, so 12k + 24 = 15k, k = 8. Girls 5 x 8 = 40 (D).
Check: 24 boys, 40 girls; 30 boys : 40 girls = 3 : 4.
Trap: A (24), the number of boys at the start. B (30) is the boys after 6 join. C (32) is 4 x 8, the girls' new ratio
part times k. E (48) is 6 x 8."""
ITEM = dict(kind="PS", choices={"A": 24, "B": 30, "C": 32, "D": 40, "E": 48}, answer="D",
            compute=lambda: [g for g in range(1, 2000) for b in range(1, 2000)
                             if 5 * b == 3 * g and 4 * (b + 6) == 3 * g][0])
