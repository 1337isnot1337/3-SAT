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
space, then **every c_r vanishes**, and the extracted operator is zero.
Thus no nonzero scalar operator on the full output grade can be obtained
from such outer shifts for this label pair. This does not rule out a
pairing using different labels or a projected output compression.

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

## Nonsingularity from reflected walks

It remains to show that G_1=...=G_h=0 forces c=0. Consider the square
kernel K_(j,r)=B_(r+j)+B_(r-j) with j=1,...,h-1 and r=0,...,h-2.
Reverse its columns and write a=h-r, so the starting coordinates a are
2,...,h in increasing order. The entry K_(j,r) counts ordinary length-2h
walks on the integers starting at 2a and ending at either +2j or -2j.
Folding at zero gives walks on the nonnegative integers with steps +/-1,
where a departure from zero has weight 2 and every other step has weight 1.
The binomial counts are exactly B_(r+j) and B_(r-j).

These weighted walks form a layered planar directed network. All vertices
reachable at a given time have the same parity, so two paths that exchange
order share a vertex. By the Lindstrom--Gessel--Viennot determinant lemma,
the determinant of the matrix with sources 2a in increasing order and
sinks 2j in increasing order is the positive weighted sum of vertex-disjoint
families connecting them in that order. At least one such family exists:
from each 2a, take two downward steps, then repeat an upward and a downward
step h-1 times. It ends at 2(a-1), stays positive and remains disjoint
from the other paths. Hence the determinant is strictly positive. The
square K matrix is nonsingular, so G_1=...=G_(h-1)=0 implies c=0.

Equation (3) is invariant under s -> -s. Consequently c=0 means each
symmetric weight sum vanishes, and the entire extracted operator on this
label pair is zero. The proof works over characteristic zero, since the
integer determinant is nonzero; reduction modulo a prime that divides it
needs separate analysis.

## Checks and limits

The h-1 scalarity equations `(-1)^j G_j = -G_1` for j=2,...,h give an
(h-1)-square rational matrix in c_0,...,c_(h-2). Exact elimination finds
rank h-1 for every h=2,...,20, and also checks the square K rank. For
h=2,...,6, an independent folded-walk dynamic program checks its binomial
entries. These finite calculations are not the all-size proof above.

`outer_filter.py` checks (3) by exact charge interpolation on every output
partition of E=0,...,h, every shift -h,...,h, and both operator orders
for h=2,3,4. It also computes the finite constraint ranks and folded-walk checks above. Saved
results and predecessor hashes are in `outer-filter-verification.json`.
The q-degree support bound of the parent package still limits input-label
capacity, but it does not by itself relate shift width to charge degree.
