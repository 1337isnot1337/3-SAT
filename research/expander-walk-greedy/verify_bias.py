#!/usr/bin/env python3
"""Exhaust polynomial coefficient families and representative walk controls."""
from fractions import Fraction
from itertools import product


def remainder(a, b):
    while a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length() - b.bit_length())
    return a


def modulus(r):
    for f in range((1 << r) | 1, 1 << (r + 1), 2):
        if all(remainder(f, g) for k in range(1, r // 2 + 1)
               for g in range((1 << k) | 1, 1 << (k + 1), 2)):
            return f
    raise AssertionError('no irreducible')


def multiply(a, b, mod, r):
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & (1 << r):
            a ^= mod
    return out


def trace(a, mod, r):
    acc = 0
    for _ in range(r):
        acc ^= a
        a = multiply(a, a, mod, r)
    assert acc in (0, 1)
    return acc


def family(p):
    r = (2 * p - 1).bit_length()
    h = 1 << r
    mod = modulus(r)
    strings = []
    for x, a in product(range(h), repeat=2):
        power = 1
        mask = 0
        for j in range(p):
            mask |= trace(multiply(a, power, mod, r), mod, r) << j
            power = multiply(power, x, mod, r)
        strings.append(mask)
    return h, strings


subset_checks = direct_cases = lists = 0
for p in range(1, 9):
    h, strings = family(p)
    assert h >= 2*p and len(strings) == h*h and h <= 4*p
    for mask in range(1, 1 << p):
        rejection = sum((mask & c).bit_count() % 2 for c in strings)
        assert 4 * rejection >= len(strings), (p, mask, rejection)
        subset_checks += 1
    if p <= 4:
        for q, shifts in ((1, (0,)), (2, (0, 1)), (4, (0, 1, 2, 3))):
            for m in range(max(1, q//2+1), q+1):
                for support in range(1, 1 << m):
                    if support.bit_count() * p < m:
                        continue
                    rejected = total = 0
                    for start in range(q):
                        for steps in product(shifts, repeat=p-1):
                            vertices = [start]
                            for step in steps:
                                vertices.append(vertices[-1] ^ step)
                            hit = sum(1 << j for j, v in enumerate(vertices) if support >> v & 1)
                            for c in strings:
                                rejected += (hit & c).bit_count() % 2
                                total += 1
                    assert 40*rejected >= total
                    direct_cases += 1
                    lists += total
assert 2 * Fraction(39, 40) ** 28 < 1
print(f'PASS: {subset_checks} nonempty position sets; {direct_cases} walk/support cases; {lists} generated lists; 28-round contraction')
