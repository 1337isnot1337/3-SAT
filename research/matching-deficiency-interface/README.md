# Matching deficiency for decision

Status: `scoped_checked`; no independent review. Task `decision-only`; base `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`. Contributor: Codex, with substantial AI assistance.

[PROOF.md](PROOF.md) composes Szeider's published deterministic `2^k poly(n)` SAT algorithm, where k is maximum clause deficiency, with the owner-accepted counting theorem. It gives a polynomial-space decision interface taking the better of the two time bounds, and proves a matching-autarky reduction. It also provides connected bounded-occurrence, no-unit, no-pure satisfiable formulas with linear maximum deficiency and a one-variable branch that increases the parameter.

The fixed-parameter algorithm and accepted theorem are cited black boxes; neither is implemented here. The example does not rule out better preprocessing. No general 3-SAT alpha improvement is claimed.

```sh
python3 -I -B research/matching-deficiency-interface/verify.py
make verify
```

The checker uses Python's standard library and performs 1,200 small exhaustive controls plus 20 planted-family checks. It does not verify the source theorem. The next concrete question is whether an existing, fully paid reduction can guarantee sublinear maximum deficiency on every resulting decision query; bounded occurrence alone cannot.
