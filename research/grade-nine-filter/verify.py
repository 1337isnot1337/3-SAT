"""Exact finite no-filter certificate for the fixed grade-nine codebooks."""
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODEL = HERE.parent / 'charged-asymmetric-crossing' / 'model.py'
EARLIER = HERE.parent / 'asymmetric-scalar-filter' / 'grade9-verification.json'
for path, expected in [(MODEL, '7f495836772409f6c705642040f6b5a4307532539037c7d28bed1bdf66fd6fef'),
                       (EARLIER, '28742bb571c3ac58db7c897894a09f28db046b4697f12b306a61eab06494f396')]:
    if sha256(path.read_bytes()).hexdigest() != expected:
        raise ValueError('Pinned predecessor changed: ' + path.name)
spec = importlib.util.spec_from_file_location('asymmetric_model', MODEL)
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)


def rank(rows, prime):
    pivots = {}
    for row in rows:
        vec = [x % prime for x in row]
        for p in sorted(pivots):
            if vec[p]:
                factor = vec[p]
                vec = [(a - factor*b) % prime for a, b in zip(vec, pivots[p])]
        p = next((i for i, x in enumerate(vec) if x), None)
        if p is not None:
            inv = pow(vec[p], -1, prime)
            pivots[p] = [(x*inv) % prime for x in vec]
    return len(pivots)


def equations(data, pairs, shifts, first_y_only=False):
    n = data['N']
    rows = []
    for x, v in pairs:
        diag0 = None
        ys = [n-1] if first_y_only else reversed(range(n))
        for y in ys:
            vectors = [dict(model.charged.piece_vector(data['row_labels'][x], data['column_labels'][v],
                                                       data['output_labels'][y], s, 1, reverse=(s < 0)))
                       for s in shifts]
            for u, output in enumerate(data['output_labels']):
                row = [values.get(output, 0) for values in vectors]
                if u != y:
                    rows.append(row)
                elif y == n-1:
                    diag0 = row
                else:
                    rows.append([a-b for a, b in zip(row, diag0)])
        model.charged.operator.cache_clear()
        model.charged.dual_operator.cache_clear()
    return rows


def matrix_hash(rows):
    return sha256(json.dumps(rows, separators=(',', ':')).encode()).hexdigest()


def main():
    data = model.construct(3)
    if (data['h'], data['N']) != (9, 8):
        raise ValueError('Grade selection changed')
    shifts = [s for s in range(-18, 19) if abs(s) >= 2]
    extremes = [-18, -17, -16, -15, -14, -13, 17, 18]
    middle = [s for s in shifts if s not in extremes]
    first_pairs = [(7, 7), (6, 7), (5, 7), (4, 7), (7, 5)]
    first = equations(data, first_pairs, shifts)
    saved = json.loads(EARLIER.read_text())
    if matrix_hash(first) != saved['integer_matrix_sha256']:
        raise ValueError('Two-order matrix differs from predecessor integer matrix')
    if any(row[shifts.index(s)] for row in first for s in extremes):
        raise ValueError('Extreme columns of first matrix are not zero')
    first_middle = [[row[shifts.index(s)] for s in middle] for row in first]
    if rank(first_middle, 65537) != len(middle):
        raise ValueError('First block does not have full middle-column rank')
    second = equations(data, [(0, 0)], extremes) + equations(data, [(0, 1)], extremes, first_y_only=True)
    if rank(second, 65537) != len(extremes):
        raise ValueError('Extreme scalarity block is not full rank')
    report = {'status': 'PASS', 'h': 9, 'N': 8, 'charge': 1, 'prime': 65537,
              'excluded_shifts': [-1, 0, 1], 'first_pairs': first_pairs,
              'first_matrix_shape': [len(first), len(shifts)], 'first_matrix_sha256': matrix_hash(first),
              'first_middle_rank': len(middle), 'first_extreme_columns_identically_zero': extremes,
              'second_full_pair': [0, 0], 'second_partial_pair': [0, 1],
              'second_partial_output_y': 7, 'second_matrix_shape': [len(second), len(extremes)],
              'second_matrix_sha256': matrix_hash(second), 'second_modular_rank': len(extremes),
              'conclusion': 'The full rational scalarity system has only zero weight with shifts -1,0,1 excluded.',
              'predecessor_model_sha256': sha256(MODEL.read_bytes()).hexdigest(),
              'predecessor_report_sha256': sha256(EARLIER.read_bytes()).hexdigest()}
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
