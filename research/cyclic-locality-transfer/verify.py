#!/usr/bin/env python3
"""Reference transfer sweep, checked against direct enumeration; standard library only."""
import itertools
import json
import math
import random


def parity(poly, bit):
    result = 0
    for term in poly:
        product = 1
        for v in term:
            product &= bit(v)
        result ^= product
    return result


def transfer(n, length, tests):
    """Tests are (start, interval_length, tuple of monomial tuples)."""
    assert 1 <= length <= n
    w = length - 1
    ending = [[] for _ in range(n)]
    wrapped = []
    for start, span, poly in tests:
        assert 0 <= start < n and 1 <= span <= length
        allowed = {(start + d) % n for d in range(span)}
        assert all(set(term) <= allowed for term in poly)
        if start + span > n:
            wrapped.append(poly)
        else:
            ending[start + span - 1].append(poly)
    total = 0
    mask = (1 << w) - 1
    for prefix in range(1 << w):
        fixed = lambda j: (prefix >> j) & 1
        if any(parity(poly, fixed) for i in range(w) for poly in ending[i]):
            continue
        initial = sum(fixed(j) << (w - 1 - j) for j in range(w))
        states = {initial: 1}
        for i in range(w, n):
            next_states = {}
            for state, count in states.items():
                for b in (0, 1):
                    extended = (state << 1) | b
                    def bit(j):
                        if j < w:
                            return fixed(j)
                        assert 0 <= i - j <= w
                        return (extended >> (i - j)) & 1
                    if any(parity(poly, bit) for poly in ending[i]):
                        continue
                    new = extended & mask
                    next_states[new] = next_states.get(new, 0) + count
            states = next_states
        for state, count in states.items():
            def boundary(j):
                if j < w:
                    return fixed(j)
                assert 0 <= n - 1 - j < w
                return (state >> (n - 1 - j)) & 1
            if not any(parity(poly, boundary) for poly in wrapped):
                total += count
    return total


def brute(n, tests):
    result = 0
    for x in range(1 << n):
        if all(not parity(poly, lambda j: (x >> j) & 1)
               for _, _, poly in tests):
            result += 1
    return result


def cyclic(n, k):
    t = n.bit_length() - 1
    length = k * t
    return length, [(i, length, tuple(tuple((i + k*j + u) % n
                                  for u in range(k)) for j in range(t)))
                    for i in range(n)]


def periodic_witness(n, k):
    """Count the cyclic witness by enumerating gcd-periodic AND patterns."""
    t = n.bit_length() - 1
    assert k * t < n
    g = math.gcd(n, k * t)
    result = 0
    valid_patterns = 0
    for pattern in range(1 << g):
        def y(i):
            return (pattern >> (i % g)) & 1
        if any(sum(y(i + k*j) for j in range(t)) % 2 for i in range(g)):
            continue
        valid_patterns += 1
        tests = []
        for i in range(n):
            term = tuple((i + u) % n for u in range(k))
            poly = (term, ()) if y(i) else (term,)
            tests.append((i, k, poly))
        result += transfer(n, k, tests)
    return result, g, valid_patterns


def main():
    checks = {'all_local_polynomials': 0, 'random_systems': 0, 'cyclic_witnesses': 0, 'tree_orders': 0, 'periodic_witnesses': 0, 'coprime_formula': 0}
    # Every Boolean polynomial on each length-at-most-three arc, including
    # constants and the zero polynomial. Cyclic arcs exercise the cut.
    for n in range(1, 6):
        for length in range(1, min(n, 3) + 1):
            for start in range(n):
                variables = [(start + i) % n for i in range(length)]
                terms = [tuple(variables[j] for j in range(length) if mask >> j & 1)
                         for mask in range(1 << length)]
                for pmask in range(1 << len(terms)):
                    poly = tuple(term for j, term in enumerate(terms) if pmask >> j & 1)
                    tests = [(start, length, poly)]
                    assert transfer(n, length, tests) == brute(n, tests)
                    checks['all_local_polynomials'] += 1
    rng = random.Random(284761)
    for _ in range(1200):
        n = rng.randrange(1, 10)
        length = rng.randrange(1, n + 1)
        tests = []
        for _ in range(rng.randrange(9)):
            start = rng.randrange(n)
            span = rng.randrange(1, length + 1)
            scope = [(start + j) % n for j in range(span)]
            terms = []
            for _ in range(rng.randrange(6)):
                terms.append(tuple(j for j in scope if rng.randrange(2)))
            tests.append((start, span, tuple(terms)))
        assert transfer(n, length, tests) == brute(n, tests)
        checks['random_systems'] += 1
    for n in range(3, 14):
        for k in (2, 3):
            length, tests = cyclic(n, k)
            if length < n:
                assert transfer(n, length, tests) == brute(n, tests)
                checks['cyclic_witnesses'] += 1
                periodic, g, _ = periodic_witness(n, k)
                assert periodic == brute(n, tests)
                checks['periodic_witnesses'] += 1
                if g == 1:
                    no_runs = sum(not any(all((x >> ((i + u) % n)) & 1
                                              for u in range(k))
                                          for i in range(n))
                                  for x in range(1 << n))
                    assert periodic == no_runs + (1 if (n.bit_length() - 1) % 2 == 0 else 0)
                    checks['coprime_formula'] += 1
    # All circular orderings of the seven-vertex binary tree: verify the
    # diameter-based minimum-span bound without assuming a good ordering.
    n, h = 7, 2
    edges = [((v - 1) // 2, v) for v in range(1, n)]
    minimum = n
    for order in itertools.permutations(range(n)):
        position = {v: i for i, v in enumerate(order)}
        width = max(min((position[u] - position[v]) % n,
                        (position[v] - position[u]) % n) for u, v in edges)
        assert 2 * h * width >= n // 2
        minimum = min(minimum, width)
        checks['tree_orders'] += 1
    print(json.dumps({'seed': 284761, 'checks': checks,
                      'seven_vertex_tree_minimum_span': minimum + 1,
                      'status': 'pass'}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
