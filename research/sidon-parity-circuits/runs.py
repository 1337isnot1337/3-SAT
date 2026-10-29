#!/usr/bin/env python3
"""Check and exploit the run formula for adjacent-product preimages."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location('arbitrary', Path(__file__).with_name('arbitrary.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
kernel, poly_mul, preimages = module.kernel, module.poly_mul, module.preimages


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def product_count(n, word):
    if word == 0:
        return fib(n - 1) + fib(n + 1)
    one = next(i for i in range(n) if (word >> i) & 1)
    result = 1
    zeros = 0
    for step in range(1, n + 1):
        bit = (word >> ((one + step) % n)) & 1
        if bit:
            if zeros:
                result *= fib(zeros - 1)
                zeros = 0
        else:
            zeros += 1
    return result


def avoids_101(n, word):
    mask = (1 << n) - 1
    next1 = (word >> 1) | ((word & 1) << (n - 1))
    next2 = (word >> 2) | ((word & 3) << (n - 2))
    return not (word & (~next1 & mask) & next2)


def main():
    word_checks = 0
    for n in range(3, 11):
        frequencies = [0] * (1 << n)
        for x in range(1 << n):
            m = x & ((x >> 1) | ((x & 1) << (n - 1)))
            frequencies[m] += 1
        for m, actual in enumerate(frequencies):
            assert product_count(n, m) == actual == preimages(n, m)
            assert (actual > 0) == avoids_101(n, m)
            word_checks += 1
    print('exhaustive_cyclic_words', word_checks, 'n=3..10')
    for n in (35, 75, 155):
        length, d, q = kernel(n)
        possible = 0
        total = 0
        for selector in range(1 << d):
            m = poly_mul(q, selector)
            if avoids_101(n, m):
                possible += 1
                total += product_count(n, m)
        print('kernel_filter', n, length, d, possible, 1 << d, 'count', total)
    print('All checks passed.')


if __name__ == '__main__':
    main()
