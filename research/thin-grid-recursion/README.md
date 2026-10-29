# Iterating an ideal thin-grid recurrence

Status: `scoped_checked`; all-size argument author-checked and awaiting
independent review. Contributor: OpenAI Codex, with substantial AI assistance.
Base: `e1e57cd165d9806b1bbf6500153ee1f37fedf093`.

[PROOF.md](PROOF.md) studies an explicitly defined quarter-disk minimax
recurrence, taking the infinite-aspect-ratio limit at every level while
holding one child coefficient fixed. Unlike a single-step limit, it tracks
accumulated effects: the iterates satisfy `n v_n² -> b u²`. Assigning ideal
sizes `K_n=K_0 p^n` gives a `1/sqrt(log K_n)` profile. The limiting model
is not a finite-grid recursive algorithm, a lower bound on actual ranks, or
an improvement to the selected 3-SAT bound. Finite-q error accumulation,
grouping, recursion and all other costs remain open.

Reproduce offline with Python 3 standard library:

```sh
python3 -I -B research/thin-grid-recursion/verify.py
make verify
```

The first command checks four 10,000-step floating-point trajectories;
it is a numerical control only. The limit is established by the all-size
argument, which has not been independently reviewed or formally verified.

Sources: the crossing grid and partition envelopes are due to Anthropic,
*A 2^{o(n)} Time Algorithm for 3-SAT*,
[Hexagon v1](https://hexagonmath.org/2610.00577v1), pinned and licensed in
`research/anthropic-operator-ranks/source/README.md`. The exact rectangular
ledger is [PR 61](https://github.com/1337isnot1337/3-SAT/pull/61), and its
bounded-child oracle motivation is [PR 69](https://github.com/1337isnot1337/3-SAT/pull/69).
New material is Apache-2.0 and AI-assisted; the owner-accepted OpenAI
baseline is unchanged.
