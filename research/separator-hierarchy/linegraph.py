#!/usr/bin/env python3
"""Finite checks for the oriented cubic line-graph construction."""
from itertools import combinations


def example(n, edges, cycle):
    edges = {tuple(sorted(e)) for e in edges}
    assert len(edges) == 3*n//2
    assert all(sum(v in edge for edge in edges) == 3 for v in range(n))
    directions = {}
    for u, v in zip(cycle, cycle[1:] + cycle[:1]):
        edge = tuple(sorted((u, v)))
        assert edge in edges
        directions[edge] = (u, v)
    for edge in edges:
        directions.setdefault(edge, edge)
    names = {edge: i+1 for i, edge in enumerate(sorted(edges))}
    clauses = [[] for _ in range(n)]
    for edge, (u, v) in directions.items():
        clauses[u].append(names[edge])
        clauses[v].append(-names[edge])
    assert all(len(c) == 3 and any(x > 0 for x in c) for c in clauses)
    assert all(sum(x in c for c in clauses) == 1 and sum(-x in c for c in clauses) == 1 for x in names.values())
    assert all(len({abs(x) for x in a} & {abs(x) for x in b}) <= 1 for a,b in combinations(clauses, 2))
    for a, b in combinations(clauses, 2):
        for x in set(a) & {-y for y in b}:
            resolvent = (set(a) - {x}) | (set(b) - {-x})
            assert len(resolvent) == 4 and not any(-y in resolvent for y in resolvent)
    m = len(edges)
    edge_list = sorted(edges)
    min_cut = None
    checked = 0
    for mask in range(1, 1 << m):
        k = mask.bit_count()
        if k > m//2:
            continue
        counts = [sum(bool(mask & (1 << i)) for i,e in enumerate(edge_list) if v in e) for v in range(n)]
        t = sum(a in (1, 2) for a in counts)
        line_cut = sum(bool(mask & (1 << i)) != bool(mask & (1 << j))
                       for i,j in combinations(range(m), 2) if set(edge_list[i]) & set(edge_list[j]))
        assert line_cut == 2*t
        min_cut = line_cut if min_cut is None else min(min_cut, line_cut)
        checked += 1
    print(f'PASS cubic graph n={n}: {m} variables, {len(clauses)} clauses, '
          f'{checked} edge subsets, minimum line-graph cut {min_cut}')


def main():
    example(4, combinations(range(4), 2), [0, 1, 2, 3])
    example(8, ((u,v) for u,v in combinations(range(8), 2) if (u^v).bit_count() == 1),
            [0, 1, 3, 2, 6, 7, 5, 4])


if __name__ == '__main__':
    main()
