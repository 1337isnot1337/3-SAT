# A rank-only modular crossing interface

Status: `scoped_checked`. This removes an explicit integer-factor construction
requirement under the stated precision contract. It does not supply a
smaller crossing rank or an improved SAT exponent.

Task: `contraction-schedule`; base
`fdb2d6d5e585b75f12e79fd0f67934eed22af173`.
Contributor: Cinna Davis, with substantial OpenAI Codex assistance.
The accepted OpenAI theorem is a premise and remains selected unchanged.

## Result and changed mechanism

For an integer matrix A of rational rank r and any precision P, the
deterministic compiler constructs `A=UV modulo 2^P` with inner dimension
at most r and canonical P-bit factors. It handles zero divisors and uses
only polynomial time in the matrix dimensions and P. It does not compute
small exact integer factors. The underlying local-ring elimination is
standard; [PROOF.md](PROOF.md) gives the algorithm and its rank guarantee.

For lambda-bit crossing pieces this costs `2^O(lambda) poly(P)` time and
space. Thus rational ranks suffice in place of explicit integer factors
when the piece values and normalizer retain the stated uniformity/height
bounds. A known even normalizer consumes its two-adic valuation in extra
precision. A global polynomial precision cap, used consistently throughout
recursion, pays all such divisions and avoids promoting a low-precision
factor identity to higher precision.

The written transfer preserves the master time envelope under this modified
rank-only contract. It charges factor construction, entries, normalizers,
branches, queries, recursion and every intermediate output bound. It also
keeps the larger precision needed by rejected greedy query candidates in
the arbitrary-density reduction. The compiler uses exponential space in
lambda; preservation of polynomial space is NOT claimed. No randomness is
introduced. No complete new SAT implementation or independent review is
claimed by these bounded component checks.

## Verification

Standard-library Python, offline, from repository root:

```sh
python3 -I -B research/modular-rank-factorization/verify.py
python3 -I -B research/modular-rank-factorization/crossing.py
make verify
```

The first checker covers 5,000 two-by-two matrices, 3,072 binary
three-by-three matrices and 240 structured rectangular cases at varied
precisions; 19,968 exact-division and 6,528 nested-division cases; and 16
inverse-valuation controls. It checks reconstructed matrices, rational rank
bounds, canonical factor heights and sorted pivot valuations. Negative
controls reject binary rank as a substitute for modular inner rank, missing
division bits, promotion of creation identities, and free generic inverses.

The second checker compresses both 64-by-64 flattenings of each of the
predecessor's four actual crossing pieces, selects a cheaper orientation,
and recovers exact counts for all 256 Boolean predicates on three variables.
Its normalizer is 64: ten working bits recover four output bits. Saved
outputs are SHA-bound; these checks stay outside default CI.

## Limits and next question

Rational rank bounds for a new, cheaper family still need proof. Integer
piece values, uniform entry evaluation, polynomial piece count and a paid
normalizer remain necessary assumptions of this deterministic two-adic
transfer. Generic inverse normalization can require exponentially many
precision bits even for a matrix with tiny integer entries; the proof gives
an explicit bidiagonal example. Singular moment pairings remain singular.

A changed next premise is to evaluate uniform rational pieces over a large
odd prime and recover bounded **integer network query values** before the
outer modulo-two reduction. This might avoid the inverse-valuation barrier.
It must pay prime sampling, all bad denominators, every random outcome and
intermediate query bound; a final-count modulus alone is insufficient.
This is an open continuation, not a result of this package.

## Sources and credit

[SOURCES.json](SOURCES.json) pins Anthropic's `def:genpieces`,
`lem:grouping-explicit`, `thm:master` and `app:onelog`, with their external
evidence boundary. The proposed transfer changes that factor interface; it
does not treat Anthropic's full theorem as owner-selected. The actual test
crossing is the unmodified [three-bit predecessor](../three-bit-macro-walsh/README.md),
which inherits the Pauli/Bell construction and adapted basis from PR 14.
The [operator rank package](../anthropic-operator-ranks/README.md) and open
PR 11 charged moments motivate the distinction between rank, factors and
normalization. They are credited, not replaced or claimed as this result.

Smith and modular linear algebra are established methods; the author-hosted
Storjohann--Mulders ESA 1998 paper is pinned as background. No novelty is
claimed for those methods. All new text/code is Apache-2.0 and substantially
AI-assisted. The all-size transfer awaits independent review.
