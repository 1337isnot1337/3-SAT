#!/usr/bin/env python3
"""Finite exact tests of charged cubic parity compression and label ranks."""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import importlib.util
import json
import sys

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
path=ROOT/'research/charged-asymmetric-crossing/model.py'
spec=importlib.util.spec_from_file_location('model',path)
model=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=model
spec.loader.exec_module(model)


def rank(matrix):
    rows=[[Fraction(v) for v in row] for row in matrix]
    count=0
    for j in range(len(rows[0])):
        k=next((i for i in range(count,len(rows)) if rows[i][j]),None)
        if k is None: continue
        rows[k],rows[count]=rows[count],rows[k]
        pivot=rows[count][j]
        for i in range(count+1,len(rows)):
            if rows[i][j]:
                factor=rows[i][j]/pivot
                rows[i]=[x-factor*y for x,y in zip(rows[i],rows[count])]
        count+=1
        if count==len(rows): break
    return count


def cubic(mu,nu,arg,charge=1):
    bound=sum(mu)+sum(arg)
    result={}
    for s in range(-bound,bound+1):
        w=(s**3-s)//6
        if w:
            for output,value in model.charged.piece_vector(mu,nu,arg,s,charge):
                result[output]=result.get(output,0)+w*value
    return result


def full_test(h,energy,charge=1):
    labels=model.predecessor.partitions(h)
    states=model.predecessor.partitions(energy)
    matrix=[]
    comparisons=0
    for mu in labels:
        row=[]
        for nu in labels:
            scalar=None
            for y in states:
                vector=cubic(mu,nu,y,charge)
                val=vector.get(y,0)
                if scalar is None: scalar=val
                assert val==scalar
                for u in states:
                    if u != y and len(u)%2==len(y)%2:
                        assert vector.get(u,0)==0
                        comparisons+=1
            row.append(scalar)
        matrix.append(row)
    return {'label_grade':h,'output_energy':energy,'charge':charge,'labels':len(labels),
            'output_states':len(states),'scalar_pairing_rank':rank(matrix),
            'offdiagonal_same_parity_checks':comparisons}


def rank_only(h):
    labels=model.predecessor.partitions(h)
    state=(h,)
    matrix=[[cubic(mu,nu,state).get(state,0) for nu in labels] for mu in labels]
    return {'label_grade':h,'labels':len(labels),'scalar_pairing_rank':rank(matrix)}


def affine_test(h):
    labels=model.predecessor.partitions(h)
    for mu in labels:
        for nu in labels:
            f0=cubic(mu,nu,()).get((),0)
            f1=cubic(mu,nu,(1,)).get((1,),0)
            fh=cubic(mu,nu,(h,)).get((h,),0)
            assert fh==(1-h)*f0+h*f1
    return {'label_grade':h,'label_pairs':len(labels)**2}


def zero_mode_check():
    checked=0
    for energy in range(6):
        for state in model.predecessor.partitions(energy):
            for q in (-1,0,1,2):
                expected={state:q**3+6*q*energy}
                counts=Counter(state)
                for r in range(1,energy+1):
                    for t in range(1,energy+1):
                        if counts[r+t]:
                            parts=list(state); parts.remove(r+t); parts.extend((r,t))
                            key=tuple(sorted(parts,reverse=True))
                            expected[key]=expected.get(key,0)+3*(r+t)*counts[r+t]
                        if counts[r] and counts[t]-(r==t)>0:
                            parts=list(state); parts.remove(r); parts.remove(t); parts.append(r+t)
                            key=tuple(sorted(parts,reverse=True))
                            expected[key]=expected.get(key,0)+3*r*t*counts[r]*(counts[t]-(r==t))
                expected={k:v for k,v in expected.items() if v}
                actual=dict(model.charged.direct_operator((1,1,1),0,state,q))
                assert actual == expected
                checked+=1
    return checked


def main():
    direct_zero_mode_checks=zero_mode_check()
    complete=[full_test(h,e) for h,e in [(2,2),(3,2),(3,3),(3,4),(4,4),(5,5)]]
    more_charges=[full_test(3,4,q) for q in (-1,0,2)]
    affine=[affine_test(h) for h in (3,4,5,6)]
    extended=rank_only(6)
    assert [x['scalar_pairing_rank'] for x in complete] == [1,2,2,2,4,5]
    assert extended['scalar_pairing_rank']==8
    paths=[HERE/'verify.py',HERE/'PROOF.md',path,*(ROOT/'research/charged-operator-moments'/name for name in
                                 ('charged.py','pairing.py','predecessor.py'))]
    print(json.dumps({'direct_cubic_zero_mode_checks':direct_zero_mode_checks,'full_parity_compression_tests':complete,'additional_charge_checks':more_charges,'affine_energy_checks':affine,
                      'one_state_rank_only':extended,
                      'sha256':{str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in paths}},indent=2))

if __name__=='__main__': main()
