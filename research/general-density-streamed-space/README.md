# Streamed general-density outer reduction

Status: `scoped_checked`; author-checked, substantially Codex-assisted and
not independently reviewed. This is stacked on PRs #106, #94 and their
predecessors. It composes an existing source reduction under explicit
crossing, prime-supply and space contracts; no improved SAT exponent or
selected result is claimed.

For fixed width, normalized sparsification branches have polynomial depth:
each branch strictly enlarges the finite syntactic-subsumption closure, whose
clause universe has polynomial size. A depth-first traversal can therefore
retain one polynomial-size formula per level. At each leaf, profile indices,
greedy check lists and rational comparisons are streamed. Each original
signed profile-network query has magnitude at most `2^(g(P+B))`, is recovered
from good-prime field queries by CRT, and is then included in the source's
power-of-two reductions. The source's time, disjointness and density bounds
remain explicit prerequisites.

[PROOF.md](PROOF.md) states the full conditional claim and its limits. The
OpenAI baseline already gives alpha 1/2 and polynomial space for general
fixed-width counting. The new composition does not exhibit a crossing family
with better rho; PR #17's unrestricted rational family is not automatically
derandomized by the structured good-prime contracts.

Reproduce with Python 3.11+ and the standard library:

```sh
python3 -I -B research/general-density-streamed-space/verify.py
make verify
```

[verification.json](verification.json) records 27,696 strict-closure branch
checks over 1,465 small antichains, 2,592 signed-CRT/outer-identity cases and
positive-X negative controls. It does not implement the actual branch
selection, profile tensor construction, prime sieve or master recurrence.
These finite checks do not establish the all-size source theorem.

The pinned Anthropic source and its `thm:onelog:a`, `app:count`,
`app:onelog` and `lem:grouping-explicit` provide the outer algorithm and time
bounds; see [PR #17's manifest](../odd-prime-rank-transfer/SOURCES.json). PRs
#60 and #94 provide the stated CRT and field-clique interfaces, and #106 the
fixed-density counterpart. The owner-accepted OpenAI source is pinned in
[SOURCES.json](../../SOURCES.json). Cinna Davis with substantial OpenAI Codex
assistance; new work is Apache-2.0.

Next: seek an actual changed crossing or reduction mechanism with a proved
better rho and all source-wide costs, or a deterministic prime supply for the
unrestricted rational interface. Refresh live research claims first.
