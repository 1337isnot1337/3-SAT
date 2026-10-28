#!/usr/bin/env python3
"""Compute the source dual pairings directly from (47), with integer arithmetic."""
from collections import Counter
from itertools import product
from math import comb, factorial


def partitions(n, minimum=1):
    if n == 0:
        yield ()
    for part in range(minimum, n+1):
        for tail in partitions(n-part, part):
            yield (part,) + tail


def compositions(n, length):
    if length == 0:
        if n == 0:
            yield ()
        return
    for x in range(1, n-length+2):
        for tail in compositions(n-x, length-1):
            yield (x,) + tail


def source_pairing(mu, nu, normalized=True):
    h = sum(mu)
    mult = Counter(nu)
    z = 1
    for k, m in mult.items():
        z *= k**m * factorial(m)
    assert factorial(h) % z == 0
    total = 0
    for chosen in product(*(range(1, part+1) for part in mu)):
        a_coeff = 1
        for part, j in zip(mu, chosen):
            a_coeff *= (-1)**(part-1)*comb(part, j)
        for ks in compositions(h, len(mu)):
            remaining = mult.copy()
            value = a_coeff
            for j, k in zip(chosen, ks):
                if remaining[k] == 0:
                    value = 0
                    break
                # binom(-k-1,j-1) = (-1)^(j-1) binom(k+j-1,j-1)
                value *= (-1)**(j-1)*comb(k+j-1,j-1)*k*remaining[k]
                remaining[k] -= 1
            total += value
    return total * (factorial(h)//z if normalized else 1)


def main():
    checks = threshold = 0
    for h in range(2, 8):
        labels = list(partitions(h))
        for mu in labels:
            for nu in labels:
                observed = source_pairing(mu, nu)
                expected = factorial(h) if mu == nu else 0
                assert observed == expected, (h, mu, nu, observed, expected)
                for p in (2, 3, 5, 7, 11):
                    assert observed % p == expected % p
                    checks += 1
        for p in (2, 3, 5, 7, 11):
            assert (factorial(h) % p != 0) == (p > h)
            threshold += 1
    restricted = 0
    surviving_below = 0
    for h in range(2, 8):
        labels = list(partitions(h))
        for p in (2, 3, 5, 7, 11):
            codebook = []
            for mu in labels:
                mult = Counter(mu)
                z = 1
                for k, m in mult.items():
                    z *= k**m * factorial(m)
                admissible = all(k % p and m < p for k, m in mult.items())
                assert admissible == bool(z % p)
                if admissible:
                    codebook.append((mu, pow(z, -1, p)))
            if p <= h and codebook:
                surviving_below += 1
            for mu, _ in codebook:
                for nu, inverse in codebook:
                    assert (source_pairing(mu, nu, False)*inverse) % p == int(mu == nu)
                    restricted += 1
    print(f'PASS: {restricted} restricted-codebook pairings, {surviving_below} surviving p<=h controls')
    print(f'PASS: {checks} direct source pairing reductions, {threshold} normalizer threshold controls')


if __name__ == '__main__':
    main()
