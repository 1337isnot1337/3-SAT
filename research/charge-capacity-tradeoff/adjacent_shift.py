"""Exact interpolation for the grade-four adjacent-shift collision."""
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'charged-operator-moments'
sys.path.insert(0, str(SOURCE))
import charged


def coefficient_weights(degree, target):
    result = []
    for x in range(degree + 1):
        poly = [Fraction(1)]
        for y in range(degree + 1):
            if x == y:
                continue
            new = [Fraction(0)] * (len(poly) + 1)
            for k, value in enumerate(poly):
                new[k] -= value * y / (x-y)
                new[k+1] += value / (x-y)
            poly = new
        result.append(poly[target])
    return result


weights = coefficient_weights(8, 6)
eigenvalues = {}
for state in charged.partitions(4):
    m = [0] + [state.count(i) for i in range(1, 5)]
    expected = -768 + 16*(1 + 29*m[1] - 112*m[2] + 210*m[3] - 224*m[4])
    for reverse in (False, True):
        out = {}
        for q, weight in enumerate(weights):
            for target, value in charged.piece_vector((1,)*4, (1,)*4, state, 3, q, reverse):
                out[target] = out.get(target, Fraction(0)) + weight*value
        out = {k:v for k,v in out.items() if v}
        assert out == ({state:expected} if expected else {}), (state, reverse, out, expected)
    eigenvalues[str(state)] = expected
assert eigenvalues['(4,)'] == eigenvalues['(2, 2)'] == -4336
print(json.dumps({'result':'PASS', 'eigenvalues':eigenvalues, 'both_operator_orders':True,
                  'source_hashes':{name:sha256((SOURCE/name).read_bytes()).hexdigest()
                                   for name in ('charged.py','predecessor.py')},
                  'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest()},
                 indent=2, sort_keys=True))
