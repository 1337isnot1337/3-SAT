# Shift-resistant tensor precision witness

Status: `scoped_checked` for the named finite checks; the all-size argument
is author-checked and has no independent review. No SAT improvement or new
alpha is claimed. Base: `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`.
Contributor: Cinna Davis with substantial OpenAI Codex assistance.

[PROOF.md](PROOF.md) constructs full packets of canonical Boolean unary
tensors for which every nonzero shifted node has its entire deformation
polynomial divisible by `2^ceil(M/4)`, while the original contraction is 1.
The zero network has identical local data at that precision and parity 0.
For arbitrary partially occupied packets in the source graph-only packing,
the same method gives precision `ceil(M/8)` at every nonzero node once
`L >= 6*128*ceil(log2(2L))`. The words are constructed deterministically
in polynomial time by conditional expectation with path transfer matrices.

This strengthens the earlier actual-network witness for growing packets,
but it does not realize the generic tapered polynomial or match its
`MD_i/u` scale. The partial-packet argument requires the source packet-count bound and
entries chosen after the graph-only packing. Tensor-aware algorithms are
not covered.
The predecessor and frozen source pins appear in the proof. The selected
result remains unchanged.

Reproduce with Python 3.11+ and the standard library:

```
python3 -I -B research/tensor-precision-realization/verify.py
python3 -I -B research/tensor-precision-realization/verify_partial.py
make verify
```

The exact finite checker compares 63 path-transfer sums to brute force,
checks all mismatched row factors for its displayed words of lengths 2, 4,
8 and 16, and expands complete packet products at lengths 2, 4 and 8.
The partial-packet checker exhausts all nonempty occupancy subsets at
lengths 2 and 4, with 114 path-transfer and 114 complete-product checks.
These finite checks do not prove the all-size construction. Next, investigate
whether tensor-specific structure can reach the taper scale at low-valuation
nodes without increasing wire count.
