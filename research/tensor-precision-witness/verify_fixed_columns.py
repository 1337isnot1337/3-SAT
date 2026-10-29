#!/usr/bin/env python3
"""Check the fixed-column divisibility and quartic remainder obstruction."""
from fractions import Fraction as Q
from itertools import combinations
from math import factorial
from pathlib import Path
import runpy

f=runpy.run_path(str(Path(__file__).with_name('verify.py')))
mul,add,val=f['mul'],f['add'],f['value']
def divide(p,q):
    p=p[:]
    while len(p)>1 and not p[-1]: p.pop()
    out=[Q(0)]*max(1,len(p)-len(q)+1)
    while len(p)>=len(q):
        i,z=len(p)-len(q),p[-1]/q[-1]
        out[i]+=z
        for j,x in enumerate(q): p[i+j]-=z*x
        while len(p)>1 and not p[-1]: p.pop()
    return out,p

triples=0
for L in (2,4,8):
    S=range(-L,L)
    C=[Q(1)]
    for t in S: C=mul(C,[Q(-t),Q(1)])
    den=Q((-1)**(L-1)*factorial(L)*factorial(L-1))
    W=[]
    for d in range(-L+1,L):
        w,r=divide(C,[Q(-d),Q(1)])
        assert r==[0]
        W.append([x/den for x in w])
    W.append(W[L-1])
    D=[Q(0),Q(1)]
    for _ in range(3): D=mul(D,[Q(L),Q(1)])
    for t in S:
        if t and t!=-L:
            D=mul(D,mul([Q(-t),Q(1)],[Q(-t),Q(1)]))
    assert len(D)-1==4*L and D[-2]==3*L
    for i,j,k in combinations(range(2*L),3):
        _,r=divide(mul(mul(W[i],W[j]),W[k]),D)
        assert r==[0]
        triples+=1
    H=[Q(1)]
    for t in S:
        if t and t%2: H=mul(H,[Q(1),Q(-1,t)])
    F=mul(mul(H,H),mul(H,H))
    _,r=divide(F,D)
    assert len(r)==4*L and r[-1]==-3*L*F[-1] and r[-1]!=0
print(f'PASS: {triples} triple products and 3 quartic remainder identities')
