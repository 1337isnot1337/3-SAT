# Branching syndrome trees and contraction degree

Status: `scoped_checked` for bounded tests; the all-size proof is author-checked
and awaiting independent review.
No improved SAT time bound or alpha is claimed. Coordination:
[issue #149](https://github.com/1337isnot1337/3-SAT/issues/149).
Base `c600b21ee7800a49c05718a254be50168e6b355b`.

The attempted change replaces the ordered shared-syndrome chain by an
arbitrary branching tree with freely grouped Boolean inputs. The
[proof](PROOF.md) constructs optimal edge states on any supplied tree and
shows that every exact tree representation of an [m,k,D] binary code
indicator, over any field, has maximum Boolean-port degree at least
`ceil(k/floor(m/D))` when k>0. The proof combines the exact cut rank with a
weighted separator containing at most floor(m/D) vertices.

For the accepted sparse-check matrix with t appended checks, let
`K=max(0,m-3n-t)`. In the regime m>P and K>0, every such tree has degree at
least K/P. When K=Omega(m), m>=n and P is polylogarithmic, this exceeds the
accepted contraction theorem's degree cap for s=O(n log log n). This stops
the proposed tree-only compression route in that stated regime. It does
not cover restricted clause-violation patterns, cyclic networks, other
encodings or arbitrary SAT algorithms. Low nullity can make it vacuous.

The minimal tree-state construction is established coding-theory material;
see Navin Kashyap, [On Minimal Tree Realizations of Linear Codes](https://arxiv.org/abs/0711.1383v1)
and [Constraint Complexity of Realizations of Linear Codes on Arbitrary Graphs](https://arxiv.org/abs/0805.2199v1).
This package supplies a self-contained Boolean-port argument and its precise
application to the repository's contraction interface, without claiming
scientific priority. Repository predecessors:
[hash-syndrome-chain](../hash-syndrome-chain/PROOF.md) and
[hash-frontier-width](../hash-frontier-width/PROOF.md).
Accepted OpenAI source commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`,
`lem:sparse-checks` and `thm:tensor-contraction`; hashes in
[SOURCES.json](../../SOURCES.json). Contributor: Cinna Davis with substantial
OpenAI Codex assistance; new material Apache-2.0.

Reproduce with Python 3.11+ and the standard library, from the repository root:

```sh
python3 -I -B research/syndrome-tree-compression/verify.py > /tmp/syndrome-tree-replay.json
cmp /tmp/syndrome-tree-replay.json research/syndrome-tree-compression/verification.json
make verify
```

[Saved evidence](verification.json) covers 2,100 matrix/layout cases, including
all two-row binary matrices with 1..4 columns on five layouts and 400 seeded
larger grouped-input cases. There are 28,200 exact integer contractions,
9,692 flattening-rank checks over F2/F3, and 2,941 separator/injectivity checks.
The controls include zero kernels, zero columns, empty internal vertices,
all inputs at one vertex, repetition codes through length 12, a Hamming-code
parameter fixture, and restricted input patterns that destroy the generic
rank obstruction. These are finite component checks, not an implementation
of the accepted SAT solver or independent review of the all-size proof.
The checker is separate from default CI. [Source pins](SOURCES.json) record
versioned external PDF hashes without redistributing those papers.

The next changed premise must use restricted input patterns or a non-tree
topology; this package does not complete the active goal of beating the SAT
bound.
