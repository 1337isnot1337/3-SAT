# Scalar parity lift for sparse polynomial queries

Status: draft. No result claimed.

Task: `dense-encoding`. Base commit: `fd6df02023122badbdd888803146f0bd92002214`.

Contributor: OpenAI Codex (AI-assisted). Disclose substantial AI assistance.

## Question and changed mechanism

Can the sparse-query encoding retain fewer incidence monomials and use a
scalar coefficient ring? The [proof](PROOF.md) replaces the source's
total-order h-lift by the exact integer parity projector
`(1 + (-1)^b product_j (1-2 z^A_j))/2`. Its coefficient divisibility
gives retained degree `k(a+p-1)` modulo `2^p`, rather than the source's
`k(a+2(p-1))` at its matching precision and truncation order.

## Statement and scope

The local identities and the smaller coefficientwise degree bound are
proved in the draft. Full composition and finite checks are in progress.
Success means a complete replacement encoding with valid entries and
costs. Stop if it only improves the degree constant; state that limit
explicitly rather than claiming a new alpha or an iterated-log saving.

## Complete cost

Pending: compose the scalar construction with the unchanged accepted
contraction theorem, incidence grouping, high-incidence branching and
the arbitrary-density reduction. The expected full asymptotic envelope
is unchanged. No selected-bound improvement is claimed.

## Evidence and reproduction

The [reference routines](scalar_lift.py) include two different coefficient
calculations, a finite incidence sum, and explicit grouped network
enumeration. These are small-input oracles, not the accepted fast
contraction algorithm. A reproducible checker will follow.

## Limits and open next questions

Finish the grouped-network proof and verify invalid codes, constants,
unused variables, degree truncation, and the sharpness of the cutoff.

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
