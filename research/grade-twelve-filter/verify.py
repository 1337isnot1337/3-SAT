"""Exact finite no-filter certificate for deterministic grade-twelve codebooks."""
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


def modular_rank(rows, prime):
    pivots = {}
    for row in rows:
        vec = [x % prime for x in row]
        for p in sorted(pivots):
            if vec[p]:
                scale = vec[p]
                vec = [(a - scale*b) % prime for a, b in zip(vec, pivots[p])]
        p = next((i for i, x in enumerate(vec) if x), None)
        if p is not None:
            inv = pow(vec[p], -1, prime)
            pivots[p] = [(x*inv) % prime for x in vec]
    return len(pivots)


def exact_rank_one(rows):
    pivot = next(((i, j) for i, row in enumerate(rows) for j, x in enumerate(row) if x), None)
    if pivot is None:
        return False
    i, j = pivot
    return all(rows[r][c]*rows[i][j] == rows[r][j]*rows[i][c]
               for r in range(len(rows)) for c in range(len(rows[0])))


def equations(data, requests, shifts):
    result = []
    for x, v, ys in requests:
        for y in ys:
            vectors = [dict(model.charged.piece_vector(data['row_labels'][x], data['column_labels'][v],
                                                       data['output_labels'][y], s, 1, reverse=(s < 0)))
                       for s in shifts]
            for u, output in enumerate(data['output_labels']):
                if u != y:
                    result.append([values.get(output, 0) for values in vectors])
        model.charged.operator.cache_clear()
        model.charged.dual_operator.cache_clear()
    return result


def matrix_hash(rows):
    return sha256(json.dumps(rows, separators=(',', ':')).encode()).hexdigest()


def main():
    data = model.construct(4)
    if (data['h'], data['N']) != (12, 16):
        raise ValueError('Grade selection changed')
    shifts = [s for s in range(-24, 25) if abs(s) >= 2]
    edge = list(range(-24, -17)) + [22, 23, 24]
    inner = [s for s in shifts if s not in edge]
    requests = [(15, 15, [15, 14, 13, 12]), (14, 15, [15, 14, 13, 12]),
                (15, 14, [15, 14, 13, 12]), (13, 15, [15, 14, 13, 12]),
                (15, 13, [15, 14, 13, 12]), (11, 15, [15]),
                (15, 12, [15, 14]), (10, 15, [15])]
    first = equations(data, requests, shifts)
    edge_block = [[row[shifts.index(s)] for s in edge] for row in first]
    inner_block = [[row[shifts.index(s)] for s in inner] for row in first]
    if len(first) != 360 or not exact_rank_one(edge_block):
        raise ValueError('First edge block does not have rational rank one')
    if modular_rank(inner_block, 65537) != 36 or modular_rank(first, 65537) != 37:
        raise ValueError('First block does not separate the middle and edge spans')
    second = equations(data, [(0, 0, [15]), (0, 1, [15])], edge)
    if len(second) != 30 or modular_rank(edge_block + second, 65537) != 10:
        raise ValueError('Edge constraints do not have full column rank')
    print(json.dumps({'status': 'PASS', 'h': 12, 'N': 16, 'charge': 1, 'prime': 65537,
                      'excluded_shifts': [-1, 0, 1], 'first_requests': requests,
                      'first_matrix_shape': [len(first), len(shifts)], 'first_matrix_sha256': matrix_hash(first),
                      'first_rank_mod_prime': 37, 'first_inner_rank_mod_prime': 36,
                      'first_edge_shifts': edge, 'first_edge_exact_rational_rank': 1,
                      'second_requests': [[0, 0, [15]], [0, 1, [15]]],
                      'second_matrix_shape': [len(second), len(edge)], 'second_matrix_sha256': matrix_hash(second),
                      'combined_edge_rank_mod_prime': 10,
                      'conclusion': 'The full rational scalarity system has only zero weight with shifts -1,0,1 excluded.',
                      'predecessor_model_sha256': sha256(MODEL.read_bytes()).hexdigest()}, indent=2))


if __name__ == '__main__':
    main()
