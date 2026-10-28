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

At commit `42bf1eb`, both scoped checkers and byte comparisons were replayed
in the detached worktree, and `make verify` passed. The expander checker
SHA-256 was `678b6c5b635c9df10371a28f868ac37f731ecf02429b343178d9d6fa6ecef372`
and its saved output SHA-256 was
`48e049fdc1002b33e99937f20b3bd39bfdc773c2d54a740d221702408d0c6eb9`.
This includes the complete scaled Tanner fixture; it remains author replay.

At commit `85a07a8`, the detached worktree repeated both scoped checkers,
both byte comparisons and `make verify`; all passed. The expander checker
SHA-256 was `c0a53b43c61e0b45d845553fa7c86db36e337653d14dd5089f5600c536891937`
and its output SHA-256 was
`4d81a8beb15488748660805e6b0c5a8fef206fa56a6affe157c3a3973bef334e`.
This adds finite information-set checks and remains an author replay.

At commit `f5dc3e6`, both scoped checkers and byte comparisons were repeated
in the detached worktree, and `make verify` passed. The expander checker
SHA-256 was `e7e23dbe76f89a9518051324d73f4cde73165ad656a27cb7984cf17b406397f8`
and its output SHA-256 was
`efcdc2a2a15622e13ffa0af7dcfc9bfe2ee691925812a99951b70ffe923b5118`.
This includes exact finite spectral PSD certificates; it remains author replay.
