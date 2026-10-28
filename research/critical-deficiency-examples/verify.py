#!/usr/bin/env python3
"""Finite checks of the connected critical-deficiency family."""
from itertools import product


def formula(r):
    assert r >= 3
    result = []
    signs = ((1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1))
    for i in range(r):
        vs = (3*i+1, 3*i+2, 3*i+3)
        result += [tuple(x*s for x,s in zip(vs, sign)) for sign in signs]
        j = (i+1) % r
        result.append((3*i+1, 3*j+1, 3*j+2))
    return result


def deficit(clauses):
    owner = {}
    def aug(i, seen):
        for lit in clauses[i]:
            v = abs(lit)
            if v in seen:
                continue
            seen.add(v)
            if v not in owner or aug(owner[v], seen):
                owner[v] = i
                return True
        return False
    for i in range(len(clauses)):
        aug(i, set())
    return len(clauses)-len(owner)


def restrict(clauses, v, value):
    satisfied = v if value else -v
    return list({tuple(x for x in clause if abs(x) != v)
                 for clause in clauses if satisfied not in clause})


def main():
    for r in (3,4,5):
        n = 3*r
        clauses = formula(r)
        assert len(clauses) == len(set(clauses)) == 5*r
        assert all(len(c) == len({abs(x) for x in c}) == 3 and any(x > 0 for x in c) for c in clauses)
        assert all(sum(v in c for c in clauses) >= 2 and sum(-v in c for c in clauses) >= 2
                   for v in range(1,n+1))
        assert max(sum(any(abs(x)==v for x in c) for c in clauses) for v in range(1,n+1)) == 6
        assert deficit(clauses) == 2*r
        masks = [sum(1 << (abs(x)-1) for x in c) for c in clauses]
        surplus = min(sum(bool(mask & c) for c in masks) - mask.bit_count()
                      for mask in range(1,1 << n))
        assert surplus == 3
        for v,value in product(range(1,n+1),(False,True)):
            assert deficit(restrict(clauses,v,value)) <= 2*r-1
        excess = sum(max(sum(any(abs(x)==v for x in c) for c in clauses)-3, 0) for v in range(1,n+1))
        assert excess == 6*r == 3*deficit(clauses)
        print(f'PASS r={r}: {n} variables, {len(clauses)} clauses, surplus {surplus}, '
              f'deficiency {2*r}, {2*n} restrictions')


if __name__ == '__main__':
    main()
