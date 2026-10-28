# Clause-polynomial rank cannot alone remove density

Status: `scoped_checked` for the named finite checks. Written arguments are
author-checked and not independently reviewed. No SAT lower bound or new
alpha is claimed. The owner-accepted OpenAI theorem is the starting point.

Task: `dense-encoding`. Base `e1e57cd165d9806b1bbf6500153ee1f37fedf093`.
Contributor: Cinna Davis with substantial OpenAI Codex assistance. Apache-2.0.

For a normalized satisfiable k-CNF with m clauses, the dimension r of the span
of its original clause-violation polynomials over any field satisfies
`m <= (2^k-1)r`; for arbitrary formulas, `m<=2^k r`. The
[proof](PROOF.md) gives a triangular support argument and a satisfiable unique-
solution family with exact rank `sum_{j=1}^k binom(n,j)` attaining the
satisfiable constant asymptotically. Thus linear relations among the original
clauses cannot by themselves turn superlinear density into a linear-size
basis. Those sharp examples are easy to solve; no arbitrary SAT lower bound
or limitation on nonlinear or formula-aware preprocessing follows.

Reproduce with Python 3.11+ and the standard library:

```sh
python3 -I -B research/clause-polynomial-rank/verify.py
make verify
```

[Saved output](verification.json) checks all 4,352 families in two registered
small domains over F2 and F3, including unsatisfiable cases; five growing
sharp-family fixtures have their unique solution and exact ranks checked. The
finite replay does not independently review the general proof.

The accepted OpenAI source commit is
`7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`; see
[SOURCES.json](../../SOURCES.json), `lem:tensor-sparse-query` and
`subsec:sharp-dense`. This applies to original clause polynomials, not the
sparse-query equation bases studied in issue #29 or cancellation-free circuits
in issue #31. Coordination is recorded in
[issue #93](https://github.com/1337isnot1337/3-SAT/issues/93).
