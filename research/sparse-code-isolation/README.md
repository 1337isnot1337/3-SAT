# Sparse-code isolation for parity-only SAT decision

Status: `scoped_checked` for bounded checks; written all-size arguments are
author-checked and await independent review. **No time or alpha improvement
is claimed.** The accepted OpenAI theorem is a premise throughout.

Task: `decision-only`. Base `45c962254338a250e712bbd79089d979a97d395f`.
Contributor: Cinna Davis with substantial OpenAI Codex assistance. Apache-2.0.

The [proof](PROOF.md) supplies a decision-interface change for unrestricted
inputs. Use the accepted sparse-check lemma to encode every assignment uniquely
into an O(n)-bit codeword with inverse-polylogarithmic relative distance.
A polylogarithmic-sparsity random affine hash family then isolates one member
of any nonempty set with constant probability at one of n+1 dimensions.
An exact unweighted parity evaluation detects a uniquely isolated survivor.
Combining this with the predecessor's random clause-violation hash wrapper
gives the same general-density time envelope, polynomial space and explicit
per-input error, without its separate random field fingerprint. The isolation
hashes themselves remain random. The accepted deterministic exact counter
already achieves that time envelope, so there is no new SAT bound.

A subtlety: selecting information coordinates does not make the parity-check
matrix dense. The encoding keeps the original sparse check equations and fixes
unused information coordinates with unary constraints. The construction of
the sparse checks takes exp(polylog(n)) time as stated in the accepted source,
not polynomial time; it is nevertheless within the accounted asymptotic
budget. Concurrent [PR #78](https://github.com/1337isnot1337/3-SAT/pull/78)
proposes a polynomial-time construction of the same check interface; this
package does not rely on its unreviewed argument. All random loops and field-free parity calls have fixed bounded length.

The bounded checker enumerates the complete hash-row distribution and all
nonempty supports of a small systematic distance-two code. It also checks a
one-bit unencoded collision control; it does not implement the accepted code
constructor, wrapper, contraction or full algorithm. Reproduce with Python
3.11+ and the standard library:

```sh
python3 -I -B research/sparse-code-isolation/verify.py
make verify
```

See [verification.json](verification.json) and [PROOF.md](PROOF.md). Source:
OpenAI commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`, labels
`lem:sparse-checks`, `lem:sparsify`, `lem:tensor-sparse-query`, and
`thm:tensor-contraction`; hashes and licenses in [SOURCES.json](../../SOURCES.json).
Credit `research/characteristic-two-decision/PROOF.md` for the wrapper and
field evaluator. This route differs from issue #53's randomness reduction for
clause-violation hashes; coordination is in
[issue #80](https://github.com/1337isnot1337/3-SAT/issues/80).
