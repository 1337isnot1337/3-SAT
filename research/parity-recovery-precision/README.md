# Parity recovery still needs precision

Task: `decision-only`. Status: `scoped_checked`, AI assisted, with no
independent review. No improved SAT algorithm or alpha.

This follows up a failed fixed-packet shortcut supplied in the user's
research transcript. That shortcut inferred `F(-2)=F(0) mod 2` from
integrality of `F(t+alpha z)`. The source does not assert integral global
coefficients, and the inference is false.

The [proof](PROOF.md) strengthens the initial counterexample to an all-node,
all-jet precision obstruction. For the actual diagonal entry
`d_L(T)=C(T)/(C'(0)T)`, `d_L(0)=1`, while **every coefficient** of
`d_L(t+2Lz)` has valuation at least `a+1-v_2(t)` at nonzero grid nodes,
with equality in the linear coefficient. Powers multiply that exact content.
These polynomials occur as deformed contractions of degree-one unary tensor
networks. Fixed packet size therefore sometimes requires `Omega(M)` input
precision and jet order to recover even origin parity through this interface.

For the motivating `L=4,t=-2`, the value at the node is zero and the shifted
linear coefficient is `-20/3`. The odd denominator is valid in the two-adic
ring; every shifted coefficient is divisible by four. Origin parity remains
one. Supplying all of those jets modulo two cannot repair the shortcut.

## Reproduction and checked scope

Python 3.11+, standard library, from the repository root:

```sh
python3 -I -B research/parity-recovery-precision/verify.py
make verify
```

[verification.json](verification.json) records hashes and actual coverage:
56 exact shifted-content checks at all nonzero grid nodes for `L=2,4,8,16`;
224 exact power-content checks for powers one through four; 244 integer-value
and parity checks; and 210 explicit sums of the actual unary packet network
at rational points, including nonintegral odd-denominator coordinates.
The finite checker is a rational reference calculation, not the accepted
recursive contraction or an independent proof review. Default CI stays small.

## Limits and next attempt

The result concerns recovery from the stated local data. It is not a lower
bound against algorithms that inspect and simplify these easy unary inputs.
For growing `L` the network family's bound is only `M/L`; it does not show
optimality of the accepted `MD/u` precision scale. The next attempt is to
test that stronger scale for generic recovery polynomials, then identify
what tensor-specific restriction would avoid the witness. A new deformation,
different node set, or a correct direct parity identity would also change
the premise. Repeating the even-node congruence without such a change is
refuted. The accepted source and selected result remain unchanged.

## Pins, overlap and credit

Canonical base: `fd6df02023122badbdd888803146f0bd92002214`. Accepted OpenAI
source: `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`, frozen by
[SOURCES.json](../../SOURCES.json). Source labels and full cost implications
are adjacent to the argument in [PROOF.md](PROOF.md).

Live refresh before this checkpoint found [PR 1](https://github.com/1337isnot1337/3-SAT/pull/1)
(mode/taper functional obstructions), [PR 2](https://github.com/1337isnot1337/3-SAT/pull/2)
(weighted characteristic-two decision), [PR 3](https://github.com/1337isnot1337/3-SAT/pull/3)
(scalar sparse-query encoding), and [PR 4](https://github.com/1337isnot1337/3-SAT/pull/4)
(Newton modes). None is modified. The present witness addresses the parity
shortcut and local recovery-data precision. The initial observation that
the shortcut is refuted came from the supplied transcript; no claim to
discovering that initial refutation is made.

Contributor: Cinna Davis, with substantial OpenAI Codex assistance in the
proof, checker and writing. New material is Apache-2.0. No scientific
priority, human review, formal verification or selected-bound change is claimed.
