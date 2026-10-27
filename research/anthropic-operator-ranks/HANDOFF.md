# Operator-piece checkpoint

Canonical base: fd6df02023122badbdd888803146f0bd92002214.
External source: Hexagon 2610.00577v1; exact TeX and archive pins in
[SOURCES.json](SOURCES.json). The external theorem as a whole is not
owner-selected or independently checked here. No upstream file changed.

## Completed

An exact, standard-library implementation of the Appendix-B definitions
matches an independent normal-ordered implementation at small energy.
The complete lambda=1,2,3 screen verifies both operator orders, duality,
and all tensor identities. Exact rank gaps do not save index bits.

The first-moment relation `sum_s s Q_s=0` on each energy space has a
written normal-ordering proof. It removes shift s=1 by integer
reweighting `(1-s)`, retaining the same h! crossing denominator and
both factorization costs. There are 4h pieces instead of 4h+1.
This is a scoped component improvement with no new alpha or full time
envelope. The finite tensor-span ranks show that one deletion is the
most possible using only scalar reweighting of these fixed pieces.

The saved [verification](verification.json) binds code, source metadata
and proof by hash. Reproduce with the README command. The checker's
peak memory is roughly 253 MiB; do not silently add it to default CI.

## Next changed mechanisms

- Study higher moments of the piece family and their exact operator
  content. Small lambda=1,2 probes found the second moment scalar on
  the y/u legs but with a singular x/v pairing; this probe is not yet
  saved as a certified result and has no claimed algorithmic use.
  Determine the pairing algebraically before assuming an inverse or
  a recovery shortcut. Third moments were nonzero, so do not assume
  that all odd moments vanish.
- A rank improvement that only deletes noncentral shifts is not enough
  when the central piece retains the worst shared-bit budget. Changing
  the piece family or proving a smaller intermediate image is the
  substantive target. Finite rank data alone do not prove its growth.

## Failed routes supplied by the user

These are scoped constraints, not lower bounds on every SAT algorithm.
Do not repeat the same premise without a new lemma.

- Even-node congruences for the OpenAI Cauchy deformation fail because
  shifted-node integrality is not global integrality. PR5 has an exact
  diagonal W_00 counterexample. The user also reports the odd-prime
  variant blocked by divisibility of C'(0) at the desired node.
- Exponentially separated interpolation nodes may improve minor
  valuations, but the user reports larger integrality shifts and lost
  tile multiplicity. A candidate kernel must pay recovery precision
  and retain M/D-type mode multiplicity, not only high valuations.
- The user reports the low-total-degree unweighted parity barrier:
  for tests P_j(v) with P_j(0)=0 on r Boolean violation variables,
  sum deg(P_j)<r makes the common-zero count even. An elementary
  proof sums `product_j(1+P_j)` over the Boolean cube modulo two:
  every retained monomial misses a variable. For the unique-solution
  unit-clause formula, v is the identity, so this interface loses
  the odd count. Weighted fingerprints and other interfaces require
  their own analysis; this does not rule them out wholesale.

Refresh canonical main and live PRs before the next round or submission.
The user has now explicitly authorized PR merges. Merge only the exact
checked head with current CI and keep the selected result and proof
review status distinct from archiving a scoped research package.
