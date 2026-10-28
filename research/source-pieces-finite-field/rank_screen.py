#!/usr/bin/env python3
"""Actual binary matrices from the source recursion; finite rank evidence only."""
from collections import Counter, defaultdict
from functools import lru_cache
import importlib.util
from pathlib import Path
from math import comb
from itertools import product, combinations


def partitions(n, minimum=1):
    if n == 0:
        yield ()
    for k in range(minimum, n+1):
        for tail in partitions(n-k, k):
            yield (k,)+tail


def source_a(mu):
    poly = {(): 1}
    for part in mu:
        out = defaultdict(int)
        for mono,c in poly.items():
            for j in range(1,part+1):
                out[tuple(sorted(mono+(j,)))] ^= c*(comb(part,j)&1)
        poly = {m:c for m,c in out.items() if c}
    return poly


@lru_cache(maxsize=None)
def mode(a,r,v):
    if not a:
        return ((v,1),) if r==0 else ()
    n, rest = a[0],a[1:]
    result = defaultdict(int)
    # Source (O2): creation is applied after the smaller field.
    for ell in range(n,sum(v)+r+1):
        c = comb(ell-1,n-1)&1
        if c:
            for term,val in mode(rest,r-ell,v):
                result[tuple(sorted(term+(ell,)))] ^= val
    # The annihilator acts first; k must occur and its integer coefficient be odd.
    for k,count in Counter(v).items():
        c = (comb(k+n-1,n-1)*k*count)&1
        if c:
            w = list(v)
            w.remove(k)
            for term,val in mode(rest,r+k,tuple(w)):
                result[term] ^= val
    return tuple((m,c) for m,c in sorted(result.items()) if c)


def apply(poly,r,values):
    out=defaultdict(int)
    for a in poly:
        for v in values:
            for target,c in mode(a,r,v):
                out[target] ^= c
    return {m for m,c in out.items() if c}


@lru_cache(maxsize=None)
def qsource(a,v,h,s,y):
    out=defaultdict(int)
    for i in range(2*h+1):
        ai = {m for m in a if i<=h+sum(m) and (comb(h+sum(m),i)&1)}
        r=s-h+i
        tmp=apply({v},-r,{y})
        for target in apply(ai,r,tmp):
            out[target] ^= 1
    return {m for m,c in out.items() if c}


def rank(rows):
    basis={}
    for row in rows:
        while row:
            lead=row.bit_length()-1
            if lead in basis:
                row ^= basis[lead]
            else:
                basis[lead]=row
                break
    return len(basis)


def main():
    # Cross-check the independent source (47) replay on all h<=3 cases.
    spec=importlib.util.spec_from_file_location("source_piece_check", Path(__file__).with_name("pieces.py"))
    direct=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(direct)
    reference_cases=0
    for h in (1,2,3):
        labels=list(partitions(h))
        for x in labels:
            direct_a=direct.source_a(x)
            a=tuple(sorted(source_a(x)))
            for v in labels:
                for y in labels:
                    for s in range(-2*h,2*h+1):
                        wanted={m for m,c in direct.qs(direct_a,{v:1},h,s,y).items() if c%2}
                        assert qsource(a,v,h,s,y)==wanted, (h,x,v,y,s)
                        reference_cases+=1
    sample=(1,7)
    independent={m for m,c in direct.qs(direct.source_a(sample),{sample:1},8,0,sample).items() if c%2}
    assert qsource(tuple(sorted(source_a(sample))),sample,8,0,sample)==independent
    print(f"PASS: {reference_cases} independently computed source (47) comparisons plus one h=8 piece")
    for h in (8,9,10,12):
        all_labels=[m for m in partitions(h) if all(k%2 and m.count(k)==1 for k in m)]
        assert len(all_labels)==(3 if h==12 else 2)
        subsets=[tuple(all_labels)]
        if len(all_labels)>2:
            subsets += list(combinations(all_labels,2))
        for labels in subsets:
            fields=[tuple(sorted(source_a(m))) for m in labels]
            n=len(labels)
            summed=defaultdict(int)
            histogram=Counter()
            zero_summary=None
            max_bits=0
            for s in range(-2*h,2*h+1):
                a_rows=[0]*(n*n)
                b_rows=[0]*(n*n)
                for x in range(n):
                    for v in range(n):
                        for y in range(n):
                            out=qsource(fields[x],labels[v],h,s,labels[y])
                            for u in range(n):
                                if labels[u] in out:
                                    a_rows[x*n+y] |= 1 << (u*n+v)
                                    b_rows[x*n+u] |= 1 << (y*n+v)
                                    summed[x,y,u,v] ^= 1
                ra,rb=rank(a_rows),rank(b_rows)
                histogram[(ra,rb)]+=1
                if ra and rb:
                    max_bits=max(max_bits,(ra-1).bit_length()+(rb-1).bit_length())
                if s==0:
                    zero_summary=(ra,rb)
            for x,y,u,v in product(range(n),repeat=4):
                assert summed[x,y,u,v] == int(x==v and y==u)
            print(f'h={h} labels={labels} s0={zero_summary} max_combined_bits={max_bits} histogram={sorted(histogram.items())}')
    print('PASS: exact F2 source-piece flattenings and crossing sums; finite dimensions only')


if __name__ == '__main__':
    main()
