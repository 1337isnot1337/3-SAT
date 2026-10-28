# Bounded replay

At commit `3076532`, a separate detached worktree replayed:

```sh
python3 -I -B research/concatenated-tanner-checks/verify.py > /tmp/3sat-concat-clean.json
cmp research/concatenated-tanner-checks/verification.json /tmp/3sat-concat-clean.json
make verify
```

All commands passed; the last command ran 17 unit tests and repository checks.
The verifier SHA-256 was
`307fa9bed9199d242cb4adcfb55d96f43be66c8720128df2224b7d6a845ebcee`;
the byte-identical output SHA-256 was
`755038076938eef7bfc040f091bf3324cb3a57007ce89ab16a1007a1fa2d16d7`.
This is a clean replay by the author, not independent review, a source-scale
q>1 Tanner build, or a verification of the all-size construction.
