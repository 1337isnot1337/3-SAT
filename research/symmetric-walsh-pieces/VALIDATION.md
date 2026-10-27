# Exact clean-export replay

Source checkpoint `0c3bfbb87bb7d57477585f87514081cc588e6987`, tree
`da1bb2277e778b7509ed390a3dc0884fe8fa0fcb`, was exported without Git
metadata. The scoped command reproduced [verification.json](verification.json)
byte for byte, and `make verify` passed all source/metadata/link checks
and all 17 repository tests. The original temporary directory was
`/tmp/3sat-walsh-export.Bb5kqc`; it is not a required persistent input.

Create a new empty directory, then reproduce from a repository containing
that checkpoint:

```sh
git archive 0c3bfbb87bb7d57477585f87514081cc588e6987 | tar -xf - -C EXPORT_DIRECTORY
cd EXPORT_DIRECTORY
python3 -I -B research/symmetric-walsh-pieces/screen.py > replay.json
cmp replay.json research/symmetric-walsh-pieces/verification.json
make verify
```

The screen is standard-library, offline, and deterministic. Its scope is
the eight exact finite constructor sizes, the listed small direct ranks,
25 symbolic dual witnesses, 327,680 full-word dual eigenidentities,
normalization and symmetry controls, and exact macro-alphabet certificates.
The all-size proofs are separate written arguments. No independent review,
formal proof build, hosted CI result, or SAT exponent improvement is claimed.
Later documentation-only additions leave the tested math and saved output
unchanged.
