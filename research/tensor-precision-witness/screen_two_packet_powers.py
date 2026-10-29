#!/usr/bin/env python3
"""Exact two-packet multilinear span and 2-adic coefficient screen."""
from fractions import Fraction as Q
from math import factorial
from pathlib import Path
import runpy

f = runpy.run_path(str(Path(__file__).with_name('verify.py')))
mul, v2 = f['mul'], f['v2']
for L in (2, 4):
    S = range(-L, L)
    den = (-1)**(L-1) * factorial(L) * factorial(L-1)
    ws = []
    for d in range(-L+1, L):
        w = [Q(1)]
        for t in S:
            if t != d: w = mul(w, [Q(-t), Q(1)])
        ws.append([x/den for x in w])
    ws.append(ws[L-1])  # The second packet's remaining row gives another W_0.
    H = [Q(1)]
    for t in S:
        if t and t % 2: H = mul(H, [Q(1), Q(-1, t)])
    cols = [[Q(1)]]
    for w in ws: cols += [mul(x, w) for x in cols]
    dim = max(map(len, cols))
    basis = {}
    for index, col in enumerate(cols):
        v = col + [Q(0)] * (dim-len(col))
        coeff = {index: Q(1)}
        for p, (b, c) in sorted(basis.items()):
            z = v[p]
            if z:
                v = [x-z*y for x,y in zip(v,b)]
                for k, t in c.items(): coeff[k] = coeff.get(k, Q(0))-z*t
        pivot = next((i for i,x in enumerate(v) if x), None)
        if pivot is not None:
            z = v[pivot]
            basis[pivot] = ([x/z for x in v], {k:x/z for k,x in coeff.items() if x})
    outcomes = []
    for power in range(1, L+1):
        target = [Q(1)]
        for _ in range(power): target = mul(target, H)
        v = target + [Q(0)] * (dim-len(target))
        solution = {}
        for p,(b,c) in sorted(basis.items()):
            z = v[p]
            if z:
                v = [x-z*y for x,y in zip(v,b)]
                for k,t in c.items(): solution[k] = solution.get(k, Q(0))+z*t
        success = not any(v)
        if success:
            # Integral multilinear coefficients imply integral Boolean table values.
            assert all(not x or v2(x) >= 0 for x in solution.values())
            reconstruction = [Q(0)] * dim
            for k,x in solution.items():
                for j,y in enumerate(cols[k]): reconstruction[j] += x*y
            assert reconstruction == target + [Q(0)] * (dim-len(target))
        outcomes.append(success)
    expected = [True, True] if L == 2 else [True, True, True, False]
    assert outcomes == expected
    print('L', L, 'subset products', len(cols), 'rank', len(basis),
          'powers 1..L', outcomes, 'solutions 2-integral')
