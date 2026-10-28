"""A bounded one-sided modular certificate for grade-nine scalarity."""
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODEL = HERE.parent / 'charged-asymmetric-crossing' / 'model.py'
if sha256(MODEL.read_bytes()).hexdigest() != '7f495836772409f6c705642040f6b5a4307532539037c7d28bed1bdf66fd6fef':
    raise ValueError('Pinned asymmetric model changed')
spec = importlib.util.spec_from_file_location('asymmetric_model', MODEL)
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)


def main():
    data = model.construct(3)
    n, h, prime = data['N'], data['h'], 65537
    if (n, h) != (8, 9):
        raise ValueError('Changed deterministic grade or dimension')
    shifts = [s for s in range(-2*h, 2*h+1) if abs(s) >= 2]
    pivots, rows = {}, []

    def add(row):
        rows.append(row)
        vec = [x % prime for x in row]
        for p in sorted(pivots):
            if vec[p]:
                scale = vec[p]
                vec = [(a - scale*b) % prime for a, b in zip(vec, pivots[p])]
        p = next((i for i, x in enumerate(vec) if x), None)
        if p is not None:
            inv = pow(vec[p], -1, prime)
            pivots[p] = [(x*inv) % prime for x in vec]

    pairs = [(7, 7), (6, 7), (5, 7), (4, 7), (7, 5)]
    for x, v in pairs:
        mu, nu = data['row_labels'][x], data['column_labels'][v]
        diag0 = None
        for y in reversed(range(n)):
            vectors = [dict(model.charged.piece_vector(mu, nu, data['output_labels'][y], s, 1)) for s in shifts]
            for u, output in enumerate(data['output_labels']):
                row = [values.get(output, 0) for values in vectors]
                if u != y:
                    add(row)
                elif y == n-1:
                    diag0 = row
                else:
                    add([a-b for a, b in zip(row, diag0)])
        model.charged.operator.cache_clear()
        model.charged.dual_operator.cache_clear()
    if len(pivots) != 26:
        raise ValueError('Certificate rank changed')
    digest = sha256(json.dumps(rows, separators=(',', ':')).encode()).hexdigest()
    print(json.dumps({'scope': 'necessary scalarity equations for five input-label pairs at h=9, N=8, charge=1; shifts -1,0,1 excluded',
                      'input_pairs': pairs, 'remaining_shifts': shifts, 'constraint_rows': len(rows),
                      'prime': prime, 'modular_rank': len(pivots),
                      'pivot_shifts': [shifts[i] for i in sorted(pivots)],
                      'rational_solution_dimension_at_most': len(shifts)-len(pivots),
                      'integer_matrix_sha256': digest}, indent=2))


if __name__ == '__main__':
    main()
