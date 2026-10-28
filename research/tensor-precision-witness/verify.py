#!/usr/bin/env python3
"""Exact rational check of interpolation realization; no external dependencies."""
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
    cases = 0
    for L in (2, 4, 8, 16):
        grid = range(-L, L)
        C = [Q(1)]
        H = [Q(1)]
        for t in grid:
            C = mul(C, [Q(-t), Q(1)])
            if t and t % 2:
                H = mul(H, [Q(1), Q(-1, t)])
        den = Q((-1)**(L-1) * factorial(L) * factorial(L-1))
        c0 = value(H, -L)
        assert v2(c0) >= 0
        result = [c0]
        for d in range(-L+1, L):
            W = [Q(1)]
            for t in grid:
                if t != d: W = mul(W, [Q(-t), Q(1)])
            W = [c / den for c in W]
            wd = value(W, d)
            assert v2(wd) == 0
            coeff = (value(H, d) - c0) / wd
            assert not coeff or v2(coeff) >= 0
            result = add(result, [coeff * c for c in W])
            cases += 1
        assert result == H
        assert value(H, 0) == 1
        if L == 4:
            assert value(H, -L) == Q(35, 3)
    print(f'PASS: {cases} exact Cauchy entries; 4 full polynomial identities and 2-adic coefficient checks')

if __name__ == '__main__': main()
