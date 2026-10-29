#!/usr/bin/env python3
"""Direct bounded mod-16 checks for removed pins and mixed pin gates."""
from fractions import Fraction as F
from itertools import product
from math import prod
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def case(L, b):
    T=2*L+1
    common=F(prod(T-j for j in range(-L,L)), prod(-j for j in range(-L,L) if j))
    W=[]
    for x in range(L):
        row=[]
        for y in range(L):
            v=common/F(T-y+x)
            assert v.denominator % 2
            row.append(v.numerator*pow(v.denominator,-1,16)%16)
        W.append(row)
    selected=tuple(2*j for j in range(b))
    states=list(product(range(3), repeat=b))  # pin retained, removed, z moment
    moments=[0]*len(states)
    gates=[[0]*(1<<b) for _ in range(1<<b)]
    for X in range(1<<L):
        z=[sum(row[y] for y in range(L) if X>>y&1)%16 for row in W]
        base=prod((1-z[x] for x in range(L) if x not in selected))%16
        pins=[1-z[j] for j in selected]
        for i,state in enumerate(states):
            term=base
            for j,s in enumerate(state):
                if s==0: term*=pins[j]
                elif s==2: term*=pins[j]*z[selected[j]]
            moments[i]=(moments[i]+term)%16
        for c in range(1<<b):
            weight=base*prod((z[j] if c>>i&1 else 1-z[j]
                              for i,j in enumerate(selected)))%16
            for t in range(1<<b):
                val=weight*prod((1-((t>>i)&1)-z[j]+2*((t>>i)&1)*z[j]
                                 for i,j in enumerate(selected)))
                gates[c][t]=(gates[c][t]+val)%16
    assert moments[0]==8 and all(x==0 for x in moments[1:])
    assert all(gates[c][t] == (8 if c==t else 0)
               for c in range(1<<b) for t in range(1<<b))
    return {'L':L,'b':b,'mixed_removed_pin_moments':len(states)-1,
            'all_nontrivial_moments_zero_mod_16':True,
            'arbitrary_pin_gate_patterns':(1<<b)**2,
            'gate_matrix_is_8_identity_mod_16':True}


def main():
    paths=[HERE/'mixed-pin-screen.py', HERE/'PROOF.md',
           ROOT/'upstream/openai-eth-2026/build/quantitative-contraction.tex']
    return {'cases':[case(8,3),case(16,3)],
            'scope':'finite direct Boolean sums, not an independent proof',
            'sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in paths}}

if __name__=='__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
