# Hook witnesses for uncharged pieces

This is an author-checked argument, not an independent or formal review.
Use the operators and the two-order identity from Anthropic's Appendix B,
pinned by `research/anthropic-operator-ranks/SOURCES.json`. The accepted
OpenAI theorem is a separate premise and is not audited here.

Fix integer h >= 2. Let e=(1,...,1) be the partition of h with h parts,
and d=(2,1,...,1). The dual polynomial a^e and the scaled b^e both equal
`t_1^h`. Write `Q_s=Q_s(t_1^h,t_1^h)` on V_h. For 1 <= l <= h,
let `y_l=(h-l+1,1^(l-1))`, and let `u_l=e` if h-l is even, otherwise
`u_l=d`. Define the Laurent polynomial

```
F_l(z) = sum_{s=-2h}^{2h} [t^u_l] Q_s t^y_l z^s.
```

**Claim.** Each F_l is symmetric under z -> 1/z; it has no term of
positive exponent greater than h+l, and the coefficient at h+l is
positive. Consequently the F_l are linearly independent, and the full
partition-space tensor family `(A_s)_{s=-2h}^{2h}` has rank at least h
on the entries with its x and v legs both e. Those entries themselves span
at most 2h+1 shift directions. If a codebook contains e, d and exactly q
of these y_l, the same argument certifies rank at least q in the encoded
piece family. These statements do not say that h or q is the full rank.

## Symmetry

For homogeneous a=b=t_1^h, the coefficient a^{<i>} is
`binom(2h,i) a`. Replace i by 2h-i in the definition of Q_{-s},
then use the source's identity exchanging the two operator orders.
The resulting expression is Q_s, because 2h is even. This holds as
an operator on V_h, independently of y and u.

## Positive endpoint and triangular independence

In the first operator order, b acts first, with mode `h-s-i`. Each of
the h fields in `t_1^h` either creates a positive-energy part or
annihilates one existing part. Acting on y_l, at most l of them can
annihilate. Thus every surviving term has at least h-l creations and
intermediate energy at least h-l. At s>h+l, every i>=0 would require
intermediate energy `2h-s-i < h-l`, so the entry is zero.

At s=h+l only i=0 can contribute. Equality in the energy bound forces
all l parts of y_l to be annihilated and the remaining h-l fields to
create parts of size one. There are `h!/(h-l)!` assignments of fields
to the l input parts, and the annihilation multipliers have product
`k=h-l+1`. Hence the first operator yields

```
B_l t_1^(h-l),       B_l = h! k/(h-l)! > 0.
```

For a=t_1^h, all creation and annihilation coefficients are positive.
If h-l is even, take `a=(h-l)/2` annihilations of parts of size one,
then create h-a parts of size one. This reaches e, with coefficient
`binom(h,a) (h-l)!/(h-l-a)! > 0`.
If h-l is odd, take `a=(h+1-l)/2` annihilations of parts of size one,
create one part of size two and h-a-1 parts of size one. This reaches d,
with coefficient `binom(h,a)(h-a)(h-l)!/(h-l-a)! > 0`.
In both cases 0 <= a <= h-l. These are the only ways to reach the
specified u_l from the intermediate state, and no cancellation is
possible. Multiplication by B_l gives the claimed positive endpoint.

Order rows by l and select columns s=h+1,...,2h. Row l has zeros in
columns greater than h+l and a nonzero entry in its h+l column, so the
h-by-h submatrix is triangular with nonzero diagonal. If only some hooks
occur in a codebook, select their corresponding rows and columns instead.
All entries used are actual entries of the piece tensors, hence this is a
characteristic-zero lower bound on their span rank. The involutive symmetry
also puts every row in the 2h+1-dimensional symmetric Laurent subspace.

## Boundary

The original binary codebook consists of the lexicographically first
2^lambda partitions at its minimum h. It need not contain every hook:
the checker reports actual coverage for lambda 1,2,3. The conditional q
bound is valid for that codebook without changing its encoding. Full-space
h is not automatically an original-codebook bound. The first-moment
relation from PR #10 gives an independent upper bound 4h on the full
piece-family rank. Closing the remaining gap requires additional witnesses
outside the fixed x=v=e slice, because that slice is symmetric. No
asymptotic SAT improvement or new scalar-reweighting optimality is claimed.
