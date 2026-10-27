# Charge-projected interval filters: a piecewise obstruction

Status: refuted construction, author-checked and substantially AI-assisted.
This note corrects the preceding draft on this branch. It does not claim
an improved ratio or SAT bound. The accepted OpenAI baseline and selected
result are unchanged.

## 1. Scalar highest-charge moments and their length rule

Put the zero mode `D_0=q Id` only on the left operator side. Let
`Q_s^(q)` be the resulting charged pieces and define

```math
 M_j^{(q)}=\sum_s s^jQ_s^{(q)},\qquad S_j=[q^j]M_j^{(q)}.
```

The normal-ordered Laurent expansion has uncontracted weight `r` multiplying
`(z_1-z_2)^r`. The `j`-th derivative kills `r>j`, while charge degree `j`
requires `j` zero currents and hence `r>=j`. Thus every survivor is a
weight-one left zero mode, so

```math
 S_j(a,b)=G_j(a,b)\operatorname{Id}.                       \tag{1}
```

For monomial labels, exactly `j` left factors remain uncontracted and no
right factor does. Full contraction pairs equal numbers of remaining
factors, giving the length rule

```math
 G_j(a_\mu,b_\nu)\ne0\quad\Longrightarrow\quad
 \ell(\mu)=\ell(\nu)+j.                                      \tag{2}
```

These two statements remain valid and are useful for later constructions.

## 2. Correction: a scalar zero is not a projected-piece zero

For a polynomial `w(s)=sum_(j=0)^d c_j s^j`, the preceding draft defined

```math
 B_s=\sum_{j=0}^d c_j s^j[q^j]Q_s^{(q)}.                      \tag{3}
```

Summing over every shift does give

```math
 \sum_sB_s=\sum_{j=0}^d c_jS_j.                               \tag{4}
```

But `w(a)=0` does **not** imply `B_a=0`: the vectors `[q^j]Q_a` need not
be proportional for different `j`. Therefore the draft's first equality
in its filtered-crossing identity was unjustified, and its claimed
central-interval deletion and improved `rho` are withdrawn.

This is not repairable by dividing (3) by `w_s` on retained shifts. Doing
so still leaves the original central `B_s` contributions in (4), and on
the proposed fixed-length minor those central contributions need not
vanish. A finite scalar pairing identity alone cannot authorize omission
of pieces.

There is a coefficientwise way to state the obstruction. Suppose a
same-shift charge-linear piece has the form

```math
 R_s=\sum_j a_j(s)[q^j]Q_s^{(q)},
```

and scalar weights `w_s` are used to realize the moment combination
`sum_j c_jS_j`. Matching independent charge/moment coefficients asks for
`w_s a_j(s)=c_j s^j`. If `w_a=0` at a nonzero central shift `a`, this
forces `c_j=0` for every `j>=1`; if `w_0=0`, it also forces `c_0=0`.
Operator relations could weaken this coefficientwise formulation, but
they must be exhibited explicitly; they cannot be assumed from (4).

## 3. The single highest-charge route does delete pieces

There is one direct implementation with genuinely vanishing central
pieces. Fix the degree `d` and use the same charge projection at every
shift:

```math
 R_s=[q^d]Q_s^{(q)},\qquad A_s=w_sR_s.
```

If `w_s=0`, then `A_s=0` without any further assumption. Since
`[q^d]M_j=0` for `j<d`, the full sum is only

```math
 \sum_s w_sR_s=c_dS_d.                                      \tag{5}
```

The lower coefficients cannot contribute. Thus this route realizes only
the highest-charge pairing, not a first-moment-anchored combination.

For the central grid `|s|<k`, take

```math
 w_h(s)=s\prod_{r=1}^{k-1}(1-s^2/r^2),\qquad d=2k-1.          \tag{6}
```

Then `c_d` is nonzero, all central projected pieces vanish, and only
`|s|>=k` remains. Equation (1) permits scalar normalization if the label
capacity and other contracts are paid.

## 4. The unavoidable capacity charge

The predecessor's support argument applies directly to `S_d`. A monomial
of `a_mu` has `ell(mu)` currents and one of `b_nu` has `ell(nu)`. Charge
degree `d` requires `ell(mu)+ell(nu)>=d`. Consequently rows or columns
of length at least `t=ceil(d/2)` cover the label matrix, and

```math
 \operatorname{rank}G_d\le2h\,p(h-t).                         \tag{7}
```

For the odd degree in (6), `t=k`. Hence any binary label dimension
`N=2^lambda` extracted from this pairing obeys

```math
 \lambda\le\kappa\sqrt{h-k}+O(\log h),                       \tag{8}
```

where `log_2 p(H)=kappa sqrt(H)+O(log H)`. For `k=h` there is no
exponential label family at all. The earlier fixed-length invariant idea
cannot avoid (7): diagonalizing a restricted minor does not increase its
rank.

Charge extraction and scalar weights preserve both source intermediate
spaces. For retained shifts, the combined directional bit envelope is
therefore maximized at `|s|=k` and equals

```math
 \kappa\sqrt h\bigl(\sqrt{2+k/h}+\sqrt{2-k/h}\bigr)+O(\log h).
```

Write `eta=k/h`. Combining this with the actual label capacity in (8),
any ratio certified by these bounds must satisfy, asymptotically,

```math
 \rho\ \gtrsim\ \frac{\sqrt{2+\eta}+\sqrt{2-\eta}}
                         {4\sqrt{1-\eta}}.                    \tag{9}
```

The denominator in (9) is the lost label capacity. Omitting it would
repeat the draft's error at the level of the rate calculation.

## 5. Exact no-improvement inequality

For `0<eta<1`, define

```math
 S(\eta)=\sqrt{2+\eta}+\sqrt{2-\eta}.
```

Then

```math
 S(\eta)^2=4+2\sqrt{4-\eta^2}.
```

We claim

```math
 \frac{S(\eta)}{4\sqrt{1-\eta}}>\frac1{\sqrt2}.             \tag{10}
```

After positive rearrangement, this is
`sqrt(4-eta^2)>2-4eta`. It is immediate when `eta>=1/2`. When
`0<eta<1/2`, squaring both positive sides gives the equivalent strict
inequality `16eta>17eta^2`, which holds because `eta<1/2<16/17`.
At `eta=0`, equality instead gives the original `1/sqrt(2)` envelope.

Thus every fixed central fraction deleted by the single highest-charge
polynomial route makes the certified two-direction ratio strictly worse
after its label loss is charged. Increasing the degree to remove more
shifts is not an improvement. This closes that route asymptotically,
not merely at finite sizes.

## 6. Remaining changed premises

This is not a lower bound on every charged construction. A successor
must change at least one premise:

1. exhibit operator relations allowing a mixed-charge scalar pairing to
   be decomposed into pieces that themselves vanish throughout a central
   interval;
2. use a genuinely charge-dependent or non-polynomial piece family and
   prove both its scalar output and label rank; or
3. use a non-scalar product recovery while preserving both required
   directional factorizations.

A new proof must state the actual retained pieces first, then verify the
crossing sum. Starting from a scalar moment identity and deleting terms
afterward is insufficient. No smaller `rho`, larger `alpha`, selected
result, independent review or formal verification is claimed here.
