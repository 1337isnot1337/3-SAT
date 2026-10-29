# Sharp moment vanishing for a single-part charged input label

Status: `scoped_checked` for the bounded operator tests. The all-grade
argument is author-checked, substantially AI-assisted, and awaits
independent or formal review. There is no new SAT bound or selected-result
change. Contributor: Cinna Davis, with substantial OpenAI Codex assistance.

## Result

For the charged source pieces, fix a single-part first input label `(h)`
and any homogeneous second label b of weight h. On every output-energy
space V_E and for every integer charge q,

```math
 \sum_s s^d Q_s^{(q)}(a^{(h)},b)=0,\qquad 1\le d\le h.
```

Consequently every polynomial shift weight f of degree at most h acts on
this input row as the constant weight f(0); if f(0)=0, the entire filtered
operator row is zero. This is an equality on the **whole output space**,
not only a compressed codebook. Any full p(h)-by-p(h) scalar pairing for
such a filter has rank at most p(h)-1 because its `(h)` row is zero. This
does not imply the remaining input labels have low rank or that a
high-capacity asymmetric label minor is impossible.

The cutoff is sharp at every h>=1. For every integer charge q and the source's single-part
second label b^(h), the next moment has a positive explicit diagonal entry:

```math
 [t_h]\left(\sum_s s^{h+1}Q_s^{(q)}(a^{(h)},b^{(h)})\right)t_h
 =(h+1)!h!\left(q^2+h{2h-1\choose h-1}+(-1)^{h-1}h\right)>0.
```

[PROOF.md](PROOF.md) gives the all-grade contraction argument, including
charge and the sharpness coefficient. It uses the predecessor's binomial
contraction identity and the same Laurent coefficient reading, not a new
proof of the owner-accepted baseline theorem. In particular, the cubic
weight `(s^3-s)/6` has a zero `(h)` row when h>=3, explaining one
component of the finite pairing-rank observations in PR #89. It does not
prove their conjectured `p(h)-p(h-3)` rank formula.

## A length-band consequence

For any two input partitions mu,nu of weight h, an operator moment of
order d vanishes whenever `abs(length(mu)-length(nu))>d`, at any output
energy and integer charge. More generally, the same holds for every shift
polynomial of degree at most d. [LENGTH-BAND.md](LENGTH-BAND.md) proves this
by counting unmatched fields in the charged contraction expansion. The
strict inequality is sharp: a grade-4 length difference of 3 gives a
nonzero third moment. This is a sparsity statement, not a bound on the rank
of the remaining band.

## Checks and limits

```sh
python3 -I -B research/charged-single-current/verify.py > /tmp/charged-single-current.json
cmp /tmp/charged-single-current.json research/charged-single-current/verification.json
python3 -I -B research/charged-single-current/band.py > /tmp/charged-length-band.json
cmp /tmp/charged-length-band.json research/charged-single-current/band-verification.json
make verify
```

The standard-library checker verifies 210 instances of the binomial
contraction identity, 3,802 complete output-vector moment identities across
h=1,...,6, several output energies and charges, and the explicit next-moment
coefficient at each grade for five charges. The separate length-band checker
verifies 1,712 complete vector moments and an exact nonzero boundary case. The report records the exact test scopes, nonzero
witnesses and hashes. The operator implementation is shared with the
predecessor and is not an independent oracle or formal review.

The conclusion removes one source-label direction from a polynomial filter;
the chosen asymmetric input codebook may not include `(h)`. It neither
bounds the remaining input rank nor gives a faster crossing, SAT runtime or
alpha. A complete improvement must still pay source reduction, entries,
queries, cut ranks, recursion, precision, recovery, time and space.

The charged operators, exact external source and licenses are pinned in
[PR #11's source manifest](../charged-operator-moments/SOURCES.json), and
its proof supplies the binomial contraction identity used here. The prior
uncharged shift-span work in [research/scalar-relation-witness](../scalar-relation-witness/README.md)
studies different label slices and is not a high-rank claim for this row.
The accepted OpenAI baseline and frozen upstream files are unchanged.
