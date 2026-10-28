"""Exact full-label, full-output scalar screen for the next charge degree."""
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'charged-operator-moments'
sys.path.insert(0,str(SOURCE))
import charged
import predecessor


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


def rational_null(rows,n):
    piv={}
    for row in rows:
        row=list(map(F,row))
        for p in sorted(piv):
            if row[p]:
                c=row[p];row=[x-c*y for x,y in zip(row,piv[p])]
        p=next((i for i,x in enumerate(row) if x),None)
        if p is None:
            continue
        c=row[p];row=[x/c for x in row]
        for q in piv:
            if piv[q][p]:
                c=piv[q][p];piv[q]=[x-c*y for x,y in zip(piv[q],row)]
        piv[p]=row
    result=[]
    for free in range(n):
        if free not in piv:
            v=[F(0)]*n;v[free]=1
            for p in piv:
                v[p]=-piv[p][free]
            assert all(sum(x*y for x,y in zip(row,v))==0 for row in rows)
            result.append(v)
    return result


def modular_rank(rows,prime):
    piv={}
    for row in rows:
        row=[(F(x).numerator*pow(F(x).denominator,-1,prime))%prime for x in row]
        for p in sorted(piv):
            if row[p]:
                c=row[p];row=[(x-c*y)%prime for x,y in zip(row,piv[p])]
        p=next((i for i,x in enumerate(row) if x),None)
        if p is not None:
            inv=pow(row[p],-1,prime);piv[p]=[(x*inv)%prime for x in row]
    return len(piv)

results=[]
for h in (2,3,4):
    labels=charged.partitions(h)
    shifts=list(range(h,2*h+1))
    coeff=interpolation_weights(2*h,2*h-3)
    pieces=[]
    for s in shifts:
        d={}
        for a in labels:
            for b in labels:
                for state in labels:
                    outputs=[]
                    for reverse in (False,True):
                        out={}
                        for q,w in enumerate(coeff):
                            for target,x in charged.piece_vector(a,b,state,s,q,reverse):
                                out[target]=out.get(target,F(0))+w*x
                        outputs.append({k:v for k,v in out.items() if v})
                    assert outputs[0]==outputs[1], (h,s,a,b,state,outputs)
                    for target,value in outputs[0].items():
                        d[(a,b,state,target)]=value
        pieces.append(d)
    rows=[]
    for a in labels:
        for b in labels:
            for y in labels:
                for u in labels:
                    key=(a,b,y,u)
                    if u!=y:
                        rows.append([p.get(key,0) for p in pieces])
                    elif y!=labels[0]:
                        rows.append([p.get(key,0)-p.get((a,b,labels[0],labels[0]),0) for p in pieces])
    basis=rational_null(rows,len(shifts))
    mr=modular_rank(rows,65537)
    assert mr == len(shifts)-len(basis)
    expected_dim=1 if h==2 else 0
    assert len(basis)==expected_dim,(h,basis)
    pair_ranks=[]
    for v in basis:
        mat=[[sum(v[i]*pieces[i].get((a,b,labels[0],labels[0]),0)
               for i in range(len(shifts))) for b in labels] for a in labels]
        pair_ranks.append(predecessor.exact_rank(mat))
    if h==2:
        assert basis==[[F(1,10),F(2,5),F(1)]] and pair_ranks==[2]
    results.append({'h':h,'shifts':shifts,'constraint_count':len(rows),
                    'modular_rank':mr,'basis':[[str(x) for x in v] for v in basis],
                    'pairing_ranks':pair_ranks})
print(json.dumps({'result':'PASS','prime':65537,'both_operator_orders':True,
                  'results':results,'source_hashes':{
                      name:sha256((SOURCE/name).read_bytes()).hexdigest()
                      for name in ('charged.py','predecessor.py')},
                  'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest()},
                 indent=2,sort_keys=True))
