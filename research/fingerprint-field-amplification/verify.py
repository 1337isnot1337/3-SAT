#!/usr/bin/env python3
"""Exact finite checks of multilinear fingerprints and equality families."""
import itertools
import json


def mul(a, b, modulus, q):
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & q:
            a ^= modulus
    return out


def fingerprint(solutions, point, modulus, q):
    value = 0
    for x in solutions:
        term = 1
        for i, r in enumerate(point):
            if x >> i & 1:
                term = mul(term, r, modulus, q)
        value ^= term
    return value


def check_all_sets(n, q, modulus):
    points = list(itertools.product(range(q), repeat=n))
    # Precompute each assignment's monomial at each field point.
    columns = [[fingerprint([x], p, modulus, q) for p in points]
               for x in range(1 << n)]
    minimum = len(points)
    for mask in range(1, 1 << (1 << n)):
        count = 0
        for j in range(len(points)):
            value = 0
            for x in range(1 << n):
                if mask >> x & 1:
                    value ^= columns[x][j]
            count += value != 0
        assert count >= (q - 1) ** n, (n, q, mask, count)
        minimum = min(minimum, count)
    assert minimum == (q - 1) ** n
    return {"variables": n, "field_size": q, "nonempty_sets": (1 << (1 << n)) - 1,
            "points_per_set": len(points), "minimum_nonzero_points": minimum}


def check_equalities(k, q, modulus):
    solutions = [sum(((bits >> i) & 1) * (3 << (2*i)) for i in range(k))
                 for bits in range(1 << k)]
    count = 0
    for point in itertools.product(range(q), repeat=2*k):
        value = fingerprint(solutions, point, modulus, q)
        product = 1
        for i in range(k):
            product = mul(product, 1 ^ mul(point[2*i], point[2*i+1], modulus, q),
                          modulus, q)
        assert value == product
        count += value != 0
    assert count == (q*q-q+1)**k
    return {"pairs": k, "field_size": q, "nonzero_points": count,
            "total_points": q**(2*k)}


def main():
    result = {"all_sets": [check_all_sets(4, 2, 0b11), check_all_sets(3, 4, 0b111)],
              "equality_families": [check_equalities(3, 2, 0b11),
                                    check_equalities(2, 4, 0b111),
                                    check_equalities(2, 8, 0b1011)]}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
