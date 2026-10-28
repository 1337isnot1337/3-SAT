# Independence polynomial as a kernel weight enumerator

Author-checked all-size argument, awaiting independent review. It uses the
accepted OpenAI contraction theorem as a premise. No SAT improvement is
claimed. Let A be an a-by-m binary matrix, with h nonzero entries, and K a
field of characteristic two. Let

    I_A(z_1,...,z_m) = sum_{S independent} product_{j in S} z_j,

where independence refers to the corresponding binary columns.

## Polynomial identity

For arbitrary field elements z_j, including non-Boolean values,

    I_A(z) = sum_{x in {0,1}^m : A x=0}
             product_{j:x_j=1} z_j product_{j:x_j=0} (1+z_j).   (1)

This is Boolean interpolation in characteristic two. To see it directly,
the coefficient of the monomial z_S on the right is the parity of the
number of kernel vectors supported inside S. That number is
2^(|S|-rank(A_S)); its image in K is 1 when A_S has independent columns
and 0 otherwise. This proves equality as a formal multilinear polynomial,
not merely at Boolean points. The identity is a rearrangement of the shared
independent-set / kernel-indicator relation in PR #2; no priority is claimed.

## Equality of the two cut ranks in characteristic two

At any cut, index the kernel predicate truth table H by left and right
Boolean bit vectors, and the independence table C by the corresponding
selected sets. The coefficient argument above gives

    C[S,T] = sum_(x subset S, y subset T) H[x,y] in K.

Thus C=Z_L H Z_R^T, where each Z is the Boolean subset-inclusion matrix.
Ordered by inclusion, these matrices are triangular with diagonal one and
therefore invertible over K. The kernel table has rank exactly 2^b, where b
is the intersection dimension of the two column spans: equal prefix and
suffix syndromes yield 2^b disjoint rank-one blocks, each nonempty. Hence
C also has rank exactly 2^b. This is an independent derivation of PR #104's
characteristic-two cut-rank identity from the kernel predicate; the Boolean
zeta transform is invertible, not a rank-losing substitution. The identity
uses characteristic two when converting the kernel truth values to
independence coefficients, and is not an odd-characteristic claim.

## A sparse nonlocal tensor network

For each input bit x_j use a bounded-degree equality tree to distribute it
to the h row occurrences and to a weight factor. To enforce one row of A,
connect the corresponding occurrences to a binary XOR accumulator:
ternary 0/1 tensors require p_next=p_old+x_j over F_2, with endpoints fixed
to zero. A row of weight zero contributes one; singleton rows have unary
zero constraints. Each row input has a unique extending accumulator path
if its parity is zero, and none otherwise. Zero columns remain free bits.
The network has O(m+a+h) wires and vertices, with all Boolean factors of
arity at most three. This does not assume a bound on row or column weight.

Each bit's local weight is z_j for x_j=1 and 1+z_j for x_j=0. Multiplying
and summing over all internal Boolean wires yields the right side of (1).
Factor entries are computable in time polynomial in A and the weights;
there is no enumeration of independent sets in the network description.

## Accepted contraction with grouped weights

Let s=m+a+h>=2 and suppose the supplied field has degree e=O(log s) over
F_2, represented by a monic irreducible degree-e polynomial. Partition
indices into at most J=ceil(s^(1/5)) groups of size at most ceil(m/J)
(use singleton groups if m<J). Replace the individual weight factors by one
factor per group, evaluating the product of that group's local weights in
K. Its arity is O(s^(4/5)+1), while every other factor has arity at most
three. This adds O(m) wires. Subdivide every edge by a binary equality
factor: the resulting graph is bipartite, has O(s) wires, and has polynomial
size description and polynomial-time/space entry routines.

Use the field lift from PR #2: evaluate each group factor in K and lift its
canonical polynomial representative to

    B = F_2[V]/(V^ell),  ell=J(e-1)+1,  P_0=1.

Every other factor has constant 0/1 entries. Each contraction summand has
degree at most J(e-1), so truncation loses nothing. After summing, reduce
modulo the field polynomial to obtain the exact K value. The representative
map itself is not asserted to be a homomorphism. Since ell=O(s^(1/5)log s)
is O(s), and the maximum degree is eventually at most s^(9/10), the accepted
`thm:tensor-contraction` applies with size parameter s. The evaluation uses

    (s+L)^O(1) 2^O(s/sqrt(log s)) bit operations

and polynomial space, where L is the total description length. Any small
exception can be evaluated by enumerating 2^m subsets or kernel words. If the
field itself must be constructed, e=O(log s) permits the deterministic
polynomial-time irreducible-polynomial search used in PR #2. For fixed field
degree the same bound applies. The procedure evaluates one polynomial at one
specified point; many points, constructing A, and any surrounding SAT
reduction must be charged separately.

## Separation from a fixed ordered chain

Take A=[I_b | I_b] with all first-copy columns ordered before the second.
Then m=2b, a=b and h=2b, so the nonlocal network above has O(b) wires. At
the successive cuts the span-intersection widths are
0,1,...,b-1,b,b-1,...,1,0, whose sum is b^2. PR #104 proves exact rank
2^width for each independence cut in characteristic two; every exact
ordered Boolean-bond chain for this ordering therefore has at least b^2
bond wires. Interleaving paired columns instead has width at most one, so
this example does not prove an all-order separation. It establishes that
the nonlocal topology bypasses the cost of this particular ordering, and
that (1) works at arbitrary field points, not only Boolean inputs.

## Limits

This is a polynomial-evaluation interface for an explicitly supplied A. The
underlying source clause-violation vector can have m much larger than n;
O(m+a+h) wires can still exceed the n log log n envelope. To obtain a full
SAT improvement one must specify the matrix and all clauses, construct every
query, integrate weighted variables and validity constraints, account for
sparsification branches, field and randomness costs, output recovery and
space, and show a uniformly smaller total bound. Neither the identity, the
finite checks, nor a cheap example establishes such a result. In particular,
no lower bound on arbitrary SAT algorithms follows from the chain comparison.

## Fixed prime-power extension

Let A be represented over F_q with q=p^r, and let K be any field of
characteristic p. The same coefficient count proves

    I_A(z) = sum_(x in ker_Fq A)
             product_(j:x_j!=0) z_j product_(j:x_j=0) (1+z_j) in K[z].

Indeed, the coefficient of z_S is the image in K of
q^(|S|-rank_Fq(A_S)), which is one for independent S and zero otherwise.
The characteristic condition matters: for binary parallel columns A=[1 1]
and z_1=z_2=1 over F_3, the independence polynomial is 0 but the weighted
kernel sum is 2. No mismatched-characteristic identity is claimed.

For fixed q=2^r and K=F_(2^e), encode each x_j by r Boolean bits in a
fixed F_2 basis of F_q. Multiplication by each fixed matrix entry is an
r-by-r binary linear map; row constraints become r systems of binary parity
checks and can be implemented by degree-three XOR and equality tensors.
Their total wires are O_q(m+a+h), with polynomial-time descriptions and
entries. The local weight selects z_j if any of the r bits is nonzero and
1+z_j otherwise. Group at most J=ceil(s^(1/5)) such weight factors as above,
where s=m+a+h, and use the same field lift. For fixed q and e=O(log s),
all wire, degree and ring hypotheses hold, giving the same accepted-theorem
complexity up to q-dependent constants. For odd p the formal identity
still holds, but the two-adic contraction application is not asserted.
For a left/right cut, the q-ary kernel truth table H has rank exactly
q^b over any coefficient field, where b is the intersection dimension of
the two represented spans: its common-syndrome blocks are disjoint and
nonempty. In characteristic p the coefficient table is

    C[S,T]=sum_(support(x) subset S, support(y) subset T) H[x,y].

This is a rectangular support-aggregation transform of H. When q=2 it is
the invertible Boolean zeta transform above; when q>2 it need not preserve
rank. For A=[1 1] over F_3, the kernel table is a 3-by-3 permutation matrix
of rank 3 over F_3, while the 2-by-2 independence table has rank 2.

This is a general matroid-polynomial component and does not replace the
binary sparse hashes in the SAT reduction.

## A sparse-matroid parity corollary

For a binary matrix with a+h=O(m) and polynomial-size input description,
s=Theta(m). The accepted theorem and the network above therefore give a
deterministic polynomial-space evaluation of I_A at one point of a field
of degree O(log m) in

    poly(m) 2^O(m/sqrt(log m))

bit operations. Moreover, put every weight equal to t. Then
I_A(t,...,t)=sum_(k=0)^m c_k t^k, where c_k is the parity of the number
of k-element independent sets. Construct F_(2^e) with 2^e>m, evaluate this
polynomial at m+1 distinct field points sequentially, and interpolate its
coefficients. Standard finite-field interpolation and the m+1 evaluations
add only polynomial time and space factors. The outputs c_k lie in F_2.
Thus all independent-set size parities have the same stated asymptotic time
and polynomial-space guarantee under the accepted theorem. The extension
to fixed q=2^r matroids has q-dependent constants and still reports parity.
This is a consequence for explicitly sparse matroid representations; it
is not an improvement to the selected general 3-SAT theorem.

## Row-space preprocessing

The independence polynomial is determined by ker(A), so replacing A by any
binary matrix B with the same row space leaves the polynomial and kernel
weight enumerator unchanged. Equality of row spaces is decidable by Gaussian
elimination: it is equivalent to rank(A)=rank(B)=rank([A;B]). Thus an
explicit proposed B can be verified in polynomial time, after which the
network size is s_B=m+rows(B)+ones(B). The original input length remains in
L and in the polynomial preprocessing/description factor; a sparse B does
not make reading a dense A free.

Two unconditional polynomial-time candidates are useful. First, sort the
original rows by Hamming weight and greedily retain a row when it increases
rank. The retained rows form a minimum-total-weight basis among subsets of
the supplied rows, by the standard vector-matroid greedy exchange argument.
Second, compute the binary reduced row-echelon basis. Choose the candidate
with fewer ones. Both have rank(A) rows, span the same row space, and have
at most as many ones as the original matrix because the first candidate is
a subset. They do not necessarily minimize the weight of a basis allowed
to use arbitrary linear combinations. The equality check and both candidate
constructions take polynomial time and space; their resulting s_B may be used
in the accepted-contraction bound while L still accounts for A.

For a concrete reduction, take even n and let B=I_n+J_n over F_2, where
J_n is all ones. Since B^2=I_n+n J_n=I_n, B is invertible. The n-by-2n
matrix A=[B | B] has 2n(n-1) ones, but its reduced row space has basis
[I_n | I_n] with 2n ones. Thus the network parameter falls from Theta(n^2)
to Theta(n) after polynomial-time row reduction. This example is easy even
without contraction: its independence polynomial is
product_i(1+z_i+z_(n+i)). It demonstrates a valid preprocessing gain, not
an unrestricted SAT improvement or a guarantee for source hash matrices.
A genuinely smaller complete SAT bound would require proving a uniformly
small equivalent representation for the relevant checks while paying all
clause, branch and query costs.
