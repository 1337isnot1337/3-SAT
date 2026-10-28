# Fixed-block grouping obstruction

Status: `scoped_checked`; all-size argument author-checked, not independently
reviewed. Contributor: OpenAI Codex, with substantial AI assistance. Base:
`ec45f184710a6adcd74e1aea31f29d7d1c44d0e2`.

[PROOF.md](PROOF.md) shows that, for every fixed group size p and large q,
some allowed 0/1 equality networks have near-half edge density but **every**
equal-size grouping contains a full p-by-p block. Consequently, the source's
common-width grouped-edge interface may cost nearly twice the original total.
The proof is probabilistic and nonconstructive; it does not show that the
specific crossing networks in [PR 61](https://github.com/1337isnot1337/3-SAT/pull/61)
realize these graphs. Alternative representations, nonuniform edges, and
structured groupings remain open. This is not a general tensor or SAT lower
bound, and selected alpha remains unchanged.

Run offline with Python 3 standard library:

```sh
python3 -I -B research/fixed-block-grouping-obstruction/verify.py
make verify
```

The exact finite control enumerates 105 pairings of eight vertices, for an
explicit 24-edge graph and a matching negative control. It illustrates the
property at p=2 and does not establish the near-half-density asymptotic
existence theorem or provide independent review.

Source: Anthropic, *A 2^{o(n)} Time Algorithm for 3-SAT*,
[Hexagon v1](https://hexagonmath.org/2610.00577v1), `def:network` and
`lem:grouping-explicit`, pinned and licensed in
`research/anthropic-operator-ranks/source/README.md`. PRs 61 and 110 provide
the rectangular cost model and finite-coefficient recurrence. The union-bound
method is standard; no general novelty is claimed. New material is
Apache-2.0 and substantially AI-assisted.
