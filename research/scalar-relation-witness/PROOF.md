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
positive. These h rows are independent. A second family of h-1 entries
with x=d and v=e has independent antisymmetric projections. Together
they show that the full partition-space tensor family `(A_s)` has rank
at least 2h-1. If a codebook contains e, d and exactly q of these y_l,
the same argument certifies rank at least 2q-1 in its encoded pieces.
These statements do not assert the full rank. The fixed x=v=e slice has
at most 2h shift directions by itself.

## Symmetry

For homogeneous a=b=t_1^h, the coefficient a^{<i>} is
`binom(2h,i) a`. Replace i by 2h-i in the definition of Q_{-s},
then use the source's identity exchanging the two operator orders.
The resulting expression is Q_s, because 2h is even. This holds as
an operator on V_h, independently of y and u.

## An exact second moment on arbitrary energy spaces

More generally, for every h>=1 and E>=0 the same homogeneous operator
family satisfies, on V_E,

```
sum_s Q_s = h! Id,             sum_s s^2 Q_s = 4hE h! Id.
```

The first equality is the source's crossing identity. For the second,
set `w_1=z, w_2=1` in the source's normal-ordered Laurent polynomial
for a=b=t_1^h, and take a matrix entry between weight-E monomials.
Every contraction pairs one field from each copy, with coefficient
`(w_1-w_2)^(-2)`. The term with all h pairs contracted contributes the
constant h! times the identity. Terms with exactly one uncontracted
field on either side cannot occur: contractions use the same number
of fields from each side. The terms with one uncontracted field from
each copy contribute, to second order at z=1,

```
h^2 (h-1)! (z-1)^2 < :J_1(z) J_1(1): >.
```

The coefficient h^2(h-1)! chooses one field from each copy and pairs
the other h-1 fields. All other terms have at least four uncontracted
fields and are divisible by `(z-1)^4` as Laurent polynomials. Any
powers of z accompanying the displayed coefficient equal one at z=1
and do not alter its second derivative.

At z=1, project the normal-ordered product to V_E. Its two-creation
and two-annihilation terms change energy; in the mixed terms only
matching indices preserve energy. Thus

```
projection_V_E(:J_1(1) J_1(1):) = 2 sum_{k>=1} k t_k partial_{t_k}
                                = 2E Id.
```

Hence F''(1)=4h^2(h-1)! E Id=4hE h! Id. Symmetry gives F'(1)=0,
so F''(1)=sum_s s^2 Q_s, proving the identity. The argument is
coefficientwise on finite-energy polynomials; no analytic convergence
is assumed. At E=h, `(s^2-4h^2)` therefore gives a nonzero linear
relation among the 2h+1 symmetric shift columns. The x=v=e slice has
rank at most 2h, strengthening the elementary symmetry bound.

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
characteristic-zero lower bound on their span rank. The involutive symmetry puts every row in the 2h+1-dimensional symmetric
Laurent subspace; the second-moment relation further bounds its rank by 2h.

## Nonsymmetric witnesses

For each 1 <= l < h use labels x=d and v=e, input y_l, and output
u=e when h-l-1 is even, otherwise u=d. Write G_l(z) for the resulting
shift polynomial. Its antisymmetric projection is G_l(z)-G_l(1/z).
We show that its largest positive exponent is exactly h+l+1.

In the first operator order b=t_1^h acts on y_l first. The preceding
energy argument bounds its positive shift support by h+l, regardless of
which a and u are used. In the exchanged order a^d acts first. Explicitly

a^d = -(t_2 + 2t_1)t_1^(h-2).

Both homogeneous components have h-1 fields. After acting on the l-part
y_l, their intermediate energy is at least h-l-1. In the exchanged
order this energy is s+i with i <= 2h, so s >= -(h+l+1). At equality
s=-(h+l+1), only i=2h survives, and the degree-(h-1) term has binomial
coefficient zero. Thus the first action is exactly by -t_2 t_1^(h-2).
Equality requires annihilating all l input parts and creating h-l-1
parts of size one. The t_2 field must annihilate a part m; its coefficient
is `binom(-m-1,1)=-(m+1)`, and the leading minus sign cancels it.
All contributions have the same positive sign. Summing over the l possible
parts, `sum(m+1)=h+l`, gives the coefficient

```
C_l = (h-2)! (h-l+1)(h+l)/(h-l-1)! > 0.
```

The subsequent b action maps the intermediate state to the chosen u:
use the same creation/annihilation count as in the previous section,
with h-l replaced by h-l-1. Its coefficient is positive. Thus G_l has
a positive coefficient at -(h+l+1), no term at +(h+l+1), and neither
sign occurs beyond that magnitude. Its antisymmetric projection therefore
has a nonzero coefficient at +(h+l+1), with all higher coefficients
zero. The h-1 projected rows are triangular and independent.

The h previously constructed F_l are symmetric, so they have zero
antisymmetric projection. Applying the projection to a linear combination
of F and G first forces all G coefficients to vanish; then the F
coefficients vanish by the earlier triangular argument. For any codebook
containing e and d, y_h=e is present. If q hook states are present, q
of the F rows and q-1 of the G rows are available, proving rank >=2q-1.

## Coverage of the original lexicographic codebook

Let p(j) count partitions, put kappa=pi*sqrt(2/3), and set
`R=floor(sqrt(h) log(h)/4)`. The source chooses the minimum h with
p(h)>=2^lambda, so `2^lambda > p(h-1)`. For a hook y with largest
part r<=R, each partition of h-r-1 maps injectively to a partition of
h by adding a part r+1. Every image has largest part at least r+1 and
therefore occurs lexicographically after y. Thus the number of states
later than y is at least p(h-r-1), which is at least p(h-R-1). If

```
p(h-R-1) > p(h)-p(h-1),
```

then y's zero-based index is strictly less than p(h-1), and y belongs
to the original codebook.

To prove the inequality asymptotically, write d_j=p(j)-p(j-1), the
number of partitions of j with no part one. For j>=2, increasing a
largest part by one injects these partitions into those of j+1 with no
part one. Thus d_j is nondecreasing. Every partition consists of some
ones and a partition without ones, so p(n)=sum_{j=0}^n d_j. With
k=floor(sqrt(h)), this gives `p(h+k) >= k d_h`. The Hardy–Ramanujan
asymptotic quoted in the pinned source makes p(h+k)/p(h) bounded, hence

```
[p(h)-p(h-1)]/p(h) = O(h^(-1/2)).
```

The same asymptotic, with R=(sqrt(h) log h)/4+O(1), gives

```
p(h-R-1)/p(h) = h^(-kappa/8+o(1)).
```

Since kappa<4, this is eventually larger than the previous O(h^-1/2)
term. Consequently the original codebook contains all R hooks with
largest parts 1,...,R for all sufficiently large h. Together with e and
d, its shift rank is at least 2R-1. The partition asymptotic and
minimality of h give sqrt(h)=Theta(lambda), yielding an
Omega(lambda log lambda) lower bound for the actual codebook. This does
not close the gap to 4h or bound any SAT runtime. The checker verifies
sufficient inequalities through h=1000, including the stronger R; that
finite range is not the asymptotic proof.

## Boundary

The original binary codebook consists of the lexicographically first
2^lambda partitions at its minimum h. It need not contain every hook:
the checker reports actual coverage for lambda 1,2,3. The conditional q
bound and the asymptotic coverage argument apply without changing its encoding. Full-space
2h-1 is not automatically an original-codebook bound. The first-moment
relation from PR #10 gives an independent upper bound 4h on the full
piece-family rank. Closing the remaining gap requires further witnesses or relations. No
asymptotic SAT improvement or new scalar-reweighting optimality is claimed.
