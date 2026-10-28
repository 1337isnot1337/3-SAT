# Optimal characteristic-two independence frontier

Status: `scoped_checked` for finite controls; the all-size proof is
author-checked and awaits independent review. No SAT bound is improved.
Task `decision-only`; base `e1e57cd165d9806b1bbf6500153ee1f37fedf093`.
Contributor: Cinna Davis, with substantial OpenAI Codex assistance. Apache-2.0.

[PROOF.md](PROOF.md) replaces the subspace-indexed ordered frontier of PR #37
with a linear state indexed by individual frontier vectors. Over any field of
characteristic two it computes the exact binary-matroid independence
indicator using `b_i` Boolean state bits at cut i, with polynomial-time local
entries. Dependence is rejected by cancellation: the state is a vector of
amplitudes, not a deterministic single-state path. Summing the selection
bits with weights also computes the full independent-set polynomial at
arbitrary field inputs.

For every cut, the independence table has rank exactly `2^b_i` over such a
field, so the state-bit count is optimal for this ordered-chain interface.
A two-dimensional binary example has rank 4 over F2 but 5 over F3; no
corresponding odd-characteristic or rational upper bound is claimed.
The total width lower bound of PR #55 still applies. For relevant sparse
checks it can make the ordered chain much larger than the nonlocal row
network in PR #83. None of these bounds rules out another topology or a
faster SAT algorithm.

## Reproduction

```sh
python3 -I -B research/independence-linear-frontier/verify.py
make verify
```

The standard-library checker covers all 4,096 binary 3-by-4 matrices and
65,536 selected subsets, verifies each frontier-state entry and all 20,480
F2 cut ranks, checks the F2/F3 separation, and compares 200 GF(8) weighted polynomial cases with direct enumeration. The
[hash-bound output](verification.json) records exact counts. Finite controls
are not an independent review or an implementation of the accepted solver.

## Credit and next questions

The independent-set identity comes from PR #2; the original frontier is PR
#37, the width area bound is PR #55, and the lower cut-rank proof is PR #74
(commit `e21ff2db8f5f800fa8e7e398f4cc4d21af496850`). Their unreviewed claims remain separate. The frozen
OpenAI source is pinned in [SOURCES.json](../../SOURCES.json); standard
linear algebra and characteristic-two cancellation are used without a
priority claim. An application still needs the ring embedding, actual input
widths and all branches, precision, recursion, decoding and space costs.
The selected result remains unchanged.
