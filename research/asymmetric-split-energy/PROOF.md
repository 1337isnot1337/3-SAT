# Reciprocal-square capacity in an ideal split model

## Model and exact result

At an internal node let the two available continuation algorithms have
positive exponential cost coefficients `e_L,e_R`. A term has normalized
nonnegative directional costs `(x,y)` on the quarter circle
`x²+y²=1`. The algorithm sees the term and chooses one direction for the
whole term; its cost coefficient is `min(e_L x,e_R y)`. The adversary
chooses the term. Define the ideal node coefficient to be the maximum of
this minimum over the whole continuous quarter circle. For a finite binary
tree, compute each internal coefficient recursively by this rule from
positive leaf coefficients. This is an abstract minimax certificate model;
it assumes the two continuation coefficients are already available and
that no other work costs anything.

**Theorem.** The coefficient at a node is

    e = (e_L^(-2) + e_R^(-2))^(-1/2).

Consequently the root coefficient for any finite binary tree is

    e_root = (sum over leaves i of e_i^(-2))^(-1/2).

This is independent of tree shape and leaf ordering. The maximizing
point is uniquely `x=e_R/sqrt(e_L²+e_R²)`,
`y=e_L/sqrt(e_L²+e_R²)`; at it the two weighted costs are equal.

Proof: put `t=min(e_L x,e_R y)`. Then
`1=x²+y² >= t²(e_L^(-2)+e_R^(-2))`, giving the upper bound.
The displayed point is on the circle and attains equality. Taking inverse
squares yields additive capacity; induction over the tree proves the second
formula. Positivity is necessary for the inverses. A full quarter disk gives
the same maximum, and mixtures of circle points lie in that disk.

If each leaf has coefficient `e_0` and there are `N` leaves, the optimum
is `e_0/sqrt(N)` for **every** tree, including completely unbalanced trees.
If a separate hypothetical size bookkeeping assigns each leaf a positive
logarithmic size `b_i` and `log K=sum b_i`, and if leaf coefficients satisfy
`e_i=c/sqrt(b_i)`, the resulting coefficient is `c/sqrt(log K)`.
This last conclusion depends on those explicit size and leaf assumptions;
the split theorem itself says nothing about feasible graph sizes.

## Connection and missing bridge

The pinned Anthropic Appendix B gives directional *upper bounds*, up to
`O(log lambda)` additive bits, of the forms
`C sqrt(2h+s)` and `C sqrt(2h-s)`, with `-2h <= s <= 2h`, and
`C sqrt(h)=lambda+O(log lambda)`. Dividing both by `2 C sqrt(h)`
produces `x²+y²=1`. The symmetric choice `e_L=e_R` gives the maximum
`1/sqrt(2)`. The original paper chooses one direction for an entire term,
not independently per rectangle. Averaging the normalized upper-bound pairs
for all rectangles lies in the disk, and the same minimax upper envelope
applies to those averages. The circle worst case is attained in the continuous
relaxation by taking identical points; discrete shift grids can approximate
it as `h` grows, but this does **not** prove actual ranks attain those bounds.

The paper's construction is a square grid and its available continuation
algorithms have the same size. It does **not** supply the arbitrary unequal
child coefficients assumed above. A rectangle with sides `g_L,g_R` has
additional straight edges, unequal multiplicities and different rebalancing
costs. No formula here proves those costs satisfy this normalized model,
or that its leaves can be combined with `log K` additive. Conversely, a
smaller actual rank envelope or correlated terms may improve the certificate.
The theorem rules out only a better value obtained by reassociating this
ideal minimax recurrence, not a better contraction or a SAT algorithm.

Additive bit overhead, grid enumeration, grouping and local evaluation,
descriptions, bit precision, recovery, dense reductions, and space are absent
from the ideal model. The theorem is not a complete runtime bound. A valid
rectangular algorithm must pay these and establish its own child interfaces.
The accepted OpenAI theorem and selected alpha remain unchanged.
