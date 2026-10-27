# Three-bit macro crossing pieces and a finite-block obstruction

Status: `scoped_checked`; no improved SAT bound. The coarse and six-class
macro families are closed by all-size support obstructions.

Task: `contraction-schedule`. Base commit:
`8ba468df535d26bca9ee925e3d9bcb7179ffb0bb`.
Contributor: Cinna Davis, with substantial OpenAI Codex assistance.

## Question, changed premise and result

Break full binary-coordinate permutation symmetry by grouping three binary
coordinates into each macro-coordinate. The first model keeps three local
classes of sizes `(1,35,28)`. A local dual closes it. A six-class refinement
over F8 has sizes `(1,7,7,7,21,21)` and escapes that local certificate.
A four-macro certificate nevertheless closes the entire refined family.
The [previous global dual](../symmetric-walsh-pieces/SYMMETRY-BARRIER.md)
did not close these families. The new block theorem supplies that obstruction.
The accepted OpenAI theorem is a premise, not a correctness-audit target.

The [construction](CONSTRUCTION.md) gives uniform actual crossing pieces,
integer factors and weighted support ranks. The coarse screen covers
R=1,...,12; the six-class screen covers R=1,...,5. Both check the exact
transform, target sum, denominator clearing and word support costs. The
direct checker additionally verifies eight exact flattening ranks and
20,480 integer factor/crossing entries at R=1, and all 18,550 valid support
codes across the retained row and column factors at R=1,2.

The [local dual](SCHEME-REFINEMENT.md) forces some coarse-family piece to
have both supports at least `28^R`. The stronger
[finite-block tensorization theorem](BLOCK-BARRIER.md) forces some
six-class macro-type-constant piece to have both supports at least
`129654^floor(R/4)`. This permits any finite number of pieces, arbitrary
characteristic-zero coefficients and cancellations. It rules out the
target rate in that family, without extrapolating finite screen trends.

The original success target was a proved shared-bit bound below
`6 sqrt(2) R+O(log R)` for lambda=3R, followed by complete master-recursion
and density costs. Both families meet their stopping condition. Do not
extend their unchanged parameter screens.

## Cost and limits

For six classes there are `(R+5 choose 5)` types and at most that many
pieces. Each matrix coefficient has O(R) bits, by the local absolute-row-sum
bound 64. Determinant bounds give polynomial heights for elimination and
the common denominator. Construction, stored coefficients, type computation,
support unranking and individual factor entries all take polynomial time
and space in R. Enumerating all factor indices still costs exponentially
in lambda; their bit counts use actual word supports. The coarse case has
only `(R+2 choose 2)` types. Padding adds at most two input coordinates.

Neither family proves an improved rate, so no new master recursion or SAT
algorithm is asserted. Reduction branches, tensor descriptions, modes,
precision, recovery, density handling, space and randomness remain charged
exactly as in the selected baseline. No smaller count of types is substituted
for a word support or an algorithmic exponential cost. A successor needs
its own full composition of all those costs.

The obstruction covers functions invariant under the stated local classes
and all macro permutations. It is not a lower bound for arbitrary Pauli
functions, less symmetric pieces, arbitrary crossing tensors or SAT. The
local threshold seven alone was insufficient; the four-block dual was the
new mechanism. Written proofs are author-checked, with no independent or
formal review claimed.

## Reproduction

Standard Python only, offline. From repository root:

```sh
python3 -I -B research/three-bit-macro-walsh/certificate.py
python3 -I -B research/three-bit-macro-walsh/direct.py
python3 -I -B research/three-bit-macro-walsh/screen.py
python3 -I -B research/three-bit-macro-walsh/refined_screen.py
python3 -I -B research/three-bit-macro-walsh/block_dual.py
make verify
```

The first command verifies the frozen four-block witness without running
the search. The last research command replays the broader b=1,...,5 search
and is optional for validating the certificate. These bounded research
checks stay outside default CI. Hash-bound outputs are in `verification/`.
The search can take minutes; the frozen certificate replay takes seconds.

## Sources, credit and next premise

The Pauli/Walsh factorization and adapted-basis method are supplied by
[the predecessor](../symmetric-walsh-pieces/CONSTRUCTION.md), merged in
PR 14 at `8ba468df535d26bca9ee925e3d9bcb7179ffb0bb`. Its module is used
unmodified, with an exact hash guard. The new work is the three-bit class
refinement, finite-block dual and tensorization argument. Finite fields,
class character tables and symmetric powers are standard tools; no priority
claim is made for those tools. The external crossing-piece contract is
Anthropic's `def:genpieces`; pins and credit are in [SOURCES.json](SOURCES.json).
The external full theorem is not automatically accepted or selected here.

The next premise must change the local class invariance, global macro
permutation symmetry, or Pauli-diagonal representation. A candidate with
smaller local orbits may escape this witness, but that alone is no positive
result. Keep polynomial piece count and explicit integer factorization in
view before launching another screen. See [CHECKPOINT.md](CHECKPOINT.md).
New work is Apache-2.0. The accepted OpenAI source and selected bound are
unchanged.
