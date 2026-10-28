# A distance and nullity obstruction to small matroid frontier width

Author-checked all-size argument; no independent or formal review. This
concerns the shared-hash independence predicate, not an unrestricted SAT
lower bound. The ordered frontier representation in PR #37 motivates the
parameter; the inequality below is self-contained and does not assume that PR.

## The inequality

Let A be an a-by-m binary matrix with m>=1 and k=dim ker(A). Suppose every
nonzero vector in ker(A) has Hamming weight at least D, where 2<=D<=m+1.
The zero kernel satisfies this hypothesis vacuously. Let the columns be in
any order, and define

    U_i=span(v_1,...,v_i), F_i=span(v_{i+1},...,v_m),
    b_i=dim(U_i intersect F_i), b=max_i b_i.

Then, for q=ceil(m/(D-1)),

    k <= sum_{j=0}^{q-1} b_{j(D-1)} <= q b.             (1)

The positions in the sum are all less than m. Partition the order into
consecutive blocks of at most D-1 columns. Every block is independent: a
dependent-set failure would be a nonzero kernel vector of weight below D.
For block B beginning at cut i, let W be its span. Its contribution to the
prefix nullity is

    |B| - (dim(U_i+W)-dim(U_i)) = dim(W intersect U_i).

Since W is contained in F_i, this is at most b_i. Summing these increments
over the blocks gives the final nullity k and proves (1). This proof is
valid for **every** ordering; no method for finding an ordering is assumed.

There is also a sharp all-cut inequality:

    sum_{i=0}^{m-1} b_i >= k(D-1).                       (2)

Write L=D-1. For each s=0,...,L-1, start with an optional first block
of s columns, then partition the remainder into consecutive blocks of
length at most L. These blocks are independent. Applying the same
nullity-increment argument gives k <= sum_{i congruent to s mod L} b_i,
where 0<=i<m; for s>0 the initial block contributes at most b_0=0.
The residue classes partition all cuts 0,...,m-1, giving (2). By
Cauchy--Schwarz, sum_i b_i^2 >= k^2(D-1)^2/m. The width-one circuit
family below achieves equality in (2), so this area bound is sharp.

In particular, if an integer P>=1 satisfies m>P and all nonzero kernel
vectors have weight at least m/P, take D=ceil(m/P). Then D-1 >= m/(2P):
for m/P in (1,2] it is at least 1, and for larger values it is at least
m/P-1 >= m/(2P). Thus q<=ceil(2P)<=2P+1, and

    b >= k/(2P+1).                                       (3)

The more precise inequalities (1) and (2) apply without introducing P.

## Application to the checked sparse-hash interface

The accepted `lem:sparse-checks` gives a matrix A^(0) with m columns, at
most 3n rows and nonzero kernel weight at least m/P, for
P=20000 B^2 (floor(log_2 m)+1)^2. This is an accepted source premise, not
reproved here. Appending t arbitrary rows, including the random rows of
[the decision wrapper](../characteristic-two-decision/PROOF.md), can only
shrink the kernel and thus preserves the distance guarantee. The resulting
matrix A has rank at most 3n+t, hence k>=max(0,m-3n-t). If m>P, every
ordering satisfies

    b >= max(0,m-3n-t)/(2P+1).                           (4)

For the particular decision-wrapper leaf j, t=8(n+ceil(log_2(j+1))+1).
If that leaf's matrix also satisfies m-3n-t >= delta m for some fixed
positive delta, (4) yields b=Omega_delta(m/P). In the source regime P is
polylogarithmic when B is polylogarithmic; for m=Theta(n), this is
Omega(n/polylog n). This is a **conditional parameter regime**, not a claim
that every sparse leaf has that many clauses, that every B admits such a
leaf, or that its hash matrix has that nullity. If m<=3n+t, this row-count
argument may be vacuous even though the actual rank could still be smaller.
The exact number of rows and actual rank must be checked for each application.

Let K=max(0,m-3n-t). In the same regime, (2) gives
sum_i b_i >= K(ceil(m/P)-1) >= K m/(2P), and the squared-width sum is
at least K^2 m/(4P^2). For the explicit frontier construction of PR #37,
a version using a separate b_i-by-b_i canonical basis encoding at each
cut allocates exactly sum_i b_i^2 internal state-bit wires. Therefore
that particular representation has at least K^2 m/(4P^2) such wires.
This is a cost of the specified encoding, not a lower bound on the bits
needed by an arbitrary encoding of reachable states.

In that regime a proposed uniformly small-b frontier analysis cannot follow
from the source's sparsity/distance premises, regardless of column ordering.
The estimate does not show that all 2^O(b^2) possible frontier subspaces are
reachable, nor lower-bound the actual running time of a compressed network.
It does not rule out different predicates, different hash families or row
counts, different representations, special structure, or an improved SAT
algorithm. The overall decision cost, including selection, clauses, branches,
precision, recovery and amplification, remains unproved for this interface.

## Why nullity is essential

For any d>=2 and q>=1, form q disjoint column blocks. In each block use
basis vectors e_1,...,e_(d-1) and their sum, with different blocks supported
on disjoint coordinates. Each block is a single d-column circuit; its only
nonzero local kernel word has weight d. The entire matrix has m=qd,
k=q, and minimum nonzero kernel weight d. Ordering whole blocks
consecutively gives width at most one: a cut within one block can only see
that block in the intersection, and its width is one; a cut between blocks
has width zero. The all-cut sum equals q(d-1)=k(D-1), and hence (2) is exact.
The maximum-width inequality is tight up to the block-rounding factor. This example prevents a conclusion that distance alone forces large
width. It also prevents extrapolating the row-count lower bound when nullity
is not known to be large.
