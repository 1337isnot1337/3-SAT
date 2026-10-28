#!/usr/bin/env python3
"""Check extremal hook witnesses against the pinned operator implementation."""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research/anthropic-operator-ranks'))
from operators import partitions, piece_vector, modular_rank  # noqa: E402


def endpoint(h, length):
    k = h - length + 1
    y = (k,) + (1,) * (length - 1)
    first = math.factorial(h) * k // math.factorial(h - length)
    if (h - length) % 2 == 0:
        a = (h - length) // 2
        second = math.comb(h, a) * math.factorial(h - length) // math.factorial(h - length - a)
        u = (1,) * h
    else:
        a = (h + 1 - length) // 2
        second = math.comb(h, a) * (h - a) * math.factorial(h - length) // math.factorial(h - length - a)
        u = (2,) + (1,) * (h - 2)
    return y, u, first * second


def run():
    report = []
    for h in range(2, 7):
        one = (1,) * h
        matrix = []
        for length in range(1, h + 1):
            y, u, expected = endpoint(h, length)
            values = [dict(piece_vector(one, one, y, s)).get(u, 0)
                      for s in range(-2 * h, 2 * h + 1)]
            assert values[3 * h + length] == expected != 0
            assert all(v == 0 for v in values[3 * h + length + 1:])
            assert values == values[::-1]
            matrix.append([values[3 * h + j] for j in range(1, h + 1)])
        assert modular_rank(matrix, 1000003) == h
        report.append({'h': h, 'hook_rows': h, 'rank_mod_1000003': h})
    codebooks = []
    for bits in range(1, 4):
        h = 2
        while len(partitions(h)) < 2**bits:
            h += 1
        states = set(partitions(h)[:2**bits])
        hooks = [length for length in range(1, h + 1) if endpoint(h, length)[0] in states]
        assert (1,) * h in states and (2,) + (1,) * (h-2) in states
        codebooks.append({'bits': bits, 'h': h, 'included_lengths': hooks})
    print(json.dumps({'hook_checks': report, 'source_codebook_coverage': codebooks}, indent=2))

if __name__ == '__main__':
    run()
