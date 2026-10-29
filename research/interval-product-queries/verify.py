#!/usr/bin/env python3
"""Exact bounded validation of interval-information-set counting."""
from random import Random


def affine_space(n, equations):
    # Each equation is (coefficient bitmask, right-hand-side bit).
    rows = [a | (b << n) for a, b in equations]
    pivots = []
    rank = 0
    for col in range(n):
        pivot = next((j for j in range(rank, len(rows)) if (rows[j] >> col) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for j in range(len(rows)):
            if j != rank and ((rows[j] >> col) & 1):
                rows[j] ^= rows[rank]
        pivots.append(col)
        rank += 1
    if any((row & ((1 << n) - 1)) == 0 and (row >> n) & 1 for row in rows):
        return None
    free = [j for j in range(n) if j not in pivots]
    origin = sum(((rows[i] >> n) & 1) << pivot for i, pivot in enumerate(pivots))
    basis = []
    for j in free:
        vector = 1 << j
        for i, pivot in enumerate(pivots):
            vector |= ((rows[i] >> j) & 1) << pivot
        basis.append(vector)
    return origin, basis


def add_to_basis(basis, v):
    while v:
        p = v.bit_length() - 1
        if p in basis:
            v ^= basis[p]
        else:
            basis[p] = v
            return True
    return False


def information_set(n, basis):
    d = len(basis)
    coord = [sum(((basis[j] >> i) & 1) << j for j in range(d)) for i in range(n)]
    best = []
    for start in range(n):
        pivots = {}
        block = []
        for length in range(d):
            pos = (start + length) % n
            if not add_to_basis(pivots, coord[pos]):
                break
            block.append(pos)
        if len(block) > len(best):
            best = block
    chosen = best[:]
    pivots = {}
    for pos in chosen:
        assert add_to_basis(pivots, coord[pos])
    for pos in range(n):
        if len(chosen) == d:
            break
        if add_to_basis(pivots, coord[pos]):
            chosen.append(pos)
    assert len(chosen) == d
    return best, chosen, coord



def triple_information_set(n, coord, d):
    selected, used, pivots, triples = [], set(), {}, 0
    # Nonwrapping disjoint triples. Rejected candidates never modify pivots.
    for start in range(max(0, n - 2)):
        positions = [start, start + 1, start + 2]
        if any(i in used for i in positions):
            continue
        trial = pivots.copy()
        if all(add_to_basis(trial, coord[i]) for i in positions):
            pivots = trial
            selected.extend(positions)
            used.update(positions)
            triples += 1
    for i in range(n):
        if len(selected) == d:
            break
        if add_to_basis(pivots, coord[i]):
            selected.append(i)
    assert len(selected) == d
    return triples, selected


def triple_words(t):
    stack = [(0, 0)]
    while stack:
        word, size = stack.pop()
        if size == t:
            yield word
            continue
        for value in range(8):
            if value != 5:
                stack.append((word | (value << (3 * size)), size + 1))

def inverse(rows):
    d = len(rows)
    augmented = [row | (1 << (d + i)) for i, row in enumerate(rows)]
    for col in range(d):
        pivot = next(j for j in range(col, d) if (augmented[j] >> col) & 1)
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        for j in range(d):
            if j != col and ((augmented[j] >> col) & 1):
                augmented[j] ^= augmented[col]
    return [row >> d for row in augmented]


def prefixes(d):
    stack = [(0, 0)]
    while stack:
        word, size = stack.pop()
        if size == d:
            yield word
            continue
        stack.append((word, size + 1))
        if size < 2 or ((word >> (size - 2)) & 3) != 1:
            stack.append((word | (1 << size), size + 1))


def avoids(n, m):
    mask = (1 << n) - 1
    a = (m >> 1) | ((m & 1) << (n - 1))
    b = (m >> 2) | ((m & 3) << (n - 2))
    return not (m & (~a & mask) & b)


def weight(n, word):
    fib = [0, 1]
    for _ in range(n + 1):
        fib.append(fib[-1] + fib[-2])
    if word == 0:
        return fib[n - 1] + fib[n + 1]
    start = next(i for i in range(n) if (word >> i) & 1)
    count, zeros = 1, 0
    for k in range(1, n + 1):
        if (word >> ((start + k) % n)) & 1:
            if zeros:
                count *= fib[zeros - 1]
                zeros = 0
        else:
            zeros += 1
    return count


def count(n, equations, force=None):
    solution = affine_space(n, equations)
    if solution is None:
        return 0, None, None, 0
    origin, basis = solution
    d = len(basis)
    block, chosen, coord = information_set(n, basis)
    r = len(block)
    triples, triple_chosen = triple_information_set(n, coord, d)
    counts = [1, 2, 4]
    for _ in range(3, r + 1):
        counts.append(2 * counts[-1] - counts[-2] + counts[-3])
    prefix_count = counts[r]
    single_cost = (1 << (d-r)) * prefix_count
    triple_cost = (1 << (d-3*triples)) * 7**triples
    use_triples = force == 'triple' or (force is None and triple_cost < single_cost)
    if use_triples:
        chosen, width = triple_chosen, 3*triples
        words = triple_words(triples)
    else:
        width = r
        words = prefixes(r)
    invert = inverse([coord[i] for i in chosen])
    shift = sum(((origin >> i) & 1) << j for j, i in enumerate(chosen))
    total = candidates = 0
    for prefix in words:
        for tail in range(1 << (d-width)):
            target = (prefix | (tail << width)) ^ shift
            z = sum(((row & target).bit_count() % 2) << j for j, row in enumerate(invert))
            m = origin
            for j in range(d):
                if (z >> j) & 1:
                    m ^= basis[j]
            candidates += 1
            if avoids(n, m):
                total += weight(n, m)
    return total, d, r, candidates


def brute(n, equations):
    total = 0
    for x in range(1 << n):
        m = x & ((x >> 1) | ((x & 1) << (n - 1)))
        total += all(((a & m).bit_count() % 2) == b for a, b in equations)
    return total


def main():
    checked = unsat = 0
    dimensions = set()
    # Exhaust all 3 by 3 matrices and right-hand sides.
    n = 3
    for matrix in range(1 << (n*n)):
        for rhs in range(1 << n):
            rows = [((matrix >> (i*n)) & ((1 << n)-1), (rhs >> i) & 1) for i in range(n)]
            answer, d, r, _ = count(n, rows)
            assert answer == brute(n, rows)
            assert count(n, rows, force='triple')[0] == answer
            checked += 1
            unsat += d is None
            if d is not None:
                dimensions.add((d, r))
    rng = Random(1958)
    for n in range(4, 10):
        for _ in range(200):
            rows = [(rng.randrange(1 << n), rng.randrange(2)) for _ in range(rng.randrange(n+3))]
            answer, d, r, _ = count(n, rows)
            assert answer == brute(n, rows)
            assert count(n, rows, force='triple')[0] == answer
            checked += 1
            unsat += d is None
            if d is not None:
                dimensions.add((d, r))
    # Consecutive duplicated coordinate forms show r need not equal d.
    n = 8
    rows = [((1 << (2*i)) | (1 << (2*i+1)), 0) for i in range(4)]
    answer, d, r, candidates = count(n, rows)
    assert (d, r) == (4, 2) and answer == brute(n, rows)
    duplicate = (n, d, r, candidates, answer)
    n = 12
    rows = [((1 << (4*i+2)) | (1 << (4*i+3)), 0) for i in range(3)]
    answer, d, r, candidates = count(n, rows, force='triple')
    assert (d, r, candidates) == (9, 4, 343)
    assert count(n, rows, force='single')[3] == 384
    assert answer == brute(n, rows)
    print('fragmented_control', 'n', n, 'd', d, 'r', r, 'triple_candidates', candidates)
    print('systems', checked, 'inconsistent', unsat, 'dimension_pairs', len(dimensions))
    print('duplicate_pair_control', 'n', duplicate[0], 'd', duplicate[1], 'r', duplicate[2], 'candidates', duplicate[3], 'count', duplicate[4])
    rhs_checks = 0
    for width in range(2, 7):
        n = 2 * width
        for rhs in range(1 << width):
            rows = [((1 << (2*i)) | (1 << (2*i+1)), (rhs >> i) & 1)
                    for i in range(width)]
            ones = rhs.bit_count()
            assert brute(n, rows) == 3**(width-ones) + (-1)**ones
            rhs_checks += 1
    print('duplicate_pair_affine_rhs_checks', rhs_checks, 'd=2..6')
    print('All direct Boolean comparisons passed.')


if __name__ == '__main__':
    main()
