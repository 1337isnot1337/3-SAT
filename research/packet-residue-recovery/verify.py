#!/usr/bin/env python3
"""Exact finite checks for residue-class packet witnesses; standard library only."""
from fractions import Fraction
from math import comb
from collections import Counter


def mul(p, q):
    out = [Fraction(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return out


def add(p, q):
    out = [Fraction(0)] * max(len(p), len(q))
    for i, x in enumerate(p): out[i] += x
    for i, x in enumerate(q): out[i] += x
    return out


def shift(p, t, alpha):
    out = [Fraction(0)] * len(p)
    for j, c in enumerate(p):
        for k in range(j + 1):
            out[k] += c * comb(j, k) * t ** (j-k) * alpha ** k
    return out


def v2(x):
    if not x: return float('inf')
    n, d = abs(x.numerator), x.denominator
    return (n & -n).bit_length() - (d & -d).bit_length()


def kernel(L, x, y):
    s = y - x
    p, den = [Fraction(1)], 1
    for t in range(-L, L):
        if t != s: p = mul(p, [-t, 1])
        if t: den *= -t
    return [v / den for v in p]


def main():
    counts = Counter()
    examples = []
    for a in range(1, 4):
        L = 1 << a
        W = [[kernel(L, x, y) for y in range(L)] for x in range(L)]
        for u in range(1, a + 1):
            for mask in range(1, 1 << L):
                occupied = [j for j in range(L) if mask >> j & 1]
                groups = [[j for j in occupied if j % (1 << u) == r]
                          for r in range(1 << u)]
                selected = max(groups, key=len)
                assert len(selected) >= (len(occupied) + (1 << u) - 1) // (1 << u)
                row_polys = []
                for x in selected:
                    row = [Fraction(0)]
                    for y in selected: row = add(row, W[x][y])
                    assert row[0] == 1
                    row_polys.append(row)
                for t in range(-L, L):
                    if not t: continue
                    i = int(v2(Fraction(t)))
                    if i >= u: continue
                    shifted_rows = []
                    for row in row_polys:
                        jet = shift(row, t, 2 * L)
                        shifted_rows.append(jet)
                        assert jet[0] == 0
                        assert all(v2(c) >= a + 1 - i for c in jet)
                        counts['row_jets'] += 1
                    # Check the complete packet polynomial independently of the product bound.
                    if mask % 17 == 0 or mask == (1 << L) - 1:
                        jet = [Fraction(1)]
                        for row in shifted_rows: jet = mul(jet, row)
                        if mask == (1 << L) - 1 and t == -1:
                            f = [Fraction(1)]
                            for row in row_polys: f = mul(f, row)
                            assert jet == shift(f, t, 2 * L)
                            counts['independent_full_shifts'] += 1
                        assert all(not c for c in jet[:len(selected)])
                        assert all(v2(c) >= len(selected) * (a + 1 - i) for c in jet)
                        counts['packet_jets'] += 1
                counts['occupancy_and_u'] += 1
                if mask == (1 << L) - 1 and u == 1:
                    examples.append((L, u, len(selected)))
        # Directly check the original X,Y summation for a sparse packet at a rational point.
        occupied = list(range(L))
        selected = occupied[::2]
        T = Fraction(1, 3)
        values = [[sum(c * T ** k for k, c in enumerate(W[x][y])) for y in range(L)] for x in range(L)]
        expected = Fraction(1)
        for x in selected: expected *= sum(values[x][y] for y in selected)
        total = Fraction(0)
        for ymask in range(1 << len(occupied)):
            if any(not (ymask >> j & 1) for j in range(len(occupied)) if occupied[j] in selected): continue
            term = Fraction(1)
            for j, x in enumerate(occupied):
                z = sum(values[x][y] for y in selected)
                term *= z if ymask >> j & 1 else 1-z
            total += term
        assert total == expected
        counts['direct_network_sums'] += 1
    print('PASS:', dict(sorted(counts.items())))
    print('full-packet examples (L, u, selected rows):', examples)


if __name__ == '__main__': main()
