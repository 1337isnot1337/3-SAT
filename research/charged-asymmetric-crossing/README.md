# Uniform asymmetric charged crossing pieces

Status: `scoped_checked`. An actual uniform rational family omits s=0 and
retains the source's two-direction rho=1/sqrt(2) envelope. No improved
rho, SAT alpha or selected-result change is claimed. Written proofs are
author-checked and await independent review.

Task: `contraction-schedule`; base
`b91287aa1361fa49d68afe5cc94c23077dce93db` (PR 11 merge).
Contributor: Cinna Davis, with substantial OpenAI Codex assistance.
The accepted OpenAI theorem is a premise; frozen upstream is unchanged.

## What changed

PR 11 proved that the charged first-moment pairing is square-zero with
rank `p(h)-p(h-1)` and left asymmetric coordinates and normalization open.
Here h is chosen minimally so that this rank is at least N=2^lambda.
Exact elimination selects a nonsingular N-by-N minor using different row
and column labels. Its rational inverse acts on x alone. Multiplying the
source pieces by s and that inverse gives an exact crossing sum, with no
central s=0 piece. Both required flattening ranks are preserved because
the inverse is local on each required cut.

[PROOF.md](PROOF.md) accounts for label capacity, uniform construction,
inverse height, entries, both ranks and full time/space transfer. The
partition space has at most `h^2 N` states and `h=Theta(lambda^2)`.
Generic inversion and entry generation take `2^O(lambda)` bit time even
when rational heights are exponential. PR 17's bounded prime-field
transfer pays that normalization and recovers exact integer outer queries.
The generic compiler's exponential space and one-sided decision error
are explicit. No full SAT implementation is claimed by this package.

Deleting one shift leaves nearby shifts with the same leading term-count
envelope. The supplied ratio stays rho=1/sqrt(2), so this is progress on
the component interface, not a faster SAT theorem. The finite actual ranks
are reported literally; they are not extrapolated.

## Verification

Standard-library Python, offline, from repository root:

```sh
python3 -I -B research/charged-asymmetric-crossing/verify.py
make verify
```

The checker constructs all normalized pieces at lambda=1,2 (h=4,6),
checks 272 exact crossing entries, 160 exact rational rank computations,
both source term bounds, 152 positive-output-grade two-order identities,
both field factorizations and all 4+16 assignment-predicate counts over
F65537. It also selects and inverts minors at lambda=3,4 (h=9,12) without
building those full operator tensors. It uses pinned predecessor modules
unchanged and hash-binds its output. These bounded research checks stay
outside default CI.

The test is not an independent review of PR 11, the source theorem, the
all-size transfer or this proof. It is not a formal proof or a full
master/dense-reduction replay. The accepted alpha remains 1/2.

## Next target, limits and credit

[NEXT.md](NEXT.md) specifies a scalar interval filter retaining leading
label and output capacity. If a valid filter removed `|s|<epsilon h`,
the conditional ratio would be
`(sqrt(2+epsilon)+sqrt(2-epsilon))/4`; this has NOT been achieved.
General higher moments are operator-valued. A generic joint-axis inverse
or a high-charge coefficient cannot be treated as a free scalarization.
The same page proves a limited support-rank bound for charge-independent
weights before any charge-dependent normalization, and keeps its scope
separate from a full filter obstruction.

[SOURCES.json](SOURCES.json) credits and pins PR 11's operator/rank formula,
PR 17's rational transfer, the source's two directional factorizations and
the earlier uncharged moment-recovery screen. The normal-form minor and
inverse algorithms are standard. New work is Apache-2.0 and substantially
Codex-assisted; no priority, independent review or theorem promotion is
claimed. The active continuation is [CHECKPOINT.md](CHECKPOINT.md).
