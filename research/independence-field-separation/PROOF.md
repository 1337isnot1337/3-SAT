# Sharp field-dependent rank of binary independence tables

Author-checked all-size proof; no independent or formal review. This concerns
one matroid representation interface, not a general SAT lower bound.

## Statement

For an arbitrary binary matrix split into left and right columns, let
E be the intersection of their spans and let b=dim E. Write N_b for the
number of subspaces of F_2^b. The Boolean independence table across the cut
has rank at most N_b over any field. There is a binary matrix, with two
copies of every nonzero vector in F_2^b split one copy per side, whose table
has rank exactly N_b over the rationals and every field of odd characteristic,
and rank exactly 2^b over every field of characteristic two.

The bounds

    2^floor(b^2/4) <= N_b <= 2^(floor(b^2/4)+b)

show the rank separation is 2^(b^2/4+O(b)) versus 2^b; the stronger
constant-factor estimate below sharpens the first exponent to b^2/4+O(1). For b=0, use the
empty matrix and N_0=1. The construction has 2(2^b-1) columns; the claim is
not a lower bound in terms of an unrelated input length or a different cut.

## General upper bound

If a selected side is dependent its entire row or column of the independence
table is zero. Otherwise let X be the selected left span intersected with E
and Y the corresponding selected right span. Their union is independent iff
X intersect Y={0}. A row is therefore determined by its X, or is the zero
row. There are at most N_b choices for X, so the table has rank at most N_b
over every field. This is the subspace-state interface from PR #37, stated
here as a rank bound.

## The subspace-disjointness matrix

For the two-copy matrix, fix for every subspace X of F_2^b an independent
subset of its nonzero vectors that forms a basis of X; use the corresponding
left and right subsets as row and column indices. The resulting N_b-square
minor has entries

    D[X,Y] = 1[X intersect Y={0}].

Order all subspaces by nondecreasing dimension and let Z[X,W]=1[W subset X].
Then Z is triangular with diagonal one, hence invertible over every field.
Define

    mu(W) = (-1)^d 2^(d(d-1)/2),  d=dim W.

The finite subspace-lattice identity

    sum_(W subset H) mu(W) = 1[H={0}]                    (2)

holds over the integers. To see this, let [d j]_2 count j-dimensional
subspaces of a d-dimensional binary space. The standard counting recurrence
`[d j]_2 = 2^j [d-1 j]_2 + [d-1 j-1]_2` gives, by induction,

    sum_j [d j]_2 (-1)^j 2^(j(j-1)/2) t^j
        = product_(r=0)^(d-1) (1-2^r t).

At t=1 this is zero for d>0 and one for d=0, proving (2). Consequently

    D = Z diag(mu(W)) Z^T                                  (3)

as an integer identity. The factorization is standard Möbius inversion on
subspaces; no novelty or priority is claimed for it.

In odd characteristic every diagonal entry of (3) is nonzero, and likewise
over Q, so D has full rank N_b. Together with the general upper bound this
gives equality for the full independence table. In characteristic two,
mu(W) is nonzero exactly for dimensions 0 and 1. There is one zero subspace
and 2^b-1 lines, so (3) has rank exactly 2^b. PR #104 independently gives
the matching upper bound 2^b for every binary matroid in characteristic two;
hence the full table also has rank exactly 2^b in that characteristic.

## Size of N_b and implications

Taking k=floor(b/2), the row spaces of the matrices `[I_k | C]` for all
binary k-by-(b-k) matrices C are distinct, giving N_b>=2^(k(b-k)). The
unique reduced-row-echelon basis of any j-dimensional subspace has at most
j(b-j) free bits for each pivot set. Summing over pivot sets gives
N_b<=sum_j binom(b,j)2^(j(b-j))<=2^(floor(b^2/4)+b).

Thus PR #37's subspace labels are optimal in worst-case rank for odd
characteristic and Q, while the cancellation-based characteristic-two chain
of PR #104 is exponentially smaller in b. This is a lower bound on the
number of terms in any exact separable decomposition across this specified
cut, by matrix rank; it does not bound arbitrary graph topologies or the
complexity of a SAT instance. It does not imply that every binary matrix has
large rank, or that an all-order chain must incur this separation.

## Prime-power extension

The same proof applies to a matroid represented over F_q, q=p^r, and a
(possibly unrelated) coefficient field K. Let N_(q,b) be the number of
F_q-subspaces of a b-dimensional intersection. For every cut, the table
rank is at most N_(q,b). If char(K)=p, factorization (3) with

    mu_q(W)=(-1)^d q^(d(d-1)/2)

gives the sharper universal upper bound

    1 + (q^b-1)/(q-1),

because only dimensions 0 and 1 survive in K. To apply the factorization to
an arbitrary cut, map independent row and column selections to their
intersection subspaces and discard dependent ones; the resulting table is a
submatrix of the full subspace-disjointness matrix, with repetitions and
zero rows or columns allowed.

For two copies of one representative of every one-dimensional subspace of
F_q^b, each possible subspace has a chosen basis on each side, so the full
subspace-disjointness matrix is a minor. Its zeta factorization is invertible
on both sides. In characteristic p its rank is exactly the displayed bound;
if char(K) differs from p, including characteristic zero, every mu_q(W) is
nonzero and its rank is N_(q,b). These ranks are therefore exact for this
configuration. The matching-characteristic upper bound need not be exact
for every representation: two copies of a basis of F_3^2 have cut rank 4
over F_3, while the universal bound is 5. The identity for mu_q follows from the same Gaussian-binomial
recurrence and product with 2 replaced by q.

The binary theorem is the q=2 case. The extension is a representation-field
statement, not a use of nonbinary checks in the accepted 3-SAT algorithm.

## Constant-factor subspace asymptotics

For each fixed q>=2, in fact N_(q,b)=Theta_q(q^floor(b^2/4)). The lower
bound follows from the same `[I_k | C]` construction over F_q. For the
upper bound, counting ordered bases gives

    [b j]_q = q^(j(b-j)) product_(h=1)^j
                (1-q^(-(b-j+h)))/(1-q^(-h))
            <= C_q q^(j(b-j)),
    C_q = product_(h>=1) (1-q^(-h))^(-1) < infinity.

The infinite product converges because sum_h q^(-h) converges. Put
k=floor(b/2); as j moves away from k, floor(b^2/4)-j(b-j) is at least
`d(d-1)` for d=|j-k|. Hence

    N_(q,b) <= 2 C_q (sum_(d>=0) q^(-d(d-1))) q^floor(b^2/4).

The displayed constant depends only on q. In particular, the binary
odd-characteristic and rational rank is exactly 2^(floor(b^2/4)+O(1)),
while its characteristic-two rank is exactly 2^b. Writing the binary example's number of columns as m=2(2^b-1), its
characteristic-two rank is exactly m/2+1, whereas its rational and odd-field
rank is 2^((log_2(m/2+1))^2/4+O(1)). This compares the ranks for the same
explicit table and same split. It does not change the fixed-cut or
no-SAT-lower-bound scope.
