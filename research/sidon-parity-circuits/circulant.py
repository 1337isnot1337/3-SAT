#!/usr/bin/env python3
"""Count affine cyclic XOR systems of adjacent Boolean products."""
import importlib.util
from pathlib import Path


def module(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + '.py'))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


a = module('arbitrary')
p = module('prefix')
r = module('runs')


def invmod(value, modulus):
    old_r, cur_r = modulus, value
    old_s, cur_s = 0, 1
    while cur_r:
        quotient, rest = a.poly_divmod(old_r, cur_r)
        old_r, cur_r = cur_r, rest
        old_s, cur_s = cur_s, old_s ^ a.poly_mul(quotient, cur_s)
    if old_r != 1:
        raise ValueError('not invertible')
    return a.poly_divmod(old_s, modulus)[1]


def affine_space(n, coeffs, rhs):
    # coeffs encode forward shifts: P_i = sum_j coeffs_j m_(i+j).
    mask = (1 << n) - 1
    if n < 3 or coeffs & ~mask or rhs & ~mask or min(coeffs, rhs) < 0:
        raise ValueError('invalid binary cyclic system')
    reflected = sum(((coeffs >> j) & 1) << ((-j) % n) for j in range(n))
    modulus = (1 << n) | 1
    h = a.poly_gcd(reflected, modulus)
    d = h.bit_length() - 1
    b, remainder = a.poly_divmod(rhs, h)
    if remainder:
        return None
    q, remainder = a.poly_divmod(modulus, h)
    assert remainder == 0 and q & 1
    if q == 1:
        origin = 0
    else:
        g, remainder = a.poly_divmod(reflected, h)
        assert remainder == 0
        origin = a.poly_divmod(a.poly_mul(invmod(g, q), b), q)[1]
    return d, q, origin


def count(n, coeffs, rhs):
    data = affine_space(n, coeffs, rhs)
    if data is None:
        return 0, None, 0
    d, q, origin = data
    total = candidates = 0
    for prefix in p.prefixes(d):
        candidates += 1
        m = origin ^ p.lift_prefix(prefix ^ (origin & ((1 << d) - 1)), d, q)
        if r.avoids_101(n, m):
            total += r.product_count(n, m)
    return total, d, candidates


def brute(n, coeffs, rhs):
    total = 0
    for x in range(1 << n):
        m = x & ((x >> 1) | ((x & 1) << (n - 1)))
        result = 0
        for i in range(n):
            parity = sum(((coeffs >> j) & 1) & ((m >> ((i + j) % n)) & 1)
                         for j in range(n)) % 2
            result |= parity << i
        total += result == rhs
    return total


def main():
    # Exhaust all 1344 affine cyclic systems at n=3..5. Add deterministic
    # larger cases, including zero, unit, and fully supported operators.
    cases = rejected = 0
    for n in range(3, 6):
        for coeffs in range(1 << n):
            for rhs in range(1 << n):
                value, dimension, _ = count(n, coeffs, rhs)
                assert value == brute(n, coeffs, rhs)
                cases += 1
                rejected += dimension is None
    for n in (6, 7, 8):
        for coeffs in (0, 1, 3, 5, (1 << n) - 1):
            for rhs in (0, 1, 3, (1 << n) - 1):
                value, dimension, _ = count(n, coeffs, rhs)
                assert value == brute(n, coeffs, rhs)
                cases += 1
                rejected += dimension is None
    print('affine_cyclic_systems', cases, 'inconsistent_linear_systems', rejected)
    print('All exact Boolean comparisons passed.')


if __name__ == '__main__':
    main()
