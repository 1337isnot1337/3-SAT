"""Exact modular obstruction to a six-macro high-type dual."""
from itertools import combinations
from math import factorial, prod
from hashlib import sha256
import json
from pathlib import Path
from collections import defaultdict
import importlib.util

ref = Path(__file__).resolve().parents[1] / 'three-bit-macro-walsh' / 'schemes.py'
spec = importlib.util.spec_from_file_location('schemes', ref)
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)
labels = [(a,b) for a in range(8) for b in range(8)]
dual = {b: next(B for B in range(8) if all(s.trace(s.multiply(a,B)) == ((a & b).bit_count() % 2) for a in range(8))) for b in range(8)}
def cls(a,b):
    A,B=a,dual[b]
    if A==0 and B==0:return 0
    if A==0:return 1
    if B==0:return 2
    return 2+s.multiply(A,B)
classes = {ab:cls(*ab) for ab in labels}
weights=[list(classes.values()).count(i) for i in range(10)]
assert weights == [1]+[7]*9
C=[]
for i in range(10):
 rows=[]
 for c,d in labels:
  if classes[c,d] == i:
   rows.append([sum((-1)**(((b&c).bit_count()+(a&d).bit_count())%2) for a,b in labels if classes[a,b]==j) for j in range(10)])
 assert all(row==rows[0] for row in rows)
 C.append(rows[0])
assert all(sum(C[i][k]*C[k][j] for k in range(10))==64*(i==j) for i in range(10) for j in range(10))
q = [(-1)**s.trace(i-2) if i >= 3 else 1 for i in range(10)]
assert all(q[classes[a,b]] == (-1)**((a&b).bit_count()%2) for a,b in labels)
assert [sum(x*y for x,y in zip(row,q)) for row in C] == [8*x for x in q]

def compositions(n, k):
    if k == 1:
        yield (n,)
    else:
        for i in range(n+1):
            for tail in compositions(n-i,k-1):
                yield (i,)+tail

def size(alpha):
    return factorial(sum(alpha))*prod(w**a for w,a in zip(weights,alpha))//prod(factorial(a) for a in alpha)

maxima = [max(map(size,compositions(n,10))) for n in range(1,7)]
assert maxima == [7,98,2058,57624,2016840,84707280]
assert all(maxima[n-1] < 2**(21*n//5) for n in range(1,6))
# 127/5 < 18 sqrt(2) < 26. Exact cutoff leaves only distinct nonzero types.
assert 127**2 < 648*25
assert (360*7**6)**5 < 2**127 and 720*7**6 > 2**26
large = [a for a in compositions(6,10) if size(a) > 360*7**6]
assert len(large)==84 and all(a[0]==0 and max(a)==1 for a in large)

seed = json.loads((ref.parent/'four-block-dual.json').read_text())
def fused(a):
    # Trace splits the six nontrivial product classes into two Frobenius orbits.
    return (a[0],a[1],a[2],a[3],sum(a[2+i] for i in range(2,8) if s.trace(i)==0),sum(a[2+i] for i in range(2,8) if s.trace(i)==1))
seed_support = {tuple(x['type']) for x in seed['witness']}
lifted = [a for a in compositions(4,10) if fused(a) in seed_support]
assert min(map(size,lifted)) == 2401


def polynomial(alpha):
 p={(0,)*10:1}
 for i in alpha:
  nxt=defaultdict(int)
  for v,x in p.items():
   for j,y in enumerate(C[i]):
    if y:
     w=list(v);w[j]+=1;nxt[tuple(w)]+=x*y
  p={k:v for k,v in nxt.items() if v}
 return p

# Matrix of the transformed weighted type polynomials minus 8^6 I.
cols=[]
for a in combinations(range(1,10),6):
 v=tuple(int(i in a) for i in range(10))
 p=polynomial(a); p[v]=p.get(v,0)-8**6
 cols.append(p)
rows=sorted(set().union(*(p.keys() for p in cols)))
prime=1000000007
basis={}
for row in rows:
 v=[p.get(row,0)%prime for p in cols]
 for k,b in basis.items():
  if v[k]:
   factor=v[k]
   v=[(x-factor*y)%prime for x,y in zip(v,b)]
 pivot=next((i for i,x in enumerate(v) if x),None)
 if pivot is not None:
  inverse=pow(v[pivot],-1,prime)
  basis[pivot]=[(x*inverse)%prime for x in v]
  if len(basis)==len(cols): break
assert len(basis)==len(cols)
print(json.dumps({
    'status':'PASS', 'scope':'ten-class local scheme, type floors through six macros, and finite modular rank',
    'class_sizes':weights, 'max_type_sizes':maxima, 'lifted_old_seed_minimum':min(map(size,lifted)),
    'six_macro_candidate_types':len(cols), 'constraint_rows':len(rows),
    'prime':prime, 'modular_rank':len(basis),
    'bindings': {str(path.relative_to(ref.parents[2])):sha256(path.read_bytes()).hexdigest()
                 for path in [Path(__file__).resolve(),ref,ref.parent/'four-block-dual.json']}
}, indent=2))
