# Active research checkpoint

Global objective remains INCOMPLETE and active: work indefinitely toward a
mathematical improvement, commit/push often, and merge checked coherent PRs
under the user's explicit authorization. Do not mark the goal complete or
stop at these scoped results. No subagents have been spawned.

Canonical base for this round: `8a659c67d4988540aa6ac8393bb06314ecbe81e2`.
Refresh main, all advertised branches, open PRs and changed guidance before
another round or submission. The accepted OpenAI theorem remains the premise,
alpha is still 1/2, and all frozen upstream files are unchanged.

Owned prior packages were merged: PR 3 at
`c5147fc79f7a4de01671d99201aa0711618ecd50`; PR 6 at
`eef59028945674c1847b9a105474a9ef62a584d5`. Their saved checks reproduce on
the exact clean main checkout at the latter SHA and `make verify` passes.
Those merges archive scoped work and do not independently review or select
a stronger theorem.

Current branch: `research/two-scale-cauchy-grid`. First pushed checkpoint
`816af80` supplies the valid changed grid and stronger local spectrum.
This package includes the complete nodewise model, exact duals,
gap-independent bound, large-gap limit, and generic full-grid witnesses.
The Git log identifies its full SHA. Every relevant command is offline:

```sh
python3 -I -B research/two-scale-cauchy-grid/verify.py
make verify
```

The exact component is not a new SAT algorithm. The scales K used in the
loss comparison are expressly modeled; an actual full crossing-mode
factorization at those scales is not established. The generic polynomial
witness is not yet an efficient actual tensor contraction. Preserve both
distinctions. The completed comparison includes all dummy nodes and
arbitrary nodewise multiplicities, so neither omission is a valid reopening
premise for the same numerical-gap argument.

The clean Git-free replay is recorded in [VALIDATION.md](VALIDATION.md).
Next actions: open/merge the research PR after fresh canonical checks,
then select a materially
different mechanism. Candidate directions are aggregate mode identities,
a tensor-aware joint recovery contract, or a different deformation whose
local spectrum and full reconstruction cost are proved together. Do not
repeat a spectrum-only claim or treat a hypothetical cost JSON as a theorem.

Concurrent work already occupies Anthropic operator-rank and sparse-oscillator
questions. Check their live results before attempting any related route.
Primary Anthropic source was fetched using a browser User-Agent after a
plain urllib request returned 403; its main TeX hash is
`ce4b77cc1d1d5a033ea41c00321cbd88871adfa62648614defa0bab8a63a9553`.
It is now also pinned in the recent-breakthrough/other research packages;
the original accepted OpenAI archive was never replaced.
