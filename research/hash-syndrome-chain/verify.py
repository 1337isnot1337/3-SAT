#!/usr/bin/env python3
"""Exhaustive small syndrome-chain and cut-rank controls."""
import hashlib
import json
import random
from pathlib import Path


def rank_rows(rows, prime):
    if not rows:
        return 0
    a = [list(r) for r in rows]
    height, width = len(a), len(a[0])
    pivot = 0
    for col in range(width):
        r = next((r for r in range(pivot, height) if a[r][col] % prime), None)
        if r is None:
            continue
        a[pivot], a[r] = a[r], a[pivot]
        inv = pow(a[pivot][col] % prime, -1, prime)
        a[pivot] = [(x*inv) % prime for x in a[pivot]]
        for r in range(pivot+1, height):
            factor = a[r][col] % prime
            if factor:
                a[r] = [(x-factor*y) % prime for x,y in zip(a[r],a[pivot])]
        pivot += 1
        if pivot == height:
            break
    return pivot


def span(vs):
    out = {0}
    for v in vs:
        out |= {x ^ v for x in out}
    return out


def syndrome(vs, bits):
    s = 0
    for j, v in enumerate(vs):
        if bits >> j & 1:
            s ^= v
    return s


def chain(vs, bits):
    futures = [span(vs[i:]) for i in range(len(vs)+1)]
    state = 0
    for i, v in enumerate(vs):
        state ^= v if bits >> i & 1 else 0
        if state not in futures[i+1]:
            return False
    return state == 0


def gf8_mul(a, b):
    out = 0
    while b:
        if b & 1:
            out ^= a
        a <<= 1
        if a & 8:
            a ^= 11  # x^3+x+1
        b >>= 1
    return out


def run():
    inputs = cuts = 0
    for packed in range(8**4):
        cols = [(packed >> (3*j)) & 7 for j in range(4)]
        for mask in range(16):
            assert chain(cols, mask) == (syndrome(cols, mask) == 0)
            inputs += 1
        for cut in range(5):
            left, right = cols[:cut], cols[cut:]
            common = span(left) & span(right)
            table = [[int(syndrome(left, x) == syndrome(right, y))
                      for y in range(1 << len(right))]
                     for x in range(1 << len(left))]
            assert rank_rows(table, 2) == len(common)
            assert rank_rows(table, 3) == len(common)
            cuts += 1
    # Fixed random fixtures include repeated literals, clauses and hash entries.
    rng = random.Random(25137)
    fingerprints = 0
    for _ in range(1000):
        clauses = [[(rng.randrange(3), rng.randrange(2)) for _ in range(3)]
                   for _ in range(4)]
        cols = [rng.randrange(8) for _ in range(4)]
        weights = [rng.randrange(8) for _ in range(3)]
        direct = via_chain = 0
        for x in range(8):
            violations = 0
            for j, clause in enumerate(clauses):
                satisfied = any(((x >> v) & 1) ^ neg for v, neg in clause)
                violations |= (not satisfied) << j
            weight = 1
            for i in range(3):
                if x >> i & 1:
                    weight = gf8_mul(weight, weights[i])
            if syndrome(cols, violations) == 0:
                direct ^= weight
            if chain(cols, violations):
                via_chain ^= weight
        assert direct == via_chain
        fingerprints += 1
    cyclic_fixtures = 0
    for n in range(4, 13):
        for t in range(1, min(n, 4)):
            clauses = {(i, (i+j) % n) for i in range(n) for j in range(1, t+1)}
            assert len(clauses) == n*t
            for i in range(n):
                assert sum(u == i for u,v in clauses) == t
                assert sum(v == i for u,v in clauses) == t
            satisfying = []
            for x in range(1 << n):
                if all(not ((x >> u) & 1) or ((x >> v) & 1) for u,v in clauses):
                    satisfying.append(x)
            assert satisfying == [0, (1 << n)-1]
            cyclic_fixtures += 1
    return {'cyclic_clause_fixtures': cyclic_fixtures, 'matrices_3x4': 4096, 'syndrome_inputs': inputs,
            'cut_ranks_in_each_of_F2_and_F3': cuts,
            'GF8_weighted_clause_fixtures': fingerprints, 'seed': 25137,
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
