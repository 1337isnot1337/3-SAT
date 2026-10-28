#!/usr/bin/env python3
"""Direct finite replay of source (47), (48), Lemmas 9 and 10."""
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import product
from math import comb, factorial
def partitions(n, minimum=1):
    if n == 0:
        yield ()
    for part in range(minimum, n+1):
        for tail in partitions(n-part, part):
            yield (part,) + tail


def source_a(mu):
    out = {(): 1}
    for part in mu:
        nxt = defaultdict(int)
        for mono, coeff in out.items():
            for j in range(1, part+1):
                nxt[tuple(sorted(mono+(j,)))] += coeff*(-1)**(part-1)*comb(part,j)
        out = nxt
    return dict(out)


def source_b(nu):
    mult = Counter(nu)
    z = 1
    for k,m in mult.items():
        z *= k**m*factorial(m)
    return {nu: factorial(sum(nu))//z}


@lru_cache(maxsize=None)
def mode(a, r, v):
    """Apply monomial field a[r] to monomial v by finite exact sum."""
    if not a:
        return ((v,1),) if r == 0 else ()
    e = sum(v)
    bound = e+abs(r)
    if not bound:
        return ()
    out = defaultdict(int)
    for ks in product(tuple(range(-bound,0))+tuple(range(1,bound+1)), repeat=len(a)):
        if sum(ks) != -r or sum(k for k in ks if k>0)>e:
            continue
        remaining = Counter(v)
        factor = 1
        for j,k in zip(a,ks):
            if k>0:
                if not remaining[k]:
                    factor = 0
                    break
                factor *= k*remaining[k]
                remaining[k] -= 1
            factor *= (-1)**(j-1)*comb(k+j-1,j-1) if k>0 else comb(-k-1,j-1) if -k-1>=j-1 else 0
        if not factor:
            continue
        for k in ks:
            if k<0:
                remaining[-k] += 1
        term = tuple(sorted(k for k,m in remaining.items() for _ in range(m)))
        out[term] += factor
    return tuple((k,v) for k,v in sorted(out.items()) if v)


def apply(poly, r, values):
    out = defaultdict(int)
    for a,ac in poly.items():
        for v,vc in values.items():
            for target,c in mode(a,r,v):
                out[target] += ac*vc*c
    return {k:v for k,v in out.items() if v}


def qs(a,b,h,s,v,reverse=False):
    out = defaultdict(int)
    for i in range(2*h+1):
        a_i = {m:c*comb(h+sum(m),i) for m,c in a.items() if i<=h+sum(m)}
        r = s-h+i
        if reverse:
            tmp = apply(a_i,r,{v:1})
            terms = apply(b,-r,tmp)
        else:
            tmp = apply(b,-r,{v:1})
            terms = apply(a_i,r,tmp)
        for t,c in terms.items():
            out[t] += (-1)**i*c
    return {k:v for k,v in out.items() if v}


def main():
    cases = 0
    for h in (1,2,3):
        labels = list(partitions(h))
        for x in labels:
            a = source_a(x)
            for v in labels:
                b = source_b(v)
                for y in labels:
                    total = defaultdict(int)
                    for s in range(-2*h,2*h+1):
                        q = qs(a,b,h,s,y)
                        assert q == qs(a,b,h,s,y,True), (h,x,v,y,s)
                        for target,c in q.items():
                            total[target] += c
                        cases += 1
                    total = {k:v for k,v in total.items() if v}
                    expected = {y:factorial(h)} if x==v else {}
                    assert total == expected, (h,x,v,y,total,expected)
                    for p in (2,3,5,7):
                        assert {k:v%p for k,v in total.items() if v%p} == {k:v%p for k,v in expected.items() if v%p}
    restricted = 0
    for h in (2,3):
        labels = list(partitions(h))
        for p in (2,3,5):
            codebook = [mu for mu in labels if all(k % p and mu.count(k)<p for k in set(mu))]
            for x in codebook:
                a = source_a(x)
                for v in codebook:
                    mult = Counter(v)
                    z = 1
                    for k,m in mult.items():
                        z *= k**m * factorial(m)
                    inverse = pow(z,-1,p)
                    for y in labels:
                        total = defaultdict(int)
                        for shift in range(-2*h,2*h+1):
                            q = qs(a,{v:1},h,shift,y)
                            assert q == qs(a,{v:1},h,shift,y,True)
                            for t,c in q.items():
                                total[t] += c
                        actual = {t:c*inverse%p for t,c in total.items() if c*inverse%p}
                        expected = {y:1} if x == v else {}
                        assert actual == expected
                        restricted += 1
    print(f'PASS: {restricted} restricted-codebook summed source identities')
    print(f'PASS: {cases} source-piece operator-order cases, exact summed identity and four prime reductions')


if __name__ == '__main__':
    main()
