# A scalar high-shift filter for one label pair

This construction is for the raw charged pieces of the predecessor and
the single label pair a=(1^h). It is not a full scalar crossing family
and does not improve the SAT bound. The written argument is author-checked
and awaits independent review.

For h>=2 and k=0,...,h define

    w_k=(1-k) binom(2h+k-1,k),
    T_h(q)=sum_(k=0)^h w_k Q_(h+k)^(q)(a,a).                (1)

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

## Capacity and evidence boundary

The effective charge degree here is e=2h-2 with q-independent weights.
The parent support theorem bounds the rank of every scalar label pairing
obtained from this coefficient by 3 for h>=4; for h=2,3 the entire label
dimension is at most 3. This remains true after a fixed output projection.
Thus the central interval removal in (1) does not preserve the growing
input-label capacity needed by the intended construction. Other charge
combinations, polynomial q-dependent weights, label normalization, both
required directional ranks, and full SAT costs remain open.

`tail_filter.py` checks (2) by exact charge interpolation for all output
partitions at energies 0,...,h and both operator orders for h=2,3,4.
The saved output binds the checker and predecessor module hashes. An
exploratory h=5 operator run was stopped before completion; it supplies no
evidence. `make verify` checks repository integrity, not this all-size
argument.
