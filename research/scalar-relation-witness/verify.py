#!/usr/bin/env python3
"""Check extremal hook witnesses against the pinned operator implementation."""
from collections import Counter, defaultdict
from itertools import product
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


def low_support_normal_order(h, length):
    """Laurent coefficients from normal ordering, for y=(h), x=v=(1^h)."""
    output = (h - 2*(length - 1),) + (2,) * (length - 1)
    multiplicities = Counter(output)
    r = (length + 1) // 2
    base = math.comb(h, r)**2 * math.factorial(h-r)
    terms = defaultdict(int)
    for choices in product(*(range(count + 1) for count in multiplicities.values())):
        split = dict(zip(multiplicities, choices))
        count_z = sum(choices)
        denominator = math.prod(math.factorial(split[k]) * math.factorial(n-split[k])
                                for k, n in multiplicities.items())
        weight_z = sum(k * count for k, count in split.items())
        numerator = h*r*math.factorial(r-1)*math.factorial(r)
        if count_z == r-1:  # annihilation of t_h at z
            terms[weight_z-r-h] += numerator // denominator
        if count_z == r:    # annihilation of t_h at 1
            terms[weight_z-r] += numerator // denominator
    result = defaultdict(int)
    for exponent, value in terms.items():
        for j in range(2*r+1):
            result[exponent+j] += base * value * math.comb(2*r, j) * (-1)**(2*r-j)
    return output, {s: v for s, v in result.items() if v}


def falling(value, degree):
    result = 1
    for i in range(degree):
        result *= value-i
    return result


def run():
    report = []
    for h in range(2, 7):
        one = (1,) * h
        matrix = []
        full_rows = []
        for length in range(1, h + 1):
            y, u, expected = endpoint(h, length)
            values = [dict(piece_vector(one, one, y, s)).get(u, 0)
                      for s in range(-2 * h, 2 * h + 1)]
            assert values[3 * h + length] == expected != 0
            assert all(v == 0 for v in values[3 * h + length + 1:])
            assert values == values[::-1]
            matrix.append([values[3 * h + j] for j in range(1, h + 1)])
            full_rows.append(values)
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
            full_rows.append(values)
            asym_rows.append([values[2*h + j] - values[2*h - j]
                              for j in range(h + 2, 2*h + 1)])
        assert modular_rank(asym_rows, 1000003) == h - 1
        diagonal = [dict(piece_vector(d, d, one, shift)).get(one, 0)
                    for shift in range(-2*h, 2*h + 1)]
        defect = sum((j*j - 4*h*h) * diagonal[j + 2*h]
                     for j in range(-2*h, 2*h + 1))
        assert defect == -8*h*(h-1)*math.factorial(h)
        full_rows.append(diagonal)
        if h == 6:
            t = 3
            u = (2,) * t + (1,) * (h - 2*t)
            low = [dict(piece_vector(one, one, (h,), shift)).get(u, 0)
                   for shift in range(-2*h, 2*h+1)]
            assert all(low[shift+2*h] == 0
                       for shift in range(-2*h, 2*h+1) if abs(shift) > h)
            r = (h-t+1)//2
            derivatives = [sum(falling(shift, degree) * low[shift+2*h]
                               for shift in range(-2*h, 2*h+1))
                           for degree in range(2*r+1)]
            expected = (math.factorial(2*r)**2 * math.comb(h, r)**2
                        * math.factorial(h-r) * h
                        // (math.factorial(t)*math.factorial(h-2*t)))
            assert derivatives[:-1] == [0]*(2*r) and derivatives[-1] == expected
            assert modular_rank(full_rows + [low], 1000003) == 2*h+1
            _, alternate = low_support_normal_order(h, 3)
            assert {s: low[s+2*h] for s in range(-2*h, 2*h+1) if low[s+2*h]} == alternate
        report.append({'h': h, 'symmetric_rows': h, 'symmetric_rank': h,
                       'antisymmetric_rows': h - 1, 'antisymmetric_rank': h - 1,
                       'diagonal_moment_defect': defect, 'prime': 1000003,
                       'low_support_rank': 2*h+1 if h == 6 else None})
    low_formula_cases = 0
    for h in range(6, 41):
        for length in range(3, h//2+1, 2):
            output, values = low_support_normal_order(h, length)
            r = (length+1)//2
            assert all(abs(shift) <= h for shift in values)
            assert all(values.get(-shift, 0) == value for shift, value in values.items())
            derivatives = [sum(falling(shift, degree)*value for shift, value in values.items())
                           for degree in range(2*r+1)]
            m = Counter(output)
            expected = (math.factorial(2*r)**2 * math.comb(h,r)**2
                        * math.factorial(h-r)*h // math.prod(math.factorial(n) for n in m.values()))
            assert derivatives[:-1] == [0]*(2*r) and derivatives[-1] == expected
            low_formula_cases += 1
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
    # Count partitions with largest part <= r independently by the standard
    # bounded-part generating function.  The complementary tail is exact.
    groups = {}
    for h in range(11, 1001):
        r = math.floor(math.sqrt(h) * math.log(h) / 2)
        groups.setdefault(r, []).append(h)
    bounded = [1] + [0] * 1000
    for r in range(1, max(groups) + 1):
        for n in range(r, 1001):
            bounded[n] += bounded[n-r]
        for h in groups.get(r, ()):
            assert partition_counts[h] - bounded[h] > partition_counts[h] - partition_counts[h-1]
    print(json.dumps({'hook_checks': report, 'source_codebook_coverage': codebooks,
                      'low_support_formula_cases': low_formula_cases,
                      'second_moment_input_states': moment_cases,
                      'mixed_moment_input_states': mixed_moment_cases,
                      'coverage_inequality_checked_h': [11, 1000],
                      'largest_part_tail_c_half_checked_h': [11, 1000]}, indent=2))

if __name__ == '__main__':
    run()
