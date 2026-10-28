#!/usr/bin/env python3
"""Exact finite Hensel lifts and complete canonical packet jets."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('packet_reference',Path(__file__).with_name('verify.py'))
v=importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
F=v.F
def pmul(a,b):
 out=0
 while b:
  t=b&-b;out ^= a<<(t.bit_length()-1);b^=t
 return out

def div(a,b):
 out=0
 while a and a.bit_length()>=b.bit_length():
  k=a.bit_length()-b.bit_length();out^=1<<k;a^=b<<k
 return out,a

def inverse(a,mod):
 a=div(a,mod)[1];r0,r1=mod,a;t0,t1=0,1
 while r1:
  q,r=div(r0,r1);r0,r1=r1,r;t0,t1=t1,t0^pmul(q,t1)
 assert r0==1
 return div(t0,mod)[1]

def lift(P,L,p):
 mod=1<<p
 unit=v.reduce2(P[-1],mod);f=[v.reduce2(x,mod)*pow(unit,-1,mod)%mod for x in P]
 e0=1|(1<<L);d0=(1<<(L-1))-1;inv=inverse(d0,e0)
 E=[1]+[0]*(L-1)+[1]; D=[1]*(L-1)
 for k in range(1,p):
  prod=v.mmul(E,D,1<<(k+1)); S=0
  for i,x in enumerate(f):
   diff=(x-prod[i])%(1<<(k+1));assert diff%(1<<k)==0
   S|=(diff>>k)<<i
  dc=div(pmul(S,inv),e0)[1]
  dd,rem=div(S^pmul(dc,d0),e0);assert rem==0 and dd.bit_length()<=L-2
  for i in range(L): E[i]+=(1<<k)*((dc>>i)&1)
  for i in range(L-2): D[i]+=(1<<k)*((dd>>i)&1)
  assert v.mmul(E,D,1<<(k+1))==[x%(1<<(k+1)) for x in f]
 assert sum(E)%mod==0
 R=[0]*L;R[-1]=E[-1]
 for k in range(L-2,-1,-1):R[k]=(E[k+1]+R[k+1])%mod
 assert (E[0]+R[0])%mod==0
 Q=v.mmul([-1,1],D,mod);Q=[unit*x%mod for x in Q]
 assert v.mmul(R,Q,mod)==[v.reduce2(x,mod) for x in P]
 return R,Q


def mod3_div(a,b):
 a=a[:]
 while len(a)>1 and a[-1]==0:a.pop()
 b=b[:]
 while len(b)>1 and b[-1]==0:b.pop()
 q=[0]*max(1,len(a)-len(b)+1)
 while len(a)>=len(b) and a!=[0]:
  k=len(a)-len(b);c=a[-1]*pow(b[-1],-1,3)%3;q[k]=c
  for i,x in enumerate(b):a[i+k]=(a[i+k]-c*x)%3
  while len(a)>1 and a[-1]==0:a.pop()
 return q,a


def mod3_mul(a,b):
 r=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):r[i+j]=(r[i+j]+x*y)%3
 return r


def mod3_powmod(a,n,f):
 r=[1]
 while n:
  if n&1:r=mod3_div(mod3_mul(r,a),f)[1]
  a=mod3_div(mod3_mul(a,a),f)[1];n//=2
 return r


def check_rational_counterexample():
 # z^5+2z+2 is irreducible over F3 by the degree-five Frobenius criterion.
 f=[2,2,0,0,0,1];x=[0,1]
 assert mod3_powmod(x,243,f)==x
 a,b=f,[0,2,0,1]  # z^3-z
 while b!=[0]:a,b=b,mod3_div(a,b)[1]
 assert len(a)==1 and a[0]!=0


def main():
 check_rational_counterexample()
 factors=jets=content_checks=0
 for L in (2,4,8,16):
  W={d:v.kernel(L,d) for d in range(-L+1,L)}; H=[F(1)]
  for t in range(-L+1,L):
   if t: H=v.mul(H,[F(1),F(-1,t)])
  a=L.bit_length()-1
  for t in range(-L+1,L):
   if not t:continue
   i=(abs(t)&-abs(t)).bit_length()-1
   shifted=v.shift(H,t,2*L)
   def valuation(c):
    if not c:return float('inf')
    n,d=abs(c.numerator),c.denominator
    return (n&-n).bit_length()-(d&-d).bit_length()
   assert min(valuation(c) for c in shifted if c)==2*(a-i)+1
   content_checks+=1
  b0=v.val(H,-L)
  P=[(v.val(H,d)-b0)/v.val(W[d],d) for d in range(-L+1,L)]
  assert sum(P)==0
  for p in (1,2,4,8,16):
   R,Q=lift(P,L,p); factors+=1
   if L>4 or p>4: continue
   mod=1<<p
   A=[R[L-1-x] for x in range(L)]
   row=[(v.reduce2(b0,mod)+sum(A[x] for x in range(L) if mask>>x&1))%mod for mask in range(1<<L)]
   cols=[(1-sum(Q))%mod]+Q
   for t in range(-L,L):
    Ws={d:[v.reduce2(c,mod) for c in v.shift(W[d],t,2*L)] for d in W}
    output=[0]
    for cindex,cb in enumerate(cols):
     zlist=[[0] for _ in range(L)] if cindex==0 else [Ws[(cindex-1)-x] for x in range(L)]
     for mask in range(1<<L):
      term=[1]
      for x,z in enumerate(zlist):
       if mask>>x&1: factor=z
       else:
        factor=[(-c)%mod for c in z];factor[0]=(factor[0]+1)%mod
       term=v.mmul(term,factor,mod)
      if len(output)<len(term):output += [0]*(len(term)-len(output))
      for k,c in enumerate(term):output[k]=(output[k]+cb*row[mask]*c)%mod
    expected=[v.reduce2(c,mod) for c in v.shift(H,t,2*L)]
    output += [0]*max(0,len(expected)-len(output))
    expected += [0]*max(0,len(output)-len(expected))
    assert output==expected
    jets+=1
 print('PASS:',{'hensel_factorizations':factors,'canonical_complete_shifted_jets':jets,'irreducibility_controls':1,'exact_content_checks':content_checks})

if __name__=='__main__':main()
