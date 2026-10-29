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
A separate virtual-period construction strengthens this: for every
nonzero node, jets through degree `(1/4-o(1))M` vanish exactly and the
entire shifted polynomial has at least that many bits of content, under
the stated source active-parameter condition.

A second construction uses periodic words to make every retained active
node vanish modulo `2^((floor(M/8)+1)*(a+2-u))` under the source packing
conditions. This is a separate input family from the all-nonzero-node
witness and gives `Omega(M(a-u))` precision when `a-u` grows. Its shifted
coefficients through degree `floor(M/8)` also vanish exactly, so those jets
do not suffice even at infinite precision. Under source active parameters,
a refined construction selects `(1/4-o(1))M` rows simultaneously; that
fraction is asymptotically sharp for the selected-row mechanism on full
packets. An explicit cycle of binary linear-character words attains its
exact averaging upper bound when the number of full packets is divisible
by `P-1`. Full
packets admit an additional `a-u+1` bits per selected row when `a>u`
through a Cauchy power-sum cancellation; this uniform row bound is sharp.
A three-slot partial packet gives a counterexample to carrying that bound over unchanged. For partial packets,
complete dyadic blocks retain a quantitative version in terms of the number
of occupied slots belonging to such blocks; the source packing alone does
not guarantee that number is large.

This strengthens the earlier actual-network witness for growing packets,
but it does not realize the generic tapered polynomial or match its
`MD_i/u` scale. The partial-packet argument requires the source packet-count
bound and entries chosen after the graph-only packing. Tensor-aware
algorithms are not covered. The predecessor, concurrent PRs #52 and #65,
and frozen source pins appear in the proof. The selected result remains
unchanged.

Reproduce with Python 3.11+ and the standard library:

```
python3 -I -B research/tensor-precision-realization/verify.py
python3 -I -B research/tensor-precision-realization/verify_partial.py
python3 -I -B research/tensor-precision-realization/verify_periodic.py
python3 -I -B research/tensor-precision-realization/verify_blocks.py
python3 -I -B research/tensor-precision-realization/verify_all_nodes.py
make verify
```

The exact finite checker compares 63 path-transfer sums to brute force,
checks all mismatched row factors for its displayed words of lengths 2, 4,
8 and 16, and expands complete packet products at lengths 2, 4 and 8.
The partial-packet checker exhausts all nonempty occupancy subsets at
lengths 2 and 4, with 114 path-transfer and 114 complete-product checks.
The periodic checker compares 66 cycle transfers with brute force and checks
672 packet products, 924 selected row factors and the partial-packet
counterexample. The block checker tests 1,432 selected rows across four
occupancy patterns. The virtual-period checker covers 440 selected rows
and 174 complete packet products. These finite checks do not prove the all-size
constructions. Next, investigate whether tensor-specific structure can reach the taper scale at low-valuation
nodes without increasing wire count.
