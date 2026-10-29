# Shift-dependent local input maps: the active algebraic question

No improved SAT bound is proved. This changes the input-side freedom in the
length-block experiment; it does not promote its finite witnesses.

## Exact sufficient condition

Let V_h have its partition basis of size N=p(h). For every retained shift
|s|>c and every charge degree 0<=d<=2h, write C_(d,s)=[q^d]Q_s(q).
For a source row label mu, regard C_(d,s)(mu,nu,y,u) as a vector indexed by
(nu,y,u). Let W be the rational span of all these vectors. Define the
N-dimensional scalar row space

    S = { (g_nu delta_yu)_(nu,y,u) : g in Q^N }.

If S is contained in W, rational matrices A_(d,s) exist such that

    sum_(d,s) sum_mu A_(d,s)(x,mu) C_(d,s)(mu,nu,y,u)
        = delta_xnu delta_yu.

This follows by solving independently for each scalar row. The map A acts
only on the x input axis, so it increases neither required flattening rank.
This allows a different local input map for each shift and charge degree,
not merely scalar weights or projections onto lengths.

Each C_(d,s) is a rational combination of 2h+1 evaluations Q_s(q), by ordinary
polynomial interpolation at distinct integer charges. Consequently its two
ranks are at most 2h+1 times their predecessor bounds. There are O(h^2)
coefficient pieces, or O(h^3) evaluated pieces. These are polynomial factors
in h, hence add only O(log h) to a factor bit count. The entire rational
linear system has exp(O(sqrt(h))) rows and columns, as do its input integers'
bit lengths under a crude determinant estimate. Thus direct exact algebra
fits exp(O(sqrt(h))) bit time and space; it is not a polynomial-space claim.
The predecessor rational transfer, good-prime handling and complete outer
algorithm would still need to be applied to any proved uniform family.

Taking c=floor(h/2) and h minimal with p(h)>=2^lambda would give the same
conditional rho and alpha target as README.md, if this containment held at
all sufficiently large grades with the necessary uniform contracts. The
containment is currently unproved. It is also sufficient to recover a scalar
row subspace of dimension exp(kappa sqrt(h)-O(log h)), normalize a minor and
retain an output codebook of that leading capacity. That weaker condition is
also unproved uniformly.

## Verified finite evidence

The full input and output spaces, with c=floor(h/2), give:

| h | p(h) | retained coefficient rows | modular span rank | scalar rows recovered |
|---|---:|---:|---:|---:|
| 4 | 5 | 364 | 118 | 5 |
| 5 | 7 | 852 | 328 | 7 |
| 6 | 11 | 1752 | 854 | 11 |
| 7 | 15 | 3408 | 1702 | 15 |
| 8 | 22 | 6112 | 3314 | 22 |

At h=4 and h=5 the script additionally solves over Q and verifies EVERY
original tensor equation. The saved rational maps are actual finite
crossings. The larger rows are modulo-65521 screens only. Modular rank
agreement alone is not a rational existence certificate, and a discrepancy
is not asserted to be rational nonmembership. All operator data reuse the
pinned predecessor recurrence; this is not an independent operator oracle.

The grades 4 and 5 solutions returned by this elimination order happen to
use only the all-ones source row. That family alone has only polynomially
many available coefficient vectors and cannot supply full leading partition
capacity asymptotically. Thus the small solutions do not justify an induction.
A separate source-row restriction to partitions without ones gives scalar
row dimensions 10 of 11 at h=6 and 16 of 22 at h=8, modulo 65521. Those
screens suggest looking at the whole source module, but establish no growing
capacity. They are scratch evidence, not part of the rational certificates.

Reproduce one grade using python-flint 0.9.0:

    python -B research/length-block-filter/left_mixing.py 5 2

The grade-eight run uses substantial memory and minutes; it is deliberately
not in default CI. No additional finite grades are a substitute for proving
the scalar row containment or a sufficient growing-dimensional substitute.

## Next proof obligation

Characterize a linear functional annihilating every retained coefficient
row. To prove full containment it suffices to show that such a functional
annihilates every scalar row. Equivalently, if every row-label generating
Laurent polynomial obtained from that functional is supported entirely in
[-c,c] for every charge, prove its output-diagonal traces vanish. This is an
all-size algebraic statement; it is the current missing theorem.

Credit: charged-operator-moments, charged-asymmetric-crossing and
charge-polynomial-filter supply the operators, rank factorizations and
polynomial recurrence. The broader local input maps and this row-space
criterion are the changed premise of this checkpoint.
