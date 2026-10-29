# Charge-deficit scalar filters

Status: `scoped_checked` for the registered finite codebooks only. No all-size
filter, smaller piece ratio, improved SAT bound, or larger alpha is claimed.
The accepted OpenAI theorem and selected result remain unchanged.

Task: `contraction-schedule`. Canonical base: `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`.
The immediately preceding raw-charge screen is preserved at branch head
`1cf8bf329bf7bc8489cbe804f0e57ed44ab9cc2e`. Contributor: Cinna Davis, with
substantial AI assistance. New work is Apache-2.0.

## Changed premise

Rescale each raw charge-polynomial entry on a row label `mu` and column label
`nu` by `q^(-length(mu)-length(nu))`. Writing `z=1/q`, coefficient `z^e` is
the raw charge coefficient `d=length(mu)+length(nu)-e`. This is a local
diagonal change on the two required input axes and therefore preserves each
piece's two flattening ranks. It records contraction deficit rather than
absolute charge degree. The earlier raw-charge negative certificates do not
cover this charge-dependent normalization.

## Finite result and success boundary

The exact screen classifies the complete scalar-output rational weight space
on the PR 19 codebooks, then tests the determinant of the entire induced
label-matrix space. At `lambda=1,h=4`, full-rank filtered crossings exist
after removing `|s|<=0,1,3`; at `lambda=2,h=6`, they exist after removing
`|s|<=0,1,2`. Removing `|s|<=5` at `h=6` leaves only singular pairings in
this finite space. These are actual finite algebraic witnesses, not an
asymptotic construction.

A full-weight-space control at `h=4` also has a rank-four scalar pairing after
removing `|s|<=1`, but only rank one after removing `|s|<=3`. This makes the
output-capacity obligation explicit rather than inferring it from a selected
minor.

Success now requires an all-size scalar identity with a constant-fraction
central interval removed and leading label AND output capacity. Polynomially
many pieces, uniform generation, coefficient heights, both directional ranks,
and the complete rational-transfer/master-recursion costs remain mandatory.
The finite positive cases alone establish none of these.

## Reproduction

From the repository root, with standard-library Python:

```sh
python3 -I -B research/deficit-charge-filter/screen.py
```

The report is saved in `verification.json`. The checker reuses the pinned
charge-polynomial recurrence and exact rational matrix routines without
modifying them. Exact integer arithmetic is used throughout; no floating
ranks or randomized determinant tests are used. These bounded checks are not
an independent proof review, a formal proof, or a SAT solver.

## Sources and credit

The operator construction is Anthropic's Appendix B, as pinned by the
predecessor packages. PRs 11, 17 and 19 supply the charged operators, rational
transfer and asymmetric codebooks. The raw charge-polynomial screen supplies
the recurrence and scalar-constraint implementation. See `SOURCES.json` and
the predecessor `research/charge-polynomial-filter/SOURCES.json`. No scientific
priority or independent review is claimed.
