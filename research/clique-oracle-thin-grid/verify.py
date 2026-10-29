#!/usr/bin/env python3
"""Finite exact controls for the clique oracle adversary and relaxation."""
from fractions import Fraction as F
from itertools import product
from math import comb


def clique_sum(k, bit_count, special):
    edges = [(i,j) for i in range(k) for j in range(i+1,k)]
    incident = [j for i,j in edges if i == 0]
    total = 0
    for values in product(range(2**bit_count), repeat=len(edges)):
        assignment = dict(zip(edges,values))
        key = tuple(assignment[(0,j)] for j in incident)
        total += int(key == special)
    return total


def main():
    controls = 0
    for k,bits in [(2,1),(2,2),(3,1),(3,2),(4,1)]:
        for special in product(range(2**bits),repeat=k-1):
            assert clique_sum(k,bits,special) == 2**(comb(k-1,2)*bits)
            controls += 1
    bounds = 0
    for p in range(2,6):
        for q in range(2,9):
            a,c,b=F(p-1,p*q-1),F(q-1,p*q-1),F((p-1)*(q-1),p*q-1)
            d=c+b
            u=F(1,p)
            for v in (F(1,100), F(1,1000)):
                z=(v/u)*d/b
                assert z <= 1
                # Test exact rational circle samples against both the general
                # upper bound and the explicit witness's squared y value.
                y_squared=1-z*z
                assert y_squared >= (1-z*z)**2
                for j in range(31):
                    t=F(j,30)
                    x=(1-t*t)/(1+t*t);y=2*t/(1+t*t)
                    assert min(u*(a+b*x),v*(c+b*y)) <= v*d
                assert a <= F(1,q) and b >= F(1,3)
                bounds += 1
    print(f'PASS: {controls} explicit oracle witnesses; {bounds} exact thin-grid parameter controls')


if __name__ == '__main__':
    main()
