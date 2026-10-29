#!/usr/bin/env python3
"""Exact arithmetic controls on retuned all-size parameter inequalities."""
from fractions import Fraction
checks=q1=qmany=0
for B in (1, 2, 3, 10, 100):
    for exponent in range(0, 121):
        for offset in (0, -1):
            m=max(1,(1 << exponent)+offset)
            mu=m.bit_length()
            t=(B*mu+1).bit_length() # ceil(log2(B*mu+2))
            R=64+8*t
            P=20000*B*B*R*R
            D=320000*B*B*R*R*mu
            d=min(m,D)
            q=1
            while q*d<m:
                q*=2
            r=(d-1).bit_length()
            h=(d+100*B*R-1)//(100*B*R)-1
            c=(d+8*B-1)//(8*B)
            assert r<=R and q*d>=m and q*d<2*m
            assert r*h <= c
            assert Fraction(2*q*r*h,1) < Fraction(m,25*B) if h else r*h == 0
            assert Fraction(1,100*B*R)*Fraction(1,200*B*R) == Fraction(1,P)
            if q>1:
                assert d==D and q<m and 2*q*c < Fraction(m,B)
                assert Fraction(d,4*(200*B*R)**2)==2*mu
                qmany+=1
            else:
                assert 2*c <= Fraction(m,4*B)+2
                q1+=1
            checks+=1
print(f'PASS: {checks} integer parameter cases, q=1: {q1}, q>1: {qmany}; field degree, row, mixing and potential bounds')
