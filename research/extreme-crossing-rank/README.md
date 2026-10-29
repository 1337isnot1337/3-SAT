# Endpoint crossing ranks and a real grouping witness

Status: `scoped_checked`; all-size proof author-checked and awaiting independent
review. Contributor: OpenAI Codex, with substantial AI assistance. Base:
`c7c5a03434b396e227e9ab573b5b7cdea52b47fa`.

[PROOF.md](PROOF.md) proves for every energy and every partition codebook
that the two extreme shifts of the pinned Appendix-B crossing have opposite
rank profiles `(1,d²)` and `(d²,1)`. An explicit positive-definite kernel
proves both necessary pairing matrices invertible for arbitrary codebooks.

In a 2-row grid, independently choosing those two shifts realizes any graph
as the column-pair rank pattern. Combining this with the fixed-block
probabilistic construction (companion branch
[fixed-block-grouping-obstruction](https://github.com/1337isnot1337/3-SAT/tree/research/fixed-block-grouping-obstruction))
gives actual crossing terms on which the equal-size, common-width column
grouping interface has an unavoidable padding loss approaching 4/3. This
proves a barrier for those pair factors; a different direction, representation
or algorithm may evade it. It is not a 3-SAT lower bound or a new alpha.

Reproduce offline using Python 3 standard library:

```sh
python3 -I -B research/extreme-crossing-rank/verify.py
make verify
```

The checker uses the existing PR 10 operator implementation and verifies
exact positive-definite blocks through energy 10 plus all endpoint entries
for lambda 1,2,3, and checks a concrete 8-column grouping pattern over all
105 pair partitions. It does not independently prove the all-size argument,
provide formal verification, or produce the nonconstructive graphs. The
selected OpenAI baseline is unchanged.

Source: Anthropic, *A 2^{o(n)} Time Algorithm for 3-SAT*,
[Hexagon v1](https://hexagonmath.org/2610.00577v1), `eq:ops`, `eq:Q`,
`eq:half-row`, `eq:half-col`; exact pin and license in
`research/anthropic-operator-ranks/source/README.md`. PR 10's finite screen
first records the endpoint ranks at lambda 1,2,3; PR 61 supplies the
rectangular cost ledger; PR 59 studies independent hook witnesses for the
shift span, a different rank question; the companion branch gives the grouping
graph.
New proof and code are Apache-2.0 and substantially AI-assisted.
