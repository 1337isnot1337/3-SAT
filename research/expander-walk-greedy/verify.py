#!/usr/bin/env python3
"""Exact finite controls for walk avoidance and parity, standard library only."""
from fractions import Fraction
from itertools import product
from math import ceil

GRAPHS = {1: (0,), 2: (0, 1), 4: (0, 1, 2, 3), 8: (0, 1, 2, 4)}
checks = paths = 0
for q, shifts in GRAPHS.items():
    d = len(shifts)
    for b in range(1, q):
        assert abs(sum((-1)**((b & s).bit_count() % 2) for s in shifts)) * 2 <= d
    for m in range(1, q + 1):
        if q > 1 and q // 2 >= m:
            continue  # q must be the least power of two >= m
        for p in range(1, 9):
            for mask in range(1, 1 << m):
                if mask.bit_count() * p < m:
                    continue
                # Exact count of avoiding walks, including starting-vertex multiplicity.
                a = [int(not (mask >> v & 1)) for v in range(q)]
                for _ in range(p - 1):
                    a = [sum(a[v ^ s] for s in shifts) * int(not (mask >> v & 1)) for v in range(q)]
                avoid = Fraction(sum(a), q * d ** (p - 1))
                rejection = (1 - avoid) / 2
                assert rejection >= Fraction(1, 20), (q, m, p, mask, rejection)
                if q <= 4 and p <= 4:
                    rejected = total = 0
                    for start in range(q):
                        for steps in product(shifts, repeat=p - 1):
                            v = start
                            walk = [v]
                            for step in steps:
                                v ^= step
                                walk.append(v)
                            for coeffs in product((0, 1), repeat=p):
                                parity = sum(c for v, c in zip(walk, coeffs) if mask >> v & 1) % 2
                                rejected += parity
                                total += 1
                    assert Fraction(rejected, total) == rejection
                    paths += total
                checks += 1
assert 2 * Fraction(19, 20) ** 14 < 1
print(f'PASS: {checks} exact support/walk checks; {paths} direct coefficient-list checks; 14-round contraction')
