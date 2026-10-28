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
unrestricted support mask, although actual operators may have smaller rank.
A uniform log-rank estimate covers all effective degrees up to 2h.
The predecessor target exp(kappa sqrt(h)-O(log h)) additionally requires
e=O(sqrt(h) log h); this is also sufficient for that capacity in the mask,
without establishing a realizable scalar pairing. In particular a weight
of degree b must satisfy b>=d-O(sqrt(h) log h) to retain the target after
extracting degree d; this is not by itself a weight-evaluation cost bound. For delta in (0,2), retaining
2^lambda label rank requires an asymptotic grade at least
`1/(1-delta/2)` times the first-moment reference grade. The precise
statement, proof, limiting cases and restrictions are in [PROOF.md](PROOF.md).
At fixed deficit e=2h-k, the exact structural rank stabilizes to a sum
of cumulative partition numbers. At e=2h the rank-one mask is actually attained: extracting q^(2h) from
an individual raw charged piece gives an explicit scalar identity on the
all-ones row and column labels. This endpoint has only one label and does
not establish a useful crossing family. One degree lower, an outer-shift
piece also attains the two-label structural rank via a scalar operator
matrix; this remains constant label capacity. One degree lower again, the
all-ones pair has a weighted number operator with a simple spectrum on
grade-h outputs, so a scalar invariant output subspace has dimension at
most one. A single simple-spectrum operator nevertheless has a rational
two-sided scalar compression of dimension floor(N/2); simultaneous label
pairing scalarity and factor costs are separate. At the adjacent shift a concrete grade-four collision produces
a two-dimensional scalar eigenspace; all 25 label-pair operators preserve
it and act scalarly, with rank-three label matrix. The [adjacent-shift proof](ADJACENT.md)
shows the analogous all-ones operator has simple spectrum for every h>=5,
so this particular example cannot extend to larger grades using the same
shift and unprojected scalar subspace. [Outer-filter constraints](OUTER-FILTER.md)
prove that weighted outer shifts cannot produce a nonzero scalar for
the all-ones output operator on the full grade-h space. The proof combines
a sign-variation argument with a reflected-walk determinant. A separate
[high-shift filter](TAIL-FILTER.md) obtains an exact full-label scalar pairing beyond that shift range,
with rank exactly three for h>=3. The same weights fail scalarity one
charge degree lower already at h=2. Other constructions remain open.

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
python3 -I -B research/charge-capacity-tradeoff/near_endpoint.py
python3 -I -B research/charge-capacity-tradeoff/second_deficit.py
python3 -I -B research/charge-capacity-tradeoff/spectrum.py
python3 -I -B research/charge-capacity-tradeoff/adjacent_shift.py
python3 -I -B research/charge-capacity-tradeoff/adjacent_pairing.py
python3 -I -B research/charge-capacity-tradeoff/adjacent_spectrum.py
python3 -I -B research/charge-capacity-tradeoff/outer_filter.py
python3 -I -B research/charge-capacity-tradeoff/tail_filter.py
python3 -I -B research/charge-capacity-tradeoff/tail_pairing.py
python3 -I -B research/charge-capacity-tradeoff/tail_next.py
make verify
```

[verification.json](verification.json) records the grade range, number of
thresholds, strict finite improvements and SHA-256 hashes. These finite
checks do not prove the all-size arguments or general operator realizability.
[endpoint-verification.json](endpoint-verification.json) records the exact
finite-difference endpoint checks; [near-endpoint-verification.json](near-endpoint-verification.json)
records rational interpolation checks of the two-label case. Both include
predecessor module hashes. [second-deficit-verification.json](second-deficit-verification.json)
records the next-coefficient operator checks; [spectrum-verification.json](spectrum-verification.json)
records the bounded simple-spectrum checks. [adjacent-shift-verification.json](adjacent-shift-verification.json)
records the finite collision. [adjacent-pairing-verification.json](adjacent-pairing-verification.json)
records the full finite label pairing and leakage checks.
[adjacent-spectrum-verification.json](adjacent-spectrum-verification.json)
records the broader adjacent-shift checks. [outer-filter-verification.json](outer-filter-verification.json)
records the weighted-shift formula and finite rank checks.
[tail-filter-verification.json](tail-filter-verification.json) records the
high-shift scalar coefficient checks; [tail-pairing-verification.json](tail-pairing-verification.json)
records the full-label checks; [tail-next-verification.json](tail-next-verification.json)
records the next-degree counterexample.
The exact partition asymptotic is the standard Hardy--Ramanujan estimate,
also used by the predecessor. The charged construction, first-moment rank,
and earlier support lemma are credited to PRs 11 and 19. No priority,
independent review or formal verification is asserted.

Next, a route to an improved component may use higher-degree weights or
other controlled scalarization, then must prove output and
label capacity, directional rank bounds, and all generation costs. In
particular, no relationship between shift interval width and d is proved
here, so the grade inflation cannot by itself rule out an alpha improvement.
