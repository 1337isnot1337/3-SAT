# Active continuation checkpoint

User goal remains active and INCOMPLETE: work indefinitely on a mathematical
improvement, push/commit often, and merge checked coherent PRs. The user
explicitly authorized merges. No subagents were spawned. Do not stop or mark
the goal complete merely because these partial packages are archived.

Working repo `/home/cinna/3-SAT`; current branch
`research/symmetric-walsh-pieces`, base
`4ec0e136b819b7d12fedf72ad2f8286098c6f4a7`. Refresh canonical main, all
advertised branches, PRs and changed rules before a new round or submission.
The selected accepted OpenAI bound remains alpha 1/2. Upstream is unchanged.

Completed owned predecessors: PR 3 scalar encoding/support entropy, merged
`c5147fc`; PR 6 generic and actual-network parity recovery precision,
merged `eef5902`; PR 13 two-scale kernel/spectrum with its full-node recovery
tradeoff, merged `4ec0e13`. Their scoped checks and all 17 repository tests
were replayed on exact clean main at the relevant merge checkpoints.
None selects a stronger theorem or constitutes independent review.

Current result: an actual uniform Pauli/Walsh crossing family with explicit
integer factors and support ranks. Small lambda=1,2,3 looks exceptionally
good, but later finite cases worsen. The **all-size** dual in
SYMMETRY-BARRIER.md closes the entire permutation-symmetric Pauli-diagonal
class, including arbitrary cancellations and any finite piece count.
No asymptotic extrapolation is used. A macro extension also closes two-bit
macro-permutation symmetry by an exact close entropy inequality.

Reproduce offline with standard Python:

```sh
python3 -I -B research/symmetric-walsh-pieces/screen.py
make verify
```

Do not extend the same binary symmetric screen: its global stopping
condition is met. The next distinct premise is **three-bit macro-coordinates**.
It is not ruled out by the present dual and has a manageable three-class
coefficient space. Let R be the number of macros, lambda=3R, and use

```text
class weights: (1,35,28)
Walsh matrix: [[1,35,28],[1,3,-4],[1,-5,4]]
target values per macro: (1,1,-1)
```

This matrix squares to 64 I and sends the target to eight times itself.
The checks independently enumerate all 4,096 actual six-bit characters
to verify those class sums. For R macros, types have three coordinates
adding to R, with weight `R!/prod(alpha_j!)*prod(class_weight_j^alpha_j)`.
The compressed transform is the symmetric-power coefficient formula in
CONSTRUCTION.md, now with three letters. Its dimension is `(R+2 choose 2)`;
its square is `64^R I`, and its target eigenvalue is `8^R`.

Adapt the exact two-flag constructor to these weighted types. Both support
counts must use the weights, not just the number of types. A smaller full
rate requires shared bits below `2 sqrt(2)*lambda+O(log lambda)`, i.e.
`6 sqrt(2) R+O(log R)`. Finite ratios are only evidence. For arbitrary input
length, padding to a multiple of three changes only O(1) bits. Keep integer
height, polynomial piece count, explicit support unranking and `2^O(lambda)`
evaluation, and charge the full external master recursion before any SAT
bound. The external paper is not automatically accepted or selected.

The [clean-export replay](VALIDATION.md) is complete. Immediate actions:
publish/merge this coherent global result, then register and run the new macro-family. Existing other
branches cover Anthropic operator ranks, charged moments, moment recovery
and sparse oscillators. Preserve them and check live overlap.
