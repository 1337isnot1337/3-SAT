# Unfused F8 type-floor dual screen

The six-class four-macro support dual does not directly settle the ten-class
unfused F8 proposal. Its lift has minimum refined type size 2,401, far below
the threshold required by the predecessor's tensorization lemma. Moreover,
no single-block, self-Fourier type-floor certificate of that form can strictly
beat the target rate at block sizes one through seven. The first five block
sizes have no sufficiently large type; at size six the 84 eligible types
admit no nonzero self-Fourier vector, as certified by full modular column
rank. At size seven, averaging over a six-element symmetry group reduces
the target-pairing problem to 399 columns, also of full modular rank. [PROOF.md](PROOF.md) specifies the method and
inequalities.

This is a finite obstruction to a *particular proof method*. It does not
show that the ten-class crossing family meets or fails the desired rate,
that a larger block cannot work, or that any SAT bound improves. The written
argument is substantially OpenAI Codex assisted, author-checked and not
independently reviewed. The selected result is unchanged.

Reproduce from the repository root:

```sh
python3 -I -B research/three-bit-macro-walsh/certificate.py
python3 -I -B research/unfused-f8-dual/screen.py
OPENBLAS_NUM_THREADS=1 python3 -I -B research/unfused-f8-dual/seven.py
make verify
```

The first, second and last commands use standard Python. The optional seven-block
check requires NumPy (tested with 2.5.4); it took about 90 seconds here and
is not part of default CI. The first command checks the predecessor's
six-class certificate; the second
checks all 4,096 local characters, type sizes, lifted support, and the
six-block modular rank. The third verifies the seven-block symmetry reduction
and rank. Saved outputs are [verification.json](verification.json) and
[seven-verification.json](seven-verification.json).
The new screen does not search larger block sizes; the proof identifies a
concrete next premise. Source base `630041c9da3a26edb8c8f59d5f8a4132a188c8bd`;
the F8 scheme, Fourier basis and tensorization lemma are credited to
[three-bit-macro-walsh](../three-bit-macro-walsh/README.md), and the target
piece contract and external source attribution to its
[source manifest](../three-bit-macro-walsh/SOURCES.json). No new external
source is required. New work is Apache-2.0.
