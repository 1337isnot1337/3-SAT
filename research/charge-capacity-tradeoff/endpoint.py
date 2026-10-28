"""Finite exact extraction of the top charge coefficient of raw pieces."""
from fractions import Fraction
from hashlib import sha256
import json
from math import comb, factorial
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'charged-operator-moments'
sys.path.insert(0, str(SOURCE))
import charged

cases = 0
for h in range(1, 4):
    degree = 2 * h
    for x in charged.partitions(h):
        for v in charged.partitions(h):
            for E in range(3):
                for state in charged.partitions(E):
                    for shift in range(-h-1, h+2):
                        for reverse in (False, True):
                            out = {}
                            for q in range(degree + 1):
                                sign = (-1) ** (degree-q) * comb(degree, q)
                                for target, value in charged.piece_vector(x, v, state, shift, q, reverse):
                                    out[target] = out.get(target, 0) + sign * value
                            out = {k: Fraction(v, factorial(degree)) for k, v in out.items() if v}
                            expected = {}
                            if x == (1,) * h and v == (1,) * h and abs(shift) <= h:
                                expected[state] = Fraction((-1) ** (h-shift) * comb(2*h, h-shift))
                            assert out == expected, (h, x, v, state, shift, reverse, out, expected)
                            cases += 1
print(json.dumps({'result': 'PASS', 'cases': cases, 'grades': [1,2,3],
                  'output_grades': [0,1,2], 'both_operator_orders': True,
                  'source_hashes': {name: sha256((SOURCE / name).read_bytes()).hexdigest()
                                    for name in ('charged.py', 'predecessor.py')},
                  'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest()},
                 indent=2, sort_keys=True))
