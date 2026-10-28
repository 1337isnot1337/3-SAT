#!/usr/bin/env python3
"""Independently check the saved polynomial bases and determinant certificates."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import importlib.util
import json
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('parity',ROOT/'research/charged-cubic-parity/verify.py')
v=importlib.util.module_from_spec(spec);sys.modules[spec.name]=v;spec.loader.exec_module(v)


def rational_det(matrix):
    rows=[[F(x) for x in row] for row in matrix]
    value=F(1)
    for j in range(len(rows)):
        pivot=next((i for i in range(j,len(rows)) if rows[i][j]),None)
        if pivot is None:return F(0)
        if pivot!=j:
            rows[j],rows[pivot]=rows[pivot],rows[j];value=-value
        a=rows[j][j];value*=a
        for i in range(j+1,len(rows)):
            factor=rows[i][j]/a
            for k in range(j+1,len(rows)):
                rows[i][k]-=factor*rows[j][k]
            rows[i][j]=0
    return value


def rank_mod(rows,p):
    pivots={}
    for row in rows:
        w=[(x.numerator%p)*pow(x.denominator,-1,p)%p for x in map(F,row)]
        for j in sorted(pivots):
            if w[j]:
                factor=w[j]
                w=[(a-factor*b)%p for a,b in zip(w,pivots[j])]
        j=next((i for i,a in enumerate(w) if a),None)
        if j is not None:
            factor=pow(w[j],-1,p)
            pivots[j]=[(factor*a)%p for a in w]
    return len(pivots)


def main():
    report=json.loads((HERE/'verification.json').read_text())
    audits=[]
    for record in report['results']:
        h=record['grade']; labels=v.model.predecessor.partitions(h);n=len(labels)
        A=[];B=[]
        for mu in labels:
            ar=[];br=[]
            for nu in labels:
                f0=v.cubic(mu,nu,()).get((),0);f1=v.cubic(mu,nu,(1,)).get((1,),0)
                ar.append(f0);br.append(f1-f0)
            A.append(ar);B.append(br)
        basis=[[F(x) for x in vector] for vector in record['degree_two_basis']]
        for vector in basis:
            assert len(vector)==3*n
            for t in range(4):
                for i in range(n):
                    value=sum(A[i][j]*vector[t*n+j] for j in range(n)) if t<=2 else 0
                    if t>=1:value+=sum(B[i][j]*vector[(t-1)*n+j] for j in range(n))
                    assert value==0
        evaluated=[[sum(vector[k*n+i]*h**k for k in range(3)) for i in range(n)] for vector in basis]
        expected=n-record['matrix_rank_at_specialization']
        for prime in (1000003,1000033,65537,1000037):
            try:
                modrank=rank_mod(evaluated,prime)
            except ValueError:
                continue
            if modrank==expected:break
        else:raise AssertionError('No chosen prime certifies evaluated-kernel rank')
        info=record['minor'];rows=info['row_indices'];cols=info['column_indices']
        coefficients=list(map(int,info['coefficients_low_degree_first']));r=len(rows)
        assert len(cols)==r==record['matrix_rank_at_specialization'] and len(coefficients)==r+1
        for energy in range(r+1):
            matrix=[[A[i][j]+energy*B[i][j] for j in cols] for i in rows]
            assert rational_det(matrix)==sum(c*energy**k for k,c in enumerate(coefficients))
        signs=[1 if x>0 else -1 for x in coefficients if x]
        if h==7:
            assert signs[0]<0 and signs[-1]>0
            assert sum(signs[i]!=signs[i-1] for i in range(1,len(signs)))==1
            assert coefficients[0]<0 and sum(coefficients)>0
        else:
            assert coefficients[0]!=0 and all(x==signs[0] for x in signs)
        no_three=[j for j,part in enumerate(labels) if 3 not in part]
        restricted=[[F(A[i][j]+h*B[i][j]) for j in no_three] for i in range(n)]
        assert rank_mod(restricted,prime)==len(no_three)==r
        audits.append({'grade':h,'basis_vectors':len(basis),'evaluated_rank_mod_prime':modrank,
                       'prime':prime,'minor_determinant_points':r+1,'no_three_column_rank_mod_prime':r})
    files=[HERE/'audit.py',HERE/'verification.json',ROOT/'research/charged-cubic-parity/verify.py',
           ROOT/'research/charged-cubic-parity/PROOF.md',ROOT/'research/charged-asymmetric-crossing/model.py',
           *(ROOT/'research/charged-operator-moments'/name for name in ('charged.py','pairing.py','predecessor.py'))]
    print(json.dumps({'audits':audits,'sha256':{str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in files}},indent=2))

if __name__=='__main__':main()
