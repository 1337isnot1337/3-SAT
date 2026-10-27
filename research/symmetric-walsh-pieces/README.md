# Symmetric Walsh pieces and a global support barrier

Status: `scoped_checked`, AI-assisted and not independently reviewed. This
supplies a uniform crossing construction and a global obstruction to its
symmetry class. No improved piece rate, SAT time or alpha is claimed.

Task: `contraction-schedule`. Base commit: `4ec0e136b819b7d12fedf72ad2f8286098c6f4a7`.

Contributor: Cinna Davis, with substantial OpenAI Codex assistance.

## Question and changed premise

Represent a crossing tensor using real Pauli matrices. For a coefficient
function f on `(F_2)^(2 lambda)`, its row and column flattening ranks are
the supports of f and its Walsh transform, respectively. The crossing
corresponds to the quadratic sign `q(a,b)=(-1)^(a dot b)`. Can q be split
into polynomially many explicitly computable pieces whose two support
logarithms sum to less than `2 sqrt(2) lambda` asymptotically?

The first family is invariant under simultaneous coordinate permutations.
It has only `binom(lambda+3,3)` orbit types, and the Walsh transform acts
by an exact symmetric-power matrix. An adapted basis for the two support
filtrations gives an actual uniform crossing decomposition, rather than
a hypothetical rank envelope. The accepted OpenAI theorem is a premise;
this is a new piece-construction attempt motivated by the external paper.

## Statement and scope

The [construction](CONSTRUCTION.md) supplies actual integer crossing pieces,
with polynomial piece count and coefficient heights and `2^O(lambda)`
entry evaluation. Both flattening ranks are exact support counts. The
registered first screen covers lambda=1,...,8, with direct rational matrix
ranks and both explicit factorizations at lambda=1,2. No randomness or
floating rank decisions are used.

The [global dual](SYMMETRY-BARRIER.md) is stronger than that finite screen.
For every decomposition into permutation-symmetric Pauli-diagonal pieces,
one piece has both supports at least
`lambda!/((lambda-3k)!(k!)^3)`, `k=floor(lambda/8)`.
Its necessary asymptotic rho is at least
`3/2-(5/16)log2(5)`, about 0.7744, above the accepted `1/sqrt(2)` target.
The proof permits arbitrary coefficients, cancellations and any finite
number of summands. It does not cover general nonsymmetric or non-Pauli
pieces. An explicit nonsymmetric singleton control demonstrates that limit.

Success for the full objective needs a proved all-size shared-bit rate below
`2 sqrt(2) lambda+O(log lambda)`, integer factors, polynomial piece count and
coefficient bit lengths, and evaluation in `2^O(lambda)` with fixed constants.
Finite support ratios alone do not establish that rate or a SAT improvement.
The global obstruction meets the stopping condition for this symmetry
class; larger scans of the same class cannot meet the target.

## Complete cost

The operator-piece contract is `def:genpieces` in Anthropic's pinned source,
identified by [the scan](../recent-breakthrough-scan/SOURCES.json) and
[the operator package](../anthropic-operator-ranks/SOURCES.json).
The new Pauli/Walsh factorization will be proved independently. Even a smaller
piece rate needs the master recursion, descriptions, integer heights,
normalization and arbitrary-density reduction charged. The external theorem
is not automatically selected or treated as owner-accepted by this experiment.
For the candidate, clearing denominators with a common D and multiplying by
`D 2^(2 lambda)` gives integer row and column factors. The actual piece
support counts determine the shared bits; the trivial all-size upper rate
is only `4 lambda`. The global lower rate rules out the desired improvement
in the stated class before a full SAT algorithm can be claimed. The selected
OpenAI result and all frozen sources are unchanged.

## Evidence and reproduction

Python 3.11+, standard library, from the repository root:

```sh
python3 -I -B research/symmetric-walsh-pieces/screen.py
make verify
```

The [saved output](verification.json) binds the written proofs, code and source
base. It checks all compressed transforms, eigenvectors, exact piece sums,
denominator clearing and support counts for the following full finite range:

| lambda | Type dimension | Pieces retained | Worst shared-bit total |
| --- | --- | --- | --- |
| 1 | 4 | 4 | 2 |
| 2 | 10 | 6 | 4 |
| 3 | 20 | 15 | 6 |
| 4 | 35 | 27 | 13 |
| 5 | 56 | 43 | 14 |
| 6 | 84 | 65 | 20 |
| 7 | 120 | 96 | 24 |
| 8 | 165 | 134 | 27 |

The first three cases' `2 lambda` cost is a false asymptotic lead. All
retained pieces at lambda=1,2 additionally pass 20 exact rational flattening
ranks and 1,872 direct factorization/crossing-entry checks. The dual checker
constructs 25 symbolic witnesses through lambda=32 and checks 327,680
individual full-word Fourier eigenidentities at lambda=8,9. It rejects an
incorrect orbit normalization, verifies the nonsymmetric singleton controls,
and checks exact macro-alphabet entropy inequalities and 4,096 direct
three-bit macro character sums. These finite checks do not independently
review the written all-size proof or implement the full contraction.

## Limits and open next questions

The obstruction also tensorizes over a fixed number of growing color
classes. A macro-alphabet version rules out two-bit macro-coordinate
permutation symmetry, by a close but exact entropy inequality. Its three-bit
analogue falls below the target and therefore leaves a different premise
open. A concrete next construction uses macro classes with multiplicities
`(1,35,28)` and Walsh matrix `[[1,35,28],[1,3,-4],[1,-5,4]]`.
That is an identified unblocked family, not an achieved rate. Its actual
factors, bit counts and eventual support bound still need to be proved.
See [CHECKPOINT.md](CHECKPOINT.md) for the continuation queue.

## Sources and credit

Accepted OpenAI source commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`,
unchanged. Anthropic source main TeX SHA-256
`ce4b77cc1d1d5a033ea41c00321cbd88871adfa62648614defa0bab8a63a9553`,
labels `def:genpieces`, `thm:master`, `eq:half-row`, `eq:half-col`.
Prior rank screens and operator-moment work are separate and preserved.
The present support/Fourier construction is not claimed scientifically novel;
it is a self-contained changed mechanism to test. New material is Apache-2.0
with substantial OpenAI Codex assistance. No independent review is claimed.

Standard Pauli/Walsh relations are prior background; see Georges et al.,
[*Pauli Decomposition via the Fast Walsh-Hadamard Transform*, v4](https://arxiv.org/abs/2408.06206v4).
Its PDF/version/license and the primary piece-contract source are pinned
separately in [SOURCES.json](SOURCES.json). The local rank identities,
integer coding and support dual are proved in full here. No scientific
priority is claimed for the background transform or the adapted-basis method.
