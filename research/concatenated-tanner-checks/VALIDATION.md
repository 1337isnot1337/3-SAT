# Bounded clean replay

At commit `e41db24`, a separate detached worktree ran:

```sh
python3 -I -B research/concatenated-tanner-checks/verify.py > /tmp/3sat-concat-replay.json
cmp research/concatenated-tanner-checks/verification.json /tmp/3sat-concat-replay.json
python3 -I -B research/concatenated-tanner-checks/verify_expander.py > /tmp/3sat-expander-replay.json
cmp research/concatenated-tanner-checks/expander-verification.json /tmp/3sat-expander-replay.json
make verify
```

All commands passed; the last ran 17 unit tests and repository checks.
The expander checker SHA-256 was
`02ae3e53e94890937b89cce01c296b33b3d5ad16183acaacae306fd399446d39`
and its byte-identical output SHA-256 was
`efcdc2a2a15622e13ffa0af7dcfc9bfe2ee691925812a99951b70ffe923b5118`.
This is an author replay, not independent review, a source-scale q>1 Tanner
build, or a verification of the all-size construction or cited spectral theorem.
