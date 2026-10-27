# A uniform charged filter that removes a central interval

Author-checked draft, substantially AI-assisted. No independent or formal
review has occurred. The accepted OpenAI theorem remains the selected
baseline. The final master-recursion consequence below is conditional on
the pinned Anthropic interface and the predecessor component arguments.

## 1. Left-charged pieces and scalar highest-charge moments

Start with the charged normal-ordered operators in
[PR 11](../charged-operator-moments/PROOF.md), but put the zero mode
`D_0=q Id` only on the left (`a`) side. The right side is the original
zero-charge module. The two operator orders still have the same Laurent
expansion, and the zeroth crossing is unchanged: fully contracted terms
have no zero mode, while every term with an uncontracted current vanishes
at the diagonal. On energy `E`, with labels of grade `h`, the energy
bound remains `|s|<=E+h`.

Write `Q_s^(q)(a,b)` for these pieces. They are polynomial in `q`; on a
monomial left label the degree is at most its number of factors. For
`j>=0`, define on each fixed energy space

```math
 M_j^{(q)}(a,b)=\sum_s s^jQ_s^{(q)}(a,b),\qquad
 S_j(a,b)=[q^j]M_j^{(q)}(a,b).
```

The source's normal-ordered expansion has terms
`Gamma (z_1-z_2)^r n_q`, where `r` is the total weight left
uncontracted. A `j`-th logarithmic derivative at the diagonal kills
terms with `r>j`. On the other hand, `[q^j]` requires `j` left zero
currents, hence `r>=j`. Thus `r=j`, and every surviving uncontracted
current is a weight-one zero mode. Its operator is a scalar. Therefore

```math
 S_j(a,b)=G_j(a,b)\operatorname{Id}                       	ag{1}
```

for a scalar bilinear pairing `G_j`, on every fixed energy space. This
is not a projection of one matrix entry or an assumption that a general
moment is scalar.

There is also a length rule. Let `ell(mu)` count parts. For monomial
labels, if `G_j(a_mu,b_nu)` is nonzero, exactly `j` left factors remain
uncontracted and no right factor does. Full contraction pairs equal
numbers of the remaining left and right factors, so

```math
 \ell(\mu)-j=\ell(\nu).                                      \tag{2}
```

Bilinearity extends (2) to labels homogeneous in partition length.

## 2. A polynomial that deletes the whole central grid

Fix a computable `0<epsilon<=1`. At grade `h`, put
`k=ceil(epsilon h)`, `d=2k-1`, and

```math
 w_h(s)=s\prod_{r=1}^{k-1}\left(1-\frac{s^2}{r^2}\right)
       =\sum_{j=0}^{d}c_{h,j}s^j.                              \tag{3}
```

Only odd powers occur, `c_(h,0)=0`, and `c_(h,1)=1`. On the integer
shift grid, `w_h(s)=0` exactly for `|s|<k`; these are precisely the
integers satisfying `|s|<epsilon h`.

Define projected pieces by

```math
 B_s^{(h)}=\sum_{j=0}^{d}c_{h,j}s^j[q^j]Q_s^{(q)}.            \tag{4}
```

Although (4) combines different charge coefficients, every term has the
same shift `s`. Extracting a charge coefficient is a rational linear
combination of evaluations at the same shift. Every such evaluation has
the source's two intermediate-space factorizations. Consequently each
`B_s` factors through those same two spaces; no rank increase or new
shift is introduced.

Equations (1) and (4) give the operator identity

```math
 \sum_{|s|\ge k}B_s^{(h)}(a,b)
 =\sum_sB_s^{(h)}(a,b)
 =\sum_{j=0}^{d}c_{h,j}G_j(a,b)\operatorname{Id}.             \tag{5}
```

The first equality uses `w_h(s)=0` throughout the central interval.

## 3. Fixed-length invariants diagonalize every filtered pairing

Recall the predecessor's symmetric-polynomial operators

```math
 L(u_j)=(j-1)u_{j-1},\qquad T=PL,
```

with the explicit maps `P` and `R_L` from PR 11. On nonvacuum input,
`L R_L=Id`, `L P=0`, `R_L` raises weight by one and preserves length,
and `P` raises weight and length by one. Moreover `P` is injective on
`ker L`, as its stated right inverse shows.

Let `R_(H,m)` be the weight-`H`, length-`m` symmetric-polynomial space
and put `a(H,m)=dim R_(H,m)`, the number of partitions of `H` into `m`
parts. For `H>=2`, `L:R_(H,m)->R_(H-1,m)` is surjective by the
symmetric translation argument in PR 11. Hence

```math
 d_(H,m):=\dim(\ker L\cap R_(H,m))=a(H,m)-a(H-1,m),
```

and, writing `r_H=p(H)-p(H-1)`,

```math
 \sum_m d_(H,m)=r_H.                                      \tag{6}
```

For `N=2^lambda`, choose the least `h>=3` such that
`r_(h-1)>=(h-1)N`. By (6), choose `m` with `d_(h-1,m)>=N`, and choose
`N` basis elements `kappa_a` of that fixed-length kernel.

Define symmetric-polynomial labels

```math
 C_a=R_L\kappa_a,\qquad R_a=P\kappa_a.                       \tag{7}
```

Both have weight `h`; every `C_a` has length `m`, and every `R_a` has
length `m+1`. They are linearly independent and

```math
 T C_a=P L R_L\kappa_a=P\kappa_a=R_a.                        \tag{8}
```

The actual operator labels need the predecessor's factorial diagonal
change. If `D` multiplies the `mu` coordinate by `m_mu!`, use `D R_a`
on the dual/`a` side and `D^-1 C_a` on the scaled-monomial/`b` side.
PR 11's first-moment formula and (8) then give

```math
 G_1(D R_a,D^{-1}C_b)=h!\,[a=b].                              \tag{9}
```

For every `j>1`, the length difference is one, so (2) forces the
corresponding pairing to vanish. Since `c_(h,0)=0` and `c_(h,1)=1`,
the entire filtered pairing in (5), on these labels, is exactly
`h!` times the identity. This holds for all the higher moments at once,
not by a perturbation or a generic-rank assumption.

Choose any `N` monomial output states of weight `h`, using the same
codebook on `y` and `u`. With `x,v` indexing the labels in (7), define
actual rational pieces

```math
 A_s(x,y,u,v)=h!^{-1}B_s^{(h)}(D R_x,D^{-1}C_v)
              [t^{\sigma_u}]\,(\cdot)\,t^{\sigma_y},
             \qquad |s|\ge k.                                \tag{10}
```

Equation (5) and scalarity on the whole energy space yield

```math
 \sum_{|s|\ge k}A_s(x,y,u,v)=[x=v][y=u].                     \tag{11}
```

No generic matrix inversion is needed. The normalizer is `h!`.

## 4. Leading label capacity and a polynomial label-space overhead

PR 11 proved that `r_H` is nondecreasing and

```math
 p(H)\le1+(H-1)r_H,\qquad p(H)\le Hp(H-1).
```

At the minimal grade chosen above, `r_(h-2)<(h-2)N`. Therefore

```math
 r_{h-1}\le p(h-1)\le1+(h-2)r_{h-2}<1+(h-2)^2N,
```

and

```math
 p(h)\le h p(h-1)<h\bigl(1+(h-2)^2N\bigr)=O(h^3N).           \tag{12}
```

Thus every grade-`h` label, output and elimination space has only
polynomial-in-`h` overhead over `N`. Hardy--Ramanujan and the defining
thresholds, including the division by `h-1`, give

```math
 h=\Theta(\lambda^2),\qquad
 \kappa\sqrt h=\lambda+O(\log\lambda),                       \tag{13}
```

where `log_2 p(H)=kappa sqrt(H)+O(log H)`. In particular the
fixed-length restriction costs at most a logarithmic amount of label
capacity, not a constant factor in the exponent.

## 5. Uniform entries, coefficient heights and both ranks

The checker or constructor can enumerate partitions by weight and
length, compute a kernel basis by exact elimination, and apply the
finite formulas for `R_L`, `P` and `D`. These coefficients have
`O(h log h)`-bit denominators and numerators up to polynomial factors in
the source coefficients. Equation (12) bounds all label-space
dimensions by `2^O(lambda)`.

In (3), bring the coefficients to the common denominator
`((k-1)!)^2`. Each numerator is a sum of at most `2^(k-1)` unit-
bounded subset terms, so the filter coefficients have `O(h log h)`
bits. Charge coefficients of `Q_s` can be obtained by evaluation at
`0,...,d` and exact rational interpolation. Integer-charge source
entries have polynomial-in-`h` original height; evaluation and
interpolation add only `O(h log h)` bits. The number of shifts, charge
samples and moment coefficients is polynomial in `h`.

The normal-order recurrence uses intermediate grades at most `4h`.
By (13), their partition spaces have `2^O(lambda)` states. Hence all
selected labels, projected entries and both factorizations are uniformly
computable in `2^O(lambda)` bit time, with `2^O(lambda)`-bit rational
heights as a deliberately loose bound. There is no hidden inversion of
an `N`-by-`N` matrix. These are component construction costs, not a
claim of polynomial space for the later generic compiler.

For each retained shift, the predecessor's source bounds remain

```math
 R_s=\sum_{i=0}^{2h}p(s+i),\qquad
 C_s=\sum_{i=0}^{2h}p(2h-s-i).
```

Charge extraction and scalar multiplication preserve the corresponding
row and column intermediate subspaces. The factorial label changes are
fixed before factorization and do not alter these bounds. Therefore
both required flattening ranks, not merely a third cut, satisfy the
same `R_s` and `C_s` envelopes.

## 6. The improved two-direction ratio

There are `O(h)` retained pieces. For `|s|>=k`, the sum of the two
directional binary costs is at most

```math
 \kappa\bigl(\sqrt{2h+s}+\sqrt{2h-s}\bigr)+O(\log h).
```

The even concave function in parentheses decreases as `|s|` increases,
so its maximum occurs at `|s|=k`. Using (13) and `k/h=epsilon+O(1/h)`
gives

```math
 c_s^{\rm row}+c_s^{\rm col}
 \le \lambda\bigl(\sqrt{2+\epsilon}+\sqrt{2-\epsilon}\bigr)
     +O(\log\lambda).
```

Thus the uniform piece contract has

```math
 \boxed{\rho(\epsilon)=
 \frac{\sqrt{2+\epsilon}+\sqrt{2-\epsilon}}4}
 <\frac1{\sqrt2}\qquad(0<\epsilon\le1).                       \tag{14}
```

Strict concavity proves the final inequality. At `epsilon=1`,
`rho=(sqrt(3)+1)/4`.

## 7. Complete transferred cost and exact evidence boundary

The projection adds only polynomially many charge/moment terms and
`2^O(lambda)` entry-generation work. The piece count remains
polynomial, both rank envelopes are proved above, and the normalizer
and rational heights are explicit. PR 17's bounded odd-prime transfer
can therefore pay exact rational factorization and signed integer
query recovery without assuming polynomial-height integer factors.
Retain all source reduction branches, rejected greedy queries, graph
profiles, entry computations, recovery, recursive calls, finite
fallbacks and the arbitrary-density overhead.

Under the pinned Anthropic master interface, the resulting conditional
exponent is

```math
 \alpha(\epsilon)=\log_2(1/\rho(\epsilon))>1/2.
```

For `epsilon=1`, this is `log_2(4/(sqrt(3)+1))`, approximately `0.55`.
The general-density iterated-log correction and the compiler's
exponential-space caveat are unchanged. Any returned count is exact;
the transfer's one-sided decision error and worst-outcome time bound
are retained.

This is an author-checked component proof and a conditional master
cost consequence, not an independently reviewed or selected SAT
result. Finite code must still replay scalarity, the length rule, the
complete output crossing and both rank bounds. The selected record is
unchanged pending the repository's review requirements.
