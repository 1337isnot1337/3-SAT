# Weighted oscillator rigidity

Status: `scoped_checked`. The [proof](PROOF.md) gives an all-size,
author-checked classification for arbitrary scalar creation and annihilation
weights under the existing h=1 two-order identity. In characteristic zero,
their products must be `c k`; if `c` is nonzero every oscillator is present
and the operators reduce to the standard family by coordinate and common
scalar changes. If `c=0`, the usual vacuum-derivative pairing vanishes on
all positive grades. Neither case excludes a different identity, a coupled
representation, or a different pairing. The proof also shows that an
infinitely supported scalar commutator sequence obeying an eventually
nondegenerate order-d recurrence, even with coefficients varying by index,
has lower support density at least 1/d;
this is sharp and applies to arbitrary weights over any field. A separate
characteristic-p example satisfies the scalar h=1 identity with nonzero c but
has missing annihilation modes and a degenerate standard vacuum pairing. No SAT time or
alpha improvement is claimed; no independent review or formal verification
was performed.

This extends the exact missing-index obstruction of
[the predecessor](../sparse-oscillator-locality/PROOF.md) to arbitrary scalar
reweighting. Source: Anthropic, *A 2^{o(n)} Time Algorithm for 3-SAT*,
Appendix B, Lemma 9, source repository commit
`16a5ce41304fcdaea4e0be7c132e1c361dc26da5`; source capture and licenses are
in [the scan](../recent-breakthrough-scan/SOURCES.json). Canonical repository
base `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`. Contributor: Cinna Davis,
with substantial OpenAI Codex assistance. New material is Apache-2.0.

Reproduce from repository root with Python 3.11+ and standard library:

```sh
python3 -I -B research/weighted-oscillator-rigidity/verify.py
make verify
```

The first command tests all 15,625 choices of three creation and three
annihilation weights in `{-2,-1,0,1,2}`. It directly applies operators for
375,000 differences at shifts 0, 1, 2 on eight basis monomials, and checks
125,000 vacuum pairing entries. It checks the finite classification on
these shifts; it does not establish the all-size proof. It also replays 14,760
finite constant- and varying-coefficient scalar-recurrence sequences and four
sharp periodic controls. It also checks 192 finite-characteristic identities
and eight pairing-radical controls. A first checker run
wrongly required a canonical zero polynomial to have a particular exponent
representation; the corrected checker compares its coefficient and checks
exponents only when nonzero. This was a checker representation bug, not a
mathematical counterexample.

Success for this round was a precise all-size necessary condition with a
finite direct replay. The stopping condition is reached for scalar weighting
of the unchanged h=1 identity and bounded-order scalar locality. The complete
global cost remains open: the
result does not supply an encoding, piece construction, recovery, recursive
schedule, or entry bounds. A useful continuation would specify a changed
operator identity with non-scalar locality, vanishing leading coefficients,
growing recurrence order, or a coupled representation and prove both
factorization orders and label recovery before evaluating cost.
