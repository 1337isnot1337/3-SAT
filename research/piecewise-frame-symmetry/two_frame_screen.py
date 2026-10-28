"""R=2 screen of a fixed adapted-basis alphabet in one or two frames."""
from collections import defaultdict
from contextlib import redirect_stdout
from hashlib import sha256
import importlib.util
import io
import json
from math import factorial, prod
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('frame_control', HERE / 'verify.py')
frame = importlib.util.module_from_spec(spec)
with redirect_stdout(io.StringIO()):
    spec.loader.exec_module(frame)
ref = ROOT / 'research/symmetric-walsh-pieces/walsh.py'
spec = importlib.util.spec_from_file_location('adapted', ref)
adapted = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapted)


def compositions(n, k):
    if k == 1:
        yield (n,)
    else:
        for i in range(n + 1):
            for tail in compositions(n - i, k - 1):
                yield (i,) + tail


def size(a):
    return factorial(sum(a)) * 7 ** (sum(a) - a[0]) // prod(factorial(x) for x in a)


def cls(a, b):
    B = frame.d[b]
    if not a and not B:
        return 0
    if not a:
        return 1
    if not B:
        return 2
    return 2 + frame.f.multiply(a, B)


labels = [(a, b) for a in range(8) for b in range(8)]
C = []
for i in range(10):
    rows = [[sum((-1) ** (((b & c).bit_count() + (a & d).bit_count()) % 2)
                 for a, b in labels if cls(a, b) == j) for j in range(10)]
            for c, d in labels if cls(c, d) == i]
    assert all(row == rows[0] for row in rows)
    C.append(rows[0])


def transform(alpha):
    result = {(0,) * 10: 1}
    for row, count in zip(C, alpha):
        for _ in range(count):
            out = defaultdict(int)
            for powers, value in result.items():
                for i, entry in enumerate(row):
                    if entry:
                        v = list(powers)
                        v[i] += 1
                        out[tuple(v)] += entry * value
            result = out
    return result


types = sorted(compositions(2, 10), key=lambda a: (size(a), a))
weights = list(map(size, types))
lookup = {a: i for i, a in enumerate(types)}
T = [[transform(beta).get(alpha, 0) for alpha in types] for beta in types]
vectors, images, _ = adapted.adapted_basis(T)
costs = []
for v, image in zip(vectors, images):
    row = sum(w for w, x in zip(weights, v) if x)
    col = sum(w for w, x in zip(weights, image) if x)
    costs.append((row - 1).bit_length() + (col - 1).bit_length())
prime = 65521
assert all(prime % k for k in range(2, 256))
values = [[(x.numerator % prime) * pow(x.denominator % prime, -1, prime) % prime for x in v]
          for v in vectors]


def kind(x):
    result = [0] * 10
    for j in range(2):
        z = (x >> (6 * j)) & 63
        result[cls(z >> 3, z & 7)] += 1
    return lookup[tuple(result)]


pairs = sorted({(kind(x), kind(frame.frame(x))) for x in range(4096)})
q = [prod(((-1) ** frame.f.trace(i - 2) if i >= 3 else 1) ** a
          for i, a in enumerate(t)) for t in types]
assert all(q[i] == q[j] for i, j in pairs)


def rank(rows):
    basis = {}
    for row in rows:
        v = [x % prime for x in row]
        for pivot, r in basis.items():
            if v[pivot]:
                factor = v[pivot]
                v = [(x - factor * y) % prime for x, y in zip(v, r)]
        pivot = next((i for i, x in enumerate(v) if x), None)
        if pivot is not None:
            inverse = pow(v[pivot], -1, prime)
            basis[pivot] = [x * inverse % prime for x in v]
    return len(basis)


def screen(threshold, two_frames):
    selected = [i for i, cost in enumerate(costs) if cost <= threshold]
    rows = []
    for a, b in pairs:
        row = [values[i][a] for i in selected]
        if two_frames:
            row += [values[i][b] for i in selected]
        rows.append(row)
    r = rank(rows)
    augmented = rank([row + [q[a]] for row, (a, _) in zip(rows, pairs)])
    return {'threshold_bits': threshold, 'two_frames': two_frames,
            'basis_atoms_per_frame': len(selected), 'rank': r, 'augmented_rank': augmented}


checks = [screen(t, two) for t in (20, 21) for two in (False, True)]
assert all(x['augmented_rank'] == x['rank'] + 1 for x in checks[:2])
assert all(x['augmented_rank'] == x['rank'] for x in checks[2:])
assert checks[0]['basis_atoms_per_frame'] == 48 and checks[2]['basis_atoms_per_frame'] == 55

# Four exact, independent dependencies bound the rational two-frame rank
# from above by 92. Together with modular rank 92 this certifies that the
# augmented modular rank 93 really excludes rational decompositions.
selected = [i for i, cost in enumerate(costs) if cost <= 20]
relations = [{0: -1, 48: 1}, {17: -1, 65: 1},
             {9: -1, 18: -1, 57: 1, 66: 1}, {47: -1, 95: 1}]
free_columns = [48, 65, 66, 95]
assert all(relation.get(column, 0) == (1 if i == j else 0)
           for i, relation in enumerate(relations) for j, column in enumerate(free_columns))
for a, b in pairs:
    row = [vectors[i][a] for i in selected] + [vectors[i][b] for i in selected]
    assert all(sum(row[i] * coefficient for i, coefficient in relation.items()) == 0
               for relation in relations)
# At 21 bits all 55 triangular adapted-basis vectors are included, so the
# original-frame target has an exact rational expansion.
assert len(vectors) == 55 and all(cost <= 21 for cost in costs)

files = [HERE / 'two_frame_screen.py', HERE / 'verify.py', ref,
         ROOT / 'research/three-bit-macro-walsh/schemes.py']
print(json.dumps({'status': 'PASS', 'scope': 'two-macro fixed adapted-basis atom alphabet',
                  'type_pairs': len(pairs), 'prime': prime, 'exact_independent_dependencies': len(relations),
                  'checks': checks,
                  'bindings': {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in files}}, indent=2))
