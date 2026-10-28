# Exact syndrome chains and a sparse-row alternative

Author-checked; no independent or formal review. No SAT speedup is claimed.
All variables z in the statements below are Boolean selection bits.

## Exact cut rank

Let A have binary columns v_1,...,v_m, let U_i and F_i be the spans of the
first i and last m-i columns, and put E_i=U_i intersect F_i and b_i=dim E_i.
For the Boolean function f(z)=1[Az=0], form its flattening across cut i.
The prefix and suffix syndromes must be equal. For every e in E_i define
functions l_e(x)=1[A_L x=e] and r_e(y)=1[A_R y=e]. Then

    f(x,y) = sum_{e in E_i} l_e(x) r_e(y)

as an integer identity, and hence over any field: at most one term is one.
Every e has a prefix and suffix preimage. Selecting one of each gives an
identity submatrix of size |E_i|=2^b_i. The sum gives an upper rank bound
of the same size. Thus the cut rank is exactly 2^b_i over **every** field.

## An optimal ordered syndrome chain

Fix a basis of E_i at each cut, computable by binary Gaussian elimination.
Use b_i Boolean wires to encode a syndrome s_i in E_i. The initial and final
states are zero. At step i+1, given selection z_(i+1), accept a transition
exactly if

    s_(i+1) = s_i + z_(i+1) v_(i+1)  in F_2^a.

The encoded next state is automatically required to be in E_(i+1). Each
valid full input z has one state path, namely its running syndromes, if
Az=0, and no state path otherwise: a globally zero syndrome makes every
prefix syndrome the suffix syndrome, while the final zero state forces
Az=0. Hence summing the product of 0/1 transition tensors over all internal
state bits gives f exactly over every field. State bits total sum_i b_i;
a transition has b_i+b_(i+1)+1 ports, and its entry is computable in
poly(a,m) time from the supplied bases. Descriptions and bases are polynomial
in the binary matrix size.

Any exact ordered chain separating its selection bits at the same cuts with
w_i Boolean bond wires has a cut factorization of rank at most 2^w_i. Thus
w_i>=b_i at every cut over any field, and this chain minimizes total Boolean
bond-wire count among those chains. Larger bond alphabets are charged by the
logarithm of their total size. This statement is about that ordered chain
interface; a general nonlocal tensor network has a different cut structure.

The predecessor identity expresses 1[Az=0] as a sum of independent-set
monomials in characteristic two on Boolean z. This chain computes the
**summed Boolean function**; it does not compute the independent-set
coefficient table or assert equality after substituting arbitrary field
values for z. When z_j is linked to a Boolean clause-violation bit, the
identity is evaluated only on its valid Boolean values.

## Direct sparse row network and Boolean clause wiring

Write a for the number of rows and h for the number of ones of A. Use one
parity-check tensor per row, with one port for each nonzero in that row. It
is one iff the sum of its input bits is zero modulo two. Connect the h row
ports to Boolean z_j bits with equality-copy trees of degree at most three.
Fix degree-zero copies as needed. This realizes exactly 1[Az=0] over any
field: for fixed z each copy tree has one valid internal assignment, and
all row factors are Boolean. The row tensors have at most the row weight
as arity, entries computable in linear time in that weight, and the network
has O(a+m+h) wires and vertices, including unused or empty rows/columns.

If z_j is the violation bit of a width-k Boolean clause in n variables,
attach its (k+1)-port truth-table tensor and use bounded-degree equality trees
to distribute each x_i to its clause occurrences. Add one unary weight
factor w_i^{x_i} per original variable. Summing Boolean internal assignments
produces

    sum_{x in {0,1}^n} (product_i w_i^{x_i}) 1[A v(x)=0],

where v(x) is the clause-violation vector. This holds over any field; in
characteristic two it is the weighted fingerprint of the predecessor for
the hashed system. Its network has O(n+km+a+h) wires and vertices and
maximum factor arity max(3,k+1, maximum row weight). Tensor entries and
descriptions are computable in polynomial time in the listed input and
weights. Repeated literals, tautologies, empty rows and unused variables
are interpreted by their literal truth tables; no uniqueness of clauses is
required. This is an exact network construction, not an implementation of
the accepted contraction solver.

For the source initial checks plus the decision wrapper's t extra rows,
a<=3n+t, each initial row has at most D_0 ones, and each extra row has at
most 2P ones, so h<=3n D_0+2Pt. At the predecessor's polylogarithmic B,P,D_0
and t=O(n), the network size is n polylog(n). This alone does not reach
the desired O(n log log n) arbitrary-density wire envelope. To use any
contraction theorem, all its ring, description, degree, precision, recursion,
recovery and randomization hypotheses and all sparsification branches must
still be checked and paid. No improvement is asserted.

## Consequence of distance and nullity

The proof in PR #55, head 0264a0cf35da09f4abab4118dc870aed121fa167,
gives sum_i b_i >= k(D-1) for binary kernel dimension k and minimum nonzero
kernel weight at least D>=2; it partitions columns into short independent
blocks at every offset. Thus an exact ordered syndrome chain has at least
k(D-1) bond wires, and no other exact chain with the same ordered cut model
can do better. For the accepted sparse checks with t appended rows, m>P,
and K=max(0,m-3n-t), this is at least K(ceil(m/P)-1). In the conditional
regime K=Omega(m), m=Theta(n) and P=polylog(n), that is
Omega(n^2/polylog(n)). The sparse row network above uses a different,
nonlocal topology and may be much smaller. The row-count condition may be
vacuous on some leaves; this says nothing about a generic lower bound on
SAT or about networks after substituting restricted violation patterns.

## A source-sparsifier leaf with too many individual inputs

The row network keeps each clause-violation bit as an individual binary
input. Under the accepted distance guarantee, if m>P, every column of A^(0)
is nonzero: a zero column would give a weight-one kernel vector. Appending
rows cannot turn a nonzero column into zero. Hence for every j, the free-bit
function f(z)=1[Az=0] satisfies f(0)=1 and f(e_j)=0, so it depends on all m
input bits. Any exact binary-port network with these m independent inputs
must connect each input at least once; the explicit row construction has at
least m input incidences. This is a representation cost, not a lower bound
for arbitrary encodings or for the original formula after substitution.

This is not vacuous for the source sparsifier's leaf conditions. Let
lambda=ceil(log_2 n), t=floor(lambda^(1/4)), and for sufficiently large n
consider all distinct width-two clauses

    (not x_i or x_(i+j)),  i in Z/nZ, 1<=j<=t.

There are exactly m=nt non-tautological clauses, with no repeated or
strictly containing clauses. Every signed literal occurs in exactly t of
them. In the source's k=3 sparsifier, sigma=1/ceil(sqrt(lambda)); its
chosen threshold M obeys M>=1/sigma, since its stopping inequality has
Gamma>=1 and h>=1. Therefore t<M. The only nonempty proper subsets of a
width-two clause are single literals, so the source's branch condition
never triggers: the normalized formula itself is a leaf. Its m exceeds
n ceil(log_2 lambda) eventually, and hence it lies beyond the source's
simple clause-network threshold. The source choice also has M=poly(lambda),
so B=poly(lambda), P=poly(lambda), and m>P for large n. Consequently a
free-violation-bit row representation of this leaf uses at least
n floor(lambda^(1/4)) individual input incidences, asymptotically more than
n log log n.

The family is deliberately easy: the j=1 implications form a directed
cycle, forcing all variables equal; exactly the all-zero and all-one
assignments satisfy it. The actual violation vectors are therefore highly
restricted, and simplifying the formula or using an alternative encoding can
avoid this representation. The example does not give an input or time lower
bound, does not preclude a faster algorithm, and does not assert that the
source code's particular output matrix is unique.

## Fitting grouped field weights into the accepted ring

For the sparse-row network, the accepted contraction theorem can be applied
under explicit source-regime parameters; the following is a cost accounting
for one hashed leaf, not a faster SAT bound. Take n>=2, fixed k, m<=Bn,
B=polylog(n), a<=3n+t with t=O(n), initial row weights at most D_0=polylog(n)
and extra row weights at most 2P=polylog(n). Let

    s = n+km+a+h,  h = number of ones of A.

Construct the Boolean network above, but group the n fingerprint weights
into J=ceil(n^(1/5)) groups, each of size at most ceil(n/J). A group tensor
on those variable bits has entry product_i w_i^(x_i), evaluated in a field
F of size 2^e>=6n with e=O(log n). The original variable bits reach their
clause gates and exactly one group tensor through equality trees. All other
tensors have entries in {0,1}. This adds only O(n) wires and has group
arity O(n^(4/5)); the row, clause and equality arities are respectively
polylog(n), k+1 and 3. Since s>=n, all degrees are eventually at most
ceil(s^(9/10)). Insert a binary equality tensor on every network edge to
make the graph bipartite, doubling the edge count and leaving these arity
bounds unchanged. Isolated scalars can be multiplied separately.

Choose a monic binary irreducible polynomial f of degree e, as in PR #2.
It and field operations are deterministically constructible in polynomial
bit time at this e. Evaluate each group entry in F, then use its canonical
degree-less-than-e polynomial representative as the tensor entry in

    B = F_2[V]/(V^ell),    ell=J(e-1)+1,    P_0=1.

Every term in the contraction contains exactly J group entries and all
other factors are constants 0 or 1. Its polynomial degree is at most
J(e-1), so truncation loses no information. Sum in B and reduce modulo f
at the end; evaluation of all group entries followed by this reduction is
the exact F-valued fingerprint. In particular no claim is made that the
canonical representative map itself is a field homomorphism. Since
J(e-1)+1=O(n^(1/5) log n)=O(s), the accepted theorem's ell<=Cs condition
holds. Descriptions are polynomial in the matrix and weight input, all
entries are computed in polynomial time and space, and the graph has O(s)
edges and polynomially many vertices. The theorem yields deterministic
exact evaluation of the one weighted hashed fingerprint in

    (s+L)^O(1) 2^O(s/sqrt(log s)) bit operations

and polynomial space, where L is its description length. For the source
rows h<=3nD_0+2Pt and s=n polylog(n). Finite exceptional n or parameter
cases can use direct enumeration. Computing A and the t random rows, all
random-bit costs, every sparsification leaf, the false-positive and
fingerprint errors, and the leaf traversal still belong to the outer
algorithm; the predecessor wrapper supplies these separately. This
construction does not claim a better total bound, since s=n polylog(n)
can exceed n log log n and the input-incidence example above prevents a
uniform O(n log log n) bound for this particular free-input network.
