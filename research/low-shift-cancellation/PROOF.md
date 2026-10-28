# Cancelling extremal shifts with two output partitions

This argument is author-checked, AI-assisted, and not independently reviewed.
We use the pinned Anthropic Appendix-B operators, in the notation and with
the hypotheses of [PR #59](../scalar-relation-witness/PROOF.md). The
accepted OpenAI theorem remains a separate premise. All partitions in this
note belong to the full weight-h partition space.

## Statement

For every h>=2, the shift span of the full uncharged crossing-piece family
has rank at least

```
2h + max(0, floor((h-3)/2)).
```

This strengthens the `2h+max(0,floor((floor((2h-3)/3)-1)/2))`
full-space lower bound in PR #59. Both bounds remain below its 4h upper
bound. The new witnesses use y=(h), which can be absent from the source's
lexicographic binary codebook; no stronger binary-codebook bound, SAT
algorithm, or time improvement is asserted.

## Two Laurent polynomials with the same endpoint

Write e=(1^h). For every odd ell with `3<=ell<=h-2`, put

```
r=(ell+1)/2,   m=h-ell,
u=(m+1,1^(ell-1)),   v=(m,2,1^(ell-2)).
```

Both u and v have ell parts; m>=2, so they are distinct partitions and
neither equals (h). Let P_u and P_v be the Laurent polynomials of the
actual piece entries with labels x=v=e, input y=(h), and outputs u and v,
respectively. In this section the symbol v in the displayed partition is
an output state; it is not the piece's fixed v=e label. Both polynomials
are symmetric by PR #59 and have positive support at most h+1: the first
operator has h fields but can annihilate at most the single input part.

Let m_j(w) be the multiplicity of j in a partition w. Normal ordering
shows that the first nonzero coefficient in the expansion of P_w about
z=1 has order 2r=ell+1 and value

```
alpha_w = binom(h,r)^2 (h-r)! (2r)! h / product_j m_j(w)! > 0.  (1)
```

Indeed the single input part must be annihilated and ell output parts
created, using exactly 2r uncontracted fields. Choose r fields on each
side in `binom(h,r)^2` ways, pair the other h-r fields, and arrange one
annihilation and ell creations. There are no other normal-ordered terms
acting nontrivially between these states with a different number of
uncontracted fields.

Let beta_w be the coefficient of z^(h+1). At that endpoint the first
operator annihilates the h-part and creates h-1 ones, producing
`h^2 t_1^(h-1)`. Only i=0 contributes. The second operator uses
h-r annihilations and r creations; after annihilation r-1 ones survive.
Thus

```
beta_w = h^2 binom(h,r) (h-1)!/(r-1)! * r!
         / [(m_1(w)-r+1)! product_{j>1} m_j(w)!].                (2)
```

The denominator is defined for u and v: their numbers of ones are
2r-2 and 2r-3, each at least r-1. Equations (1) and (2) show that
`beta_w/alpha_w` is a common positive factor times the falling factorial
`(m_1(w))_(r-1)`. Consequently

```
beta_u/alpha_u = 2 beta_v/alpha_v.                              (3)
```

This includes m=2, when v has two parts of size two: the multiplicity
factor occurs in both (1) and (2) and cancels.

Define `W_ell=alpha_v P_u - 2 alpha_u P_v`. Equation (3) cancels its
positive endpoint; symmetry cancels the negative endpoint. Therefore W_ell
is supported in [-h,h]. Its first nonzero coefficient at z=1 has order
ell+1 and equals `-alpha_u alpha_v`, so W_ell is nonzero. Distinct ell
have distinct first nonzero orders and give independent W_ell.

## Independence from the predecessor witnesses

PR #59 constructs h symmetric rows F_l with nonzero endpoints at +/-(h+l),
h-1 nonsymmetric rows G_l with positive support <=h+l and a nonzero
negative endpoint at -(h+l+1), and a diagonal row H separated from all
F_l and G_l by the even moment functional
`L(P)=sum_s (s^2-4h^2)[z^s]P`. The all-ones label slice satisfies L=0,
so every W_ell is also annihilated by L.

In any relation among the predecessor rows and W_ell, L first forces the
coefficient of H to zero. At shift +2h only F_h remains among the other
rows, so its coefficient is zero; then shift -2h isolates G_(h-1).
Proceeding downward through h+2 successively eliminates F_l and G_(l-1);
shift h+1 finally eliminates F_1. Every W_ell is supported in [-h,h].
Their distinct nonzero orders at z=1 then force all their coefficients to
zero. There are `max(0,floor((h-3)/2))` admissible odd ell, proving the
stated rank bound. The weaker PR #59 low-support rows are not added again.

## Limits

The proof invokes the predecessor's all-size identities and source normal
ordering; neither has independent review here. The finite check is not an
all-size proof. The lexicographic codebook, crossing ranks, factor sizes,
recursive schedule, outer reductions, precision and recovery would all
need separate treatment for an algorithmic consequence.
