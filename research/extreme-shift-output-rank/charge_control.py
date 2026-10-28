"""Finite controls for dependence of sampled output ranks on charge."""
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
    for bits in (1, 2, 3):
        data = verify.model.construct(bits)
        n, h = data['N'], data['h']
        profiles_at_h = []
        for charge in (0, 1, 2):
            for shift in (-h, 0, h):
                cols = [dict(verify.model.charged.piece_vector(data['row_labels'][-1], data['column_labels'][-1],
                                                               arg, shift, charge, reverse=(shift < 0)))
                        for arg in data['output_labels']]
                mat = [[cols[j].get(out, 0) for j in range(n)] for out in data['output_labels']]
                value = verify.model.predecessor.exact_rank(mat)
                if charge == 0 and shift == -h and value >= n:
                    raise ValueError('Zero-charge rank-loss control changed')
                if charge in (1, 2) and value != n:
                    raise ValueError('Nonzero-charge full-rank control changed')
                profiles_at_h.append({'charge': charge, 'shift': shift, 'rank': value})
        profiles.append({'h': h, 'N': n, 'label_pair': [n-1, n-1], 'ranks': profiles_at_h})
        verify.model.charged.operator.cache_clear()
        verify.model.charged.dual_operator.cache_clear()
    print(json.dumps({'status': 'PASS', 'scope': 'three grades and three charges; no all-size charge classification',
                      'profiles': profiles, 'verifier_sha256': sha256(VERIFIER.read_bytes()).hexdigest()}, indent=2))


if __name__ == '__main__':
    main()
