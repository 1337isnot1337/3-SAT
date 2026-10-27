# Characteristic-two decision interface

Status: `scoped_checked` for the named finite identities; written arguments are
author-checked and not independently reviewed. **No larger alpha or improved
general-case exponent is claimed.** This is an active component checkpoint.

Task: `decision-only`. Base `fd6df02023122badbdd888803146f0bd92002214`.
Contributor: 1337isnot1337, with substantial OpenAI Codex assistance. Apache-2.0.
The OpenAI theorem is accepted as true.

The changed interface is decision by a weighted characteristic-two partition
function. A nonempty Boolean solution set has a nonzero multilinear generating
polynomial even if its unweighted cardinality is even. Random field values
detect it. This lets a degree-k parity equation use the factor `1+P_i` directly:
the incidence degree is `ka`, instead of the exact-counting lift's
`k(a+2n)`. Its tensor coefficients are direct lookups, not exponential subset
inversions. The [proof](PROOF.md) gives a strict embedding into the accepted
contraction theorem's coefficient ring, and a constraint-parameter version of
the evaluator. It also replaces greedy exact-count queries by random sparse
hash rows with a paid error bound and a fixed random-bit budget per draw.

The success target is a complete better all-input time bound. This checkpoint
does not reach it: for `a=Theta(n)` and polylogarithmic row sparsity, the wire
budget remains `Theta(n log log n)` in the available upper envelope. The full
wrapper therefore retains the accepted alpha `1/2` and iterated-log factor.
Removing a lower-order query overhead is not a new asymptotic exponent.

Reproduce the bounded algebra check with standard-library Python 3.11+:

```sh
python3 -I -B research/characteristic-two-decision/verify.py
make verify
```

[Saved output](verification.json): all 256 ordered pairs of Boolean polynomials
on two variables; all 64 GF(8) weight points per pair; 16,384 evaluations; exact
agreement of truth-table, incidence and unreduced-polynomial-ring calculations.
All 81 unsatisfiable systems have zero fingerprints everywhere. Every nonempty
solution set has at most 15 zero fingerprints among 64 points, below the proved
bound 16. An even-cardinality failure control rejects plain unweighted parity.
These checks do not implement the accepted contraction or verify the all-size
proof. The checker takes under a second on the authoring machine.

Source: OpenAI commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`,
[quantitative reduction](../../upstream/openai-eth-2026/build/quantitative-reduction.tex),
labels `thm:tensor-contraction`, `lem:tensor-sparse-query`,
`eq:sharp-incidence-degree`, `eq:sharp-wire-budget`; and
[main source](../../upstream/openai-eth-2026/build/main_full_version.tex),
labels `lem:sparse-checks`, `lem:greedy-hashes`, `lem:sparsify`.
Hashes and licenses are in [SOURCES.json](../../SOURCES.json).

PR #1's mode/taper obstructions are predecessor context, not a mathematical
dependency. At this checkpoint canonical main contains no selected improvement;
the only open PR at the initial overlap check was #1. No priority claim is made.

The next experiment is aggregating equations before indexing monomials. It must
pay both aggregate coefficient evaluation and maximum tensor degree; a smaller
formal wire count alone is insufficient. A failed mechanism will be recorded
with its precise reopening condition before a pivot.
