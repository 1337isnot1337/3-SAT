"""Replay the frozen four-macro dual independently of its search."""
from collections import defaultdict
from hashlib import sha256
import importlib.util
import json
from math import factorial, prod
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
reference = ROOT / 'research/three-bit-macro-walsh/schemes.py'
spec = importlib.util.spec_from_file_location('f8_predecessor', reference)
scheme = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scheme)
labels = [(a, b) for a in range(8) for b in range(8)]
dual = {b: next(B for B in range(8) if all(
    scheme.trace(scheme.multiply(a, B)) == ((a & b).bit_count() % 2) for a in range(8)))
        for b in range(8)}


def cls(a, b):
    B = dual[b]
    if not a and not B:
        return 0
    if not a:
        return 1
    if not B:
        return 2
    return 2 + scheme.multiply(a, B)


classes = {ab: cls(*ab) for ab in labels}
weights = [sum(i == c for c in classes.values()) for i in range(10)]
assert weights == [1] + [7] * 9
C = []
for i in range(10):
    rows = []
    for c, d in labels:
        if classes[c, d] == i:
            rows.append([sum((-1) ** (((b & c).bit_count() + (a & d).bit_count()) % 2)
                             for a, b in labels if classes[a, b] == j) for j in range(10)])
    assert all(row == rows[0] for row in rows)
    C.append(rows[0])
assert all(sum(C[i][k] * C[k][j] for k in range(10)) == 64 * (i == j)
           for i in range(10) for j in range(10))
q = [1, 1, 1] + [(-1) ** scheme.trace(x) for x in range(1, 8)]
assert all(q[classes[a, b]] == (-1) ** ((a & b).bit_count() % 2) for a, b in labels)
assert [sum(x * y for x, y in zip(row, q)) for row in C] == [8 * x for x in q]
frobenius = [0, 1, 2] + [2 + scheme.multiply(x, x) for x in range(1, 8)]
swap = [0, 2, 1] + list(range(3, 10))


def permute(alpha, permutation):
    out = [0] * 10
    for i, count in enumerate(alpha):
        out[permutation[i]] = count
    return tuple(out)


def orbit(alpha):
    found, todo = {alpha}, [alpha]
    while todo:
        v = todo.pop()
        for p in (frobenius, swap):
            w = permute(v, p)
            if w not in found:
                found.add(w)
                todo.append(w)
    return found


def transform_monomial(alpha):
    terms = {(0,) * 10: 1}
    for row, count in zip(C, alpha):
        for _ in range(count):
            updated = defaultdict(int)
            for powers, value in terms.items():
                for j, coefficient in enumerate(row):
                    if coefficient:
                        new = list(powers)
                        new[j] += 1
                        updated[tuple(new)] += value * coefficient
            terms = updated
    return terms


seed = json.loads((HERE / 'seed.json').read_text())['terms']
assert len(seed) == 48
P = {}
for term in seed:
    a, coefficient = tuple(term['type']), term['coefficient']
    assert len(a) == 10 and sum(a) == 4 and isinstance(coefficient, int) and coefficient
    for b in orbit(a):
        assert b not in P
        P[b] = coefficient
assert all(a[0] == 0 and max(a) <= 2 and sum(x == 2 for x in a) <= 1 for a in P)
transformed = defaultdict(int)
for alpha, coefficient in P.items():
    for beta, value in transform_monomial(alpha).items():
        transformed[beta] += coefficient * value
transformed = {a: x for a, x in transformed.items() if x}
assert transformed == {a: 8 ** 4 * x for a, x in P.items()}
pairing = sum(x * prod(y ** a for y, a in zip(q, alpha)) for alpha, x in P.items())
assert pairing == 192
profiles = sorted({tuple(sorted((x for x in a if x), reverse=True)) for a in P})
assert profiles == [(1, 1, 1, 1), (2, 1, 1)]
entropy_min_power = 4 ** 4 * 7 ** 4 // 4
assert entropy_min_power == 153664 and entropy_min_power > 2 ** 17 and 17 ** 2 > 288

# Directly check the entropy claim on the nonzero two-seed polynomial.
power = defaultdict(int)
for a, x in P.items():
    for b, y in P.items():
        power[tuple(i + j for i, j in zip(a, b))] += x * y
power = {a: x for a, x in power.items() if x}
assert sum(x * prod(y ** a for y, a in zip(q, alpha)) for alpha, x in power.items()) == pairing ** 2
assert all(8 ** 8 * 7 ** (8 - a[0]) >= 153664 ** 2 * prod(x ** x for x in a if x)
           for a in power)

# Wrong normalization is a negative control for the weighted polynomial.
wrong = defaultdict(int)
for alpha, coefficient in P.items():
    size = factorial(4) * 7 ** 4 // prod(factorial(x) for x in alpha)
    for beta, value in transform_monomial(alpha).items():
        wrong[beta] += size * coefficient * value
assert {a: x for a, x in wrong.items() if x} != {a: 8 ** 4 * (factorial(4) * 7 ** 4 // prod(factorial(x) for x in a)) * x for a, x in P.items()}

files = [HERE / 'verify.py', HERE / 'seed.json', reference]
print(json.dumps({'status': 'PASS', 'scope': 'frozen four-macro integer dual and entropy profiles',
                  'seed_orbits': len(seed), 'nonzero_types': len(P), 'pairing': pairing,
                  'two_seed_nonzero_types': len(power),
                  'minimum_entropy_fourth_power': entropy_min_power,
                  'bindings': {str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest() for path in files}}, indent=2))
