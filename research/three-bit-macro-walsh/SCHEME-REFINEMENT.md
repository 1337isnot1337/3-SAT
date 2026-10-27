# Closing the coarse scheme before refining it

## 1. A local dual closes the whole coarse class

For the three-class matrix C and weights `(1,35,28)` in
[CONSTRUCTION.md](CONSTRUCTION.md), the local function

```math
 h=(0,1/35,-1/28)
```

satisfies `Ch=8h` and has weighted pairing two with the target
`q=(1,1,-1)`. Tensor h across R macros. Its transform is `8^R h` and its
pairing with the target is `2^R`, so some summand in any decomposition of
the crossing coefficient target has nonzero pairing with it.

This tensor dual is supported only on class patterns with no zero macro.
Every such pattern contains at least `28^R` actual Pauli labels. Therefore
any function constant on each macro-class pattern with support smaller
than `28^R` pairs to zero. The same holds if its transform has support
smaller than `28^R`, by Walsh self-adjointness. Consequently one same piece
in every such decomposition must have

```math
 |\operatorname{supp}f|\ge28^R,\qquad
 |\operatorname{supp}\widehat f|\ge28^R.
```

This does not even require permutation symmetry between macros or a bound
on the number of summands. It permits cancellations and arbitrary
characteristic-zero coefficients. Its necessary combined bit rate is
`2R log2(28)`, above the target `6 sqrt(2) R`: indeed `28^2>2^9` gives
`log2(28)>9/2>3 sqrt(2)`. Thus the coarse class cannot improve the accepted
piece rate. The finite screen was not needed to extrapolate this conclusion.

## 2. A specific refinement changes the premise

Use `F_8=F_2[t]/(t^3+t+1)`. The cubic is irreducible because it has no
root in F2. Identify a three-bit a with the polynomial-basis field element
A. Identify b with the trace-dual field element B so that
`a dot b=Tr(A B)`. The trace pairing is nondegenerate; in this fixed field
the map is also constructed and checked exhaustively.

Split the 64 labels into six classes:

1. A=B=0;
2. A=0, B nonzero;
3. A nonzero, B=0;
4. A and B nonzero with AB=1;
5. A and B nonzero with Tr(AB)=0;
6. A and B nonzero with Tr(AB)=1 and AB different from 1.

Their sizes are `(1,7,7,7,21,21)` and their target signs are
`(1,1,1,-1,1,-1)`. Multiplication `(A,B)->(uA,u^-1 B)` and simultaneous
Frobenius `(A,B)->(A^2,B^2)` preserve the symplectic character and these
classes. They are transitive on each class: nonzero products other than
one have Frobenius orbits of size three, separated by trace. Hence the
Walsh transform closes on six class values.

The refined table is computed by all 4,096 actual characters, not by
assuming it inherits the old rank envelope. Its zero-output row gives
class sizes; the row with AB=1 has coefficients `-3,9` on the final two
classes. No local eigenvector supported only on those two 21-element
classes can survive: the zero-output equation requires `x+y=0`, while
the AB=1 equation requires `-3x+9y=0`, forcing x=y=0.

A local dual supported on the large classes together with its transform
can be projected to the positive eight-eigenspace by `h+hat h/8`, without
losing a nonzero target pairing. Thus these two equations exclude the
entire corresponding local support-dual test at threshold 21.

Thus the local support-dual threshold of 21 is unavailable in this refined
scheme. The old three-class eigenvector still exists after refinement,
but now has nonzero values on seven-element classes, giving only the
weaker threshold seven. This defeats that particular coarse-class
obstruction. It does not certify a better piece rate or exclude a different
global dual.

## 3. Registered screen and subsequent stopping result

For R=1,...,5 use the six-class symmetric-power transform and weighted
type counts. Its dimension is `(R+5 choose 5)`. Check the actual transform,
exact target, factors and support costs before claiming any trend. The
success target remains a proved all-size cost below
`6 sqrt(2) R+O(log R)`, with polynomial piece count and integer heights.
The screen completed with worst combined bit counts 8,18,27,39,50. No
eventual rate is inferred from these five values. The separate four-block
dual in [BLOCK-BARRIER.md](BLOCK-BARRIER.md) now closes the entire refined
family by tensorization. The local threshold-seven test was too weak.
Source pins and predecessor credit
remain those in README.md. All written arguments are AI-assisted and
await independent review.
