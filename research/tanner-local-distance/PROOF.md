# Tanner checks with degree-sensitive local distance

The owner-accepted OpenAI `lem:sparse-checks` supplies the Tanner graph and
mixing framework. This package changes its local-distance and graph-degree
parameters. The deterministic Vandermonde local code and rational conditional
potential were developed for the source parameters in
[PR #78](https://github.com/1337isnot1337/3-SAT/pull/78), reviewed at
`7003b57622dbb327f7ee2e30fa2c9d36aa0ed774`; those mechanisms are credited
there. The argument below is author-checked, not independently reviewed.

## Statement

For positive integers n,m,B with m<=Bn, put

    mu = floor(log2 m)+1,
    H  = ceil(log2(2+B mu)),
    D  = 2^30 B^2 mu H^2,
    d  = min(m,D),
    r  = max(1,ceil(log2 d)),
    P  = 20000 B^2 r^2.

A binary matrix A on m columns can be constructed deterministically in
poly(n,m,B) bit operations and space, where the polynomial is in numeric B,
such that A has at most 3n rows, every row has at most d nonzeros, and

    0 != z in ker(A)  implies  wt(z) >= m/P.               (1)

In particular d=O(B^2 log(m+2) log^2(2+B log(m+2))) and
P=O(B^2 log^2(2+B log(m+2))). Compare the source's degree bound
O(B^2 log^3(m+2)) and denominator O(B^2 log^2(m+2)). These asymptotic bounds
hold uniformly for positive numeric B; for fixed B the denominator changes
from O(log^2 m) to O((log log m)^2). More generally, this logarithmic
order improves the source envelope when log B=o(log m); for rapidly growing B
the bound need not be smaller. No SAT time or alpha improvement is claimed. Constants are chosen for proof slack, not practical performance.

## Graph and explicit shift construction

Let q be the least power of two with qd>=m, so m<=qd<2m. Use the source's
bipartite Cayley graph with q vertices on each side, d ports, edges
(u,j)->(u XOR s_j,j), and its Walsh mixing argument. Put

    delta = 1/(100 B r),    epsilon = delta/2.

If q=1 take all shifts zero. If q>1 then d=D and q<m. Also r<=36H: indeed
B,mu<=2^H and log2 H<=H, so

    log2 D = 30+2 log2 B+log2 mu+2 log2 H <=35H,

and rounding up costs at most H. Thus

    epsilon^2 d / 4 = d/(160000 B^2 r^2)
       >= (2^30/(160000*36^2)) mu > 2mu.

For each nonzero binary character chi, maintain the products over selected
shifts of (1+epsilon chi/2) and (1-epsilon chi/2). Their total starts at
2(q-1); averaging over all q possible next shifts leaves it unchanged.
Choose a shift whose total does not increase. Arithmetic is exact: all terms
at one depth share denominator (400Br)^depth. There are d rounds, q candidate
shifts and 2(q-1) terms, each numerator having O(d log(Br+2)) bits.

If a final character sum has absolute value greater than epsilon d, choose the
corresponding sign. The inequality ln(1+x)>=x-x^2 for |x|<=1/2 implies that
its product is at least exp(epsilon^2 d/4)>exp(2mu). On the other hand the
whole potential is at most 2(q-1)<2^(mu+1)<exp(2mu), a contradiction. Hence
all nonconstant Walsh eigenvalues have magnitude at most epsilon d. The
construction and comparisons take polynomial time in numeric n,m,B, and
polynomial space; there is no floating-point test or exponential search.

## Local checks and Tanner distance

Set c=ceil(d/(8B)) and h=ceil(delta d)-1. For h=0 use c zero rows. Otherwise
construct GF(2^r), with 2^r>=d, by deterministic exhaustive irreducible-
polynomial search, polynomial in 2^r<=2d. Choose d distinct elements a_j,
form h field rows `(a_j^i)_{j=1}^d` for i=0,...,h-1, and expand each entry
into r binary bits. Pad with zero rows to c. Because

    r h < delta d r = d/(100B) <= c,

this fits. A nonzero binary word on s<=h positions cannot satisfy these field
checks: the first s rows on those positions form an invertible Vandermonde
matrix. Therefore every nonzero local kernel word has weight at least delta d.

Impose the local rows at both endpoints of each edge. For any nonzero accepted
edge word, let U,V be its touched vertices and w its weight. The local bound
gives w>=delta d max(|U|,|V|). Walsh mixing gives

    w <= d |U||V|/q + epsilon d sqrt(|U||V|).

These inequalities imply sqrt(|U||V|)>=(delta-epsilon)q and hence

    w >= delta(delta-epsilon) qd = qd/(20000 B^2 r^2) >= m/P.

This also holds for q=1, where the mixing inequality is immediate. Shorten by
keeping m of the qd coordinates and setting the rest to zero, as in the source;
the lower bound remains valid, and each check keeps at most d entries.

For q>1, d=D>=8B and c<=d/(4B), so 2qc<=qd/(2B)<m/B<=n. For q=1,
d=m and 2c<=m/(4B)+2<=n/4+2<=3n. Constructing all edges and output rows,
field arithmetic, potential updates, and shortening have polynomial time and
space in numeric n,m,B. In particular, the graph has fewer than 2m edges.

## Composition and limits

For a fixed-width CNF leaf with at most m<=Bn clauses, the matrix meets the
same interface used by the source greedy hash procedure, with the new P and
D in place of its larger source values. Each appended source hash row has
length P; each query has O(n) equations and at most O_k(max(D,P)) monomials
per equation. All candidates, including discarded ones, require valid sparse
polynomial counts. Even the source enumeration takes at most
`(2m)^P` candidate counts per round, and initial-check construction above is
polynomial; the exponential contraction cost, all sparsification leaves,
branching, tensor entries, modes, precision and recovery remain charged.
When B is polylogarithmic in n, log(max(D,P)+2)=O_k(log log n), and the
complete known arbitrary-density envelope remains
`poly(input) * 2^{O_k(n log log n/sqrt(log n))}`. The accepted fixed-density
fallback is unchanged. This local improvement does not establish a smaller
alpha or remove the iterated logarithm.

The [sparse-code isolation package](../sparse-code-isolation/README.md) uses
this interface with m=8n, B=8. Substituting the new matrix gives
P=O((log log n)^2) and check weight
D=O(log n (log log n)^2); its isolation-row length `8P ceil(log2(2n))`
becomes O(log n (log log n)^2), versus O(log^3 n) under its source parameters.
The code dimension, information-set step, isolation trials, error and full
contraction costs remain as in that package. This is a conditional composition
of author-checked components, not an implemented end-to-end SAT solver.

## Evidence and remaining work

The verifier checks 20,000 seeded parameter tuples including both q=1 and
q>1, and 3,000 sampled small-support Vandermonde tests at d=4096, h=3.
These are finite controls, not a proof of the all-size inequalities or a
source-scale q>1 graph implementation. Full independent review, particularly
of the changed asymptotic parameters and composed evaluator, remains open.
