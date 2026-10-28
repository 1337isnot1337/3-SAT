"""Exact target-threshold exclusion for a fixed two-frame three-macro alphabet."""
from contextlib import redirect_stdout
from fractions import Fraction
from hashlib import sha256
import importlib.util
import io
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('two_macro', HERE / 'two_frame_screen.py')
base = importlib.util.module_from_spec(spec)
with redirect_stdout(io.StringIO()):
    spec.loader.exec_module(base)

types = sorted(base.compositions(3, 10), key=lambda a: (base.size(a), a))
weights = list(map(base.size, types))
lookup = {a: i for i, a in enumerate(types)}
T = []
for beta in types:
    row = base.transform(beta)
    T.append([row.get(alpha, 0) for alpha in types])
vectors, images, _ = base.adapted.adapted_basis(T)
n = len(types)
assert n == 220
atoms = list(zip(vectors, images))
for j in range(n):
    vector = [Fraction(int(i == j)) for i in range(n)]
    image = [Fraction(row[j]) for row in T]
    atoms.append((vector, image))
    atoms.append((image, [64 ** 3 * x for x in vector]))

costs = []
for vector, image in atoms:
    left = sum(w for w, x in zip(weights, vector) if x)
    right = sum(w for w, x in zip(weights, image) if x)
    costs.append((left - 1).bit_length() + (right - 1).bit_length())
selected = [i for i, cost in enumerate(costs) if cost <= 25]
assert len(atoms) == 660 and len(selected) == 65


def kind(x):
    result = [0] * 10
    for j in range(3):
        z = (x >> (6 * j)) & 63
        result[base.cls(z >> 3, z & 7)] += 1
    return lookup[tuple(result)]


pairs = sorted({(kind(x), kind(base.frame.frame(x))) for x in range(64 ** 3)})
assert len(pairs) == 7092
q = [base.prod(((-1) ** base.frame.f.trace(i - 2) if i >= 3 else 1) ** a
               for i, a in enumerate(t)) for t in types]
assert all(q[a] == q[b] for a, b in pairs)
certificate = json.loads((HERE / 'three-frame-dual.json').read_text())
terms = certificate['terms']
assert len(terms) == len({row for row, _ in terms}) == 33
assert all(isinstance(row, int) and 0 <= row < len(pairs) and isinstance(c, int) and c
           for row, c in terms)
assert sum(c * q[pairs[row][0]] for row, c in terms) == certificate['target_pairing'] == -240
for i in selected:
    vector = atoms[i][0]
    for coordinate in (0, 1):
        assert sum(c * vector[pairs[row][coordinate]] for row, c in terms) == 0

files = [HERE / 'three_frame_screen.py', HERE / 'three-frame-dual.json', HERE / 'two_frame_screen.py',
         HERE / 'verify.py', ROOT / 'research/symmetric-walsh-pieces/walsh.py',
         ROOT / 'research/three-bit-macro-walsh/schemes.py']
print(json.dumps({'status': 'PASS', 'scope': 'three-macro expanded fixed atom alphabet',
                  'atoms': len(atoms), 'atoms_per_frame_through_25_bits': len(selected),
                  'type_pairs': len(pairs), 'annihilator_terms': len(terms), 'target_pairing': -240,
                  'bindings': {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in files}}, indent=2))
