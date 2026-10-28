#!/usr/bin/env python3
"""Exact quadratic character sums and independent exhaustive controls."""
import itertools
import json
import random


def toggle(poly, monomial):
    if monomial in poly:
        poly.remove(monomial)
    else:
        poly.add(monomial)


def product(left, right):
    result = set()
    for a in left:
        for b in right:
            toggle(result, a | b)  # Boolean multilinearization.
    return result


def gauss(n, poly):
    """Sum (-1)^poly(x); each monomial is a bit mask of degree <= 2."""
    poly = set(poly)
    assert all(term.bit_count() <= 2 and term < 1 << n for term in poly)
    active = set(range(n))
    scale = 1
    while True:
        pairs = [t for t in poly if t.bit_count() == 2]
        if not pairs:
            break
        pair = min(pairs)
        i, j = (k for k in range(n) if pair >> k & 1)
        a, b, c = set(), set(), set()
        for term in poly:
            if term == pair:
                continue
            if term >> i & 1:
                toggle(a, term ^ (1 << i))
            elif term >> j & 1:
                toggle(b, term ^ (1 << j))
            else:
                toggle(c, term)
        poly = c.symmetric_difference(product(a, b))
        active.remove(i); active.remove(j)
        scale *= 2
    if any(term != 0 for term in poly):
        return 0
    return scale * (1 << len(active)) * (-1 if 0 in poly else 1)


def rank_split(polys):
    pivots = {}
    affine = []
    for p in polys:
        row = set(p)
        while True:
            quad = [m for m in row if m.bit_count() == 2]
            if not quad:
                affine.append(row)
                break
            pivot = max(quad)
            if pivot not in pivots:
                pivots[pivot] = row
                break
            row.symmetric_difference_update(pivots[pivot])
    return list(pivots.values()), affine


def affine_parameterization(n, affine):
    pivots = {}
    for poly in affine:
        mask = sum(term for term in poly if term)
        rhs = int(0 in poly)
        while mask:
            p = mask.bit_length() - 1
            if p not in pivots:
                pivots[p] = (mask, rhs)
                break
            old, oldrhs = pivots[p]
            mask ^= old; rhs ^= oldrhs
        if not mask and rhs:
            return None
    free = [v for v in range(n) if v not in pivots]
    forms = [None] * n
    for k, v in enumerate(free):
        forms[v] = {1 << k}
    for v in sorted(pivots):
        mask, rhs = pivots[v]
        form = {0} if rhs else set()
        for j in range(v):
            if mask >> j & 1:
                form.symmetric_difference_update(forms[j])
        forms[v] = form
    return len(free), forms


def substitute(poly, forms):
    result = set()
    for term in poly:
        factors = [forms[j] for j in range(len(forms)) if term >> j & 1]
        out = {0}
        for factor in factors:
            out = product(out, factor)
        result.symmetric_difference_update(out)
    return result


def count(n, polys, fixed):
    assert all(0 <= m < 1 << n and m.bit_count() <= 2 for p in polys for m in p)
    quadratics, affine = rank_split(polys)
    affine.extend(({1 << v, 0} if bit else {1 << v}) for v, bit in fixed.items())
    parameter = affine_parameterization(n, affine)
    if parameter is None:
        return 0, len(quadratics)
    free, forms = parameter
    quadratics = [substitute(p, forms) for p in quadratics]
    total = 0
    for selection in range(1 << len(quadratics)):
        q = set()
        for j, poly in enumerate(quadratics):
            if selection >> j & 1:
                q.symmetric_difference_update(poly)
        total += gauss(free, q)
    assert total % (1 << len(quadratics)) == 0
    return total // (1 << len(quadratics)), len(quadratics)


def cubic_cover(polys):
    cover = set()
    for term in sorted({m for p in polys for m in p if m.bit_count() == 3}):
        if not any(term >> v & 1 for v in cover):
            cover.update(v for v in range(term.bit_length()) if term >> v & 1)
    return cover


def cubic_count(n, polys, cover, fixed):
    assert all(m.bit_count() <= 3 and 0 <= m < 1 << n for p in polys for m in p)
    cover = set(cover)
    assert all(any(m >> v & 1 for v in cover) for p in polys for m in p if m.bit_count() == 3)
    free = sorted(cover - fixed.keys())
    total, max_rank = 0, 0
    for assignment in range(1 << len(free)):
        vals = {v: fixed[v] for v in cover if v in fixed}
        vals.update({v: assignment >> j & 1 for j, v in enumerate(free)})
        residual = []
        for poly in polys:
            q = set()
            for term in poly:
                if any((term >> v & 1) and not bit for v, bit in vals.items()):
                    continue
                for v in cover:
                    term &= ~(1 << v)
                toggle(q, term)
            residual.append(q)
        remaining_fixed = {v: b for v, b in fixed.items() if v not in cover}
        # Fixed cover variables are removed from all equations; fix them again
        # to avoid introducing artificial free-variable multiplicities.
        remaining_fixed.update(vals)
        amount, r = count(n, residual, remaining_fixed)
        total += amount
        max_rank = max(max_rank, r)
    return total, max_rank


def evaluate(poly, x):
    return sum((x & term) == term for term in poly) % 2


def brute(n, polys, fixed):
    return sum(all(((x >> v) & 1) == b for v, b in fixed.items()) and
               all(evaluate(p, x) == 0 for p in polys) for x in range(1 << n))


def main():
    checks = {'individual_quadratic_sums': 0, 'random_systems': 0,
              'fixed_branches': 0, 'dependent_row_controls': 0,
              'linear_rank_controls': 0, 'block_matching_controls': 0, 'degree_three_rejected': 0,
              'cubic_systems': 0, 'cubic_fixed_branches': 0, 'cubic_cover_certificates': 0}
    n = 4
    terms = [0] + [1 << i for i in range(n)] + [(1 << i) | (1 << j)
             for i, j in itertools.combinations(range(n), 2)]
    for select in range(1 << len(terms)):
        poly = {term for j, term in enumerate(terms) if select >> j & 1}
        expected = sum((-1) ** evaluate(poly, x) for x in range(1 << n))
        assert gauss(n, poly) == expected
        checks['individual_quadratic_sums'] += 1
    rng = random.Random(121101)
    for _ in range(1800):
        n = rng.randrange(0, 8)
        terms = [0] + [1 << i for i in range(n)] + [(1 << i) | (1 << j)
                 for i, j in itertools.combinations(range(n), 2)]
        polys = [{term for term in terms if rng.randrange(3) == 0}
                 for _ in range(rng.randrange(8))]
        observed, r = count(n, polys, {})
        assert observed == brute(n, polys, {})
        assert r <= min(len(polys), n * (n - 1) // 2)
        checks['random_systems'] += 1
        fixed = {v: rng.randrange(2) for v in range(n) if rng.randrange(3) == 0}
        assert count(n, polys, fixed)[0] == brute(n, polys, fixed)
        checks['fixed_branches'] += 1
        if polys:
            copied, same_rank = count(n, polys + [set(polys[0])], fixed)
            assert same_rank == r and copied == brute(n, polys, fixed)
            checks['dependent_row_controls'] += 1
    for _ in range(800):
        n = rng.randrange(0, 8)
        terms = [mask for mask in range(1 << n) if mask.bit_count() <= 3]
        polys = [{term for term in terms if rng.randrange(5) == 0}
                 for _ in range(rng.randrange(6))]
        cover = cubic_cover(polys)
        cubics = {m for p in polys for m in p if m.bit_count() == 3}
        optimum = min((mask.bit_count() for mask in range(1 << n)
                       if all(mask & m for m in cubics)), default=0)
        assert len(cover) <= 3 * optimum
        checks['cubic_cover_certificates'] += 1
        assert cubic_count(n, polys, cover, {})[0] == brute(n, polys, {})
        checks['cubic_systems'] += 1
        fixed = {v: rng.randrange(2) for v in range(n) if rng.randrange(3) == 0}
        assert cubic_count(n, polys, cover, fixed)[0] == brute(n, polys, fixed)
        checks['cubic_fixed_branches'] += 1
    # One cubic transversal variable can expose many independent quadratics.
    n = 9
    polys = [{1 | (1 << (2*i+1)) | (1 << (2*i+2))} for i in range(4)]
    amount, max_rank = cubic_count(n, polys, {0}, {})
    assert max_rank == 4 and amount == brute(n, polys, {}) == 2**8 + 3**4
    for n in range(1, 9):
        polys = [{0, 1 << i} for i in range(n)]
        assert count(n, polys, {}) == (1, 0)
        checks['linear_rank_controls'] += 1
    for blocks in range(1, 4):
        width = 4
        n = blocks * width
        polys = []
        for b in range(blocks):
            polys.append({(1 << (b * width + 2*j)) | (1 << (b * width + 2*j + 1))
                          for j in range(width // 2)})
        observed, r = count(n, polys, {})
        assert r == blocks
        expected_block = (1 << (width - 1)) + (1 << (width // 2 - 1))
        assert observed == expected_block ** blocks == brute(n, polys, {})
        checks['block_matching_controls'] += 1
    try:
        count(3, [{0b111}], {})
        raise AssertionError('cubic term accepted')
    except AssertionError as exc:
        assert str(exc) != 'cubic term accepted'
        checks['degree_three_rejected'] += 1
    print(json.dumps({'seed': 121101, 'checks': checks, 'status': 'pass'}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
