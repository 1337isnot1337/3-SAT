"""Exact counterexample to permutation-triangularity of one sampled piece."""
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
VERIFIER = HERE / 'verify.py'
spec = importlib.util.spec_from_file_location('rank_controls', VERIFIER)
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)


def main():
    profiles = []
    for bits in (1, 2, 3, 4):
        data = verify.model.construct(bits)
        n, h = data['N'], data['h']
        mat = verify.operator_matrix(data, n-1, n-1, -h, reverse=True)
        upper = [(i, j, mat[i][j]) for i in range(n) for j in range(i+1, n) if mat[i][j]]
        cycles = [(i, j, mat[i][j], mat[j][i]) for i in range(n) for j in range(i+1, n)
                  if mat[i][j] and mat[j][i]]
        if bits < 4 and upper:
            raise ValueError('Registered small-grade triangular control changed')
        if bits == 4 and not cycles:
            raise ValueError('Grade-twelve two-cycle missing')
        profiles.append({'bits': bits, 'h': h, 'N': n, 'shift': -h,
                         'label_pair': [n-1, n-1], 'nonzero_entries_above_diagonal': len(upper),
                         'first_upper_witness': upper[0] if upper else None,
                         'two_cycles': len(cycles), 'first_two_cycle': cycles[0] if cycles else None})
    print(json.dumps({'status': 'PASS', 'scope': 'fixed sampled pieces; simultaneous row/column permutations',
                      'profiles': profiles, 'verifier_sha256': sha256(VERIFIER.read_bytes()).hexdigest()}, indent=2))


if __name__ == '__main__':
    main()
