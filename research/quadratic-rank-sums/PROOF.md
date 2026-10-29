# Exact counting by quadratic-part rank

## Scope and statement

Let `P_1,...,P_a` be explicitly listed Boolean polynomial equations over
F2 in `n` declared variables, each of degree at most two after Boolean
multilinearization. Write `Q_i` for the vector of coefficients of the distinct
quadratic monomials `x_u x_v` with `u<v`, and put
`r=rank_F2(Q_1,...,Q_a)`. The exact number of common zeros can be computed in
`2^r poly(n+B)` bit operations and `poly(n+B)` bits of space, where B is
the explicit input size. The same bound holds for a prescribed consistent
partial assignment. Here r is computed in polynomial time; no oracle is
assumed. If the fixed-bit constraints make the system inconsistent the
answer is zero. This is a structural result for degree-two systems, not a
claim about unrestricted 3-SAT or arbitrary cubic sparse queries.

Quadratic root counting and character-sum methods are classical; related
prior sources and exact pins are listed in the README. No novelty or priority
is claimed for those methods. The proof below is self-contained and gives the
specific rank and space accounting used here.

## Row reduction and affine substitution

Apply invertible Gaussian row operations to the full polynomials while using
only their quadratic coefficient vectors as pivots. Exactly r transformed
rows retain quadratic pivots; every other transformed row is affine. The
transformed system has the same zero set, including constants and dependent
rows. Append any prescribed bits as affine equations. Solve all affine
constraints in polynomial time over F2. If inconsistent, return zero.
Otherwise parameterize their solution space bijectively as
`x=x0+Uz`, with `z in F2^h` and `h<=n`. This includes declared variables
which are unused or free. Substituting into the r remaining rows gives
Boolean polynomials `q_1,...,q_r` of degree at most two in z; Boolean squares
are reduced using `z_j^2=z_j`. Expanding the substitutions requires only
polynomially many bit operations and storage for explicit degree-two tables.
No assumption that the restricted quadratics remain independent is needed.

The exact number of common zeros is

```
N = 2^(-r) sum_{lambda in F2^r} sum_{z in F2^h}
                     (-1)^(sum_i lambda_i q_i(z)).
```

This follows by expanding `prod_i (1+(-1)^q_i(z))/2` for each z. It also
handles constant and duplicate q_i, and r=0. The final division is exact
because the sum equals `2^r N`. We evaluate the 2^r inner sums serially.

## Evaluating one quadratic sum

Let `q(z)` be a degree-at-most-two Boolean polynomial. If it has a cross
term `z_i z_j`, write uniquely

```
q = z_i z_j + z_i A(w) + z_j B(w) + C(w),
```

where w denotes the other variables, A and B are affine, and C has degree
at most two. For each fixed w, direct summation over the four values of
`(z_i,z_j)` gives

```
sum_{z_i,z_j} (-1)^q = 2 (-1)^(C + A B).
```

The product `AB`, multilinearized over F2, has degree at most two. Replace q
by `C+AB`, multiply the running integer factor by 2, and remove i and j.
After at most `floor(h/2)` iterations, the remaining polynomial is affine.
Its character sum is zero if its linear part is nonzero, and otherwise is
`+2^s` or `-2^s` according to its constant, where s is the number of
remaining variables. This evaluates the original sum exactly. At every step
an explicit polynomial has at most `1+h+binom(h,2)` coefficients, and
updates, additions and multiplications are polynomial in h.

Each inner sum has magnitude at most `2^h`; the running outer sum has at
most `h+r+1` bits. Thus row reduction, substitution, all `2^r` evaluations,
exact division and the output fit `2^r poly(n+B)` bit operations and
polynomial space. The verifier implements this elimination independently of
its brute-force oracle. It is a reference implementation, not the accepted
contraction algorithm.

## A sparse family where rank helps and cover does not

Take the infinite sequence `n=2^d` with d an even power of two, let `L=d`,
and partition the variables into `n/L` blocks of L variables. In each block
use one equation

```
q_b = XOR_{j=0}^{L/2-1} x_(bL+2j) x_(bL+2j+1) = 0.
```

Every equation has `L/2 <= log2 n` monomials of degree two; each variable is
in one scope. This is a valid low-load sparse-query family with
`r=n/L=n/log2 n`, because each row has private quadratic terms. Its
interaction graph is a perfect matching, whose minimum cover is n/2. The
rank interface therefore gives `2^(n/log n) poly(n)` while the direct
interaction-cover interface of PR #113 has a linear exponent. This is a
comparison of stated upper-bound interfaces, not a lower bound on other
algorithms. In fact this family factors into independent blocks: each block
has `(4^(L/2)+2^(L/2))/2` zeros and the total count is their product. It is
presented to separate the parameters, not as a hard counting instance.

Conversely, the system of `n/2` separate equations
`x_(2i)x_(2i+1)=0` has `r=n/2` while satisfying the same low-load sparse
hypotheses. Its count is `3^(n/2)` by factorization. Thus neither sparse
input nor low incidence forces small quadratic-part rank; the rank bound on
its own cannot improve the arbitrary-query exponent.

## Cubic transversal followed by quadratic-rank counting

The quadratic routine also gives a conditional interface for a listed system
of degree at most three. Let C hit the support of every nonzero cubic
monomial, and write `t=|C|`. Enumerate all assignments to C, or only those
compatible with a prescribed partial assignment. Every cubic term loses at
least one variable or vanishes, so the resulting system is quadratic. For
assignment c, let `r(c)` be the rank of its quadratic coefficient rows, after
combining equal monomials. The exact total is the sum of the quadratic counts
on those branches, with bit complexity

```
poly(n+B) sum_{compatible c} 2^r(c)
    <= poly(n+B) 2^(t+r_max),
```

where `r_max` is the maximum of these ranks. Compute each rank on its own
branch and process branches serially; the algorithm need not know `r_max`
in advance, and uses polynomial space. Fixed bits outside C remain affine
constraints. A certificate that C hits all cubic supports is checked in
polynomial input time. Alternatively, greedily take a maximal collection of
pairwise-disjoint cubic supports and put every variable in those supports in
C. The result hits every cubic support and has size at most three times the
minimum cubic transversal; it need not minimize the combined rank cost.

The two costs cannot be collapsed into t alone, or into the original
quadratic rank. For `n=2m+1` use the equations

```
P_i = x_0 x_(2i+1) x_(2i+2) = 0,  0 <= i < m.
```

The original quadratic-part rank is zero and C=`{0}` hits every cubic term.
On branch `x_0=1`, however, the quadratic coefficient rows are m independent
pair monomials, so `r_max=m`. The branch `x_0=0` has rank zero and is
unconstrained; the total exact count is `2^(2m)+3^m`. This explicitly
exhibits rank created by cubic substitution. It does not imply that the
example is hard: the count factors. The shared variable has high incidence,
and no claim is made that this presentation survives the source's
high-incidence preprocessing unchanged.

For a width-3 CNF, the false-clause polynomial expansion has degree at most
three, and a set hitting its cubic supports yields this same exact counting
interface without auxiliary variables. This only gives the displayed bound
when its cubic-transversal and branch-rank costs are both controlled; no
uniform such bound is known here.

## Outer reduction and limits

The accepted dense reduction can generate degree-three sparse equations;
the quadratic routine alone does not handle a nonzero cubic monomial, and
the transversal interface requires both its branch and rank costs. Neither
route has a proved small-r guarantee for all generated degree-two queries, rejected
greedy candidates, or sparsification branches. A faster all-input SAT
algorithm would need a uniform reduction to admissible systems, a provable
rank bound, and a complete ledger for branches, query construction,
precision, recovery and space. A single-query structural guarantee does not
pay those costs. The accepted fixed-density and general-density results and
selected alpha remain unchanged.

All-size statements are author-checked with substantial AI assistance and
await independent human or formal review. The small exhaustive controls do
not prove the all-size theorem.
