"""Replay a six-macro dual using exact compressed character polynomials.

Requires g++ with C++17; the matrix is generated only in a temporary directory.
"""
from array import array
from collections import defaultdict
from contextlib import redirect_stdout
from fractions import Fraction
from hashlib import sha256
import importlib.util
import io
import json
from math import prod
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('entropy_predecessor', HERE / 'verify.py')
base = importlib.util.module_from_spec(spec)
with redirect_stdout(io.StringIO()):
    spec.loader.exec_module(base)


def compositions(n, k):
    if k == 1:
        yield (n,)
    else:
        for i in range(n + 1):
            for tail in compositions(n - i, k - 1):
                yield (i,) + tail


def entropy_power(a):
    return Fraction(6 ** 6 * 7 ** (6 - a[0]), prod(x ** x for x in a if x))


def coefficient(alpha, beta):
    """Compute one matrix entry independently, pruning to the output type."""
    terms = {(0,) * 10: 1}
    for i, count in enumerate(alpha):
        for _ in range(count):
            out = defaultdict(int)
            for powers, value in terms.items():
                for j, c in enumerate(base.C[i]):
                    if c and powers[j] < beta[j]:
                        new = list(powers)
                        new[j] += 1
                        out[tuple(new)] += value * c
            terms = out
    return terms.get(beta, 0)


types = list(compositions(6, 10))
eligible = {a for a in types if entropy_power(a) ** 4 > 153664 ** 6}
assert len(types) == 5005 and len(eligible) == 2688
orbits = []
for a in types:
    if a in eligible:
        group = base.orbit(a)
        assert group <= eligible
        orbits.append(group)
        eligible.difference_update(group)
assert len(orbits) == 625
remaining = set(types)
row_representatives = []
for a in types:
    if a in remaining:
        row_representatives.append(a)
        remaining.difference_update(base.orbit(a))
assert len(row_representatives) == 1234
seed = json.loads((HERE / 'six-seed.json').read_text())
denominator = seed['denominator']
terms = seed['terms']
assert isinstance(denominator, int) and denominator > 0 and len(terms) == 467
lookup = {min(group): i for i, group in enumerate(orbits)}
selected = {}
for term in terms:
    alpha, value = tuple(term['type']), term['coefficient']
    assert alpha in lookup and lookup[alpha] not in selected
    assert isinstance(value, int) and value and abs(value) < 2 ** 32
    assert entropy_power(alpha) >= 196036848
    selected[lookup[alpha]] = value
assert min(entropy_power(tuple(t['type'])) for t in terms) == 196036848
assert 2 ** 27 < 196036848 < 2 ** 28
pairing = sum(value * sum(prod(q ** count for q, count in zip(base.q, a)) for a in orbits[i])
              for i, value in selected.items())
assert pairing == denominator

with tempfile.TemporaryDirectory(prefix='f8-six-') as directory:
    directory = Path(directory)
    executable, path = directory / 'build', directory / 'matrix.bin'
    subprocess.run(['g++', '-O3', '-std=c++17', str(HERE / 'six-builder.cpp'), '-o', str(executable)], check=True)
    subprocess.run([str(executable), str(path)], check=True)
    metadata = path.with_suffix('.bin.meta').read_text().splitlines()
    assert metadata[0] == '1234 625'
    assert [tuple(map(int, line.split())) for line in metadata[1:]] == [min(group) for group in orbits]
    matrix = array('q')
    assert matrix.itemsize == 8
    with path.open('rb') as f:
        matrix.fromfile(f, 1235 * 625)
        assert not f.read(1)
    for row in range(1235):
        value = sum(int(matrix[row * 625 + col]) * c for col, c in selected.items())
        assert value == (denominator if row == 1234 else 0)
    # A rational output-row combination equals the target row on every
    # orbit with a strictly higher entropy floor than this seed.
    relation = json.loads((HERE / 'six-relation.json').read_text())
    relation_terms = relation['terms']
    relation_denominator = relation['denominator']
    assert isinstance(relation_denominator, int) and relation_denominator > 0
    assert len(relation_terms) == len({row for row, _ in relation_terms}) == 477
    assert all(isinstance(row, int) and 0 <= row < 1234 and isinstance(c, int) and c
               for row, c in relation_terms)
    higher = [i for i, group in enumerate(orbits) if entropy_power(min(group)) > 196036848]
    assert len(higher) == 485
    for col in higher:
        value = sum(int(matrix[row * 625 + col]) * c for row, c in relation_terms)
        assert value == relation_denominator * int(matrix[1234 * 625 + col])
    controls = 0
    for ri in (0, 50, 600, 1233):
        for ci in (0, 123, 300, 500, 624):
            beta = row_representatives[ri]
            value = sum(coefficient(a, beta) - (8 ** 6 if a == beta else 0) for a in orbits[ci])
            assert value == matrix[ri * 625 + ci]
            controls += 1

files = [HERE / 'six.py', HERE / 'six-builder.cpp', HERE / 'six-seed.json', HERE / 'six-relation.json', HERE / 'verify.py',
         HERE / 'seed.json', ROOT / 'research/three-bit-macro-walsh/schemes.py']
print(json.dumps({'status': 'PASS', 'scope': 'six-macro rational dual and entropy floor',
                  'seed_orbits': len(terms), 'eligible_orbits': len(orbits), 'output_orbits': len(row_representatives),
                  'pairing': pairing, 'minimum_entropy_sixth_power': 196036848,
                  'direct_entry_controls': controls, 'higher_entropy_orbits': len(higher),
                  'row_relation_terms': len(relation_terms),
                  'bindings': {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in files}}, indent=2))
