"""Check truncated high-charge recurrence and bilateral scalar screens."""
from fractions import Fraction as F
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'charged-operator-moments'
sys.path.insert(0,str(SOURCE))
sys.path.insert(0,str(HERE))
from truncated_model import p, piece

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



import charged
import hashlib
import json

prior=json.loads((HERE/'tail-next-screen-verification.json').read_text())
checks=0
for h in (2,3,4):
    states=p.partitions(h)
    coeff=interpolation_weights(2*h,2*h-3)
    for mu in states:
        for nu in states:
            for arg in states:
                for s in (-2*h,-h,h,2*h):
                    actual={}
                    for q,w in enumerate(coeff):
                        for target,value in charged.piece_vector(mu,nu,arg,s,q):
                            actual[target]=actual.get(target,F(0))+w*value
                    actual={k:v for k,v in actual.items() if v}
                    assert piece(mu,nu,arg,s,2*h-3)==actual,(h,mu,nu,arg,s)
                    checks+=1

results=[]
for h in (2,3,4,5,6):
    states=p.partitions(h)
    shifts=list(range(-2*h,-h+1))+list(range(h,2*h+1))
    pieces=[]
    for s in shifts:
        d={}
        for a in states:
            for b in states:
                for y in states:
                    for u,x in piece(a,b,y,s,2*h-3).items():
                        d[(a,b,y,u)]=x
        pieces.append(d)
    rows=[]
    for a in states:
        for b in states:
            for y in states:
                for u in states:
                    key=(a,b,y,u)
                    if u!=y:
                        rows.append([z.get(key,0) for z in pieces])
                    elif y!=states[0]:
                        rows.append([z.get(key,0)-z.get((a,b,states[0],states[0]),0) for z in pieces])
    basis=rational_null(rows,len(shifts))
    mod=modular_rank(rows,65537)
    assert mod==len(shifts)-len(basis)
    ranks=[]
    for v in basis:
        matrix=[[sum(v[i]*z.get((a,b,states[0],states[0]),0) for i,z in enumerate(pieces))
                 for b in states] for a in states]
        ranks.append(p.exact_rank(matrix))
    expected={2:(3,[2,2,2]),3:(2,[2,2]),4:(2,[4,4]),5:(2,[4,4]),6:(2,[4,4])}[h]
    assert (len(basis),ranks)==expected,(h,len(basis),ranks)
    if h<=4:
        old=next(x for x in prior['results'] if x['h']==h and x['mode']=='bilateral')
        assert [[str(x) for x in v] for v in basis]==old['basis']
    results.append({'h':h,'dimension':len(basis),'pairing_ranks':ranks,
                    'modular_rank':mod,'basis':[[str(x) for x in v] for v in basis]})
print(json.dumps({'result':'PASS','raw_comparisons':checks,'modular_prime':65537,
                  'results':results,'scope':'forward-order truncated recurrence; h<=4 raw comparison to direct interpolation',
                  'model_sha256':hashlib.sha256((HERE/'truncated_model.py').read_bytes()).hexdigest(),
                  'source_hashes':{name:hashlib.sha256((SOURCE/name).read_bytes()).hexdigest()
                                   for name in ('charged.py','predecessor.py')},
                  'prior_screen_sha256':hashlib.sha256((HERE/'tail-next-screen-verification.json').read_bytes()).hexdigest(),
                  'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
                 indent=2,sort_keys=True))
