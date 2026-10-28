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

Conversely, adding t parts of size one injects partitions of h-t into
partitions of h with at least t parts, so L_h(t)>=p(h-t) for 0<=t<=h.
In every cover expression in (2), at least one threshold is at most
ceil(e/2). Therefore, for 2<=e<=2h,

    p(h-ceil(e/2)) <= C_h(e) <= 2(h+1)p(h-floor(e/2)).       (4)

The upper bound uses the balanced cover; the lower bound works for *every*
threshold. Thus the leading exponential loss below is sharp for the
unrestricted support mask. It may be weaker than the actual operator loss.

Write kappa=pi sqrt(2/3). The Hardy--Ramanujan logarithmic estimate
`log p(n)=kappa sqrt(n)+O(log(n+1))` is used in the predecessor proof.
For a fixed 0<delta<=2 and e/h -> delta with e<=2h, equation (4) yields
the mask asymptotic

    log C_h(e) = kappa sqrt(h) sqrt(1-delta/2) + o(sqrt(h)),
    rank A <= C_h(e).                                         (5)

For delta=2 the right side is o(sqrt(h)); if e>2h, the pairing is zero.
At delta>2 the extracted pairing is eventually identically zero because no two partitions have more than
2h parts.

Consequently a scalar pairing with rank at least N=2^lambda and
lambda -> infinity along e/h -> delta in (0,2) must satisfy

    h >= (1-o(1)) (lambda log 2)^2 / [kappa^2(1-delta/2)]. (6)

The first-moment predecessor has full leading label capacity and its
minimal grade is `(1+o(1))(lambda log 2/kappa)^2`; the factor
`1/(1-delta/2)` in (6) is thus a necessary grade inflation relative to
that reference, not a sufficient construction. For delta=2, log rank is
only o(sqrt(h)), so h/lambda^2 tends to infinity if N is attained. In
particular a linear effective degree e cannot retain the full leading label
capacity at the same grade. A full-capacity sequence necessarily has
`e=o(h)`, provided the degree ratios are bounded; ratios above 2 are zero.

## Polynomial-loss capacity threshold

The target in the predecessor's `NEXT.md` asks for label capacity
`exp(kappa sqrt(h)-O(log h))`, a stronger condition than merely retaining
the leading `kappa sqrt(h)` exponent. For 2<=e<=2h, (4) and the
partition asymptotic imply, uniformly in e,

    log C_h(e) <= kappa sqrt(h)
       - kappa floor(e/2)/(2 sqrt(h)) + O(log h).             (7)

Indeed `sqrt(h)-sqrt(h-t) = t/(sqrt(h)+sqrt(h-t)) >= t/(2sqrt(h))`.
Thus if the actual pairing has rank at least
`exp(kappa sqrt(h)-K log h)` for a fixed K and all sufficiently large h,
then necessarily

    e = O(sqrt(h) log h).                                     (8)

When e>2h the mask is zero, and the bounded cases e<2 already satisfy
(8). This strengthens the earlier `e=o(h)` conclusion for the explicit
polynomial-loss target, including sublinear charge degrees.

Conversely, if e=O(sqrt(h) log h), the lower side of (4), together with
`log p(n)=kappa sqrt(n)+O(log(n+1))`, gives
`C_h(e) >= exp(kappa sqrt(h)-O(log h))`. The cases e=0,1 have the same
conclusion directly. Hence (8) is necessary and sufficient for retaining
that capacity *in the unrestricted structural mask*. Sufficiency is not
an actual charged-operator construction or scalar-output proof. In
particular, a family extracting degree d with polynomial weights of maximum
degree b must have

    b >= d - O(sqrt(h) log h)                                  (9)

if it meets that label-capacity target. This also covers b>=d trivially;
it does not imply that storing or evaluating the weights costs exponential
time, since a high-degree polynomial can be sparse. No relation between e
and the width of a central shift interval is asserted.

## Exact fixed-deficit structural rank

Let e=2h-k, with k>=0 and h>=max(1,2k). Define P(j)=sum_(i=0)^j p(i)
for j>=0 and P(-1)=0. Then the exact mask rank is

    C_h(2h-k) = P(floor(k/2)) + P(floor((k-1)/2)).            (10)

Indeed, label a partition by its deficit i=h-length. A partition of h
with deficit i corresponds, after removing one from each part, to a
partition of i with at most h-i parts. For i<=k and h>=2k, there are
exactly p(i) such labels. The support condition becomes i+j<=k;
labels with deficit above k are isolated. Its threshold covers have sizes
P(a)+P(k-a-1), for -1<=a<=k. The increments p(i) are nondecreasing,
so moving a toward the middle cannot increase this sum. The minimum is
therefore (10). For k=0,1,2,3,4 this gives ranks 1,2,3,4,6.
This fixed-deficit formula establishes only structural-mask rank; the
examples below realize k=0 and k=1, but no general attainment follows.
The finite checker also verifies (10) for all covered grades through 35.

## Attaining the rank-one endpoint

For the unweighted raw piece Q_s at any h>=1, the coefficient of q^(2h)
is zero except at row and column label `(1,1,...,1)`. At those labels it
is the following scalar operator on every output energy space:

    [q^(2h)] Q_s = (-1)^(h-s) binom(2h,h-s) Id,  |s|<=h,      (11)

and zero outside this shift range. To prove this, degree 2h forces both
partitions to have h parts, hence all ones, and forces every current to use
its zero mode. Each factor then acts as q Id with mode zero. For these
labels the dual polynomial is t_1^h and the column scale is one. In the
predecessor's alternating piece formula, zero mode in both factors forces
summation index i=h-s, and the dual taper contributes binom(2h,i), with
sign (-1)^i. These identities hold at every output grade, and the same
argument applies to either operator order. Thus each |s|<=h attains the
mask's rank-one upper bound in characteristic zero, including the outer
shift s=h. It does not retain exponentially many labels or give the two
factorization costs of a new crossing family.

`endpoint.py` checks this coefficient by exact finite differences of the
actual predecessor operators at h=1,2,3, all label pairs, output grades
0,1,2, and shifts from -h-1 through h+1 in both operator orders. This is
a finite check of the formula, not independent verification of the proof.

## A two-label actual pairing one degree below the endpoint

For h>=2 use row and column labels `a=(1^h)` and `b=(2,1^(h-2))`.
Extract q^(2h-1) from the individual raw piece Q_h. On every output grade,
the resulting operator matrix in the order (a,b) is

    [[0, -h(h-1)/2], [-1, 0]] tensor Id.                      (12)

Its determinant is `-h(h-1)/2`, nonzero over the rationals, so the
structural mask rank 2 for k=1 is attained with a scalar output. This
is an individual component, not a complete crossing family.

For (b,b), the total number of currents is 2h-2, so the coefficient is
zero. For (a,a), degree 2h-1 would require exactly one nonzero current;
the total mode of the two factors must sum to zero, so that term vanishes.
For each off-diagonal pair, attaining degree 2h-1 forces every current
into its zero mode. At s=h that also forces the alternating index i=0.
The column scale for b is h(h-1)/2 and its zero-mode coefficient is -1.
For the b row, its dual factor `-y_2=-2t_1-t_2` contributes -2+1=-1
on zero modes; its other factors contribute one. These give (12). The same
mode argument works in either operator order and for every output grade.

`near_endpoint.py` checks all four entries in both orders on output grades
0,1,2 for h=2,3,4 using rational interpolation of degree at most 2h. It
samples enough charges to remove the possible degree-2h contribution;
it does not infer a general family or prove the all-size argument.

## The next coefficient is not scalar on the full output grade

For the all-ones label pair `(a,a)` and outer shift s=h, let m_i be
the multiplicity of part i in an output partition of grade E. Direct
normal ordering gives, on that output basis vector,

    [q^(2h-2)] Q_h(a,a)
      = 2h(h-1) E + h^2 sum_(i=1)^E (-1)^i binom(2h,i) i m_i.  (13)

The first summand comes from two nonzero currents in either single factor
at alternating index zero. Each ordered pair contributes the number
operator `D_-i D_i=i m_i`; summing i gives E. The second comes from one
nonzero current in each factor: their modes force the alternating index
to be i, giving sign `(-1)^i`, taper `binom(2h,i)`, and h choices in
each factor. No other terms can have q-degree 2h-2. All terms preserve
the output basis vector. The output energy bound E<=h suffices here;
more generally the sum stops at min(E,2h).

On the full grade-h output space, compare partitions `(1^h)` and `(h)`.
Their first terms agree but their second terms differ: after removing the
common factor h^3 the values are `-2h` and `(-1)^h binom(2h,h)`,
which are unequal for all h>=2. In fact its spectrum is simple. Divide
the nonconstant term by 2h^3 and write

    S(mu)=sum_i (-1)^i binom(2h-1,i-1) m_i(mu).              (14)

For distinct partitions mu,nu of h, let i be their largest differing part
size. Cancel their common parts, including their common copies of i. One
remaining partition has at least one part i, the other has none, and each
remaining weight is at most h. Thus the total weight of parts below i in
both is at most 2h-i. Put w_j=binom(2h-1,j-1). For 1<=j<i<=h,
w_j/j is nondecreasing, because `(w_(j+1)/(j+1))/(w_j/j)=(2h-j)/(j+1)>=1`.
For i>=2, the absolute contribution from all smaller parts to the
difference S(mu)-S(nu) is therefore at most

    (2h-i) w_(i-1)/(i-1) < w_i,

since `w_i=(2h-i+1)w_(i-1)/(i-1)`. The nonzero contribution from size i
cannot be canceled. For i=1 there are no smaller parts. Hence all S(mu)
are distinct, and (13) has one-dimensional eigenspaces over Q (or any
characteristic-zero field). Every subspace on which this operator acts as
a scalar has dimension at most one. This holds for any subspace, not only
one spanned by output partitions, provided the operator acts on it as a
scalar; a separate output projection/compression is not covered. In fact,
for any diagonal N-by-N rational operator with distinct eigenvalues, a
single operator always admits two-sided scalar compression of dimension
floor(N/2). Pair its eigenvectors with eigenvalues a,b and choose any
rational c. For each pair define Q(e)=e_a+e_b and define P by
`P(e_a)=(c-b)/(a-b)` and `P(e_b)=(a-c)/(a-b)`, with the result in the
corresponding compressed coordinate. Across disjoint pairs, `PQ=I` and
`PAQ=cI`. These maps may be nonorthogonal; they do not simultaneously
scalarize the other label-pair operators or provide the necessary crossing
factor costs. Thus simple spectrum alone says nothing comparable about
that two-sided compression interface.

`spectrum.py` checks pairwise distinct exact values for all partitions of
grades 2 through 45. This is a bounded check, not the proof. The
interpolation checker `second_deficit.py` verifies the formula for h=2,3,4,
output grades E=0,...,h, and both operator orders. This is not an obstruction for other shifts, weighted combinations or
projected output compressions, and it does not prove a SAT lower bound.

## Adjacent-shift collision

The simple-spectrum result is specific to the outer shift. At h=4 and
s=3, the all-ones label pair has the following q^6 coefficient on a
partition of output grade 4 with multiplicities m_1,...,m_4:

    -768 + 16(1+29m_1-112m_2+210m_3-224m_4).                 (15)

To derive it, the zero-mode alternating index i=1 contributes
`-binom(8,1)*2*4*3*4=-768` from two nonzero currents in either factor.
One nonzero current in each factor contributes the factor 16 times the
parenthesized term. The two possible mode orders yield `m_j` and `m_j+1`;
the relevant taper coefficients are binom(8,i), with alternating signs.
There are no other contributions at degree 6. In particular `(4)` and
`(2,2)` both have eigenvalue -4336, so their span is a two-dimensional
scalar invariant subspace for this one output operator. This does not
establish scalarity of other label-pair operators or a crossing identity.
`adjacent_shift.py` verifies the diagonal formula for all five grade-four
partitions, using exact interpolation in both operator orders.

## A finite full-label pairing on the collision space

An exact finite calculation improves the preceding single-entry example.
For h=4, s=3, extraction of q^6, let W be the span of `(4)` and `(2,2)`.
In the label order `(1^4),(2,1,1),(2,2),(3,1),(4)`, all 25 resulting
operators preserve W and act on it by the scalar entries of

    G = [[-4336,  0, -24, -64, 0],
         [    0,-36,   0,   0, 0],
         [   -4,  0,   0,   0, 0],
         [   -5,  0,   0,   0, 0],
         [    0,  0,   0,   0, 0]].

The first three rows and columns form a minor of determinant 3456, and
G has rank 3, attaining the structural mask bound at h=4 and e=6. An
inverse of that minor gives a scalar identity on those three asymmetric
label coordinates and both output states. This is an exact finite
component, not a construction with growing label or output capacity.

`adjacent_pairing.py` verifies all 25 label pairs on each of the two output
states, including absence of leakage, in both operator orders, by exact
interpolation at nine charges. It checks the matrix, determinant and rank.
This finite computation is the evidence for the statement; it has not
been extended to an all-size family or complete crossing-factorization
and SAT cost accounting.

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
