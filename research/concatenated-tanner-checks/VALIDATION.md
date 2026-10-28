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

At commit `9d2d57a`, the detached worktree replayed both `verify.py` and
`verify_expander.py`, byte-compared each output to its saved JSON, and ran
`make verify`; all passed. The expander checker SHA-256 was
`09aa95adef84c7344f8c7f084d4693721e860a5f5767a723e2f1cfcd303fa06e`
and its output SHA-256 was
`ec2047efcb94cd031540e1527f96517e135a1fdf7b8c9332822c2fc19d1e9ea2`.
The source-scale and external-theorem limits above remain; this replay does
not establish the cited spectral theorem.
