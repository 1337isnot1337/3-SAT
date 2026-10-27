# Validation receipt

Computational source checkpoint:
`e6581f9225726409797a21cfbce8eb6b85cfe656`.
Its Git tree is `c2c2ebd7864a4c6c33291f5e536c912c52cc538a`.
Canonical main fetched at this boundary was still
`fd6df02023122badbdd888803146f0bd92002214`.

The checkpoint was exported with `git archive HEAD` into a fresh
directory with no .git metadata. From that export:

```sh
python3 -I -B research/scalar-parity-lift/verify.py > replay.json
cmp replay.json research/scalar-parity-lift/verification.json
make verify
```

All three commands passed. The complete JSON output matched byte for
byte. The checker took 9.11 seconds and 22,936 KiB peak RSS on this host
under `/usr/bin/time`; this is the finite checker workload, not a SAT
algorithm performance result. Repository verification passed the seven
frozen source hashes, metadata and local links, and all 17 tests.

The saved JSON separately binds scalar_lift.py, verify.py, PROOF.md and
model.json by SHA-256. The later Anthropic attribution changed PROOF.md's
bytes and its saved binding; the coefficient routines and mathematical
argument did not change. New documentation was checked with
`make verify` and `git diff --check` before its commit.

Final computational source checkpoint before merging:
`d079cee5c7b0debb101db99e52d4fe922c4bbb8e`.
A fresh Git-free archive of that branch head reproduced the
updated saved JSON byte for byte and passed all 17 tests and repository
checks. This replay includes the added Anthropic attribution in the
proof and its new artifact hash. This receipt is metadata and is not
an input to the component checker.

No independent mathematical review, Lean build, full subexponential SAT
implementation, or asymptotic performance measurement was performed.
