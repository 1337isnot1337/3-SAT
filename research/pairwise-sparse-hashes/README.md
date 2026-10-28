# Pairwise-independent indices for randomized sparse hashes

Status: `scoped_checked` for the named finite checks; the all-size proof is
author-checked and not independently reviewed. Contributor: 1337isnot1337
with substantial OpenAI Codex assistance. Base
`630041c9da3a26edb8c8f59d5f8a4132a188c8bd`. No improved time exponent or
alpha is claimed.

The predecessor randomized decision wrapper uses `2P` independently sampled
indices and `2P` independent coefficient bits for each extra sparse check.
This package generates the indices as `A*a_i+B` over the padded index field,
using two independent field elements, while retaining independent coefficient
bits. A second-moment argument preserves at least `1/4` rejection probability
for every violation vector satisfying the predecessor's support promise.
An explicit whole-universe fallback handles `2P` larger than the padded
universe. The row still has at most `2P` nonzero coordinates and the same
number of rows and tensor work are charged. Random bits per row fall from
`2P(log2 q+1)` to at most `2 log2 q+2P` for padded size q, with a smaller
fallback budget. [PROOF.md](PROOF.md) gives the conditions, complete wrapper
cost, and limitations.

Reproduce using Python 3.11+ and the standard library:

```sh
python3 -I -B research/pairwise-sparse-hashes/verify.py
make verify
```

The [saved finite output](verification.json) checks all qualifying small
supports, affine index seeds and coefficient patterns in the stated range.
It does not implement the accepted contraction or verify the all-size proof.
The immediate predecessor is
[characteristic-two decision](../characteristic-two-decision/README.md),
especially its random sparse-hash wrapper. The accepted upstream source is
OpenAI commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`, labels
`lem:sparse-checks`, `lem:sparsify`, `lem:tensor-sparse-query` and
`thm:tensor-contraction`; attribution and hashes are in
[SOURCES.json](../../SOURCES.json). No literature priority is claimed.
Apache-2.0.
