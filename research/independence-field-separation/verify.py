#!/usr/bin/env python3
"""Exact lattice-factorization and field-rank controls."""
import hashlib
import json
import itertools
from pathlib import Path


def subspaces(b):
    spaces = {frozenset({0})}
    todo = list(spaces)
    while todo:
        space = todo.pop()
        for v in range(1 << b):
            if v not in space:
                new = space | frozenset(x ^ v for x in space)
                if new not in spaces:
                    spaces.add(new)
                    todo.append(new)
    return sorted(spaces, key=lambda x: (len(x), tuple(sorted(x))))


def field_rank(matrix, prime):
    rows = [row[:] for row in matrix]
    pivot = 0
    for col in range(len(rows[0])):
        r = next((i for i in range(pivot, len(rows)) if rows[i][col] % prime), None)
        if r is None:
            continue
        rows[pivot], rows[r] = rows[r], rows[pivot]
        inv = pow(rows[pivot][col] % prime, -1, prime)
        rows[pivot] = [x*inv % prime for x in rows[pivot]]
        for i in range(pivot+1, len(rows)):
            c = rows[i][col] % prime
            if c:
                rows[i] = [(x-c*y) % prime for x,y in zip(rows[i], rows[pivot])]
        pivot += 1
        if pivot == len(rows):
            break
    return pivot


def binary_rank(vectors):
    pivots = {}
    for x in vectors:
        while x:
            bit = x.bit_length()-1
            if bit not in pivots:
                pivots[bit] = x
                break
            x ^= pivots[bit]
    return len(pivots)


def full_projective_table(b):
    columns = list(range(1, 1 << b))
    n = len(columns)
    subsets = [[v for i,v in enumerate(columns) if mask >> i & 1]
               for mask in range(1 << n)]
    return [[int(binary_rank(left+right) == len(left)+len(right))
             for right in subsets] for left in subsets]


def small_field_add(x, y, q):
    return (x+y) % 3 if q == 3 else x ^ y


def small_field_mul(x, y, q):
    if q == 3:
        return x*y % 3
    out = 0
    while y:
        if y & 1:
            out ^= x
        x <<= 1
        if x & 4:
            x ^= 7
        y >>= 1
    return out


def general_subspaces(q, b):
    zero = (0,) * b
    universe = list(itertools.product(range(q), repeat=b))
    spaces = {frozenset([zero])}
    todo = list(spaces)
    while todo:
        space = todo.pop()
        for v in universe:
            if v in space:
                continue
            new = frozenset(tuple(small_field_add(u[i], small_field_mul(c,v[i],q),q)
                                  for i in range(b))
                            for u in space for c in range(q))
            if new not in spaces:
                spaces.add(new)
                todo.append(new)
    return sorted(spaces, key=lambda x: (len(x), tuple(sorted(x))))


def run():
    results = []
    factor_checks = 0
    for b in range(5):
        spaces = subspaces(b)
        mu = []
        for z in spaces:
            d = len(z).bit_length()-1
            mu.append((-1)**d * 2**(d*(d-1)//2))
        matrix = []
        for x in spaces:
            row = []
            for y in spaces:
                intersection = x & y
                value = sum(mu[i] for i,z in enumerate(spaces) if z <= intersection)
                assert value == int(intersection == {0})
                row.append(value)
                factor_checks += 1
            matrix.append(row)
        ranks = {str(p): field_rank(matrix, p) for p in (2,3,5)}
        assert ranks['2'] == 2**b
        assert ranks['3'] == ranks['5'] == len(spaces)
        results.append({'dimension': b, 'subspaces': len(spaces), 'ranks': ranks})
    assert [r['subspaces'] for r in results] == [1,2,5,16,67]
    full_ranks = []
    for b in range(1, 4):
        full = full_projective_table(b)
        observed = {str(p): field_rank(full, p) for p in (2,3,5)}
        assert observed == results[b]['ranks']
        full_ranks.append({'dimension': b, 'table_order': len(full), 'ranks': observed})
    general_controls = []
    for q,b in ((3,1), (3,2), (3,3), (4,1), (4,2)):
        spaces = general_subspaces(q,b)
        zero = (0,) * b
        mu = []
        for space in spaces:
            power, dimension = 1, 0
            while power < len(space):
                power *= q
                dimension += 1
            assert power == len(space)
            mu.append((-1)**dimension * q**(dimension*(dimension-1)//2))
        matrix = []
        for x in spaces:
            row = []
            for y in spaces:
                meet = x & y
                value = sum(mu[i] for i,z in enumerate(spaces) if z <= meet)
                assert value == int(meet == {zero})
                row.append(value)
            matrix.append(row)
        characteristic = 3 if q == 3 else 2
        ranks = {str(p): field_rank(matrix,p) for p in (2,3,5)}
        for p in (2,3,5):
            expected = 1 + (q**b-1)//(q-1) if p == characteristic else len(spaces)
            assert ranks[str(p)] == expected
        general_controls.append({'q': q, 'dimension': b, 'subspaces': len(spaces), 'ranks': ranks})
    return {'general_prime_power_controls': general_controls,
            'dimensions_0_to_4': results, 'full_projective_table_ranks': full_ranks,
            'exact_factorization_entries': factor_checks,
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
