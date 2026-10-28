# Finite polynomial kernels for the charged cubic energy pencil

Status: `scoped_checked`; the finite certificates use the author-checked
[parity and affine-energy argument](../charged-cubic-parity/PROOF.md) from
PR #89. They have not been independently or formally reviewed. No all-grade
rank theorem, new SAT bound or selected-result change is claimed.
Contributor: Cinna Davis, with substantial OpenAI Codex assistance.

## Result

Fix charge one and use all partitions of a label grade h as both asymmetric
label families from PR #19. The predecessor gives the scalar compressed
cubic pairing `G_h(E)=A_h+E B_h`. At grades h=6,7,8,9, the checker solves
exactly over Q for all polynomial vectors of degree at most 0,1,2 in the
kernel of this pencil. It finds:

| h | Number of labels | Kernel dimensions, degrees ≤0 / ≤1 / ≤2 | Rank at E=h |
| --- | ---: | --- | ---: |
| 6 | 11 | 0 / 0 / 3 | 8 |
| 7 | 15 | 0 / 0 / 5 | 10 |
| 8 | 22 | 0 / 0 / 7 | 15 |
| 9 | 30 | 1 / 3 / 14 | 19 |

The last column is an exact rational rank. The degree-two polynomial
vectors specialize at E=h to the full kernel in each case. Consequently,
the pencil has generic ranks 8,10,15,19 over Q(E), and its rank never
exceeds the corresponding value at any rational specialization E.
The dimensions in the middle column count polynomial vectors, not the
kernel dimension at one fixed energy; the h=9 degree-two dimension 14 is
not a claim of 14 independent specialized vectors.

An exact determinant certificate strengthens the result for **every
nonnegative integer output energy**. The checker selects a full-rank
minor at E=h and reconstructs its integer determinant polynomial from
exact values. At h=6,8,9 its nonzero coefficients have one sign and its
constant term is nonzero, so the minor never vanishes for E>=0. At h=7
its coefficients change sign exactly once; its values at E=0 and E=1
have opposite signs. Descartes' rule of signs and the intermediate value
theorem put its only positive root strictly between 0 and 1, so it is
nonzero at every nonnegative integer. Combined with the polynomial-kernel
upper bounds, the four stated ranks hold at all such output energies.
At h=7 this does **not** assert the rank at every nonnegative real E.

At E=h in all four grades, the columns indexed by partitions without a
part of size 3 are linearly independent and span the full column space.
There are exactly `p(h)-p(h-3)` such partitions. This offers a concrete
candidate for a uniform lower-bound proof, but we do not assert their
independence at other energies or grades.

All statements about the cubic operator depend on PR #89's written
low-weight/affine-energy identity. The rank data match
`p(h)-p(h-3)` at these four grades, but extrapolation to all h is open.

## Evidence and reproduction

```sh
python3 -I -B research/charged-cubic-pencil/verify.py > /tmp/charged-pencil.json
cmp /tmp/charged-pencil.json research/charged-cubic-pencil/verification.json
python3 -I -B research/charged-cubic-pencil/audit.py > /tmp/charged-pencil-audit.json
cmp /tmp/charged-pencil-audit.json research/charged-cubic-pencil/audit-verification.json
make verify
```

The standard-library checker constructs the E=0 and E=1 pairing matrices,
forms the coefficient equations for a degree-d polynomial kernel vector,
and computes complete rational nullspaces for d=0,1,2. It checks each
coefficient identity, the rank of all degree-two vectors at E=h, and the
full matrix rank there. The saved report includes all degree-two basis
vectors, selected minor rows and columns, exact determinant coefficients,
and source hashes. Interpolation uses r+1 integer evaluations for an
r-by-r minor, whose degree is at most r; a further evaluation checks the
interpolated polynomial. A separate audit reads the saved bases, checks their coefficient identities,
certifies their specialized ranks and the no-part-3 column ranks modulo a
prime, and independently recomputes every displayed minor value by rational
Gaussian elimination. These are finite computations relying on shared
predecessor operator code, not a formal proof or an independent oracle.

## Remaining gap and credit

A uniform construction of polynomial kernel vectors and matching lower
minors as h grows is still missing. Even a proof of the conjectured rank
would leave a computable normalizer, coefficient heights, both directional
cut ranks, and every reduction, query, precision, recursion, recovery,
randomness, time and space cost to be paid. The cubic removes only three
shifts and does not improve the supplied asymptotic rho.

PR #11 supplies the charged operator; PR #19 supplies its label conventions;
PR #89 supplies the parity compression and affine energy identity. This
branch is based on PR #89's exact commit `298c6603b07503fd8ccef68b39405de3e36b79a6`;
it is intentionally dependent on that open PR. The source and license pins
are retained in its [predecessor manifest](../charged-asymmetric-crossing/SOURCES.json).
