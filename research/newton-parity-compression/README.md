# Scalar parity compression of sparse queries

Task: `dense-encoding`. Status: `scoped_checked`; AI assisted and not
independently reviewed. No improved asymptotic SAT bound or selected result.

The positive change is an exact Boolean parity lift in the scalar ring
`Z/2^p Z`. It replaces the source's `p`-coefficient truncated-polynomial ring
and sharpens the retained incidence-degree bound from `k(a+2p-2)` to
`k(a+p-1)`, for `a` tests of degree at most `k`. At exact-counting precision
`p=n+1`, this saves `kn` in the proven cutoff. A stored coefficient-algebra
element has `p` bits instead of `p^2` bits under the respective dense modular
representations. These are representation and cutoff improvements; no
unspecified big-O runtime constant is compared.

The [proof](PROOF.md) also gives distinct sparse nonlinear equations with
`(floor(log_2 n))^n` actual nonzero incidence coefficients. An information
bound then shows that removing zero coefficients alone cannot improve the
`Theta(n log log n)` wire order in the one-monomial-per-code architecture.
Aggregation, cancellation after identifying variable copies, and different
algorithms remain open.

## Question, success and stopping conditions

The changed premise is the coefficientwise power-of-two divisibility of the
elementary-symmetric expansion of parity in the listed monomial values.
Success for this scoped round is a proved smaller explicit cutoff and a
complete valid scalar contraction interface with exact finite reference
checks. The full target remains a uniform general-density improvement.
Stop claiming more when the retained-code entropy still has order
`n log log n`. A new round must change that representation, not repeat
zero-coefficient pruning on the same incidence family.

## Reproduction and actual evidence

From the repository root, Python 3.11+ with only the standard library:

```sh
python3 -I -B research/newton-parity-compression/verify.py
make verify
```

The scoped checker takes seconds on this host. It is a small exponential
reference experiment, not the accepted fast contraction algorithm. Saved
output is [verification.json](verification.json), including proof, checker
and frozen-source SHA-256 hashes. Its actual finite coverage is:

- All 32,768 four-variable algebraic-normal-form polynomials of degree at most
  three, including constants: 524,288 exact integer-coefficient comparisons
  between direct Boolean Mobius inversion and an independent product expansion;
  303,546 nonzero-coefficient valuation and exact-cover checks.
- All 16,384 ordered pairs of three-variable degree-at-most-two polynomials,
  at precisions `p=1,...,4`, plus explicit boundary fixtures: 65,573 modular
  count comparisons, with 31,466 omitted coefficients checked to vanish.
- The actual binary network construction on six tiny systems at all
  `p=1,...,n+1`: 1,494 degree arrays, 26,117 wire assignments, 5,266 invalid
  codes returning zero, and 25 modular counts. It includes empty systems,
  constant equations, zero-wire pairs, and unused variables.
- Independent lexicographic subset-decoding checks through ten incidences:
  2,047 valid codes, 528 invalid codes and 21 zero-wire cases.
- 735 exact CNF comparisons against the repository's exhaustive reference,
  including repeated literals, tautologies, empty clauses, empty formulas,
  zero variables, and unused declared variables.
- 60 sharp-cutoff certificates and four distinct-equation cyclic nonlinear
  fixtures, exhausting 591,130 unit-coefficient incidence monomials.

The written asymptotic proofs are separate from that finite evidence. No
human review, formal proof, scientific priority, or independent replay is
claimed. The scoped checker is deliberately outside default CI.

## Complete cost and remaining gap

[PROOF.md, Section 3](PROOF.md#3-encoding-entries-and-complete-cost) accounts
for normalization, high-incidence branches, arrays, invalid codes, descriptions,
entries, scalar precision, contraction, unused variables, and exact recovery.
It retains all queries in the accepted greedy reduction, including rejected
candidates. General-density time remains
`poly(n+m) 2^O_k(n log log n/sqrt(log n))`, with polynomial space and
`alpha=1/2`. Fixed density retains the accepted sharper clause-network route.

The next concrete target is a code for *aggregates* of incidence monomials
whose entry computations still satisfy the contraction theorem. It must
handle the cyclic family and all arbitrary sparse queries, not only chosen
hash rows or easy linear equations. The scalar lift and exact reference
checker are reusable starting points. The accepted selected-result record
and all upstream files are unchanged.

## Pins, credit and overlap

- Canonical main at the start: `fd6df02023122badbdd888803146f0bd92002214`.
- Accepted OpenAI source commit:
  `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`, pinned in
  [SOURCES.json](../../SOURCES.json). The theorem is accepted as true.
- Changed source interface: `lem:tensor-sparse-query`,
  `eq:sharp-incidence-degree`, `eq:sharp-wire-budget` and `subsec:sharp-dense`
  in the [quantitative reduction](../../upstream/openai-eth-2026/build/quantitative-reduction.tex).
- Reused accepted theorem: `thm:tensor-contraction` in that same file;
  parity-lift comparison: `lem:rational-idempotent` and `lem:total-order`
  in the [full source](../../upstream/openai-eth-2026/build/main_full_version.tex).
- Live overlap read before the round: no open Issues; [PR 1](https://github.com/1337isnot1337/3-SAT/pull/1),
  head `8790b8e14e08ea14f75c2bd6eecfdbc70fe97770`, studies mode, taper and
  local Cauchy-basis obstructions. This package concerns the separate
  sparse-query coefficient and encoding interface. No edits to that work.
- Refresh before the first push found the concurrent
  [scalar-parity-lift branch](https://github.com/1337isnot1337/3-SAT/tree/ca0a7f5beaedcadbbc1fbadfae6271ecf582b2e6/research/scalar-parity-lift)
  at `ca0a7f5beaedcadbbc1fbadfae6271ecf582b2e6`. It independently records
  the same scalar projector and degree cutoff. Those are overlapping results,
  not a separate novelty claim here. This companion adds the exact-cover
  strengthening, full composition, sharpness and actual-support information
  bound, with its separately written exhaustive checker. The concurrent
  branch is preserved. [PR 2](https://github.com/1337isnot1337/3-SAT/pull/2),
  head `887e662368200c79a8ee870603e1cf6a451108e5`, studies a distinct weighted
  characteristic-two decision interface and also leaves wire entropy open.
- Contributor: Cinna Davis, with substantial OpenAI Codex assistance in the
  proof, code, verification and writing. New material is Apache-2.0.

The parity identity is elementary and no novelty claim is made for the
identity itself. Credit for the accepted contraction, sparse-query encoding,
and outer reduction belongs to OpenAI and the predecessors cited in its
frozen paper. This package records the specific scalar replacement and its
scoped consequences.

Subsequent [PR 5](https://github.com/1337isnot1337/3-SAT/pull/5) reports the
same projector coefficients and total-selection truncation in Appendix D of
Anthropic's *A 2^{o(n)} Time Algorithm for 3-SAT*, Hexagon 2610.00577v1.
Its separately pinned comparison gives that direct predecessor credit.
That paper is not a proof dependency here; retrieval of its source in this
checkout returned HTTP 403, so this package does not claim a primary-source
replay of the comparison. The local identity, cutoff and support proof above
are self-contained. Neither concurrent scalar package establishes novelty
of the projector mechanism.
