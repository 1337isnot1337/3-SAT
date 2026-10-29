"""Exact exploratory test of three border normalizations.

Usage: python border_probe.py GRADE CUTOFF (requires SymPy).
Uses the predecessor operator recurrence, not an independent oracle.
The listed witness measures a rational function's degree at infinity;
no statement about other filters or growing grades is inferred.
"""
from pathlib import Path
import importlib.util,sys,math,json
import sympy as S
ROOT=Path(__file__).resolve().parents[2]
s=importlib.util.spec_from_file_location('lp',ROOT/'research/length-power-filter/screen.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
h=int(sys.argv[1]);cut=int(sys.argv[2]);labels=m.poly.model.predecessor.partitions(h);N=len(labels);q=S.Symbol('q')
# Full labels, full output. Compare symmetric tails and a root polynomial filter.
raw={}
for sh in range(-2*h,2*h+1):
 if abs(sh)<=cut:continue
 arr={}
 for x,mu in enumerate(labels):
  for v,nu in enumerate(labels):
   for y,arg in enumerate(labels):
    vals=dict(m.poly.piece_vector(mu,nu,arg,sh,reverse=(sh<0)))
    for u,out in enumerate(labels):
     if out in vals:arr[x,v,y,u]=vals[out]
 raw[sh]=arr
print('built',h,file=sys.stderr,flush=True)
for family in ('tails','linear','rooted'):
 B={}
 for sh,arr in raw.items():
  w=1 if family=='tails' else sh if family=='linear' else math.prod(sh-j for j in range(-cut,cut+1))
  for key,poly in arr.items():
   old=B.setdefault(key,[0]*(2*h+1))
   for d,c in enumerate(poly):old[d]+=w*c
 G=S.Matrix(N,N,lambda x,v:sum(c*q**d for d,c in enumerate(B.get((x,v,0,0),[]))))
 det=S.Poly(G.det(method='domain-ge'),q)
 if det.is_zero:
  print(json.dumps({'h':h,'cutoff':cut,'family':family,'invertible_diagonal':False}),flush=True);continue
 adj=G.adjugate(method='domain-ge');dd=det.degree();worst=-10**9;witness=None
 for y in range(N):
  for u in range(N):
   F=S.Matrix(N,N,lambda x,v:sum(c*q**d for d,c in enumerate(B.get((x,v,y,u),[]))))
   if y==u:F-=G
   C=adj*F
   for i in range(N):
    for j in range(N):
     pp=S.Poly(C[i,j],q)
     if not pp.is_zero and pp.degree()-dd>worst:worst=int(pp.degree()-dd);witness=[y,u,i,j]
 print(json.dumps({'h':h,'cutoff':cut,'family':family,'invertible_diagonal':True,'denominator_degree':dd,'largest_error_degree_at_infinity':worst,'witness':witness,'border_crossing':worst<0}),flush=True)
