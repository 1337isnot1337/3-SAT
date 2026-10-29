# Bound search checkpoint, 2026-10-29

The objective is still a proved improvement of the complete general-density
SAT bound. No such improvement has been established. Canonical main remains
c600b21ee7800a49c05718a254be50168e6b355b after the latest fetch.

## Exact rejected border variant

For the full grade-h input and output spaces, retain |s|>c and form
B(q)=sum_s w(s) Q_s(q). Take its (output 0, output 0) label matrix G(q).
The proposed normalization was G(q)^(-1) B(q). A border crossing as q tends
to infinity requires every entry of G^(-1)(B_yu-delta_yu G) to tend to zero.
Using adj(G) and det(G), this is an exact polynomial degree test, including
possible common-factor cancellation (which does not change degree difference).

At h=3,c=1, weights 1 and s give invertible G but maximum error degrees
4 and 3 respectively, so they fail. The root polynomial
w(s)=product_{j=-1}^1(s-j) gives singular G. The exact report and script are
retained. These three variants are stopped. This does not exclude other
weights, asymmetric input subspaces or a different border construction.

Reproduce with SymPy:

    python3 -B research/length-block-filter/border_probe.py 3 1

## The unresolved positive lead

The exact length-block witnesses in README.md remain valid, but they do not
supply a uniform formula or prove leading label capacity. In particular the
grade-ten witness principally uses charge degree five in a length-4/length-3
block, with only one possible contraction between charged factors at that
degree. Its three-dimensional invertibility must not be extrapolated to a
partition-sized block. The next useful result would characterize the whole
scalar matrix space with the grade and block lengths as parameters, not add
more isolated positive grades.

## Changed global premise under examination

Consider replacing each Boolean affine packet deformation by its exterior
powers: the entry between equally occupied row and column subsets is the
corresponding determinant minor; unequal occupations give zero. This still
gives equality at the identity matrix. Its modes are squarefree and its
Cauchy minors have a closed formula. The target is a better complete
mode/precision law, retaining polynomially many profiles and all signs,
entry costs, child size, recovery and outer decision costs. A merely smaller
constant in the same partition-count envelope will not establish a better
selected bound. The source affine deformation and frozen sources are not
changed. No exterior contraction algorithm is claimed here.
