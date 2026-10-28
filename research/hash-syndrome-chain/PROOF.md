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
