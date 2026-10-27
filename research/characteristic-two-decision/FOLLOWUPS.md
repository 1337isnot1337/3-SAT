# Follow-up mechanisms and exact boundaries

These are research checkpoints, not a new alpha claim. The elementary
even-node proposal and its reported failure were supplied by the repository
owner; the reconstruction below makes that failure reproducible and claims
no priority. All accepted OpenAI results remain premises.

## 1. Refuted: evaluating at an even local node preserves parity

For packet length `L=4`, let `S={-4,-3,...,3}` and use the source kernel

```math
 W_{xy}(T)=\frac{\prod_{q\in S,\ q\ne y-x}(T-q)}{C'(0)}.
```

Its diagonal entry satisfies

```math
 W_{00}(0)=1,\qquad W_{00}(-2)=0,
 \qquad [T]W_{00}(T)=1/4.
```

Thus it is not an integral-coefficient polynomial over the two-adic valuation
ring, and substituting an even integer does not preserve its value modulo 2.
Nevertheless every chart `W_00(t+8z)` for `t in S` has two-adically integral
coefficients, exactly the distinction needed here. Also
`W_20(-2)=5/3`, an integral two-adic element with odd denominator.

This is a contraction example, not merely an unrelated polynomial. In the
source's deformation formula fix the column bits to the vector having a one
only at the distinguished edge, and let the row tensor product be just the
bit on the matching row port. All other row tensors are the unary constant
one function. Summing the other row bits uses `l_0(z)+l_1(z)=1`, leaving
`F(T)=W_xx(T)` for the distinguished slot. The original network has one
consistent assignment and parity one; evaluation at any nonzero source node
has diagonal kernel zero and returns zero. Extra edges can be padded with
column bits fixed to zero and unconstrained row bits without changing this
calculation. All original tensors are Boolean-valued and unary.

This refutes the proposed parity-preservation step. It does not refute the
accepted construction, which uses recovery and mode expansion. Any future
constant-precision shortcut must establish a new invariant that passes this
example; local-chart integrality alone is insufficient.

## 2. Aggregation is algebraically valid but need not fit the degree interface

For a group of `h` equations define
`G(x)=prod_i(1+P_i(x))` and take its multilinear representative in the original
Boolean variables. For a variable subset `S`, its coefficient is

```math
 [x_S]\overline G=\sum_{T\subseteq S}G(\mathbf1_T)
 \quad\text{over characteristic two},
```

with all variables outside `S` fixed to zero. This is an unweighted parity
query on the restricted group, so the deterministic evaluator in PROOF.md
can compute the coefficient using parameter `h` when its sparsity hypotheses
hold. The coefficient identity is exact; the obstacle below is a different
interface requirement.

Grouping `a=Theta(n)` equations into `J` groups suggests only `nJ` incidences
and `O(n log J)` encoded wires. Combining that expression with the accepted
contraction cost would be invalid without checking maximum vertex degree.

Here is an explicit counterexample to automatic degree admissibility. In one
group take `h=n/J` equations on disjoint blocks of `J` variables:

```math
 P_i=\sum_{j=1}^J x_{ij},\qquad
 G=\prod_{i=1}^h(1+P_i).
```

The degree-h part has exactly `J^h` distinct monomials with coefficient one.
Split the variables into `R` groups. At most `(h+1)^R` selected-degree arrays
describe those monomials. Therefore at least one array retains at least
`J^h/(h+1)^R` choices. An injective monomial-index encoding of that array
requires the aggregate test vertex to have at least

```math
 h\log_2J-R\log_2(h+1)
```

incident Boolean wires. With `R=ceil(n^(1/4))` and `J` growing only as an
iterated logarithm, this is `Omega(n log J/J)`, which eventually exceeds
`(n log J)^(9/10)`. Thus the hoped-for wire reduction does not by itself meet
the accepted theorem's maximum-degree hypothesis. The checker gives an exact
integer instance at `n=2^128, J=8`, without enumerating its huge polynomial.

Additional distinct low-degree equations can fill the other groups; the
example is a permitted local aggregate tensor. It is not a hard-SAT lower
bound: these particular linear equations are easy by elimination. It refutes
the blanket degree assertion for this encoding, not every adaptive grouping
or an algorithm exploiting linear structure.

Reopening condition: a way to split or contract aggregate tensors that preserves
the proposed saving, or a proved extension of the contraction interface with
all precision, packing, entry and leaf costs paid.

## 3. A shared-code identity: independent sets of a binary matroid

Let `A` be a binary matrix with columns indexed by `1,...,m`. The multilinear
Boolean polynomial for the indicator of `Av=0` over F2 is exactly

```math
 \mathbf1_{Av=0}
 =\sum_{S:\ A_S\text{ has independent columns}}\prod_{j\in S}v_j.
```

To prove it, the coefficient on `S` is the characteristic-two subset inversion
sum of the indicator on vectors supported in `S`. That is the parity of
`|ker(A_S)|=2^(|S|-rank(A_S))`, which is one exactly when the columns are
independent. The empty set contributes the constant one. Substitution of
clause-violation polynomials preserves the identity on Boolean assignments.

This represents all sparse parity queries through one shared code and uses
degree at most `rank(A)` in the clause-violation symbols. It may expose
cancellations hidden by independent test-incidence expansion. However the
independence predicate is now global; a single rank-oracle tensor has too
many ports for the desired contraction interface. No efficient distributed
representation or resulting bound improvement is claimed.

The checker tests every binary 2-by-4 matrix on all 16 syndrome inputs:
4,096 exact evaluations. A next use of this identity must supply a small
network for the shared rank condition, or exploit the actual sparse-code
structure, without hiding exponential work in a high-degree tensor.

## Reproduce

```sh
python3 -I -B research/characteristic-two-decision/check_followups.py
```

The output is saved in `followup-verification.json`. All comparisons use exact
integers or rational numbers. None of these finite checks establishes a new
asymptotic bound.
