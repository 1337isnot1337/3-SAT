# Odd-node modes at the formal support scale

Status: `scoped_checked`. The all-size proof is author-checked and awaits
independent review. No SAT improvement or general algorithmic lower bound
is claimed.

Task: `weighted-modes`; base `1dfac844cbb1e570c99579ecf48c1007d72da7c9`.
Contributor: Cinna Davis, with substantial OpenAI Codex assistance.

The [proof](PROOF.md) constructs a bounded-degree weighted tensor network
and a specified valid, exactly balanced root packing. For the odd-node
Newton expansion at `t=1`, with `zeta=1` included in the evaluation set,
at least `exp(Omega(M/sqrt(u)))` distinct complete child-product summands
are inside the source's weighted budget and nonzero modulo its prescribed
precision. This matches the order of the formal enumeration envelope for
this specific representation and call.

The selected row tensor is unary `(1,2)`, so this is a **general tensor
input**, not a claim about the literal SAT reduction's clause/equality
tables. The network is disconnected and easily simplified; the source's
default labeling need not select this packing, and nonzero summands can
cancel or be aggregated. The result does not establish a SAT lower bound,
an algorithmic time lower bound, or a speedup.

The argument normalizes the odd-node row coefficients by their source
weights. Their binary matrix is a permuted Pascal matrix, hence invertible.
In the Boolean quotient the product of row factors is the delta function
at zero. Therefore every subset of modes has at least one *original*
exponent tuple with an odd normalized coefficient. The proof carefully
allows higher powers to fold in the quotient; it does not assume the
original squarefree coefficients are all odd. Pinned source mode values
are units and the actual taper leaves room for these terms.

Reproduce using Python 3.11+ and the standard library:

```sh
python3 -I -B research/odd-node-mode-support/verify.py
make verify
```

[verification.json](verification.json) binds the proof and checker to the
frozen source and PR #4's mode proof. Exact `(L,b)=(16,2),(32,4),(64,8)`
checks verify the residue permutation, binary matrix rank, original
exponent-tuple witnesses for all supports, source units, full kernel
identities and local contractions. For `b<=4` selected coefficients are
also independently recomputed as exact rationals. These finite checks do
not review the all-size proof or implement the full recursion.

Issue [#22](https://github.com/1337isnot1337/3-SAT/issues/22) coordinates
this lane. The accepted theorem, selected result and frozen upstream are
unchanged. PR #4 supplies the odd-node basis; earlier general-mode support
work is credited in the proof. New work is Apache-2.0 and substantially
Codex-assisted.
