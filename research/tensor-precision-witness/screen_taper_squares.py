#!/usr/bin/env python3
"""Test quadratic coefficients for squares of non-integral taper factors."""
from fractions import Fraction as Q
from math import factorial
from pathlib import Path
import runpy

f = runpy.run_path(str(Path(__file__).with_name('verify.py')))
mul, add, val, v2 = f['mul'], f['add'], f['value'], f['v2']
# Reuse exact monic division without executing the main quadratic screen.
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

cases=0
for L in (4,8,16,32):
    S=range(-L,L)
    den=Q((-1)**(L-1)*factorial(L)*factorial(L-1))
    C=[Q(1)]
    for t in S: C=mul(C,[Q(-t),Q(1)])
    W={}
    for d in range(-L+1,L):
        q,r=divide(C,[Q(-d),Q(1)])
        assert r==[0]
        W[d]=[x/den for x in q]
    Q0,r=divide(add(mul(W[0],W[0]),[-x for x in W[0]]),C)
    assert r==[0] and val(Q0,-L)==1/(L*den)
    for j in range(1,L.bit_length()-1):
        Pj=[Q(1)]
        for t in S:
            if t and v2(Q(t))<=j: Pj=mul(Pj,[Q(1),Q(-1,t)])
        F=mul(Pj,Pj)
        R,P=divide(F,C)
        c0=val(P,-L)
        coeff={d:(val(P,d)-c0)/val(W[d],d) for d in W}
        beta=L*den*val(R,-L)
        q={d:(d*den*val(R,d)+beta)/val(W[d],d) for d in W if d}
        result=[c0]
        for d in W: result=add(result,[coeff[d]*x for x in W[d]])
        result=add(result,[beta*x for x in add(mul(W[0],W[0]),[-x for x in W[0]])])
        for d in q: result=add(result,[q[d]*x for x in mul(W[d],W[0])])
        assert result==F
        assert all(not x or v2(x)>=0 for x in [c0,beta]+list(coeff.values())+list(q.values()))
        cases+=1
print(f'PASS: {cases} quadratic taper-square identities with 2-integral coefficients')
