# Grade-nine scalar-filter obstruction

This substantially AI-assisted finite certificate completes the grade-nine
question left open by [PR #46](../asymmetric-scalar-filter/README.md). It
has not received independent or formal review. It does not prove an
asymptotic obstruction or improve a SAT bound.

## Statement

Take the exact charge-one raw crossing pieces and deterministic asymmetric
row, column and output partition codebooks selected by the predecessor's
`construct(3)`: grade `h=9`, dimension `N=8`, shifts `-18,...,18`. Suppose
rational weights `w_s` make every weighted output matrix scalar for every
one of the 64 row/column label pairs, and suppose `w_-1=w_0=w_1=0`.
Then every `w_s` is zero. In particular no nonzero or invertible scalar
pairing on these fixed codebooks survives that exclusion.

This is an exact statement about one finite codebook. It does not classify
other codebooks, charge-dependent filters, non-scalar output identities, or
all grades, and it does not prove any lower bound for 3-SAT.

## Certificate and proof

The scalarity equations demand zero off-diagonal entries and equal diagonal
entries on the eight-state output space. They are integer homogeneous linear
constraints in the 34 noncentral weights. We use only the following subset:

1. The 315 constraints from input pairs `(7,7)`, `(6,7)`, `(5,7)`, `(4,7)`,
   and `(7,5)`, with zero-based indices in the deterministic predecessor
   codebooks. Eight columns, at shifts `-18,...,-13,17,18`, are identically
   zero as integer vectors. The other 26 columns have rank 26 over the field
   with 65537 elements. Their rational rank is therefore also 26, so all
   26 corresponding weights must vanish.
2. On those eight remaining shifts, the 63 scalarity constraints from input
   pair `(0,0)` and seven off-diagonal constraints from input pair `(0,1)`
   at output input index `y=7` form a 70 by 8 integer matrix of rank 8 modulo
   65537. Its rational kernel is zero, hence so are the remaining weights.

Combining the two blocks proves the statement: modular rank is a lower bound
on rational rank of an integer matrix, and every full scalar filter satisfies
these necessary equations. We do not assume that a modular nullspace is the
same as a rational nullspace.

## Reproduction and implementation boundary

```sh
python3 -I -B research/grade-nine-filter/verify.py > /tmp/grade-nine-filter.json
cmp /tmp/grade-nine-filter.json research/grade-nine-filter/verification.json
make verify
```

The first block's exact integer matrix hash matches the saved PR #46 matrix,
which used the original operator order. This checker uses the reverse order
for negative shifts and the original order for positive shifts. The inherited
two-order identity makes these the same operators; the hash gives an exact
finite cross-check for every entry of the first block. The reverse order
keeps negative-shift intermediate energies low and makes the targeted edge
checks practical. This is a change in evaluation schedule, not a new SAT
algorithm or a new claim about asymptotic costs.

The [saved report](verification.json) gives dimensions, field and matrix
hashes. The script checks both full-column ranks, zero columns, grade, source
pins and predecessor hash. It uses the standard library and the pinned PR #19
operator implementation; the second block is not independently implemented.
All-size input capacity, both directional ranks, entry generation, reduction,
precision, recursion, recovery and space must be paid for any proposed
improved algorithm. The baseline theorem remains owner-accepted, and the
selected result is unchanged.

## Next question and credit

Test a larger grade with the same energy-aware ordering and seek an all-size
structural argument or counterexample. A string of finite certificates alone
cannot settle asymptotic behavior. Alternative output-codebook and cubic-moment
questions are tracked separately in [issue #21](https://github.com/1337isnot1337/3-SAT/issues/21).

The charged operators and two-order identity are from
[PR #11](../charged-operator-moments/PROOF.md); deterministic asymmetric
codebooks are from [PR #19](../charged-asymmetric-crossing/PROOF.md); the
five-pair partial certificate is from [PR #46](../asymmetric-scalar-filter/README.md).
The base commit is `f2a153bac5f73c5dc2d77abe229655fb1fd954ec`. This work was
performed with substantial OpenAI Codex assistance. No independent review is
claimed.
