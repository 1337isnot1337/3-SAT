# Fixed fingerprint evaluations for XOR matchings

The statements here concern an evaluation interface, not the complexity of
SAT. All proofs are author-checked and await independent review.

## The family

Let n be positive and even, and let F be a finite field of characteristic two
with q elements. For every perfect matching M on [n], define the 2-CNF

    C_M = AND_{ij in M} ((x_i OR x_j) AND (NOT x_i OR NOT x_j)).

Its solutions independently choose exactly one endpoint of each pair. It has
n clauses, every variable occurs twice, and 2^(n/2) solutions. Its multilinear
weighted decision fingerprint from `characteristic-two-decision/PROOF.md` is

    Z_M(r) = sum_{x satisfies C_M} product_{i:x_i=1} r_i
           = product_{ij in M} (r_i+r_j).

Thus an evaluation r in F^n is nonzero exactly if the matching is proper for
the q-coloring i -> r_i. In particular the polynomial is nonzero, even though
the number of solutions is even.

A *fixed hitting set* H is a set of points in F^n chosen independently of M
such that some r in H has Z_M(r) != 0 for every perfect matching. Field
arithmetic is exact. The choice of H may depend on n and F. The result also
applies to a deterministic black-box evaluation protocol whose next query is
chosen from previous values only: follow its all-zero transcript, construct a
matching missed by those points, and the transcript remains all zero. It does
not apply if queries or the decision use the formula's explicit description.

## Lower bound

Set

    K = max(0, floor((n-2q)/2)+1).

Every fixed hitting set has at least (1-1/(2q))^(-K) points. In particular,
for n >= 2q it has size at least exp(K/(2q)); for q=o(n) this is
exp(Omega(n/q)).

Proof. Choose a perfect matching uniformly by repeatedly pairing the smallest
remaining vertex with a uniformly random other remaining vertex. For the
following probability calculation equivalently choose a uniformly random
remaining first vertex as well; both methods generate a uniform matching.
At a stage with N remaining vertices and color-class sizes c_1,...,c_q,

    Pr[same color next] = sum c_i(c_i-1)/(N(N-1))
                         >= (N-q)/(q(N-1)),

by Cauchy-Schwarz. This remains valid after conditioning on any previous
sequence of pairs because the remaining matching is uniform. For N>=2q the
right side is at least 1/(2q). There are exactly K stages with N>=2q, so

    Pr[M is proper for r] <= (1-1/(2q))^K.

If H hits every matching, the union bound over r in H has left side one,
which gives the bound. No independence between evaluations is needed. ∎

This is an information lower bound on a prescribed black-box query family,
not a lower bound for algorithms given C_M: matching XOR constraints are
trivially satisfiable and can be recognized and solved in polynomial time.
Likewise preprocessing that substitutes the constraints changes the interface
and is outside the lower bound.

## Upper bound on this family

There are (n-1)!! perfect matchings. For each M, independent uniform field
coordinates give Pr[Z_M(r)!=0] = p=(1-1/q)^(n/2). Therefore t independent
uniform points miss some M with probability at most

    (n-1)!! * (1-p)^t <= (n-1)!! * exp(-pt).

Consequently a fixed hitting set exists with at most
ceil((ln((n-1)!!)+1)/p) points. For q>=2 its logarithm is
O(n/q + log(n log(n+2))). This matches the lower bound's exponential
scale when n/q dominates the logarithmic factor. This is an existence
statement, not an efficient construction. Exhaustive greedy selection gives
one deterministic construction: enumerate all q^n points and all matchings,
select the point hitting the most remaining matchings, and repeat. Averaging
shows that each selection covers at least p of the remaining fraction, so the
same type of bound holds. Its enumeration time and storage are exponential
and are charged explicitly; it is not a SAT algorithm improvement.

## Cost implications and limits

If q is fixed, every such universal evaluation list has exponential length.
For q=o(sqrt(log n)/log log n), the lower bound has logarithm
omega(n log log n/sqrt(log n)). The list alone would exceed the accepted
general-density exponent, even if each evaluation were free apart from one
unit of work. For q on the order of sqrt(log n)/log log n the lower bound is
only of the same asymptotic scale as that exponent; unspecified constants
prevent a runtime comparison. For q>=n/2 this lower bound is vacuous.

These statements do not constrain formula-specific deterministic evaluations,
shared algebraic processing across points, or the ability to solve the
matching family directly. Nor do they prove that a field-size choice or any
full decision algorithm improves the selected result. The accepted baseline
and all its reductions, branch counts, tensor descriptions, entries,
precision, recursion, recovery and space costs are untouched. The predecessor
randomized interface has its own complete accounting; this package supplies no
replacement contraction, and does not invoke the frozen theorem as a proof
of these elementary combinatorial statements.
