# Research directions

The accepted OpenAI theorem is the starting point. These lanes seek a changed
algorithm or a useful component improvement. The [task catalogue](tasks.json)
owns the current cards and coverage; check live Issues and PRs for overlap.
Use the [construction map](CONSTRUCTION.md) to locate each component in the
frozen source.

## Weighted modes

The accepted contraction enumerates mode monomials below a weighted precision
budget. Its upper bound uses a count of modes at each weight. A new construction
may impose additional restrictions on which monomials can occur.

Start by specifying one changed mode family and its generating function. State
the extra restriction and whether it holds throughout recursion. Then compare
the resulting exponent with the accepted `M/sqrt(u)` envelope. A finite
histogram is useful evidence for that family; an asymptotic gain needs a uniform
argument and a realizable construction.

Task: `weighted-modes`. Read the [full card](tasks.json) with
`python3 scripts/tasks.py --task weighted-modes`.

## Contraction schedule

Packing, interpolation multiplicities, precision growth, and child sizes are
coupled. Improving one parameter is useful only when the full schedule remains
feasible and the leaf or entry cost does not absorb the gain.

Start with a proposed schedule on paper: root cost, wire count and retained
valuation levels at each depth, precision increments, entry cost, and leaf
threshold. Changing only the geometric recursion ratio improves a constant.
A larger alpha requires a better dominant logarithmic saving.

Task: `contraction-schedule`. Relevant source labels include
`eq:tensor-parameters`, `eq:tensor-precision-bound`, and `subsec:tensor-cost`.

## General-density encoding

The arbitrary-density route uses sparse polynomial queries and an encoding
with `O(n log log n)` wires. A smaller encoding could improve the general-case
bound even with the accepted contraction theorem unchanged.

Start with one change to monomial indexing or grouping. Count index bits,
invalid encodings, group degree, tensor-entry work, arrays, and all reduction
queries. An `O(n)`-wire result would remove the extra iterated logarithm if its
other costs fit, while keeping alpha at `1/2`.

Task: `dense-encoding`. Start at `lem:tensor-sparse-query` and
`eq:sharp-wire-budget` in the quantitative reduction source.

## Decision-only algorithms

The target asks whether a satisfying assignment exists. The accepted theorem
provides the stronger operation of exact counting, leaving room to change the
interface when only a yes/no answer is needed.

Start by naming the exact-counting operation being replaced and the guarantee
of its substitute. For a randomized proposal, give the success probability on
each fixed input and the time on every random outcome. Charge amplification
and any recovery work. The [problem contract](PROBLEM.md) permits explicit
space tradeoffs.

Task: `decision-only`.

## Complete cost accounting

Use this lane to evaluate a concrete proposal from any of the others. Copy a
[baseline model](../certificates/models/general.json) into a research package,
change the relevant assumptions, add every overhead, and run:

```sh
python3 -m satbounds.cost research/your-package/model.json
```

The output is an eventual symbolic comparison, with unspecified constants. It
does not establish that a changed assumption is achievable. The
[model's scope and failure controls](../research/baseline-cost-model/README.md)
explain what the tool can establish.

Task: `complete-cost`. A useful result may be a complete comparison, a missing
lemma stated precisely, or an obstruction to a particular proposed change.
