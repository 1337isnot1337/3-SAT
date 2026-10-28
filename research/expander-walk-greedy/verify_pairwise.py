#!/usr/bin/env python3
"""Exact pairwise index/coefficients controls, finite domains only."""
from fractions import Fraction
from itertools import product
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('bias', Path(__file__).with_name('verify_bias.py'))
bias = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bias)
checks = lists = pairs = 0
for q in (1, 2, 4):
    for p in range(1, 6):
        r = max(1, (max(q, p) - 1).bit_length())
        H = 1 << r
        mod = bias.modulus(r)
        _, strings = bias.family(p)
        sequences = [[(bias.multiply(a, j, mod, r) ^ b) & (q - 1)
                      for j in range(p)] for a, b in product(range(H), repeat=2)]
        for j in range(p):
            assert all(sum(v[j] == x for v in sequences) * q == H*H for x in range(q))
            for k in range(j):
                assert all(sum(v[j] == x and v[k] == y for v in sequences) * q*q == H*H
                           for x in range(q) for y in range(q))
                pairs += 1
        for m in range(1 if q == 1 else q//2+1, q+1):
            for support in range(1, 1 << m):
                if support.bit_count() * p < m:
                    continue
                rejected = total = 0
                for v in sequences:
                    hit = sum(1 << j for j, u in enumerate(v) if support >> u & 1)
                    for c in strings:
                        rejected += (hit & c).bit_count() % 2
                        total += 1
                assert 12*rejected >= total, (q,p,m,support,rejected,total)
                checks += 1
                lists += total
assert 2 * Fraction(11, 12) ** 8 < 1
print(f'PASS: {pairs} exact index-pair marginals; {checks} support cases; {lists} candidate lists; 8-round contraction')
