# Crossing pieces from Walsh support

Status: finite checks passed for the stated scope; written all-size
construction is AI assisted and not independently reviewed. No improved
piece rate or SAT bound is asserted.

## 1. Both ranks are support counts

Let `r=lambda`, `N=2^r`, and let `a,b,x,y` be r-bit strings. Define real
Pauli matrices by

```math
 \Gamma_{a,b}(x,y)=\mathbf{1}_{\{x=y+a\}}(-1)^{b\cdot y},
 \qquad q(a,b)=(-1)^{a\cdot b},
```

with addition and dot products over `F_2`. For a rational function f on
the `N^2` labels define

```math
 M_f(x,y,u,v)=\frac1N\sum_{a,b}f(a,b)
                                  \Gamma_{a,b}(x,y)\Gamma_{a,b}(u,v).
 \tag{1}
```

The Pauli matrices are an orthogonal basis of all N-by-N matrices:
their inner products are `N` for equal labels and zero otherwise.
Consequently the `(x,y)|(u,v)` flattening of (1) has exact rational rank
`|supp f|`.

Define the unnormalized symplectic Walsh transform

```math
 \widehat f(c,d)=\sum_{a,b}(-1)^{b\cdot c+a\cdot d}f(a,b).
```

The Bell vectors `B_(c,d)(x,u)=1_{u=x+c}(-1)^(d dot x)` are an orthogonal
basis, each of norm squared N. The operators `Gamma_(a,b) tensor Gamma_(a,b)`
have these vectors as simultaneous eigenvectors, with eigenvalue
`(-1)^(b dot c+a dot d)`. Thus the other flattening has the exact formula

```math
 M_f(x,y,u,v)=\frac1{N^2}\sum_{c,d}\widehat f(c,d)
                                  B_{c,d}(x,u)B_{c,d}(y,v),              \tag{2}
```

and exact rank `|supp hat f|`. These facts also give explicit factorizations;
they are not merely rank bounds. A direct character sum gives

```math
 M_q(x,y,u,v)=[x=v][y=u].                              \tag{3}
```

Therefore any decomposition `sum_i f_i=q` gives crossing pieces with shared
bit total `ceil(log2 |supp f_i|)+ceil(log2 |supp hat f_i|)`.

If D clears every rational denominator of all f_i values, multiply (1)-(3)
by `D N^2`. The row factors have integer coefficients `D N f_i`; the column
factors have integer coefficients `D hat f_i`. This gives a common positive
integer multiple of the crossing with integer factors in both directions.

## 2. Permutation symmetry makes the coefficient space small

Each coordinate of (a,b) has four letters `0=(0,0), 1=(1,0), 2=(0,1), 3=(1,1)`.
A type `alpha=(alpha_0,...,alpha_3)` counts those letters and has total r.
There are `binom(r+3,3)` types; a type's multiplicity is
`m_alpha=r!/prod(alpha_j!)`. Symmetric f is specified by one value per type,
while its actual word support is `sum_(alpha:f_alpha!=0) m_alpha`.

The one-coordinate Walsh matrix is

```math
 H=\begin{pmatrix}
 1&1&1&1\\1&1&-1&-1\\1&-1&1&-1\\1&-1&-1&1
 \end{pmatrix}.
```

Its compressed rth-power matrix T has entries

```math
 T_{\beta,\alpha}=[z^\alpha]
        \prod_{j=0}^3\left(\sum_{k=0}^3 H_{jk}z_k\right)^{\beta_j}.
 \tag{4}
```

This follows by summing the character over all words of fixed type alpha.
One has `T^2=4^r I`, and `T q=2^r q` with `q_alpha=(-1)^alpha_3`.
These identities are useful independent finite checks of the compression.

## 3. An actual uniform adapted-basis decomposition

Order types by increasing `m_alpha`, with a deterministic lexicographic
tie break. Process the columns of T in that order. Starting with
`v_i=e_i`, eliminate its image's highest nonzero row using previously
stored pivot columns, adjusting v_i by the identical column operations.
Stop at the first unused pivot row `p_i`. Invertibility ensures that a
pivot always exists. Each v_i has support in the first i+1 coordinates,
coefficient one at coordinate i, and `T v_i` has highest nonzero row p_i.

The pivot rows are distinct. Hence these vectors simultaneously adapt
the two prefix flags: their first-coordinate supports adapt the original
coordinate flag; a linear combination can lie in an image prefix only
if its nonzero coefficients have pivot rows in that prefix. This also
gives exact intersections for the two flags. Equal-multiplicity types can
be grouped when charging the complete support prefix.

Triangular back substitution expresses q uniquely as `sum_i c_i v_i`.
Discard zero c_i and set `f_i=c_i v_i`. Its transform is the already
computed `c_i T v_i`. This is an explicit decomposition (3), not an
assumption about an achievable support profile.

All type counts, matrix entries, column operations, decompositions and
supports use exact integers or rationals. There are only `O(r^3)` pieces.
Matrix entries have `O(r)` bits and rational elimination has polynomial
bit complexity by determinant bounds. A common product of denominators
also has polynomially many bits. Given a piece and input word one finds
its type in polynomial time; to index support words, enumerate the
polynomially many nonzero types and unrank words of a chosen type by
multinomial coefficients. Both factors in (1)-(2) then have uniform
`2^O(r)` evaluation and polynomial coefficient heights, with zero returned
for invalid codes.

Thus this procedure is a uniform family of actual integer crossing pieces.
The still-unproved part is a sufficiently small **asymptotic support rate**.
Without it, no stronger rho or SAT time follows. The trivial universal
rate is only shared-bit total at most `4r`, before any useful refinements.

## 4. What the finite screen can establish

The registered screen computes every type, every T entry, the exact pieces,
their two word-support counts and shared-bit totals for r=1,...,8. It also
checks (1)-(3) and direct flattening ranks for every retained piece at r=1,2.
This validates the finite family and can identify a structural question;
it does not prove an eventual slope, optimality among all decompositions,
or a faster SAT algorithm. Constants and logarithmic correction terms in
the external piece contract must not be inferred from a finite plot.

The separate [global symmetry dual](SYMMETRY-BARRIER.md) now proves that
this symmetric Pauli-diagonal coefficient class cannot meet the target,
regardless of the adapted basis or number of summands. That proof does
not use a finite extrapolation and does not cover nonsymmetric pieces.

The target for a genuine improvement is a proved eventual bit total below
`2 sqrt(2) r+O(log r)`, with all preceding contracts retained and the full
master recursion and arbitrary-density costs charged. The source pins and
prior work are recorded in [README.md](README.md). No novelty, formal
verification or independent review is claimed.
