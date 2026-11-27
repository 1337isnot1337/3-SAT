#!/usr/bin/env python3
"""Bounded exact controls. Standard library; no contraction solver is invoked."""
import hashlib
import itertools
import json
from pathlib import Path
import random


def span(vectors):
    values = {0}
    for v in vectors:
        values |= {x ^ v for x in values}
    return values


def syndrome(cols, word):
    out = 0
    for j, col in enumerate(cols):
        if word >> j & 1:
            out ^= col
    return out


def rank_mod(matrix, p):
    matrix = [list(row) for row in matrix]
    r = 0
    for c in range(len(matrix[0]) if matrix else 0):
        pivot = next((i for i in range(r, len(matrix)) if matrix[i][c] % p), None)
        if pivot is None:
            continue
        matrix[r], matrix[pivot] = matrix[pivot], matrix[r]
        inverse = pow(matrix[r][c], -1, p)
        matrix[r] = [(x * inverse) % p for x in matrix[r]]
        for i in range(r + 1, len(matrix)):
            q = matrix[i][c] % p
            matrix[i] = [(a - q * b) % p for a, b in zip(matrix[i], matrix[r])]
        r += 1
    return r


def layouts(m):
    # parent precedes child; ownership may include empty internal vertices.
    yield [-1] + list(range(m - 1)), [[i] for i in range(m)]
    yield [-1] + [0] * m, [[]] + [[i] for i in range(m)]
    parent, owners = [-1], [[]]
    def split(v, coordinates):
        if len(coordinates) <= 1:
            owners[v] = coordinates
            return
        mid = len(coordinates) // 2
        for chunk in (coordinates[:mid], coordinates[mid:]):
            child = len(parent)
            parent.append(v)
            owners.append([])
            split(child, chunk)
    split(0, list(range(m)))
    yield parent, owners
    yield [-1], [list(range(m))]
    yield [-1, 0, 1], [list(range(0, m, 2)), [], list(range(1, m, 2))]


def prepare(cols, parent, owners):
    children = [[] for _ in parent]
    subtree = [set(x) for x in owners]
    for v in range(1, len(parent)):
        children[parent[v]].append(v)
    for v in range(len(parent) - 1, 0, -1):
        subtree[parent[v]].update(subtree[v])
    allcoords = set(range(len(cols)))
    states = [{0}]
    widths = [0]
    for v in range(1, len(parent)):
        state = span(cols[i] for i in subtree[v]) & span(cols[i] for i in allcoords - subtree[v])
        states.append(state)
        widths.append(len(state).bit_length() - 1)
    degrees = [len(owners[v]) + widths[v] + sum(widths[c] for c in children[v]) for v in range(len(parent))]
    return children, subtree, states, widths, degrees


def contract(cols, word, owners, children, states):
    # Exact integer contraction by messages, summing every allowed bond label.
    messages = [{} for _ in owners]
    for v in range(len(owners) - 1, -1, -1):
        local = 0
        for j in owners[v]:
            if word >> j & 1:
                local ^= cols[j]
        accum = {local: 1}
        for child in children[v]:
            updated = {}
            for x, a in accum.items():
                for y, b in messages[child].items():
                    updated[x ^ y] = updated.get(x ^ y, 0) + a * b
            accum = updated
        messages[v] = {x: accum.get(x, 0) for x in states[v]}
    return messages[0][0]


def separator(parent, owners, D):
    remaining = [len(x) for x in owners]
    selected = set()
    for v in range(len(parent) - 1, -1, -1):
        if remaining[v] >= D:
            selected.add(v)
        elif parent[v] >= 0:
            remaining[parent[v]] += remaining[v]
    return selected


def components(parent, selected):
    adjacent = [set() for _ in parent]
    for v in range(1, len(parent)):
        adjacent[v].add(parent[v])
        adjacent[parent[v]].add(v)
    unseen = set(range(len(parent))) - selected
    result = []
    while unseen:
        seed = unseen.pop()
        component, stack = {seed}, [seed]
        while stack:
            for child in adjacent[stack.pop()] & unseen:
                unseen.remove(child)
                component.add(child)
                stack.append(child)
        result.append(component)
    return result


def check_case(cols, parent, owners, counters, full):
    m = len(cols)
    assert sorted(j for block in owners for j in block) == list(range(m))
    children, subtree, states, widths, degrees = prepare(cols, parent, owners)
    words = [z for z in range(1 << m) if syndrome(cols, z) == 0]
    k = len(words).bit_length() - 1
    D = min((z.bit_count() for z in words if z), default=m + 1)
    if full:
        for word in range(1 << m):
            assert contract(cols, word, owners, children, states) == int(word in words)
            counters['integer_contractions'] += 1
        for v in range(1, len(parent)):
            left = sorted(subtree[v])
            right = sorted(set(range(m)) - subtree[v])
            rows = [syndrome([cols[j] for j in left], x) for x in range(1 << len(left))]
            columns = [syndrome([cols[j] for j in right], x) for x in range(1 << len(right))]
            mat = [[int(x == y) for y in columns] for x in rows]
            for p in (2, 3):
                assert rank_mod(mat, p) == 1 << widths[v]
                counters['field_cut_ranks'] += 1
    for distance in range(1, D + 1):
        chosen = separator(parent, owners, distance)
        assert len(chosen) * distance <= m
        assert all(sum(len(owners[v]) for v in comp) < distance for comp in components(parent, chosen))
        assert k <= sum(degrees[v] for v in chosen)
        if k:
            assert k <= (m // distance) * max(degrees)
        # Independent direct injectivity of the selected input/syndrome map.
        incident = [v for v in range(1, len(parent)) if v in chosen or parent[v] in chosen]
        selectedcoords = sorted(j for v in chosen for j in owners[v])
        images = set()
        for word in words:
            inputs = tuple(word >> j & 1 for j in selectedcoords)
            syndromes = tuple(syndrome(cols, word & sum(1 << j for j in subtree[v])) for v in incident)
            images.add((inputs, syndromes))
        assert len(images) == len(words)
        counters['separator_and_injectivity_checks'] += 1
    counters['matrix_layout_cases'] += 1


def main():
    counts = dict(matrix_layout_cases=0, integer_contractions=0, field_cut_ranks=0,
                  separator_and_injectivity_checks=0)
    for m in range(1, 5):
        for cols in itertools.product(range(4), repeat=m):
            for parent, owners in layouts(m):
                check_case(cols, parent, owners, counts, True)
    rng = random.Random(14920261028)
    for m in range(5, 9):
        for iteration in range(100):
            cols = [rng.randrange(8) for _ in range(m)]
            vcount = rng.randrange(1, m + 4)
            parent = [-1] + [rng.randrange(v) for v in range(1, vcount)]
            owners = [[] for _ in parent]
            for j in range(m):
                owners[rng.randrange(vcount)].append(j)
            check_case(cols, parent, owners, counts, iteration < 10)
    controls = []
    for m in range(2, 13):
        # Repetition code: distance m, dimension one; degree stays at most 3.
        cols = [1 << j for j in range(m - 1)] + [(1 << (m - 1)) - 1]
        parent, owners = list(layouts(m))[2]
        children, subtree, states, widths, degrees = prepare(cols, parent, owners)
        assert max(degrees) <= 3
        assert len([z for z in range(1 << m) if syndrome(cols, z) == 0]) == 2
        controls.append(dict(m=m, k=1, D=m, max_degree=max(degrees)))
    # Restricted input image destroys the generic cut-rank obstruction.
    cols = [1, 1]
    restricted = [int(syndrome(cols, x | x << 1) == 0) for x in (0, 1)]
    assert restricted == [1, 1]
    # An additional exact Hamming-code parameter fixture.
    cols = list(range(1, 16))
    words = [z for z in range(1 << 15) if syndrome(cols, z) == 0]
    assert len(words) == 1 << 11 and min(z.bit_count() for z in words if z) == 3
    tree_lower = (11 + 5 - 1) // 5
    assert tree_lower == 3
    root = Path(__file__).resolve().parent
    report = {
        'status': 'bounded_checks_passed',
        'seed': 14920261028,
        'exhaustive_scope': 'All 2-row binary matrices with 1..4 columns; five tree/input layouts each.',
        'seeded_scope': '400 matrices with 3 rows and 5..8 columns, random grouped-input trees; 40 full contractions/rank replays.',
        'counts': counts,
        'low_nullity_controls': controls,
        'restricted_pattern_control': restricted,
        'hamming_parameters': {'m': 15, 'k': 11, 'D': 3, 'tree_degree_lower_bound': tree_lower},
        'sha256': {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in ('verify.py', 'PROOF.md')},
        'limits': 'Finite algebra/representation checks only; no SAT algorithm, asymptotic benchmark or independent proof review.'
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
