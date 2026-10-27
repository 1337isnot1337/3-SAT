# Mode and taper obstructions in the accepted contraction

Status: `scoped_checked`. **No improved SAT bound or larger alpha.**
The OpenAI theorem is accepted as true throughout. These new, author-checked
lemmas about proposed modifications have finite exact checks, but no
independent review or formal verification.

Task: `weighted-modes`, with a supporting `contraction-schedule` calculation.
Base: `3cebc0c307e8d680caa240c102643c35006318ae`.
Contributor: 1337isnot1337, with substantial OpenAI Codex assistance in the
derivations, implementation and writing. New material: Apache-2.0.

The question is whether stronger uniform mode weights, degree caps, an
invertible local basis change, or a different level-dependent taper can remove
the square root in Appendix D's enumeration estimate. Success would mean a
smaller exponent with representation and precision costs paid. The stopping
test was a matching obstruction within the proposed model. The latter was
reached, with the qualifications below.

The [proof](PROOF.md) establishes:

1. In the full-packet **formal** mode model, `2^Omega(M/sqrt(u))` squarefree
   exponent choices survive strengthening weight `b+1` to `a+1-i+b`, imposing
   total degree at most `M`, and imposing each packet's row-factor degree cap.
   This does not show that all those coefficients are nonzero in a SAT network.
2. For every nonnegative level-dependent multiplicity vector supported on
   `0,...,u-1`, the maximum normalized Hermite-product loss is at least
   `W/(4u)`, where `W` is total multiplicity divided by `L`. The exact real
   optimum is `W/(w^T B^-1 1)`. Thus this loss functional cannot become
   `o(M/u)` when interpolation requires `W=Omega(M)`. This does not lower-bound
   every possible recovery method, particularly one using cancellation.
3. The local Cauchy block `H[j,k]=1/(c+2(j-k))`, with `c` a two-adic unit, has
   Smith valuations `e_j=4j-2 popcount(j)`, including `e_0=0`. Their growth is
   linear, so invertible row/column basis changes cannot give this block a
   superlinear Smith spectrum. This is not a limit on all mode representations.

The second result gives an explicit optimal taper in the infinite-grid
relaxation, with loss asymptotic to `3W/u`. Conservative source choices leave
constant-factor room in this functional. No end-to-end constant improvement
is claimed; the remaining precision and runtime constants were not optimized.

## Complete cost and scope

No replacement contraction algorithm is supplied. The accepted arbitrary-density
bound remains `(n+m)^O_k(1) 2^O_k(n log log n / sqrt(log n))`; at fixed density
it remains `(n+m)^O_k,D(1) 2^O_k,D(n / sqrt(log n))`.

| Cost or interface | Treatment |
| --- | --- |
| Reduction branches and greedy queries | Accepted baseline; no change or saving claimed |
| Encoding, tensor descriptions, entries and decoding | No alternative implementation supplied |
| Modes | Lower bound for the named formal domain, not for nonzero contributions |
| Precision and recovery | Exact optimization of one product-loss functional; inherited precision and full recovery costs remain |
| Recursion and leaves | Accepted baseline; a geometric constant change alone leaves alpha unchanged |
| Bit operations, space and randomness | Exact integer/rational checker; no new SAT complexity guarantee or random bits |

These obstructions do not establish optimality of the accepted theorem.
Coefficient support, correlations between packets, cancellations, a new
deformation, or a different decision interface could still give an improvement.

## Evidence and reproduction

From the root, with Python 3.11 or newer, no additional dependencies:

```sh
python3 -I -B research/mode-taper-obstructions/verify.py
make verify
```

The package checker takes about one second on the authoring machine. Its
[saved output](verification.json) records all 14,097 Cauchy minors for dimensions
1 through 7 and shifts 1, 3 and 7, computed by exact Gaussian elimination;
eight exact primal/dual taper certificates through `u=64, a=128`; exact
convolution checks of the infinite-grid formula; 510 parameter cases for the
squarefree construction; and complete enumeration of a 256-tuple subfamily.
Displayed decimals are illustrative: all pass/fail comparisons are exact.
The checker also rejects a proposed quadratic Smith-weight lower bound at
index 4. The all-size claims depend on the written proofs, not extrapolation.

## Handoff

Do not repeat these unchanged elementary optimizations as open mechanisms.
A next mode attempt should identify a constraint on **nonzero coefficients
or their joint contraction** that excludes the squarefree witness family,
or aggregate the terms without enumeration. A recovery attempt must change
the loss functional, for example by proving cancellation in combined Hermite
coefficients. A new local kernel needs its own integrality, locality, recovery
and recursion arguments. The unresolved objective is a complete improvement
on the accepted all-input bound.

An exploratory checker first used too small a packet parameter for its own
side condition, then tried to print an enormous count in decimal. The final
check uses admissible parameters and records counts as `2^N`. These were
checker setup failures, not counterexamples; no failed output is evidence.

## Sources and overlap

Credit OpenAI's accepted construction, commit
`7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`. The frozen
[contraction source](../../upstream/openai-eth-2026/build/quantitative-contraction.tex)
has SHA-256 `671642d7b53154d92344e8c4be0240f18929632ebcfdf73b07c3e9939b873860`.
Labels: `eq:tensor-mode-expansion`, `eq:tensor-mode-multiplicity`,
`eq:tensor-mode-budget`, `eq:tensor-partition-count`, `eq:tensor-hermite-loss`,
`lem:tapered-hermite`, and `eq:tensor-precision-bound`.
The [manifest](../../SOURCES.json) supplies provenance and licenses. The
[baseline cost model](../baseline-cost-model/README.md) supplies the repository's
local-change versus alpha-gain distinction.

At the initial canonical-main pin the only package was the baseline cost model,
with no open Issues or PRs. The live 3-SAT board also had no posts. These are
overlap observations, not a priority claim.
