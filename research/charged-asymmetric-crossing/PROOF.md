# A uniform asymmetric first-moment crossing

Author-checked, substantially AI-assisted; no independent or formal review.
This completes the asymmetric-coordinate obligation of PR 11 using the
rational transfer of PR 17. It removes one central piece, not a leading
fraction of the expensive shifts, and proves no improved SAT exponent.

## 1. Predecessor identities and label capacity

Use the charge-one normal-ordered operators of
[PR 11](../charged-operator-moments/PROOF.md). For partitions mu,nu of h,
their first-moment identity on every output energy space is

```math
 \sum_s sQ_s(a_\mu,b_\nu)=G_h(\mu,\nu)\operatorname{Id},
 \qquad \operatorname{rank}G_h=r_h=p(h)-p(h-1),\quad h\ge2.
```

The explicit matrix is the factorial-diagonal rescaling of PL in that
package. It is square-zero after rescaling and a common principal label
restriction is singular. None of the present argument inverts that full
matrix or any common principal restriction. The predecessor supplies the
two-order identity, rank formula and unchanged intermediate energy spaces;
their author-checked evidence boundary is retained here.

For N=2^lambda, lambda>=1, let h be the least integer with r_h>=N.
The predecessor proved `p(h)<=1+(h-1)r_h`. Also `p(h)<=h p(h-1)`:
decrease a largest part to map a partition of h to one of h-1. A target
partition has at most h preimages, obtained by increasing a part or adding
a one. Since h>=4 and r_(h-1)<N, these inequalities give

```math
 N\le p(h)<h^2N.
```

Hardy--Ramanujan's logarithmic estimate, used with the same constant kappa
as the source, now gives
`h=Theta(lambda^2)` and `kappa sqrt(h)=lambda+O(log(2 lambda))`.
Partition counts for the grade search are computed by polynomial dynamic
programming. Only `p(h)<=h^2N` labels need enumeration at the chosen grade.

## 2. Different row and column labels

Select any nonsingular N-by-N minor of G_h by exact elimination. Let its
row partitions be mu_0,...,mu_(N-1), its column partitions nu_0,...,nu_(N-1),
and its matrix M. The rows and columns may differ. Rank r_h>=N guarantees
existence. The code uses a deterministic pivot order and verifies the
inverse explicitly.

Independently choose any N partitions sigma_0,...,sigma_(N-1) of h for
the two output axes y,u. The same output codebook must be used on those
two axes. Define

```math
 C_s(x,y,u,v)=[t^{\sigma_u}]
              Q_s(a_{\mu_x},b_{\nu_v})t^{\sigma_y}.
```

The source energy bound, now E=h, restricts s to -2h,...,2h. The scalar
first-moment identity gives exactly

```math
 \sum_s sC_s(x,y,u,v)=M_{xv}[y=u].
```

No equality of the row and column label sets is used. No scalar projection
of higher moments is assumed.

## 3. Actual rational crossing pieces

For each nonzero s in that range set

```math
 A_s(x,y,u,v)=s\sum_a(M^{-1})_{xa}C_s(a,y,u,v).
```

Then

```math
 \sum_{s\ne0}A_s(x,y,u,v)=[x=v][y=u].
```

Indeed the sum is `(M^-1 M)_(xv)[y=u]`. The omitted s=0 contribution
was identically zero after multiplication by s. These are actual functions
with rational entries, not hypothetical rank bounds or an inverse of a
singular pairing. Their normalizer is one over Q.

## 4. Both directional ranks survive

In the row flattening, the transformation multiplies C_s on its left by
`s(M^-1 tensor I_y)`. In the column flattening it multiplies C_s on its
left by `s(M^-1 tensor I_u)`. For nonzero s both are invertible rational
matrices. Thus BOTH ranks are exactly preserved, rather than only the cut
on which a generic joint-axis inverse happens to be local.

The charged source factors have the same intermediate term counts

```math
 R_s=\sum_{i=0}^{2h}p(s+i),\qquad
 C_s^{\rm terms}=\sum_{i=0}^{2h}p(2h-s-i),
```

where p(t)=0 for t<0. Restricting labels to the selected codebooks and
performing this local invertible change cannot exceed those bounds.
Consequently the sum of the two binary rank costs is at most

```math
 \kappa\bigl(\sqrt{2h+s}+\sqrt{2h-s}\bigr)+O(\log(2h))
 \le2\sqrt2\,\lambda+O(\log(2\lambda)).
```

There are 4h pieces. The inherited contract is rho=1/sqrt(2), with a
polynomial piece count. The actual ranks can be lower than these term
counts; no all-size improvement of them is proved here.

## 5. Uniform rational generation and heights

There are at most h squared times N partition states. The entries of G_h
are obtained by the explicit finite PL formula; derivative, binomial and
factorial bounds give polynomial bit length in h. Elimination, minor
selection and inversion on a matrix of size `2^O(lambda)` therefore take
`2^O(lambda)` bit operations. Determinant bounds allow `2^O(lambda)` bits
in inverse numerators/denominators; they need not be polynomial in lambda.

For each C_s entry, use the source's uniform normal-order recurrence at
grades at most 4h. The largest intervening partition space has
`p(4h)=2^O(lambda)` states. Fixed charge one adds only its scalar zero-mode
term. The same table construction is `2^O(lambda)` in bit time with
polynomial-in-h original coefficient lengths. Arbitrary selected labels
of grade h have the same bounds as the lexicographic source labels.

An A_s entry uses at most N such entries and one row of M inverse.
Exact rational arithmetic still takes `2^O(lambda)` bit time and space.
All indices, shifts, selected labels and the normalizer are uniformly
computable within that bound. This meets PR 17's rational rank-only
contract. A polynomial-height exact integer factorization is not assumed.

## 6. Full cost consequence and limits

Apply the rational transfer to compile both factors over one boundedly
sampled large prime. Its all-parameter bad-prime bound, exact signed
integer-query recovery and capped trials cover the inverse denominators.
Retain every source reduction branch, rejected greedy query, profile,
entry computation and recursive call. The resulting time has the same
rho=1/sqrt(2) master exponent and the same arbitrary-density correction.
The computability hypothesis on rho holds for this explicit algebraic
constant. Finite exceptions use the source's deterministic fallback.

For each fixed formula, any returned count is exact and success probability
exceeds 99/100; FAIL can be interpreted as NO for one-sided decision error.
Time is bounded on every random outcome. The generic compiler's exponential
space is explicit, so polynomial space is not claimed. These are transferred
consequences under the written component proofs, not a new full SAT solver
executed by this package or a selection of a new result.

The near-central shifts s=+1 and -1 still have the same leading
`2 sqrt(2) lambda` term envelope: their normalized shift tends to zero
because h=Theta(lambda^2). Deleting only s=0 cannot yield a fixed smaller
rho from that envelope. This conclusion concerns this supplied bound; it
is not a lower bound on every actual rank or every possible successor.

## 7. Checked evidence

At lambda=1,2 the checker computes all actual rational pieces at h=4,6,
verifies their full crossing sums and both flattening ranks, checks source
term bounds and compiles both directions over F65537. It checks 152
positive-grade two-order cases, 160 exact rational rank computations,
272 crossing entries and all 4+16 predicate counts. Minor selection and
inverse identities additionally cover lambda=3,4 at h=9,12 without
constructing their full operator tensors. Those finite cases are not a
proof of a lower eventual rho or of the entire source theorem.

The changed next problem is stated in [NEXT.md](NEXT.md): a valid scalar
filter removing a whole central interval while retaining leading capacity
and both directional ranks. All arguments here are substantially
Codex-assisted and await independent review.
