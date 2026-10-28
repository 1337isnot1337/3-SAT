#!/usr/bin/env python3
"""Bounded exact controls for the oriented-hypercube support witness."""
import itertools
import json
import math
import random


def construction(d):
    assert d > 0 and d % 2 == 0
    n = 1 << d
    rows = []
    for v in range(n):
        row = []
        for j in range(0, d, 2):
            a, b = (v >> j) & 1, (v >> (j + 1)) & 1
            u = v ^ (1 << (j if a == b else j + 1))
            row.append(tuple(sorted((u, v))))
        rows.append(set(row))
    return rows


def rank(vectors):
    pivots = {}
    for x in vectors:
        while x:
            bit = x.bit_length() - 1
            if bit in pivots:
                x ^= pivots[bit]
            else:
                pivots[bit] = x
                break
    return len(pivots)


def combination(rows, mask):
    edges = set()
    for i, row in enumerate(rows):
        if mask >> i & 1:
            edges.symmetric_difference_update(row)
    return edges


def eval_row(edges, x):
    return sum(((x >> a) & 1) * ((x >> b) & 1) for a, b in edges) % 2


def check_order(rows, order, d):
    n = len(rows)
    position = {v: i for i, v in enumerate(order)}
    max_edge_distance = max(min((position[u] - position[v]) % n,
                                (position[v] - position[u]) % n)
                            for row in rows for u, v in row)
    assert d * max_edge_distance >= n // 2


def affine_count(nvars, equations):
    """Number of solutions of binary masks with augmented right sides."""
    pivots = {}
    for mask, rhs in equations:
        while mask:
            bit = mask.bit_length() - 1
            if bit in pivots:
                oldmask, oldrhs = pivots[bit]
                mask ^= oldmask
                rhs ^= oldrhs
            else:
                pivots[bit] = (mask, rhs)
                break
        if not mask and rhs:
            return 0
    return 1 << (nvars - len(pivots))


def bipartite_count(rows, fixed):
    n = len(rows)
    left = [v for v in range(n) if v.bit_count() % 2 == 0]
    right = [v for v in range(n) if v.bit_count() % 2 == 1]
    right_index = {v: i for i, v in enumerate(right)}
    free_left = [v for v in left if v not in fixed]
    total = 0
    for subset in range(1 << len(free_left)):
        value = {v: fixed[v] for v in left if v in fixed}
        value.update({v: (subset >> i) & 1 for i, v in enumerate(free_left)})
        equations = []
        for v in left:
            if value[v]:
                mask = sum(1 << right_index[u if u != v else w]
                           for u, w in rows[v])
                equations.append((mask, 0))
        for v in right:
            active_parity = sum(value[u if u != v else w]
                                for u, w in rows[v]) % 2
            if active_parity:
                equations.append((1 << right_index[v], 0))
            if v in fixed:
                equations.append((1 << right_index[v], fixed[v]))
        total += affine_count(len(right), equations)
    return total


def main():
    rng = random.Random(670104)
    checks = {'cube_edges': 0, 'row_combinations': 0, 'mobius_coefficients': 0,
              'invertible_4_by_4_bases': 0, 'seeded_bases': 0,
              'cyclic_orders': 0, 'bipartite_fixed_branches': 0, 'deleted_vertex_orders': 0, 'middle_layer_controls': 0}
    for d in (2, 4, 6):
        rows = construction(d)
        n, ell = len(rows), d // 2
        all_edges = [edge for row in rows for edge in row]
        assert len(set(all_edges)) == n * ell
        assert len(all_edges) == n * d // 2
        assert all(len(row) == ell for row in rows)
        assert all(sum(v in edge for edge in all_edges) == d for v in range(n))
        assert all(sum(any(v in edge for edge in row) for row in rows) == ell + 1
                   for v in range(n))
        checks['cube_edges'] += len(all_edges)
        masks = range(1, 1 << n) if n == 4 else [rng.randrange(1, 1 << n) for _ in range(500)]
        for mask in masks:
            edges = combination(rows, mask)
            assert len(edges) == ell * mask.bit_count()
            checks['row_combinations'] += 1
            for u, v in edges:
                # Coefficient of x_u x_v in integer zero-indicator 1-P(x).
                coef = sum((-1 if ((3 ^ subset).bit_count() & 1) else 1)
                           * (1 - eval_row(edges, ((subset & 1) << u) | (((subset >> 1) & 1) << v)))
                           for subset in range(4))
                assert coef == -1
                checks['mobius_coefficients'] += 1
        orders = list(itertools.permutations(range(n))) if n == 4 else []
        if n != 4:
            for _ in range(200):
                order = list(range(n)); rng.shuffle(order); orders.append(order)
        for order in orders:
            check_order(rows, order, d)
            checks['cyclic_orders'] += 1
        if n <= 16:
            # Every deletion set, with the surviving labels in natural cyclic order.
            for deleted in range(1 << n):
                order = [v for v in range(n) if not (deleted >> v) & 1]
                if len(order) < 2:
                    continue
                b = deleted.bit_count()
                half = len(order) // 2
                first = set(order[:half])
                positions = {v: i for i, v in enumerate(order)}
                remaining_edges = [(u, v) for u, v in all_edges
                                   if u in positions and v in positions]
                crossing = sum((u in first) != (v in first) for u, v in remaining_edges)
                width = max((min((positions[u] - positions[v]) % len(order),
                                 (positions[v] - positions[u]) % len(order))
                             for u, v in remaining_edges), default=0)
                assert n * (crossing + d * b) >= 2 * half * (n - half)
                assert crossing <= 2 * d * width
                checks['deleted_vertex_orders'] += 1
        if n <= 16:
            # Independent exhaustive full assignments, then test restrictions.
            solutions = [x for x in range(1 << n)
                         if all(eval_row(row, x) == 0 for row in rows)]
            branches = []
            if n == 4:
                for choice in itertools.product(range(3), repeat=n):
                    branches.append({v: c - 1 for v, c in enumerate(choice) if c})
            else:
                for _ in range(120):
                    choices = [rng.randrange(3) for _ in range(n)]
                    branches.append({v: c - 1 for v, c in enumerate(choices) if c})
                branches.append({})
            for fixed in branches:
                expected = sum(all((x >> v) & 1 == b for v, b in fixed.items())
                               for x in solutions)
                assert bipartite_count(rows, fixed) == expected
                checks['bipartite_fixed_branches'] += 1
        if n == 4:
            for basis in itertools.product(range(1 << n), repeat=n):
                if rank(basis) == n:
                    assert all(len(combination(rows, mask)) >= ell for mask in basis)
                    checks['invertible_4_by_4_bases'] += 1
        else:
            for _ in range(100):
                basis = [1 << i for i in range(n)]
                for _ in range(4 * n):
                    a, b = rng.sample(range(n), 2)
                    basis[a] ^= basis[b]
                assert rank(basis) == n
                assert all(len(combination(rows, mask)) >= ell for mask in basis)
                checks['seeded_bases'] += 1
    for d in range(2, 22, 2):
        n = 1 << d
        middle = math.comb(d, d // 2)
        root_ceiling = math.isqrt(d) + (math.isqrt(d) ** 2 != d)
        assert middle <= n // root_ceiling
        assert 2 * sum(math.comb(d, j) for j in range(d // 2)) + middle == n
        # Cube edges flip one bit, hence cannot join weights below and above d/2.
        if d <= 8:
            for row in construction(d):
                for u, v in row:
                    assert not (u.bit_count() < d // 2 < v.bit_count() or
                                v.bit_count() < d // 2 < u.bit_count())
        checks['middle_layer_controls'] += 1
    print(json.dumps({'seed': 670104, 'checks': checks, 'status': 'pass'}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
