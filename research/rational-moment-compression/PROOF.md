# Rational output compression with polynomial signature loss

This is an author-checked component argument with substantial OpenAI Codex
assistance. It is not independently reviewed and does not improve the selected
SAT bound. The accepted OpenAI theorem is a premise.

## 1. An elementary affine packing lemma

Let x_1,...,x_N be rational vectors in Q^M, all with first coordinate one.
There are k disjoint nonempty groups G_j and rational weights a_(j,i) such that

    sum_(i in G_j) a_(j,i) x_i = c,       c_1=1,
    k >= N / T_M,                       T_M=M(M+1)/2.       (1)

The common c can be chosen to be one of the input vectors. Weights need not
be positive. In particular their sum in each group is one.

Algorithm: repeatedly remove a maximal linearly independent subset of the
remaining vectors. The rank never increases. At any rank r, every removed
subset is a basis of the same r-dimensional space: a proper containment
between two spaces of equal dimension is impossible. Let b_r be the number
of bases removed at rank r. No rank-zero remainder is possible because the
first coordinate is one. Thus N=sum_(r=1)^M r b_r. Select a rank whose b_r is
largest. Since sum r=T_M, its b_r is at least N/T_M. Choose c as any vector
in its first basis and express c uniquely in every selected basis. This
proves (1), including the common-span and disjoint-support claims.

Gaussian elimination implements the algorithm in a polynomial number of bit
operations in N, M and the input bit length. For integer inputs of magnitude
at most B, each coordinate solution uses an r-by-r nonsingular integer minor
and Cramer's rule. Numerators and denominators have O(M(log(B+1)+log(M+1)))
bits. All bases are subsets of the ORIGINAL input vectors; the algorithm
does not recursively feed growing rational outputs into new basis inputs.
Rational inputs can first be cleared coordinatewise, at polynomial cost.

## 2. Simultaneous compression of sparse matrices

Let A_1=I,A_2,...,A_M be N-by-N integer matrices. Join distinct indices i,j
when at least one A_a has a nonzero (i,j) or (j,i) entry. Suppose this
undirected graph has maximum degree at most Delta. A deterministic greedy
independent set S has size at least N/(Delta+1).

On S every matrix is diagonal. Apply the lemma to the signatures
x_i=((A_a)_(ii))_(a=1)^M, i in S. For each retained group define an embedding
column v_j=sum_(i in G_j)e_i and a projection row
u_j=sum_(i in G_j)a_(j,i)e_i^T. Write V for the columns and U for the rows.
Disjoint supports and graph independence give the exact identities

    UV=I_k,                U A_a V=c_a I_k,
    k >= N / ((Delta+1) T_M).                           (2)

These are rational oblique maps. U need not be V transpose, U and V need
not be positive, and the column space of V need not be invariant under A_a.
The stronger orthogonal-compression conclusion is NOT claimed. Coefficient
heights and construction time are polynomial in the explicitly listed
matrices' dimensions, sparsity and integer bit lengths by Section 1.

## 3. Application to charged partition zero modes

Use the zero-mode definitions and entry/transition bounds in the predecessor
[proof](../partition-transition-codebooks/PROOF.md), fixed integer charge q,
energy E>=1, and positive integer d. Include every field partition of weight
at most d, with the empty field first. Set

    M = sum_(j=0)^d p(j),
    B = ((2E+1)(E+d)(E^2+|q|+1))^d,
    Delta = 2 M (2E+1)^d.

The predecessor's normal-ordering argument bounds every integer entry by B
and the union transition degree by Delta. It applies to all E,d; no
asymptotic selection is needed for these inequalities. Equation (2) supplies

    k >= p(E) / ((1+2M(2E+1)^d) M(M+1)/2).              (3)

The predecessor instead used the diagonal-signature pigeonhole factor
(2B+1)^M. The change is to rational linear combinations on the two output
axes. This replaces that factor by T_M without claiming that basis subsets
of the improved size exist.

All matrices can be listed using at most
p(E) M (2E+1)^d poly(E,d,log(|q|+2)) operations with integer bit lengths
O(d log(E+d+|q|+2)). A polynomial amount of additional bit work in that
listing size suffices for (3). This includes constructing the maps, rather
than asserting existence without a usable entry algorithm.

For fixed q take, for all sufficiently large E,

    d(E)=floor(sqrt(E)/(ln(E))^2).

Use d=max(1,d(E)) for the finite exceptions. The source partition estimate
log p(E)=kappa sqrt(E)+O(log(E+2)), kappa=pi sqrt(2/3), and the elementary
bound M<= (d+1) exp(3 sqrt(d)) give

    log((Delta+1)T_M)=O(d log E+sqrt(d)+log(d+1))=o(sqrt E).

Consequently k>=exp(kappa sqrt(E)-o(sqrt E)), and construction takes
exp(O(sqrt E)) bit time and space. The rational map entries have
exp(o(sqrt E)) bits under the displayed bounds. This increases the supported
moment order from Theta(log^2 E) in the predecessor to
Theta(sqrt(E)/log^2 E), with the same leading output-capacity exponent.
It is a component bound, not a SAT time bound.

## 4. Actual moments, crossing directions, and what is still missing

The pinned predecessor moment argument expresses every charged moment
sum_s s^j Q_s(a,b), j<=d, as a scalar linear combination of these zero modes.
Apply U on the output coefficient axis and V on the output input axis. The
weighted sum for

    w(s)=s product_(i=1)^r (s^2-i^2),   r=floor((d-1)/2),

is therefore H(a,b) I_k and vanishes for |s|<=r. Since c in Section 1 is an
original signature, H(a,b) is EXACTLY the diagonal matrix coefficient of
that weighted sum on one original partition state. This gives a concrete
input-pairing matrix for subsequent work; it does not prove its rank.

Both maps act separately on the two output axes. For each flattening
(x,y)|(u,v) and (x,u)|(y,v), their tensor products multiply the flattened
matrix on the left/right. Rectangular multiplication cannot increase rank.
Rational entry generation fits exp(O(sqrt E)) at this scale. If a sufficient
input minor is found, its normalization must act separately on an input axis;
the rational compiler of PR #17 still requires every stated cost and error
condition. No full transfer is asserted by this component alone.

With E comparable to source grade h, the deleted interval is still o(h).
The inherited term-count envelope therefore has the SAME leading rho.
Output capacity by itself does not supply input capacity, and an improved
global bound is not established. A fixed-fraction interval or an actual-rank
improvement is needed, together with input pairing, uniform normalization,
reduction/query/entry/recursion/precision/recovery costs and an explicit space
guarantee. The present construction uses exponential space in sqrt E.

## 5. Evidence and attribution

Base: c600b21, with all predecessor sources local at that commit. The accepted
OpenAI source is 7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a; root SOURCES.json
retains its hashes and license. The Anthropic normal-ordering source and
charged definitions are pinned by the manifests of
`research/anthropic-operator-ranks` and `research/charged-operator-moments`.
The specific predecessor is issue #108 and
`research/partition-transition-codebooks`, including its dependency on the
PR #89 moment-to-zero-mode argument. The affine packing and oblique maps here
are original exposition; no literature-priority claim is made.

The finite checker tests exact rational identities, adverse affine-rank
strata, strict improvements over equality of diagonal signatures, sparse
matrix controls, and actual charged moment sums. These checks are evidence
for their registered cases, not an independent review of the all-size proof.
