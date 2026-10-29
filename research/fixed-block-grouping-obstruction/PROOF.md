# A fixed-block obstruction to universal grouping

## Statement

Fix an integer `p>=2` and any `0<epsilon<1/2`. For every sufficiently
large multiple `q` of p, there is a simple graph G on q labeled vertices such
that

1. G has at most `(1/2+epsilon) binom(q,2)` edges; and
2. for **every** partition of its vertices into `K=q/p` groups of exactly
   p vertices, some two groups have all `p²` possible edges between them.

Consequently, for the generic equality-network grouping interface described
below, every such grouping and a common grouped edge width L require

    K² L / U >= 1/(1/2+epsilon),                        (1)

where U is the ordered sum of original supplied edge costs. The constant
approaches 2 as epsilon approaches 0. This is a worst-case obstruction for
this equal-size grouping and common-width interface. It is not a lower
bound on general tensor contraction, SAT, or specialized crossing networks.

## Existence proof

Choose every edge independently with probability 1/2. For any fixed
partition, the `binom(K,2)` pairs of groups use disjoint sets of original
edges. The probability that none of their p-by-p blocks is full is exactly

    (1-2^(-p²))^binom(K,2).

There are at most `K^q` labeled assignments of vertices to groups, so the
probability that *some* valid partition has no full block is at most

    K^q (1-2^(-p²))^binom(K,2).                        (2)

For fixed p, its logarithm is at most
`q log K - 2^(-p²) binom(K,2)`, which tends to minus infinity quadratically
in q. Let X be the total edge count and `E=binom(q,2)`. By independence,
`E[X]=E/2` and `Var(X)=E/4`. Chebyshev gives

    Pr(X>(1/2+epsilon)E) <= 1/(4 epsilon² E).          (3)

The sum of (2) and (3) is below 1 for all sufficiently large multiples q,
so a graph satisfying both properties exists. This is nonconstructive and
makes no claim about a polynomial-time graph generator. The finite control in
`verify.py` checks a separate small explicit graph; it does not prove this
all-size probabilistic argument.

## Network realization and padding cost

Take the q graph vertices as network nodes. For each graph edge introduce
one independent bit at each endpoint and an equality factor between them;
use zero-bit constant factors for nonedges. Then the supplied edge costs
are `c_ab` in `{0,1}`, the ordered cost sum is `U=2|E(G)|`, and the
per-node cost sum is at most `q-1`. The source's network hypotheses allow
`P=q`, making `c_ab<=P/q`; each factor and an unrestricted node table are
available by point query.

Merge each p-node group. A pair of groups with a full block has p² independent
crossing equality factors. As a matrix between the two groups' crossing-bit
settings their product is an identity matrix of size `2^(p²)`; fixing all
other coordinates gives this identity as a submatrix. Its rank is exactly
`2^(p²)` over any field, so a factorization through L binary labels requires
`L>=p²`. This is not merely an artifact of adding supplied costs: it is a
rank bound for the **uncontracted pair factor**. The source-style replacement
of every group pair by a common-width equality edge must therefore use
`K² L >= (q/p)² p²=q²`. The density bound gives
`U<= (1/2+epsilon) q(q-1)`, establishing (1). Arbitrary simplification of
node tables, nonuniform edges, alternative group sizes, or a changed global
contraction may evade this particular interface obstruction.

## The source lemma and thin-grid implication

In the source's `lem:grouping-explicit` case (ii), the hypothesis is
`2 zeta² g >= K ln(2gK)` with `0<zeta<=1`. Taking `g=q`, `K=q/p`
requires `zeta² >= ln(2q²/p)/(2p)`, which eventually exceeds 1 for fixed
p. Case (i), `g=3K^8`, holds for at most one q for fixed p. Thus neither
case supplies a constant-ratio grouping lemma along an unbounded q sequence.
The graph result independently explains why a near-average common-width
grouping for **all** permitted networks cannot simply be assumed at constant
block size.

The rectangular minimax calculations in PRs 61, 101 and 110 concern a
particular factor-cost envelope, not all arbitrary 0/1 networks. We do not
prove that their actual crossing factors realize this graph family; showing
or excluding that realization is a separate open problem. The source's
finite precision, multiplicities, local table work, and other costs also
remain separate. The owner-accepted selected SAT result is unchanged.
