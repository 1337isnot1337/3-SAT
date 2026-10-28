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
Jointly independent disjoint intervals give a complementary bound; in
particular, t greedily selected independent triples require at most
`poly(n+a) 2^(d-3t) 7^t` bit operations. The implementation chooses the
smaller of the single-interval and triple candidate counts.

For n=2d, constraints m_(2j)=m_(2j+1) give d independent coordinates
but only r=2, so this bound has only a constant-factor saving in the
worst case. In fact, that family is polynomial-time countable by a
two-state transfer: with w right-hand-side ones its count is
`3^(d-w)+(-1)^w`. This applies the bounded-span method from
[PR #48](https://github.com/1337isnot1337/3-SAT/pull/48). The result is a
restricted quadratic-query algorithm, not a new all-input SAT algorithm or
lower bound. The original accepted
contraction theorem is a premise and the selected record is unchanged.
No unmerged code is needed.

Reproduce with Python 3.11+ and the standard library:

```sh
python3 -I -B research/interval-product-queries/verify.py
make verify
```

The first command checks 5,296 exact Boolean counts, including all
4,096 three-by-three affine systems, 1,766 linear inconsistencies, and
the short-block control. It also checks both enumerators on all systems
and verifies a fragmented n=12 example where triples use 343 candidates
versus 384 for the single interval. It is bounded evidence, not a proof
checker. It also checks all 124 right-hand sides of the transfer formula
for d=2,...,6. The written all-size argument and costs await independent review.

This continues the cyclic prefix method and run weights in
[PR #54](https://github.com/1337isnot1337/3-SAT/pull/54), but is
self-contained and applies to arbitrary A. Coordination: issue #90;
issue #25 studies shared-hash independence and issue #28 bounded-span
transfer, neither of which is a dependency. Contributor: Cinna Davis,
with substantial OpenAI Codex assistance; original material Apache-2.0.

A useful next question is whether actual sparse queries supply large
independent intervals or many independent triples after every necessary
preprocessing step, while retaining all outer query, entry and reduction
costs. The duplicate-coordinate family
shows that such a condition cannot be assumed for arbitrary matrices.
