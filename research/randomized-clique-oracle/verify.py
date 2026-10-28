#!/usr/bin/env python3
"""Enumerate the sharp zero/one-hot decision scheme at small rational errors."""
from fractions import Fraction as F
from itertools import combinations
from math import ceil


def main():
    cases = 0
    for m in range(1, 11):
        for delta in (F(0), F(1, 4), F(1, 3), F(2, 5)):
            q = ceil(m*(1-2*delta)/(1-delta))
            subsets = list(combinations(range(m), q))
            assert subsets and 0 <= q <= m
            zero_acceptance = delta  # only the immediate YES branch accepts zero
            assert 1-zero_acceptance >= 1-delta
            for hot in range(m):
                detected = sum(hot in s for s in subsets)
                probability = delta+(1-delta)*F(detected,len(subsets))
                assert probability >= 1-delta
                assert F(detected,len(subsets)) == F(q,m)
            if q:
                assert delta+(1-delta)*F(q-1,m) < 1-delta
            cases += 1
    # One-sided error cannot exploit the upfront false-positive branch.
    m, delta = 10, F(1, 4)
    two_sided = ceil(m*(1-2*delta)/(1-delta))
    one_sided = ceil(m*(1-delta))
    assert two_sided == 7 and one_sided == 8
    print(f'PASS: {cases} exact randomized schemes; one-sided comparison')


if __name__ == '__main__':
    main()
