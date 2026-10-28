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

At commit `31881d8`, the same detached worktree repeated the scoped checker,
byte comparison, and `make verify`; all passed. The checker SHA-256 was
`00e343658b65c3ac13a20edf3042ef19e82bdd1664af451ecc937d8ca1415cf8`
and the output SHA-256 was
`2561b52c041974661c30daf56efede875f56f6a3360e5343098de42ff46609a6`.
This is again an author replay with the same scope limitations.
