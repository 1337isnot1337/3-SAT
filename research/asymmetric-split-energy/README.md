# Asymmetric split energy: an ideal minimax identity

Status: `scoped_checked`; the all-size proof is author-checked and awaits
independent review. No SAT bound improvement is claimed. Contributor: OpenAI
Codex, with substantial AI assistance. Base: `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`.

[PROOF.md](PROOF.md) establishes that, for the explicitly defined continuous
quarter-circle minimax recurrence, inverse-square cost coefficients add.
Thus with fixed leaf costs every binary tree gives the same root coefficient;
unequal splits alone cannot improve that model. This develops the observation
in PR 16's `research/modular-rank-factorization/CHECKPOINT.md`.

The normalized factor upper bounds are motivated by the pinned Anthropic
Appendix B, `eq:half-row`, `eq:half-col` and `thm:halfpieces`. The actual
source uses a square grid, chooses a direction once per term, and includes
many costs absent here. No unequal-grid recursion is proved, nor is a lower
bound on actual piece ranks or SAT algorithms. A conditional logarithmic-size
corollary in the proof names the extra hypotheses explicitly. The selected
OpenAI result remains unchanged. Detailed omissions and next bridge appear in
[PROOF.md](PROOF.md).

Reproduce offline using Python 3 standard library:

```sh
python3 -I -B research/asymmetric-split-energy/verify.py
make verify
```

The checker tests exact rational equality witnesses, 303 circle points,
12 tree-size families with unequal leaf capacities, and a wrong-mean control;
it is a finite control and not a proof of the all-size theorem. The proof is
an elementary algebraic argument, not a formal verification or independent
review. Next derive the full straight-edge, rectangle-count and balancing
ledger for an actual `g_L` by `g_R` network, and establish whether child
coefficients and input sizes really satisfy the ideal model. A better
piece-rank envelope is a different premise.

Source attribution: Anthropic, *A 2^{o(n)} Time Algorithm for 3-SAT*,
[Hexagon v1](https://hexagonmath.org/2610.00577v1), pinned and licensed in
`research/anthropic-operator-ranks/source/README.md`; comparison and source
labels are in `research/recent-breakthrough-scan/METHODS.md`. The square-root
observation and next question were first recorded in PR 16's checkpoint.
Original OpenAI source is fixed by `SOURCES.json`; it is accepted by the owner
and is not audited here. New material is Apache-2.0.
