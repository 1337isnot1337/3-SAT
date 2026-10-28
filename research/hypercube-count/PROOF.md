# Exact count of the bipartite hypercube system

This is an exact counter for one explicit family of quadratic F2 systems,
not a bound for general SAT or sparse queries. The all-size arguments are
author-checked with substantial Codex assistance and await independent review.
The family arose in the local continuation of
[issue #29](https://github.com/1337isnot1337/3-SAT/issues/29#issuecomment-6459412498),
and is different from the oriented single-cube family in
[PR #73](https://github.com/1337isnot1337/3-SAT/pull/73). Both have an
obvious SAT solution; this package addresses exact counting.

## Statement

For d>=1 put m=2^d, with binary variables x_v,y_v indexed by v in F2^d,
and impose, for each v,

    x_v sum_(j=1)^d y_(v xor e_j) = 0 over F2.

Let A_d be the m-by-m cube adjacency matrix over F2. Its square is
(d mod 2)I: diagonal entries count d length-two returns, while every
nontrivial length-two destination appears twice. For fixed y, put z=A_d y.
The equation at v leaves x_v free if z_v=0 and forces x_v=0 otherwise.
Hence the exact number of solutions is

    C_d = sum_(y in F2^m) 2^(m-wt(A_d y)).                     (1)

When d is odd, A_d is its own inverse, so z ranges once over F2^m and

    C_d = sum_z 2^(m-wt(z)) = 3^m.                              (2)

When d is even, let q=m/2 and B=A_(d-1), so B^2=I. Ordering indices by
one coordinate gives A_d=[[B,I],[I,B]]. Its image is exactly
{(w,Bw): w in F2^q}: every output has that form, and A_d(0,w)=(w,Bw).
Its rank and nullity are both q, so every image point has 2^q preimages.
Consequently

    C_d = 2^q sum_(w in F2^q) 2^(m-wt(w)-wt(Bw)).               (3)

For example C_1=9 and C_2=100. Equation (3) is an exact weight-enumerator
identity, not a claimed closed form or polynomial-time method for even d.

## Uniform bit complexity and scope

Read d or the explicit instance, compute m=2^d, and construct the hypercube
neighbor lists in O(md) word operations. For odd d, compute 3^m by repeated
squaring in polynomial bit time. For even d, enumerate all q-bit w and
compute Bw from the q(d-1) adjacency incidences. Each summand and the
accumulator are at most 2^(2m), so all integers have O(m) bits. The resulting
uniform algorithm uses O(poly(m) 2^(m/2)) bit operations and polynomial
space; no randomness or hidden preprocessing is needed. A finite input can
be handled directly, including d=1; there is no asymptotic parameter
fallback or precision issue.

This counts the unconditioned system as stated. Arbitrary fixed-bit branches,
other private-edge systems, arbitrary row transformations as a representation
of a different system, and general sparse queries require separate treatment.
Invertible row transformations of this exact system preserve its solution
set and therefore its count. These formulas do not refute its coefficientwise
support obstruction: an aggregate computation can avoid enumerating the
lift's nonzero incidence coefficients. No comparison establishes a new
selected SAT time bound or improvement in alpha.
