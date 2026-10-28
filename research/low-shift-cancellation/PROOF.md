# Three-partition low-shift space

This argument is author-checked, AI-assisted, and not independently reviewed.
We use the pinned Anthropic Appendix-B operators, in the notation and with
the hypotheses of [PR #59](../scalar-relation-witness/PROOF.md). The
accepted OpenAI theorem remains a separate premise. All partitions in this
note belong to the full weight-h partition space.

## Statement

For every h>=2, the shift span of the full uncharged crossing-piece family
has rank at least

```
2h + max(0,h-4).
```

For h>=4 this is 3h-4, strengthening PR #59's lower bound of roughly 7h/3.
Both remain below its 4h upper bound. The new witnesses use y=(h), which
can be absent from the source's lexicographic binary codebook; no stronger
binary-codebook bound, SAT algorithm, or time improvement is asserted.

## The three-partition formula

Fix h>=4, labels x=v=e=(1^h), and input y=(h). For each three-part
partition u of h, write m_j(u) for the multiplicity of j and P_u(z) for
the corresponding Laurent polynomial `sum_s [t^u]Q_s t_h z^s`.
Normal ordering gives

```
P_u(z) = C_h / product_j m_j(u)! * (z-1)^4 z^(-h-2)
         * sum_{j=1}^{h-2} m_j(u) (z^j + z^(2h-j)),
C_h = 4h binom(h,2)^2 (h-2)! > 0.                             (1)
```

Indeed t_h permits exactly one annihilation and u requires three
creations, so there are precisely four uncontracted t_1 fields: two from
each copy. The remaining h-2 fields pair in `(h-2)!` ways, and the two
uncontracted fields are chosen on each side in `binom(h,2)^2` ways.
If the annihilation occurs at z, one creation is at z and two are at 1;
if it occurs at 1, two creations are at z and one is at 1. Summing over
the distinguished part j gives the two monomials in (1). The coefficient
4h counts the annihilation, its two possible positions, and the order of
the two creation slots. Equal parts contribute their displayed factorial.

The expression is symmetric under z -> 1/z. Its coefficient at z^(h+1)
is `C_h m_1(u)/product m_j(u)!`, and by symmetry the negative endpoint
is the same; no shift outside `[-h-1,h+1]` occurs. Each j has unique
monomials z^j and z^(2h-j), because `1<=j<=h-2`. Thus multiplication by
the common nonzero Laurent polynomial in (1) embeds the rational vector
space spanned by the multiplicity vectors `(m_1,...,m_{h-2})` into the
space spanned by the piece entries.

## Dimension of the multiplicity-vector span

The span of the three-partition multiplicity vectors over Q has dimension
h-3. To prove this, let `(c_1,...,c_{h-2})` annihilate every such vector.
For each `1<=i<=h-2`, the partition `(i,1,h-i-1)` gives

```
c_i + c_1 + c_{h-i-1}=0.
```

For each `1<=i<=h-3`, the partition `(i,2,h-i-2)` gives
`c_i+c_2+c_{h-i-2}=0`. Subtracting, the successive differences
`c_j-c_(j-1)` are all equal for 2<=j<=h-2. Hence `c_j=A+Bj`.
The three-partition equations reduce to `3A+Bh=0`, which defines a
one-dimensional annihilator. Conversely every such affine vector does
annihilate every three-part partition. The span dimension is therefore
`(h-2)-1=h-3`.

The coordinate functional m_1 is nonzero on this span, for example on
`(h-2,1,1)`. Its kernel has dimension h-4. By (1), that kernel corresponds
to an h-4-dimensional space of genuine rational combinations of piece
entries supported entirely in `[-h,h]`: m_1=0 cancels both endpoint
coefficients. Multiplicity-vector embedding ensures no nonzero vector in
this kernel maps to the zero Laurent polynomial.

## Independence from the predecessor witnesses

PR #59 constructs h symmetric rows F_l with nonzero endpoints at +/-(h+l),
h-1 nonsymmetric rows G_l with positive support <=h+l and a nonzero
negative endpoint at -(h+l+1), and a diagonal row H separated from all
F_l and G_l by the even moment functional
`L(P)=sum_s (s^2-4h^2)[z^s]P`. Its all-ones label slice satisfies L=0,
so every row in the low-support space above is also annihilated by L.

In a relation between that space and the predecessor rows, L first forces
the coefficient of H to zero. At shift +2h only F_h remains among the
other rows, so its coefficient is zero; then shift -2h isolates G_(h-1).
Proceeding downward through h+2 successively eliminates F_l and G_(l-1);
shift h+1 finally eliminates F_1. The low-support space has no terms at
those shifts, so it meets the predecessor span only at zero. Its h-4
additional independent directions give rank at least 3h-4 for h>=4.
For h=2,3 the predecessor's 2h bound applies. The previous PR's
low-support witnesses are not counted again.

## Limits

The proof invokes the predecessor's all-size identities and source normal
ordering; neither has independent review here. The finite check is not an
all-size proof. The lexicographic codebook, crossing ranks, factor sizes,
recursive schedule, outer reductions, precision and recovery would all
need separate treatment for an algorithmic consequence.
