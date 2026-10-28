# Expander-walk candidates for greedy sparse checks

Status: author-checked scoped argument, pending independent review. Base `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`. Issue [#40](https://github.com/1337isnot1337/3-SAT/issues/40). Task: dense-encoding. Contributor: Cinna Davis, with substantial OpenAI Codex assistance.

The credited [near-one equation construction](NEAR-ONE.md) uses a modest polylogarithmic increase in row width to achieve n+o(n) total equations per query on the original-distance sparse leaves, while retaining polynomially many candidates. This changes no selected SAT exponent. A separately credited [composition of PR #64](HANDOFF-64.md) retains 3n greedy rounds and at most 6n equations using O(m²P²) candidates, at row length at most 2P. [PAIRWISE.md](PAIRWISE.md) independently gives a polynomial-size deterministic candidate family: affine pairwise-independent index sequences combined with polynomial-size coefficient strings yield fewer than 64 max(q,P)^2 P^2 candidates per round and 8n rounds. This replaces the source’s exp(polylog n) candidate multiplicity with polynomially many calls, while leaving the contraction cost and selected bound unchanged. [PROOF.md](PROOF.md) first replaces independent clause-index lists in the accepted theorem's greedy parity selection with walks on a deterministic constant-gap Walsh-Cayley graph. It gives q d^(P-1) 2^P candidates per round, q<2m and d=O(log(m+2)), versus (2m)^P; 14n rounds suffice, compared with the source's 3n. The bound holds for every large violation support and every candidate remains an admissible sparse query. A further [polynomial coefficient family](SMALL-BIAS.md) reduces the factor 2^P to h^2 <= 16P^2, with 28n rounds and at most 31n+1 equations per candidate. A theorem-dependent [constant-degree refinement](CONSTANT-DEGREE.md) further gives m 2^{O(P)} poly(P,n) calls; its external expander construction and spectral tester are not implemented here. This reduces the quasipolynomial overhead but does not improve the selected alpha or prove a new 3-SAT time bound. The proof relies on the owner-accepted upstream counting theorem, not a local implementation.

Reproduce the finite exact checks and repository verification:

```sh
python3 -I -B research/expander-walk-greedy/verify.py
python3 -I -B research/expander-walk-greedy/verify_bias.py
python3 -I -B research/expander-walk-greedy/verify_pairwise.py
python3 -I -B research/expander-walk-greedy/verify_handoff.py
python3 -I -B research/expander-walk-greedy/verify_near_one.py
python3 -I -B research/expander-walk-greedy/verify_ceiling.py
make verify
```

The verifier enumerates small supports and uses exact rational walk probabilities, also directly enumerating coefficient strings and repeated-vertex paths in a smaller domain. It is a finite check of the construction and parity identity, not a proof of the asymptotic argument. No human review or formal proof is claimed. See [PROOF.md](PROOF.md) for scope, assumptions, algorithm, and all costs.

Credit: OpenAI source commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`, `lem:sparse-checks`, `lem:greedy-hashes`, and `eq:hash-query`; source manifest [SOURCES.json](../../SOURCES.json). The graph uses the same Walsh shift construction, with a constant rather than density-dependent spectral target. Expander walks and averaging are standard; no priority or novelty claim for these techniques is made. Issue #53 uses related pairwise-independent indices in randomized hashes; this package enumerates the family for deterministic greedy counting. Issue #29 and #31 concern incidence indexing and row bases, not candidate enumeration. The source's local-code and greedy framework remain intact.

Open: Can a different contraction or preprocessing contract make the reduced oracle count affect a dominant term? Can the theorem-dependent constant-degree construction be made explicit and efficient with a concrete small-case threshold and independently replayed? Neither question is resolved here.
