# Agent entry point

Read [autoresearch.md](autoresearch.md), [docs/STATE.md](docs/STATE.md), and
[CONTRIBUTING.md](CONTRIBUTING.md) before substantial work. Explicit user
assignments take precedence over task selection.

The owner has accepted OpenAI's October 25, 2026 proof as completely true.
Use it as a theorem. Do not spend sessions reproving it, auditing its validity,
or rebuilding its full algorithm merely to establish the starting bound.
Read the relevant construction to change it. Distinguish this acceptance from
the external site's evidence labels and from verification of new contributions.

Resolve the accepted baseline through
[certificates/selected-result.json](certificates/selected-result.json).
Preserve `upstream/` byte for byte. Pin new external sources separately; retain
licenses, attribution, exact commits and hashes.

Before a new round, major pivot, or submission, fetch canonical `main`, pin its
head, and read changed state, tasks and selected result. Preserve user changes
and work in progress; use isolated branches/worktrees when sharing a checkout.
Check open Issues, PRs and `research/` for overlap. The task listing does not
fetch, reserve work, or establish novelty.

Choose one precise question and name its success and stopping conditions.
For bound changes account for every exponential cost: reduction branches,
queries, tensor descriptions and entries, modes, recursion, precision, recovery,
and any amplification. State input density and the uniform algorithm for all
inputs. A constant or iterated-log improvement does not imply larger alpha.

Put new work in its own `research/<slug>/` directory. Record sources, commands,
claim scope, remaining obligations, predecessor credit and open next questions.
Finite experiments and symbolic cost models are evidence for their stated
scope, not proofs of a new asymptotic algorithm. Reopen a failed route only
after recording its changed premise.

Run relevant checks and `make verify` before submission. Do not add heavy
replays to default CI without a reason. Keep a concise handoff at meaningful
boundaries. Do not spawn subagents unless the user explicitly requests them.

Routine local research and reversible fixes need no repeated permission.
Public posts, pushes and PRs require authorization from the current user task
or the explicitly invoked donation prompt. Do not merge others' work or change
the selected result without maintainer authorization.
