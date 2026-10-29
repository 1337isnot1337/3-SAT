# Heterogeneous parity-check budgets

Status: draft, author-checked argument; bounded replay and independent review
pending. Coordination [issue #153](https://github.com/1337isnot1337/3-SAT/issues/153).
No unrestricted SAT improvement or alpha change is claimed.

The [proof](PROOF.md) combines two changes: use a reduced initial-check
budget n0=ceil(n/log log n), and encode the wide initial checks separately
from the narrower appended checks. The resulting proposed decision bound
for m<=n(log n)^c is

    poly(n+m) 2^{O(n [log(B+2)+log log log n]/sqrt(log n))},
    B=max(1,ceil(m/n)),

with guarded logarithms, fixed k,c, polynomial space and explicit bounded
error. It relies on the named author-checked retuned Tanner and weighted
decision arguments, plus the accepted contraction theorem. When
B=(log log n)^O(1), this improves the general-density envelope for an
unbounded-density regime. General sparsification can still have
log B=Theta(log log n), so the unrestricted target remains open. The
accepted fixed-density route is retained when stronger.

No code in this package implements the full accepted contraction or SAT
algorithm. The next step is a bounded exact replay of the two-layer encoding
and row-budget parameters before publishing this as a checked component.

Base c600b21ee7800a49c05718a254be50168e6b355b; accepted OpenAI source
7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a. Predecessors:
[retuned checks](../polynomial-sparse-checks/RETUNED.md),
[degree-sensitive checks](../tanner-local-distance/PROOF.md), and
[weighted decision](../characteristic-two-decision/PROOF.md).
Contributor: Cinna Davis with substantial OpenAI Codex assistance.
New material Apache-2.0; no independent review or priority claim.
