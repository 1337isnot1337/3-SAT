# Operator moments and scalar recovery

Status: `scoped_checked`. AI-assisted, author-checked, not independently
reviewed. No improved alpha, rho or complete SAT bound.

Task: `contraction-schedule`. Base commit: `7561c0836b94d33166fc9e0eff6e15cc160f03ef`.

Contributor: OpenAI Codex (AI-assisted). Disclose substantial AI assistance.

## Question and changed premise

The [preceding operator package](../anthropic-operator-ranks/README.md)
proved a first-moment identity and removed one piece. This round changes
the proposed recovery: use higher weighted moments of the same pieces
and normalize their label pairing, rather than another scalar
reweighting preserving the original crossing verbatim.

Question: can a higher moment yield an invertible scalar label pairing
and avoid the costly central pieces without losing the two-direction
factorization contract? The external source is Anthropic's pinned
Hexagon 2610.00577v1, Appendix B. The accepted OpenAI baseline is unchanged.

## Statement and scope

The [proof](PROOF.md) gives two all-size component identities in the
source's zero-charge polynomial-ring module:

- The second moment is scalar on each energy space:
  `sum_s s^2 Q_s(a,b)=4E G(a,b) Id`, with the explicit integral
  Wick-contraction pairing G.
- For j>=2, the j-th moment has rank at most `p(j)-1` across
  `(x,v)|(y,u)`, where p is the partition function. This third cut is
  distinct from the two cuts that control rho.

The finite codebook results are:

| lambda | h | Binary dimension | Second pairing rank | Scalar weight-space dimension |
| --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 1 | 3 |
| 2 | 4 | 4 | 3 | 3 |
| 3 | 6 | 8 | 5 | 3 |

In these cases every scalar recovery weight is quadratic:
`f_s=a+b*s+c*s^2`. Dropping the central source piece sets a=0 and
leaves the singular second-moment pairing. Thus this tested interface
cannot omit the central piece and normalize an invertible crossing.
This is a finite classification, not an all-h obstruction or a result
about a general product `B(x,v)K(y,u)`.

For lambda=2,3 the exact third-cut ranks for j=2,...,6 are
`1,2,4,6,10`, attaining `p(j)-1`. Full energy-space Wick-pairing matrices
at h=2,...,12 have exact ranks agreeing with `p(h)-p(h-2)`. That latter
pattern is a finite observation; no uniform rank formula is proved.

Success would require valid normalization with paid integer heights,
entries and smaller required directional costs. The scalar interface
fails at the tested sizes. A next round must change the codebook,
product recovery or piece family and state that changed premise.

## Complete cost

The primitive does not supply a new contraction schedule. The original
crossing already has third-cut rank one while both required cut ranks
are D^2. The checker includes this control. A rank in the third cut
therefore cannot be substituted for the source's row/column costs.

The reference Wick recursion is a finite oracle. No uniform low-height
integer factorization of normalized moments is provided. A generic
matrix inverse can have exponentially large bit length in lambda even
if its arithmetic time is 2^O(lambda). Low-order moments have few third-cut
components; taking order Theta(h) can require 2^Theta(lambda) of them.
The [proof's cost boundary](PROOF.md) charges these unresolved obligations.
The selected general-density time, fixed-density time and alpha remain
unchanged. No randomness is introduced.

## Evidence and reproduction

Run offline from the repository root using Python 3's standard library:

```sh
python3 -I -B research/operator-moment-recovery/screen.py
make verify
```

The [saved report](verification.json) binds this implementation, its
proof and the frozen predecessor operator module. Every complete tensor
at lambda=1,2,3 is hashed against the predecessor's independently saved
screen before use. A direct operator sum checks the separate Wick
formula on 217 general homogeneous cases and all 4,368 coded tensor
entries. All reported ranks over Q are rational elimination or a
modular lower bound meeting a separately proved nullvector upper bound.
No modular rank is used as an unproved characteristic-zero upper bound.

The exact [reference code](moments.py) evaluates full contractions by
permanents with labeled repeated parts; [screen.py](screen.py) performs
the scalar linear constraints and middle-cut ranks. The first complete
run took 17.40 seconds and roughly 229 MiB peak RSS on this host. These
are checker resources, not a SAT speed claim. The screen is not in
default CI. No Lean build or end-to-end fast SAT solver was run.

## Limits and open next questions

Both all-size component arguments await independent review. The full
pairing rank pattern and a uniform scalar-weight classification remain
open. [HANDOFF.md](HANDOFF.md) records the next changed recovery question
and the exact cost constraints that an improvement must meet.

## Sources and credit

The predecessor is [PR 10](https://github.com/1337isnot1337/3-SAT/pull/10),
computational source `0c11b353577fea1317171cbcea3f1951bc841cba` and
integration head `7561c0836b94d33166fc9e0eff6e15cc160f03ef`.
Its [source metadata](../anthropic-operator-ranks/SOURCES.json) and
[source license](../anthropic-operator-ranks/source/README.md) preserve
Anthropic's attribution, exact version and CC BY 4.0 text. This package
does not duplicate or modify that source. The external full theorem and
Lean development have not been independently verified here.

The original code and arguments here are Apache-2.0 and substantially
OpenAI Codex-assisted. No independent review or priority claim is made.
