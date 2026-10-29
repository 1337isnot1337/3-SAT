#!/usr/bin/env python3
"""Finite controls for the credited PR #64 handoff."""
from itertools import product
from pathlib import Path
from fractions import Fraction
import importlib.util
spec = importlib.util.spec_from_file_location('bias', Path(__file__).with_name('verify_bias.py'))
bias = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bias)
hit_checks = root_checks = 0
for p in (1, 2, 3):
    length = 2*p
    rQ = (16*length-1).bit_length()
    Q = 1 << rQ
    modQ = bias.modulus(rQ)
    for mask in range(1, 1 << length):
        zeros = 0
        for x in range(Q):
            power = 1
            value = 0
            for i in range(length):
                if mask >> i & 1:
                    value ^= power
                power = bias.multiply(power, x, modQ, rQ)
            zeros += value == 0
        assert zeros <= length-1 and Fraction(Q-zeros, 2*Q) >= Fraction(15,32)
        root_checks += 1
    for q in (1, 2, 4, 8):
        for m in range(1 if q == 1 else q//2+1, q+1):
            for support in range(1, 1 << m):
                if support.bit_count()*p < m:
                    continue
                if length > q:
                    assert support != 0
                else:
                    r=(q-1).bit_length()
                    mod=bias.modulus(r)
                    hits=0
                    for a,b in product(range(q),repeat=2):
                        seq=[bias.multiply(a,i,mod,r)^b for i in range(length)]
                        hits += any(support >> v & 1 for v in seq)
                    assert 2*hits >= q*q
                hit_checks += 1
assert 2*Fraction(49,64)**3 < 1
print(f'PASS: {hit_checks} affine or fallback support cases; {root_checks} coefficient root cases; 3-round contraction')
