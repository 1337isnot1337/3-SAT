# Registered full charge-coefficient scalar filter screen

Base: `630041c9da3a26edb8c8f59d5f8a4132a188c8bd` (PR 19 merge).
The preceding actual asymmetric crossing omits s=0 but keeps rho=1/sqrt(2).
Use its fixed nonprincipal row/column labels and output labels; preserve
the predecessor unchanged and pin its model. All other guidance and the
selected alpha=1/2 stay unchanged. User goal ACTIVE, INCOMPLETE: work
indefinitely, commit/push often. Owner has authorized merges. No subagents.

Changed premise: include EVERY coefficient of the charge polynomial, not
only one fixed charge or a few moment weights. For these fixed codebooks,
raw Q_s^q has degree at most D=max length(mu_row)+max length(nu_col).
Its coefficients span exactly the span of Q_s^q over all rational charge
values, by interpolation at D+1 distinct points. Thus the finite screen
covers every linear combination of charge values on those codebooks.

Register lambda=1,2, at the predecessor's grades h=4,6. Build all exact
charge-coefficient tensors for s=-2h,...,2h by polynomial normal-order
recurrence, with degree bounds and evaluations against pinned operators.
For each T in the distinct sorted list

    0, 1, floor(h/2)-1, h-1, 2h-1

allow only shifts with |s|>T. Solve the COMPLETE scalar-output constraints:
all off-diagonal y,u blocks vanish and every diagonal output block agrees.
Compute the induced label-matrix space on x,v. Its dimension is at most
N squared. Test its determinant polynomial exactly (N<=4), not merely a
few random combinations. A nonzero polynomial gives a deterministic grid
witness, exact full-rank label matrix and local normalization. A zero
polynomial certifies absence of a full-rank scalar pairing for that finite
codebook, charge span and interval. It is not an all-size obstruction.

Success is a genuine finite filtered crossing with exact scalarity, label
rank, missing interval and both directional rank costs accounted for; then
seek an ALL-SIZE identity before any alpha claim. The asymptotic target
requires epsilon=T/h bounded away from zero and leading label/output
capacity, not only a finite successful minor. Stop unchanged small-grid
extensions after the registered screen; a fresh experiment needs a new
structural premise.

Uniformity caution: exact symbolic determinant classification is cheap at
N<=4, but is not asserted to take `2^O(lambda)` for general N. A future
uniform selector needs an explicit identity or a paid randomized matrix-
space test. Generic rational normalization is already paid by PR 17;
existence/scalarity and the full rank curve remain the central obligations.

Credit: PRs 11,17,19; Anthropic Appendix B; the earlier uncharged
operator-moment-recovery branch (commit
`8191d2e2813615e4941216c012b151c96c5d7ce5`) supplies the scalar-output
constraint pattern. This experiment changes charge span and codebooks.
All work is substantially Codex-assisted and has no independent review.
