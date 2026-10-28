#!/usr/bin/env python3
"""Exact finite full-label pairing ranks via the two-energy identity."""
from hashlib import sha256
from pathlib import Path
import importlib.util
import json
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('parity_verify',HERE/'verify.py')
verify=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=verify
spec.loader.exec_module(verify)


def main():
    results=[]
    for h in (7,8,9,10):
        labels=verify.model.predecessor.partitions(h)
        matrix=[]
        for mu in labels:
            row=[]
            for nu in labels:
                f0=verify.cubic(mu,nu,()).get((),0)
                f1=verify.cubic(mu,nu,(1,)).get((1,),0)
                row.append((1-h)*f0+h*f1)
            matrix.append(row)
        digest=sha256(json.dumps(matrix,separators=(',',':')).encode()).hexdigest()
        results.append({'grade':h,'dimension':len(labels),'rank':verify.rank(matrix),
                        'matrix_sha256':digest})
    assert [(r['dimension'],r['rank']) for r in results]==[(15,10),(22,15),(30,19),(42,27)]
    files=[HERE/'rank_screen.py',HERE/'verify.py',HERE/'PROOF.md',
           ROOT/'research/charged-asymmetric-crossing/model.py',
           *(ROOT/'research/charged-operator-moments'/name for name in
             ('charged.py','pairing.py','predecessor.py'))]
    print(json.dumps({'scope':'E=h pairing reconstructed from E=0,1 using the written affine-energy argument; no all-grade rank claim',
                      'results':results,
                      'sha256':{str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in files}},indent=2))

if __name__=='__main__':main()
