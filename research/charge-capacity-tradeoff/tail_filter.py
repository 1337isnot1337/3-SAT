"""Check a high-shift scalar coefficient, exactly at small grades."""
from fractions import Fraction
from hashlib import sha256
import json
from math import comb
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

cases=0
for h in range(2,5):
    shifts={h+k:(1-k)*comb(2*h+k-1,k) for k in range(h+1) if k!=1}
    coeff=interpolation_weights(2*h,2*h-2)
    for E in range(h+1):
        for state in charged.partitions(E):
            expected=-2*h*(h*h-h+1)*E
            for reverse in (False,True):
                out={}
                for s,v in shifts.items():
                    for q,w in enumerate(coeff):
                        for target,value in charged.piece_vector((1,)*h,(1,)*h,state,s,q,reverse):
                            out[target]=out.get(target,Fraction(0))+v*w*value
                out={k:v for k,v in out.items() if v}
                assert out==({state:expected} if expected else {}), (h,E,state,reverse,out,expected)
                cases+=1
print(json.dumps({'result':'PASS','operator_cases':cases,'grades':[2,4],
                  'output_grades':'0 through h','both_operator_orders':True,
                  'source_hashes':{name:sha256((SOURCE/name).read_bytes()).hexdigest()
                                   for name in ('charged.py','predecessor.py')},
                  'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest()},
                 indent=2,sort_keys=True))
