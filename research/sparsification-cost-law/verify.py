#!/usr/bin/env python3
"""Numerical controls for a specified model; no SAT runtime inference."""
import math

checks = 0
for a,b,beta,c in ((1,1,1,0),(3,2,4,1),(0.1,7,2,5)):
    for lam in (1e4,1e6,1e8,1e10,1e12):
        def cost(s):
            L=math.log(2/s)
            return a*s+b/math.sqrt(lam)*(c*math.log(lam)+beta*(L+math.log(L)))
        def derivative(s):
            L=math.log(2/s)
            return a-b*beta/(s*math.sqrt(lam))*(1+1/L)
        if derivative(1) <= 0:
            continue
        lo,hi=1e-15,1.0
        for _ in range(160):
            mid=(lo+hi)/2
            if derivative(mid)<0:
                lo=mid
            else:
                hi=mid
        s=(lo+hi)/2
        assert abs(derivative(s)) <= 1e-10*max(1,a)
        assert cost(s)<=cost(s*.99) and cost(s)<=cost(s*1.01)
        ratio=a*s*math.sqrt(lam)/(b*beta)
        assert 1 < ratio < 1+1/math.log(2/s)+1e-12
        checks+=1
assert checks>=12
print(f'PASS: {checks} finite optimizer and derivative controls across three coefficient sets')
