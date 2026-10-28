#!/usr/bin/env python3
"""Exact finite checks of sparse affine isolation on a systematic code."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import json


def parity(x):
    return x.bit_count() & 1


def main():
    # Two information bits encode systematically into a length-four code.
    code = (0, 3, 12, 15)
    assert min((x ^ y).bit_count() for x,y in combinations(code,2)) == 2
    assert {(x & 1, (x >> 2) & 1) for x in code} == set(product((0,1),repeat=2))
    # Each of two independent positions and coefficient bits is uniform.
    single = [(i,b) for i in range(4) for b in (0,1)]
    rows = Counter()
    for picks in product(single, repeat=2):
        mask = 0
        for i,b in picks:
            mask ^= b << i
        rows[mask] += 1
    assert sum(rows.values()) == 64
    for a,b in combinations(code,2):
        collision = sum(w for row,w in rows.items() if not parity(row & (a^b)))
        d = (a^b).bit_count()
        assert Fraction(collision,64) == (1 + Fraction(4-d,4)**2)/2
        assert Fraction(collision,64) <= Fraction(5,8)
    # Exhaust every nonempty support, choosing t=ceil(log2(2*S)).
    probabilities = []
    for size in range(1,5):
        t = (2*size-1).bit_length()
        for support in combinations(code,size):
            good = 0
            for chosen in product(rows.items(), repeat=t):
                masks = [item[0] for item in chosen]
                weight = 1
                for _,w in chosen:
                    weight *= w
                for target in range(1<<t):
                    count = sum(sum(parity(mask & x)<<i for i,mask in enumerate(masks)) == target
                                for x in support)
                    if count == 1:
                        good += weight
            probability = Fraction(good, 64**t*(1<<t))
            assert probability >= Fraction(1,16)
            probabilities.append(probability)
    # Without distance, a one-bit difference collides with probability 25/32.
    unencoded = Fraction(sum(w for row,w in rows.items() if not parity(row & 1)),64)
    assert unencoded == Fraction(25,32)
    print(json.dumps({'codewords':len(code),'row_outcomes':sum(rows.values()),
        'nonempty_supports':len(probabilities),'min_isolation_probability':str(min(probabilities)),
        'max_encoded_collision':'5/8','unencoded_one_bit_collision':'25/32',
        'status':'PASS'},indent=2))

if __name__ == '__main__':
    main()
