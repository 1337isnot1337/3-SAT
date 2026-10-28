# Finite coefficients in the ideal thin-grid recurrence

Status: `scoped_checked`; all-size proof author-checked and awaiting independent
review. Contributor: OpenAI Codex, with substantial AI assistance. Base:
`343b301cc28302bcbad0d4fb7c55f16fd17fe8bd`.

[PROOF.md](PROOF.md) takes the exact rectangular coefficient model of
[PR 61](https://github.com/1337isnot1337/3-SAT/pull/61), sets `q_n=q_0 p^n`,
and proves that the finite coefficients retain the asymptotic law
`n v_n² -> ((p-1)/p)u²`. This removes the repeated infinite-aspect-ratio
limit from [PR 101](https://github.com/1337isnot1337/3-SAT/pull/101) within
the continuous minimax model. It does not construct a SAT algorithm or prove
that the cost envelope is tight for real pieces. Finite partition/rounding
errors, grouping, and the complete cost ledger remain open.

Run offline, Python 3 standard library:

```sh
python3 -I -B research/finite-grid-recursion/verify.py
make verify
```

The first command checks four 10,000-step floating-point trajectories; it
is a numerical control, not the proof. The all-size argument is not formally
verified or independently reviewed. The proof also handles more general
summable offset sequences under its explicit condition.

Source: Anthropic, *A 2^{o(n)} Time Algorithm for 3-SAT*,
[Hexagon v1](https://hexagonmath.org/2610.00577v1), the grid and Appendix B;
pin and license are in `research/anthropic-operator-ranks/source/README.md`.
Predecessors PRs 61, 69 and 101 supply the model, oracle motivation and
limiting recurrence. New material is Apache-2.0 and substantially AI-assisted.
The owner-accepted OpenAI result and selected alpha are unchanged.
