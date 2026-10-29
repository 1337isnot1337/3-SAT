#!/usr/bin/env python3
"""Bounded integer and Vandermonde checks for the altered Tanner parameters."""
import json
import random


def parameters(n, m, B):
    assert n >= 1 and m >= 1 and B >= 1 and m <= B*n
    mu = m.bit_length()
    H = (1 + B*mu).bit_length()  # ceil(log2(2+B*mu))
    D = (1 << 30) * B*B * mu * H*H
    d = min(m, D)
    r = max(1, (d-1).bit_length())
    q = 1 << ((m+d-1)//d-1).bit_length()
    P = 20000*B*B*r*r
    c = (d+8*B-1)//(8*B)
    h = (d+100*B*r-1)//(100*B*r)-1
    return mu, H, D, d, r, q, P, c, h


def rem(a, b):
    while a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length()-b.bit_length())
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


def main():
    rng = random.Random(719491)
    regimes = {'q1': 0, 'q_gt_1': 0}
    for _ in range(20000):
        bits = rng.randint(1, 512)
        m = rng.randrange(1 << (bits-1), 1 << bits)
        B = rng.randint(1, 1000)
        n = (m+B-1)//B
        mu, H, D, d, r, q, P, c, h = parameters(n, m, B)
        assert q*d >= m and q*d < 2*m
        assert r <= 36*H
        assert r*h <= c
        assert 2*q*c <= 3*n
        assert P == 20000*B*B*r*r
        if q > 1:
            assert d == D
            assert d >= 320000*B*B*r*r*mu
            regimes['q_gt_1'] += 1
        else:
            assert d == m
            regimes['q1'] += 1

    # One modest source-form local code exercises h>1 without constructing
    # a source-scale q>1 graph. Vandermonde powers test distinct supports.
    m, B = 4096, 1
    _, _, _, d, r, q, _, c, h = parameters(m, m, B)
    assert (d, r, q, h) == (4096, 12, 1, 3) and r*h <= c
    f = field(r)
    checks = 0
    for size in (1, 2, 3):
        for _ in range(1000):
            support = rng.sample(range(d), size)
            sums = [0]*h
            for a in support:
                power = 1
                for i in range(h):
                    sums[i] ^= power
                    power = mul(power, a, f, r)
            assert any(sums), support
            checks += 1
    print(json.dumps({'seed': 719491, 'parameter_cases': sum(regimes.values()),
                      'regimes': regimes, 'max_input_bits': 512,
                      'local_d': d, 'local_h': h, 'local_support_samples': checks,
                      'result': 'pass'}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
