"""Explore scalar row spaces under shift-dependent local input maps.

Arguments: grade, cutoff, optional mode ('coefficients' or 'value').
Requires python-flint. Positive cases at grades <=5 additionally solve and
verify every original equation over Q. Modular ranks at larger grades are
screens only; they do not certify rational nonmembership or an all-size bound.
"""
from pathlib import Path
import importlib.util,sys,json,time
from flint import nmod_mat,fmpq_mat
R=Path(__file__).resolve().parents[2]
s=importlib.util.spec_from_file_location('poly',R/'research/charge-polynomial-filter/polynomial.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
h=int(sys.argv[1]);cut=int(sys.argv[2]);kind=sys.argv[3] if len(sys.argv)>3 else 'coefficients'
st=m.model.predecessor.partitions(h);N=len(st);p=65521;names=[];cols=[]
for mu in st:
 for shift in range(-2*h,2*h+1):
  if abs(shift)<=cut:continue
  block=[[0]*(N**3) for _ in range(2*h+1)]
  for v,nu in enumerate(st):
   for y,arg in enumerate(st):
    values=dict(m.piece_vector(mu,nu,arg,shift,reverse=shift<0))
    for u,out in enumerate(st):
     for k,c in enumerate(values.get(out,())):block[k][(v*N+y)*N+u]=c
  if kind=='value':block=[[sum(x) for x in zip(*block)]]
  for k,b in enumerate(block):
   if any(b):names.append((mu,shift,k));cols.append(b)
 m.clear_caches()
 print('input',mu,'vectors',len(cols),file=sys.stderr,flush=True)
targets=[[int(v==x and y==u) for v in range(N) for y in range(N) for u in range(N)] for x in range(N)]
a=nmod_mat([[x%p for x in row] for row in cols],p); ar,rank=a.rref();del a
b=nmod_mat([[x%p for x in row] for row in cols+targets],p);ra=b.rank();del b
res={'h':h,'cutoff':cut,'mode':kind,'N':N,'columns':len(cols),'rank_mod':rank,'augmented_rank_mod':ra,'scalar_row_dimension_mod':rank+N-ra,'full_crossing_mod':rank==ra}
if rank==ra and h<=5:
 erows=[next(j for j in range(N**3) if ar[i,j]) for i in range(rank)]
 small=nmod_mat([[cols[j][i]%p for j in range(len(cols))] for i in erows],p);sr,_=small.rref()
 pivots=[next(j for j in range(len(cols)) if sr[i,j]) for i in range(rank)]
 exact=fmpq_mat([[cols[j][i] for j in pivots] for i in erows])
 rhs=fmpq_mat([[t[i] for t in targets] for i in erows]);sol=exact.solve(rhs)
 ok=all(sum(sol[j,k]*cols[z][i] for j,z in enumerate(pivots))==targets[k][i] for k in range(N) for i in range(N**3))
 res['rational_verified']=ok
 if ok:
  res['weights']=[{'mu':names[z][0],'shift':names[z][1],'degree':names[z][2],'row':[str(sol[j,k]) for k in range(N)]} for j,z in enumerate(pivots) if any(sol[j,k] for k in range(N))]
print(json.dumps(res),flush=True)
