# Fixed-density clause-network space composition

Status: `scoped_checked`; author-checked, substantially Codex-assisted and
not independently reviewed. This package is stacked on PR #94 and its
predecessors. It is conditional on the source crossing-rank, streamability and
good-prime contracts; it does not select or improve the accepted SAT bound.

The source fixed-density clause/equality network has at most `k m` occurrence
bits, polynomial-space entry evaluators and an original integer query bounded
by `2^(k m)`. The PR #94 depth-first field-clique executor and PR #60's
sequential CRT can therefore be composed with this network using polynomial
workspace, when their explicit uniform hypotheses hold. The source's
fixed-density time calculation remains charged, as do prime generation,
every field query, CRT and input/output. Empty clauses, empty formulas and
unused declared variables have explicit handling.

[PROOF.md](PROOF.md) gives the conditional deterministic counting statement,
full time/space accounting and limits. The selected OpenAI theorem already
has polynomial-space alpha 1/2 for fixed density. This work does not improve
that bound, show the structured examples meet a better rho, or cover the
arbitrary-density sparsification/profile/greedy reduction.

Reproduce with Python 3.11+ and the standard library:

```sh
python3 -I -B research/fixed-density-streamed-space/verify.py
make verify
```

[verification.json](verification.json) records 2,613 direct network and CRT
comparisons for 871 small formulas and three groupings, including empty
clauses, tautologies, repeated literals and unused variables. It does not run
the full master recurrence or the large explicit prime-supply sieve.

The source clause-network and fixed-density cost are credited to Anthropic's
pinned source in [PR #17's manifest](../odd-prime-rank-transfer/SOURCES.json),
labels `sec:proof`, `lem:grouping-explicit` and `thm:master:c`. PR #60 supplies
CRT and prime certification; #94 supplies the conditional streamed clique
space bound. The accepted OpenAI source is pinned in
[SOURCES.json](../../SOURCES.json). Contributor: Cinna Davis with substantial
OpenAI Codex assistance; new material is Apache-2.0.

Next: separately analyze the space and time of all arbitrary-density outer
queries and the sparsification branch generator; preserve the stronger
conditions required for a full SAT claim.
