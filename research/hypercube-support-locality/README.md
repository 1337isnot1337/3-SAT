# Hypercube support and cyclic-span obstruction

Status: `scoped_checked`. Substantially AI assisted; no independent review,
selected-result change, general SAT lower bound or faster SAT algorithm.

For even `d`, put `n=2^d` and orient the hypercube so that each vertex has
`d/2` outgoing edges. The corresponding `n` sparse quadratic equations have
original variable scope and load `d/2+1`. Every invertible row basis retains
at least `(d/2)^n` nonzero degree-`2n` incidence coefficients in the scalar
zero-indicator lift. As in [PR #44](https://github.com/1337isnot1337/3-SAT/pull/44),
its injective coefficientwise indexing requires `Omega(n log log n)` bits
in some degree array.

As a second scope control, fixing one color class leaves linear equations on
the other. Summing their exact solution counts gives a `2^(n/2) poly(n)` time,
polynomial-space algorithm, including any prescribed fixed-bit branch. It is
asymptotically slower than the accepted general bound and gives no SAT speedup.

The new boundary: every cyclic order and every invertible row basis has an
equation with cyclic span at least `1+n/(2d)`. This blocks the logarithmic
cyclic-span premise of [PR #48](https://github.com/1337isnot1337/3-SAT/pull/48)
for this family. The span bound also survives `B=o(n/log n)` arbitrary fixed-bit substitutions
and any residual spanning basis, but this does not cover the source
preprocessing allowance `O(n/sqrt(log n))`. Removing the middle Hamming
layer gives an explicit half-cut with no surviving crossing edges at that
allowance scale; this only limits that proof technique. It does not rule out
other aggregation, simplification,
variable elimination, nonlinear changes, or other algorithms; the all-zero
assignment is an immediate solution. See [PROOF.md](PROOF.md) for the exact
representation, cost limits, and all-size arguments.

Reproduction from the repository root, Python 3 and standard library:

```sh
python3 -I -B research/hypercube-support-locality/verify.py
make verify
```

Saved [verification.json](verification.json) covers dimensions 2, 4 and 6:
228 edges, 1,015 combinations, 56,060 integer Mobius coefficients, all
20,160 invertible 4-by-4 bases, 200 seeded larger bases, 424 cyclic orders, 65,530 deleted-vertex/order
cases, 10 middle-layer arithmetic controls, and 202 fixed-bit branches
checked against exhaustive counts. Finite checks do not prove the asymptotic statements. The written
proof awaits independent review.

Sources: canonical main `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`;
accepted OpenAI source `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`,
`lem:tensor-sparse-query`, `eq:sharp-incidence-degree`,
`eq:sharp-wire-budget`; scalar support predecessor
[PR #44](https://github.com/1337isnot1337/3-SAT/pull/44) at
`93dd174db3c354d3548bce4b291af30a6964977f`; locality predecessor
[PR #48](https://github.com/1337isnot1337/3-SAT/pull/48). The private-edge
support argument is credited to PR #44; this package changes the graph and
proves its cyclic-span boundary. Before issue #67 was opened, a concurrent
[issue #29 continuation](https://github.com/1337isnot1337/3-SAT/issues/29#issuecomment-6459412498)
independently proposed the same private-edge hypercube/nonlocality objective
using a bipartite double cover; its later branch analysis is not claimed here.
Contributor: 1337isnot1337, with substantial
OpenAI Codex assistance. New material is Apache-2.0.
