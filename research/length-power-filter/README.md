# Length-power charge filters

Status: `scoped_checked` for the registered finite codebooks only. No all-size
filter, smaller piece ratio, improved SAT bound, or larger alpha is claimed.
The accepted OpenAI theorem and selected result remain unchanged.

Task: `contraction-schedule`. Canonical base:
`630041c9da3a26edb8c8f59d5f8a4132a188c8bd`. This branch starts after the
charge-deficit checkpoint at `4e117f8d2bb81bde26e31594efc2cf2f667c9b60`.
Contributor: Cinna Davis, with substantial AI assistance. New work is Apache-2.0.

## Changed premise

For a row partition `mu` and column partition `nu`, rescale each charged entry
by

```math
Q_s^{(q)}(\mu,\nu)\longmapsto q^{2(\ell(\mu)+\ell(\nu))}Q_s^{(q)}(\mu,\nu).
```

For nonzero `q` this is an invertible diagonal transformation on each required
input axis, so it preserves both flattening ranks at every charge evaluation.
Its coefficient of degree `e=d+2(length(mu)+length(nu))` is exactly the raw
charge coefficient of degree `d`. This differs from the raw, inverse-length,
and length-amplified spaces registered by the predecessor packages.

## Finite result and sharp control

The exact screen spans the complete scalar-output rational weight space on the
PR 19 codebooks, computes the entire induced label-matrix space, and tests its
determinant polynomial. At `lambda=2,h=6`, the raw space has no full-rank scalar
pairing after removing `|s|<=5`, while the new length-power space has an actual
normalized crossing after removing every shift `-6,...,6`. Its entire scalar
matrix space is singular after removing `|s|<=7`. At `lambda=1,h=4`, the new
space has a full-rank crossing through cutoff 4 and none at cutoff 5.

Thus the two positive cases remove the central interval through `|s|<=h`.
They are finite algebraic witnesses only; two grades do not prove a uniform
pattern or leading asymptotic capacity. The checker verifies every normalized
crossing entry in memory and records finite rank-inflation bounds. It does not
infer an all-size ratio from those finite bounds.

## Extreme-shift recovery of the first-moment minor

A sharper finite test asks for a specified invertible pairing rather than an
arbitrary full-rank matrix in the scalar span. On the PR 19 asymmetric
codebooks at `h=4` and `h=6`, and on the custom full-rank codebook at
`h=7,N=4`, the scalar space generated using only `|s|>=h` contains the
highest-charge first-moment pairing. Its selected minor has ranks `2`, `4`,
and `4`, respectively. Thus the finite witnesses recover the already uniform
PR 19 local inverse instead of relying on a new generic matrix inversion.

The checker computes the complete scalar-output rational weight space and
tests exact membership of the induced label matrix. The three saved reports
also record the other tested highest-charge and uncharged moments. These are
still three finite grades: no uniform recovery formula, all-size scalarity,
leading capacity, or improved bound follows without the remaining proof.

An all-size successor with the same leading capacities and a constant-fraction
central omission would give the conditional piece ratio

```math
\rho(\epsilon)=(\sqrt{2+\epsilon}+\sqrt{2-\epsilon})/4<1/\sqrt2,
```

with `epsilon=1` corresponding to the finite cutoff pattern above. This is a
success criterion, not an achieved result. Scalarity, invertible pairings,
leading row/column/output capacity, polynomially many uniform pieces,
coefficient heights, both directional ranks, rational transfer, and the full
master recursion all remain mandatory.

## Reproduction

From the repository root, with standard-library Python:

```sh
python3 -I -B research/length-power-filter/screen.py
python3 -I -B research/length-power-filter/moment_recovery.py 4 2 \
  --output research/length-power-filter/moment-recovery-h4.json
python3 -I -B research/length-power-filter/moment_recovery.py 6 4 \
  --output research/length-power-filter/moment-recovery-h6.json
python3 -I -B research/length-power-filter/moment_recovery.py 7 4 \
  --output research/length-power-filter/moment-recovery-h7.json
make verify
```

The report is saved in `verification.json`. The checker reuses the pinned
charge recurrence and exact rational matrix routines without modifying them.
All ranks, determinants, and crossing entries use exact integer or rational
arithmetic. These bounded checks are not an independent proof review, a formal
proof, or a SAT solver.

## Sources and credit

The operator construction is Anthropic's Appendix B, as pinned by the
predecessor packages. PRs 11, 17 and 19 supply the charged operators, rational
transfer and asymmetric codebooks. The charge-polynomial package supplies the
recurrence and complete scalar classifier. See `SOURCES.json`. No scientific
priority or independent review is claimed.
