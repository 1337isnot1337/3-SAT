# Charged crossing pieces and their first-moment pairing

These are author-checked, AI-assisted arguments about a changed operator
representation. They are not an independent review of Anthropic's theorem,
a formal proof, or a larger SAT alpha. The external definitions are those
of Appendix B in [Hexagon 2610.00577v1](https://hexagonmath.org/2610.00577v1),
with source and predecessor pins in [SOURCES.json](SOURCES.json).

## 1. The charged variation retains the zeroth crossing

For an integer q, keep `D_-k=t_k` and `D_k=k partial/partial t_k` for
positive k, and add `D_0=q Id`. In the normal-ordered definition of a[r],
allow zero indices as well as nonzero ones, using the same coefficient
`binom(-k-1,n-1)`. Thus a zero index on a part n contributes
`(-1)^(n-1) q`. Equivalently the source recurrence O2 gains the term
`(-1)^(n-1) q a'[r]` when `a=t_n a'`.

Keep the source dual polynomials `a_mu` and scaled monomials `b_nu` at
weight h, and its binomial alternation defining Q_s. The nonzero-mode
commutators are unchanged and D_0 is central. The normal-ordering argument
for the two operator orders therefore still applies. Its common Laurent
polynomial, on an energy-E matrix coefficient, has the form

```math
 F_q(z_1,z_2)=\sum\Gamma\,(z_1-z_2)^r n_q,
 \qquad r=\text{total weight of the uncontracted fields}.
```

This is the source's contraction expansion; the change adds the regular
Laurent term `(-1)^(n-1)q z^-n` to each current of weight n. Terms with
r=0 are fully contracted and do not involve q. Every r>0 term vanishes
at `(z_1,z_2)=(1,1)`. Hence the zeroth sum is unchanged:

```math
 \sum_s Q_s^{(q)}(a_\mu,b_\nu)=h![\mu=\nu]\operatorname{Id}. \tag{1}
```

The source energy bound `|s|<=E+h` still holds: in the original order
the first output grade is negative above that interval; in the reversed
order it is negative below it. Equality of the two orders gives both
vanishings. This also justifies every finite moment below.

At E=h and the source's binary-encoded basis, (1) supplies integer
crossing pieces for each fixed integer q. Both directional intermediate
spaces have exactly the original partition dimensions. The source table
recurrence gains one scalar summand, so its exponential-in-lambda
construction bound and polynomial-in-lambda integer bit-height bounds
are retained for fixed q. The factorization ratio remains
`rho=1/sqrt(2)`. This supplies a family of valid component variations,
not a faster full algorithm.

## 2. Exact first-moment formula

Let `m_mu!=product_j mult_j(mu)!`, and use another copy of the polynomial
ring, `R=Q[u_1,u_2,...]`, with `weight(u_j)=j`. Define

```math
 L=\sum_{j\ge2}(j-1)u_{j-1}\frac{\partial}{\partial u_j},\qquad
 P=\sum_{r\ge0}\frac{(-1)^r}{r!}u_{r+1}L^r,\qquad T=PL.
```

These sums are finite on any polynomial. For partitions mu,nu of h,
on every energy space V_E,

```math
 \sum_s s Q_s^{(q)}(a_\mu,b_\nu)
 =q h!\frac{m_\mu!}{m_\nu!}[u^\mu]T(u^\nu)\operatorname{Id}. \tag{2}
```

Here is a coefficient derivation. In the Laurent expansion of Section 1,
only r=1 terms can contribute to the first derivative at the diagonal.
Exactly one current of weight one remains. Its coefficient between
equal-energy vectors is q times the identity: all its nonzero modes
change energy.

The contraction coefficient for fields t_n on the first side and t_m
on the second is

```math
 \gamma_{n,m}=(-1)^{n-1}\frac{(n+m-1)!}{(n-1)!(m-1)!}.
```

For the encoded first-side factor
`(-1)^(r-1) y_r=(-1)^(r-1) sum_(n=1)^r binom(r,n)t_n`, its contraction
with t_m simplifies, by the finite binomial identity, to

```math
 \widetilde\gamma_{r,m}
 =\sum_{n=1}^r(-1)^{r-1}\binom rn\gamma_{n,m}
 =m\binom{m-1}{r-1}.                                      \tag{3}
```

If the free current comes from b_nu, the contracted column weight is
h-1 while the encoded row weight is h. Each factor in (3) requires
column part >= row part, so this contribution is zero. If the free
current comes from the factor indexed by r in mu, its coefficient is
`(-1)^(r-1)r`. All other factors contract using (3). In particular the
row partition has one more part than the column partition.

The same calculation with no free current proves the fully contracted
pairing in (1) directly: equal total weights force every matched pair
of parts to be equal; repeated-part multiplicities and the scale of
b_nu then give exactly h! on the diagonal and zero off it.

Let `A(u_j)=sum_(n=1)^j binom(j-1,n-1)u_n`. Counting assignments of the
remaining factors and the factorials of repeated parts gives the scalar
in (2), divided by q h!, as

```math
 \frac{m_\mu!}{m_\nu!}[u^\mu]
 \left(\sum_{r\ge1}(-1)^{r-1}r u_r\right) A(u^\nu).
```

Since `A=exp(L)`, extracting weight h is the same as using

```math
 \sum_{r\ge1}\frac{(-1)^{r-1}}{(r-1)!}u_rL^r=PL.
```

This proves (2), including independence from the output energy E.
Equations (2)-(3) are also checked independently against the direct
normal-ordered operators at the finite energies listed in the artifact.

## 3. Nilpotence and exact rank

The two summands of the derivative of each `u_(r+1)L^r/r!` cancel after
shifting r, so `LP=0`. Consequently `T^2=PLPL=0`. Also L preserves
the number of factors and P adds one factor. Thus T strictly raises
partition length. Any principal submatrix on a common set of encoded
labels is nilpotent by this length filtration, whether or not that
submatrix preserves the stronger square-zero relation. The first-moment
pairing on such a common nonempty label space cannot be inverted.

On the full weight-h space, for h>=2, the rank is exactly

```math
 \operatorname{rank}T_h=\dim\ker L_h=p(h)-p(h-1).            \tag{4}
```

To prove both surjectivities needed for (4), split by partition length m.
Identify length-m monomials `u_(a_1+1)...u_(a_m+1)` with the averaged
symmetric monomials in m variables `x_1^a_1...x_m^a_m`. Under this
identification, L is `sum_j partial/partial x_j`. It maps homogeneous
symmetric polynomials of positive degree surjectively to the next lower
degree: write `c=(sum x_j)/m`, use translation-invariant differences
`x_j-c`, and integrate the powers of c. The primitive stays symmetric.
Thus `L:R_h -> R_(h-1)` is surjective when h>=2.

Under the same identification, P is the averaging operation

```math
 (Pf)(x_1,...,x_{m+1})
 =\frac1{m+1}\sum_{j=1}^{m+1}
 f(x_1-x_j,...,\widehat{x_j-x_j},...,x_{m+1}-x_j).
```

For a symmetric translation-invariant polynomial g in m+1 variables,
set `f(x_1,...,x_m)=g(x_1,...,x_m,0)`. Every summand above equals g,
so P maps onto ker L at the target length. A positive-weight invariant
of length one exists only at weight one; thus there is no missing
length-one component when h>=2. Since L is surjective and P maps onto
ker L, `image T_h=ker L_h`. Dimension subtraction proves (4).

For additional explicit controls, let
`B=sum_(j>=1) u_(j+1) partial/partial u_j`. On length m, `[L,B]=m Id`.
A finite right inverse of L on any nonvacuum input is

```math
 R_L=\sum_{j\ge0}\frac{(-1)^j}{m^{j+1}(j+1)!}B^{j+1}L^j.
```

The two sums in `LR_L` cancel except for the identity. On an invariant
of length m, a right inverse for P is `(1/m) partial/partial u_1`, as
the symmetric evaluation formula also shows. The checker verifies these
identities independently on the finite grades in its saved output.

## 4. What the image size permits and what remains unpaid

The number in (4) counts partitions with no part equal to one. Write it
as r_h. It is nondecreasing for h>=2: increase the largest part by one,
an injection whose image has a unique largest part. Removing all ones
from an arbitrary partition gives

```math
 p(h)=1+\sum_{j=2}^h r_j\le1+(h-1)r_h.
```

Therefore `(p(h)-1)/(h-1)<=r_h<=p(h)` and
`log r_h=log p(h)+O(log h)`. Its leading label capacity is the same
as that of the original partition space. This is an image-dimension
statement, not an implemented recovery construction.

An asymmetric choice of row and column label subspaces could use a
nondegenerate minor of this pairing. Its uniform coordinates, integer
denominators, bit heights and entry costs still need proof; a generic
inverse of an exponentially large matrix does not automatically meet
the piece contract. Even removing just the central shift leaves nearby
shifts with the same leading `rho=1/sqrt(2)` envelope. A larger alpha
would need a further change, for example a paid filter that avoids an
entire range of expensive intermediate spaces.

No all-h rank lower bound for the original uncharged pieces, no larger
alpha, and no selected-result change follow from this package.
