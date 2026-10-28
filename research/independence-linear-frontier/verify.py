#!/usr/bin/env python3
"""Exact checks of characteristic-two span-membership transitions."""
import hashlib
import json
import random
from pathlib import Path


def rank(xs):
    pivots = {}
    for x in xs:
        while x:
            p = x.bit_length()-1
            if p not in pivots:
                pivots[p] = x
                break
            x ^= pivots[p]
    return len(pivots)


def span(xs):
    out = {0}
    for x in xs:
        out |= {u ^ x for u in out}
    return out


def rank_mod3(rows):
    a = [list(r) for r in rows]
    p = 0
    for c in range(len(a[0])):
        pivot = next((j for j in range(p, len(a)) if a[j][c] % 3), None)
        if pivot is None:
            continue
        a[p], a[pivot] = a[pivot], a[p]
        mult = pow(a[p][c] % 3, -1, 3)
        a[p] = [v*mult % 3 for v in a[p]]
        for j in range(p+1, len(a)):
            mult = a[j][c]
            a[j] = [(x-mult*y) % 3 for x,y in zip(a[j],a[p])]
        p += 1
        if p == len(a):
            break
    return p


def table(cols, cut):
    rows = []
    left, right = cols[:cut], cols[cut:]
    for s in range(1 << cut):
        selected_l = [v for j,v in enumerate(left) if s >> j & 1]
        row = []
        for t in range(1 << len(right)):
            selected = selected_l + [v for j,v in enumerate(right) if t >> j & 1]
            row.append(int(rank(selected) == len(selected)))
        rows.append(row)
    return rows


def gf8_mul(a, b):
    out = 0
    while b:
        if b & 1:
            out ^= a
        a <<= 1
        if a & 8:
            a ^= 11
        b >>= 1
    return out


def run():
    transition_checks = cut_checks = inputs = 0
    for packed in range(8**4):
        cols = [(packed >> (3*j)) & 7 for j in range(4)]
        prefixes = [span(cols[:i]) for i in range(5)]
        futures = [span(cols[i:]) for i in range(5)]
        frontiers = [prefixes[i] & futures[i] for i in range(5)]
        for mask in range(16):
            states = {0: 1}
            selected = []
            for i, v in enumerate(cols):
                take = (mask >> i) & 1
                new = {}
                for u in frontiers[i+1]:
                    # Terms outside E_i have amplitude zero.
                    value = states.get(u, 0)
                    if take:
                        value ^= states.get(u ^ v, 0)
                    new[u] = value
                if take:
                    selected.append(v)
                selected_span = span(selected)
                independent = rank(selected) == len(selected)
                for u in frontiers[i+1]:
                    assert new[u] == (independent and u in selected_span)
                    transition_checks += 1
                states = new
            assert states[0] == (rank(selected) == len(selected))
            inputs += 1
        for cut in range(5):
            rows = table(cols, cut)
            bitrows = [sum(v << j for j,v in enumerate(row)) for row in rows]
            assert rank(bitrows) == len(frontiers[cut])
            cut_checks += 1
    # All nonzero vectors of F2^2 on both sides: rank differs by field.
    witness = [1,2,3,1,2,3]
    rows = table(witness, 3)
    bitrows = [sum(v << j for j,v in enumerate(row)) for row in rows]
    assert rank(bitrows) == 4
    assert rank_mod3(rows) == 5
    # Zero column: two identical transitions cancel when selection is 1.
    assert (int(0 == 0) ^ int(0 == 0)) == 0
    rng = random.Random(25174)
    weighted_controls = 0
    for _ in range(200):
        cols = [rng.randrange(8) for _ in range(6)]
        weights = [rng.randrange(8) for _ in cols]
        states = {0: 1}
        for i, v in enumerate(cols):
            frontier = span(cols[:i+1]) & span(cols[i+1:])
            states = {u: states.get(u, 0) ^ gf8_mul(weights[i],
                      states.get(u, 0) ^ states.get(u ^ v, 0))
                      for u in frontier}
        direct = 0
        for mask in range(1 << len(cols)):
            chosen = [v for i,v in enumerate(cols) if mask >> i & 1]
            if rank(chosen) == len(chosen):
                term = 1
                for i, w in enumerate(weights):
                    if mask >> i & 1:
                        term = gf8_mul(term, w)
                direct ^= term
        assert states[0] == direct
        weighted_controls += 1
    return {'GF8_weighted_polynomial_controls': weighted_controls,
            'weighted_seed': 25174, 'matrices_3x4': 4096, 'selected_subsets': inputs,
            'state_entry_checks': transition_checks, 'cut_rank_checks_F2': cut_checks,
            'F2_F3_witness_ranks': [4,5],
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
