#!/usr/bin/env python3
"""Exact lattice-factorization and field-rank controls."""
import hashlib
import json
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
    return {'dimensions_0_to_4': results, 'exact_factorization_entries': factor_checks,
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
