# Endpoint pieces have maximal directional rank

## Statement

Use the pinned Anthropic Appendix-B crossing family. Fix any energy `h>=1`
and any nonempty set S of distinct partitions of h (in particular, the
source's binary codebook). Let `d=|S|` and form its four-index tensors
`A_s(x,y,u,v)`. Over Q the two endpoints satisfy

    rank_row(A_-2h)=1,  rank_col(A_-2h)=d²,
    rank_row(A_+2h)=d², rank_col(A_+2h)=1.            (1)

Here row means `(x,y)|(u,v)` and col means `(x,u)|(y,v)`. This holds for
every such codebook, not just the source's first `2^lambda` partitions.
For the source binary codebook, the maximal rank is `2^(2 lambda)` and
both endpoint costs are exactly `(0,2 lambda)` or `(2 lambda,0)` in the
respective directions. The lower bound is rational rank; the matching upper
bounds are the source's integral endpoint factorizations and trivial full
factorization. No SAT bound improvement is claimed.

## A positive-definite partition pairing

Write `ell(mu)` for the number of parts of mu, `z_mu=product_k k^m_k m_k!`,
and `s_mu=(-1)^(h-ell(mu))`. Define

    M_mu,nu = [1] (t^mu)[-h] t^nu,
    C_mu,nu = [t^nu] a^mu[h] 1,

using the source's `eq:ops` and `lem:dual`. Define, for positive integers
n,k,

    B(n,k) = (n+k-1)!/(n! k!) = binom(n+k,n)/(n+k).  (2)

For equal-length partitions, `B[mu,nu]` is the matrix with entries
`B(mu_i,nu_j)`. The operator formulas yield

    M_mu,nu = s_mu (product mu_i)(product nu_i) perm B[mu,nu],
    C_mu,nu = M_mu,nu / z_nu;                         (3)

both matrices are zero when the two lengths differ. To derive the first
formula, only positive modes can reach the vacuum in (O3); every derivative
must remove a factor of `t^nu`, so the lengths agree. Use
`binom(-k-1,n-1)=(-1)^(n-1) n B(n,k)`, account for the k from each
`nabla_k`, and sum all assignments, including the derivative multiplicities;
this is precisely the permanent. For C, only negative modes act on 1.
Each factor `(-1)^(n-1)y_n` creates mode k with coefficient

    (-1)^(n-1) sum_{j=1}^n binom(n,j)binom(k-1,j-1)
      = (-1)^(n-1) n B(n,k).

Summing over assignments produces the permanent divided by the factorials
of repeated parts of nu, yielding the stated relation to M.

The kernel B is strictly positive definite on every finite set of positive
integers: by Vandermonde,

    B(n,k) = integral_0^1 x^(n+k-1) sum_j binom(n,j)binom(k,j) dx.

For any nonzero real vector `(c_n)`, the quadratic form is a sum of
integrals of squares, and its `j=0` term is
`integral_0^1 x^(-1)(sum_n c_n x^n)^2 dx > 0`.
The symmetric tensor powers of its Gram vectors therefore give strictly
positive-definite permanent Gram matrices indexed by distinct multisets.
Thus each equal-length block of `perm B[mu,nu]` is positive definite;
any principal submatrix is also positive definite. Formula (3) shows that
both M and C, restricted to any S, are invertible: the remaining factors
are nonzero diagonal scalings, and the blocks have distinct lengths.

## Endpoint formulas

Let `D_v=h!/z_{mu(v)}` and `P_xy=s_{mu(x)} M_{mu(x),mu(y)}`.
At shift `-2h`, the source's row factorization `eq:half-row` has only
`i=2h`, with intermediate energy zero. The binomial taper selects the
weight-h part `s_mu t^mu` of `a^mu`, and `b^v[h]1=b^v`. Hence

    A_-2h(x,y,u,v) = P_xy D_v [u=v].                 (4)

P and D are invertible. The row flattening is a nonzero outer product,
while the column flattening is, up to permutations, a block diagonal
matrix with invertible P blocks and diagonal D; its rank is d².

At shift `+2h`, the source's column factorization `eq:half-col` has only
`i=0`, again through energy zero. It gives

    A_+2h(x,y,u,v) = C_xu D_v M_vy.                 (5)

C and M are invertible. The column flattening is a nonzero outer product,
while the row flattening is a Kronecker product of invertible matrices up
to permutations, so its rank is d². This proves (1).

## Implication for rectangular grouping

For a 2-row, q-column grid, there is one rectangle per pair of columns.
Choose `s=-2h` for edges of any graph G on the columns and `s=+2h` for
nonedges. Different rectangles use disjoint original diagonal-edge strings.
The column-network factor on a column pair has two straight equality wires
and one endpoint factor: its exact rational factor rank is `d^4` on graph
edges and `d²` on nonedges. For binary codebooks its exact factor cost is
`4 lambda` or `2 lambda` respectively. The branch is a valid term of the
source's expansion; no claim is made that the SAT input or all terms have
this pattern.

For any fixed integer group size `t>=2`, the elementary union-bound
argument in the companion branch `research/fixed-block-grouping-obstruction`
constructs, for all sufficiently large multiples q of t, graphs of density
at most `1/2+epsilon` for which every partition into t-column groups has a
full t-by-t edge block. In the grouped column factor for such a block, all
original edge variables are disjoint; the tensor product of `t²` full-rank
pair factors has rank `d^(4t²)`. Thus a common binary width L must satisfy
`L>=4 lambda t²`. If U is the ordered sum of the exact ungrouped pair
costs, the graph density bound gives

    K² L / U >= 2/(3/2+epsilon),  K=q/t.

This tends to 4/3 as epsilon decreases, up to the harmless finite-q factor.
It is a lower bound for the **uncontracted grouped pair factor** under this
specific equal-size, common-width column interface; a different direction,
nonuniform representation, changed crossing decomposition or global
algorithm may evade it. It does not prove a 3-SAT lower bound or a new alpha.
The asymptotic graph proof is nonconstructive. As a finite control, at
lambda=1 the graph on eight columns obtained by deleting a perfect matching
has 24 edges; all 105 pair partitions contain a full block. Its exact
ungrouped ordered pair cost is U=208, while common-width padding costs at
least K²L=256, a ratio of 16/13. The accepted OpenAI result is unchanged.
