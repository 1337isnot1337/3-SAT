# Scoped clean-export validation

Checked source checkpoint:
`fa7d6603a6e3c0c482650321985a1ddd4c75411e`, tree
`d39dc199a45c46e15834767e81c6679384bf353e`.

An export produced with `git archive` contained no `.git` directory.
Running the package checker there reproduced [verification.json](verification.json)
byte for byte; `make verify` passed source/metadata/link checks and all
17 repository tests. The original replay directory was
`/tmp/3sat-two-scale-export.kGGR87`; the directory need not persist to
reproduce the result.

From a repository containing that commit, create a new empty export and run:

```sh
git archive fa7d6603a6e3c0c482650321985a1ddd4c75411e | tar -xf - -C EXPORT_DIRECTORY
cd EXPORT_DIRECTORY
python3 -I -B research/two-scale-cauchy-grid/verify.py > replay.json
cmp replay.json research/two-scale-cauchy-grid/verification.json
make verify
```

`EXPORT_DIRECTORY` must already be a new empty directory. No external
libraries, network requests or Git metadata are used by these checks.

The saved scope is: 103,228 direct minors; 960 complete shifted kernels;
27,648 kernel coefficients; 390 exact nodewise primal/dual and large-gap
certificates; 1,496 direct full-node matrix entries; and two generic
witnesses with all 32 charts and 9,184 coefficients expanded. This checks
the finite statements and bindings only. It is not independent review,
formal verification, a fast contraction implementation, hosted CI, or a
SAT-bound selection. Later documentation-only additions do not alter the
tested proof, checker or saved-output bytes.
