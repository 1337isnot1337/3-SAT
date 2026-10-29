from collections import Counter
from functools import lru_cache
from math import comb
from pathlib import Path
from fractions import Fraction as F
import sys
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'charged-operator-moments'
sys.path.insert(0,str(SOURCE))
import predecessor as p
MAX_NONZERO=3

def add(out,terms,mult,extra=0):
 for (state,k),v in terms:
  if k+extra<=MAX_NONZERO:
   key=(state,k+extra);out[key]=out.get(key,0)+mult*v

def freeze(out):return tuple(sorted((k,v) for k,v in out.items() if v))

@lru_cache(maxsize=200000)
def op(mon,mode,arg):
 target=sum(arg)+mode
 if target<0:return ()
 if not mon:return (((arg,0),1),) if mode==0 else ()
 n,tail=mon[0],mon[1:];out={}
 for created in range(n,target+1):
  for (state,k),v in op(tail,mode-created,arg):
   if k<MAX_NONZERO:
    key=(tuple(sorted(state+(created,),reverse=True)),k+1)
    out[key]=out.get(key,0)+comb(created-1,n-1)*v
 add(out,op(tail,mode,arg),(-1)**(n-1))
 for destroyed,multiplicity in Counter(arg).items():
  reduced=list(arg);reduced.remove(destroyed)
  add(out,op(tail,mode+destroyed,tuple(reduced)),p.binomial(-destroyed-1,n-1)*destroyed*multiplicity,1)
 return freeze(out)

@lru_cache(maxsize=200000)
def dual(mu,taper,mode,arg):
 h=sum(mu);out={}
 for mon,val in p.dual_polynomial(mu):add(out,op(mon,mode,arg),val*p.binomial(sum(mon)+h,taper))
 return freeze(out)

def piece(mu,nu,arg,s,degree):
 h=sum(mu);needed=len(mu)+len(nu)-degree
 if needed<0 or needed>MAX_NONZERO:return {}
 out={}
 for i in range(2*h+1):
  scale=(-1)**i*p.dual_scale(nu)
  for (mid,k1),v1 in op(nu,h-s-i,arg):
   for (end,k2),v2 in dual(mu,i,s-h+i,mid):
    if k1+k2==needed:out[end]=out.get(end,0)+scale*v1*v2
 return {k:v for k,v in out.items() if v}
