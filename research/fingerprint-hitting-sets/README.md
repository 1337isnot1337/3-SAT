# Fixed hitting sets for weighted decision fingerprints

Status: `scoped_checked`; the all-size argument is author-checked and has not
been independently reviewed. **No SAT time improvement or lower bound is
claimed.** The owner-accepted OpenAI theorem remains the starting point.

Task: `decision-only`. Base: `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`.
Contributor: Cinna Davis with substantial OpenAI Codex assistance. New
material is Apache-2.0.

The changed premise is to replace independent random field points in the
[weighted decision interface](../characteristic-two-decision/PROOF.md) by a
formula-independent deterministic hitting set. The stopping test is a proved
all-size obstruction for a concrete sparse formula family, with bounded exact
checks. The [proof](PROOF.md) meets that test: for 2-CNF formulas formed by
perfect matchings of XOR pairs, any fixed hitting set over a q-element field
has at least `(1-1/(2q))^(-K)` points, where
`K=max(0,floor((n-2q)/2)+1)`. A probabilistic upper bound on this exact family
has logarithm `O(n/q + log(n log(n+2)))`. The proof therefore fixes the
exponential scale where `n/q` dominates logarithms.

These formulas are easy to solve once their descriptions are inspected. The
obstruction applies to a fixed set of evaluations or to a formula-blind
black-box protocol, not to formula-aware preprocessing or arbitrary SAT
algorithms. It does not improve or change the selected alpha `1/2`. Issue
[#26](https://github.com/1337isnot1337/3-SAT/issues/26) and
[PR #38](https://github.com/1337isnot1337/3-SAT/pull/38) investigate a
different, random-evaluation and amplification question; this result uses
adversarial matchings against a universal deterministic list. The independent
predecessor fingerprint construction is credited above.

Reproduce with Python 3.11+ and no additional dependencies:

```sh
python3 -I -B research/fingerprint-hitting-sets/verify.py
make verify
```

[Saved output](verification.json) records every q-coloring and matching for
`(n,q)=(2,2),(4,2),(6,2),(8,2),(4,4),(6,4),(8,4)`. It verifies the claimed
probability bound and exact mean over colorings; for q=2 it independently
sums the fingerprint over every satisfying Boolean assignment. This is finite
evidence only, not an independent review of the all-size proof. The checker
runs in seconds and is not added to default CI.

Sources: accepted OpenAI source commit
`7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`, with hashes and licenses in
[SOURCES.json](../../SOURCES.json); predecessor
`research/characteristic-two-decision/PROOF.md`, sections 1 and 5. The proof
and its complete scope and cost boundary are in [PROOF.md](PROOF.md). Next:
explore whether stronger formula classes yield useful deterministic hitting
sets at polynomial field sizes, or whether the sparse-query reduction exposes
structured formula-aware evaluations; avoid interpreting matching obstructions
as unconditional algorithm lower bounds.
