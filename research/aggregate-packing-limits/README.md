# Aggregate packing limits

Task: `dense-encoding`. Status: `scoped_checked` for the named finite checks;
the written all-size argument is author-checked and not independently reviewed.
No improved asymptotic SAT bound or selected result is claimed.

Contributor: 1337isnot1337, with substantial AI assistance from Kimi. New
material is Apache-2.0. The OpenAI theorem is accepted as true.

## Question and changed premise

Can aggregated one-monomial-per-code incidence tensors reduce the sparse-query
wire order while still using the accepted balanced-packing recursion and
direct-sum leaves? The changed premise is that a root encoding with fewer
wires might remain usable even when its aggregate vertices violate the source's
`s^(9/10)` maximum-degree hypothesis.

The success condition was a degree-admissible recursive representation with
`o(n log log n)` wires and all entry and leaf costs paid. The stopping condition
was a quantitative obstruction specific to that representation. This round
reaches the stopping condition.

## Result and scope

The [proof](PROOF.md) shows two things:

- Balanced real-port packing necessarily requires maximum degree at most
  `3M/r`, independently of the sufficient variance estimate used in the source.
  Unsplit old vertices retain their degree in every child, so this condition
  persists through recursion.
- In the stated aggregate model with `J` blocks, nominal wires
  `M=Theta(n log J)`, and `R=ceil(n^(1/4))` degree buckets, some aggregate
  vertex has degree lower bound `Omega(n log J/J)`. Consequently
  `M=o(n log log n)` forces this obstruction to be asymptotically larger than the
  accepted leaf-scale exponent. Keeping it within that scale requires
  `J=Omega(sqrt(log n))`, which retains the `Theta(n log log n)` wire order.

This is a representation-specific tradeoff, not a SAT hardness result, a lower
bound on every tensor network, or a review of the accepted theorem. The
particular disjoint-linear witness is easy by other methods.

## Complete cost and next question

No new algorithm or running time is claimed. The accepted general envelope
remains `poly(n+m) 2^O_k(n log log n/sqrt(log n))`, with `alpha=1/2`; the
fixed-density bound is unchanged. There are no new queries, branches,
precision levels, modes, random bits, or amplification costs.

Reopening the route requires a degree-bounded tensor decomposition preserving
the aggregate saving, an unbalanced recursion with a complete non-geometric
cost proof, or a faster leaf algorithm for persistent high-degree tensors.
Root-only packing work is insufficient.

## Evidence and reproduction

From the repository root with Python 3.11+ and only the standard library:

```sh
python3 -I -B research/aggregate-packing-limits/verify.py
make verify
```

The scoped checker covers 5,367 exact small support/degree-array evaluations
in 45 families, star-packing controls, and 15 numerical fixtures for the
written asymptotic formulas. Its [saved output](verification.json) records
`pass` and the proof/checker hashes. Finite checks do not independently prove
the all-size argument, and no human review, formal proof, independent replay,
or priority claim is made.

## Sources, pins, and credit

- Canonical main at branch creation:
  `fdb2d6d5e585b75f12e79fd0f67934eed22af173`.
- Accepted OpenAI source:
  `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`; labels
  `thm:tensor-contraction`, `lem:tensor-packets`,
  `eq:tensor-recursion-identity`, `subsec:tensor-cost`, and
  `eq:sharp-wire-budget` in the frozen sources.
- Immediate predecessor: the characteristic-two decision follow-up at branch
  `research/dense-decision-compression`, commit
  `3a42c2648eee5df19954d887a33e9e018adc5ccf`, especially its aggregate degree
  counterexample. This package independently states the support calculation
  and adds the balanced-packing persistence and exact wire/leaf tradeoff.
- Related merged support barrier:
  [Scalar parity compression](../newton-parity-compression/README.md). That
  package rules out zero-pruning in the scalar one-monomial architecture; this
  package addresses aggregated codes and recursion, not the same claim.
- Live overlap at selection: open PRs #11 and #12 concern charged operator
  moments and documentation, respectively. No open Issues were present.
