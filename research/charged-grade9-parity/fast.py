#!/usr/bin/env python3
"""Finite h=9 pairing, local normalization, and one direct operator-vector control."""
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
    data=p.model.construct(3);h,n=data['h'],data['N']
    assert (h,n)==(9,8)
    even=[x for x in data['states'] if len(x)%2==0]
    odd=[x for x in data['states'] if len(x)%2==1]
    assert (len(even),len(odd))==(14,16)
    outputs=even[:n]
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
    assert all(sum((inverse[x][k]*pairing[k][v] for k in range(n)),F(0))==int(x==v)
               for x in range(n) for v in range(n))
    a,v,y=7,7,3
    vector=p.cubic(data['row_labels'][a],data['column_labels'][v],outputs[y])
    assert all(vector.get(out,0)==pairing[a][v]*int(u==y) for u,out in enumerate(outputs))
    files=[HERE/'fast.py',ROOT/'research/charged-cubic-parity/verify.py',
           ROOT/'research/charged-cubic-parity/PROOF.md',ROOT/'research/charged-asymmetric-crossing/model.py',
           *(ROOT/'research/charged-operator-moments'/name for name in ('charged.py','pairing.py','predecessor.py'))]
    print(json.dumps({'grade':h,'dimension':n,'even_partition_count':len(even),'odd_partition_count':len(odd),
                      'row_labels':data['row_labels'],'column_labels':data['column_labels'],
                      'output_labels':outputs,'pairing':[[str(x) for x in row] for row in pairing],
                      'inverse':[[str(x) for x in row] for row in inverse],
                      'direct_vector_control_indices':[a,v,y], 'direct_projected_entry_checks':n,
                      'sha256':{str(path.relative_to(ROOT)):sha256(path.read_bytes()).hexdigest() for path in files}},indent=2))

if __name__=='__main__':main()
