# Residue-class packet precision witness

Status: `scoped_checked`, author-checked with substantial OpenAI Codex
assistance; no independent review. This proves an all-size lower bound on
precision and jet order for the retained-node interpolation-data interface,
using canonical Boolean unary tensors and any graph-only packet assignment.
It does not prove a SAT lower bound or an improved alpha.

For `M` matched real edges in packets of `L=2^a` slots and `1 <= u <= a`,
choose a most populated occupied slot class modulo `2^u` in each packet. If
`K` slots are selected in total, `K >= ceil(M/2^u)`. A degree-one Boolean
network with original contraction one has full shifted data divisible by
`2^{K(a+1-i)}` at every retained node of valuation `i<u`; its jets below
degree `K` vanish even at infinite precision. The zero network gives the
same data with opposite origin parity. See [PROOF.md](PROOF.md) for the
precise quantifiers, construction, comparison and limitations.

For a full packet this uses `L/2^u` selected rows, improving the predecessor's
one-row-per-packet bound by that factor. The result works for arbitrary
partially occupied packets. It does not match the generic-polynomial
`MD_i/u` precision scale in general, realize its polynomial, or constrain a
solver which exploits the easy unary input directly.

## Reproduction

Python 3.11+, standard library only, from the repository root:

```sh
python3 -I -B research/packet-residue-recovery/verify.py
make verify
```

The exact rational reference checker covers all 798 nonempty occupancy and
`u` cases for `L=2,4,8`; 14,130 row-node jets; 522 packet-node products;
six independently shifted full packet polynomials; and three direct network
sums. It checks finite examples, not the all-size proof. The full-packet
product checks are exponential reference calculations, not a fast algorithm.

## Sources and concurrent work

Canonical base `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`; accepted
OpenAI source `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`, pinned in
[SOURCES.json](../../SOURCES.json). The direct predecessor is
[parity-recovery-precision](../parity-recovery-precision/PROOF.md), especially
Sections 3--5. This work is tracked in [issue #35](https://github.com/1337isnot1337/3-SAT/issues/35).

Concurrent [PR #56](https://github.com/1337isnot1337/3-SAT/pull/56), head
`6e282300d9d39442257927a415362c4c5ed0914a`, constructs a shift-resistant
Boolean word giving `Omega(M)` simultaneous precision for *all nonzero*
nodes on full packets. Its stated scope does not include arbitrary partial
packets. Our construction applies to arbitrary occupancy and gives a
valuation-dependent bound on retained levels only; neither is presented as
superseding the other. [PR #52](https://github.com/1337isnot1337/3-SAT/pull/52),
head `5ad154243e1f08e501197c9f7236da50d1a368e3`, realizes the `u=1`
generic polynomial over the 2-adic coefficient ring with prescribed full
packets, not with canonical Boolean unary tensors. No priority claim is made.

Contributor: Cinna Davis, with substantial OpenAI Codex assistance. New
material is Apache-2.0. The selected result and upstream bytes are unchanged.
