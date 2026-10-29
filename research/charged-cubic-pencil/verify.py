#!/usr/bin/env python3
"""Exact finite polynomial-kernel certificates for the cubic energy pencil."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import importlib.util
import json
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    spec.loader.exec_module(module)
    return module

control=load('pencil_control',ROOT/'research/charged-cubic-parity/kernel_control.py')
v=control.v


def equations(A,B,degree):
    n=len(A);width=(degree+1)*n;rows=[]
    for t in range(degree+2):
        for i in range(n):
            row=[0]*width
            if t<=degree:row[t*n:(t+1)*n]=A[i][:]
            if t>=1:row[(t-1)*n:t*n]=B[i][:]
            rows.append(row)
    return rows


def determinant(matrix):
    rows=[row[:] for row in matrix]
    n=len(rows); sign=1; previous=1
    for k in range(n-1):
        pivot=next((i for i in range(k,n) if rows[i][k]),None)
        if pivot is None:return 0
        if pivot!=k:
            rows[k],rows[pivot]=rows[pivot],rows[k]
            sign=-sign
        value=rows[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator=rows[i][j]*value-rows[i][k]*rows[k][j]
                assert numerator%previous==0
                rows[i][j]=numerator//previous
        previous=value
        for i in range(k+1,n):rows[i][k]=0
    return sign*rows[-1][-1]


def interpolate(values):
    differences=[]
    row=values[:]
    while row:
        differences.append(row[0])
        row=[row[i+1]-row[i] for i in range(len(row)-1)]
    result=[F(0)]*len(values); basis=[F(1)]
    for k,coefficient in enumerate(differences):
        for j,value in enumerate(basis):result[j]+=coefficient*value
        next_basis=[F(0)]*(len(basis)+1)
        for j,value in enumerate(basis):
            next_basis[j]-=value*k/F(k+1)
            next_basis[j+1]+=value/F(k+1)
        basis=next_basis
    assert all(x.denominator==1 for x in result)
    return [int(x) for x in result]


def minor_certificate(A,B,h,matrix_h,matrix_rank):
    row_ids,col_ids=v.model.minor_indices(matrix_h,matrix_rank)
    def value(energy):
        return determinant([[A[i][j]+energy*B[i][j] for j in col_ids] for i in row_ids])
    values=[value(energy) for energy in range(matrix_rank+1)]
    coeff=interpolate(values)
    assert sum(c*(matrix_rank+1)**i for i,c in enumerate(coeff))==value(matrix_rank+1)
    signs=[1 if c>0 else -1 for c in coeff if c]
    assert coeff[0]!=0
    if h==7:
        assert signs[0]==-1 and signs[-1]==1
        assert sum(signs[i]!=signs[i-1] for i in range(1,len(signs)))==1
        assert value(0)<0 and value(1)>0
        certificate='one positive root between 0 and 1 by Descartes; nonzero at all integer energies >=0'
    else:
        assert all(sign==signs[0] for sign in signs)
        certificate='all nonzero coefficients have one sign; nonzero at all real energies >=0'
    return {'row_indices':row_ids,'column_indices':col_ids,
            'coefficients_low_degree_first':[str(x) for x in coeff],
            'nonnegative_energy_certificate':certificate}


def calc(h):
    labels=v.model.predecessor.partitions(h);n=len(labels);A=[];B=[]
    for a in labels:
        row0=[];row1=[]
        for b in labels:
            f0=v.cubic(a,b,()).get((),0)
            f1=v.cubic(a,b,(1,)).get((1,),0)
            row0.append(f0);row1.append(f1-f0)
        A.append(row0);B.append(row1)
    bases=[]
    for degree in (0,1,2):
        rows=equations(A,B,degree)
        basis=control.nullspace(rows)
        assert all(sum(x*y for x,y in zip(row,b))==0 for row in rows for b in basis)
        bases.append(basis)
    evaluation=[[sum(b[k*n+i]*h**k for k in range(3)) for i in range(n)] for b in bases[2]]
    eval_rank=v.rank(evaluation)
    matrix_h=[[x+h*y for x,y in zip(a,b)] for a,b in zip(A,B)]
    matrix_rank=v.rank(matrix_h)
    no_three=[j for j,label in enumerate(labels) if 3 not in label]
    restricted_rank=v.rank([[row[j] for j in no_three] for row in matrix_h])
    assert restricted_rank==len(no_three)==matrix_rank
    assert eval_rank==n-matrix_rank
    assert all(sum(x*y for x,y in zip(row,b))==0 for row in matrix_h for b in evaluation)
    encoded=json.dumps([[[str(x) for x in b] for b in base] for base in bases],separators=(',',':'))
    minor=minor_certificate(A,B,h,matrix_h,matrix_rank)
    return {'grade':h,'dimension':n,'polynomial_nullities_degree_0_1_2':[len(x) for x in bases],
            'specialization_energy':h,'evaluated_kernel_rank':eval_rank,'matrix_rank_at_specialization':matrix_rank,
            'columns_without_part_three':len(no_three),'restricted_column_rank_at_specialization':restricted_rank,
            'basis_sha256':sha256(encoded.encode()).hexdigest(),
            'degree_two_basis':[[str(x) for x in vector] for vector in bases[2]],'minor':minor}


def main():
    results=[calc(h) for h in (6,7,8,9)]
    assert [x['polynomial_nullities_degree_0_1_2'] for x in results]==[[0,0,3],[0,0,5],[0,0,7],[1,3,14]]
    assert [x['matrix_rank_at_specialization'] for x in results]==[8,10,15,19]
    files=[HERE/'verify.py',ROOT/'research/charged-cubic-parity/kernel_control.py',
           ROOT/'research/charged-cubic-parity/verify.py',ROOT/'research/charged-cubic-parity/PROOF.md',
           ROOT/'research/charged-asymmetric-crossing/model.py',
           *(ROOT/'research/charged-operator-moments'/name for name in ('charged.py','pairing.py','predecessor.py'))]
    print(json.dumps({'scope':'Exact polynomial-kernel computation over Q, using the predecessor affine-energy identity',
                      'results':results,'sha256':{str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in files}},indent=2))

if __name__=='__main__':main()
