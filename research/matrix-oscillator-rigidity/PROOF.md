# Matrix-valued oscillator test

This is a changed model, not a consequence of the scalar source identity.
Take a characteristic-zero field F and a fixed number q of colours. For each
positive grade k, use commuting variables t_{k,j}, and operators

    D_-k^a = sum_j A_k[a,j] t_{k,j},
    D_k^b  = sum_j B_k[b,j] partial/partial t_{k,j},
    C_k[b,a] = [D_k^b,D_-k^a] = sum_j B_k[b,j] A_k[a,j].

Operators at different grades commute; D_0^a=0. Rows of A_k and B_k may be
singular, and numbers of variables may vary by grade. Assume the stronger
entrywise extension of the source h=1 test: for every ordered colour pair
(a,b) and every integer s, the two products have the same alternating sum,

    sum_{i=-1}^1 (1,-2,1)_i D_{-(s+i)}^a D_{s+i}^b
    = sum_{i=-1}^1 (1,-2,1)_i D_{s+i}^b D_{-(s+i)}^a.    (1)

The hypothesis at every pair is a model assumption; the scalar h=1 identity
alone does not imply it. For k>0, define G(k)[b,a]=C_k[b,a],
G(0)=0, G(-k)=-C_k^T. The difference of the two sides of (1) is minus
the entrywise second difference of G. Thus (1) for all pairs and shifts
holds exactly when G(k)=k C_1 for every integer k. Negative k then also
force `C_1=C_1^T`; equivalently

    C_k = k C, all k>=1, for one symmetric q-by-q matrix C.      (2)

Conversely (2) gives (1) directly. The zero-shift condition is essential:
without it, an arbitrary nonsymmetric C is possible at positive shifts.

## Pairing and the retained modes

Define the vacuum pairing between an annihilator word and a creator word as
its action on 1 followed by evaluation at zero. Since the two operator
families commute within themselves and commutators are scalars, this is the
usual sum over pairings, with contractions C_k and zero across grades.
Let r=rank C. Any colour vector in the right kernel of C produces a creation
operator pairing to zero with every annihilator word; any colour vector in
the left kernel produces the analogous annihilator radical. Choose invertible
row and column changes putting C into diag(I_r,0); apply the same changes at
every grade. Such independent changes are used to analyze the pairing, not
to claim that (1) is invariant under arbitrary separate colour changes. In the
resulting nondegenerate r-colour sector, the pairing of occupation monomials
is diagonal with entries `product_{k,a} m_{k,a}! k^m_{k,a}`, all nonzero in
characteristic zero. Hence the vacuum-pairing quotient has Hilbert series

    product_{k>=1} (1-z^k)^(-r).

When r>=1 it contains all ordinary partitions at every grade, so colour
mixing in this model cannot give square-index growth by removing grades.
When r=0 every positive-grade vector lies in the pairing radical. This is a
statement about this vacuum pairing, not about every possible label recovery.
Characteristic zero is necessary for nonzero k and factorials. A field of
positive characteristic requires separate analysis.

## Limits and attribution

The h=1 relation for all colour pairs is imposed, not derived from a new
vertex algebra. A useful replacement needs its own crossing identity,
nondegenerate label pairing, both directional factorizations, entries,
recursion and global cost. This package supplies no SAT algorithm, runtime
lower bound, or alpha improvement. It builds on the pinned Anthropic Appendix B
source and `research/sparse-oscillator-locality/PROOF.md`, and independently
extends the one-colour weighted screen in PR #43 (issue #30).

## Diagonal testing does not imply the all-pairs condition

The all-pairs hypothesis in (1) cannot be replaced merely by checking the
identity for the same arbitrary colour vector in both slots. For q=2 over Q,
let

    J = [[0,1],[-1,0]],  C_k = k I + k^2 J  (k>0).

Realize these matrices with A_k=I, B_k=C_k. Every C_k is nonsingular, since
its determinant is `k^2+k^4`. For any colour vector x, the scalar
commutator is `x^T C_k x = k x^T x`, because `x^T J x=0`; at negative k
it is the odd extension. Its second differences vanish, so the same-vector
h=1 relation holds for every x and every integer shift.

Nevertheless `C_2-2C_1=2J` is nonzero, so the mixed-pair relation already
fails at shift s=1. This is a concrete oscillator realization, not merely
an abstract matrix sequence. At each grade its usual vacuum pairing is
nondegenerate, yet the all-pairs two-order identity fails. No full crossing
or SAT algorithm follows from the diagonal checks.

More generally, over characteristic different from 2, diagonal tests see
only `S_k=(C_k+C_k^T)/2`: they hold for all colour vectors and all shifts
exactly when `S_k=k S_1` for k>0. The skew part can vary freely with k.
The equivalence follows from scalar second-difference rigidity applied to
`x^T C_k x` and polarization of quadratic forms. This precisely identifies
what the diagonal test omits; neither this relaxation nor the counterexample
establishes the remaining crossing and recovery identities.
