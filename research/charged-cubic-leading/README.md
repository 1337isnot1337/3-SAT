# Leading-charge scalar crossing from a cubic filter

Status: `scoped_checked` for finite calculations; the all-grade component
argument is author-checked and awaits independent or formal review. There
is no improved SAT bound or selected-result change. Contributor: Cinna Davis,
with substantial OpenAI Codex assistance.

## Result

For the charged source operators let
`M(q)=sum_s (s^3-s)/6 Q_s^(q)`. The coefficient of q^3 in M is a scalar
operator on the entire output energy space, with a label pairing H that is
independent of output energy. [PROOF.md](PROOF.md) gives the explicit formula

```math
 H_h(\mu,\nu)=h!\frac{m_\mu!}{m_\nu!}
 [u^\mu t^3]\exp(tC)\exp(L)\exp(t\partial_{u_1})u^\nu,
```

where `L=sum_(j>=2)(j-1)u_(j-1) partial_(u_j)`,
`C=sum_(j>=1)(-1)^(j-1)j u_j`, and `m_mu!` is the product of multiplicity
factorials. The final exponential acts first. The result follows by counting
three uncontracted weight-one fields and uses PR #11's binomial contraction
identity.

A four-charge finite difference extracts the coefficient in the **weighted
sum**. For each s define
`D_s=(Q_s^(2)-3Q_s^(1)+3Q_s^(0)-Q_s^(-1))/6`. Then

```math
 \sum_s (s^3-s)D_s/6=H_h(\mu,\nu)\operatorname{Id}.
```

At h=9, H has rank 19 and contains an exact invertible 8-by-8 nonprincipal
minor. Normalizing that minor on the first input axis gives an eight-label
crossing on any eight grade-nine output states, with s=-1,0,1 omitted.
The [saved report](verification.json) records explicit row/column labels,
output labels, minor and inverse. This construction mixes four charges and
may change the input labels, so it does not contradict the fixed-charge,
fixed-input grade-nine obstruction.

The finite ranks for h=3,...,15 match
`p(h)-p(h-3)-[h even]`. This is an observation, not an all-grade theorem.
A uniform high-rank pairing and all costs remain open. Even with such a
pairing, deleting only three shifts does not improve the inherited leading
rank envelope or alpha.

## Verification

```sh
python3 -I -B research/charged-cubic-leading/verify.py > /tmp/charged-cubic-leading.json
cmp /tmp/charged-cubic-leading.json research/charged-cubic-leading/verification.json
make verify
```

The checker compares 492 entire output vectors against the formula for all
label pairs at grades 2–6, with output energies 0 and 1 and additionally 2
at grades 2–4. These use direct finite differences of the shared charged
operator implementation. It calculates the full rational label ranks through
grade 15, verifies the grade-nine minor and inverse, and hash-binds the
code, proof and predecessor modules. It does not directly reconstruct every
grade-nine crossing tensor entry; that crossing follows from the written
all-grade coefficient identity and exact minor. There is no independent
operator oracle or formal review.

## Cost and provenance

Each mixed piece is a sum of four source pieces; both source directional
rank bounds grow by at most a factor four, and local first-axis normalization
does not increase either rank. A uniform construction would still require
high-rank minors at h=O(lambda^2), with `p(h)=2^O(lambda)`, computable
rational entries and inverse, and the full reduction, query, precision,
recursion, recovery, time and space accounting. No polynomial-height inverse
is assumed. See the conditional cost boundary in [PROOF.md](PROOF.md).

PR #11 provides charged normal ordering and the contraction identity;
PR #17 supplies the bounded rational-transfer framework. PR #32's
high-charge-degree capacity analysis is distinct from this fixed q^3
coefficient. Exact external source and license pins are in
[PR #11's source manifest](../charged-operator-moments/SOURCES.json).
