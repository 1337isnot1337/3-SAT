# Contributions and review

Start from [AGENTS.md](AGENTS.md) and [autoresearch.md](autoresearch.md).
The OpenAI baseline is accepted as true by owner instruction. Contributions
should improve or build on it; a baseline correctness audit is not needed.

Use one focused branch and one scoped research package. Preserve frozen
predecessors. Include the exact source commit and labels, a complete statement,
assumptions, the changed mechanism, cost accounting, reproduction commands,
actual evidence, limits, open next questions, and contributor credit.
`scripts/new_experiment.py` creates a draft without inventing results.

For an asymptotic improvement, give a uniform algorithm and a proof for all
permitted inputs. Account for reductions, branches and queries, coefficient
bit lengths, entry computation, recursive calls, decoding, space, and any
randomness. Keep arbitrary-density and fixed-density results separate. Prove
the finite-exception fallback and any parameter restrictions needed by the
changed construction. A hypothetical cost ledger does not establish that the
hypotheses can be achieved simultaneously.

Every randomized claim must meet the probability and worst-run time contract
in [docs/PROBLEM.md](docs/PROBLEM.md). Counting, decision, and search guarantees
must be distinguished. Polynomial space is a baseline property, not a mandatory
condition on every faster decision algorithm; state a space tradeoff explicitly.

Research package statuses are `draft`, `scoped_checked`, `reviewed`, `refuted`,
or `superseded`. `scoped_checked` means only that the named checks passed.
`reviewed` requires a written independent review naming its reviewer (including
whether AI assisted), reviewed commit, proof scope, commands and remaining
assumptions. A PR merge archives material; it does not automatically review a
proof or change the selected bound. Human review and formal verification must
be described literally, with evidence. Our owner-accepted baseline does not
change the Speedrun site's external evidence classification.

Only an authorized maintainer selects a new result. Update
`certificates/selected-result.json`, `docs/STATE.md`, the relevant task coverage,
and a written review together. An alpha increase needs a complete global cost
bound with alpha larger than `1/2`. A smaller logarithmic correction or leading
constant can still be retained with its precise statement.

Run `make verify` and any package-specific reproduction commands. Keep default
checks small and offline. Declare additional dependencies and bounded runtime
in the package; do not silently download tools or run all historical searches.
Record failures and the changed hypothesis that would justify another attempt.

Use original prose and retain source attribution. New contributions are under
Apache-2.0. Disclose substantial AI assistance. Do not claim priority from a
timestamp alone or invent a human review, independent replay, or formal proof.
