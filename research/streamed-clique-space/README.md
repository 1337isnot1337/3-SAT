# Polynomial workspace for a streamed field-clique query

Status: `scoped_checked`; author-checked, substantially Codex-assisted and
not independently reviewed. This package is stacked on PRs #84, #71 and #60.
It proves a conditional workspace bound for the source's field-clique
recursion, not a new SAT exponent or a complete polynomial-space SAT algorithm.

If root tensor entries and crossing factors have uniformly bounded
polynomial-workspace evaluators, the recursion can enumerate crossing choices,
groupings and child settings depth first, recomputing child entries rather than
storing their exponential tables. A field accumulator, each frame and each
counter have polynomial bit length, and the source recursion has
`O(log log H)` levels. The source's on-demand query time accounting charges
recomputation, factor generation and the root query cost `tau`. The inherited
master time bound is conditional on all its rank and recurrence hypotheses.

[PROOF.md](PROOF.md) contains the precise contracts, space and time argument,
root-query requirements and remaining gap. PR #84 supplies appropriate
factor-entry formulas for its named structured families; that does not make
those families satisfy an improved rho. The generic matrix compiler and the
full fixed- or arbitrary-density SAT reduction are not covered. Exact CRT
query recovery can be composed sequentially when its own inputs and root
oracles satisfy the stated space contracts.

With Python 3.11+ and the standard library:

```sh
python3 -I -B research/streamed-clique-space/verify.py
make verify
```

[verification.json](verification.json) records 256 finite two-layer lazy
contractions, 768 field-versus-exhaustive comparisons, signed integer CRT
recovery and a three-frame maximum in that toy evaluator. These checks do not
implement the master recursion or establish its asymptotic space bound.

The accepted OpenAI baseline and primary Anthropic source are pinned in the
predecessor manifests; source reference labels include `lem:grouping`,
`lem:grouping-explicit`, `prop:level` and `thm:master:b`. Credits: the cited
source for the clique/grouping recursion and query-cost model; PRs #16 and #17
for call-size and rational field transfer, #60 for CRT, #71 for structured
good primes, and #84 for streamed factor entries. Contributor: Cinna Davis
with substantial OpenAI Codex assistance; new material is Apache-2.0.

Next: bound the space of every outer reduction, especially sparsification
branch generation, profile and greedy-query enumeration, before asserting a
full SAT space guarantee. Coordinate via live issues first.
