# Optimal characteristic-two frontier for independence

Author-checked all-size proof, awaiting independent review. The construction
improves the interface of PR #37; it is not a SAT-time improvement. Let A
be binary with columns v_1,...,v_m, and define

    U_i=span(v_1,...,v_i), F_i=span(v_(i+1),...,v_m),
    E_i=U_i intersect F_i, b_i=dim E_i.

All spans and vector sums are over F_2. Tensor amplitudes are over a field K
of characteristic two, including any extension field of F_2.

## A linear state instead of a subspace label

For a chosen prefix S, let P_i be its span. Define a vector g_i indexed by
u in E_i by

    g_i(u) = 1[S independent] 1[u in P_i] in K.

At i=0 the unique entry is g_0(0)=1. Entries outside E_i are interpreted
as zero. When v=v_(i+1) is not selected, put g_(i+1)(u)=g_i(u). When it
is selected, put

    g_(i+1)(u)=g_i(u)+g_i(u+v),   u in E_(i+1).          (1)

Both u and u+v are in F_i. If either is outside E_i, it cannot belong to
P_i subset U_i, so the zero extension is correct. If the old prefix is
dependent, all entries remain zero. If it is independent but v belongs to
P_i, the two indicators coincide and cancel in characteristic two; the
new prefix is dependent. If v is outside P_i, the two cosets P_i and
v+P_i are disjoint, and their sum is the membership indicator of the new
span. This proves the invariant in every case, including a zero column.
At i=m, E_m=0 and g_m(0) is exactly the independence indicator of the full
chosen set.

Choose a basis for each E_i and represent u by b_i Boolean bits. Each
transition is a tensor with b_i+b_(i+1)+1 ports, indexed by the old state,
selection bit and new state. For selection 0 its entry is [old=new]; for
selection 1 its entry is [old=new]+[old=new+v] in K. If the two tests
coincide their values cancel, rather than being combined by Boolean OR.
The endpoint states are zero. Contracting the state bits computes the
independence indicator. It uses exactly sum_i b_i internal state-bit wires,
with each entry computed in polynomial time by expanding the fixed bases and
checking binary equality. The bases and descriptions are found by Gaussian
elimination in polynomial time in the matrix dimensions. The intermediate
state is a vector of amplitudes, not one deterministically chosen syndrome;
cancellations are essential.

If a field-valued variable z_i weights selecting v_i, sum the local
selection bit with weights 1 and z_i. By distributivity the resulting
chain computes the full multilinear polynomial

    sum_{S independent} product_{i in S} z_i

for arbitrary z_i in K. At Boolean z this equals 1[Az=0] by the shared-code
identity in PR #2. For arbitrary field inputs it is that polynomial, not a
Boolean kernel predicate. This distinction is essential for applications.

## Exact cut rank over characteristic two

For a cut, let E=U intersect V have dimension b. If either selected side is
dependent, the full set is dependent. Otherwise their union is independent
iff X intersect Y={0}, where X and Y are the selected-side spans intersected
with E. For subspaces X,Y over F_2,

    1[X intersect Y={0}] = sum_{u in E} 1[u in X] 1[u in Y] in K,

because the sum is 2^dim(X intersect Y), which is 1 for dimension zero and
0 in characteristic two otherwise. This is a sum of 2^b separable terms, so
the independence table has rank at most 2^b.

The reverse inequality is established in PR #74 at head
`e21ff2db8f5f800fa8e7e398f4cc4d21af496850`: choose independent columns on each side that form bases modulo E,
fix those columns as selected, and complete each to a basis. In the quotient
by the fixed columns, the two completions are bases of E. Reindexing row
subsets by their complements gives a block triangular 2^b-square minor; its
diagonal blocks are the exterior powers of the invertible binary change of
basis, so it is invertible over F_2. Thus rank is exactly 2^b over K. In
particular every exact ordered chain needs at least b Boolean bond wires
at that cut, and the chain above is optimal in their total count.

This exact upper bound is field-specific. With left and right columns each
`(01,10,11)` in F_2^2, b=2 and the independence table has rank 4 over F_2
but rank 5 over F_3. The latter also implies rational rank at least 5.
The finite checker computes both ranks. PR #74's rational lower bound remains
valid; this construction makes no rational or odd-characteristic upper claim.

## Cost boundary

PR #55 (head `0264a0cf35da09f4abab4118dc870aed121fa167`) shows that
sum_i b_i>=k(D-1) when A has kernel dimension k and minimum nonzero kernel
weight at least D>=2. The present chain uses exactly sum_i b_i wires, the minimum for any exact
chain under the stated ordered cut model; k(D-1) is a further lower bound. For
the accepted initial sparse checks plus t rows, K=max(0,m-3n-t), m>P and
the source distance give at least K(ceil(m/P)-1) Boolean bond wires; this
is conditional on the row count leaving nonzero K. In a linear-nullity,
m=Theta(n), polylog-P regime the required width sum is
Omega(n^2/polylog(n)). Other network topologies, representation after
substitution, and changed hashes are outside this chain obstruction.

All application costs remain to be proved: actual hash dimensions and
ordering, the full sparse-query representation, input construction and
entry cost, coefficient ring embedding, contraction precision and recursion,
recovery, branches, queries, space and randomness. No exponent, selected
result or full SAT algorithm is changed.

## Accepted-contraction evaluation of the weighted chain

The selected-contraction theorem can evaluate the independent-set polynomial
for field weights when e=O(log s), with the chain's complete wire count s
as its size parameter. Let

    s = m + sum_(i=1)^(m-1) b_i,

and assume s>=2; tiny cases are directly enumerated. Consecutive frontier
widths differ by at most one, since

    b_i = rank(U_i)+rank(F_i)-rank(A)

and advancing a column changes the two ranks by at most +1 and -1,
respectively. As b_0=b_m=0, if B=max_i b_i, the width at a position at
distance d from a maximum is at least B-d while d<=B. These two triangular
ramps lie within the sequence and give sum_i b_i>=B^2. Thus each transition
has at most 2B+1<=2 sqrt(s)+1 ports, eventually below s^(9/10).

To evaluate the polynomial at supplied weights in F_(2^e), expose each of
the m Boolean selection bits and connect it to its transition tensor and
to one of q<=J=ceil(s^(1/5)) weight-group tensors. A group tensor returns
product z_i^(selection_i) over its group, in the field. Groups have at most
ceil(m/J) ports, so their degree is O(s^(4/5)+1). This adds O(m) wires.
If m<J, use m singleton groups. Subdivide every edge with a binary equality
tensor to make the graph bipartite; this multiplies the wire count by two
and leaves maximum degree in the theorem's range. All transition and
equality entries are 0/1 and computed by binary linear algebra; group
entries are computable in polynomial time and space from the supplied field
and weights. The full description has polynomial size in the original
matrix, field description and weights.

Use the PR #2 field lift with P_0=1 and
ell=q(e-1)+1 in F_2[V]/(V^ell). Only the q group tensors carry nonconstant
polynomial entries, each of degree below e. Each complete summand therefore
has degree at most q(e-1), so truncation is exact and reduction modulo the
field polynomial gives the required field value. Here ell=O(s^(1/5) log s)
is O(s). Apply the accepted theorem to get deterministic time

    (s+L)^O(1) 2^O(s/sqrt(log s))

and polynomial space for this evaluation, where L is the total description
length. If the field polynomial must be constructed, deterministic exhaustive
irreducibility search is polynomial for e=O(log s). This is a parameterized
matroid-polynomial evaluator, not a whole SAT solver. In particular s can
be quadratic or larger in the number of variables after composing reductions;
all input preparation, many evaluations, branches, precision and probability
costs remain to be paid before any SAT conclusion.
