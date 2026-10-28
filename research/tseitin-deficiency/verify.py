#!/usr/bin/env python3
"""Bounded controls for cubic-graph Tseitin parity CNFs."""
from itertools import combinations, product


def tseitin(n, edges):
    edges = sorted(tuple(sorted(e)) for e in edges)
    assert len(edges) == 3*n//2 and len(set(edges)) == len(edges)
    incidence = [[i+1 for i,e in enumerate(edges) if v in e] for v in range(n)]
    assert all(len(vs)==3 for vs in incidence)
    blocks = []
    for v, variables in enumerate(incidence):
        charge = int(v == 0)
        blocks.append([tuple(-x if bit else x for x,bit in zip(variables,bits))
                       for bits in product((0,1), repeat=3) if sum(bits)%2 != charge])
    return blocks, len(edges)


def sat(clauses, n):
    return any(all(any(bits[abs(x)-1] == (x > 0) for x in cl) for cl in clauses)
               for bits in product((False,True),repeat=n))


def deficit(clauses):
    owner = {}
    def aug(i, seen):
        for x in clauses[i]:
            v=abs(x)
            if v in seen:
                continue
            seen.add(v)
            if v not in owner or aug(owner[v],seen):
                owner[v]=i
                return True
        return False
    for i in range(len(clauses)):
        aug(i,set())
    return len(clauses)-len(owner)


def restrict(clauses, v, val):
    return list({tuple(x for x in c if abs(x)!=v) for c in clauses if (v if val else -v) not in c})


def check(n, edges):
    blocks, nvars = tseitin(n, edges)
    clauses = [cl for block in blocks for cl in block]
    assert len(clauses) == len(set(clauses)) == 4*n
    assert all(sum(v in c for c in clauses)==4 and sum(-v in c for c in clauses)==4
               for v in range(1,nvars+1))
    assert not sat(clauses, nvars)
    for v in range(n):
        assert sat([c for i,block in enumerate(blocks) if i != v for c in block],nvars)
    for i in range(len(clauses)):
        assert sat(clauses[:i] + clauses[i+1:], nvars)
    for c,d in combinations(clauses,2):
        for lit in set(c) & {-x for x in d}:
            res = (set(c)-{lit}) | (set(d)-{-lit})
            if not any(-x in res for x in res):
                assert len(res)==4
    k = deficit(clauses)
    assert k == 4*n-nvars
    for v,val in product(range(1,nvars+1),(False,True)):
        assert deficit(restrict(clauses,v,val)) <= k-1
    masks = [sum(1 << (abs(x)-1) for x in c) for c in clauses]
    surplus = min(sum(bool(mask & c) for c in masks)-mask.bit_count() for mask in range(1,1 << nvars))
    assert surplus >= 2
    print(f'PASS graph {n} vertices: {nvars} variables, {len(clauses)} clauses, '
          f'deficiency {k}, surplus {surplus}, single-clause removal, block-removal and resolvent checks')


def main():
    check(4, combinations(range(4),2))
    check(8, ((u,v) for u,v in combinations(range(8),2) if (u^v).bit_count()==1))
    edges = [e for e in combinations(range(4),2) if e != (0,1)]
    edges += [(a+4,b+4) for a,b in combinations(range(4),2) if (a,b) != (0,1)]
    edges += [(0,8),(1,8),(4,9),(5,9),(8,9)]
    blocks, nvars = tseitin(10, edges)
    bridge = sorted(tuple(sorted(e)) for e in edges).index((8,9)) + 1
    # Charge is at vertex 0, so the bridge must be 1. The removed clause
    # must be falsified by a wrong-parity assignment with bridge equal to 0.
    removed = next(c for c in blocks[9] if bridge in c)
    clauses = [c for block in blocks for c in block]
    clauses.remove(removed)
    assert not sat(clauses,nvars)
    print('PASS articulation control: deleting one clause can leave UNSAT')


if __name__ == '__main__':
    main()
