# Shift-resistant tensor precision witness

Status: `scoped_checked` for the named finite checks; the all-size argument
is author-checked and has no independent review. No SAT improvement or new
alpha is claimed. Base: `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`.
Contributor: Cinna Davis with substantial OpenAI Codex assistance.

[PROOF.md](PROOF.md) constructs full packets of canonical Boolean unary
tensors for which every nonzero shifted node has its entire deformation
polynomial divisible by `2^ceil(M/4)`, while the original contraction is 1.
The zero network has identical local data at that precision and parity 0.
The shift-resistant binary word is constructed deterministically in
polynomial time by conditional expectation with path transfer matrices.

This strengthens the earlier actual-network witness for growing packets,
but it does not realize the generic tapered polynomial or match its
`MD_i/u` scale. Full packets and a specified embedding are essential scope
conditions; arbitrary packing and tensor-aware algorithms are not covered.
The predecessor and frozen source pins appear in the proof. The selected
result remains unchanged.

Reproduce with Python 3.11+ and the standard library:

```
python3 -I -B research/tensor-precision-realization/verify.py
make verify
```

The exact finite checker compares 63 path-transfer sums to brute force,
checks all mismatched row factors for its displayed words of lengths 2, 4,
8 and 16, and expands complete packet products at lengths 2, 4 and 8.
These finite checks do not prove the all-size construction. Next, investigate
whether useful shift-resistant words can be built on arbitrary partially
filled packets, and whether tensor-specific structure can reach the taper
scale at low-valuation nodes without increasing wire count.
