# Odd-node modes at the formal support scale

Status: `scoped_checked`. The all-size proof is author-checked and awaits
independent review. No SAT improvement or general algorithmic lower bound
is claimed.

Task: `weighted-modes`; base `1dfac844cbb1e570c99579ecf48c1007d72da7c9`.
Contributor: Cinna Davis, with substantial OpenAI Codex assistance.

The [proof](PROOF.md) constructs fixed-density unit-clause CNF inputs
whose subdivided tensor networks admit specified, exactly balanced root
packings. For the odd-node
Newton expansion at `t=1`, with `zeta=1` included in the evaluation set,
at least `exp(Omega(M/sqrt(u)))` distinct complete child-product summands
are inside the source's weighted budget and nonzero modulo its prescribed
precision. This matches the order of the formal enumeration envelope for
this specific representation and call.

The proof gives fixed-density unit-CNF constructions using the source's
literal per-edge subdivision. One has repeated identical clauses; a second
has no duplicates but contains opposing unit clauses and is immediately
unsatisfiable. Four packets per gadget and an even-row pinning lemma preserve
the support scale. Both inputs are easily simplified. The source's
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
are units and the actual taper leaves room for these terms. For the Boolean
clause construction, an auxiliary packet has a local Cauchy block equal to
the identity modulo two, so summing its bits recovers the same normalized
coefficient parity.

Reproduce using Python 3.11+ and the standard library:

```sh
python3 -I -B research/odd-node-mode-support/verify.py
python3 -I -B research/odd-node-mode-support/filler-moments.py
python3 -I -B research/odd-node-mode-support/reduction-gadget.py
python3 -I -B research/odd-node-mode-support/mixed-pin-screen.py
make verify
```

[verification.json](verification.json) binds the proof and checker to the
frozen source and PR #4's mode proof. Exact `(L,b)=(16,2),(32,4),(64,8)`
checks verify the residue permutation, binary matrix rank, original
exponent-tuple witnesses for all supports, source units, full kernel
identities and local contractions. They also check the auxiliary Cauchy
block modulo two and toy packet-pair labels. For `b<=4`, weighted-unary and
Boolean-clause selected coefficients are recomputed as exact rationals, and
a conditional local subdivision/pin gate is checked for every external bit
vector. A separate all-size filler lemma proves that a paired unit-clause
and free-variable subdivision packet contributes exactly three powers of
two; its modulo-16 expansion is checked through `L=64`. An all-size moment
lemma then proves simultaneous pinning on even rows after removing that
factor; a finite screen finds a last-row exception, and the broader
nonboundary generalization remains unproved. The separate reduction-gadget
checker verifies both bounded four-packet variants and the boundary bit;
the mixed-pin screen checks arbitrary pin/gate patterns for three rows. These
finite checks do not review the all-size proof or implement the full recursion.

Issue [#22](https://github.com/1337isnot1337/3-SAT/issues/22) coordinates
this lane. The accepted theorem, selected result and frozen upstream are
unchanged. PR #4 supplies the odd-node basis; earlier general-mode support
work is credited in the proof. New work is Apache-2.0 and substantially
Codex-assisted.
