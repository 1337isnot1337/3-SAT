# Second-moment spectrum and quadratic crossing filter

Status: `scoped_checked`. The all-size algebra and uniform construction are
author-checked and substantially AI-assisted; independent review is still
required. The component piece count improves from `4h+1` to `4h-1`, but the
leading `rho=1/sqrt(2)` envelope, SAT alpha and selected result are unchanged.

Task: `contraction-schedule`. Canonical base:
`630041c9da3a26edb8c8f59d5f8a4132a188c8bd`.
Contributor: 1337isnot1337, with substantial AI assistance from Kimi.

## Question and result

PR 11 derived a charged first moment. PR 19 normalized an asymmetric minor to
omit `s=0` and left higher moments and wider filters open. This package derives
the **uncharged second moment** and uses its exact spectrum to omit two shifts.

[PROOF.md](PROOF.md) defines `A=exp(L)`,
`F=sum_(r>=1)(-1)^(r-1)r u_r`, and

```math
 U_h=\frac1{2h}F(FA+2A\partial_{u_1}).
```

On every output energy space,

```math
 \sum_s s^2Q_s(a_\mu,b_\nu)
 =4hE\,h!\,\frac{m_\mu!}{m_\nu!}[u^\mu]U_h(u^\nu)\operatorname{Id}.
```

The all-size spectral theorem gives

```math
 U_h(U_h-1)(U_h+(h-2)/h)=0,
 \qquad \operatorname{rank}U_h=p(h)-p(h-2).
```

The image is `ker L^2`; the nonzero eigenvalue multiplicities are
`p(h)-p(h-1)` and `p(h-1)-p(h-2)`. In particular the full common-label pairing
is singular for every `h>=2`, but its nonzero spectrum is explicit.

## Actual quadratic filter

At output energy `h`, normalize the zeroth and second moments by `h!`. Then

```math
 \sum_s C_s=I,\qquad \sum_s s^2C_s=4h^2U_h.
```

The normalizer `I-4h^2U_h` has an explicit rational inverse using only `U_h`
and `U_h^2`. Multiplying by `1-s^2` and that inverse constructs actual rational
crossing pieces for every shift except `+1` and `-1`.

Both directional flattening ranks are preserved by local invertible transforms.
The construction uses `4h-1` pieces, two fewer than the source and one fewer
than PR 19. Uniform generation and coefficient heights fit the predecessor's
`2^O(lambda)` rational-entry contract. The central and nearby shifts remain, so
this is a scoped component improvement, not a smaller rho or SAT time bound.

## Complete cost

The label count is `2^O(lambda)` with `h=Theta(lambda^2)`. Explicit spectral
inversion avoids generic adjugate heights. PR 17's bounded prime-field transfer
pays rational normalization and exact signed recovery while retaining every
reduction, query, entry and recursive cost. Its exponential space and one-sided
decision error remain explicit. No full SAT algorithm is implemented.

## Evidence and reproduction

From the repository root, offline with Python 3.11+ and only the standard
library:

```sh
python3 -I -B research/operator-second-moment/verify.py
make verify
```

The checker covers 594 independent operator-moment entries, 1,386 spectral
identity inputs, 41,073 integrality entries, twelve explicit inverse controls,
723 actual crossing sums and eight directional rank comparisons.
[verification.json](verification.json) records exact scopes and hashes. Finite
checks do not independently review the all-size proof or full transfer.

## Sources and next question

[SOURCES.json](SOURCES.json) pins the external paper and predecessors. The next
substantive target is a paid family of higher moments or another mechanism that
removes a whole central interval while retaining leading capacity and both rank
bounds. Repeating isolated-shift deletions does not improve the leading rho.
