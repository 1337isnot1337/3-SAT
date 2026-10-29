#!/usr/bin/env python3
"""Check row-survival counts and extreme-node forcing for all small pairs."""
pairs=0
for L in (2,4,8,16):
    S=range(-L,L)
    for y1 in range(L):
        for y2 in range(L):
            shifts=[y-x for y in (y1,y2) for x in range(L)]
            r={t:shifts.count(t) for t in S}
            assert sum(r.values())==2*L and max(r.values())<=2
            assert sum(3-r[t] for t in S)==4*L
            assert r[-L]==0
            assert bool(r[L-1]) == (y1==L-1 or y2==L-1)
            assert bool(r[-L+1]) == (y1==0 or y2==0)
            if r[L-1] and r[-L+1]: assert {y1,y2}=={0,L-1}
            pairs+=1
print(f'PASS: {pairs} one-hot column pairs, divisor degrees and endpoint forcing')
