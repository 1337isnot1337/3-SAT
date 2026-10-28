#!/usr/bin/env python3
"""Construct and verify the binary independence-table rank witness."""
import hashlib
import json
import random
from pathlib import Path


def rank(vectors):
    pivots = {}
    for v in vectors:
        while v:
            p = v.bit_length()-1
            if p not in pivots:
                pivots[p] = v
                break
            v ^= pivots[p]
    return len(pivots)


def span(vectors):
    out = {0}
    for v in vectors:
        out |= {x ^ v for x in out}
    return out


def extend(seed, candidates):
    basis = list(seed)
    added = []
    for v in candidates:
        if rank(basis + [v]) > len(basis):
            basis.append(v)
            added.append(v)
    return added


def witness(cols, cut):
    left, right = cols[:cut], cols[cut:]
    intersection = span(left) & span(right)
    e_basis = extend([], sorted(intersection))
    b = len(e_basis)
    assert b == rank(left) + rank(right) - rank(cols)
    # A and B project to bases of the two spaces modulo their intersection.
    a = extend(e_basis, left)
    c = extend(e_basis, right)
    assert rank(a+c) == len(a)+len(c)
    assert rank(a+c+e_basis) == len(a)+len(c)+b
    i = extend(a, left)
    j = extend(c, right)
    assert len(i) == len(j) == b
    fixed = a+c
    rows = []
    for s in range(1 << b):
        ls = fixed + [v for h, v in enumerate(i) if s >> h & 1]
        row = 0
        for t in range(1 << b):
            selection = ls + [v for h, v in enumerate(j) if t >> h & 1]
            if rank(selection) == len(selection):
                row |= 1 << t
        rows.append(row)
    assert rank(rows) == 1 << b
    return b


def run():
    histogram = {}
    cuts = 0
    for packed in range(8**4):
        cols = [(packed >> (3*j)) & 7 for j in range(4)]
        for cut in range(5):
            b = witness(cols, cut)
            histogram[str(b)] = histogram.get(str(b), 0)+1
            cuts += 1
    random_cuts = 0
    rng = random.Random(3725)
    for _ in range(1000):
        cols = [rng.randrange(16) for _ in range(8)]
        for cut in range(9):
            witness(cols, cut)
            random_cuts += 1
    return {'exhaustive_matrices_3x4': 8**4,
            'exhaustive_cut_witnesses': cuts,
            'exhaustive_width_histogram': histogram,
            'seeded_matrices_4x8': 1000, 'seeded_cut_witnesses': random_cuts,
            'seed': 3725,
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
