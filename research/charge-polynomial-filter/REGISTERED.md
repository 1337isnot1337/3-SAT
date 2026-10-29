# Registered charge-filter constructions and rescaling comparison

Base: canonical main `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`.
Task: `contraction-schedule`. The accepted OpenAI baseline and selected result
remain unchanged.

## Raw and inverse-length spaces

The original screen spans every raw charge coefficient on the PR 19 codebooks.
The subsequently registered inverse-length premise multiplies a raw `(mu,nu)`
entry by `q^(-len(mu)-len(nu))`, or equivalently reindexes charge degree `d` to
contraction deficit `len(mu)+len(nu)-d`. `deficit.py` classifies every cutoff
in that finite space.

## New length-amplified space

`generalized.py` tests the distinct local diagonal rescaling

```text
Q_s^(q)(mu,nu) -> q^(len(mu)+len(nu)) Q_s^(q)(mu,nu).
```

For nonzero charge this is invertible on each row/column label pair and hence
preserves both directional ranks at each charge. Its coefficient of degree
`d+len(mu)+len(nu)` is exactly the raw degree-`d` coefficient. The checker
compares fixed-charge evaluations, spans the complete resulting scalar space,
and tests actual normalized crossings.

At `lambda=2,h=6`, the raw space has an invertible scalar pairing through
cutoff 4 but none at cutoff 5. The length-amplified space has an actual
crossing through cutoff 5, removing `-5,...,5`, but its entire scalar matrix
space is identically singular at cutoff 6. These are finite results only;
no all-size selector, uniform capacity proof, smaller rho or larger SAT alpha
is claimed.

The separate `charged-interval-filter` counterexample concerns a proposed
all-size highest-charge identity. It does not alter these explicit finite
raw, deficit or amplified witnesses.
