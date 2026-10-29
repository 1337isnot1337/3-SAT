#!/usr/bin/env python3
"""Larger finite label-rank screen via the predecessor two-energy identity."""
from hashlib import sha256
from pathlib import Path
import importlib.util
import json
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('parity',ROOT/'research/charged-cubic-parity/verify.py')
v=importlib.util.module_from_spec(spec);sys.modules[spec.name]=v;spec.loader.exec_module(v)


def main():
    h=11;labels=v.model.predecessor.partitions(h);n=len(labels);matrix=[]
    for i,mu in enumerate(labels):
        row=[]
        for nu in labels:
            f0=v.cubic(mu,nu,()).get((),0);f1=v.cubic(mu,nu,(1,)).get((1,),0)
            row.append((1-h)*f0+h*f1)
        matrix.append(row)
        print('row',i+1,'of',n,file=sys.stderr,flush=True)
    rank=v.rank(matrix)
    subset=[j for j,part in enumerate(labels) if 3 not in part]
    restricted=v.rank([[row[j] for j in subset] for row in matrix])
    assert (n,rank,len(subset),restricted)==(56,34,34,34)
    digest=sha256(json.dumps(matrix,separators=(',',':')).encode()).hexdigest()
    files=[HERE/'grade11.py',ROOT/'research/charged-cubic-parity/verify.py',
           ROOT/'research/charged-cubic-parity/PROOF.md',ROOT/'research/charged-asymmetric-crossing/model.py',
           *(ROOT/'research/charged-operator-moments'/name for name in ('charged.py','pairing.py','predecessor.py'))]
    print(json.dumps({'grade':h,'dimension':n,'energy':h,'rank':rank,'no_three_columns':len(subset),
                      'no_three_column_rank':restricted,'matrix_sha256':digest,
                      'scope':'Interpolated E=h pairing; identification uses the predecessor affine-energy proof',
                      'sha256':{str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in files}},indent=2))

if __name__=='__main__':main()
