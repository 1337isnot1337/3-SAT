#!/usr/bin/env python3
"""Exact bounded checks of the matching fingerprint hitting-set argument."""
from fractions import Fraction
from itertools import product
from collections import Counter
import json


def matchings(vertices):
    if not vertices:
        yield ()
        return
    a = vertices[0]
    for i in range(1, len(vertices)):
        b = vertices[i]
        for tail in matchings(vertices[1:i] + vertices[i + 1:]):
            yield ((a, b),) + tail


def verify(n, q):
    pairs = list(matchings(tuple(range(n))))
    threshold = max(0, (n - 2*q)//2 + 1)
    bound = Fraction(2*q - 1, 2*q)**threshold
    histogram = Counter()
    for colors in product(range(q), repeat=n):
        good = sum(all(colors[a] != colors[b] for a, b in matching)
                   for matching in pairs)
        assert Fraction(good, len(pairs)) <= bound
        histogram[good] += 1
    # Average over random colorings must equal (1-1/q)^(n/2).
    total_good = sum(k*v for k, v in histogram.items())
    assert Fraction(total_good, q**n * len(pairs)) == Fraction(q-1, q)**(n//2)
    # Each matching's Boolean XOR formula has exactly 2^(n/2) assignments.
    # Evaluate its polynomial independently in GF(2) for every binary point.
    if q == 2:
        for matching in pairs:
            satisfying = [x for x in product(range(2), repeat=n)
                          if all(x[a] != x[b] for a, b in matching)]
            assert len(satisfying) == 2**(n//2)
            for colors in product(range(2), repeat=n):
                value = 0
                for x in satisfying:
                    term = 1
                    for a in range(n):
                        if x[a]:
                            term &= colors[a]
                    value ^= term
                expected = int(all(colors[a] != colors[b] for a, b in matching))
                assert value == expected
    return {'n':n,'q':q,'matchings':len(pairs),'colorings':q**n,
            'max_good':max(histogram),'bound':str(bound),
            'mean_good_probability':str(Fraction(total_good,q**n*len(pairs)))}


def main():
    cases = [(2,2),(4,2),(6,2),(8,2),(4,4),(6,4),(8,4)]
    print(json.dumps({'cases':[verify(n,q) for n,q in cases], 'status':'PASS'}, indent=2))

if __name__ == '__main__':
    main()
