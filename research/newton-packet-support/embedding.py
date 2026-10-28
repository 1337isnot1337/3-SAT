#!/usr/bin/env python3
"""Small exact slot-packing control for the explicitly specified embedding."""
from collections import Counter
from itertools import product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def main():
    # Toy r=2, a=3 is a packing control, not the source's r=64 schedule.
    r, a, K = 2, 3, 3
    L = 2**a
    B = L
    packets = []
    special_pairs = ((0, 1), (0, 0), (0, 0))
    for pairs in product(((0, 0), (0, 1), (1, 1)), repeat=a):
        a_unequal = sum(x != y for x, y in pairs)
        count = B*2**a_unequal//L
        for packet_no in range(count):
            slots = []
            for x in range(L):
                row, col = [], []
                for i, (lo, hi) in enumerate(pairs):
                    if lo == hi:
                        row.append(lo)
                        col.append(lo)
                    elif (x >> i) & 1:
                        row.append(hi)
                        col.append(lo)
                    else:
                        row.append(lo)
                        col.append(hi)
                special = pairs == special_pairs and packet_no == 0
                live = not special or x in range(0, 2*K, 2)
                slots.append((tuple(row), tuple(col), x, live))
            packets.append((pairs, packet_no, slots))
    assert len(packets) == B*(r**(2*a))//L
    loads = Counter((row, col) for _, _, slots in packets
                    for row, col, _, live in slots if live)
    all_labels = list(product(range(r), repeat=a))
    for row in all_labels:
        for col in all_labels:
            loads.setdefault((row, col), 0)
    M = sum(loads.values())
    assert M == B*r**(2*a) - (L-K)
    assert max(loads.values()) == B
    deviations = sum((r**(2*a)*load-M)**2 for load in loads.values())
    # Compare the exact variance to 2*M*Delta with Delta=3 in this toy.
    assert deviations <= 2*M*3*(r**(2*a))**2
    group_rows, group_cols = Counter(), Counter()
    for _, _, slots in packets:
        for row, col, _, live in slots:
            if live:
                for i in range(a):
                    group_rows[i, row[i]] += 1
                    group_cols[i, col[i]] += 1
    assert max(group_rows.values())*r <= 3*M
    assert max(group_cols.values())*r <= 3*M
    assert len(packets)*L <= 3*M
    special = next(slots for pairs, n, slots in packets if pairs == special_pairs and n == 0)
    assert [(row[0], col[0], x) for row, col, x, live in special if live] == [
        (0, 1, 0), (0, 1, 2), (0, 1, 4)]
    files = [HERE/'embedding.py', HERE/'PROOF.md',
             ROOT/'upstream/openai-eth-2026/build/quantitative-contraction.tex']
    return {'toy_parameters': {'r': r, 'a': a, 'L': L, 'B': B, 'K': K},
            'packets': len(packets), 'real_edges': M,
            'pair_classes': len(loads), 'max_pair_load': max(loads.values()),
            'group_load_max': max(*group_rows.values(), *group_cols.values()),
            'packing_checks': True, 'special_slots': [0, 2, 4],
            'precision_or_source_schedule_claimed_for_toy': False,
            'sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in files}}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
