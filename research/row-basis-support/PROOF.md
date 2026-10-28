# A row-basis-resistant coefficientwise family

This argument concerns the specific scalar-lift and injective coefficientwise
indexing interface of [the predecessor](../scalar-parity-lift/PROOF.md), not
the accepted theorem or arbitrary algorithms. It is author-checked with
substantial Codex assistance and awaits independent review.

## Construction and loads

Let n be sufficiently large, L=floor(log2 n), and L<n/2. Variables are
x_0,...,x_(n-1), with indices modulo n. Define n homogeneous quadratic
F2 equations P_i=0 by

    P_i = sum_{j=1}^L x_i x_(i+j).

Write E_i for the set of unordered degree-two monomials in P_i. The E_i
are pairwise disjoint: equality of edges with different starting points
would require two positive forward offsets summing to n, impossible
because 2L<n. Each E_i has L edges. Row i has exactly L+1 variables,
and every variable occurs in exactly L+1 row scopes. Thus the original
incidence count is N0=n(L+1); the source's threshold
ceil(N0/n) ceil(sqrt(ceil(log2 n))) does not trigger high-incidence
branching on this presentation. It is an admissible degree-2 instance of
the fixed-k sparse-query interface. The all-zero assignment satisfies it;
it is deliberately not a hard SAT family.

## Every invertible row basis

For a row vector a in F2^n, the normalized polynomial Q_a=sum a_i P_i
has exactly L wt(a) distinct degree-two monomials. No cancellation occurs
because the E_i are disjoint. The original rows are independent, and every
basis row is a nonzero linear combination. Therefore for every invertible
n-by-n F2 row transformation, all n transformed equations contain at least
L monomials. The transformed equations remain homogeneous quadratics.

Associate separate incidence variables with each transformed equation,
and use the predecessor's integer zero-indicator lift. For any degree-two
monomial S in a row, its coefficient is -1: by Boolean Mobius inversion
on its two variables, all terms of the row are zero on proper subsets of S,
and exactly that one monomial is one at S. Thus choose one monomial in
each row. The product has at least L^n distinct incidence monomials, all
of degree 2n and coefficient (-1)^n. They survive modulo 2^(n+1).
The predecessor's total-degree cutoff for a=n, k=2, p=n+1 is 4n, so all
are retained. Each individual contribution to the assignment sum also
survives modulo 2^(n+1), since its union contains at least two variables.
This individual survival does not assert that their sum cannot cancel.

Take J=ceil(n^(1/4)) groups on each side. The predecessor's degree-array
scheme has at most (2n+1)^(J^2) arrays for these chosen degree-2n terms;
all arrays of the full cutoff also number 2^O(sqrt(n) log n). By pigeonhole,
some array has at least L^n/(2n+1)^(J^2) distinct nonzero valid index
assignments. Any injective Boolean index for those assignments requires

    n log2 L - J^2 log2(2n+1) = Omega(n log log n)

bits. This bound holds independently for every invertible row basis,
including dense ones, at this stated pre-branch coefficientwise interface.
It does not require materializing all coefficients; it is a count of the
valid assignments any such injective indexing must represent.

## The all-zero high-incidence branch

The preceding argument also survives a bounded set of zero substitutions,
even if the row basis changes both before and after the substitutions.
Let B variables be fixed to zero. Each variable belongs to exactly 2L of
the private edges, so at most 2LB edges disappear. Call an original row
good if at least L/2 of its edges survive. Each bad row has lost more than
L/2 edges, and there are therefore fewer than 4B bad rows. Surviving edges
are still private to their original rows. The surviving good rows are
independent, with at least g>=n-4B of them.

Any collection of residual quadratic equations that spans the restricted
row space has at least g rows with a nonzero coefficient in a good original
row: their projections to the good coordinates must span F2^g. Every such
row has at least L/2 distinct quadratic monomials. This includes any
invertible transformation before the substitutions and any subsequent
choice of basis of the restricted row space. Each residual equation remains
homogeneous, and its zero-indicator lift has constant coefficient one.
Pick a surviving quadratic monomial independently in each of g of those rows
and use the constant coefficient in all other rows. The product gives at
least (L/2)^g distinct incidence monomials of degree 2g and coefficient
+/-1 modulo 2^(f+1), where f=n-B is the number of free variables. They
are within the scalar cutoff: there are a>=g residual equations and
2g<=2(a+f). Each individual assignment-sum contribution also survives.
For B=o(n) this remains 2^Omega(n log log n), even after the degree-array
pigeonhole count. This is an existential branch statement, not a lower
bound for an algorithm that simplifies or recognizes the entire instance.

For the source's single high-incidence step, let N be the total incidence
count at that step, even after an invertible row change. A variable is fixed
only when its load exceeds ceil(N/n) ceil(sqrt(ceil(log2 n))). The sum of
loads is N, so B<=n/ceil(sqrt(ceil(log2 n)))=o(n). The all-zero branch is
one of the enumerated branches and has the property above. With arbitrary
nonzero fixed values the residual equations may have linear and constant
terms; this proof makes no claim for those branches. Repeating the branching
step or allowing other preprocessing also requires a new argument.

## Limits and complete cost boundary

The result does not show a full-run lower bound or rule out preprocessing
that resolves this easy instance.
Its all-zero witness, the common factor x_i in each original row, and the
cyclic locality all leave aggregation and alternative algorithms open.
Non-invertible, nonlinear or instance-dependent transformations, grouping
of coefficients without injective indexing, and changed kernels are not
covered. Issue #28 studies transfer aggregation on a different cyclic
family; this result does not contradict that route.

No changed algorithm is supplied. Hence this is not a complete exponential
cost ledger or a claim about reduction branches, query counts, tensor entry
time, modes, recursive calls, precision, recovery, space or randomness.
Those costs must all be paid for any future positive construction. The
accepted fixed-density and general-density bounds and alpha remain unchanged.
