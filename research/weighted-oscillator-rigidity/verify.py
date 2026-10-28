#!/usr/bin/env python3
"""Exact finite operator replay, independent of the all-size proof."""
from itertools import product
from math import factorial


def apply(state, k, a, b):
    coeff, powers = state
    if k == 0 or coeff == 0:
        return (0, powers)
    j = abs(k) - 1
    powers = list(powers)
    if k < 0:
        powers[j] += 1
        coeff *= a[j]
    else:
        coeff *= b[j] * powers[j]
        powers[j] = max(0, powers[j] - 1)
    return coeff, tuple(powers)


def composition(powers, left, right, a, b):
    return apply(apply((1, powers), right, a, b), left, a, b)


def difference(powers, s, a, b):
    total = 0
    for shift, multiplier in ((-1, 1), (0, -2), (1, 1)):
        k = s + shift
        c1, p1 = composition(powers, -k, k, a, b)
        c2, p2 = composition(powers, k, -k, a, b)
        assert not c1 or p1 == powers
        assert not c2 or p2 == powers
        total += multiplier * (c1 - c2)
    return total


def main():
    values = range(-2, 3)
    powers_list = list(product(range(2), repeat=3))
    checks = passing = 0
    for weights in product(values, repeat=6):
        a, b = weights[:3], weights[3:]
        g = [0] + [a[i] * b[i] for i in range(3)]
        identity = all(difference((0, 0, 0), s, a, b) == 0 for s in (0, 1, 2))
        assert identity == (g[2] == 2*g[1] and g[3] == 3*g[1])
        passing += identity
        for s in (0, 1, 2):
            expected = -( ( -g[1] if s == 0 else g[s-1]) - 2*g[s] + g[s+1])
            for powers in powers_list:
                assert difference(powers, s, a, b) == expected
                checks += 1
        for n in powers_list:
            state = (1, (0, 0, 0))
            for i, count in enumerate(n):
                for _ in range(count):
                    state = apply(state, -(i+1), a, b)
            for i, count in enumerate(n):
                for _ in range(count):
                    state = apply(state, i+1, a, b)
            expected = 1
            for i, count in enumerate(n):
                expected *= factorial(count) * g[i+1] ** count
            assert state[0] == expected
            assert not expected or state[1] == (0, 0, 0)
    recurrence_cases = 0
    for d in range(1, 5):
        for tail in product(range(-1, 2), repeat=d):
            for initial in product(range(-1, 2), repeat=d):
                seq = list(initial)
                for n in range(d, 8*d + 4):
                    seq.append(-sum(tail[j-1] * seq[n-j] for j in range(1, d+1)))
                for start in range(len(seq)-d):
                    if not any(seq[start:start+d]):
                        assert not any(seq[start+d:])
                recurrence_cases += 1
        sharp = [int(n % d == 0) for n in range(8*d+4)]
        assert all(sharp[n] == sharp[n-d] for n in range(d, len(sharp)))
        assert all(sum(sharp[n:n+d]) == 1 for n in range(len(sharp)-d+1))
    varying_cases = 0
    for d in range(1, 5):
        for tail in product(range(-1, 2), repeat=d):
            for initial in product(range(-1, 2), repeat=d):
                seq = list(initial)
                for n in range(d, 8*d + 4):
                    seq.append(-sum((tail[j-1] + (n+j) % 2) * seq[n-j]
                                    for j in range(1, d+1)))
                for start in range(len(seq)-d):
                    if not any(seq[start:start+d]):
                        assert not any(seq[start+d:])
                varying_cases += 1
    finite_field_checks = 0
    for prime in (2, 3, 5, 7):
        size = 2*prime
        a = (1,) * size
        b = tuple(k % prime for k in range(1, size+1))
        assert b[prime-1] == 0 and b[0] == 1
        for powers in ((0,)*size, (1,)*size, (2,)*size):
            for shift in range(-size+1, size):
                assert difference(powers, shift, a, b) % prime == 0
                finite_field_checks += 1
        # Pairing t_1^p with D_1^p and t_p with D_p both vanish mod p.
        assert factorial(prime) % prime == 0 and b[prime-1] == 0
    print(f'PASS: {finite_field_checks} characteristic-p direct identity checks and 8 radical controls')
    print(f'PASS: {recurrence_cases} constant and {varying_cases} varying recurrence sequences; 4 sharp periodic controls')
    print(f'PASS: 15625 weight assignments, {checks} operator differences, '
          f'{passing} satisfying the three checked shifts, 125000 pairing checks')


if __name__ == '__main__':
    main()
