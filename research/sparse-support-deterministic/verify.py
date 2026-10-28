#!/usr/bin/env python3
"""Exact support-isolation and GF(16) interpolation checks."""
from itertools import combinations
import json


def primes(count):
    out = []
    x = 2
    while len(out) < count:
        if all(x % p for p in out if p*p <= x):
            out.append(x)
        x += 1
    return out


def polynomial(n, support, p):
    a = [0] * (n*(p-1)+1)
    for x in support:
        exponent = sum(pow(2,i,p) for i in range(n) if x >> i & 1)
        a[exponent] ^= 1
    return a


def mul(a,b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        if a & 16:
            a ^= 0b10011
        b >>= 1
    return result


def power(a,k):
    z = 1
    while k:
        if k & 1:
            z = mul(z,a)
        a = mul(a,a)
        k >>= 1
    return z


def interpolate(values):
    d = len(values)
    rows = []
    for x,y in enumerate(values):
        row = [1]
        for _ in range(1,d):
            row.append(mul(row[-1],x))
        rows.append(row+[y])
    for col in range(d):
        pivot = next(j for j in range(col,d) if rows[j][col])
        rows[col], rows[pivot] = rows[pivot], rows[col]
        inv = power(rows[col][col],14)
        rows[col] = [mul(z,inv) for z in rows[col]]
        for j in range(d):
            if j != col:
                c = rows[j][col]
                rows[j] = [a ^ mul(c,b) for a,b in zip(rows[j],rows[col])]
    return [r[-1] for r in rows]


def evaluate_fingerprint(n, support, p, t):
    weights = [power(t,pow(2,i,p)) for i in range(n)]
    result = 0
    for x in support:
        term = 1
        for i in range(n):
            if x >> i & 1:
                term = mul(term,weights[i])
        result ^= term
    return result


def main():
    cases = 0
    max_prime_index = 0
    for n in range(1,5):
        N = 1 << n
        ps = primes(n*(N-1)+1)
        for mask in range(1, 1 << N):
            support = [i for i in range(N) if mask >> i & 1]
            L = n*(len(support)-1)+1
            anchor = support[0]
            j = next(j for j,p in enumerate(ps[:L])
                     if all((x-anchor) % p for x in support[1:]))
            max_prime_index = max(max_prime_index,j+1)
            p = ps[j]
            a = polynomial(n,support,p)
            reduced = [0]*p
            for i,c in enumerate(a):
                reduced[i % p] ^= c
            assert reduced[anchor % p] == 1
            cases += 1
    interpolation_cases = 0
    for n in range(1,4):
        for size in range(0, min(4,1 << n)+1):
            for support in combinations(range(1 << n),size):
                for p in (2,3,5):
                    expected = polynomial(n,support,p)
                    vals = [evaluate_fingerprint(n,support,p,t)
                            for t in range(len(expected))]
                    assert interpolate(vals) == expected
                    interpolation_cases += 1
    assert evaluate_fingerprint(1,(0,1),2,1) == 0  # unweighted parity fails
    print(json.dumps({'support_isolation_cases':cases,
                      'largest_first_isolating_prime_index':max_prime_index,
                      'gf16_interpolations':interpolation_cases,
                      'unweighted_even_support_control':'PASS',
                      'status':'PASS'},indent=2))

if __name__ == '__main__':
    main()
