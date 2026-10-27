# Nodewise taper loss: exact symmetrization

Status: `scoped_checked` for the named checks; written proofs are author-checked
and await independent review. **No improved SAT bound or larger alpha.**

Task: `contraction-schedule`. Base `fd6df02023122badbdd888803146f0bd92002214`.
Contributor: 1337isnot1337, with substantial OpenAI Codex assistance. Apache-2.0.
The OpenAI theorem is accepted as true.

The changed premise is to assign multiplicities independently to every nonzero
interpolation node, rather than requiring equal multiplicities at equal
two-adic valuation. This tests a loophole left by the level-dependent analysis
in [PR #1](https://github.com/1337isnot1337/3-SAT/pull/1), pinned predecessor
`8790b8e14e08ea14f75c2bd6eecfdbc70fe97770`.

The [proof](PROOF.md) establishes an exact optimum for a normalized nodewise
loss functional that includes the highest-jet evaluation term. For any real
nonnegative multiplicities supported on valuation levels `0,...,u-1`, with
total mass divided by `L` at least `W`, the optimum is

```math
 \frac{W}{w^T B_+^{-1}\mathbf1},\qquad
 \frac{W}{2u}\le\frac{W}{w^T B_+^{-1}\mathbf1}\le\frac{9W}{u}.
```

A maximum principle handles inactive nodes; averaging over odd residue
multiplication proves that a level-symmetric optimum exists. The ordinary
Hermite formula's highest-jet coefficient then has normalized loss at least
`W/(2u)-1` at some active node for integer multiplicities. The degree condition
requires `W=Omega(M)`, leaving the `M/u` scale intact.

A separate construction strengthens the generic recovery obstruction. For
`M>=16u`, it gives a degree-at-most-`M(2L-1)` rational polynomial with value
one at zero, integral coefficients on every source chart, and **every** Taylor
coefficient on each retained chart zero modulo `2^floor(M D_t/(8u))`.
Even joint access to all these coefficients cannot distinguish it from zero.
This excludes uniformly smaller generic precision using only the degree and
chart-integrality hypotheses. It does not prove that the witness polynomial
is realizable by a tensor network or a SAT reduction. Structure of the actual
deformation polynomials remains a concrete possible escape.

Success would have meant an `o(M/u)` loss within this changed family; the
matching-order obstruction met the stopping condition. Reopen only with a
proved extra structure of actual deformation polynomials, new nodes/kernel,
or a mode-aggregation mechanism. Merely making the same multiplicities
node-dependent is no longer an untested route.

## Complete cost boundary

No SAT algorithm is changed. Reduction branches, query counts, encoding,
tensor entries and descriptions, recursion, leaves and amplification retain
the accepted costs. The local functional optimum does not certify a smaller
runtime, independent of how its constants compare. The accepted general
exponent `O(n log log n/sqrt(log n))`, fixed-density exponent
`O_D(n/sqrt(log n))`, and alpha `1/2` remain unchanged.

## Checks

```sh
python3 -I -B research/nodewise-taper-loss/verify.py
make verify
```

The standard-library checker takes under a second on the authoring machine.
[Saved output](verification.json): 17,111 nonzero multiplicity vectors checked
exhaustively; ten exact primal/dual certificates through `a=128,u=64`; 68 lifted
full-node dual identities; and 18 highest-jet coefficients computed as actual
rational products; and two explicitly expanded generic witness polynomials,
with all 24 shifted charts checked coefficient by coefficient. Displayed
decimals are illustrations only; all pass/fail
checks are exact. These checks support their finite scope, not independent
review of the all-size argument or a contraction implementation.

Credit the accepted OpenAI construction, commit
`7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`,
[contraction source](../../upstream/openai-eth-2026/build/quantitative-contraction.tex),
labels `lem:tapered-hermite`, `eq:tensor-hermite-origin`,
`eq:tensor-hermite-loss`, and `eq:tensor-precision-bound`.
The source SHA-256 is
`671642d7b53154d92344e8c4be0240f18929632ebcfdf73b07c3e9939b873860`.
Licensing and full source pins are in [SOURCES.json](../../SOURCES.json).
PR #1 supplies predecessor context; this proof includes the new argument in full.
No priority or external evidence-level claim is made.
