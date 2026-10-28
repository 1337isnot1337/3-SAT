#!/usr/bin/env python3
"""Check the clause-variable matching certificate and a short-clause control."""
from itertools import product
from random import Random


def matching(clauses):
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

    if not all(augment(i, set()) for i in range(len(clauses))):
        return None
    return {v: next(lit > 0 for lit in clauses[i] if abs(lit) == v) for v, i in owner.items()}


def main():
    rng = Random(103008)
    count = 0
    for n in range(3, 15):
        for _ in range(100):
            remaining = {v: 3 for v in range(1, n+1)}
            clauses = []
            for _ in range(3*n):
                available = [v for v in remaining if remaining[v]]
                if len(available) < 3:
                    break
                chosen = rng.sample(available, 3)
                clauses.append(tuple(v if rng.randrange(2) else -v for v in chosen))
                for v in chosen:
                    remaining[v] -= 1
            witness = matching(clauses)
            assert witness is not None
            assert all(any(witness.get(abs(lit)) == (lit > 0) for lit in clause) for clause in clauses)
            count += 1
    unsat = [(1, 3), (1, -3), (-2, 4), (-2, -4), (-1, 2)]
    assert max(sum(v in {abs(x) for x in cl} for cl in unsat) for v in range(1, 5)) == 3
    assert all(any(v in cl for cl in unsat) and any(-v in cl for cl in unsat) for v in range(1, 5))
    assert not any(all(any(bits[abs(lit)-1] == (lit > 0) for lit in clause) for clause in unsat)
                   for bits in product((False, True), repeat=4))
    print(f'PASS: {count} seeded width-three matching witnesses; short-clause unsatisfiable control')


if __name__ == '__main__':
    main()
