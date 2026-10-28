#!/usr/bin/env python3
"""Exact cyclic-kernel count via 101-free prefix generation."""
import importlib.util
from pathlib import Path


def module(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + '.py'))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


arbitrary = module('arbitrary')
runs = module('runs')


def prefixes(d):
    # Iterative depth-first generation: an appended 1 after 10 is forbidden.
    stack = [(0, 0)]
    while stack:
        word, size = stack.pop()
        if size == d:
            yield word
            continue
        stack.append((word, size + 1))
        if size < 2 or ((word >> (size - 2)) & 3) != 1:
            stack.append((word | (1 << size), size + 1))


def lift_prefix(prefix, d, quotient):
    # q[0]=1 makes m=qv lower-triangular with unit diagonal.
    value = 0
    for j in range(d):
        if ((value ^ prefix) >> j) & 1:
            value ^= quotient << j
    return value


def count(n):
    length, d, quotient = arbitrary.kernel(n)
    assert quotient & 1
    candidates = eligible = total = 0
    for prefix in prefixes(d):
        candidates += 1
        m = lift_prefix(prefix, d, quotient)
        assert m.bit_length() <= n
        if runs.avoids_101(n, m):
            eligible += 1
            total += runs.product_count(n, m)
    return length, d, candidates, eligible, total


def main():
    # Independent recurrence and brute-force controls on prefix generation.
    a = [1, 2, 4]
    for j in range(3, 21):
        a.append(2 * a[-1] - a[-2] + a[-3])
    for d in range(16):
        generated = list(prefixes(d))
        assert len(set(generated)) == len(generated) == a[d]
        assert all(not any(((x >> j) & 7) == 5 for j in range(d - 2)) for x in generated)
    for n in (16, 17, 18, 31, 32, 35, 42, 63, 64, 66, 75, 100, 128, 155):
        length, d, candidates, eligible, total = count(n)
        assert candidates == a[d]
        if d <= 7:
            assert total == arbitrary.count(n)[1]
        if n in (16, 17, 18):
            assert total == arbitrary.brute(n)
        if n == 155:
            assert eligible == 435
            assert total == 247220362414275525275866163932095
        print(n, length, d, candidates, eligible, total)
    print('All checks passed.')


if __name__ == '__main__':
    main()
