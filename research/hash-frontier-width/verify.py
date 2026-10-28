#!/usr/bin/env python3
"""Exact controls for a distance/nullity frontier-width inequality."""
import hashlib
import itertools
import json
from pathlib import Path


def rank(vectors):
    pivots = {}
    for v in vectors:
        while v:
            p = v.bit_length() - 1
            if p in pivots:
                v ^= pivots[p]
            else:
                pivots[p] = v
                break
    return len(pivots)


def distance(columns):
    m = len(columns)
    best = m + 1
    for s in range(1, 1 << m):
        total = 0
        for j, col in enumerate(columns):
            if (s >> j) & 1:
                total ^= col
        if total == 0:
            best = min(best, s.bit_count())
    return best


def widths(columns):
    r = rank(columns)
    return [rank(columns[:i]) + rank(columns[i:]) - r
            for i in range(len(columns)+1)]


def run():
    cases = orderings = useful = width_sum_checks = 0
    for packed in range(8**4):
        cols = tuple((packed >> (3*j)) & 7 for j in range(4))
        k = 4-rank(cols)
        d = distance(cols)
        cases += 1
        if d < 2:
            continue
        useful += 1
        q = (4 + d-2) // (d-1)
        for ordered in itertools.permutations(cols):
            ws = widths(ordered)
            assert k <= q * max(ws)
            # Sharper bound: nullity gained in each short block is at most
            # the width immediately before that block.
            start = 0
            total_width = 0
            while start < 4:
                total_width += ws[start]
                start += d-1
            assert k <= total_width
            orderings += 1
            width_sum_checks += 1
    repetitions = []
    for block_length in range(2, 7):
        for blocks in range(1, 5):
            cols = []
            for j in range(blocks):
                basis = [1 << (j*(block_length-1)+i)
                         for i in range(block_length-1)]
                cols.extend(basis + [sum(basis)])
            assert 0 not in cols
            ws = widths(cols)
            assert max(ws) == 1
            assert len(cols)-rank(cols) == blocks
            # Each block is one circuit, and supports are disjoint, so the
            # all-size distance equals block_length; tiny cases also brute force.
            if len(cols) <= 18:
                assert distance(cols) == block_length
            repetitions.append({'block_length': block_length, 'blocks': blocks,
                                'max_width': max(ws), 'kernel_dimension': blocks})
    return {'matrices': cases, 'matrices_with_distance_at_least_2': useful,
            'permutation_checks': orderings, 'block_sum_checks': width_sum_checks,
            'direct_sum_circuit_controls': repetitions,
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
