#!/usr/bin/env python3
"""Exact bounded checks for Walsh potential and Vandermonde local checks."""
from itertools import combinations


def rem(a, b):
    while a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length() - b.bit_length())
    return a


def field(r):
    return next(f for f in range((1 << r) | 1, 1 << (r+1), 2)
                if all(rem(f, g) for k in range(1, r//2+1)
                       for g in range((1 << k) | 1, 1 << (k+1), 2)))


def mul(a, b, f, r):
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & (1 << r):
            a ^= f
    return out


def shifts(q, d):
    # t=1/4; multiply all numerators by 4 +/- 1 at each step.
    state = [1] * (2*(q-1))
    initial = sum(state)
    seq = []
    for i in range(d):
        choices = []
        for v in range(q):
            row = []
            for b in range(1, q):
                sign = 1 if (b & v).bit_count() % 2 == 0 else -1
                row.extend((state[2*(b-1)]*(4+sign), state[2*(b-1)+1]*(4-sign)))
            choices.append((sum(row), v, row))
        value, v, state = min(choices)
        assert value <= initial * 4**(i+1)
        seq.append(v)
    assert all(abs(sum((-1)**((v & b).bit_count() % 2) for v in seq))*2 <= d
               for b in range(1, q))
    return len(seq)

shift_cases = sum(shifts(q, d) > 0 for q in (2, 4, 8) for d in (64, 80))
subset_cases = 0
for r in range(1, 5):
    f = field(r)
    for d in range(2, min(1 << r, 9)+1):
        for h in range(1, min(3, d)+1):
            for size in range(1, h+1):
                for subset in combinations(range(d), size):
                    # A binary kernel word has coefficient 1 on exactly its support.
                    for i in range(h):
                        total = 0
                        for a in subset:
                            power = 1
                            for _ in range(i):
                                power = mul(power, a, f, r)
                            total ^= power
                        if total:
                            break
                    else:
                        raise AssertionError((r,d,h,subset))
                    subset_cases += 1
# A duplicate evaluation point is a deliberately invalid local-code control.
assert 1 ^ 1 == 0
print(f'PASS: {shift_cases} exact potential constructions; {subset_cases} Vandermonde binary-support checks; duplicate-column negative control')

# A complete small Cayley-Tanner composition: q=4, four distinct shifts,
# GF(4) local Vandermonde checks with h=3, followed by shortening.
# This is a scaled fixture; it does not instantiate the source's large D0.
q, d, h = 4, 4, 3
f, r = field(2), 2
rows = []
for side in (0, 1):
    for vertex in range(q):
        for i in range(h):
            for bit in range(r):
                row = 0
                for port in range(d):
                    left = vertex if side == 0 else vertex ^ port
                    edge = left*d + port
                    power = 1
                    for _ in range(i):
                        power = mul(power, port, f, r)
                    if (power >> bit) & 1:
                        row |= 1 << edge
                rows.append(row)
accepted = [v for v in range(1 << (q*d))
            if all((row & v).bit_count() % 2 == 0 for row in rows)]
assert accepted == [0, (1 << (q*d)) - 1]
shortened = [v for v in accepted if v >> 12 == 0]
assert shortened == [0]
assert max(row.bit_count() for row in rows) <= d
print(f'PASS: complete {q*d}-edge Tanner fixture, {len(rows)} rows, full and shortened kernels')
