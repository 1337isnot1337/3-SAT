# A second contraction mechanism and its improvement contract

Source: Claude (Anthropic), *A 2^{o(n)} Time Algorithm for 3-SAT*,
[Hexagon v1](https://hexagonmath.org/2610.00577v1), with exact file pins in
[SOURCES.json](SOURCES.json). This is a construction comparison, not an audit
of the owner-accepted OpenAI theorem or a new accepted SAT bound.

## The interface worth importing

For a length-`lambda` crossing `[x=v][y=u]`, Definition 7 supplies pieces
`A_s` and a nonzero integer `d` such that their sum is `d[x=v][y=u]`.
Each piece factors in the row direction `(x,y)|(u,v)` and in the column
direction `(x,u)|(y,v)`. The combined bit cost must obey

```math
 c_s^{\rm row}+c_s^{\rm col}\le4\rho\lambda+O(\log\lambda).
```

The number of pieces, uniform construction and entry algorithms, output
integer lengths, denominator `d`, graph balancing, recurrence overhead,
base instances and conversion to bit operations all remain obligations.
A low rank in only one direction does not meet this contract. A succinct
description with exponential entry evaluation can erase a formal saving.

The elementary eight-square construction supplies `rho=11/12`. Appendix B
replaces it by operators on `Q[t_1,t_2,...]`, graded by `weight(t_j)=j`.
Its grade dimensions are partition numbers `p(E)`. Lemma 9 supplies an
operator identity working in both orders; Lemma 10 supplies a dual family
that recovers equality of labels. Theorem B uses `p(h)>=2^lambda` and has
factorization lengths

```math
 R_s^{\rm row}=\sum_{i=0}^{2h}p(s+i),\qquad
 R_s^{\rm col}=\sum_{i=0}^{2h}p(2h-s-i).
```

The growth `log p(E)=C sqrt(E)+O(log E)` bounds their combined bit cost by
`2 sqrt(2) lambda+O(log lambda)`, hence `rho=1/sqrt(2)`. Theorem A's
essentially squared graph-size growth converts a feasible `rho` into
`alpha=log2(1/rho)`. Better rank estimates for actual pieces, or another
graded operator identity with a smaller feasible ratio, could improve that
alpha. This is an external mechanism to study, not a result established
by this scan.

## Conditional growth calculation

Suppose a changed construction met all the same uniform piece and recovery
contracts, with grade dimensions `d(E)` satisfying
`log2 d(E)=C E^beta+o(E^beta)`, `0<beta<1`, and the same intermediate
grade bounds `2h+s` and `2h-s`. Suppose also its label family has
`lambda=C h^beta+o(h^beta)` bits. Concavity gives a combined directional
bit envelope of

```math
 C\bigl((2h+s)^\beta+(2h-s)^\beta\bigr)
 \le2^{\beta+1}C h^\beta.
```

This would give `rho=2^(beta-1)` and `alpha=1-beta`, provided the rest of
Theorem A's interface were still achieved. For example, `beta=1/3` targets
`alpha=2/3`. This is conditional cost algebra. A Hilbert-series growth
change does not prove the operator identity, dual label pairing or cheap
realizable pieces.

A precise first experiment is to retain only square-indexed oscillators,
whose partition growth is smaller, and test Lemma 9 before claiming any
gain. The source's commutator cancellation uses every oscillator index.
Whether a modified operator identity can preserve locality after thinning
is the actual missing condition. A finite-rank drop without that identity
would not establish a new contraction algorithm.

## Two other transfer conditions

The blocky-matrix decomposition theorem in
[Carenini's paper](https://eccc.weizmann.ac.il/report/2026/153/) counts signed
equality-kernel pieces. The number of labels within one piece is unbounded:
an identity matrix is already blocky and has full rank. A bound on that
piece count does not by itself bound the directional costs needed above.

Similarly, faster finite-field interpolation from
[Mohapatra](https://eccc.weizmann.ac.il/report/2026/278/) does not automatically
apply to the accepted two-adic recovery ring. Original recovery work is
already polynomial in its parameters. A new use must change a dominating
cost or permit a previously infeasible schedule, while checking algebraic
hypotheses and the randomized worst-outcome time contract.

The accepted general-density `log log n` overhead is a separate obligation.
Improving an explicitly polynomial subroutine or a finite matrix product
does not remove it or increase global alpha.
