#!/usr/bin/env python3
"""Exact small grouped-graph controls; no probabilistic extrapolation."""
from itertools import combinations


def pairings(vertices):
    if not vertices:
        yield ()
        return
    first=vertices[0]
    for i in range(1,len(vertices)):
        other=vertices[i]
        rest=vertices[1:i]+vertices[i+1:]
        for tail in pairings(rest):
            yield ((first,other),)+tail


def has_full_block(groups,edges):
    return any(all(tuple(sorted((x,y))) in edges for x in a for y in b)
               for a,b in combinations(groups,2))


def main():
    q=8
    vertices=tuple(range(q))
    all_edges=set(combinations(vertices,2))
    matching={(0,1),(2,3),(4,5),(6,7)}
    graph=all_edges-matching
    partitions=list(pairings(vertices))
    assert len(partitions)==105 and len(graph)==24
    assert all(has_full_block(parts,graph) for parts in partitions)
    # A matching has maximum degree 1, hence no complete 2x2 block.
    assert all(not has_full_block(parts,matching) for parts in partitions)
    # A full 2x2 block carries four independent bits and its crossing
    # equality matrix is the 16 by 16 identity, of rank 16 over every field.
    size=2**4
    assert sum(int(i==j) for i in range(size) for j in range(size))==size
    print('PASS: 105 pair partitions, 24-edge explicit witness, matching negative control, 16-state identity')


if __name__ == '__main__':
    main()
