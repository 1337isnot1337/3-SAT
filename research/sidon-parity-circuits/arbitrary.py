#!/usr/bin/env python3
"""Count the Sidon-query family by enumerating the cyclic-product kernel."""
from math import gcd


def poly_divmod(a, b):
    if not b:
        raise ZeroDivisionError
    q = 0
    while a and a.bit_length() >= b.bit_length():
        shift = a.bit_length() - b.bit_length()
        q ^= 1 << shift
        a ^= b << shift
    return q, a


def poly_gcd(a, b):
    while b:
        a, b = b, poly_divmod(a, b)[1]
    return a


def poly_mul(a, b):
    out = 0
    while b:
        if b & 1:
            out ^= a
        a <<= 1
        b >>= 1
    return out


def kernel(n):
    if n < 16:
        raise ValueError('n must be at least 16')
    length = n.bit_length() - 3
    shifts = [1 << t for t in range(length)]
    # Reversal and a monomial unit match the output convention
    # P_i = sum_t m_(i+2^t) in the cyclic polynomial ring.
    degree = shifts[-1]
    reflected = sum(1 << (degree - shift) for shift in shifts)
    modulus = (1 << n) | 1
    divisor = poly_gcd(reflected, modulus)
    d = divisor.bit_length() - 1
    quotient, rem = poly_divmod(modulus, divisor)
    assert rem == 0
    return length, d, quotient


def preimages(n, monomials):
    # Sum over cyclic x with x_i*x_(i+1)=m_i, fixing x_0 first.
    total = 0
    for first in (0, 1):
        state = [0, 0]
        state[first] = 1
        for i in range(n):
            wanted = (monomials >> i) & 1
            state = [sum(state[a] for a in (0, 1) if (a & b) == wanted)
                     for b in (0, 1)]
        total += state[first]
    return total


def count(n):
    length, d, quotient = kernel(n)
    return d, sum(preimages(n, poly_mul(quotient, selector))
                  for selector in range(1 << d))


def brute(n):
    shifts = [1 << t for t in range(n.bit_length() - 3)]
    rows = [sum(1 << ((i + t) % n) for t in shifts) for i in range(n)]
    total = 0
    for x in range(1 << n):
        m = x & ((x >> 1) | ((x & 1) << (n - 1)))
        total += all((m & row).bit_count() % 2 == 0 for row in rows)
    return total


def main():
    print('n L d gcd_bound count')
    for n in (16, 17, 18, 20, 31, 32, 35, 42, 63, 64, 66, 75, 100, 128):
        length, d, quotient = kernel(n)
        bound = gcd(n // (n & -n), (1 << length) - 1)
        assert d <= bound
        # Check every enumerated vector against the original row convention.
        shifts = [1 << t for t in range(length)]
        for selector in range(1 << d):
            m = poly_mul(quotient, selector)
            assert m.bit_length() <= n
            assert all(sum((m >> ((i + t) % n)) & 1 for t in shifts) % 2 == 0
                       for i in range(n))
        actual_d, answer = count(n)
        assert actual_d == d
        if n in (16, 17, 18):
            assert answer == brute(n)
        print(n, length, d, bound, answer)
    for length in range(3, 9):
        n = 5 * ((1 << length) - 1)
        actual_length, d, _ = kernel(n)
        assert actual_length == length
        assert d == (1 << (length - 1)) - 1 == (n - 5) // 10
        print('linear_kernel', n, d)
    print('Exhaustive original x assignments checked at n=16,17,18; all checks passed.')


if __name__ == '__main__':
    main()
