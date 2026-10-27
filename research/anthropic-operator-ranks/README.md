# Exact ranks of the Anthropic operator pieces

Status: `scoped_checked`. AI-assisted and not independently reviewed.
No improvement to alpha or the selected time envelope.

Task: `contraction-schedule`. Base commit: `fd6df02023122badbdd888803146f0bd92002214`.

Contributor: OpenAI Codex (AI-assisted). Disclose substantial AI assistance.

## Question and changed premise

The user supplied [Hexagon 2610.00577v1](https://hexagonmath.org/2610.00577v1).
It states the same alpha=1/2 as the accepted OpenAI baseline, using a
different construction. This round changes the research mechanism to
its Appendix-B operator pieces rather than adjusting Cauchy/Hermite
parameters. The external theorem is not assumed or selected here.

Question: do the actual row/column flattening ranks of its small
pieces leave substantial slack in the stated partition-space bounds?
The relevant source labels are `eq:ops`, `eq:Q`, `lem:dual`,
`eq:half-row`, `eq:half-col`, `thm:halfpieces` and `thm:master`.

## Statement and scope

Start with lambda=1,2, then lambda=3 if the exact operator construction
is feasible. Compute every piece as an integer tensor and check both
operator orders and the crossing identity. Use exact rational ranks
for small matrices; modular ranks alone are lower bounds. They do not
establish characteristic-zero upper bounds or an asymptotic gain.

Success is a proved smaller-rank representation with a uniform
factorization and a paid full recursion budget. A finite rank gap is
only a lead. Stop an unchanged screen after exact saturation or after
the finite scope is clear; then change the construction or isolate a
specific image-space identity to prove.

## Complete cost

For this paper's piece contract, improving rho below 1/sqrt(2) could
improve alpha under its master recursion. Both integer factorizations,
piece count, integer heights, evaluation cost, grouping and dense
reduction must remain feasible. No such full improvement is claimed.

## Evidence and reproduction

The pinned [source](source/README.md) is available offline and checked by
hash. The [operator module](operators.py) implements the recurrence O2
and a separate direct normal-ordered definition for finite cross-checks.
The [saved screen](verification.json) covers all pieces at lambda=1,2,3,
with respective energies h=2,4,6. It computes exact rational ranks:
modular ranks certify exactness only when they match a separate proved
upper bound, and every remaining case uses rational elimination. A
bad-prime control explicitly rejects using a modular rank as an upper
bound. There are 13 strict rank gaps in total, but none saves an index
bit relative to the capped formal bounds at these sizes.

The screen found a first-moment relation that has an all-size
[normal-ordering proof](PROOF.md): `sum_s s A_s=0`. Consequently the
pieces `(1-s) A_s` for s different from 1 give the same crossing
identity with the same denominator h!, using 4h pieces instead of
4h+1. Integer factorizations and their shared-bit counts are preserved.
This is a component reduction in piece count, not a smaller rho.

| lambda | h | Original pieces | Retained pieces | Tensor span rank | Worst shared-bit total |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 9 | 8 | 8 | 4 |
| 2 | 4 | 17 | 16 | 16 | 8 |
| 3 | 6 | 25 | 24 | 24 | 12 |

The finite span ranks also show that, within scalar reweightings of
these fixed tensors, at most one piece can be eliminated and the
central piece must retain coefficient one. This finite conclusion is
not asserted for arbitrary h or for changed pieces.

Reproduce with Python 3 and the standard library:

```sh
python3 -I -B research/anthropic-operator-ranks/screen.py
make verify
```

The bounded screen checks 196 independent direct-normal-order versus
recursive operator evaluations; 217 more general homogeneous
first-moment cases; 13,960 full output-vector comparisons of the two
operator orders; and all 4,368 entries of each crossing, first-moment
and pruned-crossing identity. It also verifies the full-state dual
pairings at h=2,4,6, not just the chosen binary code states. Its last
run took 45.74 seconds and about 253 MiB peak RSS on this host. This
is checker cost, not a SAT speed result. The screen is separate from
default CI; `make verify` remains lightweight.
A clean Git-free export reproduced the full saved screen byte for byte;
the exact checkpoint and scope are in [VALIDATION.md](VALIDATION.md).

## Limits and open next questions

The all-size relation awaits independent review. The one-piece reduction
does not change the dominant shared-bit bound, and the tested finite
rank gaps do not lower the bit counts. The next round needs a changed
factorization or recovery, rather than pruning another piece by an
unproved linear relation. [HANDOFF.md](HANDOFF.md) records possible next
questions and the user's failed-route reports to avoid repeating.
No Lean development or SAT solver has been run.

## Sources and credit

Anthropic's paper is CC BY 4.0; exact source hashes and attribution are
in [SOURCES.json](SOURCES.json) and [source/README.md](source/README.md).
The comparison was first recorded on
[PR 5](https://github.com/1337isnot1337/3-SAT/pull/5).
The accepted OpenAI source remains at
`7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a` and is not audited here.
All new reasoning and code are AI-assisted; no independent review or
scientific-priority claim is made.
