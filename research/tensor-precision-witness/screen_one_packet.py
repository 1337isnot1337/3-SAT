#!/usr/bin/env python3
"""Rational rank screen: one packet, fixed Boolean columns, affine row tensor."""
from fractions import Fraction as Q
from math import factorial

def rank(a):
 a=[row[:] for row in a]; rows=len(a); cols=len(a[0]); k=0
 for j in range(cols):
  piv=next((i for i in range(k,rows) if a[i][j]),None)
  if piv is None: continue
  a[k],a[piv]=a[piv],a[k]; z=a[k][j]; a[k]=[x/z for x in a[k]]
  for i in range(k+1,rows):
   z=a[i][j]
   if z: a[i]=[x-z*y for x,y in zip(a[i],a[k])]
  k+=1
  if k==rows:break
 return k
for L in (2,4,8):
 S=list(range(-L,L)); den=(-1)**(L-1)*factorial(L)*factorial(L-1)
 def h(t):
  q=Q(1)
  for k in S:
   if k%2:q*=Q(k-t,k)
  return q
 def w(d,t):
  if d!=t:return Q(0)
  p=1
  for k in S:
   if k!=t:p*=t-k
  return Q(p,den)
 successes=[]
 for mask in range(1<<L):
  mat=[[Q(1)]+[sum((w(y-x,t) for y in range(L) if mask>>y&1),Q(0)) for x in range(L)] for t in S]
  if rank(mat)==rank([r+[h(t)] for r,t in zip(mat,S)]): successes.append(mask)
 assert not successes
 print('L',L,'column masks',2**L,'realizing masks',len(successes))
