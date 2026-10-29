from pathlib import Path
import importlib.util,sys,json,math
from flint import nmod_mat,fmpq_mat
R=Path(__file__).resolve().parents[2]
s=importlib.util.spec_from_file_location('lp',R/'research/length-power-filter/screen.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
h=int(sys.argv[1]);cut=int(sys.argv[2]);states=m.poly.model.predecessor.partitions(h);O=len(states)
first=m.poly.model.pairing.first_pairing(states)
N=O-len(m.poly.model.predecessor.partitions(h-1));ri,ci=m.poly.model.minor_indices(first,N)
for length in sorted(set(len(states[i]) for i in ri)):
 if len(sys.argv)>3 and length!=int(sys.argv[3]):continue
 rows=[i for i in ri if len(states[i])==length]
 cols=[i for i in ci if len(states[i])==length-1]
 if not cols:continue
 nr,nc=len(rows),len(cols);d=2*length-1;raw={}
 for shift in range(-2*h,2*h+1):
  if abs(shift)<=cut:continue
  block=[[0]*(nr*nc*O*O) for _ in range(d+1)]
  for x,i in enumerate(rows):
   for v,j in enumerate(cols):
    for y,arg in enumerate(states):
     values=dict(m.poly.piece_vector(states[i],states[j],arg,shift,reverse=(shift<0)))
     for u,out in enumerate(states):
      ix=((x*O+y)*O+u)*nc+v
      for k,c in enumerate(values.get(out,())):block[k][ix]=c
  for k,c in enumerate(block):
   if any(c):raw[k,shift]=c
 m.poly.clear_caches()
 target=[int(first[i][j]) if y==u else 0 for i in rows for y in range(O) for u in range(O) for j in cols]
 names=list(raw);cs=list(raw.values());p=65521
 a=nmod_mat([[int(v)%p for v in c] for c in cs],p)
 b=nmod_mat([[int(v)%p for v in c] for c in cs+[target]],p)
 r=a.rank();ra=b.rank();result={'h':h,'cutoff':cut,'length':length,'rows':[states[i] for i in rows],'cols':[states[i] for i in cols],'dimensions':[nr,nc,O],'columns':len(cs),'rank_mod':r,'augmented_rank_mod':ra,'member_mod':r==ra}
 tracefree=[]
 for x in range(nr):
  for v in range(nc):
   ref=((x*O)*O)*nc+v
   for y in range(O):
    for u in range(O):
     if y==u==0:continue
     ix=((x*O+y)*O+u)*nc+v
     tracefree.append([(c[ix]-(c[ref] if y==u else 0))%p for c in cs])
 kern,nullity=nmod_mat(tracefree,p).nullspace()
 pairings=[]
 for z in range(nullity):
  entry=[sum(cs[j][((x*O)*O)*nc+v]*int(kern[j,z]) for j in range(len(cs)))%p for x in range(nr) for v in range(nc)]
  if any(entry):pairings.append(entry)
 pr=nmod_mat(pairings,p).rref() if pairings else (None,0)
 basis=[[int(pr[0][i,j]) for j in range(nr*nc)] for i in range(pr[1])]
 ranks=[nmod_mat(nr,nc,g,p).rank() for g in basis]
 from random import Random
 rng=Random(148+h*100+length)
 for _ in range(100):
  coeff=[rng.randrange(p) for g in basis]
  entry=[sum(a*g[j] for a,g in zip(coeff,basis))%p for j in range(nr*nc)]
  ranks.append(nmod_mat(nr,nc,entry,p).rank())
 result['scalar_nullity_mod']=nullity
 result['scalar_pairing_dimension_mod']=len(basis)
 result['scalar_pairing_basis_mod']=basis
 result['maximum_sampled_scalar_rank_mod']=max(ranks,default=0)
 if max(ranks,default=0)==min(nr,nc) and nr==nc:
  tc=nmod_mat(tracefree,p).transpose()
  tr,trank=tc.rref()
  erows=[next(j for j in range(len(tracefree)) if tr[i,j]) for i in range(trank)]
  small=nmod_mat([tracefree[i] for i in erows],p)
  sr,_=small.rref()
  pivots=[next(j for j in range(len(cs)) if sr[i,j]) for i in range(trank)]
  free=[j for j in range(len(cs)) if j not in pivots]
  # Rebuild original integer constraints, not their modular representatives.
  exact=[]
  for x in range(nr):
   for v in range(nc):
    ref=((x*O)*O)*nc+v
    for y in range(O):
     for u in range(O):
      if y==u==0:continue
      ix=((x*O+y)*O+u)*nc+v
      exact.append([c[ix]-(c[ref] if y==u else 0) for c in cs])
  square=fmpq_mat([[exact[i][j] for j in pivots] for i in erows])
  for attempt in range(8):
   fv=[rng.randrange(-2*nr,2*nr+1) for _ in free]
   rhs=fmpq_mat([[-sum(exact[i][j]*z for j,z in zip(free,fv))] for i in erows])
   sol=square.solve(rhs)
   w=[0]*len(cs)
   for j,z in zip(free,fv):w[j]=z
   for j,z in zip(pivots,sol.entries()):w[j]=z
   denominator=math.lcm(*(int(z.denominator) if hasattr(z,'denominator') else 1 for z in w))
   wi=[int(z*denominator) for z in w]
   assert all(sum(row[j]*wi[j] for j in range(len(cs)))==0 for row in exact), 'rational nullspace verification failed'
   g=[[sum(w[j]*cs[j][((x*O)*O)*nc+v] for j in range(len(cs))) for v in range(nc)] for x in range(nr)]
   det=fmpq_mat(g).det()
   if det:
    result['rational_scalar_crossing']=True
    result['scalar_pairing']=[[str(z) for z in row] for row in g]
    result['scalar_pairing_determinant']=str(det)
    result['scalar_weights']=[{'degree':names[j][0],'shift':names[j][1],'weight':str(z)} for j,z in enumerate(w) if z]
    result['construction_attempt']=attempt
    break
  else:result['rational_scalar_crossing']=False
 if r==ra:
  ar,rank=a.rref()
  erows=[next(j for j in range(len(target)) if ar[i,j]) for i in range(rank)]
  small=nmod_mat([[int(cs[j][i])%p for j in range(len(cs))] for i in erows],p)
  sr,_=small.rref()
  ccols=[next(j for j in range(len(cs)) if sr[i,j]) for i in range(rank)]
  mat=fmpq_mat([[cs[j][i] for j in ccols] for i in erows])
  rhs=fmpq_mat([[target[i]] for i in erows])
  sol=mat.solve(rhs)
  w=[0]*len(cs)
  for j,c in zip(ccols,sol.entries()):w[j]=c
  valid=all(sum(w[j]*cs[j][i] for j in ccols)==target[i] for i in range(len(target)))
  result['member_rational']=valid
  if valid:result['weights']=[{'degree':names[j][0],'shift':names[j][1],'weight':str(c)} for j,c in enumerate(w) if c]
 print(json.dumps(result),flush=True)
