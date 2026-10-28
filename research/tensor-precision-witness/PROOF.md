# Interpolating the u=1 witness with Cauchy packets

Work over `Z_(2)` and its fraction field. Write
`C(T)=product_(t in S)(T-t)` and `C0=C'(0)` as in the accepted source, and
`W_d(T)=C(T)/(C0(T-d))` for `d=-L+1,...,L-1`. Each `d` is the difference
between two slots in a full packet. The omitted grid point `-L` cannot be a
slot difference, so all `W_d(-L)=0`. At the other grid points,

```
W_d(e) = 0 if e != d, and W_d(d) = C'(d)/C'(0).
```

The complete residue grid modulo `2L` gives `v2(C'(d))=v2(C'(0))`;
therefore `W_d(d)` is a unit of `Z_(2)`.

Let `H_1` be the polynomial defined in the README. It has degree `L` and
is in `Z_(2)[T]` because all its root denominators are odd. Set

```
c_* = H_1(-L),
c_d = (H_1(d)-c_*) / W_d(d).
```

All coefficients `c_*` and `c_d` are in `Z_(2)`. Both sides of

```
H_1(T) = c_* + sum_d c_d W_d(T)                         (1)
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
multilinear affine deformation, summing the row bits replaces every marked
`Y_(x_d)` in `A` by `(WX)_(x_d)=W_d(T)`. The unmarked row sum is one.
Equation (1) proves that the deformed contraction is exactly `H_1(T)`.
Tensor entry evaluation is a sum of `2L-1` stored coefficients. Repeating
independently `h` times multiplies the contractions to `H_1(T)^h`.

This network has `M=2hL` real ports and maximum tensor degree `2L-1`.
There are no hidden sums in the entry oracle beyond polynomially many
operations; the denominators are odd. This construction does not show that
its packetization satisfies all balance conditions of the source's packing
lemma or that the corresponding Boolean network exists.

For an odd grid node, the predecessor's exact content formula gives
`v2(content H_1(t+2Lz)^h) = h(a+1+L sum_(j=1)^a j/2^j) = Theta(hL)`.
Since `M=2hL`, this is `Theta(M)`, not the generic witness's
`Theta(ML)` scale at `u=1`. Full jets through degree below `h` also vanish.
Neither observation is a lower bound on tensor-aware algorithms that can
inspect these particularly simple tensors. No reduction, recursion, entry,
leaf or SAT cost is claimed to improve.

For the integer-entry observation, at `T=-L` every `W_d` is zero, so the
contraction is `A(0) sum_X B(X)`, an integer when all tensor entries are
integers. At `L=4`, multiplication over odd roots gives `H_1(-4)=35/3`.
This excludes literal equality in that narrower class, while multiplication
by 3 removes this specific obstruction and leaves the origin odd.
