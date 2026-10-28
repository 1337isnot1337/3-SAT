#!/usr/bin/env python3
"""Exact scalar leading-charge formula and finite crossing certificates."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import importlib.util
import json
import math
import sys

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
path=ROOT/'research/charged-asymmetric-crossing/model.py'
spec=importlib.util.spec_from_file_location('model',path)
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
pair=m.pairing


def rank(matrix):
    rows=[[F(x) for x in row] for row in matrix];r=0
    for j in range(len(rows[0])):
        pivot=next((i for i in range(r,len(rows)) if rows[i][j]),None)
        if pivot is None:continue
        rows[r],rows[pivot]=rows[pivot],rows[r];v=rows[r][j]
        for i in range(r+1,len(rows)):
            if rows[i][j]:
                z=rows[i][j]/v
                rows[i]=[x-z*y for x,y in zip(rows[i],rows[r])]
        r+=1
        if r==len(rows):break
    return r


def translate(poly):
    result={};current=poly;degree=0
    while current:
        for part,value in current.items():result[part]=result.get(part,F(0))+value/math.factorial(degree)
        current=pair.L(current);degree+=1
    return result


def multiply_C(poly,h):
    result={}
    for part,value in poly.items():
        for r in range(1,h+1):
            if sum(part)+r<=h:
                key=tuple(sorted(part+(r,),reverse=True))
                result[key]=result.get(key,F(0))+value*(-1)**(r-1)*r
    return result


def column(nu,h):
    result={};ones=nu.count(1)
    for l in range(min(ones,3)+1):
        reduced=nu[:len(nu)-l]
        current=translate({reduced:F(math.comb(ones,l),math.factorial(3-l))})
        for _ in range(3-l):current=multiply_C(current,h)
        for part,value in current.items():
            if sum(part)==h:result[part]=result.get(part,F(0))+value
    return result


def matrix(h):
    labels=m.predecessor.partitions(h)
    columns=[column(nu,h) for nu in labels]
    H=[[math.factorial(h)*F(pair.multiplicity_factorial(mu),pair.multiplicity_factorial(nu))
        *columns[j].get(mu,F(0)) for j,nu in enumerate(labels)] for mu in labels]
    return labels,H


def source_leading(mu,nu,state):
    result={};bound=sum(mu)+sum(state)
    for s in range(-bound,bound+1):
        weight=(s**3-s)//6
        if not weight:continue
        for q,coefficient in ((2,1),(1,-3),(0,3),(-1,-1)):
            for output,value in m.charged.piece_vector(mu,nu,state,s,q):
                result[output]=result.get(output,F(0))+F(weight*coefficient*value,6)
    return {part:value for part,value in result.items() if value}


def main():
    checks=[]
    for h in range(2,7):
        labels,H=matrix(h);vectors=0;entries=0
        energies=(0,1,2) if h<=4 else (0,1)
        for energy in energies:
            states=m.predecessor.partitions(energy)
            for i,mu in enumerate(labels):
                for j,nu in enumerate(labels):
                    for state in states:
                        actual=source_leading(mu,nu,state)
                        expected={state:H[i][j]} if H[i][j] else {}
                        assert actual==expected
                        vectors+=1;entries+=len(states)
        checks.append({'grade':h,'energies':energies,'label_count':len(labels),
                       'full_output_vectors_checked':vectors,'output_entries_covered':entries})
        print('direct grade',h,'checked',file=sys.stderr,flush=True)
    ranks=[]
    for h in range(2,16):
        labels,H=matrix(h);r=rank(H)
        ranks.append({'grade':h,'dimension':len(labels),'rank':r})
        print('rank grade',h,'checked',file=sys.stderr,flush=True)
    labels,H=matrix(9);n=8
    rows,cols=m.minor_indices(H,n)
    minor=[[H[i][j] for j in cols] for i in rows]
    inverse=m.inverse(minor)
    assert all(sum((inverse[i][k]*minor[k][j] for k in range(n)),F(0))==int(i==j)
               for i in range(n) for j in range(n))
    output=labels[:n]
    files=[HERE/'verify.py',HERE/'PROOF.md',path,
           *(ROOT/'research/charged-operator-moments'/name for name in ('charged.py','pairing.py','predecessor.py'))]
    print(json.dumps({'direct_operator_checks':checks,'finite_label_ranks':ranks,
                      'grade9_crossing':{'dimension':n,'row_labels':[labels[i] for i in rows],
                                         'column_labels':[labels[j] for j in cols],'output_labels':output,
                                         'minor':[[str(x) for x in row] for row in minor],
                                         'inverse':[[str(x) for x in row] for row in inverse]},
                      'sha256':{str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in files}},indent=2))

if __name__=='__main__':main()
