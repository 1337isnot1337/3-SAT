"""Check the 2h-1 coefficient by exact polynomial interpolation."""
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
    weights = []
    for x in range(degree + 1):
        poly = [Fraction(1)]
        for y in range(degree + 1):
            if x == y:
                continue
            nxt = [Fraction(0)] * (len(poly) + 1)
            for k, c in enumerate(poly):
                nxt[k] -= c * y / (x - y)
                nxt[k+1] += c / (x - y)
            poly = nxt
        weights.append(poly[target])
    return weights


cases = 0
for h in range(2, 5):
    labels = [(1,) * h, (2,) + (1,) * (h-2)]
    weights = coefficient_weights(2*h, 2*h-1)
    for row, x in enumerate(labels):
        for col, v in enumerate(labels):
            for E in range(3):
                for state in charged.partitions(E):
                    for reverse in (False, True):
                        result = {}
                        for q, weight in enumerate(weights):
                            for target, value in charged.piece_vector(x, v, state, h, q, reverse):
                                result[target] = result.get(target, Fraction(0)) + weight * value
                        result = {key: value for key, value in result.items() if value}
                        value = [[0, -h*(h-1)//2], [-1, 0]][row][col]
                        expected = {state: Fraction(value)} if value else {}
                        assert result == expected, (h, x, v, state, reverse, result, expected)
                        cases += 1
print(json.dumps({'result': 'PASS', 'cases': cases, 'grades': [2,3,4],
                  'output_grades': [0,1,2], 'both_operator_orders': True,
                  'source_hashes': {name: sha256((SOURCE / name).read_bytes()).hexdigest()
                                    for name in ('charged.py','predecessor.py')},
                  'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest()},
                 indent=2, sort_keys=True))
