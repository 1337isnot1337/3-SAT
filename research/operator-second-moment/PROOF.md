# Second-moment spectrum and a quadratic crossing filter

Status: author-checked, substantially AI-assisted research. The OpenAI theorem
is accepted as a premise. This note studies the external Anthropic operator
construction; it neither audits that theorem nor claims a SAT bound improvement.
Source and predecessor pins are in [SOURCES.json](SOURCES.json).

## 1. Polynomial operators and the exact second moment

Let `R=Q[u_1,u_2,...]`, with `weight(u_j)=j`. For a partition `nu`, write
`u^nu=prod_(j in nu)u_j` and `m_nu!=prod_j mult_j(nu)!`. Define

```math
 L=\sum_{j\ge2}(j-1)u_{j-1}\frac{\partial}{\partial u_j},
 \qquad A=e^L,
```

```math
 B=\sum_{j\ge1}u_{j+1}\frac{\partial}{\partial u_j},
 \qquad F=\sum_{r\ge1}(-1)^{r-1}r u_r,
```

```math
 U_h=\frac1{2h}F\left(FA+2A\frac\partial{\partial u_1}\right).
```

Every expression is finite on a polynomial. On weight-`h` input, `U_h` is
followed by extraction of weight `h`, giving an operator `R_h -> R_h`.
Also `A(u_j)=sum_(n=1)^j binom(j-1,n-1)u_n`.

**Theorem 1.** For every `h>=1`, partitions `mu,nu` of `h`, and every output
energy space `V_E`, the uncharged pieces satisfy

```math
 \sum_s s^2Q_s(a_\mu,b_\nu)
 =4hE\,h!\,\frac{m_\mu!}{m_\nu!}[u^\mu]U_h(u^\nu)\operatorname{Id}.
 \tag{1}
```

The derivation uses the Laurent contraction expansion of PR 11. Terms with no
uncontracted field have no second derivative at the diagonal, and one free
weight-one current has no equal-energy matrix coefficient in the uncharged
construction. Only two free weight-one currents contribute, with scalar mode
trace `4hE`.

If both free factors are on the encoded first side, the transformed contraction
identity

```math
 \sum_n(-1)^{r+n}{r\choose n}\gamma_{n,m}
 =m{m-1\choose r-1}
```

leaves `A` on the other factor pairs and gives `F^2A`. If one free factor is on
each side, selecting the column factor differentiates its monomial before `A`.
Weight conservation and the same alternating binomial sums cancel every column
part except `u_1`, giving `2FA partial/partial u_1`. Two free factors on the
second side alone cannot conserve weight. This proves (1). The independent
normal-ordered implementation checks the formula entry by entry at the finite
grades and energies in [verification.json](verification.json).

The same factorial bookkeeping shows that `2hU_h` has integer entries in the
partition-label normalization. The checker also tests this integrality
explicitly through weight 14.

## 2. The all-size spectral decomposition

Write `p(h)` for the partition count, with `p(t)=0` for `t<0`, and put
`a_h=(h-2)/h`. PR 11 proved that `L:R_j -> R_(j-1)` is surjective for every
`j>=2`. On each fixed partition length `m`, `[L,B]=m Id`.

**Lemma 2 (operator identities).** For every `h>=1`,

```math
 L^2U_h=0,                                               \tag{2}
```

```math
 U_hk=k\qquad(Lk=0),                                    \tag{3}
```

and, on `H_h=ker L_h^2`,

```math
 L(U_h+a_h)=0.                                          \tag{4}
```

These are graded polynomial identities. For (2), expand
`F(FA+2A partial/partial u_1)` and collect weight-`h` terms; the transformed
binomial coefficients cancel after two applications of `L`. For (3), `Ak=k`
on `ker L`, and the remaining symmetric translation-invariant sum is the
constant term. For (4), decompose `f in H_h` as `f=k_0+Bk_1`, where
`Lk_0=Lk_1=0`: surjectivity of `L` and `[L,B]=m` make this decomposition
unique. Substitution in the definition of `U_h` gives
`U_h(Bk_1)+a_hBk_1 in ker L`, while (3) handles `k_0`. Equivalently,
`LU_h=-a_hL` on `H_h`. [verify.py](verify.py) independently checks all three
identities through weight 14; the finite checks are evidence for, not a
replacement of, this expansion.

**Theorem 3.** For every `h>=1`,

```math
 U_h(U_h-1)(U_h+a_h)=0,                                 \tag{5}
```

```math
 \operatorname{rank}U_h=p(h)-p(h-2).                    \tag{6}
```

Moreover `image U_h=H_h`. The eigenvalue `1` has multiplicity
`p(h)-p(h-1)`, and `-(h-2)/h` has multiplicity `p(h-1)-p(h-2)` (with the
obvious small-`h` conventions).

**Proof.** By (2), `image U_h` is contained in `H_h`. Since `L^2` is surjective
onto `R_(h-2)`,

```math
 \dim H_h=p(h)-p(h-2).
```

On `H_h`, (3) and (4) imply `(U_h-1)(U_h+a_h)=0`. For arbitrary `g`, `U_hg`
lies in `H_h`, proving (5). The restriction of `L` to `H_h` has kernel
`ker L_h` and is onto `ker L_(h-1)`: if `Lk=0` has length `m`, then
`L(Bk/m)=k`. Thus the two nonzero eigenvalue multiplicities are

```math
 \dim\ker L_h=p(h)-p(h-1),\qquad
 \dim\ker L_{h-1}=p(h-1)-p(h-2).
```

Their sum is `dim H_h`. The restriction of `U_h` to `H_h` has full rank on
that subspace (including the rank-one `h=2` case), so `image U_h=H_h` and (6)
follows. ∎

In particular the full common-label second-moment pairing is singular for every
`h>=2`, with nullity `p(h-2)`, but its nonzero spectrum is completely explicit.

## 3. An explicit normalizer inverse

For `h>=3`, define spectral projectors

```math
 P_0=-a_h^{-1}(U_h-1)(U_h+a_h),\qquad
 P_1=\frac{U_h(U_h+a_h)}{1+a_h},
```

```math
 P_-=\frac{U_h(U_h-1)}{a_h(1+a_h)}.
```

Then

```math
 (I-4h^2U_h)^{-1}
 =P_0+\frac{P_1}{1-4h^2}+\frac{P_-}{1+4h(h-2)}.         \tag{7}
```

The denominators are nonzero. For `h=1`, `U_1=1` and the inverse is `-1/3`.
For `h=2`, `U_2^2=U_2` and

```math
 (I-16U_2)^{-1}=I-\frac{16}{15}U_2.                     \tag{8}
```

Thus the inverse uses only `U_h` and `U_h^2`, not generic exponential-height
adjugates. Since `2hU_h` is integral, its entries have polynomial-in-`h`
height. Summing over at most `p(h)` labels and clearing the displayed
polynomial denominators preserves a polynomial-in-`h` bit-height bound up to
the explicit label-count factor accounted below.

## 4. Actual crossing pieces omitting `s=+1` and `s=-1`

Normalize the source pieces at output energy `E=h` by `h!`, writing

```math
 \sum_s C_s=I,\qquad \sum_s s^2C_s=4h^2U_h.              \tag{9}
```

Let `M_h=I-4h^2U_h`. For every shift other than `+1` and `-1`, define

```math
 A_s=(1-s^2)(M_h^{-1}\otimes I)C_s,                     \tag{10}
```

where the inverse acts on the first (`x`) label. Then

```math
 \sum_{s\ne\pm1}A_s=M_h^{-1}(I-4h^2U_h)=I.              \tag{11}
```

These are actual rational functions, not merely a rank hypothesis. On the row
flattening the transformation is `(1-s^2)M_h^{-1}\otimes I_y`, and on the
column flattening it is `(1-s^2)M_h^{-1}\otimes I_u`. Both are invertible for
every retained shift. Consequently BOTH directional ranks are exactly
preserved.

For a target `N=2^lambda`, choose the least `h` with `p(h)>=N` and use all
partitions of `h` as labels. The predecessor's injection gives
`p(h)<=h p(h-1)`, so minimality implies

```math
 N\le p(h)<hN.                                          \tag{12}
```

Thus only `2^O(lambda)` labels are needed, and `h=Theta(lambda^2)` by the same
Hardy--Ramanujan estimate used in PR 19. Explicit generation of `U_h`, its
square and (7), followed by the source normal-order recurrence, takes
`2^O(lambda)` bit time. The rational entries have `O(lambda)` bits apart from
polynomial bookkeeping in `h`; no factorial-height inverse is used.

There are `4h-1` pieces: the original `4h+1` shifts with `+1` and `-1`
removed. This improves the piece count by two, and by one relative to PR 19's
first-moment family. The central shift and all other nearby shifts remain.
The source's two-direction term envelope is unchanged, so the supplied ratio
is still `rho=1/sqrt(2)`, with no SAT alpha improvement.

## 5. Full cost transfer and evidence boundary

PR 17's bounded exact prime-field transfer applies to this explicit rational
rank-only family. It pays all parameter denominators, recovers exact signed
integer outer queries and preserves the source master-time envelope. Retain
every reduction branch, rejected greedy query, profile, entry computation and
recursive call. The generic compiler's exponential space and one-sided
decision error remain explicit. No full SAT solver is implemented here.

The checker verifies the spectral inverse against independent Gauss--Jordan
elimination, constructs all actual filtered pieces through weight 4, checks
723 crossing identities and compares both directional flattening ranks with
the unfiltered pieces. It also checks (2)--(6) at bounded grades. These finite
checks do not independently review the all-size proof, the external theorem or
the full transfer. No selected-result change is claimed.

Deleting two isolated shifts cannot improve the leading term envelope while
`s=0` and nearby shifts remain. A further improvement needs a higher-moment
family or another mechanism that removes a whole central interval with paid
normalization and both rank bounds.
