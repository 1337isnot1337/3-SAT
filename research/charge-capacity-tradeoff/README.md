# Charge-degree capacity tradeoff

Status: `scoped_checked`. No improved SAT bound or interval filter is
claimed. The all-size argument is author-checked and awaits independent
review. Contributor: Cinna Davis with substantial OpenAI Codex assistance.
Task `contraction-schedule`; base `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`.

For polynomial q-dependent shift weights of degree at most b, any linear
extraction that vanishes below degree d has effective degree e=d-b. The
length support mask has an exact structural rank given by a minimum
threshold cover. This improves the
predecessor's general cover in some finite cases; it need not be attainable
by the actual operators. When e/h tends to a fixed positive delta, this
implies a leading label-capacity loss; that leading rate is sharp for the
unrestricted support mask, although actual operators may have smaller rank. For delta in (0,2), retaining
2^lambda label rank requires an asymptotic grade at least
`1/(1-delta/2)` times the first-moment reference grade. The precise
statement, proof, limiting cases and restrictions are in [PROOF.md](PROOF.md).
At fixed deficit e=2h-k, the exact structural rank stabilizes to a sum
of cumulative partition numbers. At e=2h the rank-one mask is actually attained: extracting q^(2h) from
an individual raw charged piece gives an explicit scalar identity on the
all-ones row and column labels. This endpoint has only one label and does
not establish a useful crossing family.

This quantifies the charge-independent support lemma in
[the predecessor](../charged-asymmetric-crossing/NEXT.md), merged in PR 19;
it also covers bounded-degree charge-dependent weights and combinations
of higher charge coefficients. It does not cover arbitrary charge-dependent
normalization or weights of unrestricted degree. The
accepted OpenAI theorem remains a premise; the selected result and frozen
upstream sources are unchanged. Complete algorithmic costs and the absence
of an inferred SAT time bound are discussed in the proof.

Reproduce the bounded independent matching check and repository checks:

```sh
python3 -I -B research/charge-capacity-tradeoff/verify.py
python3 -I -B research/charge-capacity-tradeoff/endpoint.py
make verify
```

[verification.json](verification.json) records the grade range, number of
thresholds, strict finite improvements and SHA-256 hashes. These finite
checks do not prove the all-size arguments or general operator realizability.
[endpoint-verification.json](endpoint-verification.json) records the exact
finite-difference endpoint checks and predecessor module hashes.
The exact partition asymptotic is the standard Hardy--Ramanujan estimate,
also used by the predecessor. The charged construction, first-moment rank,
and earlier support lemma are credited to PRs 11 and 19. No priority,
independent review or formal verification is asserted.

Next, a route to an improved component may use higher-degree weights or
other controlled scalarization, then must prove output and
label capacity, directional rank bounds, and all generation costs. In
particular, no relationship between shift interval width and d is proved
here, so the grade inflation cannot by itself rule out an alpha improvement.
