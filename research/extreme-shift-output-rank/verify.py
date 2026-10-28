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


def unequal_energy_controls():
    data = model.construct(1)
    h = data['h']
    profiles = []
    for energy in (0, 1, 3, 5):
        states = model.predecessor.partitions(energy)
        checked = 0
        for charge in (1, 2):
            for shift in sorted({-energy-h, -energy-h+1, 0, energy+h-1, energy+h}):
                columns = []
                for arg in states:
                    args = (data['row_labels'][0], data['column_labels'][0], arg, shift, charge)
                    result = model.charged.piece_vector(*args, reverse=(shift < 0))
                    if result != model.charged.piece_vector(*args, reverse=not (shift < 0)):
                        raise ValueError('Unequal-energy operator orders disagree')
                    columns.append(dict(result))
                mat = [[columns[y].get(out, 0) for y in range(len(states))] for out in states]
                t = energy+h-abs(shift)
                upper = sum(model.partition_count(k) for k in range(max(0, t-2*h), t+1))
                if model.predecessor.exact_rank(mat) > upper:
                    raise ValueError('Unequal-energy rank exceeds bound')
                checked += 1
        profiles.append({'h': h, 'E': energy, 'output_dimension': len(states),
                         'charges': [1, 2], 'two_order_and_rank_checks': checked})
        model.charged.operator.cache_clear()
        model.charged.dual_operator.cache_clear()
    return profiles


def main():
    profiles = []
    for bits in (1, 2):
        data = model.construct(bits)
        n, h = data['N'], data['h']
        shifts = [-2*h, -2*h+1, -2*h+2, 0, 2*h-2, 2*h-1, 2*h]
        count = 0
        endpoint_scalar_checks = 0
        maximum = 0
        all_matrices = {}
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
                    all_matrices[(x, v, shift)] = mat
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
        # A separable mixture of two row and two column labels remains one
        # piece by bilinearity; its rank is bounded by K, not four times K.
        mixed_checks = 0
        for shift in shifts:
            mat = [[sum(all_matrices[(x, v, shift)][u][y]
                        for x in (0, n-1) for v in (0, n-1))
                    for y in range(n)] for u in range(n)]
            if model.predecessor.exact_rank(mat) > budget(h, shift):
                raise ValueError('Separable label mixture exceeds single-piece bound')
            mixed_checks += 1
        central_ranks = []
        for shift in range(-h, h+1):
            max_rank = max(model.predecessor.exact_rank(operator_matrix(data, x, v, shift, shift < 0))
                           for x in (0, n-1) for v in (0, n-1))
            if max_rank != n:
                raise ValueError('Registered central full-rank control changed')
            central_ranks.append({'shift': shift, 'maximum_rank': max_rank})
        profiles.append({'bits': bits, 'h': h, 'N': n, 'fixed_label_pairs': 4,
                         'shifts': shifts, 'two_order_and_rank_checks': count,
                         'separable_label_mixture_checks': mixed_checks,
                         'central_full_rank_controls': central_ranks,
                         'max_observed_compressed_rank': maximum,
                         'endpoint_pair_budget': budget(h,-2*h)+budget(h,2*h),
                         'endpoint_scalar_weight_checks': endpoint_scalar_checks})
        model.charged.operator.cache_clear()
        model.charged.dual_operator.cache_clear()
    print(json.dumps({'status': 'PASS', 'scope': 'finite fixed-label compressed operator controls; all-size argument is in PROOF.md',
                      'profiles': profiles, 'unequal_energy_controls': unequal_energy_controls(),
                      'model_sha256': sha256(MODEL.read_bytes()).hexdigest()}, indent=2))


if __name__ == '__main__':
    main()
