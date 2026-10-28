# A scalar high-shift filter for one label pair

This construction is for the raw charged pieces of the predecessor. It
produces an exact full-label scalar pairing of rank three for h>=3, but
does not preserve growing input-label capacity or improve the SAT bound. The written argument is author-checked
and awaits independent review.

For h>=2 and k=0,...,h define

    w_k=(1-k) binom(2h+k-1,k),
    T_h(q)=sum_(k=0)^h w_k Q_(h+k)^(q)(a,a).                (1)

The displayed T_h is the all-ones entry of a full-label construction below.
The k=1 weight is zero. Thus the support is the single shift h and the
shifts h+2,...,2h: all shifts with |s|<h are absent. On every output
energy E=0,...,h,

    [q^(2h-2)] T_h(q) = -2h(h^2-h+1) E Id.                    (2)

In particular, on grade E=h it is the nonzero scalar
`-2h^2(h^2-h+1) Id` over Q. This uses shifts outside the `|s|<=h` range
of the [outer-shift obstruction](OUTER-FILTER.md); it is a concrete
boundary of that obstruction, not a contradiction.

## Proof

For s=h+k with k>=1, the required coefficient has exactly one nonzero
current in each factor. Its operator on a grade-E partition is diagonal
and has eigenvalue

    h^2 sum_(j=k)^E (-1)^(j-k) binom(2h,j-k) j m_j.          (3)

For k=0 there is in addition the scalar `2h(h-1)E` from two nonzero
currents in a single factor. The two modes must be opposite; with s>=h
the first mode order produces `D_-j D_j=j m_j`. At k=1 the weight is zero.
These statements follow by the same normal-order count as in
OUTER-FILTER.md; out-of-range binomial coefficients are zero.

Set W(z)=sum_(k=0)^h w_k z^k. The generalized binomial series gives

    W(z) = (1 - 2h z/(1-z)) (1-z)^(-2h) mod z^(h+1).

Indeed the coefficient of z^k on the right is exactly w_k. Multiplying
by `(1-z)^(2h)` gives coefficient 1 at degree 0 and -2h at each degree
1,...,h. Therefore, after weighting (3), the coefficient of each `j m_j`
for j<=E is -2h. Since `sum j m_j=E`, the total is
`2h(h-1)E - 2h^3 E`, which is (2). Both operator orders agree. The
weights are integers with O(h) bits, uniformly computable in polynomial
bit time in h, and there are h+1 formal terms.

## The complete scalar label pairing

Use the same weights for every label pair mu,nu, and write
`delta_mu=h-length(mu)`, `delta_nu=h-length(nu)`. On every output grade
E<=h the extracted operator is `G_E(mu,nu) Id`, where

    G_E(mu,nu) = -2h(h^2-h+1)E            if delta_mu+delta_nu=0,
                 h! / z_nu                  if delta_mu+delta_nu=2,
                 0                          otherwise,                  (4)

and `z_nu=product_i i^(m_i(nu)) m_i(nu)!`. To see this, the total number
of currents is `2h-delta_mu-delta_nu`. If the deficit sum exceeds two,
the coefficient vanishes. If it equals one, producing the requested
charge degree uses exactly one nonzero-mode current; its mode cannot sum
to zero, so the coefficient vanishes. If it equals two, all currents use
zero mode, which forces the alternating index zero and shift s=h. The
row dual monomial has zero-mode coefficient `(-1)^delta_mu`, and the
column monomial has coefficient `(-1)^delta_nu h!/z_nu`. Their signs
multiply to +1. Deficit sum zero is the all-ones pair treated in (2).
This proves scalarity, including absence of output leakage, for every
label pair and all E<=h.

For h>=3 this scalar matrix has **rank exactly 3**, attaining the parent
structural bound. A deficit-one label has diagonal entry h(h-1)/2, a
deficit-two row has a nonzero all-ones column, and the all-ones row has
a nonzero deficit-two column. These give rank at least three; the support
bound gives at most three. For h=2 the rank is two at E>0 and one at E=0.
A nonprincipal rank-three minor can be normalized on a label axis, but
its constant dimension does not retain the input-label capacity needed
by the intended construction. Fixed output projections cannot increase
this scalar label rank. Other charge combinations, polynomial q-dependent
weights, both directional ranks, and full SAT costs remain open.

`tail_filter.py` checks (2) by exact charge interpolation for all output
partitions at energies 0,...,h and both operator orders for h=2,3,4.
`tail_pairing.py` additionally checks every label pair, all output
partitions at energies 0,...,h, both operator orders and the exact ranks
for h=2,3,4. The saved outputs bind checker and predecessor module hashes. An
exploratory h=5 operator run was stopped before completion; it supplies no
evidence. `make verify` checks repository integrity, not this all-size
argument.

## The next coefficient is not automatically scalar

Reusing the same weights one degree lower does not preserve the result.
At h=2 the filter is Q_2-10 Q_4. Extracting q^1 on the all-ones label
pair, its grade-two output operator maps `(1,1)` to `-48(2)` and `(2)`
to `-48(1,1)`. Thus it is not scalar even before considering the other
label pairs. `tail_next.py` checks all four state/order cases by exact
charge interpolation. Nor does parity compression repair this weight:
at h=3, projecting the odd-length output sector `span{(1,1,1),(3)}`
and using row `(1,1,1)` and column `(2,1)`, the q^3 coefficient has
respective diagonal entries 414 and 738. The same checker verifies both
states in both orders. These finite counterexamples do not exclude a
different higher-capacity weight or codebook; they do not contradict the
different cubic-moment compression of PR 89.

## A bounded next-degree tail screen

The preceding counterexample only rules out one weight vector. A wider
exact screen lets every weight on the positive tail `s=h,...,2h` vary
independently, extracts q^(2h-3), and imposes all scalarity equations for
every full grade-h row label, column label and output basis state. At h=2
the weight space is one-dimensional, spanned by `(1,4,10)` in shift
order, and its scalar label pairing has rank 2. At h=3 and h=4 the only
scalarizing weight is zero. These are exact finite statements; they do
not cover negative shifts, restricted or compressed output spaces, other
charge-degree combinations, or larger h.

`tail_next_screen.py` constructs every constraint using exact charge
interpolation in both operator orders, computes rational nullspaces, and
independently certifies the constraint ranks modulo 65537. Its output is
hash-bound in `tail-next-screen-verification.json`.
