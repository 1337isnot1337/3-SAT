#!/usr/bin/env python3
"""Exhaustive finite checks of defect-to-deficiency and restriction bounds."""
from itertools import combinations, product
from random import Random


def norm(clauses):
    return sorted({tuple(sorted(set(c), key=lambda x: (abs(x), x))) for c in clauses
                   if not any(-x in c for x in c)})


def defect(clauses, width=3):
    variables = {abs(x) for c in clauses for x in c}
    shortfall = sum(width - len(c) for c in clauses)
    excess = sum(max(0, sum(any(abs(x) == v for x in c) for c in clauses) - width)
                 for v in variables)
    return shortfall + excess


def deficiency(clauses):
    best = 0
    for mask in range(1 << len(clauses)):
        chosen = [c for i, c in enumerate(clauses) if mask & (1 << i)]
        best = max(best, len(chosen) - len({abs(x) for c in chosen for x in c}))
    return best


def restrict(clauses, v, value):
    satisfied = v if value else -v
    return norm(tuple(x for x in c if abs(x) != v)
                for c in clauses if satisfied not in c)


def main():
    rng = Random(103001)
    checks = 0
    for n in range(1, 7):
        for _ in range(200):
            clauses = []
            for _ in range(rng.randrange(11)):
                vs = rng.sample(range(1, n+1), rng.randrange(min(3,n)+1))
                clauses.append(tuple(v if rng.randrange(2) else -v for v in vs))
            clauses = norm(clauses)
            before = defect(clauses)
            assert 3*deficiency(clauses) <= before
            for v in range(1, n+1):
                for value in (False, True):
                    after = restrict(clauses, v, value)
                    assert defect(after) <= before+3
                    checks += 1
    all_signs = [tuple((i+1) if bit else -(i+1) for i, bit in enumerate(bits))
                 for bits in product((False, True), repeat=3)]
    assert defect(all_signs) == 15 and deficiency(all_signs) == 5
    k4 = list(combinations(range(1,5), 2))
    assert defect(k4) == 6 and deficiency(k4) == 2
    tight = [(1,2,3), (1,4,5), (1,6,7)]
    assert defect(tight) == 0 and defect(restrict(tight, 1, False)) == 3
    print(f'PASS: 1200 seeded formulas; {checks} restrictions; '
          'two sharp deficiency controls and one sharp restriction control')


if __name__ == '__main__':
    main()
