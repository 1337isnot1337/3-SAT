# Quadratic-rank character-sum counting

Status: `scoped_checked`; substantially AI assisted, not independently
reviewed. No general SAT improvement or selected-result change.

For explicitly listed degree-at-most-two F2 systems, let r be the rank of
the rows of quadratic coefficients. Gaussian elimination separates affine
constraints from r quadratic equations; expanding their zero indicators gives
`2^r` quadratic character sums, each evaluable in polynomial time by pair
elimination. The exact count, including prescribed fixed-bit branches, takes
`2^r poly(input)` time and polynomial space. The proof and full local bit
costs are in [PROOF.md](PROOF.md).

An explicit low-load sparse-query family has `r=n/log2 n` while its
interaction graph is a perfect matching with minimum vertex cover n/2. It
separates this parameter from the interface of PR #113; that particular family
also factors and is easy by a direct product. Separate disjoint pair equations
show that the sparse-query hypotheses allow `r=n/2`. For cubic systems, a supplied set C hitting all cubic monomials permits a
second exact interface, with time `poly(input) sum_c 2^r(c)` over assignments
to C and polynomial space. Small C does not imply small branch rank: the
proof gives a single-variable transversal exposing linearly many independent
quadratics. No uniform bound on these combined costs for all greedy candidates
is claimed.

Reproduce from the repository root, Python 3 with standard library:

```sh
python3 -I -B research/quadratic-rank-sums/verify.py
make verify
```

The saved [verification.json](verification.json) covers all 2,048 four-bit
quadratic character sums, 1,800 seeded systems and fixed-bit branches, 1,538
dependent-row controls, eight affine-rank controls, three matching-block
fixtures, 800 cubic systems and fixed branches, 800 cubic-cover controls,
and explicit rejection of cubic inputs by the quadratic-only routine. Exhaustive counting is independent
of the character-sum routine. Finite controls do not prove asymptotic claims.

Canonical base `c7c5a03434b396e227e9ab573b5b7cdea52b47fa`; accepted OpenAI
source `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`, especially
`lem:tensor-sparse-query` and `subsec:sharp-dense`. Prior work includes:

- Sanyam Agarwal and Gorav Jindal, [*Deterministic NC Quadratic Root Counting
  in Characteristic Two*](https://arxiv.org/abs/2609.12669), arXiv
  `2609.12669v1` (2026), PDF SHA-256
  `c7d447b0fbe9e2aadbddaba4e3b9b6597a7bd77cdd2b755dafc3ffbab4e8de3a`;
  this paper credits Ehrenfeucht and Karpinski's earlier polynomial-time
  quadratic root counting.
- Xiaodie Luo and Kaimin Cheng, [*Counting solutions to a system of quadratic
  form equations over finite fields*](https://doi.org/10.3934/math.2025619)
  (2025), PDF SHA-256
  `7a66e280c8bcc5792fc8a47f6aa573a20d6ea0baaea31b61270404e26098614d`;
  it uses character sums for systems of homogeneous quadratic forms.

These are background and attribution; the argument here is self-contained.
No priority claim is made. Contributor: 1337isnot1337 with substantial OpenAI
Codex assistance. New material is Apache-2.0.
