# Bounded clean replay

At commit `935f972`, a separate detached worktree ran:

```sh
python3 -I -B research/concatenated-tanner-checks/verify.py > /tmp/3sat-concat-replay.json
cmp research/concatenated-tanner-checks/verification.json /tmp/3sat-concat-replay.json
python3 -I -B research/concatenated-tanner-checks/verify_expander.py > /tmp/3sat-expander-replay.json
cmp research/concatenated-tanner-checks/expander-verification.json /tmp/3sat-expander-replay.json
make verify
```

All commands passed; the last ran 17 unit tests and repository checks.
The expander checker SHA-256 was
`c2ef917ec40f178e742d538c855269fb9edfcc28e9513f8d568a9dd5f57d5793`
and its byte-identical output SHA-256 was
`0066595a04a8cb5cc61584533e59fd06086e5fde7f5cc29f694d31c4444b2f6c`.
This is an author replay, not independent review, a source-scale q>1 Tanner
build, or a verification of the all-size construction or cited spectral theorem.
