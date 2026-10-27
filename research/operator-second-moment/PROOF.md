# Exact second moment of the uncharged crossing pieces

Status: author-checked, substantially AI-assisted research. The OpenAI theorem
is accepted as a premise. This note studies the external Anthropic operator
construction; it neither audits that theorem nor claims a SAT bound improvement.
Source and predecessor pins are in [SOURCES.json](SOURCES.json).

## 1. Polynomial operators

Let `R=Q[u_1,u_2,...]`, with `weight(u_j)=j`. For a partition `nu`, write
`u^nu=prod_(j in nu)u_j` and `m_nu!=prod_j mult_j(nu)!`. Define

```math
 L=\sum_{j\ge2}(j-1)u_{j-1}\frac{\partial}{\partial u_j},
 \qquad A=e^L,
```

```math
 F=\sum_{r\ge1}(-1)^{r-1}r u_r,
 \qquad
 U_h=\frac1{2h}F\left(FA+2A\frac\partial{\partial u_1}\right).
```

Every expression is finite on a polynomial. Although `A` and `F` can change
weight, `U_h` is followed by extraction of weight `h`. On monomials of weight
`h`, this gives a linear operator `R_h -> R_h`. Equivalently,

```math
 A(u_j)=\sum_{n=1}^j {j-1\choose n-1}u_n.
```

The implementation in [second.py](second.py) evaluates this definition without
using the normal-ordered operator code.

## 2. Exact second-moment formula

**Theorem 1.** For every `h>=1`, partitions `mu,nu` of `h`, and every output
energy space `V_E`, the uncharged pieces satisfy

```math
 \sum_s s^2Q_s(a_\mu,b_\nu)
 =4hE\,h!\,\frac{m_\mu!}{m_\nu!}[u^\mu]U_h(u^\nu)\operatorname{Id}.
 \tag{1}
```

Equivalently, the scalar in the predecessor's partition-label normalization is
`4hE h! U_h`.

The derivation uses the same Laurent contraction expansion as PR 11. Terms with
no uncontracted field have no second derivative at the diagonal. A single free
weight-one current has no equal-energy matrix coefficient in the uncharged
construction. Thus only two free weight-one currents contribute. Their two
opposite energy shifts give the scalar factor `4hE`; the remaining factorial is
the same fully contracted normalization as in the zeroth crossing.

There are two possible locations for the free factors:

1. Both are on the encoded first side. The transformed contraction identity
   `sum_n (-1)^(r+n) binom(r,n) gamma_(n,m)=m binom(m-1,r-1)` leaves the
   exponential `A` on all other factor pairs. The two free insertions give
   `F^2A`.
2. One is on each side. Selecting the free column factor differentiates its
   monomial before applying `A`. Weight conservation and the same alternating
   binomial sums cancel every column part except `u_1`; the remaining row
   insertion gives `2FA partial/partial u_1`.

Two free factors on the second side alone cannot conserve weight: the
transformed contraction requires each contracted column part to be at least its
matched row part. Combining the two cases and the mode trace yields (1). The
independent normal-ordered implementation checks this formula entry by entry at
the finite grades and energies recorded in [verification.json](verification.json).

## 3. Length filtration and uniform singularity

Multiplication by `F` adds one factor and `partial/partial u_1` removes one.
Consequently

```math
 U_h(R_{h,\ell})\subseteq R_{h,\ell}\oplus R_{h,\ell+2},
```

where `R_(h,ell)` is the length-`ell` subspace. No term lowers partition length.
This explains the block-triangular structure but does not by itself prove
singularity: some length-preserving diagonal entries are nonzero.

**Proposition 2.** The full common-label pairing in (1) is singular for every
`h>=2`.

For `h=2`, `U_2(u_2)=0`. For `h=3`,

```math
 U_3(6u_3-u_1^3)=0.
```

For `h>=4`, we exhibit a larger uniform kernel family. Put

```math
 D=A\frac\partial{\partial u_1}A^{-1}
  =\frac\partial{\partial u_1}-\frac\partial{\partial u_2},
```

where the conjugation identity follows from `[L,partial/partial u_1]=-partial/partial u_2`.
Let `v=u_1+u_2`, `C=sum_(r>=3)(-1)^(r-1)r u_r`, and

```math
 S=-\frac34u_1^2+\left(v-\frac C2\right)u_1.
```

Then `D(u_1)=1`, `D(v)=D(C)=0`, and `2DS=-F`. Hence, for every polynomial
`f` with `Df=0`,

```math
 (F+2D)(e^Sf)=0.                                    \tag{2}
```

The variables `v,u_3,u_4,...` generate `ker D` and have weights `2,3,4,...`.
Choose any nonzero `f in ker D` of weight `h-2`; such an `f` exists for every
`h>=4`. Define

```math
 g=[A^{-1}(e^Sf)]_{\rm weight\ }h.                  \tag{3}
```

Only grades at most `h` of `e^Sf` can enter `F(F+2D)Ag` before the final weight
`h` extraction. Thus (2) implies `U_h(g)=0`. Finally `S` starts in weight two,
with weight-two component `u_1^2/4`, so the weight-`h` component of `g` is
`u_1^2f/4`. In particular `g` is nonzero. This proves the proposition.

The construction gives a lower bound on nullity, not the exact rank. Finite
exact elimination observes

```math
 \operatorname{rank}U_h=p(h)-p(h-2)                 \tag{4}
```

for `1<=h<=10`. It also observes the operator identity

```math
 U_h(U_h-1)\left(U_h+\frac{h-2}{h}\right)=0          \tag{5}
```

on the same finite grades. Equations (4) and (5) are **finite observations, not
all-size claims** in this package. An all-size proof would supply a much
sharper spectral decomposition and is the next algebraic target.

## 4. Possible crossing filter and its unpaid obligations

At output energy `E=h`, divide the zeroth and second moments by `h!`:

```math
 \sum_s C_s=I,
 \qquad
 \sum_s s^2C_s=4h^2U_h.                              \tag{6}
```

Formally, if `I-4h^2U_h` has a uniform computable inverse with paid entry costs,
multiplying the pieces by `1-s^2` and that inverse gives a crossing sum using
only shifts with `s not in {+1,-1}`. The finite identity (5) shows invertibility
at the checked grades. It is not yet a uniform construction. A successor must
prove all-size invertibility, preserve both directional flattening ranks, and
charge inverse heights, entries, precision and every recursive overhead.

Even if completed, deleting only `+1` and `-1` leaves `s=0` and nearby shifts;
it does not by itself improve the leading `rho=1/sqrt(2)` envelope or SAT alpha.
This is a concrete component-filter route, not a claimed asymptotic result.

## 5. Scope and cost boundary

No new reduction, query family, tensor network, recursive schedule or SAT
algorithm is constructed here. There are therefore no new reduction branches,
queries, tensor entries, modes, precision levels, random bits or amplification
costs to charge. The accepted general and fixed-density envelopes and the
selected result remain unchanged. The exact formula and singularity are results
about the named operator pairing; the finite ranks and spectral checks are not
independent review or proof of an asymptotic algorithm.
