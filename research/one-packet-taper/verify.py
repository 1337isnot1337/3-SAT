#!/usr/bin/env python3
"""Exact single-packet interpolation and canonical lift checks."""
from fractions import Fraction as F
from math import comb


def mul(p,q):
 r=[F(0)]*(len(p)+len(q)-1)
 for i,x in enumerate(p):
  for j,y in enumerate(q): r[i+j]+=x*y
 return r

def add(p,q):
 r=[F(0)]*max(len(p),len(q))
 for i,x in enumerate(p): r[i]+=x
 for i,x in enumerate(q): r[i]+=x
 return r

def val(p,x): return sum(c*x**i for i,c in enumerate(p))

def shift(p,t,alpha):
 r=[F(0)]*len(p)
 for i,c in enumerate(p):
  for k in range(i+1): r[k]+=c*comb(i,k)*t**(i-k)*alpha**k
 return r

def kernel(L,d):
 p=[F(1)]; den=1
 for t in range(-L,L):
  if t!=d: p=mul(p,[-t,1])
  if t: den*= -t
 return [c/den for c in p]

def reduce2(x,mod):
 x=F(x); assert x.denominator%2
 return x.numerator*pow(x.denominator,-1,mod)%mod

def div_zminus1(p):
 assert sum(p)==0
 q=[F(0)]*(len(p)-1); q[-1]=p[-1]
 for k in range(len(q)-2,-1,-1): q[k]=p[k+1]+q[k+1]
 return q

def mmul(p,q,mod):
 r=[0]*(len(p)+len(q)-1)
 for i,x in enumerate(p):
  for j,y in enumerate(q): r[i+j]=(r[i+j]+x*y)%mod
 return r

def main():
 cases=jet_checks=0
 for L in (2,4,8,16):
  W={d:kernel(L,d) for d in range(-L+1,L)}
  H=[F(1)]
  for t in range(-L,L):
   if t%2: H=mul(H,[F(1),F(-1,t)])
  b0=val(H,-L)
  b=[(val(H,d)-b0)/val(W[d],d) for d in range(-L+1,L)]
  Q=b[:]
  for _ in range(L-1): Q=div_zminus1(Q)
  assert len(Q)==L and all(c.denominator%2 for c in Q)
  R=[F((-1)**(L-1-i)*comb(L-1,i)) for i in range(L)]
  assert mul(R,Q)==b
  A=[R[L-1-x] for x in range(L)]
  B0=1-sum(Q)
  assert B0.denominator%2 and b0.denominator%2
  reconstructed=[b0]
  for d,c in zip(range(-L+1,L),b): reconstructed=add(reconstructed,[c*x for x in W[d]])
  assert reconstructed==H+[F(0)]*(len(reconstructed)-len(H))
  cases+=1
  if L>4: continue
  for prec in range(1,5):
   mod=1<<prec
   row=[reduce2(b0+sum(A[x] for x in range(L) if mask>>x&1),mod) for mask in range(1<<L)]
   cols=[reduce2(B0,mod)]+[reduce2(q,mod) for q in Q]
   for t in range(-L,L):
    Ws={d:[reduce2(c,mod) for c in shift(W[d],t,2*L)] for d in W}
    output=[0]
    for cindex,cb in enumerate(cols):
     zlist=[[0] for _ in range(L)] if cindex==0 else [Ws[(cindex-1)-x] for x in range(L)]
     for mask in range(1<<L):
      term=[1]
      for x,z in enumerate(zlist):
       if mask>>x&1: factor=z
       else:
        factor=[(-v)%mod for v in z]; factor[0]=(factor[0]+1)%mod
       term=mmul(term,factor,mod)
      if len(output)<len(term): output += [0]*(len(term)-len(output))
      for k,z in enumerate(term): output[k]=(output[k]+cb*row[mask]*z)%mod
    expected=[reduce2(x,mod) for x in shift(H,t,2*L)]
    output += [0]*max(0,len(expected)-len(output))
    expected += [0]*max(0,len(output)-len(expected))
    assert output==expected
    jet_checks+=1
 print('PASS:',{'exact_factorizations':cases,'canonical_complete_shifted_jets':jet_checks})

if __name__=='__main__': main()
