"""Exact central full-output-rank controls on four fixed codebooks."""
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
        ranks = []
        upper_witnesses = None
        for shift in range(-h, h+1):
            mat = verify.operator_matrix(data, n-1, n-1, shift, reverse=(shift < 0))
            value = verify.model.predecessor.exact_rank(mat)
            if value != n:
                raise ValueError('Full-rank control failed')
            if shift == -h:
                upper_witnesses = [(i, j, mat[i][j]) for i in range(n) for j in range(i+1, n) if mat[i][j]]
            ranks.append({'shift': shift, 'rank': value})
        profiles.append({'bits': bits, 'h': h, 'N': n, 'label_pair': [n-1, n-1], 'ranks': ranks,
                         'upper_nonzero_at_shift_minus_h': len(upper_witnesses),
                         'first_upper_witness': upper_witnesses[0] if upper_witnesses else None})
        verify.model.charged.operator.cache_clear()
        verify.model.charged.dual_operator.cache_clear()
    print(json.dumps({'status': 'PASS', 'scope': 'one fixed input-label pair at each of four grades; no scalarity or all-size claim',
                      'profiles': profiles, 'verifier_sha256': sha256(VERIFIER.read_bytes()).hexdigest()}, indent=2))


if __name__ == '__main__':
    main()
