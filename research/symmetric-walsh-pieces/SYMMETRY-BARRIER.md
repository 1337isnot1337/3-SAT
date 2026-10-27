# A global support dual for symmetric Pauli pieces

This proves an all-size obstruction for the coefficient class used in
[CONSTRUCTION.md](CONSTRUCTION.md). It is not inferred from the finite
screen. It allows arbitrary cancellations, arbitrary characteristic-zero
coefficients, and any finite number of pieces. No claim about arbitrary
crossing decompositions or SAT algorithms follows.

## 1. An invariant dual polynomial

Use the four-letter Walsh matrix H from the construction. For variables
`z=(z_0,z_1,z_2,z_3)`, put

```math
 J(z)=z_0z_1z_2z_3\prod_{j=0}^3(Hz)_j,
 \qquad L(z)=z_0+z_1.
```

Since `H^2=4I`,

```math
 J(Hz)=2^8J(z),\qquad L(Hz)=2L(z).
```

For `r=8k+s`, `k=floor(r/8)>=1`, `0<=s<8`, define

```math
 P_r(z)=J(z)^k L(z)^s.                                \tag{1}
```

It is homogeneous of degree r, satisfies `P_r(Hz)=2^r P_r(z)`, and is
divisible by `(z_0z_1z_2z_3)^k`. Let `m_alpha` be the orbit multiplicity
and define the symmetric coefficient function h_r by

```math
 P_r(z)=\sum_{|\alpha|=r}m_\alpha h_r(\alpha)z^\alpha.
```

Polynomial substitution is exactly the Walsh transform on these symmetric
coefficient functions. Hence `hat h_r=2^r h_r`.

The quadratic sign's letter vector is `q=(1,1,1,-1)`, and `Hq=2q`.
Thus

```math
 \langle h_r,q\rangle
 :=\sum_\alpha m_\alpha h_r(\alpha)(-1)^{\alpha_3}
 =P_r(1,1,1,-1)=16^k2^s\ne0.                         \tag{2}
```

This pairing is the sum over all `4^r` words, not an unweighted sum of
orbit values. That distinction is essential.

## 2. Both supports must contain an entire large orbit

Every nonzero coefficient of (1) has `alpha_j>=k` for all j. Among all
such compositions, the smallest orbit multiplicity is

```math
 m_r=\frac{r!}{(r-3k)!(k!)^3}
    =\frac{r!}{(5k+s)!(k!)^3}.                         \tag{3}
```

Indeed moving one unit from a smaller coordinate above k to a largest
coordinate increases the product of coordinate factorials. Repeating
gives `(r-3k,k,k,k)` up to permutation, maximizing that denominator.

Let f be any permutation-symmetric function. If `|supp f|<m_r`, none of
the orbits supporting h_r can have a nonzero f value. Thus
`<h_r,f>=0`. Walsh self-adjointness on word space also gives

```math
 \langle h_r,\widehat f\rangle
 =\langle\widehat h_r,f\rangle=2^r\langle h_r,f\rangle.
```

Therefore `|supp hat f|<m_r` likewise forces `<h_r,f>=0`.

Now suppose `sum_i f_i=c q` for any nonzero scalar c, with every f_i
permutation symmetric. By (2), at least one summand pairs nontrivially
with h_r. For that same summand,

```math
 |\operatorname{supp}f_i|\ge m_r,\qquad
 |\operatorname{supp}\widehat f_i|\ge m_r.              \tag{4}
```

This is a single-piece, two-support conclusion. It does not select
different large pieces for the two inequalities. It does not assume
positivity, bounded coefficients or a polynomial number of summands.

## 3. The asymptotic rate is worse than the accepted target

By the exact flattening-rank formulas in the construction, (4) implies
that some piece has combined shared-bit cost at least `2 log_2 m_r`.
Let

```math
 h_* = H_2(5/8,1/8,1/8,1/8)
     =3-\frac58\log_2 5.
```

Elementary factorial estimates give

```math
 \log_2 m_r=h_*r-O(\log r).
```

For completeness, monotonicity of log gives
`log(n!)=n log n-n+O(log(n+1))` by upper/lower integral sums.
Apply that to the five factorials in (3). Since
`k=r/8+O(1)` and every limiting proportion is positive, the resulting
entropy is `h_*+O(1/r)`. No fitted finite slope is used.

Consequently every such symmetric decomposition has a piece of cost

```math
 \left(6-\frac54\log_2 5\right)r-O(\log r).            \tag{5}
```

The leading coefficient is strictly above three: `5^5<2^12` implies
`log_2 5<12/5`. Hence (5) exceeds `3r-O(log r)`, while the accepted
crossing target is `2 sqrt(2) r+O(log r)<3r+O(log r)`.
More precisely the necessary rho is at least
`h_*/2 = 3/2-(5/16)log_2 5`, approximately 0.7744, which is larger than
`1/sqrt(2)`. No additive logarithmic term can close that linear gap.

Thus permutation-symmetric **Pauli-diagonal** pieces cannot even match
the accepted piece rate, and cannot improve alpha through that contract.
The earlier finite constructor's very small initial cases are not an
asymptotic lead.

## 4. Fixed numbers of color blocks do not remove the obstruction

The dual tensorizes. If a coefficient function is invariant under separate
coordinate permutations in blocks of lengths `r_1,...,r_B`, use the product
of the corresponding h_(r_j); on a shorter block the same formula has
`k=0` and minimum orbit bound one. It remains
a Walsh eigenfunction, has nonzero pairing with q, and every supporting
block orbit has size at least the product of the m_(r_j). Thus some piece
has both supports at least that product. Its bit cost is at least

```math
 2h_*\sum_j r_j-O\left(\sum_j\log(r_j+1)\right).
```

In particular any fixed number of color classes of growing length has
the same leading obstruction. This does not cover symmetry broken into
linearly many short blocks.

## 5. A larger macro-alphabet has a different boundary

There is a useful quantitative extension for choosing the next premise.
Group w binary coordinates into one macro-coordinate, with `D=4^w`
Pauli letters and Walsh matrix H_D. It satisfies `H_D^2=D I` and its
quadratic sign is an eigenvector with eigenvalue `sqrt(D)=2^w`.
For functions symmetric under permutations of R macro-coordinates use

```math
 J_D(z)=\prod_{g=1}^{D}z_g\prod_{g=1}^{D}(H_Dz)_g.
```

It has degree `2D`, obeys `J_D(H_D z)=D^D J_D(z)`, and has nonzero
pairing with the quadratic sign. The same argument, using an additional
eigen-linear factor for the bounded residue of R modulo `2D`, gives the
necessary shared-bit rate per macro-coordinate

```math
 2h_D R-O_w(\log R),\qquad
 h_D=\log_2(2D)-\frac{D+1}{2D}\log_2(D+1).
```

Total input length is `lambda=wR`, so the necessary rho is at least
`h_D/(2w)`. For w=2 this is

```math
 \frac14\left(5-\frac{17}{32}\log_2 17\right)>1/\sqrt2.
```

This close inequality has an exact certificate: `17^100000<2^408747`
bounds the logarithm above by `408747/100000`, and the square of the
resulting rational lower bound for rho is larger than `1/2`.
Thus grouping pairs of binary coordinates and then imposing macro-
permutation symmetry still cannot reach the accepted rate.

For w=3, this particular dual lower bound is **below** `1/sqrt2`:
`log_2 65>6` bounds it above by `253/384`, whose square is below `1/2`.
That is not an improvement theorem. It identifies a changed premise not
closed by this certificate: symmetric three-bit macro-coordinates.
Additional within-macro invariance can reduce their 64 letters to the
three classes zero, nonzero positive quadratic sign, and negative sign.
Their Walsh matrix and multiplicities are, respectively,

```math
 \begin{pmatrix}1&35&28\\1&3&-4\\1&-5&4\end{pmatrix},
 \qquad (1,35,28).
```

The compressed matrix squares to `64I` and sends `(1,1,-1)` to eight
times itself. These claims follow from the character and quadratic Gauss
sums; an actual new family still needs all integer-factor and cost checks.
No such macro-family rate is claimed in this package.

## 6. Exact scope and remaining mechanism

The conclusion concerns pieces M_f of the specified Pauli-diagonal form
with coordinate-permutation-symmetric coefficient functions. Arbitrary
pieces in Anthropic's construction need not have this form. Symmetrizing
an arbitrary nonsymmetric f can enlarge its supports by an exponential
factor, so no without-loss-of-generality symmetry claim is made.

Nonsymmetric coefficient functions, other operator bases, or pieces
outside the simultaneous Pauli/Bell-diagonal algebra remain open. A new
round must change one of those premises rather than search larger values
of r in the unchanged symmetric class. The direct Pauli factorization and
integer coding are reusable, but no improved SAT algorithm is obtained.

The identity and dual are proved here in full; no scientific-priority,
independent-review or formal-verification claim is made. Standard Pauli
and Walsh identities have extensive prior literature, referenced in the
package source notes. New analysis is AI-assisted and Apache-2.0.
