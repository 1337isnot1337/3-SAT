#!/usr/bin/env python3
"""Exhaust small linear codes and their Hamming-packing inequalities."""
from math import comb
cases=0
for m in range(1, 6):
    for rows_count in range(0, 4):
        for table in range(1 << (m*rows_count)):
            rows=[(table >> (m*i)) & ((1<<m)-1) for i in range(rows_count)]
            code=[z for z in range(1<<m) if all((z & row).bit_count()%2==0 for row in rows)]
            rank=m-(len(code).bit_length()-1)
            assert len(code)==1 << (m-rank)
            distance=min((z.bit_count() for z in code if z), default=m+1)
            t=(distance-1)//2
            volume=sum(comb(m,j) for j in range(t+1))
            assert len(code)*volume <= 1 << m
            assert volume <= 1 << rank
            cases+=1
print(f'PASS: {cases} binary matrices, exact kernels and Hamming-ball packing')
