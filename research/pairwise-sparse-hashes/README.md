# Pairwise-independent indices for randomized sparse hashes

Status: `scoped_checked` for the named finite checks; the all-size proof is
author-checked and not independently reviewed. Contributor: 1337isnot1337
with substantial OpenAI Codex assistance. Base
`630041c9da3a26edb8c8f59d5f8a4132a188c8bd`. No improved time exponent or
alpha is claimed.

The predecessor randomized decision wrapper uses `2P` independently sampled
indices and `2P` independent coefficient bits for each extra sparse check.
Generate indices as `A*a_i+B` over the padded index field, using two uniform
field elements. Generate coefficients with a separate logarithmic-size seed
using traces of powers over an auxiliary field. A second-moment bound and a
polynomial-root bound give at least `15/64` rejection probability for every
violation vector satisfying the predecessor's support promise. An explicit
whole-universe fallback handles `2P` larger than the padded universe. The
original row count, width and tensor work still suffice. Random bits per row
fall from `2P(log2 q+1)` to `O(log(q+1)+log(P+1))`, where q is the padded
universe size. A matching order-of-magnitude lower bound on row width holds
when the guarantee must cover *all* supports meeting the size promise; it does
not restrict formula-aware methods. [PROOF.md](PROOF.md) gives exact constants,
complete wrapper cost, and limitations.

Reproduce using Python 3.11+ and the standard library:

```sh
python3 -I -B research/pairwise-sparse-hashes/verify.py
make verify
```

The [saved finite output](verification.json) checks all qualifying small
supports, affine index seeds and trace-coefficient patterns in the stated range.
It does not implement the accepted contraction or verify the all-size proof.
The immediate predecessor is
[characteristic-two decision](../characteristic-two-decision/README.md),
especially its random sparse-hash wrapper. The accepted upstream source is
OpenAI commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`, labels
`lem:sparse-checks`, `lem:sparsify`, `lem:tensor-sparse-query` and
`thm:tensor-contraction`; attribution and hashes are in
[SOURCES.json](../../SOURCES.json). No literature priority is claimed.
Apache-2.0.
