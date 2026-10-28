"""Replay a frozen nonzero modular minor and direct coefficient controls.

Requires a C++17 compiler and NumPy. No binary or matrix is retained.
"""
from collections import defaultdict
from contextlib import redirect_stdout
from hashlib import sha256
import importlib.util
import io
import json
from math import factorial, isqrt, prod
from pathlib import Path
import subprocess
import tempfile

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
# The six-block checker separately constructs the complete ten-class table.
spec = importlib.util.spec_from_file_location('f8_six', HERE / 'screen.py')
six = importlib.util.module_from_spec(spec)
with redirect_stdout(io.StringIO()):
    spec.loader.exec_module(six)
C = six.C
prime = 65521
assert all(prime % d for d in range(2, isqrt(prime) + 1))
assert (prime - 1) ** 2 + prime - 1 < 2 ** 63


def compositions(total, letters):
    if letters == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in compositions(total - first, letters - 1):
                yield (first,) + tail


def size(alpha):
    return factorial(8) * 7 ** (8 - alpha[0]) // prod(factorial(x) for x in alpha)


def permute(alpha, permutation):
    out = [0] * 10
    for i, x in enumerate(alpha):
        out[permutation[i]] = x
    return tuple(out)


frobenius = [0, 1, 2] + [2 + six.s.multiply(x, x) for x in range(1, 8)]
swap = [0, 2, 1] + list(range(3, 10))
group = []
for step in range(3):
    for flip in range(2):
        p = list(range(10))
        for _ in range(step):
            p = [frobenius[x] for x in p]
        if flip:
            p = [swap[x] for x in p]
        assert all(C[p[i]][p[j]] == C[i][j] for i in range(10) for j in range(10))
        group.append(p)

all_types = list(compositions(8, 10))
allowed = {a for a in all_types if size(a) > 14527298520}
assert len(all_types) == 24310 and len(allowed) == 6345
assert max(size(a) for a in all_types if a not in allowed) == 14527298520
assert min(map(size, allowed)) == 16602626880
# 1697/50 < 24 sqrt(2) < 679/20.
assert 1697 ** 2 < 50 ** 2 * 1152
assert 679 ** 2 > 20 ** 2 * 1152
assert 14527298520 ** 50 < 2 ** 1697
assert 16602626880 ** 20 > 2 ** 679

remaining = set(all_types)
row_representatives = []
for a in all_types:
    if a in remaining:
        row_representatives.append(a)
        remaining.difference_update(permute(a, p) for p in group)
input_orbits = []
for a in all_types:
    if a in allowed:
        orbit = {permute(a, p) for p in group}
        assert orbit <= allowed
        input_orbits.append(orbit)
        allowed.difference_update(orbit)
assert len(row_representatives) == 5594 and len(input_orbits) == 1382


def direct_coefficient(alpha, beta):
    """Independent coefficient DP, pruning terms outside one output type."""
    terms = {(0,) * 10: 1}
    for i, count in enumerate(alpha):
        for _ in range(count):
            out = defaultdict(int)
            for powers, value in terms.items():
                for j, c in enumerate(C[i]):
                    if c and powers[j] < beta[j]:
                        new = list(powers)
                        new[j] += 1
                        out[tuple(new)] += value * c
            terms = out
    return terms.get(beta, 0)


with tempfile.TemporaryDirectory(prefix='f8-eight-') as directory:
    directory = Path(directory)
    executable, matrix_path = directory / 'build', directory / 'matrix.bin'
    subprocess.run(['g++', '-O3', '-std=c++17', str(HERE / 'eight.cpp'), '-o', str(executable)], check=True)
    subprocess.run([str(executable), str(matrix_path)], check=True)
    assert matrix_path.stat().st_size == 5594 * 1382 * 2
    matrix = np.memmap(matrix_path, mode='r', dtype=np.uint16, shape=(5594, 1382))
    controls = 0
    for ri in (0, 123, 1234, 2800, 5593):
        for ci in (0, 300, 700, 1381):
            b = row_representatives[ri]
            value = sum(direct_coefficient(a, b) - (8 ** 8 if a == b else 0)
                        for a in input_orbits[ci])
            assert value % prime == int(matrix[ri, ci])
            controls += 1
    pivots = json.loads((HERE / 'eight-pivot-rows.json').read_text())
    assert len(pivots) == len(set(pivots)) == 1382
    assert all(isinstance(x, int) and 0 <= x < 5594 for x in pivots)
    minor = matrix[pivots, :].astype(np.int64)
    for col in range(1382):
        assert minor[col, col] != 0
        minor[col, col:] = minor[col, col:] * pow(int(minor[col, col]), -1, prime) % prime
        factors = minor[col + 1:, col].copy()
        minor[col + 1:, col + 1:] = (minor[col + 1:, col + 1:] - factors[:, None] * minor[col, col + 1:]) % prime
        minor[col + 1:, col] = 0
    del matrix

bindings = [HERE / 'eight.py', HERE / 'eight.cpp', HERE / 'eight-pivot-rows.json', HERE / 'screen.py',
            HERE.parent / 'three-bit-macro-walsh' / 'schemes.py',
            HERE.parent / 'three-bit-macro-walsh' / 'four-block-dual.json']
print(json.dumps({'status': 'PASS', 'scope': 'eight-macro high-floor invariant dual rank',
                  'all_types': 24310, 'eligible_types': 6345, 'input_orbits': 1382,
                  'output_orbits': 5594, 'prime': prime, 'minor_rank': 1382,
                  'direct_entry_controls': controls,
                  'bindings': {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in bindings}}, indent=2))
