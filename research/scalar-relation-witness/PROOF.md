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
with one moment-separated diagonal entry they show that the full
partition-space tensor family `(A_s)` has rank at least 2h. If a codebook
contains e, d and exactly q of these y_l,
the same argument certifies rank at least 2q in its encoded pieces.
A family of low-support full-space witnesses strengthens 2h to
`2h+max(0,floor((floor((2h-3)/3)-1)/2))`. These statements do not assert the full rank.
The fixed x=v=e slice has at most 2h shift directions by itself.

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

## One more independent direction from second moments

Let `a^d=-(t_2+2t_1)t_1^(h-2)` and
`b^d=c t_2 t_1^(h-2)`, where `c=h!/[2(h-2)!]`. The following
operator identities hold on every V_E, for h>=2:

```
sum_s s^2 Q_s(a^d,b^e) = 0,
sum_s s^2 Q_s(a^d,b^d) = -4E(h-2) h! Id.
```

For the first identity, each homogeneous component of a^d contains h-1
fields, whereas b^e contains h. Contractions pair one field from each
side. After projection to V_E, the only possible uncontracted term of
weight below three has one t_1 field on the b side; its single current
changes energy and vanishes on projection. Therefore its Laurent
polynomial has zero second derivative at z=1. The general first-moment
identity converts that derivative to the stated second moment. The
zeroth crossing is also zero by the source's duality for d!=e.

For the second identity, both sides have h-1 fields. The only
uncontracted terms of total weight two leave one t_1 field on each side;
a lone uncontracted t_2 would leave unequal numbers of fields for
contraction. The contraction constants in the source's normal ordering
are `Gamma_11=1, Gamma_12=2, Gamma_21=-2, Gamma_22=-6`. For h>=3, the
coefficient of the resulting normal-ordered current pair is

```
-c (h-2)^2 [-(4h-6)(h-3)!]
-2c (h-1)(h-2) [2(h-2)!]
= -(h-2)h!.
```

The first term leaves a t_1 field from the t_2 t_1^(h-2) component;
its two bracketed contributions pair the two t_2 fields together or
cross-pair them with t_1 fields. The second term leaves a t_1 field
from the 2t_1^(h-1) component. When h=2, b^d has no t_1 field and the
coefficient is zero, agreeing with the same formula. As above, the
normal-ordered current pair projects to 2E Id, and differentiation
contributes a factor two. This gives the second identity.

On V_h define the even moment functional
`L(F)=sum_s (s^2-4h^2) [z^s]F`. The first and zeroth identities above
show that L annihilates every G_l, while the all-ones second-moment
identity shows it annihilates every F_l. In contrast, on the single
x=v=d, y=u=e entry it equals `-8h(h-1)h!`, which is nonzero. That
entry is independent of all previous witnesses. It requires only e,d,
so the rank bounds improve from 2h-1 and 2q-1 to 2h and 2q.

## Low-support witnesses in the full space

For every odd integer ell with `3<=ell<=floor((2h-3)/3)`, put
`k=(ell+3)/2` and `a=h-ell-k+2`. Choose y=(h) and
`u_ell=(a,2^(k-1),1^(ell-k))`, and use labels x=v=e. The bound on ell
gives a>=2, so u_ell has ell parts of which k are at least two. Its
Laurent polynomial W_ell has support inside `[-h,h]` and is nonzero.

To prove support, b^e acts first on the one-part state y. At most one
of its h fields can annihilate, so intermediate energy is at least h-1.
Thus the positive shift is at most h+1. At s=h+1, only i=0 and
intermediate `t_1^(h-1)` can occur. If A of a^e's h fields annihilate
and C=h-A create, the output has `(h-1)-A+C` parts. Matching u_ell's
ell parts forces `C=(ell+1)/2`. Every one of its k non-one parts must
be created because the intermediate parts are all ones, but k=C+1. The
endpoint therefore vanishes; symmetry gives the same bound on the
negative end.

For nonvanishing, let `r=(ell+1)/2` and let m_k be the multiplicity of
k in u_ell. In the normal-ordered expansion, y can reach u_ell only by
annihilating its single part h and creating the ell parts of u_ell,
requiring exactly 2r uncontracted fields. At z=1, one annihilation has
coefficient h and all creation coefficients are one. The r uncontracted
fields from each side can be chosen in `binom(h,r)^2` ways, and the rest
paired in `(h-r)!` ways. Thus the coefficient of `(z-1)^(2r)` is

```
binom(h,r)^2 (h-r)! (2r)! h / product_k(m_k!) > 0.
```

No smaller order can contribute. As ell varies, these first nonzero
orders ell+1 are distinct, proving the W_ell linearly independent.
All have all-ones labels and hence the even functional L from the
preceding section vanishes on them. Any relation involving the W_ell,
the previous F_l, G_l and diagonal entry first has zero diagonal
coefficient. At the largest remaining shift k=2h, the positive endpoint
isolates F_h and the negative endpoint then isolates G_(h-1). Descending
through k=h+2 similarly eliminates F_(k-h) and G_(k-h-1); finally the
positive endpoint h+1 eliminates F_1. Every W_ell has no support at
those shifts, and their independence finishes the argument. There are
`max(0,floor((floor((2h-3)/3)-1)/2))` such rows, so the full
partition-space rank is at least 2h plus that number for h>=2. This does not improve the
encoded bound: the original codebook can omit y=(h). The checker compares
a closed normal-order formula with the complete h=6 recurrence and
checks a larger finite range; the all-size claim is the written argument.

## Coverage of the original lexicographic codebook

Let p(j) count partitions and put kappa=pi*sqrt(2/3). The source chooses
the minimum h with p(h)>=2^lambda, so `2^lambda > p(h-1)`. For a hook
y with largest part r, every partition whose largest part exceeds r is
lexicographically later than y. If the number of those partitions exceeds
`p(h)-p(h-1)`, y's zero-based index is less than p(h-1), and y belongs
to the original codebook.

Write d_j=p(j)-p(j-1), the number of partitions of j with no part one.
For j>=2, increasing a largest part by one injects these partitions into
those of j+1 with no part one. Thus d_j is nondecreasing. Every partition
consists of some ones and a partition without ones, so p(n)=sum_{j=0}^n
d_j. With k=floor(sqrt(h)), this gives `p(h+k) >= k d_h`. The
Hardy–Ramanujan asymptotic quoted in the pinned source makes
p(h+k)/p(h) bounded, hence

```
[p(h)-p(h-1)]/p(h) = O(h^(-1/2)).                         (1)
```

We next show that, for every fixed c with `1/kappa < c < 2/kappa`,
all hooks of largest part at most `R=floor(c sqrt(h) log h)` are in
the codebook for sufficiently large h. Put L=floor(sqrt(h)). For each
j=R+1,...,R+L, the number of partitions of h with largest part exactly
j equals the number of partitions of h-j whose parts are all <=j: remove
one largest part j, or append it in the reverse direction.

For n large and j=c sqrt(n) log n+O(sqrt(n)), the fraction of partitions
of n containing a part >j tends to zero. Indeed, a union bound gives at
most `sum_{k>j} p(n-k)` such partitions. The partition asymptotic implies,
uniformly for k<=n/2,

```
p(n-k)/p(n) <= C exp(-kappa k/(2 sqrt(n))),
```

for a constant C; the remaining at most n terms contribute an exponentially
small fraction, since each is at most p(n/2). The sum is therefore at most
`O(sqrt(n) exp(-kappa j/(2 sqrt(n))))+o(1)=o(1)` because c>1/kappa.
This bound is uniform for the stated interval of j, with n=h-j.
Consequently each of the L disjoint largest-part classes above has at
least `(1-o(1)) p(h-j)` members. The tail after every hook with r<=R
therefore has at least

```
(1-o(1)) L p(h-R-L)
  = p(h) h^(1/2-kappa c/2+o(1)).
```

As c<2/kappa, this is larger than the O(p(h) h^-1/2) bound in (1).
Thus these R hooks all occur in the source codebook eventually. Since c
can approach 2/kappa from below, the codebook has
`q >= (2/kappa-o(1)) sqrt(h) log h` witness hooks. Together with e and
d, its shift rank is at least 2q. Minimality of h and the same partition
asymptotic imply `sqrt(h)~(log 2/kappa) lambda`; hence this is at least
`(8 log 2/kappa^2-o(1)) lambda log lambda`. This does not close the gap
to 4h or bound any SAT runtime. The checker verifies a sufficient
largest-part inequality at c=1/2 for 11<=h<=1000; this finite range is
not the asymptotic proof.

## Boundary

The original binary codebook consists of the lexicographically first
2^lambda partitions at its minimum h. It need not contain every hook:
the checker reports actual coverage for lambda 1,2,3. The conditional q
bound and the asymptotic coverage argument apply without changing its encoding. Full-space
2h-1 is not automatically an original-codebook bound. The first-moment
relation from PR #10 gives an independent upper bound 4h on the full
piece-family rank. Closing the remaining gap requires further witnesses or relations. No
asymptotic SAT improvement or new scalar-reweighting optimality is claimed.
