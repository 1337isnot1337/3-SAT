# Continuation checkpoint

User objective: continue mathematical research indefinitely, pursue an
improvement aggressively, and commit/push validated checkpoints often.
This file is a handoff, not a completion claim.

Canonical main is still `fd6df02023122badbdd888803146f0bd92002214` at the
latest round refresh. The selected accepted result remains alpha `1/2`;
the accepted theorem and all upstream bytes are unchanged. Refresh main,
open PRs and advertised research branches before starting another round.

Owned completed checkpoint: [PR 3](https://github.com/1337isnot1337/3-SAT/pull/3),
branch `research/newton-parity-compression`, commit
`10e6eafc5fbf18325968218b7773e9175a11a4ef`. It includes the complete scalar
parity interface, cover valuations, sharp cutoff, actual-support lower
bound, and exhaustive reference checker. It credits the overlapping
`research/scalar-parity-lift` work. No bound improvement was selected.

Current branch: `research/parity-recovery-precision`. Initial pushed
checkpoint `8b98f92` proves the all-jet diagonal witness and its actual
unary-network realization. The next commit adds the matching `MD_i/u`
generic-polynomial witness, finite checks and this handoff. The Git log and
remote head, not a recursively embedded self-hash, identify that commit.

Run from the repository root:

```sh
python3 -I -B research/parity-recovery-precision/verify.py
make verify
```

The new all-size conclusion concerns a generic recovery interface, not a
SAT lower bound. The generic taper witness is not yet realized as a whole
growing-packet tensor family. The unary witness is actual but only gives
the `M/L` scale for growing packets. Do not conflate those scopes.

## Live research queue

1. Investigate which generic recovery witnesses occur as actual deformed
   contractions with creation-time canonical `0/1` lifts. Arbitrary signed
   tensor entries can change the later shifted polynomial when replaced by
   those lifts, although they preserve origin parity. Preserve this distinction.
2. Test a concrete alternative mechanism after refreshing PRs: aggregate
   incidence representations, a tensor-aware recovery, or a genuinely changed
   deformation. Merely reducing output precision or retuning a fixed taper
   does not close the exposed gap.
3. Keep input density, candidate queries, entry computations, random bits,
   decoding, maximum degree and the whole recursive budget explicit before
   claiming a new SAT time bound. Stop only at user direction or the actual
   goal constraints; these scoped packages do not complete the research goal.

Current outside work at the last read: PR 1 mode/taper functional bounds;
PR 2 weighted characteristic-two decision; PR 4 rational Newton modes;
PR 5 scalar parity and a construction comparison. Preserve their work and
credit overlaps. No agents were spawned in this session.
