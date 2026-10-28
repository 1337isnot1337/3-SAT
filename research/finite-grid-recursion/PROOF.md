# Finite-width corrections in a thin-grid cost recurrence

## Model and theorem

Fix integer `p>=2`, `q_0>=2`, `u>0` and `v_0>0`. Put
`q_n=q_0 p^n` and

    a_n=(p-1)/(p q_n-1), b=(p-1)/p, c=1/p,
    T_n(v)=max_{x,y>=0,x²+y²<=1}
             min(u[a_n+(1-a_n)b x], v(1-a_n)[c+b y]),
    v_{n+1}=T_n(v_n).                                  (1)

These are the exact normalized *straight-edge and rectangle multiplicity
coefficients* from PR 61, combined with its ideal continuous quarter-disk
factor-cost relaxation and a fixed row-child coefficient u. The sequence of
ideal grid sizes is `p q_n`. It does not follow that actual recursive child
algorithms satisfy (1); a full algorithm would need a valid grouping and
all omitted costs.

**Theorem.** The positive iterates of (1) obey

    n v_n² -> b u²,
    1/v_{n+1}² - 1/v_n² -> 1/(b u²).                  (2)

Hence `v_n ~ u sqrt(b log p / log(p q_n))`. The same proof applies to any
finite integer sequence `q_n>=2` for which `sum a_n<infinity` and
`n^(3/2) a_n -> 0`; the displayed geometric sequence satisfies both.
This is an exact result for the **model**, not a SAT runtime or lower bound.

## Proof

Let

    T(v)=max_{x,y>=0,x²+y²<=1} min(u b x, v(c+b y)).

The source-independent elementary analysis in PR 101 proves
`0<T(v)<v` for `v>0`, continuity, and for small v

    T(v)=v-v³/(2 b u²)+O(v⁵),
    1/T(v)²-1/v²=1/(b u²)+O(v²).                     (3)

For completeness, the expansion follows by equalizing the increasing row
cost `u b x` and decreasing column cost `v(c+b sqrt(1-x²))` on the quarter
circle. Their intersection has `x=v/(u b)+O(v³)`.

For every v, monotonicity in the added row offset and the 1-Lipschitz
property of min give

    (1-a_n) T(v) <= T_n(v) <= (1-a_n)T(v)+u a_n,     (4)
    T_n(v) <= (1-a_n)v.                               (5)

The minimax is over a fixed compact set, and (4) implies `T_n` converges
uniformly to T on bounded v-intervals. By (5), `v_n` decreases to a limit;
that limit must be a fixed point of T and hence is zero. All v_n are
positive, for example by taking both x and y positive.

We next control the inverse-square growth without presuming its conclusion.
Write `w_n=1/v_n²`. For all sufficiently large n, (3), (4), and `a_n -> 0`
give

    w_{n+1} <= (1-a_n)^(-2) (w_n+C)
              <= (1+4a_n)(w_n+C)                    (6)

for a fixed C. Because `sum a_n<infinity`, the products of `(1+4a_n)`
are bounded. Iterating (6) yields `w_n=O(n)`, so `v_n >= d/sqrt(n)` for
some `d>0` and all large n.

By (4), `|T_n(v_n)-T(v_n)| <= a_n(u+v_0)`. Both arguments of the inverse
square are at least `v_n/2` eventually, by (3) and (4). The mean-value
inequality therefore gives

    |1/T_n(v_n)² - 1/T(v_n)²| = O(a_n/v_n³)
                                 = O(n^(3/2) a_n) -> 0.

Combining this with (3) proves the increment limit in (2). Cesaro averaging
then gives `w_n/n -> 1/(b u²)`, proving the first limit. Since
`log(p q_n)=n log p+O(1)`, the stated equivalent follows.

## Scope

This result removes the repeated-limit gap in PR 101 for this particular
finite-q *cost recurrence*. It does not prove the quarter-disk upper bound
is tight for actual pieces, that finite rounding and partition errors are
summable, or that an algorithm can group both children while keeping fixed u
and the stipulated sizes. It omits piece enumeration, straight-edge local
work, factor computation, precision, recovery, dense reductions and space.
It neither improves nor lower-bounds general 3-SAT; the selected OpenAI
result remains unchanged. A changed piece family or structured child-table
interface lies outside the model.
