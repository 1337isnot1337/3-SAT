#!/usr/bin/env python3
"""Exact endpoint identities and positive-pairing controls at bounded energy."""
from fractions import Fraction
from math import factorial, prod
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'anthropic-operator-ranks'))
from operators import partitions,operator,dual_operator,dual_scale,piece_vector,exact_rank


def positive_definite(matrix):
    # Symmetric exact LDL^T without square roots.
    n=len(matrix)
    lower=[[Fraction(0) for _ in range(n)] for _ in range(n)]
    diag=[Fraction(0) for _ in range(n)]
    for i in range(n):
        lower[i][i]=1
        diag[i]=matrix[i][i]-sum(lower[i][k]**2*diag[k] for k in range(i))
        if diag[i]<=0: return False
        for j in range(i+1,n):
            lower[j][i]=(matrix[j][i]-sum(lower[j][k]*lower[i][k]*diag[k] for k in range(i)))/diag[i]
    return True


def main():
    pairs=0
    for h in range(1,11):
        states=partitions(h)
        M=[[dict(operator(a,-h,b)).get((),0) for b in states] for a in states]
        for i,a in enumerate(states):
            c=dict(dual_operator(a,0,h,()))
            for j,b in enumerate(states):
                z=factorial(h)//dual_scale(b)
                assert M[i][j]==z*c.get(b,0)
                assert len(a)==len(b) or M[i][j]==0
                pairs+=1
        for length in set(map(len,states)):
            ids=[i for i,a in enumerate(states) if len(a)==length]
            G=[[Fraction((-1)**(h-length)*M[i][j],prod(states[i])*prod(states[j]))
                for j in ids] for i in ids]
            assert all(G[i][j]==G[j][i] for i in range(len(ids)) for j in range(len(ids)))
            assert positive_definite(G)
        assert exact_rank(M)==len(states)
    entries=0
    for bits in (1,2,3):
        d=2**bits;h=1
        while len(partitions(h))<d:h+=1
        states=partitions(h)[:d]
        M=[[dict(operator(a,-h,b)).get((),0) for b in states] for a in states]
        C=[[dict(dual_operator(a,0,h,())).get(b,0) for b in states] for a in states]
        for x,a in enumerate(states):
            for v,b in enumerate(states):
                D=dual_scale(b)
                for y,c in enumerate(states):
                    for sign in (-1,1):
                        vec=dict(piece_vector(a,b,c,sign*2*h))
                        for ui,state in enumerate(states):
                            want=((-1)**(h-len(a))*M[x][y]*D*int(ui==v)
                                  if sign==-1 else C[x][ui]*D*M[v][y])
                            assert vec.get(state,0)==want
                            entries+=1
    print(f'PASS: {pairs} exact pairing entries through h=10; {entries} endpoint tensor entries; exact positive-definite blocks')


if __name__=='__main__':main()
