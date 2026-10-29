# Active bound attempt: length-block charged filters

**Goal incomplete. No improved SAT bound yet.** This package is a working
checkpoint, not a submission of another component as completion.
Coordination: issues #148 and #23. Base c600b21ee7800a49c05718a254be50168e6b355b.
Substantial OpenAI Codex assistance; new material Apache-2.0.

The target is a uniform crossing supported on |s|>h/2, retaining leading
partition capacity in both inputs and outputs. With the predecessor rank
and rational-transfer contracts, this would replace rho=1/sqrt(2) by
(sqrt(5/2)+sqrt(3/2))/4 and yield a strictly larger alpha. That conclusion
requires an all-size existence and cost proof; the current finite evidence
does not establish it.

The changed premise is independent projection onto each row-length and
column-length block, before choosing a charge/shift filter. Both projections
are local on each required rank cut. There are only polynomially many such
blocks, so this does not introduce an exponential piece count. The original
first-moment pairing is block diagonal between row length l and column length
l-1. Independent block filters are more general than a common weight after
rescaling by the SUM of the two lengths.

Exploratory exact results:

- Grade 8: all blocks of the canonical rank-seven first-moment input minor
  recover that pairing with |s|>4 on the entire 22-state output space.
- Grade 10, length-four/length-three block: the prescribed first-moment
  pairing is absent in the modulo-65521 screen, but a DIFFERENT invertible
  three-by-three scalar pairing exists over Q with |s|>5 on all 42 output
  states. The script solves and verifies its rational nullspace equations
  and exact nonzero determinant. Thus the missing particular moment does
  not refute the crossing goal. No rational non-membership claim is made
  from a modular rank discrepancy alone.

The h=6,8 reports were produced by the initial exact first-moment solver
in this investigation. The current `probe.py` additionally constructs a
rational scalar pairing even when the prescribed target is unavailable;
its complete output need not byte-match those earlier exploratory reports.
It is an exploratory tool, not an independent operator oracle. All operator
values come from the pinned predecessor recurrence. Only the stated finite
spaces and grades have been checked.

Current command (Python 3.11+, python-flint 0.9.0 installed in the isolated
local environment /tmp/3sat-bound-env):

    /tmp/3sat-bound-env/bin/python -B research/length-block-filter/probe.py 10 5 4

Arguments are grade, central cutoff, and optional row length. No large replay
is added to default CI. The full output tables grow exponentially in sqrt(h),
so arbitrary additional grades are not a substitute for the missing proof.

Next mathematical obligations: characterize the scalar matrix space for
all h after these length projections; exhibit an invertible minor of leading
partition capacity; give uniform selectors and rational bit-height bounds;
then compose both directional ranks, field transfer, outer decision reduction,
all random failure budgets and the full recurrence. A bound change will not
be asserted before these are settled. No selected-result edits are made.

Credit: `charged-operator-moments` supplies the charged identity and exact
first-moment rank; `charged-asymmetric-crossing` supplies the asymmetric
minor and local inverse; `charge-polynomial-filter` and `length-power-filter`
supply the exact coefficient recurrence and earlier scalar-span tests;
`charge-capacity-tradeoff` supplies the charge/label-capacity limitation;
`extreme-shift-output-rank` bounds the possible support-only improvement.
These predecessors remain unchanged. The accepted OpenAI theorem remains a
premise, with frozen source commit 7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a.

The active extension is described in [LEFT-MODULE.md](LEFT-MODULE.md):
shift-dependent local input maps recover the entire scalar row space in
finite tests, rather than a chosen length-block pairing. The uniform
containment and full SAT bound remain unproved.
