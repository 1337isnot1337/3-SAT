#!/usr/bin/env python3
"""Enumerate the three-row L=2 integer lifts and check full shifted jets."""
from fractions import Fraction as Q
from math import comb
from pathlib import Path
import runpy

f = runpy.run_path(str(Path(__file__).with_name('verify.py')))
mul, add, v2 = f['mul'], f['add'], f['v2']
L = 2
S = range(-L, L)
def val(p, t): return f['value'](p, t)
def shifted(p, t):
    q = [Q(0)] * len(p)
    for k, c in enumerate(p):
        for j in range(k + 1): q[j] += c * comb(k, j) * t**(k-j) * (2*L)**j
    return q

def residue(x, p):
    mod = 2**p
    assert x.denominator % 2
    return x.numerator * pow(x.denominator, -1, mod) % mod

H = [Q(1), Q(0), Q(-1)]
ws = []
for d in (1, 0, -1):
    w = [Q(1)]
    for t in S:
        if t != d: w = mul(w, [Q(-t), Q(1)])
    ws.append([x / -2 for x in w])
c0 = val(H, -L)
cs = [(val(H, d) - c0) / val(w, d) for d, w in zip((1, 0, -1), ws)]
for p in (1, 2, 3, 4, 5):
    actual = [Q(0)]
    for mask in range(8):
        a = residue(c0 + sum((cs[i] for i in range(3) if mask & (1 << i)), Q(0)), p)
        term = [Q(a)]
        for i, w in enumerate(ws):
            term = mul(term, w if mask & (1 << i) else add([Q(1)], [-x for x in w]))
        actual = add(actual, term)
    difference = add(actual, [-x for x in H])
    assert residue(val(actual, 0), 1) == 1
    for t in S:
        assert all(not x or v2(x) >= p for x in shifted(difference, t))
print('PASS: 5 integer lifts, all 4 nodes, complete shifted polynomials')
