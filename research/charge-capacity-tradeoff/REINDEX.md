# Reindexing the first moment to arbitrary charge degree

The weight-degree condition in [PROOF.md](PROOF.md) is a necessary
capacity condition, not a claim that high extraction degree is expensive
or impossible. The first-moment pairing of PR 11 gives a simple actual
boundary example, without a new operator calculation.

Fix h>=2 and any integer d>=1. For each shift s use the polynomial
weight `w_s(q)=s q^(d-1)`. It has degree at most b=d-1, and

    [q^d] sum_s w_s(q) Q_s^(q)
      = [q] sum_s s Q_s^(q).

The predecessor's exact first-moment identity states that the latter is
a scalar output operator whose full grade-h label matrix has rank
`p(h)-p(h-1)`. That rank has capacity
`exp(kappa sqrt(h)-O(log h))`, with `kappa=pi sqrt(2/3)`; the predecessor
already supplies the needed capacity estimate. Thus this actual operator
retains the target label capacity even if d is chosen much larger than h.
The effective degree is `d-b=1`, consistent with the necessary
`O(sqrt(h) log h)` condition. The example also shows that a high weight
degree alone does not impose a dense polynomial representation: these
weights are monomials.

The weight vanishes at s=0, but does not remove a fixed-fraction central
interval. It does not change the predecessor's supplied directional
rank envelope, construct a new faster SAT algorithm, or show that any
q-dependent normalization is free. The first-moment identity and rank
are premises credited to [PR 11](https://github.com/1337isnot1337/3-SAT/pull/11)
and [the merged proof](../charged-operator-moments/PROOF.md), not new
claims from this package. The observation is a direct algebraic substitution;
no new finite operator replay is needed to establish it.
