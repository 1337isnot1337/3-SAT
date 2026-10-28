#!/usr/bin/env python3
"""Exact hit and coefficient bounds for finite near-one examples."""
import importlib.util
from fractions import Fraction
from itertools import product
from math import log, ceil
from pathlib import Path
spec=importlib.util.spec_from_file_location('bias',Path(__file__).with_name('verify_bias.py'))
bias=importlib.util.module_from_spec(spec)
spec.loader.exec_module(bias)
hits=roots=0
for q,p,t in ((8,1,8),(16,1,8),(16,2,8)):
    L=t*p
    r=(q-1).bit_length()
    mod=bias.modulus(r)
    for support in range(1,1<<q):
        if support.bit_count()*p < q:
            continue
        count=0
        for a,b in product(range(q),repeat=2):
            count+=any(support >> (bias.multiply(a,j,mod,r)^b) & 1 for j in range(L))
        assert Fraction(count,q*q) >= Fraction(t,t+2)
        hits+=1
    Q=1 << (t*L-1).bit_length()
    f=bias.modulus((Q-1).bit_length())
    for mask in (1,(1<<L)-1,sum(1<<j for j in range(0,L,2))):
        zeros=0
        for x in range(Q):
            val=0
            power=1
            for j in range(L):
                if mask>>j&1:
                    val ^= power
                power=bias.multiply(power,x,f,(Q-1).bit_length())
            zeros+=val==0
        assert Fraction(Q-zeros,2*Q) >= Fraction(t-1,2*t)
        roots+=1
for t in (8,9,16,64,1000):
    rho=Fraction(t+5,2*(t+2))
    for n in (1,2,17,1000,100000):
        T=n+ceil(32*n/t)+1
        assert n*log(2)+T*log(float(rho)) < 0
print(f'PASS: {hits} affine support cases, {roots} coefficient root cases, 25 round-budget controls')
