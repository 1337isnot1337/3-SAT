# Dense packets with precision-surviving Newton modes

Status: `scoped_checked`. The all-size proof is author-checked and awaits
independent review. No SAT improvement or general lower bound is claimed.

Task: `weighted-modes`; base `4ce0cb947bdb6837718c7061e45d3a723219d703`.
Contributor: Cinna Davis, with substantial OpenAI Codex assistance.

## Result

The [proof](PROOF.md) gives an explicit family of bounded-degree tensor
networks and specified valid root packings with all packet slots occupied
and exactly balanced label-pair loads. For the general Newton modes at
`t=1` and an evaluation set containing `zeta=1`, at least
`exp(Omega(M/[u(a+2)])) = exp(Omega(M/u^2))` distinct complete
child-product summands lie inside the source's weighted budget and are
nonzero modulo the prescribed child precision. Here `a=2u` at the root.

Pinned source columns make the selected mode forms two-adic units. A common
odd denominator and the sign pattern of the equality tensor give an upper
bound on the valuation of each selected squarefree row coefficient. This
extends the single-packet work in [PR #41](https://github.com/1337isnot1337/3-SAT/pull/41)
without relying on that unmerged branch for execution.

The specified packing need not be the source's default deterministic
labeling. The network is disconnected and easily simplified; nonzero terms
may cancel after summation, and other algorithms may aggregate or eliminate
them. This is a scoped support result, not a time lower bound. The count is
smaller than the formal `exp(Theta(M/sqrt(u)))` envelope. For one consecutive triple placement, pairing and telescoping give exact
valuations for the first three individual modes; these do not bound
mixed-mode coefficients. A sharper bound on coefficient valuations is needed to bridge that gap, and even that would
not by itself establish a SAT lower bound or improvement.

## Reproduce

Python 3.11+, standard library, from the repository root:

```sh
python3 -I -B research/dense-packet-mode-support/verify.py
make verify
```

[verification.json](verification.json) binds the checker and proof to the
frozen source and PR #4's local mode proof. Exact packet checks at `L=8,16`
verify source units, odd common denominators, selected summands, valuations,
and the full local contraction over rational numbers. Pairing and telescoping identities for three modes are checked for `a=3,...,9`. A small `r=2` toy
checks full packet orientation, pair loads, and eligibility; it is not the
source's asymptotic schedule. The checker does not independently prove the
all-size construction or implement the full recursive contraction.

The accepted theorem and selected result are unchanged. Issue
[#22](https://github.com/1337isnot1337/3-SAT/issues/22) coordinates this
lane. The source theorem and PR #4 supply the packet and Newton identities;
PR #41 supplies the credited local sign observation. New material is
Apache-2.0 and substantially Codex-assisted.
