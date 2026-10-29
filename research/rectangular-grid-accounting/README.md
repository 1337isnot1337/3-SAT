# Rectangular crossing ledger and weighted minimax

Status: `scoped_checked`; mathematical argument author-checked, not independently
reviewed. No improved SAT bound. Base: `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`.
Contributor: OpenAI Codex, with substantial AI assistance.

[PROOF.md](PROOF.md) extends the square-grid edge count to `p` by `q`:
it counts ordered straight and diagonal edge costs exactly and derives a
weighted continuous minimax including aspect-ratio offsets. The equal-weight
ideal coefficient tends to `1/2` with `p=2` and growing `q`, compared to
`1/sqrt(2)` for large square grids. This is a local certificate only: the
small row child cannot be assumed to have the continuation cost of the large
column child, and the recursive construction and other expenses are missing.
The result makes that obstacle concrete; it does not change selected alpha.

Run offline with standard Python:

```sh
python3 -I -B research/rectangular-grid-accounting/verify.py
make verify
```

The finite controls enumerate all 36 grid-dimension pairs in 2..7,
check every edge incidence, and check 404 rational circle samples against
four exact bisection brackets. These checks are not independent review or a
proof of asymptotic bounds. The proof states precisely what is assumed and
what remains to establish a real rectangular algorithm.

Sources and credit: the row/column grid transformation and two factorization
bounds are from Anthropic, *A 2^{o(n)} Time Algorithm for 3-SAT*,
[Hexagon v1](https://hexagonmath.org/2610.00577v1), source pinned and licensed
in `research/anthropic-operator-ranks/source/README.md`; see `prop:level`,
`eq:shared-bits`, `thm:master`, and Appendix B. PR 16's
`research/modular-rank-factorization/CHECKPOINT.md` first noted the ideal
square-root relation; the follow-up [PR 49](https://github.com/1337isnot1337/3-SAT/pull/49)
proves its tree form. New material is Apache-2.0 and AI-assisted. The
owner-accepted OpenAI baseline is unchanged and is not audited.
