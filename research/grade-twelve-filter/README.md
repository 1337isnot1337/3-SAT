# Grade-twelve scalar-filter obstruction

This substantially AI-assisted finite certificate extends the fixed-codebook
screens of [PR #46](../asymmetric-scalar-filter/README.md) and
[PR #97](../grade-nine-filter/README.md). It has not been independently or
formally reviewed. It does not prove an asymptotic obstruction or improve a
SAT bound.

## Statement

Take the charge-one raw crossing pieces and deterministic asymmetric row,
column and output partition codebooks selected by `construct(4)` in
[PR #19](../charged-asymmetric-crossing/model.py): grade `h=12`, dimension
`N=16`, shifts `-24,...,24`. If rational weights make every weighted output
matrix scalar for all 256 input label pairs, and if `w_-1=w_0=w_1=0`, then
all weights are zero. No nonzero or invertible scalar pairing on these fixed
codebooks survives that exclusion.

This is one finite codebook. Other codebooks, charge-dependent filters,
non-scalar output identities and all-size behavior are not classified; this
is not a general 3-SAT lower bound.

## Certificate and proof

Off-diagonal zero conditions alone give integer linear equations in the 46
noncentral shift weights. Use the 360 equations from the input pairs and
output indices listed in [verification.json](verification.json). Split the
columns into 36 middle shifts and ten edge shifts `-24,...,-18,22,23,24`.
The integer edge block has exact rational rank one: the checker verifies a
nonzero entry and every two-by-two minor involving that entry vanishes. The
middle block has rank 36 modulo 65537, and the whole 360-by-46 matrix has
rank 37 modulo 65537.

Over the rationals the whole rank is at least 37 by reduction modulo the
prime and at most 37 because there are 36 middle columns and the edge block
has rank one. The middle and edge column spans are therefore independent,
and the 36 middle columns are linearly independent. Consequently any
rational solution of this first block has all 36 middle weights zero.

Now retain only the ten edge weights. The first block's edge columns together
with 30 off-diagonal equations (15 each from input pairs `(0,0)` and `(0,1)`
at output input index `y=15`) have rank 10 modulo 65537. Their rational kernel
is zero, so the ten edge weights vanish too. Every scalar-output filter
satisfies these necessary off-diagonal equations, proving the finite claim.
All indices are zero-based in the predecessor's deterministic codebooks.

## Reproduction and limits

```sh
python3 -I -B research/grade-twelve-filter/verify.py > /tmp/grade-twelve-filter.json
cmp /tmp/grade-twelve-filter.json research/grade-twelve-filter/verification.json
make verify
```

The checker uses exact integer tensor entries, verifies the exact edge rank
one, and independently obtains all stated rank lower bounds by forward
elimination over the prime field. It uses only the standard library and the
hash-pinned predecessor implementation. Negative shifts use the reverse
operator order, positive shifts the original order; their equality is the
inherited PR #11 identity. The grade-nine package cross-checks this order
against its full predecessor integer matrix. The grade-twelve second block is
not independently implemented. Matrix shapes and hashes are in the saved
report.

The finite screen does not establish leading codebook capacity, a uniform
filter, or any asymptotic cost. A proposed algorithm must still pay for both
flattening ranks, entry generation, reductions and queries, precision,
recursion, recovery and space. The accepted theorem and selected result are
unchanged.

## Next question and credit

A genuinely all-size argument or a counterexample is needed; additional
finite grades alone cannot settle it. The separate alternative-codebook and
cubic-moment route is tracked in [issue #21](https://github.com/1337isnot1337/3-SAT/issues/21).

Charged operators and the two-order identity are from
[PR #11](../charged-operator-moments/PROOF.md); the deterministic asymmetric
codebook is from [PR #19](../charged-asymmetric-crossing/PROOF.md). The
finite-screen method builds on PRs #46 and #97. This package was started at
main commit `c7c5a03434b396e227e9ab573b5b7cdea52b47fa` and was created with
substantial OpenAI Codex assistance. No independent review is claimed.
