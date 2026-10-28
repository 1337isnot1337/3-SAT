# Binary matroid independence has large cut rank

Author-checked all-size argument; no independent or formal review. This is a
lower bound on a specified independence predicate and separation, not on SAT
or arbitrary representations of the final hash predicate.

## Statement

Let A be a binary matrix whose columns are partitioned into ordered lists L
and R. Let U and V be their F_2 spans and let b=dim(U intersect V). Form the
0/1 matrix M with rows and columns indexed by all subsets S of L and T of R:

    M[S,T] = 1 iff S union T is linearly independent over F_2.

Then rank(M) is at least 2^b over every field of characteristic two and over
the rationals. It is enough to exhibit an invertible 2^b-by-2^b minor over
F_2; its integer determinant is odd, hence is nonzero over Q and remains
nonzero in every characteristic-two field. No claim is made here for odd
positive characteristic.

## Choosing a common-basis minor

Let E=U intersect V. Choose a subset A_L of columns in L whose images form a
basis of U/E, and a subset A_R of columns in R whose images form a basis of
V/E. They are independent, and C=span(A_L union A_R) has zero intersection
with E: U/E and V/E are disjoint in (U+V)/E. In particular the union A_L
and A_R is independent.

Complete A_L to a basis of U using b further left columns I_1,...,I_b;
complete A_R to a basis of V using b further right columns J_1,...,J_b.
Modulo C, both U and V have image exactly (E+C)/C, of dimension b. The
images of I_1,...,I_b and J_1,...,J_b each form a basis of this common
space. These selections can be constructed by Gaussian elimination.

Restrict M to rows that select every column of A_L, any subset S of the I
columns, and no other left column; similarly fix A_R on the right, allow a
subset T of J, and set all other right columns to zero. Because the fixed
columns are independent, the selected columns are independent iff the
images of I_S and J_T are independent in the quotient by C. Choose the I
basis as coordinates, and write the J basis as the columns of an invertible
binary b-by-b matrix H.

## The minor is invertible

For each row S replace its index with R=[b] minus S, and order rows by |R|
and columns T by |T|, both increasing. An entry vanishes if |T|>|R|, because
more than b vectors are selected. Therefore the minor is block lower
triangular, with a square block for each k=0,...,b. For |R|=|T|=k, the
entry is det(H[R,T]) in F_2: after eliminating the selected I columns,
the remaining k-by-k determinant is exactly that minor of H. Over F_2 its
value equals the Boolean independence indicator.

The kth diagonal block is the matrix of the kth exterior power of H (the
compound matrix of its k-by-k minors). It is invertible because the exterior
power of H inverse is its inverse; the k=0 block is [1]. Every diagonal block
is invertible, so the entire 2^b-by-2^b matrix is invertible over F_2. The
case b=0 gives the 1-by-1 minor [1]. This completes the proof.

## Consequences and limits

A sum of r products f_j(S)g_j(T) over either stated field has matrix rank at
most r. Hence any exact two-sided decomposition of this independence table
requires r>=2^b. In a linear chain with independent-set selection bits
assigned to their respective sides and w Boolean bond bits crossing this
cut, summing bond assignments gives at most 2^w separable terms, so w>=b.
This applies to arbitrary entries and cancellations in that specified chain,
not merely the canonical subspace-state encoding of PR #37.

For a sequence of m selection bits, add these lower bounds across the m-1
chain cuts. The distance/nullity argument of PR #55 at commit 0264a0c gives
sum_i b_i>=k(D-1) when the binary kernel has dimension k and minimum nonzero
weight at least D>=2. Briefly, partition the order into blocks shorter than
D, so every block is independent; the prefix nullity gained in each block is
at most the width at its start. Shift the blocks through each residue modulo
D-1 and sum. Thus the total number of Boolean bond-bit incidences in any
such exact independence chain is at least k(D-1). This is tight for disjoint
circuits, as shown in PR #55.

For the accepted sparse checks, if m>P and K=max(0,m-3n-t), appending t
rows preserves minimum distance at least ceil(m/P) and leaves nullity at
least K. Therefore every exact chain of this kind needs at least
K(ceil(m/P)-1) >= K m/(2P) bond-bit incidences. In the conditional regime
m=Theta(n), K=Omega(m), P=polylog(n), this is Omega(n^2/polylog(n)). The
row-count condition is not asserted for all leaves. This is a lower bound
for an explicitly described chain computing the independent-set coefficient
predicate; it does not rule out a different network, shared nonlocal bonds,
a computation of the summed kernel predicate after cancellation, changed
hashing, or another SAT algorithm. It does not establish a SAT lower bound.
The full costs and embedding of any proposed algorithm remain open.
