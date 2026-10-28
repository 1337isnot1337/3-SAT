#!/usr/bin/env python3
"""Check independent-set / kernel weight-enumerator identity over GF(8)."""
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


def mul(a, b):
    out = 0
    while b:
        if b & 1:
            out ^= a
        a <<= 1
        if a & 8:
            a ^= 11
        b >>= 1
    return out


def carryless_mul(a, b):
    out = 0
    while b:
        if b & 1:
            out ^= a
        a <<= 1
        b >>= 1
    return out


def reduce_gf8(a):
    while a.bit_length() > 3:
        a ^= 11 << (a.bit_length()-4)
    return a


def row_gate_paths(cols, row, mask):
    # Sum local ternary XOR tensors over every accumulator state.
    paths = [1, 0]
    for j, col in enumerate(cols):
        if col >> row & 1:
            x = (mask >> j) & 1
            next_paths = [0, 0]
            for old in range(2):
                for new in range(2):
                    next_paths[new] += paths[old] * int(new == (old ^ x))
            paths = next_paths
    return paths[0]


def evaluate(cols, weights):
    independent = kernel = lifted = 0
    m = len(cols)
    for mask in range(1 << m):
        chosen = [v for i,v in enumerate(cols) if mask >> i & 1]
        if rank(chosen) == len(chosen):
            term = 1
            for i,z in enumerate(weights):
                if mask >> i & 1:
                    term = mul(term,z)
            independent ^= term
        syndrome = 0
        for v in chosen:
            syndrome ^= v
        if syndrome == 0:
            groups = []
            for indices in (range(0, m//2), range(m//2,m)):
                term = 1
                for i in indices:
                    term = mul(term, weights[i] if mask >> i & 1 else 1 ^ weights[i])
                groups.append(term)
            kernel ^= mul(*groups)
            lifted ^= carryless_mul(*groups)
    assert independent == kernel == reduce_gf8(lifted)
    assert lifted.bit_length() <= 5


def run():
    exhaustive = gate_cases = 0
    for packed in range(8**4):
        cols = [(packed >> (3*j)) & 7 for j in range(4)]
        for mask in range(16):
            paths = 1
            for row in range(3):
                paths *= row_gate_paths(cols, row, mask)
            syndrome = 0
            for j, col in enumerate(cols):
                if mask >> j & 1:
                    syndrome ^= col
            assert paths == int(syndrome == 0)
            gate_cases += 1
            weights = [(mask >> j) & 1 for j in range(4)]
            evaluate(cols, weights)
            exhaustive += 1
    rng = random.Random(25104)
    for _ in range(2000):
        cols = [rng.randrange(8) for _ in range(6)]
        weights = [rng.randrange(8) for _ in range(6)]
        evaluate(cols, weights)
    # The pair family [I_b|I_b] has a triangular width profile of area b^2.
    controls = []
    for b in range(1, 33):
        widths = list(range(b+1)) + list(range(b-1,-1,-1))
        assert sum(widths) == b*b
        controls.append({'b': b, 'columns': 2*b, 'ones': 2*b,
                         'ordered_width_sum': sum(widths)})
    return {'matrices_3x4': 4096, 'boolean_weight_cases': exhaustive,
            'explicit_xor_gate_cases': gate_cases,
            'GF8_weighted_and_group_lift_cases': 2000, 'seed': 25104,
            'paired_order_controls': controls,
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
