"""Replay the frozen four-macro dual independently of its search."""
from collections import defaultdict
from hashlib import sha256
import importlib.util
import json
from itertools import combinations
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

# A strictly larger four-macro entropy floor permits only four distinct
# nonzero classes. Eliminate the invariant system exactly modulo a prime.
distinct = {tuple(int(i in choice) for i in range(10))
            for choice in combinations(range(1, 10), 4)}
distinct_orbits = []
while distinct:
    a = min(distinct)
    group = orbit(a)
    assert group <= distinct
    distinct_orbits.append(group)
    distinct.difference_update(group)
assert len(distinct_orbits) == 33
columns = []
for group in distinct_orbits:
    column = defaultdict(int)
    for alpha in group:
        for beta, value in transform_monomial(alpha).items():
            column[beta] += value
        column[alpha] -= 8 ** 4
    columns.append(column)
rows = sorted(set().union(*(column.keys() for column in columns)))
prime = 65521
assert all(prime % k for k in range(2, 256))
basis = {}
for row in rows:
    v = [column.get(row, 0) % prime for column in columns]
    for pivot, r in basis.items():
        if v[pivot]:
            factor = v[pivot]
            v = [(x - factor * y) % prime for x, y in zip(v, r)]
    pivot = next((i for i, x in enumerate(v) if x), None)
    if pivot is not None:
        inverse = pow(v[pivot], -1, prime)
        basis[pivot] = [x * inverse % prime for x in v]
assert len(basis) == len(distinct_orbits)

# A nonlocal quadratic-isometric relabeling on two three-bit macros.
# The controlled-X uses bit 0 of one macro and bit 3 of the other.
def relabel(a, b):
    return a ^ ((a & 1) << 3), b ^ ((b >> 3) & 1)


def sign(a, b):
    return (-1) ** ((a & b).bit_count() % 2)


def sample_function(a, b):
    return (17 * a + 29 * b) % 7 - 3


for a in range(64):
    for b in range(64):
        aa, bb = relabel(a, b)
        assert sign(a, b) == sign(aa, bb)
        assert relabel(aa, bb) == (a, b)
for x, y in ((0, 0), (1, 8), (7, 19), (63, 47), (40, 3)):
    lx, ly = relabel(x, y)
    pulled_hat = sum(sample_function(*relabel(a, b)) * sign(b, x) * sign(a, y)
                     for a in range(64) for b in range(64))
    original_hat = sum(sample_function(a, b) * sign(b, lx) * sign(a, ly)
                       for a in range(64) for b in range(64))
    assert pulled_hat == original_hat

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
                  'distinct_only_orbit_rank': len(basis), 'rank_prime': prime,
                  'nonlocal_relabel_labels': 4096, 'fourier_controls': 5,
                  'minimum_entropy_fourth_power': entropy_min_power,
                  'bindings': {str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest() for path in files}}, indent=2))
