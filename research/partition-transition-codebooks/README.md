# Partition transition codebooks for many charged moments

Status: `scoped_checked` for the registered small operator checks. The all-size
argument is author-checked and awaits independent review. **No smaller rho,
SAT time improvement, or alpha change is claimed.**

Task: `contraction-schedule`. Base `ec45f184710a6adcd74e1aea31f29d7d1c44d0e2`.
Contributor: Cinna Davis with substantial OpenAI Codex assistance. Apache-2.0.

The [proof](PROOF.md) constructs a single output partition codebook on which
all charged zero modes of weight at most d compress to scalars. It selects a
largest diagonal-signature class and a greedy independent set of the union
of their transition graphs. For `d=floor((ln E)^2/144)`, its size retains
`exp(pi sqrt(2E/3)-o(sqrt(E)))` output states, and construction takes
`exp(O(sqrt(E)))` time and space. Via the moment argument of
[PR #89](https://github.com/1337isnot1337/3-SAT/pull/89), a polynomial filter
then removes a growing `Theta(log^2 E)` central shift interval while staying
scalar on this output codebook.

This output compression is not a complete crossing identity. The scalar
input-label pairing is not shown nonzero or high rank; the removed interval
is o(E), not the fixed fraction needed for the stated rho target. No
normalizer, full two-direction rank bound, polynomial-space transfer, or SAT
algorithm is supplied. The codebook is not invariant under the operators.
The construction complements PR #89's parity-sector compression and leaves
its input-rank continuation to issue #21.

Reproduce with Python 3.11+, standard library:

```sh
python3 -I -B research/partition-transition-codebooks/verify.py
make verify
```

[Saved output](verification.json) gives 21 exact codebooks for energies 1..7
and mode weights 1, 3 and 4; 231 direct normal-ordering comparisons; and 39
actual charged-filter diagonal checks with degrees 3 and 5. The degree-5
full-label pairing ranks at h=2,...,6 are 2, 2, 5, 6, 10 out of dimensions
2, 3, 5, 7, 11. Those output codebooks are singletons; these exact finite
ranks do not establish a growing-codebook rank bound. The verifier reuses the pinned predecessor operator modules;
it does not implement a contraction or review the all-size proof.

Credit the charged first-moment construction in
`research/charged-operator-moments`, the asymmetric crossing in
`research/charged-asymmetric-crossing`, and PR #89 at
`431477efe926c611e693804f323c50ac76969192` for the cubic moment/compression
and moment-to-zero-mode argument. The accepted OpenAI source commit is
`7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`; upstream hashes and licenses are
in [SOURCES.json](../../SOURCES.json). No external priority claim is made.
Coordination: [issue #108](https://github.com/1337isnot1337/3-SAT/issues/108).
