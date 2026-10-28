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
