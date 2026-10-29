#!/usr/bin/env python3
"""Exact control against naive multiplication stability of the pairing kernel."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import importlib.util
import json
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('parity_verify',HERE/'verify.py')
v=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=v
spec.loader.exec_module(v)


def nullspace(rows):
    rows=[[F(x) for x in row] for row in rows]
    width=len(rows[0]);pivots=[]
    for j in range(width):
        k=next((i for i in range(len(pivots),len(rows)) if rows[i][j]),None)
        if k is None: continue
        r=len(pivots);rows[r],rows[k]=rows[k],rows[r]
        scale=rows[r][j];rows[r]=[x/scale for x in rows[r]]
        for i in range(len(rows)):
            if i!=r and rows[i][j]:
                scale=rows[i][j];rows[i]=[x-scale*y for x,y in zip(rows[i],rows[r])]
        pivots.append(j)
    result=[]
    for j in range(width):
        if j in pivots: continue
        vector=[F(0)]*width;vector[j]=1
        for i,k in enumerate(pivots):vector[k]=-rows[i][j]
        result.append(vector)
    return result


def matrix(h,energy):
    labels=v.model.predecessor.partitions(h)
    matrix=[]
    for a in labels:
        row=[]
        for b in labels:
            f0=v.cubic(a,b,()).get((),0)
            f1=v.cubic(a,b,(1,)).get((1,),0)
            value=(1-energy)*f0+energy*f1
            state=(energy,)
            assert value==v.cubic(a,b,state).get(state,0)
            row.append(value)
        matrix.append(row)
    return labels,matrix


def main():
    small,a=matrix(4,4)
    big,b=matrix(5,4)
    basis=nullspace(a)
    assert len(basis)==1
    kernel=basis[0]
    assert all(sum(x*y for x,y in zip(row,kernel))==0 for row in a)
    product=[F(0)]*len(big)
    for i,label in enumerate(small):
        target=tuple(sorted(label+(1,),reverse=True))
        j=big.index(target)
        # b_label = dual_scale(label) * t_label.
        product[j]+=kernel[i]*F(v.model.predecessor.dual_scale(label),
                                v.model.predecessor.dual_scale(target))
    residual=[sum(x*y for x,y in zip(row,product)) for row in b]
    assert any(residual)
    files=[HERE/'kernel_control.py',HERE/'verify.py',HERE/'PROOF.md',
           ROOT/'research/charged-asymmetric-crossing/model.py',
           *(ROOT/'research/charged-operator-moments'/name for name in
             ('charged.py','pairing.py','predecessor.py'))]
    print(json.dumps({'charge':1,'output_energy':4,'from_grade':4,'to_grade':5,
                      'grade4_labels':small,'grade4_kernel':[str(x) for x in kernel],
                      'grade5_labels':big,'scaled_product':[str(x) for x in product],
                      'grade5_residual':[str(x) for x in residual],
                      'sha256':{str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in files}},indent=2))

if __name__=='__main__':main()
