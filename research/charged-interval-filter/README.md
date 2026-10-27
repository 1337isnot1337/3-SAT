# Charged interval-filter counterexample

Status: `scoped_checked`; no interval filter or improved SAT bound. The former
uniform construction and its conditional rho/alpha formulas are withdrawn.

The left-charged highest-charge moment is scalar and obeys its length rule only
for the whole unweighted moment. A root of the scalar filter polynomial does
not imply that the associated charge-projected piece vanishes. The exact `h=3`
tensor in [PROOF.md](PROOF.md) leaves a non-scalar defect after the central
shifts are omitted. An additional rooted-polynomial factor also fails.

The note records two corrections needed even for the full unfiltered pairing:
a general invariant basis requires its nonsingular minor inverse, and the
factorial label rescaling is `D^-1 R` on the left with `D C` on the right.

Reproduce the exact controls and counterexample with:

```sh
python3 -I -B research/charged-interval-filter/verify.py
make verify
```

`PASS` means that the valid controls and the counterexample were reproduced,
not that a filter was constructed. Finite raw-charge witnesses in the separate
`charge-polynomial-filter` package are not refuted. The selected result remains
unchanged.
