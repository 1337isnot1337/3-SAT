# Charge-polynomial scalar filters

Status: `scoped_checked` for the first registered finite raw-charge screen.
No all-size filter, smaller rho or improved SAT alpha is claimed. This is
an active research checkpoint; [CHECKPOINT.md](CHECKPOINT.md) records the
changed next premise. Selected alpha remains 1/2 and upstream is untouched.

Task: `contraction-schedule`; base
`630041c9da3a26edb8c8f59d5f8a4132a188c8bd` (PR 19).
Contributor: Cinna Davis, with substantial OpenAI Codex assistance.

[METHOD.md](METHOD.md) classifies the entire scalar pairing space over ALL
charge coefficients at lambda=1,2, not a sample of charge values. It tests
four cutoffs at h=4 and five at h=6. Exact symbolic determinants distinguish
invertible combinations from spaces consisting only of singular matrices.
Each positive witness is normalized on x and checked entry by entry.

The four-label case admits an actual filtered crossing after removing
shifts -2 through 2. Removing -5 through 5 leaves only singular pairings
in the same raw-charge space. Both are finite facts. The checker does not
classify unlisted cutoffs or prove an eventual rate from these two grades.

Reproduce offline with standard Python:

```sh
python3 -I -B research/charge-polynomial-filter/screen.py
make verify
```

The report covers 560 polynomial operator evaluations against the pinned
reference, 744 full-piece charge evaluations, 186 coefficientwise two-order
checks, nine complete scalar-space classifications and exact positive
crossing witnesses. Code, registration and predecessor hashes are retained.
This research replay is outside default CI. No complete master/SAT solver,
independent review or formal proof is claimed.

The coefficient rank inflation from interpolation is at most D+1 in each
direction, with D<=2h. A uniform constant-fraction interval filter would
still need full leading label/output capacity, polynomial pieces, rational
generation and the complete PR 17 cost transfer. Those obligations are open.
The generic matrix and polynomial calculations use exponential space.

PRs 11,17,19 and Anthropic's operator factorizations are credited in
[SOURCES.json](SOURCES.json). The earlier uncharged moment-recovery branch
supplies the scalar-output constraint pattern; this package changes both
charge span and codebooks. Standard exact elimination, interpolation and
determinant algorithms are not claimed as new. New analysis/code is
Apache-2.0 and substantially Codex-assisted.
