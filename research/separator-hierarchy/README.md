# Separator hierarchy composition

Status: `scoped_checked`; written proof has not received independent review. Task `decision-only`, base `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`. Contributor: Codex, with substantial AI assistance.

[PROOF.md](PROOF.md) gives a deterministic exact-counting wrapper for a supplied and verified primal-graph separator hierarchy. It pays the maximum separator size sum along a root-to-leaf path, plus the accepted leaf-solver cost, and uses polynomial space. It also shows that an explicit constant-degree expander encoded as a bounded-occurrence 2-CNF can require linear balanced separators. That formula is easy to satisfy; this is an obstruction to a structural guarantee, not a SAT lower bound. [LINE-GRAPH.md](LINE-GRAPH.md) strengthens the obstruction: an existential family has exactly two occurrences per variable, no pure literals, and no original one-step resolvent shorter than four literals. These formulas are also satisfied by all-true. The selected alpha remains 1/2.

The promised hierarchy may yield faster algorithms for restricted classes, but no efficient hierarchy with the required load is given for all 3-CNF. The fixed-density leaf bound needs local density or bounded occurrence, not merely global linear density. The accepted theorem is used as a black box, not reimplemented. The expander theorem is an external dependency, explicitly pinned in the proof.

Run:

```sh
python3 -I -B research/separator-hierarchy/verify.py
python3 -I -B research/separator-hierarchy/linegraph.py
make verify
```

The first command checks 1,200 reproducibly generated small CNFs against exhaustive counting, including empty clauses and free variables, and exhaustively checks balanced separators of a 16-vertex graph instance and checks the exact-width-three encoding on it. These are finite controls, not verification of the all-size proof or of expansion. The line-graph checker covers K4 and the cube and their eligible edge subsets. Both checkers use only Python's standard library.

A useful continuation would identify a nontrivial SAT-preserving preprocessing that provably produces low-load hierarchies, and charge its branches and time. Any general claim must handle formulas that retain expander primal graphs after the proposed preprocessing.
