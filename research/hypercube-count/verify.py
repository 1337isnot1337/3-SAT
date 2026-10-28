#!/usr/bin/env python3
"""Direct finite controls for the cube-adjacency count."""
import hashlib
import json
import itertools
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent

def adjacency(d, vector):
    m = 1 << d
    out = 0
    for v in range(m):
        bit = 0
        for j in range(d):
            bit ^= (vector >> (v ^ (1 << j))) & 1
        out |= bit << v
    return out

def formula(d):
    m = 1 << d
    if d % 2:
        return 3 ** m
    q = m // 2
    return (1 << q) * sum(1 << (m - w.bit_count() - adjacency(d-1, w).bit_count())
                          for w in range(1 << q))

def direct_y(d):
    m = 1 << d
    return sum(1 << (m - adjacency(d, y).bit_count()) for y in range(1 << m))

def direct_xy(d):
    m = 1 << d
    count = 0
    for y in range(1 << m):
        for x in range(1 << m):
            valid = True
            for v in range(m):
                parity = sum((y >> (v ^ (1 << j))) & 1 for j in range(d)) % 2
                if ((x >> v) & 1) and parity:
                    valid = False
                    break
            count += valid
    return count

def branch_direct(d, xmask, xones, ymask, yones):
    m = 1 << d
    allbits = (1 << m) - 1
    count = 0
    for y in range(1 << m):
        if y & ymask != yones:
            continue
        z = adjacency(d, y)
        if z & xones:
            continue
        count += 1 << ((~xmask & ~z & allbits).bit_count())
    return count

def branch_fourier(d, xmask, xones, ymask, yones):
    m = 1 << d
    allbits = (1 << m) - 1
    xzero = xmask & ~xones
    free = allbits & ~xmask
    total = 0
    subset = ymask
    while True:
        a = adjacency(d, subset)
        if not (a & xzero):
            value = (3 ** ((free & ~a).bit_count())) * (1 << xzero.bit_count())
            total += -value if (subset & yones).bit_count() % 2 else value
        if not subset:
            break
        subset = (subset - 1) & ymask
    divisor = 1 << ymask.bit_count()
    assert total % divisor == 0
    return total // divisor

def main():
    checks = {'basis_square_checks': 0, 'block_image_checks': 0,
              'all_xy_assignments': 0, 'all_y_assignments': 0,
              'formula_counts': {}, 'odd_branch_cases': 0, 'contradictory_branches': 0}
    for d in range(1, 11):
        m = 1 << d
        for v in range(m):
            vector = 1 << v
            assert adjacency(d, adjacency(d, vector)) == (vector if d % 2 else 0)
            checks['basis_square_checks'] += 1
        if d % 2 == 0:
            q = m // 2
            for v in range(m):
                vector = 1 << v
                image = adjacency(d, vector)
                low, high = image & ((1 << q) - 1), image >> q
                assert adjacency(d-1, low) == high
                checks['block_image_checks'] += 1
    for d in range(1, 5):
        actual = direct_y(d)
        assert formula(d) == actual
        checks['all_y_assignments'] += 1 << (1 << d)
        if d <= 3:
            assert direct_xy(d) == actual
            checks['all_xy_assignments'] += 1 << (2 * (1 << d))
        checks['formula_counts'][str(d)] = str(actual)
    assert formula(1) == 9 and formula(2) == 100
    rng = random.Random(20261028)
    for d in (1, 3):
        m = 1 << d
        assignments = itertools.product(range(3), repeat=2*m) if d == 1 else (
            tuple(rng.randrange(3) for _ in range(2*m)) for _ in range(800))
        for digits in assignments:
            xmask = sum(1 << i for i, z in enumerate(digits[:m]) if z)
            xones = sum(1 << i for i, z in enumerate(digits[:m]) if z == 2)
            ymask = sum(1 << i for i, z in enumerate(digits[m:]) if z)
            yones = sum(1 << i for i, z in enumerate(digits[m:]) if z == 2)
            expected = branch_direct(d, xmask, xones, ymask, yones)
            assert branch_fourier(d, xmask, xones, ymask, yones) == expected
            checks['odd_branch_cases'] += 1
            checks['contradictory_branches'] += expected == 0
    print(json.dumps({'scope': 'bounded exact controls; no independent proof review',
                      'checks': checks,
                      'sha256': {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                                 for name in ('PROOF.md', 'verify.py')}}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
