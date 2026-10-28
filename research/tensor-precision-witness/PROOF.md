# Interpolating the tapered witness with Cauchy packets

Work over `Z_(2)` and its fraction field. Let `L=2^a`, `a>=1`, and
`S={-L,...,L-1}`. Write `C(T)=product_(t in S)(T-t)`, `C0=C'(0)`, and
`W_d(T)=C(T)/(C0(T-d))` for `d=-L+1,...,L-1`, as in the accepted source.
Each `d` is a difference of two slots in a full packet. The omitted grid
point `-L` is not a slot difference, so all `W_d(-L)=0`. For `d,e` in `S`
with `d != -L`,

```
W_d(e) = 0 if e != d, and W_d(d) = C'(d)/C'(0).
```

The complete residue grid modulo `2L` gives `v2(C'(d))=v2(C'(0))`;
therefore `W_d(d)` is a unit of `Z_(2)`.

For `0<=j<a`, define the polynomial

```
P_j(T) = product over nonzero t in S with v2(t)<=j of (T-t)/(-t).
```

Its degree is `2L-L/2^j < 2L` and `P_j(0)=1`. It has integral values at
every grid node: a root gives zero, and at any nonroot `t`, either `t=0`
or `v2(t)>j`, so every factor has valuation zero. Its coefficients need
not be in `Z_(2)[T]`; only its grid values are used here. Let

```
c_* = P_j(-L),
c_d = (P_j(d)-c_*) / W_d(d).
```

All `c_*` and `c_d` lie in `Z_(2)`. Both sides of

```
P_j(T) = c_* + sum_d c_d W_d(T)                         (1)
```

have degree at most `2L-1` and agree at all `2L` points of `S`, proving (1).
The rational coefficients have polynomial bit length in `L`: they consist
of products and ratios of `O(L)` integers of size `O(L)`. Their residues
modulo `2^p` can be calculated in polynomial time in `L,p` by inverting odd
integers modulo `2^p`.

Use two full packets. In the first fix the column bits to zero except for
`X_(L-1)=1`; its rows `x=0,...,L-1` produce shifts `d=L-1-x`.
In the second fix all column bits to zero except `X_0=1`; its rows
`x=1,...,L-1` produce the negative shifts `d=-x`. Mark these `2L-1`
rows, and on them use the single tensor

```
A(Y) = c_* + sum_d c_d Y_(x_d).
```

The one unmarked row is unrestricted, represented by a unary `(1,1)` tensor;
column bits are fixed by unary `(1,0)` or `(0,1)` tensors. In the source's
multilinear affine deformation, summing row bits replaces each marked
`Y_(x_d)` in `A` by `(WX)_(x_d)=W_d(T)`. The unmarked row sum is one.
Equation (1) proves that the deformed contraction is exactly `P_j(T)`.
Tensor entry evaluation is a sum of `2L-1` stored coefficients.

For `1<=u<=a`, the predecessor's generic witness with multiplicity parameter
`h>=1` is exactly

```
H(T) = product_(j=0,...,u-1) P_j(T)^h.                  (2)
```

Indeed a nonzero node of valuation `i` occurs once for each `j>=i`, giving
multiplicity `h max(0,u-i)`. Independent copies multiply contractions. Thus
(2) is realized with `M=2huL` real ports, one degree-`2L-1` row tensor per
factor copy, and all remaining tensors unary. There are no hidden sums in
the entry oracle beyond polynomially many operations; denominators are odd.
The construction does not show that this prescribed packetization satisfies
all balance conditions of the source's packing lemma or that a corresponding
Boolean network exists.

For a retained node of valuation `i<u`, the predecessor's exact content
formula and bounds give `Theta(hL/2^i)`. With `M=2huL`, this becomes
`Theta(M/(u 2^i))`, a factor `L` below the generic witness's
`Theta(ML/(u 2^i))` scale when its multiplicity is chosen from this same
actual port budget. The relevant constants are uniform under the stated
parameter restrictions. Neither observation is a lower bound on tensor-aware
algorithms that inspect these simple tensors. No reduction, recursion, entry,
leaf or SAT cost is claimed to improve.

For the integer-entry observation, at `T=-L` every `W_d` is zero, so the
contraction is `A(0) sum_X B(X)`, an integer when all tensor entries are
integers. At `L=4`, `u=h=1`, multiplication over odd roots gives
`H(-4)=35/3`. This excludes literal equality in that narrower class, while
multiplication by 3 removes this specific obstruction and leaves the origin
odd.
