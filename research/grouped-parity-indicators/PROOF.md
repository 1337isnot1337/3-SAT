# A certificate for grouped Boolean indicators

Author-checked, substantially OpenAI Codex assisted; not independently reviewed.
This is a sufficient interface and an exact finite checker, not an improved
bound for unrestricted SAT. The grouped coefficient identity itself is already
proved in `characteristic-two-decision/FOLLOWUPS.md`, Section 2. The changed
work here is to expose the simultaneous degree, profile, entry and wire costs
in a checkable certificate, including Boolean cancellations.

## Input and exact identity

Normalize each listed F2 polynomial to squarefree monomials, cancelling repeats.
Partition the equations into groups G_i. Let C_i be the unique multilinear
Boolean representative of the product of (1+P) over P in G_i. Its value is the
indicator that the group's equations vanish. Let I_i be its actual variable
support and d_i its degree; reject immediately if C_i is zero, and discard a
constant-one factor. Neither grouping nor discarding a constant factor removes
a declared variable from an already specified weighted partition function.

The coefficient of x_S in C_i is the parity of the number of solutions of the
group with all variables outside S fixed to zero. It can always be computed by
2^|S| evaluations of the listed equations, in polynomial working space. Computing
ALL coefficients and discovering I_i,d_i costs 2^O(q) poly(input) where q is the
largest ORIGINAL group scope. An implementation storing the coefficient table
uses exponential space. Alternatively scan all coefficients sequentially with
subset summation, using at most 3^q poly(input) time and polynomial space. A
claimed small post-cancellation support does not pay this discovery cost.
A supplied symbolic identity can replace discovery only with its own proof.

Fix a characteristic-two field F and weights r_v. The polynomial
Z(r)=sum_{x satisfying all equations} product_{v:x_v=1} r_v is exactly

    sum_{S_1,...,S_H} (product_i [x_(S_i)]C_i)
        product_{v in union S_i} r_v
        product_{v outside union S_i} (1+r_v).

This follows by expanding the indicator product and summing each Boolean
variable. It includes empty systems, constant contradictions, zero weights,
and unused declared variables. Distinct assignments have distinct weight
monomials, so for |F|>=6n a nonempty solution set gives a nonzero evaluation
with probability at least 5/6 for independently uniform weights. There are
no false positives. Bit generation, field construction and arithmetic are
polynomial in input size; bounded small inputs can be enumerated. The
finite checker uses F16 only to check identities, not to claim the 5/6 bound
for its test sizes.

## Profile/index representation

Partition active variables into J sets X_j, and put N_ij=|I_i intersect X_j|.
For each factor use the set D_i of degree vectors
(|S intersect X_j|)_j attained by a nonzero monomial x_S of C_i. Enumerate
profiles in D_1 x ... x D_H. This is exact: every surviving incidence monomial
appears once. A simpler exhaustive profile enumeration can include all vectors
with sum at most d_i. It need not discover the true support first.

For a fixed profile (d_ij), the edge i,j has

    b_ij = ceil(log2 binom(N_ij,d_ij))

Boolean wires. Both endpoints decode an index as a subset of size d_ij.
Invalid binary indices contribute zero. A factor tensor tests its coefficient
on the union of the decoded subsets. A variable tensor gives the product of
r_v or (1+r_v), according to whether a copy of v was selected. Both are explicit
entry algorithms; no table of all entries is assumed. Profiles may contain
zero-valued choices, which correctly contribute zero to the contraction.

Let W=max_profile sum_ij b_ij, Delta=max_profile max(max_i sum_j b_ij,
max_j sum_i b_ij), and R=product_i |D_i|. The checker calculates these exactly
for its finite inputs. They are distinct costs: a profile with zero wires can
still belong to an exponentially large profile enumeration. Replacing all
profiles by their wire maximum alone is invalid.

For a uniform upper estimate, put D=sum_i d_i and N=sum_ij N_ij. If D>0,

    W <= HJ + log2 binom(N+D,D)
      <= HJ + D log2(e(N+D)/D),
    R <= product_i (d_i+1)^J <= (D+1)^(HJ).

The first bound encodes all selected incidence subsets of degree at most D;
the second is a deliberately loose bound on degree vectors. These are upper
bounds, not lower bounds on actual tensor ranks or runtime.

## Sufficient contraction certificate and complete cost

For a chosen integer size parameter s>=2, suppose the following hold with
fixed constants C,A,b, uniformly over the input class under consideration:

- W<=Cs; Delta<=ceil(s^(9/10)); H+J is polynomially bounded in s.
- Each factor coefficient and variable entry is computable in
  (s+L)^b 2^(A s^(9/10)) time and (s+L)^b space, with total description L.
- For e=ceil(log2(max(2,6n))), (H+J)(e-1)+1<=Cs.
- Profiles and their descriptions are generated within a stated preprocessing
  cost Q, or with a polynomial cost per profile. Any discovery of I_i,d_i,D_i
  and the grouping itself is included in Q.

The source theorem `thm:tensor-contraction`, together with the finite-field
embedding already proved in `characteristic-two-decision/PROOF.md`, then gives

    Q + R (s+L)^O(1) 2^O(s/sqrt(log s))

bit operations for one weighted evaluation. The embedding uses P0=1 and
ell=(H+J)(e-1)+1, canonical polynomial representatives of field entries, then
reduction modulo the defining irreducible polynomial. All entry products have
degree less than ell; it is not assumed that canonical representatives preserve
multiplication. Mode enumeration, precision and recovery are paid by the
accepted theorem, not removed by the field-valued outer indicator.

Sequential profiles and subset enumeration retain polynomial space provided Q
and the profile generator do too. The finite checker materializes coefficient
tables and is not that polynomial-space implementation. The number of original
variable groups can be chosen separately from factor grouping, but the three
hypotheses involving Delta, profile count and field embedding must all be
checked again. Reductions, high-incidence branches, randomized hash failures
and any repeated weighted evaluations remain outer costs. This certificate by
itself supplies none of the all-input guarantees those reductions need.

The direct coefficient algorithm satisfies the entry condition if the largest
post-normalization scope is O(s^(9/10)); discovering that normalization still
uses the original scopes. The predecessor also permits a faster coefficient
parity evaluator under its small-sparsity hypotheses. That changes entry cost,
not Delta or the profile count.

## Two controls and the unresolved mechanism

For P1=x0*x1 and P2=x0*x1+x0*x2, Boolean reduction gives

    (1+P1)(1+P2) = 1 + x0*x1 + x0*x2 + x0*x1*x2.

Thus the degree sum falls from four to three when the factors are grouped.
This is a real cancellation, with no inference about a global asymptotic gain.
Conversely, grouping h disjoint equations P_i=x_(2i)*x_(2i+1) produces degree
2h, although there is only ONE group. The coefficient of the product of all
2h variables is one. The group count cannot replace D in the wire budget.
These are easy families and imply no SAT hardness result.

The registered six-equation fixture exhausts all 203 groupings and retains a
Pareto frontier for profile count, wire count, maximum tensor degree and original
scope. The frontier is a finite cost tradeoff, not an optimized running-time
bound: the hidden constant in the contraction theorem is not known from these
measurements. The predecessor aggregate degree and persistent-leaf obstruction
still applies. A global improvement requires a uniform grouping or a changed
leaf/decomposition method for every generated sparse query such that the ENTIRE
above cost, summed over the outer reduction, is smaller than the selected bound.
No such construction is established.

## Attribution and evidence

Accepted OpenAI source: commit 7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a,
`thm:tensor-contraction`, `lem:tensor-sparse-query`, `eq:sharp-wire-budget`.
Immediate predecessors at canonical base c600b21ee7800a49c05718a254be50168e6b355b:
`characteristic-two-decision/PROOF.md` and `FOLLOWUPS.md`, and
`aggregate-packing-limits/PROOF.md`. Boolean subset inversion, the fingerprint
argument, and combinatorial indexing are credited to those sources; no new
priority claim is made. The exact fixture search and simultaneous certificate
are this package's scope. All new material is Apache-2.0.
