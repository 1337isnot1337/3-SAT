#!/usr/bin/env python3
"""Exact h=9 crossing using the predecessor input labels and even output partitions."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import importlib.util
import json
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('cubic_parity',ROOT/'research/charged-cubic-parity/verify.py')
p=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=p
spec.loader.exec_module(p)


def main():
    data=p.model.construct(3)
    h,n=data['h'],data['N']
    assert (h,n)==(9,8)
    states=data['states']
    even=[x for x in states if len(x)%2==0]
    odd=[x for x in states if len(x)%2==1]
    assert (len(even),len(odd))==(14,16)
    output=even[:n]
    pairing=[]
    for a in data['row_labels']:
        row=[]
        for b in data['column_labels']:
            f0=p.cubic(a,b,()).get((),0)
            f1=p.cubic(a,b,(1,)).get((1,),0)
            row.append((1-h)*f0+h*f1)
        pairing.append(row)
    assert p.rank(pairing)==n
    inverse=p.model.inverse(pairing)
    assert all(sum((inverse[i][k]*pairing[k][j] for k in range(n)),F(0))==int(i==j)
               for i in range(n) for j in range(n))
    checks=0
    for a,mu in enumerate(data['row_labels']):
        for v,nu in enumerate(data['column_labels']):
            for y,arg in enumerate(output):
                vector=p.cubic(mu,nu,arg)
                for u,out in enumerate(output):
                    assert vector.get(out,0)==pairing[a][v]*int(u==y)
                    checks+=1
        print('completed label row',a+1,'of',n,file=sys.stderr,flush=True)
    assert checks==n**4
    # The local inverse is on the first input axis, preserving both source cuts.
    for x in range(n):
        for y in range(n):
            for u in range(n):
                for v in range(n):
                    value=sum((inverse[x][a]*pairing[a][v] for a in range(n)),F(0))*int(u==y)
                    assert value==int(x==v and y==u)
    files=[HERE/'verify.py',ROOT/'research/charged-cubic-parity/verify.py',
           ROOT/'research/charged-cubic-parity/PROOF.md',ROOT/'research/charged-asymmetric-crossing/model.py',
           *(ROOT/'research/charged-operator-moments'/name for name in ('charged.py','pairing.py','predecessor.py'))]
    print(json.dumps({'grade':h,'dimension':n,'even_partition_count':len(even),'odd_partition_count':len(odd),
                      'row_labels':data['row_labels'],'column_labels':data['column_labels'],
                      'output_labels':output,'pairing':[[str(x) for x in row] for row in pairing],
                      'inverse':[[str(x) for x in row] for row in inverse],
                      'full_scalar_entry_checks':checks,'normalized_crossing_entry_checks':n**4,
                      'sha256':{str(path.relative_to(ROOT)):sha256(path.read_bytes()).hexdigest() for path in files}},indent=2))

if __name__=='__main__':main()
