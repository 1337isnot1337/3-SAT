# Consecutive information sets for adjacent-product queries

Status: `scoped_checked`; substantial OpenAI Codex assistance; no independent
review. Task `dense-encoding`; canonical base
`4ce0cb947bdb6837718c7061e45d3a723219d703`. Selected alpha remains 1/2.

For any binary matrix A and right-hand side b, this package counts Boolean
solutions of `A m=b` with cyclic adjacent products `m_i=x_i x_(i+1)`.
If the linear system is consistent, let d be its nullity and let r be the
largest cyclic interval on which its kernel coordinate projections are
independent. [PROOF.md](PROOF.md) gives a deterministic exact algorithm
using `poly(n+a) 2^(d-r) lambda^r` bit operations and polynomial space,
where lambda=1.754877666.... Inconsistency is detected in polynomial time.
The algorithm finds r rather than assuming it; it also handles r=0.

For n=2d, constraints m_(2j)=m_(2j+1) give d independent coordinates
but only r=2, so this bound has only a constant-factor saving in the
worst case. The result is a restricted quadratic-query algorithm, not
a new all-input SAT algorithm or lower bound. The original accepted
contraction theorem is a premise and the selected record is unchanged.
No unmerged code is needed.

Reproduce with Python 3.11+ and the standard library:

```sh
python3 -I -B research/interval-product-queries/verify.py
make verify
```

The first command checks 5,296 exact Boolean counts, including all
4,096 three-by-three affine systems, 1,766 linear inconsistencies, and
the short-block control. It is bounded evidence, not a proof checker.
The written all-size argument and costs await independent review.

This continues the cyclic prefix method and run weights in
[PR #54](https://github.com/1337isnot1337/3-SAT/pull/54), but is
self-contained and applies to arbitrary A. Coordination: issue #90;
issue #25 studies shared-hash independence and issue #28 bounded-span
transfer, neither of which is a dependency. Contributor: Cinna Davis,
with substantial OpenAI Codex assistance; original material Apache-2.0.

A useful next question is whether an actual family of sparse queries has
large r after every necessary preprocessing step, while retaining all
outer query, entry and reduction costs. The duplicate-coordinate family
shows that such a condition cannot be assumed for arbitrary matrices.
