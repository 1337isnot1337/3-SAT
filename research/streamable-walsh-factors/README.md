# Streamable factors for cyclic Walsh crossings

Status: `scoped_checked`; author-checked, substantially Codex-assisted and
not independently reviewed. This is stacked on PR #71 and PR #60. It provides
per-entry factor formulas, not a full polynomial-space recursive algorithm or
an improved SAT bound.

PR #17's generic rational-rank compiler explicitly stores exponentially large
matrices. For the structured Pauli/Bell families, cyclic conjugation instead
has direct formulas for both crossing cuts. Given coefficient evaluation and
support-unranking routines with polynomial workspace, each field-factor entry
uses polynomial workspace and `2^O(lambda) poly(log p)` bit time. It uses
exactly the rational support label budget and returns zero for invalid codes.
PRs #14 and #15 supply the relevant structured coefficient and unranking
interfaces; their known rate obstructions remain in force.

[PROOF.md](PROOF.md) specifies the field, label, denominator and indexing
hypotheses, the four exact factor formulas, their cost and the unresolved
recursive-space question. PR #71 supplies good primes for its stated fixed
base families and compact base-denominator certificate. No generic factor
compiler, global SAT space bound, new rho, or alpha improvement follows.

Reproduce using Python 3.11+ with the standard library:

```sh
python3 -I -B research/streamable-walsh-factors/verify.py
make verify
```

[verification.json](verification.json) records 65,536 comparisons of the two
factorizations against independently constructed tensor entries for the
actual six-class R=1 family under base-3 cyclic conjugation over primes 23 and
47. It checks invalid binary label-code slots as well. This bounded checker
stores arrays and does not implement the full recursive algorithm or prove
asymptotic unranking.

Base PR #71 head `b22894b`; underlying base main and accepted OpenAI theorem
are pinned in the predecessor packages and [SOURCES.json](../../SOURCES.json).
Credits: PR #14 for Pauli/Bell factors and symmetric support indexing, PR #15
for six-class macro data, PR #17 for rational crossing transfer, PR #60 for
CRT and PR #71 for cyclic conjugation and good primes. Contributor: Cinna Davis
with substantial OpenAI Codex assistance. New material is Apache-2.0.

Next: prove or refute a complete polynomial-space composition through recursive
factor descriptions, enumeration and integer-query recovery, without worsening
the master time. Refresh open claims before taking that separate step.
