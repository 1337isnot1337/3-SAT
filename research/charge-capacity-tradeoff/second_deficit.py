"""Check the q^(2h-2) output operator by exact interpolation."""
from fractions import Fraction
from hashlib import sha256
import json
from math import comb
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'charged-operator-moments'
sys.path.insert(0, str(SOURCE))
import charged


def weights(degree, target):
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


cases = 0
for h in range(2, 5):
    a = (1,) * h
    coeff = weights(2*h, 2*h-2)
    for E in range(h+1):
        for state in charged.partitions(E):
            expected = 2*h*(h-1)*E + h*h*sum(
                (-1)**i * comb(2*h, i) * i * state.count(i)
                for i in range(1, E+1))
            for reverse in (False, True):
                out = {}
                for q, w in enumerate(coeff):
                    for target, value in charged.piece_vector(a, a, state, h, q, reverse):
                        out[target] = out.get(target, Fraction(0)) + w * value
                out = {key: value for key, value in out.items() if value}
                assert out == ({state: expected} if expected else {}), (h, state, reverse, out, expected)
                cases += 1
print(json.dumps({'result': 'PASS', 'cases': cases, 'grades': [2,3,4],
                  'output_grades': '0 through h', 'both_operator_orders': True,
                  'source_hashes': {name: sha256((SOURCE/name).read_bytes()).hexdigest()
                                    for name in ('charged.py','predecessor.py')},
                  'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest()},
                 indent=2, sort_keys=True))
