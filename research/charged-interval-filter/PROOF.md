# Obstruction to the registered charged interval-filter identity

Status: `scoped_checked` counterexample, substantially AI-assisted. The OpenAI
theorem is accepted as a premise. This note does not review that theorem and
claims no component-ratio or SAT-bound improvement. Source pins are in
[SOURCES.json](SOURCES.json).

## 1. The valid highest-charge moment statement

Put a zero-mode charge `q` only on the dual/`a` side and keep the operator/`b`
side uncharged. Write `Q_s^(q)` for the resulting pieces and
`Q_(s,j)=[q^j]Q_s^(q)`. On any fixed output energy space, the unweighted moment

```math
 S_j(a,b)=\sum_s s^jQ_(s,j)(a,b)
```

is scalar. Indeed the `j`-th logarithmic derivative leaves at most `j` weight
uncontracted, while charge degree `j` requires `j` zero currents. Thus all
surviving uncontracted currents are scalar zero modes. The same contraction
count gives the length rule `ell(mu)=ell(nu)+j` for a nonzero monomial pairing.
These statements concern the **whole unweighted moment**. The checker verifies
both of them and the equality of the two operator orders at bounded grades.

They do not say that `Q_(s,j)` is scalar at a fixed shift, nor that an arbitrary
shift-weighted highest-charge sum is scalar. At a fixed Laurent coefficient,
terms with more than `j` uncontracted weight can occur; the local derivative
argument no longer applies.

## 2. Two repairable normalization errors in the draft

Let `kappa_a` be a basis of a fixed-length subspace of `ker L`, and put
`C_a=R_L kappa_a` and `R_a=P kappa_a`. Then `T C_a=R_a`, but a general basis
does not make the first-moment pairing the identity. It gives the nonsingular
Gram/minor

```math
 M_(ab)=h!\sum_mu R_a[mu]\,(TC_b)[mu].
```

An actual crossing must apply `M^-1`; diagonal recovery without that inverse
was unjustified.

There is also a factorial-orientation correction. If `D` multiplies the `mu`
coordinate by `m_mu!`, the actual labels must be `D^-1 R_a` on the dual side
and `D C_b` on the scaled-monomial side. This follows directly from the
predecessor pairing `h!(m_mu!/m_nu!)[u^mu]T(u^nu)`. The opposite orientation in
the draft does not give `M`.

These two repairs make the full, unweighted projected identity testable. They
do not repair the central omission below.

## 3. A polynomial root does not kill a charge-projected piece

For an odd polynomial `w(s)=sum_j c_j s^j`, the draft defined

```math
 B_s=\sum_j c_j s^jQ_(s,j).                                  (1)
```

The assertion `w(s)=0 => B_s=0` is algebraically invalid: `Q_(s,j)` are
different tensors for different `j`, not a common tensor multiplied by `q^j`.
Consequently the retained sum need not equal the full moment sum.

The checker constructs the complete `h=3` example. With
`w(s)=s(s^2-1)=-s+s^3`, the corrected one-label minor is `M=6`. At output
`y=(1,1,1)`, the full sum is the required scalar `-6`, but after omitting
`|s|<2` the retained sum is

```text
(1,1,1): -324,  (3): -504.
```

The omitted central sum is therefore `(1,1,1):318, (3):504`; in particular it
has a nonzero off-diagonal output. At least one central projected piece is
nonzero. Thus (1) does not construct the claimed crossing with `s=-1,0,1`
removed, even after both normalization repairs.

The overall sign relative to the draft's normalized polynomial `s(1-s^2)` is
immaterial. This is a complete tensor counterexample, not a rank computation
or an inference from one matrix entry.

## 4. Multiplying by another rooted polynomial does not fix it

A proposed repair replaces `B_s` by `w(s)B_s`. Now the central pieces vanish,
but the retained sum contains weighted highest-charge terms

```math
 \sum_s w(s)s^jQ_(s,j).
```

These need not be scalar: the additional weight changes the effective moment
order without increasing the charge order. Terms with more uncontracted
weight than `j` survive, exactly the terms excluded in Section 1.

In the same `h=3` example, the repaired retained sum is `-1296` on `(1,1,1)`,
whereas the first-moment prediction is `-26208`. Hence this repair also fails.
A cubic first-charge-only filter can accidentally retain scalarity in small
cases, but quintic filters already exhibit non-scalar outputs; such bounded
observations are not used as a uniform construction here.

## 5. Evidence boundary and the remaining problem

The independent finite raw-charge screen in `charge-polynomial-filter` remains
useful evidence about particular codebooks. It does not validate the proposed
all-size identity, and the present counterexample does not refute those finite
constructions or every possible charge filter.

A valid constant-fraction central filter must either control the entire omitted
central tensor sum or use a genuinely different scalar recovery mechanism. It
must still prove leading label/output capacity, both directional rank bounds,
uniform entry heights and every rational-transfer and recursion cost. The
former draft's conditional `rho(epsilon)` and alpha formulae are therefore
withdrawn. No selected-result change is claimed.
