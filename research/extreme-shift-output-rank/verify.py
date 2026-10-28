"""Finite exact checks for the extreme-shift output-rank bound."""
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


def operator_matrix(data, x, v, shift, reverse):
    n = data['N']
    columns = [dict(model.charged.piece_vector(data['row_labels'][x], data['column_labels'][v],
                                              arg, shift, 1, reverse=reverse))
               for arg in data['output_labels']]
    return [[columns[y].get(data['output_labels'][u], 0) for y in range(n)] for u in range(n)]


def budget(h, shift):
    t = 2*h-abs(shift)
    return sum(model.partition_count(k) for k in range(max(0, t-2*h), t+1))


def main():
    profiles = []
    for bits in (1, 2):
        data = model.construct(bits)
        n, h = data['N'], data['h']
        shifts = [-2*h, -2*h+1, -2*h+2, 0, 2*h-2, 2*h-1, 2*h]
        count = 0
        endpoint_scalar_checks = 0
        maximum = 0
        for x in (0, n-1):
            for v in (0, n-1):
                matrices = {}
                for shift in shifts:
                    mat = operator_matrix(data, x, v, shift, reverse=(shift < 0))
                    reverse = operator_matrix(data, x, v, shift, reverse=not (shift < 0))
                    if mat != reverse:
                        raise ValueError('Two operator orders disagree')
                    rank = model.predecessor.exact_rank(mat)
                    if rank > budget(h, shift):
                        raise ValueError('Rank exceeds intermediate-space bound')
                    matrices[shift] = mat
                    maximum = max(maximum, rank)
                    count += 1
                # For N>2, two endpoint operators have total rank at most 2<N.
                # Enumerate integer weights to check the scalar-zero consequence.
                if n > 2:
                    a, b = matrices[-2*h], matrices[2*h]
                    for wa in range(-2, 3):
                        for wb in range(-2, 3):
                            mat = [[wa*a[i][j]+wb*b[i][j] for j in range(n)] for i in range(n)]
                            scalar = all(mat[i][j] == (mat[0][0] if i == j else 0)
                                         for i in range(n) for j in range(n))
                            if scalar and mat[0][0] != 0:
                                raise ValueError('Nonzero scalar below rank threshold')
                            endpoint_scalar_checks += 1
        profiles.append({'bits': bits, 'h': h, 'N': n, 'fixed_label_pairs': 4,
                         'shifts': shifts, 'two_order_and_rank_checks': count,
                         'max_observed_compressed_rank': maximum,
                         'endpoint_pair_budget': budget(h,-2*h)+budget(h,2*h),
                         'endpoint_scalar_weight_checks': endpoint_scalar_checks})
        model.charged.operator.cache_clear()
        model.charged.dual_operator.cache_clear()
    print(json.dumps({'status': 'PASS', 'scope': 'finite fixed-label compressed operator controls; all-size argument is in PROOF.md',
                      'profiles': profiles, 'model_sha256': sha256(MODEL.read_bytes()).hexdigest()}, indent=2))


if __name__ == '__main__':
    main()
