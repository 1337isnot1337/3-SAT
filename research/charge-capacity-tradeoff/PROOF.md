# Charge-degree support and capacity

The predecessor's charged operators and label bases are fixed in
[PR 19](https://github.com/1337isnot1337/3-SAT/pull/19), especially its
`NEXT.md`. Let h be the common label grade and let p(h) be the number of
partitions of h. Let L_h(t) count grade-h partitions with at least t parts,
with L_h(t)=p(h) for t<=0 and L_h(t)=0 for t>h. Let d and b be
nonnegative integers. Give each raw charged piece a
polynomial weight in q of degree at most b. Apply a linear functional on
polynomials that annihilates every polynomial of degree less than d; it may,
for example, extract q^d or combine any finite set of coefficients at
degrees at least d. Apply any fixed linear functional to the output operator
entries (in particular, take the scalar coefficient when the operator is a
scalar identity). Assume d>=b and put e=d-b.

The resulting p(h)-square label matrix A has

    A[mu,nu] = 0 when length(mu)+length(nu)<e.                  (1)

Indeed each label current contributes at most one q, and there are exactly
length(mu)+length(nu) currents. Multiplication by the weight adds at most b
to that degree, so the resulting polynomial is annihilated when the length
sum is less than d-b. This uses the predecessor's raw normal ordering and
fixed label bases; it does not cover q-dependent changes of those bases or
weights of unbounded degree. Setting b=0 and taking the coefficient of q^d
recovers the predecessor's model.

## Exact structural rank

For any field and any matrix supported on (1),

    rank A <= C_h(e) = min_{0<=t<=h+1} [L_h(t)+L_h(e-t+1)].  (2)

For each t, select every row of length at least t and every column of
length at least e-t+1. These cover all potentially nonzero entries. A
matrix supported on r rows and c columns has rank at most r+c.

Moreover C_h(e) is the largest possible rank over any field among
*all matrices with this zero pattern*. To see that the displayed cover is
minimum, take any vertex cover. If all rows are selected, its size is at
least L_h(0). Otherwise let t-1 be the maximum length of an unselected row.
Every column of length at least e-t+1 must be selected, and every row of
length at least t must be selected. Thus that cover has size at least the
corresponding expression. A maximum matching has the same size as the
minimum cover by the bipartite matching theorem. Put ones on matching
edges and zero on all other entries: the matching submatrix is a permutation
matrix, so its rank attains the cover bound over any field. This
sharpness concerns the support mask only, not realizability by charged
operators, a scalar pairing, or the two required flattening ranks.

The predecessor's bound is recovered with t=ceil(e/2), up to a possible
one-unit improvement for even e, and rank is also at most p(h). The minimum
can sometimes be substantially smaller; the finite checker compares it to
an independently constructed greedy matching.

## Asymptotic consequence

For t>=1 conjugate partitions, remove a largest part, and inject them into
partitions of integers at most h-t. Hence

    L_h(t) <= sum_{j=0}^{h-t} p(j) <= (h+1) p(h-t).          (3)

Write kappa=pi sqrt(2/3). The Hardy--Ramanujan logarithmic estimate
`log p(n)=kappa sqrt(n)+O(log(n+1))` is used in the predecessor proof.
For a fixed 0<delta<=2 and e/h -> delta, choose t=floor(e/2)
(the same conclusion follows at delta=2 by (3)). Equations (2)-(3) yield

    log rank A <= kappa sqrt(h) sqrt(1-delta/2) + o(sqrt(h)).  (4)

A zero matrix is included by interpreting (4) as the equivalent exponential
upper bound. For delta=2 the right side is o(sqrt(h)). At delta>2 the
extracted pairing is identically zero because no two partitions have more than
2h parts.

Consequently a scalar pairing with rank at least N=2^lambda and
lambda -> infinity along e/h -> delta in (0,2) must satisfy

    h >= (1-o(1)) (lambda log 2)^2 / [kappa^2(1-delta/2)]. (5)

The first-moment predecessor has full leading label capacity and its
minimal grade is `(1+o(1))(lambda log 2/kappa)^2`; the factor
`1/(1-delta/2)` in (5) is thus a necessary grade inflation relative to
that reference, not a sufficient construction. For delta=2, log rank is
only o(sqrt(h)), so h/lambda^2 tends to infinity if N is attained. In
particular a linear effective degree e cannot retain the full leading label
capacity at the same grade. A full-capacity sequence necessarily has
`e=o(h)`, provided the degree ratios are bounded; ratios above 2 are zero.

## Limits and cost

No relation between charge degree and the size of a removed shift interval
is proved. Grade inflation is not itself a crossing-rank or SAT running-time
lower bound; a new construction must account for both directional ranks,
output codebook capacity, entries and exact arithmetic, reduction branches,
queries, modes, recursion, recovery, density, space and any error. This
bound permits polynomial q-dependent weights of degree at most b and
linear combinations of coefficients of degrees at least d. It does not cover
q-dependent label normalization, rational weights, or arbitrary changed
decompositions. If b is comparable to d, the effective degree e may be too
small for a leading loss.
The exact cover may overestimate the true charged pairing rank. No central
interval filter or improved alpha is claimed.
