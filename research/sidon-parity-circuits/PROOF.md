# Shared XOR trees on a sparse-query family

## Statement

For every integer n >= 16 put L = floor(log2 n)-2. Let indices be
cyclic modulo n, let m_j = x_j x_(j+1), and define n quadratic equations

    P_i = XOR_{0 <= t < L} m_(i+2^t) = 0,   i in Z/nZ.

Consider a binary XOR DAG with input symbols m_0,...,m_(n-1), one
output for each *given* P_i, and internal gates that combine two
nonempty, **disjoint** sets of input symbols. A gate computes the XOR
of its two inputs. Fanout is allowed. This disjointness condition is
imposed at every gate, including gates feeding other gates; it means
that no symbol is cancelled on its way to an output. There are no
constant inputs or other operations.

Every such DAG has at least n(L-1) distinct XOR gates. This is tight:
build a separate binary tree for each row. For that tree construction,
the number of internal gate-to-gate connections is n(L-2). More
strongly, because no nontrivial gate can be shared between outputs and
within an output no gate is used twice, this same count of
input-to-output-tree gate connections applies to every DAG in this
model. Each is an individual connection in the standard per-gate
factor-network translation, before subdivision or copying.

The system is a valid instance of the sparse-query hypothesis: n rows,
L distinct degree-two monomials per row, and every variable appears in
exactly 2L-1 scopes. The source's prescribed high-incidence preprocessing
branches on no variable for n >= 16. These facts hold for the original
given equations. They do not assert anything about an altered row basis.

## Proof

All shifts 2^t are distinct as integers modulo n. Their largest positive
difference is less than 2^(L-1), and hence less than n/8. A positive
difference 2^a - 2^b with a>b has 2-adic valuation exactly b, which
identifies b, and then a. Thus all positive differences of shifts are
distinct. Opposite signed differences cannot be equal modulo n because
their absolute values sum to less than n; equal-signed differences
cannot wrap. It follows that the cyclic shift set is Sidon: if two
translates have two distinct points in common, equal differences force
the same two shift indices, and then the translates are equal. Hence
any two distinct row supports meet in at most one monomial symbol.

For a fixed output, recursively unfold its gates into a binary tree.
Disjoint gate inputs prevent a symbol from appearing twice among its
leaves. A repeated internal gate would produce repeated nonempty leaf
support, so it is impossible within that output's unfolded tree. The
L leaves are its L input symbols and therefore it contains L-1 distinct
gates. A gate used by two outputs has a support of size at least two
contained in both output supports, contradicting their intersection
bound. Summing the gate counts proves the lower bound, and separate
trees attain it. Each full tree has L-2 edges between internal gate
vertices, giving the specified n(L-2) connections. The model allows
arbitrary tree shapes and reuse of leaf input symbols; it is not limited
to a particular parenthesization.

For the original system, each row's monomials are distinct and its
variable scope is the union of adjacent pairs {j,j+1} for the selected
shifts. Among distinct powers of two, only 1 and 2 are consecutive.
As the entire shift interval lies strictly within a cyclic arc shorter
than n-1, there are no wraparound adjacencies; consequently each row
scope has 2L-1 variables. Translation symmetry implies each variable
has the same load 2L-1, so N_0=n(2L-1). With lambda=ceil(log2 n),
the source threshold is (2L-1) ceil(sqrt(lambda)), which is at least
the actual load. The criterion is strict (> threshold), so no variable
is selected for branching.

## Cost and limitations

A direct count network gives each XOR gate its three-port parity table,
each product m_j its Boolean multiplication table, and each variable a
copy/equality tree; constrain each output bit to zero. Internal bits
have unique extensions, so each satisfying x contributes exactly one.
Subdivide edges with equality tables to obtain a bipartite network.
The separate-tree construction has Theta(n L) wires and bounded-degree
local tables, with polynomial-size description and entry calculation;
unused variables (if any) can be handled separately. For exact counting,
use modulus 2^(n+1), then recover the value in [0,2^n]. The accepted
contraction theorem thus supplies an upper envelope
poly(n) 2^O(n L / sqrt(log(n L))) = poly(n) 2^O(n sqrt(log n))
for this direct construction. This is a coarser *upper bound* than the
accepted sparse-query envelope, not a lower bound on a contraction
algorithm's runtime. Its root modes, recursion, precision, and recovery
are those of the unchanged accepted theorem. The construction is
standalone: no sparsification, greedy query enumeration, randomness, or
amplification is needed for the stated family. An all-input SAT
algorithm would have to pay those outer costs and cover every candidate
query; none is provided here.

The theorem is only about the stated formal-input, cancellation-free,
per-gate circuit representation for the given rows. Gaussian row
operations, XOR gates with overlapping supports and cancellation,
nonlinear identities among the actual Boolean monomials, a larger tensor
that absorbs multiple gates, and aggregate coefficient representations
can all change the model. The rows need not be hard to solve; no time
lower bound for SAT, arbitrary sparse-query counting, general XOR
circuits, or even this family's counting problem follows. The all-size
argument is written but has not received independent or formal review.

## A changed representation solves the power-of-two subfamily

Suppose n=2^r >= 16. This particular family can be counted in polynomial
time, demonstrating the limitation of the circuit obstruction. Write
m=(m_0,...,m_(n-1)) and g(Y)=sum_(t=0)^(L-1) Y^(2^t) over F_2. The
equations form a cyclic convolution by g, with a possible reversal of
indices; reversal does not affect its kernel dimension. In
F_2[Y]/(Y^n-1), the modulus is (Y+1)^n. Since g(1)=L mod 2 and g'(Y)=1,
the gcd of g with the modulus is 1 when L is odd and Y+1 when L is even.
Thus its kernel is respectively {0} and the one-dimensional ideal
generated by (Y+1)^(n-1). For n a power of two this generator equals
1+Y+...+Y^(n-1), so the only possible monomial vectors are all zero, or
also all one when L is even.

If all m_j are zero, x is an independent set of the n-cycle. Its number
is the Lucas number L_n=F_(n-1)+F_(n+1), with F_0=0 and F_1=1.
If all m_j are one, every x_j is one, giving exactly one additional
assignment. Therefore

    # solutions = F_(n-1)+F_(n+1) + [L is even].

This count follows from the original equations, not an assumption that
the monomials are algebraically independent. Conversely, both listed
monomial vectors satisfy the parity equations under their stated parity
condition. The cycle count is the trace of the nth power of the transfer
matrix [[1,1],[1,0]]. Repeated squaring computes it with O(log n) integer
matrix multiplications on O(n)-bit integers and polynomial bit time.
The number of assignments, not merely its residue, is returned; the
algorithm is deterministic and uses polynomial space. This is a
special-family algorithm, not an all-input SAT improvement.

The companion checker independently performs GF(2) row reduction at
n=16,32,64,128,256 and checks every one of the 2^16 original x-assignments
at n=16, where the exact count is 2208. These checks support the statement
but do not replace its polynomial-gcd proof.
