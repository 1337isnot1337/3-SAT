# Outer-shift scalarity constraints

This author-checked continuation concerns one all-ones label pair, the
q^(2h-2) coefficient, and the full grade-h output space. It does not
cover restricted or compressed output codebooks, other label pairs,
charge-dependent normalization, or a complete crossing family.

## An all-size necessary condition

For h>=2 let a=(1^h), and combine raw charged pieces Q_s(a,a) with
q-independent scalar weights w_s supported on `2<=|s|<=h`. Define

    c_r=(-1)^r(w_(h-r)+w_-(h-r)),  0<=r<=h-2,
    B_k=binom(2h,k), with B_k=0 outside 0<=k<=2h,
    G_j=sum_(r=0)^(h-2) c_r (B_(r+j)+B_(r-j)).             (1)

If the extracted q^(2h-2) operator is scalar on the full grade-h output
space, then **G_j=0 for every j=1,...,h**. In particular, any nonzero
scalar value must come entirely from the output-independent terms. This
condition does not prove those terms vanish.

For a proof, set r=h-s, let m_j be part multiplicities in a grade-E
output partition, and define

    K_r=sum_(j=1)^r (-1)^(r-j) B_(r-j) j
       =(-1)^(r-1) binom(2h-2,r-1),                         (2)

where the endpoints r=0,2h have K_r=0. Direct normal ordering yields

    [q^(2h-2)]Q_(h-r)(a,a)
     =(-1)^r B_r 2h(h-1)E + h^2 K_r
       +h^2 sum_(j=1)^E (-1)^(r+j)
          (B_(r+j)+B_(r-j)) j m_j.                          (3)

The first term comes from two nonzero currents in a single factor, with
alternating index r. The rest comes from one nonzero current in each
factor: the two mode orders contribute `j m_j` and `j(m_j+1)` when their
indices are in range. This is diagonal for E<=h. The binomial symmetry
and (2) show that the same coefficient at shifts s and -s is identical.

At E=h, compare the partition `(j,1^(h-j))` with `(1^h)`. Scalarity
forces `(-1)^j G_j` to have the same value t for all j=1,...,h. To show
t=0, put

    H(z)=sum_(r=0)^(h-2) c_r(z^r+z^(2h-r)),
    F(z)=(1+z)^(2h) H(z).

H has at most 2h-2 nonzero monomials. The coefficient of z^(2h+j) in F
is G_j, and F is palindromic of degree 4h. If t is nonzero, the h
coefficients on each side of the central coefficient alternate in sign,
and the two coefficients adjacent to the center agree. Irrespective of
the central coefficient, the coefficient sequence of F has at least
2h-2 sign changes. H has at most 2h-3. Multiplying a real coefficient
sequence by `(1+z)` cannot increase its sign changes (zeros are omitted),
a contradiction. For complex weights, apply the real argument to the
real or imaginary part of a hypothetical nonzero t. Therefore t=0 and
all G_j vanish.

## Finite rank evidence and open step

The h-1 scalarity equations `G_j*(-1)^j = -G_1` for j=2,...,h give an
(h-1)-square rational matrix in c_0,...,c_(h-2). Exact elimination finds
rank h-1 for every h=2,...,20. If this matrix were proved nonsingular for
all h, the symmetric shift weights would all vanish; antisymmetric
weights cancel in this particular output operator by (3). The finite
rank list is **not** an all-size proof, and no stronger conclusion is
asserted here. It would concern only this one input-label pairing even if
proved.

`outer_filter.py` checks (3) by exact charge interpolation on every output
partition of E=0,...,h, every shift -h,...,h, and both operator orders
for h=2,3,4. It also computes the finite constraint ranks above. Saved
results and predecessor hashes are in `outer-filter-verification.json`.
The q-degree support bound of the parent package still limits input-label
capacity, but it does not by itself relate shift width to charge degree.
