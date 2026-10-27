# Three-bit macro-coordinate crossing construction

Status: `scoped_checked`. The uniform algebraic construction is written
below; both coarse and refined rates are obstructed. No improved
eventual rate or SAT algorithm is claimed.

## 1. A closed weighted three-class Walsh space

One macro has three-bit labels a,b and 64 total Pauli labels. Let class zero
contain only `(a,b)=(0,0)`, class plus contain nonzero labels with even
`a dot b`, and class minus contain labels with odd `a dot b`. Their sizes
are `w=(1,35,28)`. The symplectic Walsh transform on class-constant functions is

```math
 C=\begin{pmatrix}1&35&28\\1&3&-4\\1&-5&4\end{pmatrix}.
```

For a nonzero output label h of quadratic sign epsilon, the full character
sum is zero and the quadratic Gauss sum is `8 epsilon`. Splitting the two
sign classes and removing the zero label gives `4 epsilon-1` and
`-4 epsilon`, proving the rows. The zero output gives the class sizes.
In particular `C^2=64I`, `C(1,1,-1)^T=8(1,1,-1)^T`, and
`diag(w) C=C^T diag(w)`.

For R macros let a type alpha have three nonnegative counts adding to R.
Its number of actual Pauli words is

```math
 m_\alpha=\frac{R!}{\alpha_0!\alpha_+!\alpha_-!}
                         35^{\alpha_+}28^{\alpha_-}.
```

The compressed transform is

```math
 T_{\beta,\alpha}=[z^\alpha]\prod_{j=0}^2
                              \left(\sum_{k=0}^2 C_{jk}z_k\right)^{\beta_j}.
```

It satisfies `T^2=64^R I` and `T q=8^R q` for
`q_alpha=(-1)^alpha_-`. It is self-adjoint with respect to the weighted
type inner product: `diag(m)T=T^T diag(m)`. Counting types instead of
their word multiplicities would give incorrect flattening ranks.

## 2. Actual uniform pieces and the missing rate

Order types by increasing m_alpha and lexicographic ties. Apply the exact
two-flag adapted-basis construction of the predecessor, then decompose q
in that basis. This gives actual functions f_i whose sum is q, together
with their exact transforms. Both word supports are computed with m_alpha.
The predecessor's Pauli/Bell identities give the two exact flattening ranks
and both factorizations on input strings of length lambda=3R.

Clearing a common denominator D and multiplying by `D 2^(2 lambda)` gives
integer factors. There are at most `(R+2 choose 2)` pieces. Matrix entries
have `O(R)` bits and its dimension is `O(R^2)`, so rational elimination and
denominator clearing have polynomial bit complexity. Given a Pauli label,
its macro type and function value are computed in polynomial time. Actual
support words can be indexed by first unranking the macro class sequence
and then the choices within its 35/28-element local classes. Invalid codes
give zero. Uniform `2^O(lambda)` entry evaluation therefore remains feasible.

Padding an arbitrary lambda to `3 ceil(lambda/3)` and restricting to padded
strings preserves the crossing identity and adds only O(1) to a linear
shared-bit bound. None of this proves a smaller rho. The missing result is
an eventual total support-bit bound below `6 sqrt(2) R+O(log R)` for the
same realizable pieces, followed by the full master and dense-reduction
composition. Finite low-order data cannot replace that proof.

This family changes the symmetry premise: it is not invariant under all
permutations of the 3R individual binary-coordinate pairs. The predecessor
dual does not exclude it. Its own general 64-letter macro lower bound is
below the target and hence provides no improvement theorem either.

## 3. Six-class refinement

Replace the three classes by the six trace-product classes in
[SCHEME-REFINEMENT.md](SCHEME-REFINEMENT.md), with weights
`(1,7,7,7,21,21)`. Replace C by its explicit six-by-six table and use six
counts in each type. Every formula above remains valid with the new weights
and target signs `(1,1,1,-1,1,-1)`. The dimension is `(R+5 choose 5)` and
matrix entries still have O(R) bits, so construction, heights, piece count
and support unranking remain polynomial. The direct checker verifies actual
integer factors, ranks and codes rather than only this formal substitution.

The local and four-block duals respectively close the coarse and refined
families. See [the block proof](BLOCK-BARRIER.md) for the new all-size result.
The missing-rate discussion above records the original target, not an open
conjecture within these now-obstructed families.

All reasoning is AI-assisted, author-checked and not independently reviewed.
The source pins and accepted-baseline boundaries are in [README.md](README.md).
