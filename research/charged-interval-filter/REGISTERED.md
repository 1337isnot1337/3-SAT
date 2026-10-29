# Registered proposal status: falsified as stated

Base: canonical main `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`.
Task: `contraction-schedule`. The accepted OpenAI baseline and selected result
are unchanged.

The registered left-charged polynomial interval filter proposed to combine
`s^j[q^j]Q_s^(q)` and then omit shifts at the roots of the scalar polynomial.
Exact tensor construction shows that this omission is invalid: the charge
coefficients are different tensors, so a scalar polynomial root does not make
their combination vanish.

See [PROOF.md](PROOF.md) for the complete `h=3` counterexample, the failed
extra-factor repair, and two corrections to the full unfiltered normalization.
The predicted uniform rho(epsilon) and alpha(epsilon) consequences are
withdrawn. The separate finite raw-charge constructions are outside the scope
of this counterexample.
