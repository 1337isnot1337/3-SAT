#!/usr/bin/env python3
"""Exact coefficient ranks for normalized finite clause families."""
from itertools import combinations
from math import comb
import json


def polynomial(support,pattern,p):
    terms = {pattern:1}
    optional = support ^ pattern
    sub = optional
    while sub:
        terms[pattern|sub] = (-1 if sub.bit_count()%2 else 1) % p
        sub = (sub-1) & optional
    return terms


def rank(rows,p):
    basis={}
    for row in rows:
        row={i:v%p for i,v in row.items() if v%p}
        while row:
            j=max(row)
            if j not in basis:
                inv=pow(row[j],-1,p)
                basis[j]={i:v*inv%p for i,v in row.items()}
                break
            factor=row[j]
            for i,v in basis[j].items():
                z=(row.get(i,0)-factor*v)%p
                if z: row[i]=z
                else: row.pop(i,None)
    return len(basis)


def supports(n,k):
    return [sum(1<<i for i in c) for d in range(1,k+1)
            for c in combinations(range(n),d)]


def patterns(s):
    out=[]; v=s
    while True:
        out.append(v)
        if v == 0: return out
        v=(v-1)&s


def main():
    checks=0; satisfiable=0
    # All families on n=2, width <=2, and n=3, width exactly 2.
    for n,k,exact in [(2,2,False),(3,2,True)]:
        ss=supports(n,k)
        if exact: ss=[s for s in ss if s.bit_count()==k]
        clauses=[(s,a) for s in ss for a in patterns(s)]
        for mask in range(1<<len(clauses)):
            family=[c for j,c in enumerate(clauses) if mask>>j&1]
            sat=any(all((x&s)!=a for s,a in family) for x in range(1<<n))
            support_count=len({s for s,_ in family})
            for p in (2,3):
                r=rank([polynomial(s,a,p) for s,a in family],p)
                assert r >= support_count
                assert len(family) <= 2**k*r
                if sat: assert len(family) <= (2**k-1)*r
                checks+=1
            satisfiable+=sat
    fixtures=[]
    for n in range(3,8):
        k=3; ss=[s for s in supports(n,k) if s.bit_count()==k]
        family=[(s,a) for s in ss for a in patterns(s) if a]
        expected=sum(comb(n,j) for j in range(1,k+1))
        for p in (2,3):
            r=rank([polynomial(s,a,p) for s,a in family],p)
            assert r==expected
        assert sum(all((x&s)!=a for s,a in family) for x in range(1<<n)) == 1
        fixtures.append({'n':n,'clauses':len(family),'rank':expected})
    print(json.dumps({'exhaustive_rank_checks':checks,'satisfiable_families':satisfiable,
                      'sharp_family':fixtures,'status':'PASS'},indent=2))

if __name__=='__main__': main()
