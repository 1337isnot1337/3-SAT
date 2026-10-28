# Randomized decision still faces the clique-oracle floor

Status: `scoped_checked`; argument author-checked and awaiting independent
review. Contributor: OpenAI Codex, with substantial AI assistance. Base:
`630041c9da3a26edb8c8f59d5f8a4132a188c8bd`. No change to selected alpha.

[PROOF.md](PROOF.md) gives a sharp worst-outcome query bound for bounded-error
randomized decision on a zero-versus-one-hot subfamily of the source's
unrestricted clique table interface. For a fixed error below 1/2, a constant
fraction of `2^((K-1)lambda)` queries remains necessary. A matching scheme
is provided for that restricted subfamily. It extends the deterministic
point-query floor in [PR 69](https://github.com/1337isnot1337/3-SAT/pull/69).
This is not a 3-SAT lower bound: structured or succinct tables may admit
other access methods, and the matching scheme is not a general clique solver.

Reproduce offline with Python 3 standard library:

```sh
python3 -I -B research/randomized-clique-oracle/verify.py
make verify
```

The finite control enumerates 40 small random-subset schemes using exact
rational probabilities and checks the rounding threshold. It is not the
all-size proof or independent review. The proof states the fixed-input error
and worst-random-outcome requirements, and explains how a failure flag must
be handled. Any application to a new algorithm must still account for the
whole algorithm and its resources.

Source: Anthropic, *A 2^{o(n)} Time Algorithm for 3-SAT*,
[Hexagon v1](https://hexagonmath.org/2610.00577v1), `def:achievable` and
`thm:master`; exact pin and license in
`research/anthropic-operator-ranks/source/README.md`. The coupling adversary
is a standard information argument and is not claimed as a new general
query-complexity technique. New material is Apache-2.0, AI-assisted.
