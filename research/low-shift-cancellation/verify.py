#!/usr/bin/env python3
"""Check the two-partition low-shift cancellation against exact operators."""
from collections import Counter, defaultdict
from itertools import product
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research/anthropic-operator-ranks'))
from operators import piece_vector, modular_rank  # noqa: E402


def normal_order(h, output):
    """Exact Laurent coefficients for x=v=1^h, y=(h), odd-length output."""
    counts = Counter(output)
    r = (len(output) + 1)//2
    base = math.comb(h, r)**2 * math.factorial(h-r)
    terms = defaultdict(int)
    for choices in product(*(range(n+1) for n in counts.values())):
        split = dict(zip(counts, choices))
        count_z = sum(choices)
        denominator = math.prod(math.factorial(split[k])*math.factorial(n-split[k])
                                for k, n in counts.items())
        weight = sum(k*n for k, n in split.items())
        numerator = h*r*math.factorial(r-1)*math.factorial(r)
        if count_z == r-1:
            terms[weight-r-h] += numerator//denominator
        if count_z == r:
            terms[weight-r] += numerator//denominator
    coefficients = defaultdict(int)
    for exponent, value in terms.items():
        for j in range(2*r+1):
            coefficients[exponent+j] += base*value*math.comb(2*r, j)*(-1)**j
    alpha = (base*math.factorial(2*r)*h
             // math.prod(math.factorial(n) for n in counts.values()))
    return {s: v for s, v in coefficients.items() if v}, alpha



def three_partitions(h):
    for a in range(1, h//3+1):
        for b in range(a, (h-a)//2+1):
            yield (h-a-b, b, a)


def closed_three(h, output):
    counts = Counter(output)
    denominator = math.prod(math.factorial(n) for n in counts.values())
    factor = 4*h*math.comb(h, 2)**2*math.factorial(h-2)
    coefficients = defaultdict(int)
    for part, count in counts.items():
        assert factor*count % denominator == 0
        scalar = factor*count//denominator
        for j in range(5):
            value = scalar*math.comb(4, j)*(-1)**j
            coefficients[part-h-2+j] += value
            coefficients[h-part-2+j] += value
    return {s: v for s, v in coefficients.items() if v}


def run():
    prime = 1000003
    formula_cases = 0
    recurrence_rows = 0
    for h in range(4, 41):
        rows = []
        one = (1,)*h
        for output in three_partitions(h):
            vector = [output.count(j) for j in range(1, h-1)]
            rows.append(vector)
            expected = closed_three(h, output)
            enumerated, _ = normal_order(h, output)
            assert expected == enumerated
            assert all(expected.get(-shift, 0) == value for shift, value in expected.items())
            if h <= 6:
                direct = {shift: dict(piece_vector(one, one, (h,), shift)).get(output, 0)
                          for shift in range(-2*h, 2*h+1)}
                assert {s: value for s, value in direct.items() if value} == expected
                recurrence_rows += 1
            formula_cases += 1
        reference = next(row for row in rows if row[0])
        low_rows = [[reference[0]*value-row[0]*base
                     for value, base in zip(row, reference)] for row in rows]
        assert modular_rank(rows, prime) == h-3
        assert modular_rank(low_rows, prime) == h-4
    print(json.dumps({'h_range': [4, 40], 'three_partition_formula_cases': formula_cases,
                      'complete_recurrence_row_comparisons': recurrence_rows,
                      'multiplicity_and_kernel_rank_cases': 37, 'prime': prime}, indent=2))


if __name__ == '__main__':
    run()
