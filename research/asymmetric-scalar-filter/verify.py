"""Exact scalar-filter linear constraints for the predecessor's fixed codebooks."""
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODEL = HERE.parent / 'charged-asymmetric-crossing' / 'model.py'
EXPECTED = '7f495836772409f6c705642040f6b5a4307532539037c7d28bed1bdf66fd6fef'
if sha256(MODEL.read_bytes()).hexdigest() != EXPECTED:
    raise ValueError('Pinned model changed')
spec = importlib.util.spec_from_file_location('asymmetric_model', MODEL)
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)


def rref(rows, n):
    pivots = {}
    for row in rows:
        row = list(map(F, row))
        for p in sorted(pivots):
            if row[p]:
                scale = row[p]
                row = [a - scale * b for a, b in zip(row, pivots[p])]
        p = next((i for i, x in enumerate(row) if x), None)
        if p is None:
            continue
        scale = row[p]
        row = [x / scale for x in row]
        for q in pivots:
            if pivots[q][p]:
                scale = pivots[q][p]
                pivots[q] = [a - scale * b for a, b in zip(pivots[q], row)]
        pivots[p] = row
    return pivots


def nullspace(rows, n):
    pivots = rref(rows, n)
    basis = []
    for free in range(n):
        if free in pivots:
            continue
        v = [F(0)] * n
        v[free] = 1
        for p, row in pivots.items():
            v[p] = -row[free]
        basis.append(v)
    if len(basis) + len(pivots) != n or any(
        sum(a * b for a, b in zip(row, v)) for row in rows for v in basis
    ):
        raise ValueError('Nullspace certificate failed')
    return basis


def modular_rank(rows, prime):
    """Independent forward elimination gives a lower bound for rational rank."""
    pivots = {}
    for row in rows:
        vec = [(F(x).numerator * pow(F(x).denominator, -1, prime)) % prime for x in row]
        for p in sorted(pivots):
            if vec[p]:
                factor = vec[p]
                vec = [(a - factor * b) % prime for a, b in zip(vec, pivots[p])]
        p = next((i for i, x in enumerate(vec) if x), None)
        if p is not None:
            inv = pow(vec[p], -1, prime)
            pivots[p] = [(x * inv) % prime for x in vec]
    return len(pivots)


def screen(bits):
    data = model.construct(bits)
    n, h = data['N'], data['h']
    shifts = list(range(-2*h, 2*h+1))
    pieces = []
    for s in shifts:
        raw, _, _ = model.piece(data, s)
        pieces.append(raw)
    constraints = []
    for x in range(n):
        for v in range(n):
            for y in range(n):
                for u in range(n):
                    if y != u:
                        constraints.append([p[x][y][u][v] for p in pieces])
                    elif y:
                        constraints.append([p[x][y][y][v] - p[x][0][0][v] for p in pieces])
    full = nullspace(constraints, len(shifts))
    mod_rank = modular_rank(constraints, 65537)
    if mod_rank != len(shifts) - len(full):
        raise ValueError('Independent modular rank does not certify rational rank')
    # Both known moments must satisfy every scalar constraint.
    for power in [0, 1]:
        if any(sum(c * s**power for c, s in zip(row, shifts)) for row in constraints):
            raise ValueError('Known moment is not scalar')
    profiles = []
    for radius in range(0, 2*h+2):
        extra = [[int(i == j) for i in range(len(shifts))]
                 for j, s in enumerate(shifts) if abs(s) < radius]
        basis = nullspace(constraints + extra, len(shifts))
        # A pairing entry is the common output diagonal coefficient.
        pairings = [[[sum(w * p[x][0][0][v] for w, p in zip(vec, pieces))
                      for v in range(n)] for x in range(n)] for vec in basis]
        # A zero span proves no pairing; full-rank basis vectors certify existence.
        ranks = [model.predecessor.exact_rank(matrix) for matrix in pairings]
        profiles.append({'excluded_abs_less_than': radius, 'weight_dimension': len(basis),
                         'pairing_basis_ranks': ranks,
                         'weight_basis': [[str(x) for x in vec] for vec in basis]})
    quadratic = all(all(v[i+3] - 3*v[i+2] + 3*v[i+1] - v[i] == 0
                        for i in range(len(v)-3)) for v in full)
    if bits == 2 and not (len(full) == 3 and quadratic):
        raise ValueError('Grade-six quadratic classification changed')
    return {'bits': bits, 'h': h, 'N': n, 'shifts': shifts,
            'row_labels': data['row_labels'], 'column_labels': data['column_labels'],
            'output_labels': data['output_labels'],
            'constraint_count': len(constraints), 'modular_rank_prime': 65537,
            'modular_rank': mod_rank, 'all_weights_quadratic': quadratic,
            'unrestricted_weight_dimension': len(full),
            'profiles': profiles}


if __name__ == '__main__':
    print(json.dumps({'scope': 'fixed first-moment-selected input labels and first N output partitions; charge=1',
                      'results': [screen(1), screen(2)]}, indent=2))
