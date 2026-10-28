# A grade-nine charged cubic crossing on even output partitions

Status: `scoped_checked` for the finite pairing and sampled direct check below. The written
all-grade parity identity from [PR #89](../charged-cubic-parity/PROOF.md)
is author-checked and awaits independent review. This package gives no
asymptotic SAT improvement or selected-result change. Contributor: Cinna
Davis, with substantial OpenAI Codex assistance.

## Construction

Use exactly the charge-one, h=9, N=8 asymmetric **input** row and column
labels selected by `construct(3)` in PR #19. Replace its output codebook
with the first eight partitions of 9 having even length:

```text
(2,1,1,1,1,1,1,1), (2,2,2,1,1,1), (3,2,1,1,1,1), (3,2,2,2),
(3,3,2,1), (4,1,1,1,1,1), (4,2,2,1), (4,3,1,1).
```

Let `w_s=(s^3-s)/6`. The h=9 energy bound restricts s to -18,...,18,
and w vanishes at -1,0,1. For the chosen input and output labels, the
weighted sum of the source tensors is `G[a,v] [y=u]`, where the exact
8-by-8 rational pairing G is invertible. The report contains G and its
inverse. Multiplying each piece on its first input axis by the inverse and
by w_s gives the crossing identity `[x=v][y=u]`, with all three central
pieces absent. This is a compression to the named output codebook; the
codebook need not be invariant under the weighted operator.

The 14 even and 16 odd output partitions both contain eight states.
The actual direct checker below uses the eight named even states, not all
possible eight-state codebooks. The predecessor's parity theorem supplies the scalar-compression identity
used here. One output vector is checked directly; exhaustive direct tensor
verification is running and has not yet been reported.

## Relation to the grade-nine obstruction

The merged [grade-nine filter obstruction](https://github.com/1337isnot1337/3-SAT/blob/572a226d56cf5fe38a80197dadf89cf300eeef39/research/grade-nine-filter/README.md)
proves that no nonzero scalar weight with these three zeros works on a
different, fixed original output codebook. It does not cover this changed
output selection. The present construction keeps the input labels and
changes the output states; it is a finite counterexample to extending that
obstruction to all eight-state output codebooks, not a correction of the
original result.

## Evidence and limits

From the repository root with Python 3.11+ and the standard library:

```sh
python3 -I -B research/charged-grade9-parity/fast.py > /tmp/charged-grade9-fast.json
cmp /tmp/charged-grade9-fast.json research/charged-grade9-parity/fast-verification.json
make verify
```

The checker builds the exact pairing by the two-energy identity and checks
its inverse. It directly computes one cubic weighted output vector and checks its eight
projected entries; it verifies the exact 8-by-8 inverse identity. The full
crossing statement relies on the predecessor's written parity and affine
energy identities. An exhaustive direct check is running separately and
is not counted as evidence here. The shared predecessor implementation is not an
independent operator oracle. The first-input-axis inverse preserves both
source cut ranks, but this example does not prove any improved all-size
rank envelope. Coefficient heights, uniform label/output selection, input
pairing rank, and all full SAT costs remain obligations for a general family.

The filter removes only three shifts; the nearest retained shifts are ±2,
so their source cost envelope approaches the original central maximum as
h grows. No new rho, alpha, general-density time bound or SAT solver is
claimed. The example is based on PR #89 commit
`298c6603b07503fd8ccef68b39405de3e36b79a6` and is a dependent continuation.
Source, hash, license and predecessor credit are preserved in
[PR #19's source manifest](../charged-asymmetric-crossing/SOURCES.json).
