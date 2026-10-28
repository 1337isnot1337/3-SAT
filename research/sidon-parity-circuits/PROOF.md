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

## An arbitrary-size kernel-parameterized count

The same change of representation applies to every n >= 16. Let

    h(Y) = gcd(g(Y), Y^n-1),    d = deg h,
    n_odd = n / 2^v2(n),       D = gcd(n_odd, 2^L-1).

There is a deterministic exact counting algorithm using
`poly(n) 2^d` bit operations and polynomial space, with `d <= D`.
Its cost is polynomial for every subfamily with `d=O(log n)`. In
particular, if D=1, the Lucas formula above holds verbatim, even if n
is not a power of two. For example, n=3*2^r with even r has
L=r-1 odd and D=1, giving an infinite non-power-of-two subfamily.
These are conditions on this special family, not on general queries.

To prove the count, write f=Y^n-1 and q=f/h. If the coefficient
convention reverses g, replace g by the reversal Y^deg(g) g(Y^-1);
this is a unit times the original under cyclic reversal, so d is the
same. The convolution kernel consists exactly of polynomials qv with
`deg v<d`: after dividing g and f by h, the quotients are coprime,
forcing q to divide every kernel element. Conversely, every such
multiple is in the kernel. All qv have degree <n and are distinct, so
this lists precisely 2^d cyclic vectors m.

For each vector m, count its Boolean preimages x by the trace of the
ordered matrix product

    product_(j=0)^(n-1) A_(m_j),
    A_0=[[1,1],[1,0]],  A_1=[[0,0],[0,1]],

where A_b[a,c]=1 iff a*c=b. This product enforces every adjacent
relation and the cyclic boundary; its trace counts each labeled x
exactly once. Summing the 2^d traces counts precisely the solutions.
Binary-polynomial gcd, division and kernel generation use polynomial
bit time and space; each matrix entry is at most 2^n. Enumerating v
sequentially gives the stated worst-run cost and polynomial space.
No randomness, amplification, outer reduction, or contraction is used
for this special-family algorithm.

For the bound on d, g'=1, so g and h are squarefree. In characteristic
two, telescoping gives `g(Y)^2+g(Y)=Y^(2^L)+Y`; each root of g lies in
F_(2^L). A common root with f is nonzero, has order dividing n_odd,
and has order dividing 2^L-1. The cyclic multiplicative group of
F_(2^L) contains exactly D roots whose order divides both numbers.
Since h is squarefree, its degree is the number of its distinct roots
in a splitting field, and d<=D. When D=1 the only possible common root
is 1. It is present exactly when L is even, yielding the same zero or
all-one kernel as above.

Run `python3 -I -B research/sidon-parity-circuits/arbitrary.py` for exact
checks at 14 sizes, including nontrivial dimensions d=3 and d=7. The
program checks every generated kernel vector against the original rows
and directly exhausts every x-assignment at n=16,17,18. The enumeration
is exponential in d by design; the bound on d does not make it
polynomial for arbitrary n.

The kernel enumeration is exponentially large on an explicit infinite
subsequence. For each integer L>=3 take n=5(2^L-1). Then
`floor(log2 n)-2=L`, and `2^L-1` divides n. Dividing the telescoping
identity by Y gives the exact factorization

    (g(Y)/Y) (g(Y)+1) = Y^(2^L-1)+1.

Consequently g/Y divides Y^n-1. Since Y does not divide Y^n-1,
`gcd(g,Y^n-1)=g/Y`, and the actual dimension is

    d = 2^(L-1)-1 = (n-5)/10.

Thus this enumeration uses `2^((n-5)/10)` kernel iterations on that
subsequence. This is a cost of the stated algorithm, not a lower bound
on every possible representation or counting algorithm.

## Filtering the kernel by realizable product patterns

There is an exact local characterization of vectors m that actually
come from adjacent products. For any cyclic binary word of length
n>=3, such a preimage exists if and only if m avoids the cyclic
substring 101. If m is all zero, its number of preimages is the Lucas
number above. If m contains a 1 and its maximal zero runs have lengths
r_1,...,r_k, then its number of preimages is

    product_i F_(r_i-1),

with the empty product equal to 1. Indeed, each 1 edge forces both its
endpoints to 1. A zero run of length r is an r-edge path with its two
endpoints forced to 1 and no adjacent pair of ones. It has F_(r-1)
valid assignments, and distinct runs have disjoint interiors. A
one-edge zero run has F_0=0 and is exactly a cyclic occurrence of 101;
all longer runs have a positive factor. The all-zero case has no
forced boundary and is counted separately.

This gives a linear-time predicate and explicit weight for each
candidate kernel word; it does not avoid generating 2^d candidates.
On the linear-kernel subsequence, exact enumeration finds respectively
1, 20 and 435 realizable vectors among 8, 128 and 32768 kernel words
at n=35,75,155. These are finite observations, not an asymptotic
estimate. A new algorithm would need to enumerate or aggregate only
realizable codewords efficiently, and its all-input costs would still
need to be paid. `runs.py` exhausts all 2,040 cyclic words at lengths
3 through 10 against both direct Boolean preimage counts and the
independent matrix routine, then reproduces the three finite screens.
