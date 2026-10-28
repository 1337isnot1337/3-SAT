#!/usr/bin/env python3
"""Finite independent partition/digit and local-operator controls."""
from itertools import product
from math import factorial


def partitions(n, minimum=1):
    if n == 0:
        yield ()
    for k in range(minimum, n+1):
        for tail in partitions(n-k, k):
            yield (k,) + tail


def digits(part, p):
    result = {}
    for k in set(part):
        number, j = part.count(k), 0
        while number:
            number, d = divmod(number, p)
            if d:
                result[(k, j)] = d
            j += 1
    return result


def direct_digits(n, p):
    modes = []
    for k in range(1, n+1):
        power, j = 1, 0
        while k*power <= n:
            modes.append((k, j, k*power))
            power *= p
            j += 1
    def walk(i, rem, state):
        if i == len(modes):
            if rem == 0:
                yield tuple(state)
            return
        k, j, weight = modes[i]
        for d in range(min(p-1, rem//weight)+1):
            if d:
                state.append(((k, j), d))
            yield from walk(i+1, rem-d*weight, state)
            if d:
                state.pop()
    yield from walk(0, n, [])


def apply(state, k, p):
    coefficient, powers = state
    if k == 0 or not coefficient:
        return 0, powers
    index = abs(k)-1
    powers = list(powers)
    if k < 0:
        if powers[index] == p-1:
            return 0, tuple(powers)
        powers[index] += 1
    else:
        coefficient = coefficient * powers[index] % p
        if powers[index]:
            powers[index] -= 1
    return coefficient, tuple(powers)


def main():
    cases = pairs = count = 0
    for p in (2, 3, 5, 17):
        for n in range(13):
            left = {tuple(sorted(digits(part, p).items())) for part in partitions(n)}
            right = {tuple(sorted(d)) for d in direct_digits(n, p)}
            assert left == right
            for state in left:
                pairing = 1
                for (_, _), d in state:
                    pairing = pairing*factorial(d) % p
                assert pairing
                count += 1
            cases += 1
        for powers in product(range(p), repeat=3):
            for s in (0, 1, 2):
                value = 0
                for offset, factor in ((-1,1), (0,-2), (1,1)):
                    k = s+offset
                    a = apply(apply((1, powers), k, p), -k, p)
                    b = apply(apply((1, powers), -k, p), k, p)
                    if a[0]:
                        assert a[1] == powers
                    if b[0]:
                        assert b[1] == powers
                    value += factor*(a[0]-b[0])
                assert value % p == (1 if s == 1 else 0)
                pairs += 1
    print(f'PASS: {cases} grade bijections, {count} nonzero diagonal pairings, {pairs} direct h=1 operator comparisons')


if __name__ == '__main__':
    main()
