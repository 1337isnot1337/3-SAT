#!/usr/bin/env python3
"""Exact finite controls for the row-basis support construction."""
import hashlib
import itertools
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent

def rank(rows):
    pivots = {}
    for x in rows:
        while x:
            p = x.bit_length() - 1
            if p in pivots:
                x ^= pivots[p]
            else:
                pivots[p] = x
                break
    return len(pivots)

def edges(n, length):
    return [{(1 << i) | (1 << ((i + j) % n))
             for j in range(1, length + 1)} for i in range(n)]

def projector_coefficient(edge_set, mask):
    # Boolean Mobius inversion, independently of the support argument.
    ans = 0
    sub = mask
    while True:
        parity = sum((sub & e) == e for e in edge_set) % 2
        ans += (-1 if (mask.bit_count() - sub.bit_count()) % 2 else 1) * (1 - parity)
        if sub == 0:
            return ans
        sub = (sub - 1) & mask

def main():
    checks = {"systems": 0, "nonzero_row_combinations": 0,
              "mobius_edge_coefficients": 0, "exhaustive_invertible_4x4": 0,
              "sampled_invertible_bases": 0, "negative_controls": 0}
    rng = random.Random(20261027)
    for n in range(3, 10):
        length = min(n.bit_length() - 1, (n - 1) // 2)
        rows = edges(n, length)
        assert all(len(row) == length for row in rows)
        assert len(set.union(*rows)) == n * length
        scopes = [set(v for e in row for v in range(n) if e & (1 << v)) for row in rows]
        assert all(len(s) == length + 1 for s in scopes)
        assert all(sum(v in s for s in scopes) == length + 1 for v in range(n))
        for selection in range(1, 1 << n):
            combined = set().union(*(rows[i] for i in range(n) if selection >> i & 1))
            assert len(combined) == length * selection.bit_count()
            for edge in combined:
                assert projector_coefficient(combined, edge) == -1
                checks["mobius_edge_coefficients"] += 1
            checks["nonzero_row_combinations"] += 1
        checks["systems"] += 1
        for _ in range(100):
            basis = [1 << i for i in range(n)]
            for _ in range(6 * n):
                i, j = rng.sample(range(n), 2)
                basis[i] ^= basis[j]
            assert rank(basis) == n
            product = 1
            for row in basis:
                product *= length * row.bit_count()
            assert product >= length ** n
            checks["sampled_invertible_bases"] += 1
    for basis in itertools.product(range(16), repeat=4):
        if rank(basis) == 4:
            assert all(basis)
            checks["exhaustive_invertible_4x4"] += 1
    assert checks["exhaustive_invertible_4x4"] == 20160
    # Duplicate monomials cancel over F2: a private support hypothesis is essential.
    a = {(1 << 0) | (1 << 1)}
    assert not (a ^ a)
    assert projector_coefficient(a ^ a, 3) == 0
    checks["negative_controls"] += 1
    result = {"scope": "bounded exact checks only; no independent proof review",
              "checks": checks,
              "sha256": {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
                         for name in ("PROOF.md", "verify.py")}}
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
