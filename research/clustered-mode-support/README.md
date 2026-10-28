# Clustered Newton modes at the source precision

Status: `scoped_checked`. The all-size argument is author-checked and awaits
independent review. No SAT improvement or general lower bound is claimed.

Task: `weighted-modes`; base `8d6010ab8934b8942611ba98c3a80723f65e0d53`.
Contributor: Cinna Davis, with substantial OpenAI Codex assistance.

The [proof](PROOF.md) gives an explicit bounded-degree tensor-network family
with full, exactly balanced root packets and a specified valid packing.
At `t=1` with `zeta=1` included in the evaluation set, at least
`exp(Omega(M/sqrt(u(a+2)))) = exp(Omega(M/u))` distinct complete
child-product summands are within the source's weighted mode budget and
nonzero modulo its prescribed child precision. Here `a=2u` at the root.

The construction groups selected rows into short intervals, so all first `b`
mode coefficients in a packet share only `O(b)` distinct odd denominator
factors. Pinned source bits give unit mode values; the common denominator
and row signs bound the exact valuation of every chosen squarefree term.
This improves the representation-specific `exp(Omega(M/u^2))` count in
[PR #105](https://github.com/1337isnot1337/3-SAT/pull/105), and remains below
the formal `exp(Theta(M/sqrt(u)))` envelope.

The network is disconnected and easily simplified. The source's default
labeling need not choose this packing, and nonzero terms can cancel or be
aggregated. The result is not a SAT lower bound, a lower bound against all
contraction methods, or a speedup. Independent review, the remaining
valuation gap, and any full algorithmic cost analysis remain open.

Reproduce using Python 3.11+ and the standard library:

```sh
python3 -I -B research/clustered-mode-support/verify.py
make verify
```

[verification.json](verification.json) binds the proof, checker and frozen
source by SHA-256. Exact cases `(L,b)=(16,2),(32,3),(64,4)` check the common
odd denominator, row-entry and summand valuation bounds, source units,
full Newton kernel and complete local contraction. These finite checks do
not prove the all-size result or implement the full recursion. Issue
[#22](https://github.com/1337isnot1337/3-SAT/issues/22) coordinates the lane.
The accepted source, selected result and upstream files are unchanged;
PR #4 supplies the Newton expansion. New work is Apache-2.0 and substantially
Codex-assisted.
