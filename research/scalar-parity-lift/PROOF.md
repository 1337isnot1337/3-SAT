# Scalar parity projectors

This changes the sparse-query encoding in the owner-accepted OpenAI theorem.
It does not audit that theorem. The construction and proof below are
AI-assisted and have no independent review.

## 1. An exact local lift

Normalize an equation over F_2 on Boolean variables by multilinearizing its
monomials and canceling duplicate monomials modulo two. Write it as

```math
 P_i(x)=b_i+\sum_{j=1}^{t_i}x^{A_{ij}}\pmod2,
 \qquad b_i\in\{0,1\},\quad 1\le |A_{ij}|\le k.
```

Each test has its own incidence variables z_iv. In the integer Boolean
quotient, where z_iv^2=z_iv, define

```math
 E_i(z_i)=\frac{1+(-1)^{b_i}
                    \prod_{j=1}^{t_i}(1-2z_i^{A_{ij}})}2.
 \tag{1}
```

The numerator is coefficientwise even: its constant coefficient is
1+(-1)^b_i, and all its other expansion terms contain a factor of two.
Equation (1) therefore defines an integer multilinear polynomial. The
division is in the integers before reduction; division by two in
Z/2^p Z is neither required nor valid in general.

At every Boolean assignment, each product factor is (-1)^(x^A_ij).
Thus E_i is exactly the zero-indicator of P_i, with values zero and one.
This includes constant equations: E_i=1 for P_i=0 and E_i=0 for P_i=1.

For a nonempty support S, its coefficient is

```math
 c_i(S)=(-1)^{b_i}\sum_{\substack{\varnothing\ne R\subseteq[t_i]\\
                              \bigcup_{j\in R}A_{ij}=S}}
                            (-1)^{|R|}2^{|R|-1}.
 \tag{2}
```

Every summand has |R|>=ceil(|S|/k). Consequently

```math
 2^{w_i(S)}\mid c_i(S),\qquad
 w_i(S)=\max\{0,\lceil |S|/k\rceil-1\}.
 \tag{3}
```

For S empty set w_i(S)=0; its coefficient is (1+(-1)^b_i)/2.
Zero coefficients satisfy every divisibility assertion. Cancellation in
(2) can increase the valuation, but cannot decrease (3).

One coefficient can be evaluated directly, without constructing E_i:

```math
 c_i(S)=\sum_{T\subseteq S}(-1)^{|S|-|T|}
                       \mathbf1_{\{P_i(\mathbf1_T)=0\}}.
 \tag{4}
```

This is Boolean Mobius inversion, because E_i agrees with the indicator
at every Boolean point. Its time is 2^|S| times a polynomial in the input
length and p, and its space is polynomial. Work modulo 2^p throughout
the sum if only that residue is needed. No formal expansion table is
needed by the algorithm.

## 2. A smaller retained degree over a scalar ring

Give different tests disjoint incidence variables and take F=prod_i E_i.
For a monomial with local supports S_1,...,S_a and incidence degree
d=sum_i |S_i|, its coefficient is the product prod_i c_i(S_i). Equation
(3) implies divisibility by 2^max(0,ceil(d/k)-a): indeed, the sum of the
ceilings is at least the ceiling of the sum, and replacing a negative
individual lower bound by zero can only increase it.

Fix an integer p>=1. If d>k(a+p-1), then ceil(d/k)-a>=p. All such
coefficients vanish in Z/2^p Z. Thus **coefficientwise**, before any
variable identifications or sums, F modulo 2^p has degree at most

```math
 K_{scalar}=\min\{N,\ k(a+p-1)\},
 \tag{5}
```

where N is the number of test-variable incidences. Equivalently it is
enough to retain local supports with sum_i w_i(S_i)<p, a stronger
support-sensitive restriction that we do not need for the degree bound.

For f free Boolean variables choose p=f+1. The exact zero count is at
most 2^f<2^p, so its least nonnegative residue recovers it. The product
sum is

```math
 \#\{x:P_i(x)=0\ \forall i\}
 =\sum_{(S_i)}\left(\prod_i c_i(S_i)\right)
        2^{f-|\bigcup_i S_i|}\pmod{2^p}.
 \tag{6}
```

Here the union uses original variable names, whereas d counts their
separate incidence copies. An unused variable contributes its factor of
two. Equation (5) justifies discarding all tuples above the cutoff in
(6), including when several tests use the same original variable.

The source retains degree k(a+2n) for p=ell=n+1 using the auxiliary
algebra (Z/2^p Z)[V]/(V^ell) and the total h-order. At the same p=n+1,
the new bound is k(a+n), capped by N. The ambient algebra can have
ell=1: it is just Z/2^p Z. This is a smaller degree envelope and a
smaller coefficient representation, not yet a smaller asymptotic
running-time envelope.

## 3. Grouped Boolean networks and every entry

Use the source's high-incidence preprocessing. For original declared size
n, put lambda=ceil(log_2 n), and branch on variables in more than
`max(1,ceil(N_0/n))*ceil(sqrt(lambda))` test scopes. There are at most
n/sqrt(lambda) such variables. On each branch normalize again, reject a
constant-one equation, and drop constant-zero equations. Let f<=n be
the number of remaining declared variables, including unused ones.
If no equations remain, return 2^f. The surviving scope sizes and
variable loads are bounded by fixed powers of lambda, as in the source.

Set J=ceil(n^(1/4)). Partition both the a tests and the f free variables
into J groups, balanced on each side. There are at most
n^(3/4) lambda^O(1) incidences at each group vertex. Let N_gh count
incidences between test group g and variable group h. Enumerate degree
arrays d_gh with 0<=d_gh<=N_gh and sum d_gh<=K, where
K=min(N,k(a+f)). There are at most (K+1)^(J^2) arrays.

For one fixed array, give pair (g,h) exactly
ceil(log_2 binom(N_gh,d_gh)) Boolean wires. The two endpoints decode
the same lexicographically indexed subset of incidences. If the index
is invalid, its tensor entry is zero. If the binomial is one, the
unique subset uses no wires; it may be the full incidence set, not
only the empty set. Unranking with binomial coefficients needs only
polynomial time and space: the binomial integers have at most N bits,
and N=n lambda^O(1).

The test-group tensor entry is the scalar product

```math
 T_g=\prod_{i\in\mathcal T_g}c_i(S_i)\pmod{2^{f+1}}.
```

Use (4) one test at a time. The variable-group entry is

```math
 X_h=2^{|\{v\in\mathcal X_h:v\notin\bigcup_i S_i\}|}
       \pmod{2^{f+1}}.
```

Thus every retained incidence monomial occurs in exactly one array
and one valid wire assignment. The contraction sums its coefficient
times the Boolean assignment sum. The sum over arrays is (6); all
other coefficients vanish by (5). There is no coefficient-sum map
after contraction and no V-coordinate to decode.

For each array its wire count obeys

```math
 M\le J^2+\log_2\prod_{g,h}\binom{N_{gh}}{d_{gh}}
  \le J^2+\log_2\binom{N+K}{K}
  =O_{k,c}(n\log\log n).
 \tag{7}
```

The middle bound encodes the selected squarefree subset as a monomial
of degree at most K in N variables; stars and bars bounds their total
number by binom(N+K,K). If K=0 or N=0 there are no wires and the
scalar is evaluated directly. The final bound uses
K=O(n), N<=n lambda^O(1); when N<K before capping, M<=N=O(n)
also suffices. The maximum degree is at most the incidence count of
its group, since ceil(log_2 binom(q,d))<=q for every q>=1.

Choose the accepted contraction theorem's size parameter s=n*nu,
nu=max(1,ceil(log_2 lambda)), and ell=1, P_0=f+1. For all sufficiently
large n, (7) gives O(s) wires, and the group degrees are below
s^(9/10). Equation (4) computes each entry in
2^(lambda^O_{k,c}(1)) times a polynomial; this is eventually at most
poly(s)*2^(A*s^(9/10)) for a fixed A. Entries use polynomial space,
including counters and accumulators. The graph and entry descriptions
are polynomial length, as are all bit lengths. Thus all hypotheses of
`thm:tensor-contraction` hold over the scalar ring it explicitly permits.

The contraction's modes, packets, recursion, precision increases,
canonical lifting, interpolation and scalar extension remain exactly
those of the accepted theorem. Applying that theorem charges them
together; they are not assumed free or reimplemented by our oracle.
Using ell=1 stays closed under all its operations. The theorem still
has unspecified constants; a smaller degree envelope is not a proved
constant factor improvement in its running time.

The finite exceptional range depends only on fixed k,c. One uniform
algorithm computes the explicit graph/entry parameter bounds and uses
direct Boolean enumeration if these do not meet the fixed constants
in the accepted contraction theorem. They eventually do, so fallback
is confined to a bounded range. It preserves the claimed eventual
time and polynomial-space bounds.

## 4. Complete composition

Per sparse query, the contraction exponent is O(n*nu/sqrt(lambda)).
High-incidence branching adds at most n/sqrt(lambda); enumerating
degree arrays adds O(sqrt(n)*log(n)). Process both sequentially and
sum branch counts in an (n+1)-bit integer accumulator. Within a
branch, recover its exact count from its residue modulo 2^(f+1).
The sums are exact integers, and the branch solution sets are disjoint.

For an arbitrary fixed-width CNF, retain the accepted sparsification
with sigma=1/ceil(sqrt(lambda)), including its disjointness and
2^O(n/sqrt(lambda)) tree size. Retain all initial parity checks,
every tested greedy candidate, the count comparisons that select a
row, and the final count query. Each queried system, even a rejected
candidate that accepts nonsolutions of the original CNF, satisfies
the sparse-query hypotheses. Our proof holds for every such system;
it does not assume that only the ultimately selected systems occur.
There are 2^(lambda^O_k(1)) candidates and preprocessing work per
leaf, which is lower order than n*nu/sqrt(lambda).

Input normalization takes a fixed polynomial in n+m for fixed width.
The total deterministic exact-counting time is still

```math
 (n+m)^{O_k(1)}\,2^{O_k(n\log\log n/\sqrt{\log n})},
```

with polynomial space. The unchanged fixed-density clause network
retains its O_D(n/sqrt(log(n))) exponent; tiny inputs, empty clauses,
the empty formula, tautologies, and unused declared variables retain
the source's explicit treatment. Exact counting also decides and
supports variable self-reduction for search, with a polynomial number
of calls if search is requested. The contribution here is counting.
No randomness, error probability or amplification is introduced.

There is no new alpha: it remains 1/2. Neither the general-density
iterated logarithm nor the root square-root saving has changed.

## 5. Sharpness of the scalar degree bound

Fix k>=1 and f=a>=2k. On variables cyclically indexed modulo f, take
test i to be the XOR of the two disjoint degree-k monomials supported
on `{i,...,i+k-1}` and `{i+k,...,i+2k-1}`. In the incidence variables,
its projector is `1-A-B+2AB`. The unique full-incidence monomial of
the whole product has degree 2kf=k(a+f) and coefficient 2^f. Every
original variable is covered, so its variable-side assignment weight
is one. It survives modulo 2^(f+1). Lowering the cutoff by one drops
this unique top-degree monomial and changes the answer by 2^f modulo
2^(f+1). The generic scalar cutoff cannot be decreased uniformly.

Each scope has size 2k and each variable has load 2k; the source's
high-incidence step fixes none of them. This is a statement about this
encoding, allowing repeated or linearly related equations. It is not
a lower bound on algorithms that preprocess the equations differently.

## 6. Why this alone cannot remove log log n

There are normalized, low-load families with exponentially many
retained, nonzero incidence coefficients even for the scalar lift.
Here is an explicit family for every fixed k>=2 and arbitrarily large
n that are powers of two. Let L be the largest odd integer at most
log_2(n); for large n, 1<L and L+k-1<n. Put

```math
 m_j(x)=x_jx_{j+1}\cdots x_{j+k-1},\qquad
 P_i(x)=\sum_{j=0}^{L-1}m_{i+j}(x)\pmod2,
```

with all indices modulo n, and take a=n tests. Each equation has L
distinct degree-k terms, scope L+k-1, and every variable belongs to
exactly L+k-1 scopes. There is no high-incidence branch. The equations
are linearly independent as vectors of monomial coefficients: their
matrix is multiplication by g(y)=1+y+...+y^(L-1) modulo y^n-1 over
F_2. Since n is a power of two, y^n-1=(y+1)^n, and g(1)=1 because
L is odd. Thus the circulant is invertible.

For a support that is exactly one of a test's degree-k terms, (2)
has just its singleton summand. Distinct terms of equal size cannot
be proper subsets of that support. Its coefficient is -1. Choose
one such term independently at each of the n tests. This yields
L^n different incidence monomials of degree kn, all with coefficient
(-1)^n, and all satisfying the scalar cutoff k(a+n)=2kn. Each covers
at least k original variables, so its individual contribution after
the variable assignment sum also survives modulo 2^(n+1).

Consequently this encoding can have

```math
 L^n=2^{\Theta(n\log\log n)}
```

retained nonzero coefficients. Group arrays do not eliminate this
support entropy: there are only 2^O(sqrt(n)*log(n)) arrays. Some
array therefore has at least L^n divided by that many nonzero valid
assignments, requiring Omega(n*log(log(n))) wires in any injective
Boolean indexing of its monomials. Equation (7) has the right order
for this coefficientwise indexing scheme.

This does not rule out aggregating coefficients, changing bases or
the contraction kernel. In fact this witness's row space has the
sparser basis of the individual m_j equations, since its circulant
matrix is invertible. A row-space change is a changed premise, not
a contradiction to the support count of the stated input encoding.

## 7. A control for the refuted even-node shortcut

The user supplied a prior attempt to replace Hermite recovery by an
even-node evaluation modulo two. It inferred F(t)=F(0) mod 2 from
the source's shifted integrality. This is false. In
`eq:tensor-cauchy`, take L=4, alpha=8, and the diagonal entry

```math
 W_{00}(T)=\frac{\prod_{q\in\{-4,-3,-2,-1,1,2,3\}}(T-q)}{-144}.
```

It has W_00(0)=1 and W_00(-2)=0. Its global leading coefficient
is -1/144, which is not two-adically integral. Every shifted
polynomial W_xy(t+8z), for t in the eight-node grid, is
coefficientwise two-adically integral, exactly as the accepted
lemma states. Those facts are compatible. A single real port in
slot zero at each end, with unary tensors selecting bit one, gives
the corresponding deformed contraction F(T)=W_00(T).

The checker verifies all 128 shifted blocks with exact rational
arithmetic, as well as the two unequal values. This is a local
counterexample to the proposed congruence, not an audit of the
accepted theorem. The scalar lift in Sections 1-4 instead has
globally integral coefficients by construction.
