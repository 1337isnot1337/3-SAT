#!/usr/bin/env python3
"""Finite independent checks of separator counting and graph obstruction."""
from itertools import product
from random import Random


def restrict(clauses, assignment):
    result = []
    for clause in clauses:
        if any(abs(lit) in assignment and assignment[abs(lit)] == (lit > 0) for lit in clause):
            continue
        result.append(tuple(lit for lit in clause if abs(lit) not in assignment))
    return result


def graph(vertices, clauses):
    adj = {v: set() for v in vertices}
    for clause in clauses:
        vs = {abs(lit) for lit in clause}
        for v in vs:
            adj[v].update(vs - {v})
    return adj


def parts(vertices, adj):
    todo = set(vertices)
    out = []
    while todo:
        stack = [todo.pop()]
        group = set(stack)
        while stack:
            for w in adj[stack.pop()] & todo:
                todo.remove(w)
                group.add(w)
                stack.append(w)
        out.append(group)
    return out


def hierarchy(vertices, clauses):
    vertices = set(vertices)
    if len(vertices) <= 2:
        return (vertices, [])
    adj = graph(vertices, clauses)
    ordered = sorted(vertices)
    left, right = set(ordered[:len(ordered)//2]), set(ordered[len(ordered)//2:])
    sep = {v for v in left if adj[v] & right}
    if not sep and len(parts(vertices, adj)) == 1:
        sep = {ordered[0]}
    children = parts(vertices - sep, adj)
    assert all(len(c) < len(vertices) for c in children)
    trees = []
    for c in children:
        local = [tuple(x for x in cl if abs(x) in c) for cl in clauses
                 if {abs(x) for x in cl} <= c | sep and any(abs(x) in c for x in cl)]
        trees.append(hierarchy(c, local))
    return (sep, trees)


def all_count(vertices, clauses):
    return sum(all(any(bits[abs(x)-1] == (x > 0) for x in cl) for cl in clauses)
               for bits in product((False, True), repeat=max(vertices, default=0)))


def tree_count(tree, clauses):
    sep, children = tree
    if not children:
        return sum(not any(not cl for cl in restrict(clauses, dict(zip(sorted(sep), bits))))
                   for bits in product((False, True), repeat=len(sep)))
    scopes = [tree_vertices(t) for t in children]
    total = 0
    for bits in product((False, True), repeat=len(sep)):
        rest = restrict(clauses, dict(zip(sorted(sep), bits)))
        if any(not cl for cl in rest):
            continue
        sub = [[] for _ in children]
        for cl in rest:
            matches = [i for i, scope in enumerate(scopes) if {abs(x) for x in cl} <= scope]
            assert len(matches) == 1
            sub[matches[0]].append(cl)
        prod = 1
        for t, cls in zip(children, sub):
            prod *= tree_count(t, cls)
        total += prod
    return total


def tree_vertices(tree):
    sep, children = tree
    return sep | set().union(*(tree_vertices(t) for t in children))


def expander_graph(side):
    n = side * side
    adj = {i: set() for i in range(1, n+1)}
    for x in range(side):
        for y in range(side):
            v = 1 + x * side + y
            for a, b in ((x+1, y), (x, y+1), (x+y, y), (x, y+x)):
                w = 1 + (a % side) * side + b % side
                if v != w:
                    adj[v].add(w)
                    adj[w].add(v)
    return adj


def check():
    rng = Random(2601027)
    checked = 0
    for n in range(1, 9):
        for _ in range(150):
            clauses = []
            for _ in range(rng.randrange(0, 14)):
                width = rng.randrange(0, min(3, n) + 1)
                variables = rng.sample(range(1, n+1), width)
                clauses.append(tuple(v if rng.randrange(2) else -v for v in variables))
            tree = hierarchy(set(range(1, n+1)), clauses)
            assert tree_count(tree, clauses) == all_count(set(range(1, n+1)), clauses)
            checked += 1
    adj = expander_graph(4)
    n = len(adj)
    assert max(map(len, adj.values())) <= 8
    minimum = n
    balanced_count = 0
    for mask in range(1 << n):
        sep = {v for v in adj if mask & (1 << (v-1))}
        cs = parts(set(adj) - sep, adj)
        if all(3 * len(c) <= 2 * n for c in cs):
            minimum = min(minimum, len(sep))
            balanced_count += 1
    assert minimum > 0
    print(f'PASS: {checked} seeded CNFs; 4x4 graph, {sum(map(len, adj.values()))//2} edges; '
          f'{balanced_count} balanced separators; minimum size {minimum}')


if __name__ == '__main__':
    check()
