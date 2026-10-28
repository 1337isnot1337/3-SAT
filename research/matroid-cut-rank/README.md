# Cut rank of the binary-matroid independence predicate

Status: `scoped_checked` for finite witness construction; the all-size proof
is author-checked and awaits independent review. No SAT bound is claimed.
Task `decision-only`; base `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`.
Contributor: Cinna Davis, with substantial OpenAI Codex assistance. Apache-2.0.

[PROOF.md](PROOF.md) proves that the two-sided independence table for a
binary matrix has rank at least `2^b` over characteristic-two fields and Q,
where b is the intersection dimension of the column spans on either side.
The proof constructs an invertible minor using quotient bases and compound
matrices. This strengthens the paired-column example in PR #37 to arbitrary
binary matrices and bounds every exact separation across the stated cut,
not just a particular state encoding. No odd-characteristic claim is made.

Combined with the distance/nullity width-sum argument in PR #55, every exact
ordered chain of this independence predicate has at least `k(D-1)` Boolean
bond-bit incidences, for binary kernel dimension k and minimum nonzero kernel
weight D>=2. Applied to the source sparse checks in the conditional regime
with residual nullity K=max(0,m-3n-t)>0 and m>P, this gives at least
`K(ceil(m/P)-1)` such incidences. The bound does not apply automatically to
other network topologies or the final summed hash predicate; no claim is made
that all leaves have the needed nullity or that SAT itself has a lower bound.

## Reproduction

```sh
python3 -I -B research/matroid-cut-rank/verify.py
make verify
```

The checker constructs the explicit invertible minor at every cut of all
4,096 binary 3-by-4 matrices (20,480 witnesses), and at every cut of 1,000
seeded 4-by-8 matrices (9,000 witnesses). It checks the quotient-basis
conditions and rank over F_2. The [saved output](verification.json) pins the
checker hash and reports the observed width distribution. The finite screen is
not an independent review and does not prove the all-size statement.

## Credit and next steps

The shared-code identity is from PR #2; PR #37 supplies the frontier network,
and PR #55 supplies the distance/nullity cost context. Both are separate
unreviewed research contributions. Their pinned heads at authoring time are
`498b10ceb2d0dcb2dfc3fbfa5e3b6be23dfe8b50` and
`0264a0cf35da09f4abab4118dc870aed121fa167` respectively; the source's accepted sparse-check
lemma is in [main_full_version.tex](../../upstream/openai-eth-2026/build/main_full_version.tex)
and the frozen source is identified in [SOURCES.json](../../SOURCES.json).
The connectivity dimension, exterior powers and rank-factorization bound are
standard; no priority is claimed for these methods or the result. A next
question is whether another topology can exploit cancellation after the
independent-set terms are summed, with all reduction and contraction costs
paid. The selected theorem remains unchanged.
