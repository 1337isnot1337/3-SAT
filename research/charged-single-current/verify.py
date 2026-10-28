#!/usr/bin/env python3
"""Bounded operator-vector tests for the single-current moment identity."""
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


def main():
    algebra_checks=0
    for h in range(1,21):
        for k in range(1,h+1):
            total=sum((-1)**(h-1+j-1)*math.comb(h,j)*
                      math.factorial(j+k-1)//(math.factorial(j-1)*math.factorial(k-1))
                      for j in range(1,h+1))
            assert total==k*math.comb(k-1,h-1)
            algebra_checks+=1
    reports=[]
    for h in range(1,7):
        labels=m.predecessor.partitions(h)
        energies=sorted({0,1,2,h})
        charges=(-1,0,1,2) if h<=4 else (0,1)
        vector_checks=0;piece_calls=0
        for energy in energies:
            for state in m.predecessor.partitions(energy):
                for q in charges:
                    for b in labels:
                        moments=[{} for _ in range(h)]
                        for shift in range(-energy-h,energy+h+1):
                            vector=m.charged.piece_vector((h,),b,state,shift,q)
                            piece_calls+=1
                            for d in range(1,h+1):
                                for out,value in vector:
                                    moments[d-1][out]=moments[d-1].get(out,0)+shift**d*value
                        assert all(not any(vec.values()) for vec in moments)
                        vector_checks+=h
        # A concrete nonzero next moment shows the cutoff h cannot generally be extended.
        sharp=m.charged.moment((h,),(h,),(h,),h+1,1)
        expected=math.factorial(h+1)*math.factorial(h)*(1+h*math.comb(2*h-1,h-1)+(-1)**(h-1)*h)
        assert dict(sharp).get((h,),0)==expected and expected>0
        reports.append({'grade':h,'energies':energies,'charges':charges,
                        'complete_vector_identities':vector_checks,'piece_calls':piece_calls,
                        'next_moment_witness':[[list(part),value] for part,value in sharp],
                        'sharpness_formula_value':expected})
        print('grade',h,'completed',file=sys.stderr,flush=True)
    files=[HERE/'verify.py',HERE/'PROOF.md',path,
           *(ROOT/'research/charged-operator-moments'/name for name in ('charged.py','pairing.py','predecessor.py'))]
    print(json.dumps({'binomial_contraction_checks':algebra_checks,'results':reports,
                      'sha256':{str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in files}},indent=2))

if __name__=='__main__':main()
