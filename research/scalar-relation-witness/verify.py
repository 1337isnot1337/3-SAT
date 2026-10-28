#!/usr/bin/env python3
"""Check extremal hook witnesses against the pinned operator implementation."""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research/anthropic-operator-ranks'))
from operators import (partitions, piece_vector, modular_rank, operator,
                       dual_operator, dual_scale)  # noqa: E402


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
        asym_rows = []
        d = (2,) + (1,) * (h - 2)
        for length in range(1, h):
            y = (h - length + 1,) + (1,) * (length - 1)
            intermediate = h - length - 1
            first = (math.factorial(h - 2) * (h - length + 1) * (h + length)
                     // math.factorial(intermediate))
            if intermediate % 2 == 0:
                u = one
                a = intermediate // 2
                second = (math.comb(h, a) * math.factorial(intermediate)
                          // math.factorial(intermediate - a))
            else:
                u = d
                a = (intermediate + 1) // 2
                second = (math.comb(h, a) * (h - a) * math.factorial(intermediate)
                          // math.factorial(intermediate - a))
            values = [dict(piece_vector(d, one, y, s)).get(u, 0)
                      for s in range(-2 * h, 2 * h + 1)]
            bound = h + length + 1
            assert values[2*h - bound] == first * second != 0
            assert values[2*h + bound] == 0
            assert sum((j*j - 4*h*h) * values[j + 2*h]
                       for j in range(-2*h, 2*h + 1)) == 0
            assert all(values[2*h + j] == values[2*h - j] == 0
                       for j in range(bound + 1, 2*h + 1))
            asym_rows.append([values[2*h + j] - values[2*h - j]
                              for j in range(h + 2, 2*h + 1)])
        assert modular_rank(asym_rows, 1000003) == h - 1
        diagonal = [dict(piece_vector(d, d, one, shift)).get(one, 0)
                    for shift in range(-2*h, 2*h + 1)]
        defect = sum((j*j - 4*h*h) * diagonal[j + 2*h]
                     for j in range(-2*h, 2*h + 1))
        assert defect == -8*h*(h-1)*math.factorial(h)
        report.append({'h': h, 'symmetric_rows': h, 'symmetric_rank': h,
                       'antisymmetric_rows': h - 1, 'antisymmetric_rank': h - 1,
                       'diagonal_moment_defect': defect, 'prime': 1000003})
    codebooks = []
    for bits in range(1, 4):
        h = 2
        while len(partitions(h)) < 2**bits:
            h += 1
        states = set(partitions(h)[:2**bits])
        hooks = [length for length in range(1, h + 1) if endpoint(h, length)[0] in states]
        assert (1,) * h in states and (2,) + (1,) * (h-2) in states
        codebooks.append({'bits': bits, 'h': h, 'included_lengths': hooks})
    moment_cases = 0
    for h in range(1, 5):
        label = (1,) * h
        for energy in range(h + 2):
            for y in partitions(energy):
                result = {}
                for shift in range(-energy - h, energy + h + 1):
                    for i in range(2*h + 1):
                        scale = (shift**2 - 4*h*energy) * (-1)**i * math.comb(2*h, i)
                        if not scale:
                            continue
                        for mid, v in operator(label, h - shift - i, y):
                            for u, w in operator(label, shift - h + i, mid):
                                result[u] = result.get(u, 0) + scale*v*w
                assert not any(result.values())
                moment_cases += 1
    mixed_moment_cases = 0
    for h in range(2, 5):
        e = (1,) * h
        d = (2,) + (1,) * (h - 2)
        for energy in range(h + 2):
            for y in partitions(energy):
                for label, expected in ((e, 0),
                                        (d, -4*energy*(h-2)*math.factorial(h))):
                    result = {}
                    for shift in range(-energy-h, energy+h+1):
                        for i in range(2*h+1):
                            scale = shift**2 * (-1)**i * dual_scale(label)
                            for mid, v in operator(label, h-shift-i, y):
                                for u, w in dual_operator(d, i, shift-h+i, mid):
                                    result[u] = result.get(u, 0) + scale*v*w
                    assert all(v == expected*(u == y) for u, v in result.items())
                    assert result.get(y, 0) == expected
                    mixed_moment_cases += 1
    partition_counts = [1] + [0] * 1000
    for part in range(1, 1001):
        for n in range(part, 1001):
            partition_counts[n] += partition_counts[n - part]
    for h in range(11, 1001):
        for r in (math.isqrt(h), math.floor(math.sqrt(h) * math.log(h) / 4)):
            assert (partition_counts[h - r - 1]
                    > partition_counts[h] - partition_counts[h - 1])
    print(json.dumps({'hook_checks': report, 'source_codebook_coverage': codebooks,
                      'second_moment_input_states': moment_cases,
                      'mixed_moment_input_states': mixed_moment_cases,
                      'coverage_inequality_checked_h': [11, 1000]}, indent=2))

if __name__ == '__main__':
    run()
