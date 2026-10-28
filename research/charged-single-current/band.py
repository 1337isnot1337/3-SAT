#!/usr/bin/env python3
"""Bounded complete-vector checks for the input-length moment band."""
from hashlib import sha256
from pathlib import Path
import importlib.util
import json
import sys

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
path=ROOT/'research/charged-asymmetric-crossing/model.py'
spec=importlib.util.spec_from_file_location('model',path)
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)


def main():
    reports=[]
    for h in range(1,6):
        labels=m.predecessor.partitions(h)
        energies=sorted({0,1,h})
        checks=0;pieces=0
        for energy in energies:
            for state in m.predecessor.partitions(energy):
                for q in (0,1):
                    for a in labels:
                        for b in labels:
                            difference=abs(len(a)-len(b))
                            if not difference:continue
                            degree=min(difference-1,3)
                            moments=[{} for _ in range(degree+1)]
                            for shift in range(-energy-h,energy+h+1):
                                vector=m.charged.piece_vector(a,b,state,shift,q);pieces+=1
                                for d in range(degree+1):
                                    scale=shift**d
                                    for out,value in vector:
                                        moments[d][out]=moments[d].get(out,0)+scale*value
                            assert all(not any(row.values()) for row in moments)
                            checks+=degree+1
        reports.append({'grade':h,'energies':energies,'charges':[0,1],
                        'complete_vector_moments':checks,'piece_calls':pieces})
        print('grade',h,'completed',file=sys.stderr,flush=True)
    sharp=m.charged.moment((1,1,1,1),(4,),(4,),3,1)
    assert dict(sharp).get((4,),0)==14400
    files=[HERE/'band.py',HERE/'LENGTH-BAND.md',path,
           *(ROOT/'research/charged-operator-moments'/name for name in ('charged.py','pairing.py','predecessor.py'))]
    print(json.dumps({'results':reports,'boundary_witness':[[list(part),value] for part,value in sharp],
                      'sha256':{str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in files}},indent=2))

if __name__=='__main__':main()
