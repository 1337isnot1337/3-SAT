# Scalar parity lift for sparse polynomial queries

Status: `scoped_checked`. AI-assisted; no independent review. The selected
bound is unchanged.

Task: `dense-encoding`. Base commit: `fd6df02023122badbdd888803146f0bd92002214`.

Contributor: OpenAI Codex (AI-assisted). Disclose substantial AI assistance.

## Result

The [proof](PROOF.md) replaces the sparse-query encoding's total-order
h-lift by the exact integer parity projector
`(1 + (-1)^b product_j (1-2 z^A_j))/2`. Its coefficient divisibility
gives retained degree `k(a+p-1)` modulo `2^p`, rather than the source's
`k(a+2(p-1))` at its matching precision and truncation order. All products
are multilinearized in the separate test-variable incidences.

For a branch with f free variables, use p=f+1 and recover its exact
count. At the source's precision p=n+1, the degree envelope decreases
from `k(a+2n)` to `k(a+n)`, before capping either by N, the incidence
count. Scalar coefficients in `Z/2^p Z` replace the `n+1` coordinates
in the source's truncated V-algebra. Integer division occurs before
reduction; no inverse of two is used.

This is a constructive component improvement for deterministic exact
counting. It is not an improvement of the selected full time envelope,
does not remove log log n, and does not increase alpha. The new cutoff
is sharp for this encoding. A separate family has
`2^Theta(n log log n)` retained nonzero coefficients even after the
source's high-incidence preprocessing; coefficientwise support indexing
alone therefore cannot remove that wire entropy.

The precise question was whether a different local parity lift could
reduce degree and coefficient representation without increasing entry
cost. That succeeds. The stopping condition was unchanged dominant
asymptotic cost; it is reached. A further round needs a changed mechanism,
not another constant-only cutoff optimization.

## Complete cost

Sections 3-4 of the proof supply the grouped networks, invalid codes,
entry procedures, finite fallback, precision recovery, branches, arrays,
all greedy query candidates and outer sparsification costs. The accepted
contraction theorem is used unchanged with ell=1; its modes, recursion,
interpolation and precision costs are included by that theorem.

The complete deterministic general-density bound remains
`(n+m)^O_k(1) 2^O_k(n log log n / sqrt(log n))`, with polynomial space.
The unchanged clause network retains the accepted fixed-density bound.
The [cost model](model.json) preserves alpha `1/2` and the iterated
logarithm. Its symbolic comparison is bookkeeping, not a proof of the
new lift. The proof is the separate algebraic argument.

## Evidence and reproduction

Run from the repository root, using Python 3 and its standard library:

```sh
python3 -I -B research/scalar-parity-lift/verify.py
python3 -B -m satbounds.cost research/scalar-parity-lift/model.json
make verify
```

The bounded [checker](verify.py) reproduces [verification.json](verification.json).
It verifies 33,046 normalized local polynomials with 526,410 independent
union-product/Mobius coefficient comparisons, the same number of
divisibility and Boolean-evaluation checks, 16,660 ordered systems at
66,340 precisions, and 32,440 discarded nonzero integer coefficients.
Its 47 explicitly contracted grouped networks exhaust 47,779 wire
assignments, including 8,704 invalid codes. It also checks combinatorial
unranking, branch-specific precision and unused variables, exact sharp
cutoff witnesses, finite support-family witnesses, and exact rational
controls rejecting the even-node congruence supplied by the user.

The [reference routines](scalar_lift.py) enumerate small cases; they do
not implement the accepted subexponential contraction algorithm. No
native speed measurement or end-to-end fast SAT solver is claimed.
`make verify` passes all 17 repository tests and source/metadata checks.
A Git-free export reproduced the checker output byte for byte; see
[VALIDATION.md](VALIDATION.md) for its exact source checkpoint and scope.

## Limits and open next questions

The written all-size component proof awaits independent review. No human
or Lean review is claimed. The smaller stars-and-bars bit ceilings in
the saved evidence are encoding envelopes, not measured contractions or
proved time-constant ratios. [HANDOFF.md](HANDOFF.md) names the remaining
questions and the changed premise needed for another round.

The user also supplied Anthropic's paper during this run. Its
[pinned comparison](EXTERNAL-COMPARISON.md) records a different
operator/partition construction, the same stated alpha, and the precise
piece-improvement condition worth investigating. It is not a proof
dependency, and the Lean development has not been built here.

## Sources and credit

OpenAI, *The Exponential Time Hypothesis is False*, revised October 25,
2026, source commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`.
The changed source is
[quantitative-reduction.tex](../../upstream/openai-eth-2026/build/quantitative-reduction.tex),
labels `lem:tensor-sparse-query`, `eq:sharp-incidence-degree`,
`eq:sharp-wire-budget`, and `thm:tensor-contraction`.
Its SHA-256 is `0b2b136c4f37ee0583dda40ee0c0d692f4751537d3d18539a389cd467ea8359a`.
The parity-projector identity is elementary; no scientific-priority
claim is made. Original material is Apache-2.0 and AI-assisted.

Adjacent work was checked in open PRs 1-4. PR 2's weighted
characteristic-two fingerprint preserves decision; this component
preserves deterministic exact counts. Neither PR is a proof dependency.
The concurrent [PR 3](https://github.com/1337isnot1337/3-SAT/pull/3)
explicitly credits this branch's first checkpoint `ca0a7f5` and develops
the same scalar cutoff, full composition and support-entropy obstruction.
Those core conclusions overlap; this package does not claim exclusive
priority. Its checker, exact control for the user's refuted shortcut and
new external-paper comparison are separately supplied here.
