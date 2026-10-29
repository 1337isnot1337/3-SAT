"""Check the entire finite scalar pairing on the adjacent-shift eigenspace."""
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'charged-operator-moments'
sys.path.insert(0, str(SOURCE))
import charged
import predecessor


def weights(degree, target):
    result = []
    for x in range(degree + 1):
        poly = [Fraction(1)]
        for y in range(degree + 1):
            if x == y:
                continue
            new = [Fraction(0)] * (len(poly) + 1)
            for k, value in enumerate(poly):
                new[k] -= value*y/(x-y)
                new[k+1] += value/(x-y)
            poly = new
        result.append(poly[target])
    return result


labels = charged.partitions(4)
assert labels == ((1,1,1,1),(2,1,1),(2,2),(3,1),(4,))
states = ((4,), (2,2))
expected = [[-4336,0,-24,-64,0], [0,-36,0,0,0],
            [-4,0,0,0,0], [-5,0,0,0,0], [0,0,0,0,0]]
coeff = weights(8, 6)
cases = 0
for i, a in enumerate(labels):
    for j, b in enumerate(labels):
        for state in states:
            for reverse in (False, True):
                out = {}
                for q, w in enumerate(coeff):
                    for target, value in charged.piece_vector(a,b,state,3,q,reverse):
                        out[target] = out.get(target,Fraction(0)) + w*value
                out = {k:v for k,v in out.items() if v}
                scalar = expected[i][j]
                assert out == ({state: scalar} if scalar else {}), (a,b,state,reverse,out)
                cases += 1
assert predecessor.exact_rank(expected) == 3
minor = [row[:3] for row in expected[:3]]
det = (minor[0][0] * (minor[1][1]*minor[2][2] - minor[1][2]*minor[2][1])
       - minor[0][1] * (minor[1][0]*minor[2][2] - minor[1][2]*minor[2][0])
       + minor[0][2] * (minor[1][0]*minor[2][1] - minor[1][1]*minor[2][0]))
assert det == 3456
print(json.dumps({'result':'PASS','label_pairs':25,'operator_cases':cases,
                  'output_states':['(4)', '(2,2)'], 'rank':3,
                  'rank_three_minor_determinant':3456,
                  'source_hashes':{name:sha256((SOURCE/name).read_bytes()).hexdigest()
                                   for name in ('charged.py','predecessor.py')},
                  'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest()},
                 indent=2,sort_keys=True))
