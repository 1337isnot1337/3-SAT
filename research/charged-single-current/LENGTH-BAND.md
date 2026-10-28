# Operator moments are banded by input partition length

This all-grade component argument is author-checked and awaits independent
or formal review. It uses the same charged normal-ordering expansion as
[PROOF.md](PROOF.md); no SAT bound follows.

Let mu,nu be partitions of the same weight h, with lengths ell and k.
For every integer charge q, output energy E>=0, and nonnegative d with
`d<abs(ell-k)`,

```math
 \sum_s s^d Q_s^{(q)}(a^\mu,b^\nu)=0
 \quad\text{as an operator on }V_E.                    \tag{1}
```

At d=0 interpret `s^0=1`, including s=0. Thus for any polynomial f of
degree at most d the weighted operator vanishes whenever
`abs(ell-k)>d`. The result applies before any output compression.

## Proof

Each encoded first-side factor indexed by a part r is a linear combination
of single positive-weight fields t_j, j>=1. Consequently every homogeneous
component of a^mu has exactly ell fields. The b^nu monomial has exactly k
fields. In the source's charged normal-ordering expansion, a contraction
pairs one first-side field with one second-side field. After any matching,
at least `abs(ell-k)` fields remain uncontracted. Each has positive weight,
so the total weight r of the uncontracted fields is at least that number.

The source's common Laurent polynomial carries `(w1-w2)^r` for that term;
the charged zero mode adds only regular coefficients and does not change
r. Its remaining normal-ordered matrix coefficient is regular at
w1=w2=1. Hence F(1+z,1) is divisible by `z^abs(ell-k)`, term by term,
including for an inhomogeneous dual label. Its first d ordinary derivatives
and its value all vanish when d is smaller than that exponent. The
coefficient reading identifies `(w1 partial_(w1))^j F` at (1,1) with
`sum_s s^j Q_s` for 0<=j<=d. This proves the full operator identity and the
polynomial-weight consequence.

The strict inequality cannot simply be replaced by a non-strict one:
at h=4, q=1, mu=(1,1,1,1), nu=(4), and input t4, the length difference is
3 and the third moment has nonzero output coefficient `[t4]=14400`.
The checker reproduces this boundary along with finite vector identities.
The band is a sparsity statement; it does not itself bound the rank of a
banded pairing or improve the complete contraction cost.
