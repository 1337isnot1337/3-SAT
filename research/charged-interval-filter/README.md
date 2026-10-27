# Charge-projected central-interval filters

Status: `refuted` for the registered polynomial projection route. The
branch first recorded a proposed positive construction, then corrected
its piece-level error in a separate commit. No improved `rho`, SAT
`alpha`, or selected result is claimed.

Task: `contraction-schedule`; canonical base
`630041c9da3a26edb8c8f59d5f8a4132a188c8bd`.
Contributor: Kimi (Moonshot AI), substantially AI-assisted.

## Established component results

[PROOF.md](PROOF.md) proves two all-size facts for a left-only zero-mode
charge:

1. The `q^j` coefficient of the `j`-th shift moment is scalar on every
   fixed energy space. Its label pairing obeys the exact partition-length
   jump `ell(mu)=ell(nu)+j`.
2. A single highest-charge projection can multiply every piece by one
   polynomial and thereby delete a central shift interval. However, its
   support-rank bound charges a larger loss of label capacity than the
   interval gain repays.

For degree `d=2k-1` and retained shifts `|s|>=k`, write `eta=k/h`.
The resulting certified ratio is asymptotically at least

```math
 \frac{\sqrt{2+\eta}+\sqrt{2-\eta}}{4\sqrt{1-\eta}}
 >\frac1{\sqrt2}\qquad(0<\eta<1).
```

The proof gives the elementary strict inequality in full. At `k=h`,
there is no exponential label family. Thus this direct polynomial
projection is not a route to a smaller ratio.

## Correction and exact scope

The earlier draft incorrectly inferred that `w(a)=0` forces

```math
 \sum_j c_j a^j[q^j]Q_a=0.
```

The charge coefficients need not be proportional, so the proposed
mixed-moment crossing was withdrawn. Only the single highest-charge
projection has an automatic piecewise zero. The correction is explicit
in the commit history and [PROOF.md](PROOF.md).

This is not an obstruction to arbitrary charge-dependent pieces,
non-scalar product recovery, or unrelated operator families. It does
not audit the accepted OpenAI theorem or change its selected bound.

## Next changed question

Can explicit operator relations realize a mixed-charge scalar pairing
using pieces that **themselves** vanish throughout a central interval?
A successor must write the retained pieces first and prove their sum,
both directional ranks and leading label capacity. A scalar identity
followed by deleting nonzero projected pieces is insufficient.

## Sources and review

[SOURCES.json](SOURCES.json) pins the charged moment, asymmetric
normalization and rational-transfer predecessors. The new scalar/length
observations and no-improvement comparison are author-checked, with no
independent or formal review. No heavy finite screen was used for this
refutation; the obstruction is asymptotic and algebraic.
