#!/usr/bin/env python3
"""Finite controls for matching deficiency and the alternating-path autarky."""
from itertools import product
from random import Random


def matched(clauses):
    owner = {}
    def augment(i, seen):
        for lit in clauses[i]:
            v = abs(lit)
            if v in seen:
                continue
            seen.add(v)
            if v not in owner or augment(owner[v], seen):
                owner[v] = i
                return True
        return False
    for i in range(len(clauses)):
        augment(i, set())
    return owner


def extract(clauses):
    owner = matched(clauses)
    roots = set(range(len(clauses))) - set(owner.values())
    reached_c = set(roots)
    reached_v = set()
    stack = list(roots)
    while stack:
        for lit in clauses[stack.pop()]:
            v = abs(lit)
            if v not in reached_v:
                reached_v.add(v)
                assert v in owner
                i = owner[v]
                if i not in reached_c:
                    reached_c.add(i)
                    stack.append(i)
    assignment = {v: next(x > 0 for x in clauses[i] if abs(x) == v)
                  for v, i in owner.items() if i not in reached_c}
    core = [cl for i, cl in enumerate(clauses) if i in reached_c]
    assert all(abs(x) not in assignment for cl in core for x in cl)
    assert all(any(assignment.get(abs(x)) == (x > 0) for x in cl)
               for i, cl in enumerate(clauses) if i not in reached_c)
    assert len(reached_c)-len(reached_v) == len(roots)
    return core, assignment, len(roots)


def sat(clauses, n):
    return any(all(any(bits[abs(x)-1] == (x > 0) for x in c) for c in clauses)
               for bits in product((False, True), repeat=n))


def brute_deficiency(clauses):
    best = 0
    for mask in range(1 << len(clauses)):
        indices = [i for i in range(len(clauses)) if mask & (1 << i)]
        vertices = {abs(x) for i in indices for x in clauses[i]}
        best = max(best, len(indices) - len(vertices))
    return best


def main():
    rng = Random(20261028)
    for n in range(1, 7):
        for _ in range(200):
            clauses = set()
            for _ in range(rng.randrange(11)):
                vs = rng.sample(range(1, n+1), rng.randrange(min(3,n)+1))
                clauses.add(tuple(sorted((v if rng.randrange(2) else -v for v in vs), key=abs)))
            clauses = sorted(clauses)
            core, _, deficiency = extract(clauses)
            assert sat(clauses, n) == sat(core, n)
            assert deficiency == brute_deficiency(clauses)
    for r in range(1, 21):
        clauses = []
        for j in range(r):
            a, b, c = (3*j+1, 3*j+2, 3*j+3)
            clauses += [(a,b,c), (a,b,-c), (a,-b,c), (-a,b,c), (a,-b,-c)]
        clauses += [(3*j+1, 3*j+4) for j in range(r-1)]
        assert len(clauses) == 6*r-1
        assert all(any(x > 0 for x in cl) for cl in clauses)
        assert all(any(v in cl for cl in clauses) and any(-v in cl for cl in clauses)
                   for v in range(1, 3*r+1))
        assert max(sum(v in {abs(x) for x in cl} for cl in clauses)
                   for v in range(1, 3*r+1)) <= 7
        assert len(clauses) - len(matched(clauses)) == 3*r-1
    before = [(1, 2), (1, -2)]
    after = [(2,), (-2,)]
    assert brute_deficiency(before) == 0 and brute_deficiency(after) == 1
    print('PASS: 1200 seeded formulas; exhaustive deficiency, autarky and decision checks; '
          '20 linear-deficiency controls; branch-increase control')


if __name__ == '__main__':
    main()
