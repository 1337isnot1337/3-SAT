"""Check the adjacent-shift formula and grade-wise eigenvalue collisions."""
from collections import defaultdict
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


def interpolation_weights(degree, target):
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


def partitions(n, largest):
    if n == 0:
        yield ()
        return
    for k in range(min(n, largest), 0, -1):
        for tail in partitions(n-k, k):
            yield (k,) + tail


def spectral_weight(h, j):
    if j == 1:
        return 1 + comb(2*h,2)
    return (-1)**(j+1)*j*comb(2*h,j+1)


operator_cases = 0
for h in range(2, 6):
    a = (1,) * h
    coeff = interpolation_weights(2*h, 2*h-2)
    for E in range(h+1):
        for state in charged.partitions(E):
            expected = -4*h*h*(h-1)*E + h*h*(1 + sum(spectral_weight(h,j) for j in state))
            for reverse in (False,True):
                out = {}
                for q,w in enumerate(coeff):
                    for target,value in charged.piece_vector(a,a,state,h-1,q,reverse):
                        out[target] = out.get(target,Fraction(0)) + w*value
                out = {k:v for k,v in out.items() if v}
                assert out == ({state:expected} if expected else {}), (h,state,reverse,out,expected)
                operator_cases += 1

counts = {}
collisions = {}
for h in range(2, 46):
    vals = defaultdict(list)
    weights = [0]+[spectral_weight(h,j) for j in range(1,h+1)]
    for state in partitions(h,h):
        vals[sum(weights[j] for j in state)].append(state)
    repeated = [group for group in vals.values() if len(group)>1]
    if h == 4:
        assert repeated == [[(4,), (2,2)]], repeated
    else:
        assert not repeated, (h,repeated)
    counts[str(h)] = sum(map(len, vals.values()))
    if repeated:
        collisions[str(h)] = repeated
print(json.dumps({'result':'PASS','operator_cases':operator_cases,'operator_grades':[2,5],
                  'spectral_grades':[2,45], 'partition_vectors':sum(counts.values()),
                  'collisions':collisions,'source_hashes':{name:sha256((SOURCE/name).read_bytes()).hexdigest()
                           for name in ('charged.py','predecessor.py')},
                  'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest()},
                 indent=2,sort_keys=True))
