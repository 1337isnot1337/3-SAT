#!/usr/bin/env python3
"""Reference interaction-cover counter and independent exhaustive checks."""
import itertools
import json
import random


def edges_of(polys):
    return {edge for poly in polys for term in poly
            for edge in itertools.combinations(sorted(set(term)), 2)}


def greedy_cover(polys):
    cover = set()
    for u, v in sorted(edges_of(polys)):
        if u not in cover and v not in cover:
            cover.update((u, v))
    return cover


def affine_count(n, constraints):
    pivots = {}
    for mask, rhs in constraints:
        while mask:
            pivot = mask.bit_length() - 1
            if pivot in pivots:
                oldmask, oldrhs = pivots[pivot]
                mask ^= oldmask; rhs ^= oldrhs
            else:
                pivots[pivot] = (mask, rhs)
                break
        if not mask and rhs:
            return 0
    return 1 << (n - len(pivots))


def count(n, polys, cover, fixed):
    cover = set(cover)
    assert all(0 <= v < n for v in cover | fixed.keys())
    if not all(u in cover or v in cover for u, v in edges_of(polys)):
        raise ValueError('not a cover')
    remaining = [v for v in range(n) if v not in cover]
    index = {v: j for j, v in enumerate(remaining)}
    free_cover = sorted(cover - fixed.keys())
    total = 0
    for bits in range(1 << len(free_cover)):
        c = {v: fixed[v] for v in cover if v in fixed}
        c.update({v: bits >> j & 1 for j, v in enumerate(free_cover)})
        equations = []
        for poly in polys:
            mask = constant = 0
            for term in poly:
                term = set(term)  # Boolean multilinearization.
                if any(c[v] == 0 for v in term & cover):
                    continue
                outside = term - cover
                assert len(outside) <= 1
                if outside:
                    mask ^= 1 << index[next(iter(outside))]
                else:
                    constant ^= 1
            equations.append((mask, constant))
        equations.extend((1 << index[v], bit) for v, bit in fixed.items() if v in index)
        total += affine_count(len(remaining), equations)
    return total


def brute(n, polys, fixed):
    total = 0
    for x in range(1 << n):
        if any(((x >> v) & 1) != b for v, b in fixed.items()):
            continue
        if all(sum(all((x >> v) & 1 for v in term) for term in poly) % 2 == 0
               for poly in polys):
            total += 1
    return total


def minimum_cover(n, edges):
    return min(mask.bit_count() for mask in range(1 << n)
               if all(mask >> u & 1 or mask >> v & 1 for u, v in edges))


def main():
    rng = random.Random(991054)
    checks = {'individual_polynomials': 0, 'random_systems': 0,
              'cover_certificates': 0, 'fixed_branches': 0,
              'matching_family': 0, 'cnf_systems': 0, 'invalid_cover_rejected': 0}
    # Exhaust all degree <=2 polynomials on three variables, including constants.
    terms = [tuple(i for i in range(3) if mask >> i & 1)
             for mask in range(8) if mask.bit_count() <= 2]
    for pmask in range(1 << len(terms)):
        polys = [tuple(term for j, term in enumerate(terms) if pmask >> j & 1)]
        cover = greedy_cover(polys)
        assert count(3, polys, cover, {}) == brute(3, polys, {})
        checks['individual_polynomials'] += 1
    for _ in range(1600):
        n = rng.randrange(9)
        polys = []
        for _ in range(rng.randrange(7)):
            poly = []
            for _ in range(rng.randrange(7)):
                # Includes constants, repeated terms and repeated variables.
                poly.append(tuple(rng.randrange(n) for _ in range(rng.randrange(4))) if n else ())
            polys.append(tuple(poly))
        cover = greedy_cover(polys)
        edges = edges_of(polys)
        assert all(u in cover or v in cover for u, v in edges)
        assert len(cover) <= 2 * minimum_cover(n, edges)
        checks['cover_certificates'] += 1
        assert count(n, polys, cover, {}) == brute(n, polys, {})
        checks['random_systems'] += 1
        fixed = {v: rng.randrange(2) for v in range(n) if rng.randrange(3) == 0}
        assert count(n, polys, cover, fixed) == brute(n, polys, fixed)
        checks['fixed_branches'] += 1
    for _ in range(400):
        n = rng.randrange(1, 7)
        clauses = [tuple((rng.randrange(n), bool(rng.randrange(2)))
                         for _ in range(rng.randrange(4)))
                   for _ in range(rng.randrange(7))]
        polys = []
        for clause in clauses:
            poly = [()]
            for v, positive in clause:
                # The false indicator is 1+x_v for x_v and x_v for not x_v.
                factors = [(), (v,)] if positive else [(v,)]
                poly = [tuple(set(a) | set(b)) for a in poly for b in factors]
            polys.append(tuple(poly))
        expected = sum(all(any(((x >> v) & 1) == positive for v, positive in clause)
                           for clause in clauses) for x in range(1 << n))
        assert count(n, polys, greedy_cover(polys), {}) == expected
        checks['cnf_systems'] += 1
    for pairs in range(1, 7):
        polys = [((2*i, 2*i+1),) for i in range(pairs)]
        assert minimum_cover(2*pairs, edges_of(polys)) == pairs
        assert count(2*pairs, polys, set(range(0, 2*pairs, 2)), {}) == 3 ** pairs
        checks['matching_family'] += 1
    try:
        count(2, [((0, 1),)], set(), {})
        raise AssertionError('invalid cover accepted')
    except ValueError:
        checks['invalid_cover_rejected'] += 1
    print(json.dumps({'seed': 991054, 'checks': checks, 'status': 'pass'}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
