#!/usr/bin/env python3
"""Exhaust four-state output codebooks with exact modular certificates."""
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('linear', HERE / 'linear.py')
linear = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = linear
spec.loader.exec_module(linear)
model = linear.model
PRIME = 1000003


def mod_value(x):
    x = Fraction(x)
    return x.numerator % PRIME * pow(x.denominator, -1, PRIME) % PRIME


def full_column_rank_mod(rows, n):
    pivots = {}
    for row in rows:
        v = [mod_value(x) for x in row]
        for j in sorted(pivots):
            if v[j]:
                scale = v[j]
                v = [(x-scale*y) % PRIME for x,y in zip(v,pivots[j])]
        j = next((i for i,x in enumerate(v) if x), None)
        if j is None:
            continue
        scale = pow(v[j], -1, PRIME)
        pivots[j] = [(x*scale) % PRIME for x in v]
        if len(pivots) == n:
            return True
    return False


def main():
    data = model.construct(2)
    n,h = data['N'],data['h']
    states = data['states']
    assert (n,h,len(states)) == (4,6,11)
    shifts = [s for s in range(-2*h,2*h+1) if abs(s)>=2]
    # tensor[a][v][y][u][s], where outputs range over ALL partitions of h.
    tensor = [[[[[None for s in shifts] for u in states] for y in states]
              for v in range(n)] for a in range(n)]
    for a,mu in enumerate(data['row_labels']):
        for v,nu in enumerate(data['column_labels']):
            for y,arg in enumerate(states):
                for k,s in enumerate(shifts):
                    out = dict(model.charged.piece_vector(mu,nu,arg,s,1))
                    for u,state in enumerate(states):
                        tensor[a][v][y][u][k] = out.get(state,0)
    full_mod=0
    exceptional=[]
    for code in combinations(range(len(states)),n):
        anchor=code[0]
        constraints=[]
        pairing=[]
        for a in range(n):
            for v in range(n):
                anchor_row=tensor[a][v][anchor][anchor]
                pairing.append(anchor_row)
                for y in code:
                    for u in code:
                        if u != y:
                            constraints.append(tensor[a][v][y][u])
                        elif y != anchor:
                            constraints.append([x-z for x,z in zip(tensor[a][v][y][u],anchor_row)])
        if full_column_rank_mod(constraints,len(shifts)):
            full_mod+=1
            continue
        basis=linear.nullspace(constraints,len(shifts))
        images=[[sum(row[k]*b[k] for k in range(len(shifts))) for row in pairing] for b in basis]
        image_dimension=linear.matrix_rank(images)
        ranks=[linear.matrix_rank([im[i*n:(i+1)*n] for i in range(n)]) for im in images]
        assert len(basis) == 1 and image_dimension == 1 and ranks == [n]
        witness = linear.integers(basis[0])
        assert all(sum(row[k]*witness[k] for k in range(len(shifts))) == 0 for row in constraints)
        flat = [sum(row[k]*witness[k] for k in range(len(shifts))) for row in pairing]
        witness_matrix = [flat[i*n:(i+1)*n] for i in range(n)]
        assert linear.matrix_rank(witness_matrix) == n
        exceptional.append({'indices':code,'states':[states[i] for i in code],
                            'nullity':len(basis),'pairing_image_dimension':image_dimension,
                            'pairing_rank':ranks[0], 'weight_vector':witness,
                            'pairing_matrix':[[str(x) for x in row] for row in witness_matrix],
                            'vanishes_at_minus_and_plus_2':witness[shifts.index(-2)] == witness[shifts.index(2)] == 0})
    assert full_mod == 296 and len(exceptional) == 34
    cubic = [(s**3-s)//6 for s in shifts]
    assert all(e['weight_vector'] == cubic and not e['vanishes_at_minus_and_plus_2'] for e in exceptional)
    # Independent order control for the first retained output codebook.
    first = exceptional[0]['indices']
    reverse_checks = 0
    for a,mu in enumerate(data['row_labels']):
        for v,nu in enumerate(data['column_labels']):
            for y in first:
                for s in shifts:
                    forward = model.charged.piece_vector(mu,nu,states[y],s,1)
                    reverse = model.charged.piece_vector(mu,nu,states[y],s,1,reverse=True)
                    assert forward == reverse
                    reverse_checks += 1
    assert reverse_checks == n*n*n*len(shifts)
    files=[HERE / 'codebooks.py', HERE / 'linear.py',
           HERE.parent / 'charged-asymmetric-crossing/model.py',
           *(HERE.parent / 'charged-operator-moments' / name for name in
             ('charged.py','pairing.py','predecessor.py'))]
    print(json.dumps({'prime':PRIME,'grade':h,'input_dimension':n,'states':states,
                      'row_labels':data['row_labels'],'column_labels':data['column_labels'],
                      'active_shifts':shifts,'codebooks':full_mod+len(exceptional),
                      'full_column_rank_mod_prime':full_mod,'reverse_order_vector_checks':reverse_checks,
                      'exact_exceptions':exceptional,
                      'sha256':{str(p.relative_to(HERE.parents[1])):sha256(p.read_bytes()).hexdigest() for p in files}},indent=2))


if __name__ == '__main__':
    main()
