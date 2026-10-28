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
from operators import piece_vector  # noqa: E402


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


def falling(s, degree):
    return math.prod(s-i for i in range(degree))


def run():
    cases = 0
    comparisons = 0
    for h in range(5, 41):
        one = (1,)*h
        for length in range(3, h-1, 2):
            gap = h-length
            u = (gap+1,) + (1,)*(length-1)
            v = (gap, 2) + (1,)*(length-2)
            pu, alpha_u = normal_order(h, u)
            pv, alpha_v = normal_order(h, v)
            assert pu.get(h+1, 0)*alpha_v == 2*pv.get(h+1, 0)*alpha_u
            assert pu.get(h+1, 0) != 0 and pv.get(h+1, 0) != 0
            w = {s: alpha_v*pu.get(s, 0)-2*alpha_u*pv.get(s, 0)
                 for s in set(pu)|set(pv)}
            assert all(not value for s, value in w.items() if abs(s)>h)
            assert all(w.get(-s, 0) == value for s, value in w.items())
            for degree in range(length+1):
                assert sum(falling(s, degree)*value for s, value in w.items()) == 0
            assert (sum(falling(s, length+1)*value for s, value in w.items())
                    == -math.factorial(length+1)*alpha_u*alpha_v)
            if h <= 6:
                for state, reference in ((u, pu), (v, pv)):
                    direct = {shift: dict(piece_vector(one, one, (h,), shift)).get(state, 0)
                              for shift in range(-2*h, 2*h+1)}
                    assert {s: value for s, value in direct.items() if value} == reference
                    comparisons += 1
            cases += 1
    print(json.dumps({'h_range': [5, 40], 'normal_order_cancellation_cases': cases,
                      'complete_recurrence_row_comparisons': comparisons}, indent=2))


if __name__ == '__main__':
    run()
