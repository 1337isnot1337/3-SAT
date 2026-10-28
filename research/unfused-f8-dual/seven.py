import importlib.util
from pathlib import Path
from itertools import combinations
from collections import defaultdict
from math import factorial,prod
import numpy as np
import json
from hashlib import sha256
from math import isqrt
root=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('scheme',root/'research/three-bit-macro-walsh/schemes.py')
s=importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
labels=[(a,b) for a in range(8) for b in range(8)]
dual={b:next(B for B in range(8) if all(s.trace(s.multiply(a,B))==((a&b).bit_count()%2) for a in range(8))) for b in range(8)}
def cls(a,b):
 A,B=a,dual[b]
 if A==0 and B==0:return 0
 if A==0:return 1
 if B==0:return 2
 return 2+s.multiply(A,B)
classes={ab:cls(*ab) for ab in labels}
C=[]
for i in range(10):
 rows=[[sum((-1)**(((b&c).bit_count()+(a&d).bit_count())%2) for a,b in labels if classes[a,b]==j) for j in range(10)] for c,d in labels if classes[c,d]==i]
 assert all(r==rows[0] for r in rows); C.append(rows[0])
def comps(n,k):
 if k==1:yield (n,)
 else:
  for i in range(n+1):
   for tail in comps(n-i,k-1):yield (i,)+tail
def size(a):return factorial(sum(a))*7**(sum(a)-a[0])//prod(factorial(x) for x in a)
rows=list(comps(7,10)); lookup={a:i for i,a in enumerate(rows)}
allowed={a for a in rows if size(a)>840*7**7}
assert len(allowed)==1800
assert min(map(size,allowed)) == 1260*7**7
assert max(size(a) for a in rows if a not in allowed)==840*7**7
# 59/2 < 21 sqrt(2) < 149/5; strict exact type cutoff.
assert 59**2 < 4*882 and 149**2 > 25*882
assert (840*7**7)**2 < 2**59 and (1260*7**7)**5 > 2**149
frob=[0,1,2]+[2+s.multiply(x,x) for x in range(1,8)]
swap=[0,2,1]+list(range(3,10))
def perm(a,p):
 out=[0]*10
 for i,x in enumerate(a):out[p[i]]=x
 return tuple(out)
orbits=[]
while allowed:
 a=min(allowed); seen={a}; todo=[a]
 while todo:
  x=todo.pop()
  for p in [frob,swap]:
   y=perm(x,p)
   if y not in seen:seen.add(y);todo.append(y)
 assert seen<=allowed
 allowed-=seen;orbits.append(sorted(seen))
assert len(orbits)==399
p=65521
assert all(p % x for x in range(2,isqrt(p)+1))
assert (p-1)**2+(p-1) < 2**63
M=np.zeros((len(rows),len(orbits)),dtype=np.int64)
group=[]
identity=list(range(10))
for shift in range(3):
 for flip in range(2):
  z=identity[:]
  for _ in range(shift):z=[frob[x] for x in z]
  if flip:z=[swap[x] for x in z]
  assert all(C[z[i]][z[j]]==C[i][j] for i in range(10) for j in range(10))
  signs=[1,1,1]+[(-1)**s.trace(x) for x in range(1,8)]
  assert all(signs[z[i]]==signs[i] for i in range(10))
  group.append(z)
for col,orbit in enumerate(orbits):
 a=orbit[0]; q={(0,)*10:1}
 for i,count in enumerate(a):
  for _ in range(count):
   z=defaultdict(int)
   for b,x in q.items():
    for j,y in enumerate(C[i]):
     if y:
      v=list(b);v[j]+=1;z[tuple(v)]+=x*y
   q={k:v for k,v in z.items() if v}
 poly=defaultdict(int); seen=set()
 for g in group:
  target=perm(a,g)
  if target in seen:continue
  seen.add(target)
  for b,x in q.items():poly[perm(b,g)]+=x
  poly[target]-=8**7
 assert seen==set(orbit)
 for b,x in poly.items():M[lookup[b],col]=x%p

# The orbit sum columns are invariant: identical rows can be represented once.
representatives=[]
seen_rows=set()
for a in rows:
 if a in seen_rows: continue
 orbit={perm(a,g) for g in group}
 seen_rows.update(orbit)
 first=lookup[a]
 assert all(np.array_equal(M[first],M[lookup[b]]) for b in orbit)
 representatives.append(first)
M=M[representatives].copy()
rank=0
for col in range(len(orbits)):
 nz=np.flatnonzero(M[rank:,col])
 if not len(nz):continue
 pivot=rank+int(nz[0]);M[[rank,pivot]]=M[[pivot,rank]]
 M[rank]=(M[rank]*pow(int(M[rank,col]),-1,p))%p
 factors=M[rank+1:,col].copy()
 M[rank+1:]=(M[rank+1:]-factors[:,None]*M[rank])%p
 rank+=1
assert rank == len(orbits)
print(json.dumps({'status':'PASS', 'scope':'seven-macro high-floor invariant dual rank',
 'all_types':len(rows), 'eligible_types':1800, 'input_orbits':len(orbits),
 'output_orbits':len(representatives), 'prime':p, 'rank':rank,
 'max_excluded':840*7**7, 'min_included':1260*7**7,
 'bindings':{str(path.relative_to(root)):sha256(path.read_bytes()).hexdigest() for path in [Path(__file__).resolve(),root/'research/three-bit-macro-walsh/schemes.py']}},indent=2))
