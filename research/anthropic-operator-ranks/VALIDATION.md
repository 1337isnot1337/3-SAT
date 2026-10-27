# Exact-source replay

Computational checkpoint:
`0c11b353577fea1317171cbcea3f1951bc841cba`.
The source, operator code, screen, proof and saved evidence were exported
with `git archive` into a new directory without Git metadata.

The commands

```sh
python3 -I -B research/anthropic-operator-ranks/screen.py > replay.json
cmp replay.json research/anthropic-operator-ranks/verification.json
make verify
```

all passed there. The JSON output matched byte for byte. The scoped
screen binds operators.py, screen.py, SOURCES.json and PROOF.md by
SHA-256, as well as the decompressed external paper. The compressed
external text retains its own CC BY 4.0 attribution.

After the replay, canonical-main additions were integrated; the new
operator package's computational files did not change. Metadata-only
receipt edits are not inputs to the screen. Repository checks and
all 17 tests passed again on the integrated branch. CI also checks
Python 3.11 and 3.14; a green CI run is not an independent mathematical
review of the all-size proof.

No full SAT implementation, SAT speed comparison, Lean build or
independent proof review was performed.
