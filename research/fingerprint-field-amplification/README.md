# Small-field decision fingerprints and amplification

Status: `scoped_checked`; written argument author-checked, not independently
reviewed. This component changes the characteristic-two fingerprint sampling
in the existing decision wrapper. It claims no improved 3-SAT exponent, alpha,
or selected result. Contributor: 1337isnot1337 with substantial OpenAI Codex
assistance. Base `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`.

For any nonempty Boolean solution set in N variables, independent uniform
weights in a q-element characteristic-two field give a nonzero fingerprint
with probability at least `(1-1/q)^N`. This is tight for a full Boolean cube.
A disjoint equality-constraint family, in which every variable occurs in two
clauses, has exact success `(1-(q-1)/q^2)^(N/2)`. Thus independent sampling
requires `exp(Theta(N/q))` repetitions in the worst case at this interface.
The equality family is efficiently simplified; this is no SAT lower bound.

Charging the repetitions in the existing randomized sparse-hash wrapper
permits `q=Theta(sqrt(log n)/log log n)` (rounded to a power of two) without
worsening its accepted general-density exponent. The predecessor used `q>=6N`
for constant success per evaluation. This is a field-size tradeoff, not an
asymptotic time improvement. [PROOF.md](PROOF.md) gives exact assumptions,
probability, full cost ledger, and limitations. Investigating a correlated or
input-aware evaluation strategy is a changed premise, not a consequence.

Reproduce with Python 3.11+ and no extra dependencies:

```sh
python3 -I -B research/fingerprint-field-amplification/verify.py
make verify
```

[verification.json](verification.json) records bounded exhaustive counts.
These checks do not establish the all-size argument or implement contraction.
The source is OpenAI's frozen commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`,
`thm:tensor-contraction`, `lem:tensor-sparse-query`, `lem:sparse-checks`, and
`lem:sparsify`; see [SOURCES.json](../../SOURCES.json). Credit for the
fingerprint, finite-field embedding and randomized wrapper belongs to the
[characteristic-two decision package](../characteristic-two-decision/README.md).
No novelty or literature priority is claimed. Apache-2.0.
