# Exact hash syndrome chains and sparse row networks

Status: `scoped_checked` for finite controls; the all-size argument is
author-checked and awaits independent review. No SAT speedup is claimed.
Task `decision-only`; base `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`.
Contributor: Cinna Davis, with substantial OpenAI Codex assistance. Apache-2.0.

For a binary check matrix A, [PROOF.md](PROOF.md) proves the Boolean predicate
`1[Az=0]` has exact cut rank `2^b` over every field, with b the intersection
dimension of the prefix and suffix column spans. An ordered chain tracking
just the running syndrome in this intersection uses exactly b Boolean bits
at the cut and is optimal among exact chains with that ordered separation.
It computes the **summed Boolean hash predicate**, not the independent-set
coefficient table from PR #37; it does not claim the same formula for
arbitrary field values substituted for z.

The proof also supplies a different sparse-row tensor network with bounded
degree equality trees. After linking Boolean clause violations and weights,
it computes the hashed weighted fingerprint with `O(n+km+a+h)` wires,
where h is the number of ones of the a-by-m check matrix. For the source
checks and decision wrapper, `h<=3n D_0+2Pt`, giving `n polylog(n)` size
in the stated regime. This does not establish an improvement over the
accepted arbitrary-density bound. An ordered chain may need quadratically
many wires in a conditional linear-nullity regime; the nonlocal sparse-row
network is not subject to that chain bound.

## Reproduction

```sh
python3 -I -B research/hash-syndrome-chain/verify.py
make verify
```

The checker covers all 4,096 binary 3-by-4 matrices, 65,536 syndrome inputs,
and 20,480 cut tables over each of F2 and F3. It also compares 1,000 seeded
GF(8) weighted clause fixtures with their syndrome-chain evaluation. The
[hash-bound output](verification.json) records counts and seed. The tests
are finite controls; no accepted contraction solver is implemented.

## Scope and credit

The source sparse-check lemma and decision wrapper are credited to the
frozen OpenAI source and PR #2; source pins are in
[SOURCES.json](../../SOURCES.json). PR #37 records the independent-set
frontier and PR #55 its all-cut width bound; PR #74 proves an independence
cut-rank lower bound. This package treats the simpler summed Boolean kernel
function and different row-network topology. Standard syndrome trellises,
parity factors, equality trees and matrix rank are used; no priority claim is
made. Before an algorithmic improvement one must satisfy the full ring,
degree, precision, recursion, recovery, all-leaf and randomness contracts.
The accepted theorem and selected result remain unchanged.
