#!/usr/bin/env python3
"""Numerical controls of the limiting recursion, not an all-size proof."""
import math


def step(p, u, v):
    b=(p-1)/p
    c=1/p
    if u*b <= v*c:
        return u*b
    lo,hi=0.0,1.0
    for _ in range(60):
        x=(lo+hi)/2
        if u*b*x < v*(c+b*math.sqrt(max(0.0,1-x*x))):
            lo=x
        else:
            hi=x
    x=(lo+hi)/2
    return u*b*x


def main():
    cases=0
    for p,u,v in [(2,0.5,0.2),(3,0.4,2.0),(7,1.3,0.5),(2,0.1,3.0)]:
        b=(p-1)/p
        previous=v
        for n in range(1,10001):
            v=step(p,u,v)
            assert 0 < v < previous
            previous=v
        ratio=n*v*v/(b*u*u)
        assert 0.99 < ratio < 1.01, (p,ratio)
        cases+=1
    print(f'PASS: {cases} 10000-step float trajectories, asymptotic ratios within 1%')


if __name__ == '__main__':
    main()
