# Deterministic detection for sparse solution fingerprints

Status: `scoped_checked` for the recorded finite checks. The all-size argument
is author-checked, not independently reviewed. No general SAT improvement or
new alpha is claimed. The owner-accepted OpenAI theorem is the starting point.

Task: `decision-only`. Base `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`.
Contributor: Cinna Davis with substantial OpenAI Codex assistance. Apache-2.0.

The [proof](PROOF.md) gives a deterministic black-box test for nonempty
multilinear F2-coefficient fingerprints of support at most S, using
`poly(n,S)` evaluations over binary fields with `O(log(nS))` bits per element.
It uses modular Kronecker exponents, exact polynomial interpolation and a
prime that isolates a chosen support monomial. It never accepts empty support;
outside the support promise it may reject nonempty support. For polynomial S,
it gives polynomially many evaluations. A conditional application to
fixed-density k-CNF with at most polynomially many solutions retains the
accepted `2^O(n/sqrt(log n))` envelope and polynomial space, relying on the
written predecessor evaluator. Exact counting already gives the same envelope
without the promise, so this is an interface construction, not a time gain.

The arbitrary-density randomized hash wrapper can introduce extra survivors;
a solution-count promise on the original formula does not give the necessary
support bound on its intermediate system. The new construction does not
remove that gap or certify a smaller selected result. Issue
[#66](https://github.com/1337isnot1337/3-SAT/issues/66) records this lane;
[#26](https://github.com/1337isnot1337/3-SAT/issues/26) concerns random field
amplification, and [#45](https://github.com/1337isnot1337/3-SAT/issues/45)
fixed hitting-set lower bounds. The two are separate interfaces.

Reproduce, Python 3.11+, standard library:

```sh
python3 -I -B research/sparse-support-deterministic/verify.py
make verify
```

[Saved output](verification.json) checks all nonempty supports through n=4
against the promised isolation bound, plus exact GF(16) interpolation and an
even-support unweighted-parity failure control. These checks do not implement
the accepted contraction, establish its assumptions on new inputs, or
independently review the all-size argument.

Credit the characteristic-two weighted decision interface in
`research/characteristic-two-decision/PROOF.md`, especially Sections 1-4,
and OpenAI source commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`,
`lem:tensor-sparse-query` and `thm:tensor-contraction`; exact hashes and
licenses are in [SOURCES.json](../../SOURCES.json). No external priority claim
is made. Concrete follow-ups and full cost boundaries are in [PROOF.md](PROOF.md).
