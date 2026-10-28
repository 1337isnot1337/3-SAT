# A sharp characteristic separation for independence cut rank

Status: `scoped_checked` for finite controls; the all-size argument is
author-checked and awaits independent review. No SAT bound is claimed.
Task `decision-only`; base `1dfac844cbb1e570c99579ecf48c1007d72da7c9`.
Contributor: Cinna Davis, with substantial OpenAI Codex assistance. Apache-2.0.

[PROOF.md](PROOF.md) proves that for two copies of all nonzero vectors of
`F2^b` split one per side, the binary independence table has rank exactly
`N_b`, the number of subspaces, over Q and every odd-characteristic field,
but rank exactly `2^b` over characteristic two. Here
`N_b=Theta(2^floor(b²/4))`. On the same example with `m=2(2^b-1)`
columns, the characteristic-two rank is `m/2+1` while the rational and odd
field ranks are `2^((log2(m/2+1))²/4+O(1))`. A general cut of intersection
dimension b has rank at most `N_b` over any field.

More generally, for matrices represented over `F_q` with `q=p^r`, the full
projective configuration has rank `1+(q^b-1)/(q-1)` when the coefficient
field has characteristic p, and rank `N_(q,b)` otherwise. The same values
are universal upper bounds in their respective cases. For fixed q, `N_(q,b)=Theta_q(q^floor(b²/4))`. This is an algebraic
extension, not a nonbinary SAT construction.

The proof takes one basis for each subspace and factors the resulting
subspace-disjointness minor as `Z diag(mu) Z^T`. Its integer Möbius
coefficients are nonzero in odd characteristic and vanish in characteristic
two except in dimensions zero and one. This establishes that the
subspace-indexed upper envelope in PR #37 is worst-case sharp over Q and odd
characteristic; the characteristic-two cancellation from PR #104 is a real
field-specific compression. The claim is for a specified cut and does not
imply a SAT lower bound or an all-order separation.

## Reproduction

```sh
python3 -I -B research/independence-field-separation/verify.py
make verify
```

The checker enumerates all binary subspaces through dimension four, checks
every entry of the integer factorization and calculates the matrix ranks
over F2, F3 and F5. It also constructs the full independent-set tables
through dimension three and checks their ranks over those fields. Additional
checks cover subspace lattices over F3 through dimension three and F4 through
dimension two, with coefficient fields F2, F3 and F5; the complete
projective independence tables are also checked through dimension two.
A paired-basis F3 control shows the universal upper bound need not be
achieved by every matrix. The [hash-bound output](verification.json) records exact
counts. Finite checks do not constitute independent review of the proof.

## Credit and limits

The original frontier state is PR #37, the cut-rank lower bound is PR #74,
and the characteristic-two exact rank and amplitude chain are PR #104.
The source theorem is owner-accepted and pinned in
[SOURCES.json](../../SOURCES.json). Gaussian binomial identities, subspace
Möbius inversion, and matrix-rank bounds are standard; no priority is claimed.
No new 3-SAT bound, general network lower bound, or faster algorithm follows.
