#!/usr/bin/env python3
"""Exact rational checks of all taper factors and their packet interpolation."""
from fractions import Fraction as Q
from math import factorial


def mul(p, q):
    out = [Q(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return out


def add(p, q):
    out = [Q(0)] * max(len(p), len(q))
    for i, x in enumerate(p): out[i] += x
    for i, x in enumerate(q): out[i] += x
    while len(out) > 1 and out[-1] == 0: out.pop()
    return out


def value(p, x):
    result = Q(0)
    for c in reversed(p): result = result * x + c
    return result


def v2(q):
    assert q
    n, d = abs(q.numerator), q.denominator
    return (n & -n).bit_length() - (d & -d).bit_length()


def main():
    factors = entries = 0
    for L in (2, 4, 8, 16):
        a = L.bit_length() - 1
        shifts = {L - 1 - x for x in range(L)} | {-x for x in range(1, L)}
        assert shifts == set(range(-L + 1, L))
        grid = range(-L, L)
        den = Q((-1)**(L-1) * factorial(L) * factorial(L-1))
        ws = {}
        for d in shifts:
            W = [Q(1)]
            for t in grid:
                if t != d: W = mul(W, [Q(-t), Q(1)])
            ws[d] = [c / den for c in W]
            assert v2(value(ws[d], d)) == 0
            entries += 1
        product = [Q(1)]
        for j in range(a):
            P = [Q(1)]
            for t in grid:
                if t and v2(Q(t)) <= j:
                    P = mul(P, [Q(1), Q(-1, t)])
            assert len(P) - 1 == 2 * L - L // 2**j
            c0 = value(P, -L)
            assert v2(c0) >= 0
            result = [c0]
            for d in sorted(shifts):
                coeff = (value(P, d) - c0) / value(ws[d], d)
                assert not coeff or v2(coeff) >= 0
                result = add(result, [coeff * c for c in ws[d]])
            assert result == P and value(P, 0) == 1
            product = mul(product, P)
            direct = [Q(1)]
            for t in grid:
                if t:
                    for _ in range(max(0, j + 1 - v2(Q(t)))):
                        direct = mul(direct, [Q(1), Q(-1, t)])
            assert product == direct
            if L == 4 and j == 0: assert c0 == Q(35, 3)
            factors += 1
    print(f'PASS: {entries} Cauchy entries, {factors} factor identities and taper factorizations')

if __name__ == '__main__': main()
