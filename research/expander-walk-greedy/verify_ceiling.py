#!/usr/bin/env python3
"""Exhaust support-only one-row averaging on small binary cubes."""
from fractions import Fraction
from math import comb
cases=0
for m in range(1,11):
    for P in (4,5,8):
        s=(m+P-1)//P
        supports=[v for v in range(1<<m) if v.bit_count()>=s]
        missing=sum(comb(m,j) for j in range(s))
        assert len(supports)==(1<<m)-missing
        ceiling=Fraction(1<<(m-1),len(supports))
        for row in range(1<<m):
            odd=sum((row&v).bit_count()%2 for v in supports)
            assert Fraction(odd,len(supports))<=ceiling
            cases+=1
print(f'PASS: {cases} binary rows and eligible-support averages')
