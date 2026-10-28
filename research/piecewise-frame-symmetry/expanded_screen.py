"""Exact two-frame screen with adapted, type and Fourier-type atoms."""
from contextlib import redirect_stdout
from fractions import Fraction
from hashlib import sha256
import importlib.util
import io
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('atom_screen', HERE / 'two_frame_screen.py')
base = importlib.util.module_from_spec(spec)
with redirect_stdout(io.StringIO()):
    spec.loader.exec_module(base)

n = len(base.types)
atoms = list(zip(base.vectors, base.images))
for j in range(n):
    vector = [Fraction(int(i == j)) for i in range(n)]
    image = [Fraction(row[j]) for row in base.T]
    atoms.append((vector, image))
    atoms.append((image, [4096 * value for value in vector]))

costs = []
for vector, image in atoms:
    left = sum(w for w, x in zip(base.weights, vector) if x)
    right = sum(w for w, x in zip(base.weights, image) if x)
    costs.append((left - 1).bit_length() + (right - 1).bit_length())
low = [i for i, cost in enumerate(costs) if cost <= 18]
assert len(atoms) == 165 and len(low) == 69
certificate = json.loads((HERE / 'expanded-dual.json').read_text())
terms = certificate['terms']
assert len(terms) == len({row for row, _ in terms}) == 33
assert all(isinstance(row, int) and 0 <= row < len(base.pairs) and isinstance(c, int) and c
           for row, c in terms)
assert sum(c * base.q[base.pairs[row][0]] for row, c in terms) == certificate['target_pairing'] == -16
for i in low:
    vector = atoms[i][0]
    for coordinate in (0, 1):
        assert sum(c * vector[base.pairs[row][coordinate]] for row, c in terms) == 0

# The 19-bit one-frame alphabet spans all 55 rational type coordinates:
# full modular row rank gives the same characteristic-zero rank.
high = [i for i, cost in enumerate(costs) if cost <= 19]
assert len(high) == 146
prime = base.prime
rows = [[atoms[i][0][j].numerator % prime * pow(atoms[i][0][j].denominator % prime, -1, prime) % prime
         for i in high] for j in range(n)]
assert base.rank(rows) == n == 55

files = [HERE / 'expanded_screen.py', HERE / 'expanded-dual.json', HERE / 'two_frame_screen.py',
         HERE / 'verify.py', ROOT / 'research/symmetric-walsh-pieces/walsh.py',
         ROOT / 'research/three-bit-macro-walsh/schemes.py']
print(json.dumps({'status': 'PASS', 'scope': 'two-macro expanded fixed atom alphabet',
                  'atoms': len(atoms), 'atoms_per_frame_through_18_bits': len(low),
                  'annihilator_terms': len(terms), 'target_pairing': certificate['target_pairing'],
                  'atoms_through_19_bits': len(high), 'one_frame_modular_rank': n,
                  'prime': prime,
                  'bindings': {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in files}}, indent=2))
