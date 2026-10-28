#!/usr/bin/env python3
"""Exact finite checks of simultaneous zero-mode compression."""
from pathlib import Path
from fractions import Fraction
from itertools import combinations
from hashlib import sha256
import importlib.util
import json
import sys

ROOT=Path(__file__).resolve().parents[2]
path=ROOT/'research/charged-asymmetric-crossing/model.py'
spec=importlib.util.spec_from_file_location('codebook_model',path)
model=importlib.util.module_from_spec(spec);sys.modules[spec.name]=model;spec.loader.exec_module(model)
partitions=model.predecessor.partitions
charged=model.charged


def exact_rank(rows):
    matrix=[[Fraction(x) for x in row] for row in rows]
    n=len(matrix); r=0
    for j in range(n):
        pivot=next((i for i in range(r,n) if matrix[i][j]),None)
        if pivot is None:
            continue
        matrix[r],matrix[pivot]=matrix[pivot],matrix[r]
        p=matrix[r][j]
        matrix[r]=[x/p for x in matrix[r]]
        for i in range(r+1,n):
            p=matrix[i][j]
            if p:
                matrix[i]=[x-p*y for x,y in zip(matrix[i],matrix[r])]
        r+=1
    return r


def construct(E,d,q):
    states=list(partitions(E))
    fields=[a for r in range(d+1) for a in partitions(r)]
    vectors={(i,a):dict(charged.operator(a,0,st,q))
             for i,st in enumerate(states) for a in fields}
    signatures={}
    for i,st in enumerate(states):
        signature=tuple(vectors[i,a].get(st,0) for a in fields)
        signatures.setdefault(signature,[]).append(i)
    # Deterministic largest class, ties settled by insertion order.
    candidates=max(signatures.values(),key=len)
    chosen=[]
    for i in candidates:
        if all(not any(vectors[i,a].get(states[j],0) or
                       vectors[j,a].get(states[i],0) for a in fields)
               for j in chosen):
            chosen.append(i)
    for i in chosen:
        for j in chosen:
            for a in fields:
                val=vectors[i,a].get(states[j],0)
                assert val == (vectors[chosen[0],a].get(states[chosen[0]],0) if i==j else 0)
    return states,fields,chosen,vectors


def main():
    cases=[]; comparisons=0; max_zero_modes=0
    for E in range(1,8):
        for d in (1,3,4):
            states,fields,chosen,vectors=construct(E,d,1)
            # Direct independent operator expansion for a smaller registered domain.
            if E<=4:
                for i,s in enumerate(states):
                    for a in fields:
                        assert vectors[i,a]==dict(charged.direct_operator(a,0,s,1))
                        comparisons+=1
            B=((2*E+1)*(E+d)*(E*E+2))**d
            assert len(chosen)*(2*B+1)**len(fields)*(1+2*len(fields)*(2*E+1)**d)>=len(states)
            max_zero_modes=max(max_zero_modes,len(fields))
            cases.append({'E':E,'d':d,'states':len(states),'fields':len(fields),'selected':len(chosen)})
    # Test actual crossing moment filters, not just their candidate mode span.
    filter_checks=0
    for h,E,d in ((2,3,3),(3,3,3),(2,4,5),(3,4,5)):
        states,fields,chosen,_=construct(E,d,1)
        for mu in partitions(h):
            for nu in partitions(h):
                diagonals=[]
                for i in chosen:
                    values={}
                    for shift in range(-(E+h),E+h+1):
                        weight=shift
                        for j in range(1,(d-1)//2+1):
                            weight *= shift*shift-j*j
                        if weight:
                            for out,value in charged.piece_vector(mu,nu,states[i],shift,1):
                                values[out]=values.get(out,0)+weight*value
                    diagonals.append(values.get(states[i],0))
                    for j in chosen:
                        if i!=j:
                            assert values.get(states[j],0)==0
                    filter_checks+=1
                assert len(set(diagonals))<=1
    rank_cases=[]
    for h in range(2,7):
        states,_,chosen,_=construct(h,5,1)
        st=states[chosen[0]]
        labels=partitions(h)
        matrix=[]
        for mu in labels:
            row=[]
            for nu in labels:
                value=0
                for shift in range(-2*h,2*h+1):
                    weight=shift*(shift*shift-1)*(shift*shift-4)
                    if weight:
                        value+=weight*dict(charged.piece_vector(mu,nu,st,shift,1)).get(st,0)
                row.append(value)
            matrix.append(row)
        rank_cases.append({'h':h,'output_states':len(chosen),'input_labels':len(labels),
                           'rank':exact_rank(matrix)})
    assert [x['rank'] for x in rank_cases]==[2,2,5,6,10]
    print(json.dumps({'cases':cases,'direct_operator_comparisons':comparisons,
        'degree_five_pairing_ranks':rank_cases,
        'actual_filter_diagonal_checks':filter_checks,
        'largest_zero_mode_family':max_zero_modes,'predecessor_model_sha256':sha256(path.read_bytes()).hexdigest(),
        'status':'PASS'},indent=2))

if __name__=='__main__':main()
