#!/usr/bin/env python3
"""Numerical controls of the exact coefficient recurrence, not its proof."""
import math


def step(p,invq,u,v):
    # a=(p-1)/(p*q-1), evaluated without constructing huge q.
    a=(p-1)*invq/(p-invq)
    b=(1-a)*(p-1)/p
    c=(1-a)/p
    if u*a >= v*(c+b):
        return v*(c+b)
    if u*(a+b) <= v*c:
        return u*(a+b)
    lo,hi=0.0,1.0
    for _ in range(60):
        x=(lo+hi)/2
        if u*(a+b*x) < v*(c+b*math.sqrt(max(0.0,1-x*x))):
            lo=x
        else:
            hi=x
    x=(lo+hi)/2
    return u*(a+b*x)


def main():
    cases=0
    for p,q,u,v in [(2,2,0.5,0.2),(2,2,0.1,3.0),(3,3,0.4,2.0),(7,2,1.3,0.5)]:
        b=(p-1)/p
        invq=1/q
        for n in range(1,10001):
            old=v
            v=step(p,invq,u,v)
            assert 0 < v <= old*(1+1e-14)
            invq/=p
        ratio=n*v*v/(b*u*u)
        assert 0.99 < ratio < 1.01, (p,ratio)
        cases+=1
    print(f'PASS: {cases} 10000-step finite-coefficient float trajectories, asymptotic ratios within 1%')


if __name__ == '__main__':
    main()
