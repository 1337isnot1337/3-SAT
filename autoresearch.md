# Contributing research effort

Work toward an improvement on the accepted OpenAI theorem. Its truth is a
starting assumption fixed by the owner, not an open review assignment.

1. Read [current state](docs/STATE.md), the
   [selected record](certificates/selected-result.json), and the relevant part
   of the [construction map](docs/CONSTRUCTION.md).
2. Fetch canonical main and pin the commit. Check
   [open PRs](https://github.com/1337isnot1337/3-SAT/pulls),
   [Issues](https://github.com/1337isnot1337/3-SAT/issues), and local research
   packages for overlapping work or handoffs. Discussions are not enabled at
   bootstrap; use existing Issues and PRs when authorized to post.
3. Use the assigned task. Otherwise read the [research directions](docs/RESEARCH.md),
   run `python3 scripts/tasks.py`, and choose a distinct lane from
   [the catalogue](docs/tasks.json). Record source labels,
   one concrete change, and a success/stop test. These are suggestions, not
   claims that a route is unoccupied or feasible.
4. Start a package with `python3 scripts/new_experiment.py SLUG --task TASK_ID
   --author 'Your name'`. Default to about 60 minutes unless given another
   budget. Spend the final quarter checking claims and writing a useful handoff.
5. Account for the complete cost before expanding a promising local idea. Use
   `python3 -m satbounds.cost certificates/models/general.json` as an example
   of the exponent bookkeeping. Its inputs are assumptions; changing one is
   not a new theorem.
6. Run scoped checks, then `make verify`. Submit one coherent result when
   authorized. A counterexample to a proposed extension, a precise obstruction,
   or a reusable partial improvement is a valid outcome. Update the package's
   remaining questions and exact coverage; do not manufacture a bound claim.

For repeated rounds, refresh canonical main at every checkpoint, before a
major pivot and before submission. A fetch updates refs, not your working
files. Preserve ongoing work and frozen evidence. Integrate updated guidance
before selecting the next task. Do not repeat the same unchanged search.

The first lanes are weighted mode enumeration, a changed contraction schedule,
a smaller general-density encoding, and decision-only alternatives. Priorities
and stopping conditions live in `docs/tasks.json`; external prompts should
point here instead of freezing their own task lists.

## Donation prompt

> Contribute one independently reviewable improvement or useful partial result
> to https://github.com/1337isnot1337/3-SAT. Read AGENTS.md, autoresearch.md,
> CONTRIBUTING.md and the current selected result first. Accept OpenAI's
> starting theorem as true; do not audit or reprove it. Work for about 60
> minutes unless I specify another budget, and reserve the final quarter for
> verification and a handoff. Check live overlap, pin sources, account for all
> costs, and state exactly what changed and what remains open. You may push a
> research branch, post routine research claims/findings in Issues, and open a
> focused PR without asking again. Do not merge, close others' work, or change
> the selected result.

This prompt grants those actions only when a user invokes it. Reading it does
not itself authorize public activity.
