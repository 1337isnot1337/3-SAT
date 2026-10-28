#!/usr/bin/env python3
"""Finite F2 checks plus exact Cauchy-node controls; standard library only."""
from fractions import Fraction as F
from math import comb


def mul(p,q):
    r=[F(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q): r[i+j]+=x*y
    return r


def shift(p,t,alpha):
    r=[F(0)]*len(p)
    for i,c in enumerate(p):
        for k in range(i+1): r[k]+=c*comb(i,k)*t**(i-k)*alpha**k
    return r


def v2(x):
    if not x: return float('inf')
    x=F(x); n,d=abs(x.numerator),x.denominator
    return (n & -n).bit_length() - (d & -d).bit_length()


def kernel(L,d):
    p=[F(1)]; den=1
    for s in range(-L,L):
        if s != d: p=mul(p,[-s,1])
        if s: den*= -s
    return [c/den for c in p]


def poly_mul_binary(a,b):
    p=0
    while b:
        t=b & -b
        p ^= a << (t.bit_length()-1)
        b ^= t
    return p


def main():
    counts={'exact_kernel_jets':0,'onehot_candidates':0,
            'escape_node_checks':0,'polynomial_factor_checks':0,
            'escape_exact_precision_controls':0}
    for a in range(1,4):
        L=1<<a
        W={d:kernel(L,d) for d in range(-L+1,L)}
        for d,p in W.items():
            for t in range(-L,L):
                jet=shift(p,t,2*L)
                assert v2(jet[0])==0 if d==t else not jet[0]
                assert all(v2(x)>=1 for x in jet[1:])
                counts['exact_kernel_jets']+=1
        for u in range(1,a+1):
            step=1<<u
            target=sum(1<<(d+L-1) for d in range(-L+1,L) if d%step)
            first=(1<<(step-1))-1
            second=sum(1<<(step*r) for r in range(2*L//step))
            assert target==poly_mul_binary(first,second)
            # In characteristic two this geometric factor is (1+z)^(2L-step).
            assert second==poly_mul_binary(1, sum((comb(2*L-step,k)%2)<<k for k in range(2*L-step+1)))
            counts['polynomial_factor_checks']+=1
            for col in range(1<<L):
                if col.bit_count()%2 != 1: continue
                for row in range(1<<L):
                    rev=sum(((row>>x)&1)<<(L-1-x) for x in range(L))
                    assert poly_mul_binary(rev,col) != target
                    counts['onehot_candidates']+=1
        # Exact t=1 value of the zero-plus-one-hot Boolean escape.
        w = shift(W[1], 1, 2*L)[0]
        assert w == F(-(L+1), L-1)
        value = 2 + (L-1)*(1-w)
        assert value == 2*(L+1) and v2(value)==1
        counts['escape_exact_precision_controls'] += 1
        # A(Y)=1+sum Y mod 2, B=1 on the all-zero and one-hot inputs.
        for t in range(-L,L):
            result=1  # all-zero column input gives Y=0
            for y in range(L):
                bits=[int(y-x==t) for x in range(L)]
                result ^= 1 ^ (sum(bits)%2)
            assert result == int(t%2==0)
            counts['escape_node_checks']+=1
    print('PASS:',counts)


if __name__=='__main__': main()
