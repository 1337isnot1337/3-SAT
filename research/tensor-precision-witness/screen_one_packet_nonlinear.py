#!/usr/bin/env python3
"""Exact rational screen for fixed columns and arbitrary one-packet row tensors."""
from fractions import Fraction as Q
from math import factorial
import runpy
from pathlib import Path
f=runpy.run_path(str(Path(__file__).with_name('verify.py')));mul,add=f['mul'],f['add']
for L in (2,4):
 S=range(-L,L);den=(-1)**(L-1)*factorial(L)*factorial(L-1)
 ws={}
 for d in range(-L+1,L):
  w=[Q(1)]
  for t in S:
   if t!=d:w=mul(w,[Q(-t),Q(1)])
  ws[d]=[x/den for x in w]
 H=[Q(1)]
 for t in S:
  if t and t%2:H=mul(H,[Q(1),Q(-1,t)])
 counts=[0]*L
 for mask in range(1<<L):
  z=[]
  for x in range(L):
   p=[Q(0)]
   for y in range(L):
    if mask>>y&1:p=add(p,ws[y-x])
   z.append(p)
  cols=[[Q(1)]]
  for w in z:cols +=[mul(p,w) for p in cols]
  dim=max(map(len,cols));basis={}
  for col in cols:
   v=col+[Q(0)]*(dim-len(col))
   for p,b in sorted(basis.items()):
    t=v[p]
    if t:v=[x-t*y for x,y in zip(v,b)]
   pivot=next((i for i,x in enumerate(v) if x),None)
   if pivot is not None:
    t=v[pivot];basis[pivot]=[x/t for x in v]
  t=[Q(1)]
  for power in range(1,L+1):
   t=mul(t,H)
   if len(t)>dim:continue
   v=t+[Q(0)]*(dim-len(t))
   for p,b in sorted(basis.items()):
    t0=v[p]
    if t0:v=[x-t0*y for x,y in zip(v,b)]
   if not any(v):counts[power-1]+=1
 assert counts == [0]*L
 print('L',L,'masks',2**L,'successful counts for powers 1..L',counts,flush=True)
