# Piece-dependent Pauli frames and the shared-dual boundary

Two specific quadratic-preserving Pauli label frames generate the full
contragredient `GL(3R,2)` action from their unfused F8 type symmetries.
Consequently any common dual that is type-constant in both frames has a
supporting type with entropy at most `log2(14)` per macro. It cannot
satisfy the `3 sqrt(2)` entropy floor used by the common-frame certificate
method. See [PROOF.md](PROOF.md) for the all-size group argument.

This is a limitation of a specific proof method and a possible changed
construction premise. It does not construct cheaper crossing pieces or
establish a SAT bound. The proof is author-checked with substantial OpenAI
Codex assistance and has no independent or formal review.

From the repository root, offline, with standard Python:

```sh
python3 -I -B research/piecewise-frame-symmetry/verify.py
make verify
```

The checker verifies 49 independent local rank-one maps, the commutator
identity and all generated orbits on 4,096 and 262,144 labels. Its
[output](verification.json) pins the source and checker; finite checks do
not substitute for the written all-size group proof. The predecessor's
F8 scheme, Pauli ranks and source attribution are credited in
[three-bit-macro-walsh](../three-bit-macro-walsh/README.md). The entropy
floor mechanism is developed in the pending branch
`research/unfused-f8-entropy` and coordinated in issue #27; this package
is independent of that unmerged source. Starting main was
`88b5f35432f8707a005c51d346e4c4c4cf6e416c`. New work is Apache-2.0.
