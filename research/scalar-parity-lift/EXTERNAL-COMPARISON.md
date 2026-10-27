# Relevance of Hexagon 2610.00577v1

The user supplied [Anthropic's paper](https://hexagonmath.org/2610.00577v1)
during this round. Its title is *A 2^{o(n)} Time Algorithm for 3-SAT*,
version 1, October 27, 2026. The source archive and main TeX file are
independently pinned in [EXTERNAL-SOURCES.json](EXTERNAL-SOURCES.json).
The landing page licenses the paper CC BY 4.0. This file contains our
comparison, not a copied or modified paper. The external result is not
a dependency of the scalar parity-lift proof and is not automatically
selected or owner-accepted by reading it.

## What it states

Its main theorem, `intro:thm:strong`, gives deterministic exact counting
in time

```math
 2^{O(\min\{k^2n\log\log n/\sqrt{\log n},\quad
                       km/\sqrt{\log m}\})},
```

with an absolute implicit constant. It counts the variables that occur;
declared unused variables can be handled separately when comparing to
this repository's input contract. For fixed k, it has alpha 1/2, the same
general-density logarithmic correction, and the same square-root saving
at fixed density as the accepted OpenAI baseline. Its stated theorem
does not by itself improve the repository's selected exponent.

The paper explicitly says it does not know whether the log log n factor
can be removed (`ov:stronger`). No inference about practical SAT speed
follows from this asymptotic comparison.

## The different construction that matters

The main body uses factorizable pieces of a crossing-equality tensor,
with an initial parameter rho=11/12. Appendix B (`app:half`) uses
operators on Q[t_1,t_2,...] to obtain rho=1/sqrt(2). Weighted energy E
has a basis indexed by ordinary partitions, of dimension p(E).
Hardy--Ramanujan growth makes log_2 p(E)=Theta(sqrt(E)).

The encoded bit strings use partitions at the smallest h with
p(h)>=2^lambda. A piece indexed by s factors through spaces whose
dimensions are bounded by

```math
 R_s^{row}=\sum_{i=0}^{2h}p(s+i),\qquad
 R_s^{col}=\sum_{i=0}^{2h}p(2h-s-i).
```

Equations `eq:half-row` and `eq:half-col` are the concrete algebraic
factorizations. Their shared-bit total is at most
2sqrt(2)*lambda+O(log(lambda)). The master recursion has
log(K_ell)=Theta(2^ell) and e_ell=Theta(rho^ell), producing the saving
alpha'=log_2(1/rho). Appendix D (`app:onelog`) transfers the improved
rate to arbitrary density with the displayed iterated-log correction.

This supplies another mechanism to change. It does not use the OpenAI
Cauchy/Hermite even-node shortcut supplied earlier by the user. The
specific OpenAI restriction L=2^Theta(u) therefore does not establish
an obstruction for this other construction.

A concrete success test for work on these pieces is a family with
rho<1/sqrt(2), while retaining all hypotheses of `def:genpieces`:
the exact crossing identity, both integer factorizations, polynomially
many pieces, polynomial coefficient bit lengths, and evaluation time
2^O(lambda) with uniform fixed constants. The full master recursion
and arbitrary-density reduction must still be charged. Reducing a
formal intermediate-space count without a realizable factorization
does not meet this test.

One narrow next experiment is to compute the actual two flattening
ranks of small Appendix-B pieces and compare them with R_s^{row}
and R_s^{col}. A strict finite gap could motivate an image-space
identity; it would not establish a better rho. If the ranks saturate,
record that scope and change the pieces or their algebra rather than
only their partition-count estimate. No such rank experiment has
been run in this package.

## What was and was not checked about Lean

Appendix E reports Lean 4.33.1 proofs of the two main propositions,
using only the standard axioms, with replay checks by leanchecker and
nanoda through Comparator. It describes machine-model and encoding
differences between the formal statements and printed theorem, and
notes that AI models compared the two proofs. These are statements
from the paper, not independent checks performed in this round.

The [formal repository](https://github.com/anthropics/formal-math/tree/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth)
was available at the pinned commit. Its eth directory contains
MainResults.lean, Challenge.lean, Solution.lean, a proof directory,
build metadata and scripts. This round did not build the development,
run a checker, or audit the machine semantics.

## Relationship to concurrent research

[PR 1](https://github.com/1337isnot1337/3-SAT/pull/1) studies formal
mode counts, Hermite tapering and local Cauchy bases. Its obstructions
do not automatically apply to these different operator pieces.
[PR 2](https://github.com/1337isnot1337/3-SAT/pull/2) uses weighted
characteristic-two fingerprints for decision. The scalar lift here
instead preserves deterministic exact counting modulo 2^(f+1).
These PRs are credited as adjacent work, not proof dependencies.
