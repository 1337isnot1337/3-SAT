#!/usr/bin/env python3
"""All coordinate output codebooks for the fixed grade-six cubic moment."""
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('linear', HERE / 'linear.py')
linear=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=linear
spec.loader.exec_module(linear)
model=linear.model


def main():
    data=model.construct(2)
    states=data['states']
    n,h=data['N'],data['h']
    assert (n,h,len(states)) == (4,6,11)
    shifts=[s for s in range(-2*h,2*h+1) if abs(s)>=2]
    operators={}
    for a,mu in enumerate(data['row_labels']):
        for v,nu in enumerate(data['column_labels']):
            for y,arg in enumerate(states):
                totals={}
                for s in shifts:
                    weight=(s**3-s)//6
                    for out,c in model.charged.piece_vector(mu,nu,arg,s,1):
                        totals[out]=totals.get(out,0)+weight*c
                for u,out in enumerate(states):
                    operators[a,v,y,u]=totals.get(out,0)
    diag={y:tuple(operators[a,v,y,y] for a in range(n) for v in range(n)) for y in range(len(states))}
    edges=[]
    for y,u in combinations(range(len(states)),2):
        if diag[y] == diag[u] and all(operators[a,v,y,u] == operators[a,v,u,y] == 0
                                      for a in range(n) for v in range(n)):
            edges.append((y,u))
    edge_set=set(edges)
    def merged(partition):
        results=set()
        for i,j in combinations(range(len(partition)),2):
            parts=[v for k,v in enumerate(partition) if k not in (i,j)]
            results.add(tuple(sorted(parts+[partition[i]+partition[j]],reverse=True)))
        return results
    missing={(y,u) for y,u in combinations(range(len(states)),2) if (y,u) not in edge_set}
    single_merge={(y,u) for y,u in combinations(range(len(states)),2)
                  if states[u] in merged(states[y]) or states[y] in merged(states[u])}
    assert missing == single_merge
    codebooks=[]
    for size in range(1,len(states)+1):
        for subset in combinations(range(len(states)),size):
            if all((a,b) in edge_set for a,b in combinations(subset,2)):
                d=diag[subset[0]]
                rank=linear.matrix_rank([d[i*n:(i+1)*n] for i in range(n)])
                codebooks.append({'indices':subset,'size':size,'pairing_rank':rank})
    maximal=[c for c in codebooks if not any(set(c['indices']) < set(d['indices']) for d in codebooks)]
    counts={str(k):sum(c['size']==k for c in codebooks) for k in range(1,len(states)+1)}
    full_counts={str(k):sum(c['size']==k and c['pairing_rank']==n for c in codebooks) for k in range(1,len(states)+1)}
    assert len(edges) == 38
    assert [int(counts[str(k)]) for k in range(1,12)] == [11,38,54,34,9,1,0,0,0,0,0]
    assert counts == full_counts
    paths=[HERE/'cubic_graph.py',HERE/'linear.py',HERE.parent/'charged-asymmetric-crossing/model.py',
           *(HERE.parent/'charged-operator-moments'/name for name in ('charged.py','pairing.py','predecessor.py'))]
    print(json.dumps({'grade':h,'input_labels':n,'states':states,'edges':edges,
                      'counts_by_size':counts,'full_pairing_counts_by_size':full_counts,
                      'nonedges_are_exactly_single_merges':True,
                      'maximal_codebooks':maximal,
                      'sha256':{str(p.relative_to(HERE.parents[1])):sha256(p.read_bytes()).hexdigest() for p in paths}},indent=2))

if __name__ == '__main__':
    main()
