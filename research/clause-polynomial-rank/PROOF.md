# Clause-violation rank and density

All-size argument author-checked; not independently reviewed. Fix a field F,
a width k>=1, and a CNF in distinct variables after deleting tautological
clauses, collapsing repeated literals and deleting duplicate clauses. Each
nonempty remaining clause has a variable support A and forbids precisely one
Boolean pattern a on A. Its violation polynomial is the multilinear function

    V_{A,a}(x) = product_{i in A:a_i=1} x_i
                  * product_{i in A:a_i=0} (1-x_i).

Let m be the number of clauses and r the dimension over F of the span of
these polynomials in the formal multilinear monomial basis. The same dimension
is obtained as Boolean functions: the Boolean zeta matrix is unit triangular
when subsets are ordered by size, over every field.

## Theorem

For every such formula, m <= 2^k r. If the formula is satisfiable, then
m <= (2^k-1) r. Consequently m=O(n) if and only if r=O(n), for fixed k.
The same conclusion holds for affine spans up to one extra dimension.

Proof. Pick one violation polynomial for each distinct variable support A.
Its coefficient on monomial x_A is (-1)^(number of zero entries of a), a
nonzero field element, and all its monomials have support contained in A.
Order the chosen supports by cardinality. The coefficient submatrix whose
columns are those same supports is triangular with nonzero diagonal, so the
number h of distinct supports satisfies h<=r. Each support of size d has at
most 2^d distinct forbidden patterns, so m<=2^k h. If the whole formula is
satisfiable, at least the satisfying assignment's restriction to each support
is not forbidden; hence that support has at most 2^d-1 clauses. Therefore
m<=(2^k-1)h<=(2^k-1)r. A satisfiable formula cannot contain an empty clause.
For an unsatisfiable formula an empty clause, if present, has support empty,
polynomial 1 and its single pattern; the first bound still applies. Finally
r<=m is immediate. An affine span has dimension at least r-1. ∎

The result also handles characteristic two; no rank preservation under a
change of field is assumed. Linear combinations can be arbitrarily dense or
sparse: dimension alone does not give their entry cost, and the inequality
says only that compressing the complete original clause-violation list by
linear span cannot make an actual superlinear-density normalized formula into
O(n) equations.

## Sharp satisfiable family

Let n>=k and for every k-subset A include the clauses forbidding all nonzero
Boolean patterns on A. The all-zero assignment satisfies every clause; since
every variable lies in some A, it is the unique solution. The number of
clauses is

    m = (2^k-1) binom(n,k).

For each nonempty T subset of A, the monomial x_T equals the sum of V_{A,a}
over the patterns a with a_i=1 for all i in T. Both sides are multilinear
and agree pointwise on the Boolean cube; the zeta matrix gives equality as
polynomials. Every nonempty T of size at most k lies in some A. Conversely
every V_{A,a} has degree at most k and zero constant coefficient, since a is
nonzero. Hence, over every field,

    r = sum_{j=1}^k binom(n,j).

For fixed k, m/r tends to 2^k-1 as n tends to infinity. Thus the satisfiable
constant is asymptotically sharp, including k=1. These formulas are trivially
solvable from their structure: the example is a rank obstruction for this
representation, not a lower bound on SAT solving, general preprocessing,
nonlinear compression, random fingerprints or the later sparse-query row
space.

## Cost and scope

The theorem is an algebraic preprocessing boundary. It changes no reduction,
tensor description, entries, mode enumeration, precision, recursion, recovery,
amplification, space or time bound. In particular it cannot show that the
accepted arbitrary-density encoding is optimal. Nonlinear clause aggregation,
special formula simplification, and basis changes on the O(n) *hashed queries*
are distinct and remain open. Original clause count and rank may be computed
in polynomial time for fixed k, but computing them is not presented as an
algorithmic improvement. Duplicates and tautologies must be normalized before
using the density statement.
