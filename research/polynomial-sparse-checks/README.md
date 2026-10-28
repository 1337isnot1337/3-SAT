# Polynomial construction of initial sparse checks

Status: author-checked scoped argument pending independent review. Base `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`. Coordination: [issue #70](https://github.com/1337isnot1337/3-SAT/issues/70). Contributor: Cinna Davis with substantial OpenAI Codex assistance.

[PROOF.md](PROOF.md) gives deterministic polynomial-time constructions of the Walsh shift family and the local check code in the accepted theorem's initial Tanner sparse-check matrix. It preserves the source parameters and output contract. The source uses exhaustive search costing exp(polylog n); the new construction is polynomial in n, m, and the numeric value of B. This is a preprocessing result, not a new SAT exponent or alpha. PR #51 separately reduces greedy candidate enumeration; neither result removes the main contraction cost.

Run `python3 -I -B research/polynomial-sparse-checks/verify.py` and `make verify`. The checker covers small independently enumerable potential and local-code cases and exhausts a scaled 16-edge Cayley-Tanner fixture before and after shortening. The fixture does not instantiate the source parameters; this is not an end-to-end source construction or an independent proof review.

Credit: accepted source commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`, `lem:sparse-checks`; conditional expectations, finite-field parity checks and the Vandermonde determinant are standard. No novelty or priority claim is made for these methods. Remaining work: independently review the bit cost, source-parameter inequalities and all-size argument; see whether an actual dominant contraction or outer cost can be improved.
