# A two-scale packet grid

Status: scoped finite checks passed; written component argument is AI assisted
and not independently reviewed. No full contraction or SAT bound is established.

## 1. A small grid with an arbitrarily large valuation gap

Let `d=2^r`, `H=2^t` with `r,t>=1`, and let `b>=r+2`, `B=2^b`.
Use the `L=dH` distinct port positions

```math
 X=\{x+By:0\le x<d,\ 0\le y<H\}.
```

Use the interpolation grid

```math
 S=\{a+Bc:-d\le a<d,\ -H\le c<H\},\qquad |S|=4L.
```

Since `B>2d`, these representations are unique and `X-X` is contained in
`S`. Write `C(T)=prod_(s in S)(T-s)`. All derivatives at the grid nodes
have the same two-adic valuation

```math
 v_2(C'(s))=2H\gamma_r+(2H-1)b+\gamma_t,
 \qquad \gamma_r=v_2((2d-1)!),\quad\gamma_t=v_2((2H-1)!).
 \tag{1}
```

Indeed, if two nodes have different low coordinates, their difference
has the valuation of the low-coordinate difference, at most `r`; the
high difference is divisible by `2^b`. Each other low coordinate has
`2H` high-coordinate choices. For equal low coordinates and unequal high
coordinates, the valuation is `b+v_2(c-c')`. Each low and high grid is a
complete residue interval of power-of-two size, so its derivative valuation
is independent of the selected coordinate. This proves (1).

Put `alpha=2^(b+t+1)`. Every nonzero difference of grid nodes has valuation
at most `b+t`, strictly less than that of `alpha`. Define the deformed
packet matrix as in the accepted source, but at the new positions:

```math
 W_{xy}(T)=\frac{C(T)}{C'(0)(T-(y-x))}\qquad (x,y\in X).
 \tag{2}
```

Its entries are rational polynomials of degree `4L-1`. One has `W(0)=I`.
At a grid point `s`, only pairs with `y-x=s` survive, all with the common
unit scalar `C'(s)/C'(0)`. For every `s in S` and `q=y-x`, the complete
polynomial `W_xy(s+alpha z)` is integral over `Z_(2)`. Its content is
zero when `q=s`; otherwise it is exactly

```math
 b+t+1-v_2(s-q)\ge1.
 \tag{3}
```

To see this, factor the known powers of two from every linear factor in
the numerator. Formula (1) cancels the derivative's valuation. Omitting
the factor indexed by `q` either removes the root factor `alpha z`,
leaving an odd constant, or removes a factor of valuation `v_2(s-q)`.
In the latter case the first nonzero coefficient is linear and has the
valuation in (3). The argument is coefficientwise and extends to the
source's unramified valuation ring as well.

Thus a numerical valuation range much larger than `log L` is possible
with only `O(L)` interpolation nodes and unchanged packet slot count.
This by itself does **not** produce more useful taper levels or a better
precision bound.

## 2. Exact local Cauchy spectrum

In their natural order write `x_j=(j mod d)+B floor(j/d)`, `0<=j<L`.
For any odd unit `c`, consider the normalized block

```math
 G_{ij}=\frac1{c+2(x_i-x_j)}.
```

The Smith valuations are exactly

```math
 e_j=2j+2v_2(j!)+2(b-r)\lfloor j/d\rfloor
    =4j-2\operatorname{popcount}(j)+2(b-r)\lfloor j/d\rfloor,
 \qquad 0\le j<L.                                      \tag{4}
```

For distinct indices `i,j`,

```math
 v_2(x_i-x_j)=v_2(i-j)+(b-r)[d\mid i-j].                 \tag{5}
```

If their low coordinates differ, the valuation is below `r` and unchanged;
otherwise remove their common factor `d` in index space and `B` in port
space to obtain the extra `b-r`.

For a `k`-element index set, the first term in its Vandermonde valuation
is at least `sum_(j<k) v_2(j!)`: the integer binomial-evaluation determinant
proves this standard divisibility. The second term in (5) counts pairs
in the same residue class modulo `d`. This is minimized by balancing the
class sizes; its minimum is `sum_(j<k) floor(j/d)`. Consecutive index sets
attain both minima simultaneously, so the minimum is their sum.

The Cauchy determinant identity and the unit denominators now give the
minimum valuation of a `k`-minor as

```math
 k(k-1)+2\sum_{j<k}v_2(j!)+2(b-r)\sum_{j<k}\lfloor j/d\rfloor.
```

Successive differences of these determinantal divisors prove (4). It
holds over the unramified extension too, since the same minors attain
the bound and all denominators remain units. For fixed `d` a growing
gap increases the asymptotic slope. If `j<d`, it gives no improvement.
This is a changed coordinate family, outside the fixed-interval spectrum
of the earlier package; no basis change on the original block is claimed
to alter its invariant factors.

## 3. Algorithmic obligations still open

The old combinatorial packing can use the binary digits of the low and
high coordinates in place of contiguous index bits. At a surviving
nonzero difference with nonzero low coordinate, its lowest set bit flips
the corresponding low-coordinate bit; if the low difference is zero,
the lowest high-coordinate bit flips. Hence the familiar localization
argument has a candidate coordinate assignment. Grid nodes with low
coordinate `-d` or high coordinate `-H` have no real matching pairs and
give the zero packet matrix. Their jets are not automatically local.

Every integer in (2) has bit length polynomial in `L,b,t`; a common
denominator has at most `O(L(b+t+r))` bits. Product evaluation, extraction
of known powers of two, and odd-unit inversion therefore have polynomial
bit cost at specified polynomial precision. Taking `b` to be a fixed
power of `log s` does not itself violate a polynomial description budget.

The missing step is a **joint** recovery and mode decomposition at these
same parameters. The source's complete-grid taper formula cannot simply
replace its `u` by the numerical gap `b`. There are no interpolation nodes
at most of those intermediate valuations. The larger spectrum (4) must
also be shown for the actual crossing tiles, with controlled multiplicity
and efficiently computable source/target factors. Jets at dummy nodes,
all child sizes, inherited precision, leaves and outer reductions must be
charged. The accepted contraction theorem does not automatically apply
to this changed deformation.

The present component alone establishes neither a better contraction
envelope nor an increase from alpha `1/2`. A proof that the extra gap
cancels between mode divisibility and recovery precision would close this
particular attempt; otherwise the complete schedule is the next target.

## Credit

The accepted OpenAI source, exact labels and predecessor packages are pinned
in [README.md](README.md). The derivative and shifted-integrality proof
generalizes its regular-grid argument. The local minor argument follows
the earlier Cauchy-spectrum proof with the additional residue-pair term.
No priority or independent review is claimed.
