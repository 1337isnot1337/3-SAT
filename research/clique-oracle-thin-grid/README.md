# Clique-oracle floor and a thin-grid certificate limit

Status: `scoped_checked`. Author-checked all-size argument, not independently
reviewed; no 3-SAT lower bound or improvement. Contributor: OpenAI Codex, with
substantial AI assistance. Base: `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`.

[PROOF.md](PROOF.md) proves a simple deterministic point-query lower bound
for the source's universal clique table interface, including exact conversion
to its `K² lambda` exponent convention. For bounded row-child size, the
bound prevents the row coefficient from tending to zero. In the continuous
rectangular minimax model of [PR 61](https://github.com/1337isnot1337/3-SAT/pull/61),
this means a thin split's ideal worst-case coefficient approaches the large
child's coefficient as that coefficient tends to zero. This does not bound
actual tensor ranks, structured SAT tables, randomized algorithms, or total
SAT runtime, and does not prove the model is implementable.

Reproduction, offline, Python 3 standard library:

```sh
python3 -I -B research/clique-oracle-thin-grid/verify.py
make verify
```

The script evaluates small Boolean oracle witnesses and exact rational controls
of the model; these are finite controls, not a formal proof or independent
review. The all-size oracle argument is a standard adversary, included to
make the source interface and scope explicit. Future work must investigate
whether actual structured row tables have cheaper access, or derive balanced
rectangular grouping and a complete recursion with growing child sizes.

Sources: Anthropic, *A 2^{o(n)} Time Algorithm for 3-SAT*,
[Hexagon v1](https://hexagonmath.org/2610.00577v1), `def:achievable`,
`prop:level`, `thm:master`; pinned source and license in
`research/anthropic-operator-ranks/source/README.md`. PR 61 supplies the
rectangular cost formula; PR 49 addresses the offset-free abstract model.
The owner-accepted OpenAI baseline is unchanged. New material is Apache-2.0
and substantially AI-assisted.
