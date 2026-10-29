"""Deterministic rational oblique compression; standard library, Apache-2.0.

Matrices are sparse columns: matrices[a][j][i] = A_a[i,j].
The identity must be the first matrix. No positivity is asserted.
"""
from fractions import Fraction


def independent_indices(vectors):
    pivots = {}
    selected = []
    for i, vector in enumerate(vectors):
        row = list(map(Fraction, vector))
        for p, basis in sorted(pivots.items()):
            c = row[p]
            if c:
                row = [x - c*y for x, y in zip(row, basis)]
        p = next((j for j, x in enumerate(row) if x), None)
        if p is not None:
            c = row[p]
            pivots[p] = [x/c for x in row]
            selected.append(i)
    return selected


def coordinates(basis, target):
    """Exact unique coordinates of target in an independent vector list."""
    r = len(basis)
    rows = [[Fraction(v[j]) for v in basis] + [Fraction(target[j])]
            for j in range(len(target))]
    pivot = 0
    for col in range(r):
        p = next(i for i in range(pivot, len(rows)) if rows[i][col])
        rows[pivot], rows[p] = rows[p], rows[pivot]
        c = rows[pivot][col]
        rows[pivot] = [x/c for x in rows[pivot]]
        for i in range(len(rows)):
            if i != pivot and rows[i][col]:
                c = rows[i][col]
                rows[i] = [x-c*y for x, y in zip(rows[i], rows[pivot])]
        pivot += 1
    if any(not any(row[:-1]) and row[-1] for row in rows):
        raise ValueError("Target outside the basis span")
    return [rows[i][-1] for i in range(r)]


def affine_groups(signatures):
    """Pack disjoint maximal bases, all spanning the final surviving point."""
    if not signatures or any(v[0] != 1 for v in signatures):
        raise ValueError("Nonempty signatures with leading coordinate one required")
    remaining = list(range(len(signatures)))
    layers = {}
    groups = []
    while remaining:
        local = independent_indices([signatures[i] for i in remaining])
        group = [remaining[i] for i in local]
        groups.append(group)
        layers.setdefault(len(group), []).append(group)
        removed = set(group)
        remaining = [i for i in remaining if i not in removed]
    target = signatures[groups[-1][0]]
    weights = [coordinates([signatures[i] for i in g], target) for g in groups]
    return groups, weights, target, {r: len(gs) for r, gs in layers.items()}


def compress(matrices):
    """Return sparse U rows and V columns with UV=I and U A_a V=c_a I."""
    n = len(matrices[0])
    if any(len(a) != n for a in matrices):
        raise ValueError("Matrix dimensions disagree")
    if matrices[0] != [{j: 1} for j in range(n)]:
        raise ValueError("First matrix must be exactly the identity")
    graph = [set() for _ in range(n)]
    for a in matrices:
        for j, column in enumerate(a):
            for i, value in column.items():
                if i != j and value:
                    graph[i].add(j)
                    graph[j].add(i)
    chosen = []
    excluded = set()
    for i in range(n):
        if i not in excluded:
            chosen.append(i)
            excluded.add(i)
            excluded.update(graph[i])
    signatures = [tuple(a[i].get(i, 0) for a in matrices) for i in chosen]
    groups, weights, target, layers = affine_groups(signatures)
    u = [{chosen[i]: c for i, c in zip(g, w) if c}
         for g, w in zip(groups, weights)]
    v = [{chosen[i]: 1 for i in g} for g in groups]
    return {"u": u, "v": v, "scalars": target, "independent": chosen,
            "layers": layers, "max_degree": max(map(len, graph), default=0)}


def sandwich(u, matrix, v):
    result = []
    for row in u:
        result.append([sum(c * matrix[j].get(i, 0) * z
                           for i, c in row.items() for j, z in col.items())
                       for col in v])
    return result
