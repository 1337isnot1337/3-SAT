#!/usr/bin/env python3
"""Exact finite controls for the shared binary-matroid frontier construction."""
import hashlib
import json
from pathlib import Path


def span(vectors):
    out = {0}
    for v in vectors:
        out |= {x ^ v for x in out}
    return frozenset(out)


def binary_rank(rows):
    pivots = {}
    for x in rows:
        while x:
            p = x.bit_length() - 1
            if p not in pivots:
                pivots[p] = x
                break
            x ^= pivots[p]
    return len(pivots)


def all_subspaces(b):
    spaces = {frozenset({0})}
    frontier = list(spaces)
    while frontier:
        s = frontier.pop()
        for v in range(1 << b):
            if v not in s:
                t = s | frozenset(x ^ v for x in s)
                if t not in spaces:
                    spaces.add(t)
                    frontier.append(t)
    return spaces


def run():
    matrices = selections = transitions = identities = 0
    for encoded in range(8 ** 4):
        cols = [(encoded >> (3*j)) & 7 for j in range(4)]
        futures = [span(cols[i:]) for i in range(5)]
        for mask in range(16):
            selected = [cols[j] for j in range(4) if mask >> j & 1]
            independent = binary_rank(selected) == len(selected)
            state = frozenset({0})
            prefix = []
            alive = True
            for j, v in enumerate(cols):
                if not alive:
                    break
                assert state == span(prefix) & futures[j]
                take = (mask >> j) & 1
                if take and v in state:
                    alive = False
                else:
                    if take:
                        state = state | frozenset(x ^ v for x in state)
                        prefix.append(v)
                    state = state & futures[j+1]
                    assert state == span(prefix) & futures[j+1]
                transitions += 1
            assert alive == independent
            selections += 1
        # Coefficients of the kernel indicator are exactly independent sets.
        for x in range(16):
            syndrome = 0
            for j, v in enumerate(cols):
                if x >> j & 1:
                    syndrome ^= v
            value = 0
            s = x
            while True:
                chosen = [cols[j] for j in range(4) if s >> j & 1]
                value ^= binary_rank(chosen) == len(chosen)
                if s == 0:
                    break
                s = (s-1) & x
            assert value == (syndrome == 0)
            identities += 1
        matrices += 1
    counts = [len(all_subspaces(b)) for b in range(5)]
    assert counts == [1, 2, 5, 16, 67]
    paired = []
    for b in range(9):
        n = 1 << b
        rows = [sum((not (s & t)) << t for t in range(n)) for s in range(n)]
        rank = binary_rank(rows)
        assert rank == n
        paired.append({'width': b, 'cut_rank': rank})
    return {'matrices': matrices, 'selected_subsets': selections,
            'live_transitions': transitions, 'kernel_identity_evaluations': identities,
            'subspace_counts_dimensions_0_to_4': counts,
            'paired_cut_ranks': paired,
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
