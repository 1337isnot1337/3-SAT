"""Counterexample to reusing the high-shift weights one charge degree lower."""
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'charged-operator-moments'
sys.path.insert(0,str(SOURCE))
import charged


def interpolation_weights(degree,target):
    result=[]
    for x in range(degree+1):
        p=[Fraction(1)]
        for y in range(degree+1):
            if x==y:
                continue
            nxt=[Fraction(0)]*(len(p)+1)
            for i,v in enumerate(p):
                nxt[i] -= v*y/(x-y)
                nxt[i+1] += v/(x-y)
            p=nxt
        result.append(p[target])
    return result

coeff=interpolation_weights(4,1)
for state,target in (((1,1),(2,)),((2,),(1,1))):
    for reverse in (False,True):
        out={}
        for shift,multiplier in ((2,1),(4,-10)):
            for q,w in enumerate(coeff):
                for result,value in charged.piece_vector((1,1),(1,1),state,shift,q,reverse):
                    out[result]=out.get(result,Fraction(0))+multiplier*w*value
        out={k:v for k,v in out.items() if v}
        assert out=={target:-48},(state,reverse,out)
print(json.dumps({'result':'PASS','h':2,'charge_degree':1,'operator_cases':4,
                  'source_hashes':{name:sha256((SOURCE/name).read_bytes()).hexdigest()
                                   for name in ('charged.py','predecessor.py')},
                  'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest()},
                 indent=2,sort_keys=True))
