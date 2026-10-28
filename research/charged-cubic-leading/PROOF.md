# The leading charge coefficient of the cubic moment

This is an author-checked, AI-assisted component argument, not an independent
review or an improved SAT bound. The charged operators, source's Laurent
coefficient reading and binomial contraction identity are from
[PR #11](../charged-operator-moments/PROOF.md). PR #32 studies a distinct
high-degree extraction/capacity obstruction; this note extracts the fixed
coefficient q^3 and does not assume its input rank.

## Scalar coefficient and explicit pairing

Fix grade h>=1, integer charge q, output energy E, and source labels
mu,nu, both partitions of h. Write

```math
 M_{\mu\nu}(q)=\sum_s {s+1\choose3}
       Q_s^{(q)}(a^\mu,b^\nu).
```

As an operator on V_E, M is a polynomial in q of degree at most 3. Its
coefficient of q^3 is `H_h(mu,nu) Id`, with the same H for every E.
Set `m_mu!=product_j mult_j(mu)!` and

```math
 L=\sum_{j\ge2}(j-1)u_{j-1}\partial_{u_j},\qquad
 C=\sum_{j\ge1}(-1)^{j-1}j u_j.
```

All operations below are finite after extracting weight h. Then

```math
 H_h(\mu,\nu)=h!\frac{m_\mu!}{m_\nu!}
 [u^\mu t^3]\;\exp(tC)\exp(L)\exp(t\partial_{u_1})u^\nu.    \tag{1}
```

The last exponential acts first. In particular, it is not equivalent to
substituting `u_1+t` after applying exp(L).

## Derivation

The source's common Laurent polynomial F has coefficient reading
`F(w1,w2)=sum_s Q_s w1^s w2^(-s)` on each output matrix coefficient.
The cubic weight is the z^3 coefficient of `(1+z)^(s+1)`, so M is the
z^3 coefficient of `(1+z)F(1+z,1)`. Normal-order terms with total uncontracted weight r
carry z^r and at most r fields. Each charged zero mode supplies one factor
q. Thus no term contributing through degree 3 has q-degree above 3. A
q^3 contribution must have exactly three uncontracted fields, all of weight
one, and use their three zero modes. It occurs at order z^3, has scalar
coefficient independent of E, and is unaffected by the extra factor 1+z.

For each encoded first-side part r, leaving its t1 field uncontracted
contributes `(-1)^(r-1) r`; collecting an arbitrary labeled set of such
fields gives exp(tC). A second-side uncontracted weight-one field can only
come from a part 1, and selecting them gives exp(t partial_(u1)) before
contraction. The contraction of an encoded first-side part r with a
second-side part m is `m binom(m-1,r-1)`, the identity in PR #11. After
cancelling the source's `product m` factors, its multiplicative action on
u is exp(L). Counting repeated parts yields the same factorial ratio
`h! m_mu!/m_nu!` as in that predecessor. Extracting t^3 and weight h gives
(1). The argument is entrywise, so the q^3 coefficient is H times the
identity on the entire V_E, not merely on a compressed codebook.

## Four-charge crossing and cost boundary

For each shift define the exact rational operator

```math
 D_s=\bigl(Q_s^{(2)}-3Q_s^{(1)}+3Q_s^{(0)}-Q_s^{(-1)}\bigr)/6.
```

Because M(q) has q-degree at most 3, finite differences give
`sum_s binom(s+1,3) D_s=H Id`. The individual D_s need not be leading
q-coefficients; the identity is for the weighted sum. Weights vanish at
s=-1,0,1. If an N-by-N minor H_IJ is invertible, local multiplication by
its inverse on the first input axis produces an exact N-label crossing on
any N selected output states. The checker finds such an 8-by-8 minor at
h=9; its labels and inverse are recorded in verification.json.

Each D_s is a sum of four charged source pieces. The two cut ranks are at
most four times the corresponding source term bounds; local first-axis
normalization does not increase them. There are polynomially many shifts
and four fixed charges. For an all-size construction one must prove a
uniform family of minors of size `N=2^lambda` at h=O(lambda^2), with
p(h)=2^O(lambda), and pay exact entries, the rational normalizer, finite
field conversion, outer reduction/queries, precision, recursion, recovery,
time and space. A generic inverse can have exponentially many bits in
lambda; it is not assumed polynomial-height. PR #17's bounded rational
transfer may be applicable once its hypotheses are checked.

The checker finds ranks through h=15 that match
`p(h)-p(h-3)-[h even]` for h>=3. This is a finite observation, not an
all-grade rank theorem. Deleting only shifts -1,0,1 does not reduce the
source's leading central envelope, and no better rho or SAT bound is
claimed even conditionally on that rank pattern.
