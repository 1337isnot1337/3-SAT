"""Direct interpolation spot checks for the truncated recurrence at h=5,6."""
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'charged-operator-moments'
sys.path.insert(0,str(SOURCE))
sys.path.insert(0,str(HERE))
import charged
from truncated_model import piece


def interpolation_weights(degree,target):
    result=[]
    for x in range(degree+1):
        p=[F(1)]
        for y in range(degree+1):
            if x==y:
                continue
            nxt=[F(0)]*(len(p)+1)
            for i,v in enumerate(p):
                nxt[i] -= v*y/(x-y)
                nxt[i+1] += v/(x-y)
            p=nxt
        result.append(p[target])
    return result

cases=0
for h in (5,6):
    a=(1,)*h
    b=(2,)+(1,)*(h-2)
    state=(h,)
    coeff=interpolation_weights(2*h,2*h-3)
    for shift in (-2*h,-h,h,2*h):
        expected=piece(a,b,state,shift,2*h-3)
        for reverse in (False,True):
            out={}
            for q,w in enumerate(coeff):
                for target,value in charged.piece_vector(a,b,state,shift,q,reverse):
                    out[target]=out.get(target,F(0))+w*value
            out={k:v for k,v in out.items() if v}
            assert out==expected,(h,shift,reverse,out,expected)
            cases+=1
print(json.dumps({'result':'PASS','grades':[5,6],'operator_cases':cases,
                  'both_operator_orders':True,
                  'model_sha256':sha256((HERE/'truncated_model.py').read_bytes()).hexdigest(),
                  'source_hashes':{name:sha256((SOURCE/name).read_bytes()).hexdigest()
                                   for name in ('charged.py','predecessor.py')},
                  'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest()},
                 indent=2,sort_keys=True))
