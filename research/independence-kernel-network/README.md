# Nonlocal kernel network for the independence polynomial

Status: `scoped_checked` for finite identities; the all-size argument is
author-checked and awaits independent review. No SAT speedup is claimed.
Task `decision-only`; base `c7c5a03434b396e227e9ab573b5b7cdea52b47fa`.
Contributor: Cinna Davis, with substantial OpenAI Codex assistance. Apache-2.0.

[PROOF.md](PROOF.md) rewrites the binary-matroid independence polynomial
at **arbitrary** characteristic-two field values as a weighted sum over
`ker(A)`, using the Boolean interpolation factors `z_j` and `1+z_j`.
The same identity also gives an invertible Boolean zeta transform from the
kernel truth table to the independence coefficient table; it recovers the
exact `2^b` characteristic-two cut rank from PR #104. An exact nonlocal
network uses sparse row parity constraints, equality
trees and `O(m+a+h)` wires for an a-by-m binary matrix with h ones.
Grouping field weights and applying the owner-accepted contraction theorem
then evaluates one point in polynomial space and
`(s+L)^O(1) 2^O(s/sqrt(log s))` time, with `s=m+a+h` and field degree
`O(log s)`. It is a component evaluation, not a full SAT algorithm.

The polynomial identity extends to `F_q`-represented matroids when the
coefficient field has characteristic p and `q=p^r`. For fixed `q=2^r`,
the same accepted-contraction evaluation works after encoding each F_q
symbol in r Boolean bits; the odd-characteristic case is an algebraic
identity only. For q>2 the support-aggregation map is rectangular and can
lower cut rank; an F3 parallel-pair control has kernel rank 3 and
independence rank 2.

For `[I_b | I_b]` with separated copies, the network has O(b) wires while
the ordered chain from PR #104 needs b² bond wires; an interleaved order
avoids that separation. Thus the topology bypasses a fixed-order width cost,
not every ordering or every SAT representation. General clause inputs can
still require more than the desired `n log log n` wires.

For matrices with `a+h=O(m)`, the bound is
`poly(m) 2^O(m/sqrt(log m))` with polynomial space. Evaluating at `m+1`
field points and interpolating also recovers the parity of the number of
independent sets of every cardinality within that same envelope. These are
conditional consequences of the accepted contraction theorem for sparse
matroid inputs, not new general 3-SAT bounds.

## Reproduction

```sh
python3 -I -B research/independence-kernel-network/verify.py
make verify
```

The checker compares the independent-set and kernel formulas on all 4,096
binary 3-by-4 matrices and all 16 Boolean weight vectors, with explicit
XOR-accumulator path counts and zeta coefficient checks, plus 2,000 seeded GF(8) weight vectors with
grouped polynomial-lift controls, plus 200 end-to-end GF(8) size-parity
interpolations. The prime-power identity is checked
exhaustively on 2-by-2 matrices over F3 and F4, with a mismatched-
characteristic failure control, including explicit binary
linear-map controls for the F4 row checks. It also checks
32 paired-column width profiles. The [saved output](verification.json) pins
the checker hash and seed. These are finite controls, not an independent
review or an implementation of the accepted contraction solver.

## Credit and next steps

The shared-code identity and field lift are from PR #2, the free Boolean
kernel row network from PR #83, and the ordered independence chain and cut
rank from PR #104. All remain separate unreviewed research. The frozen OpenAI
source is pinned in [SOURCES.json](../../SOURCES.json), especially
`thm:tensor-contraction`. Standard interpolation and parity networks are used
without a priority claim. A SAT application must integrate actual clauses,
all queries, branching, precision, recovery, randomness and the full cost;
the selected result remains unchanged.
