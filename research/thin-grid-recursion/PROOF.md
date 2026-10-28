# Iterating the limiting thin-grid cost model

## Setup and statement

Fix a real `p>=2`, `b=(p-1)/p`, `c=1/p`, and `u>0`. Define

    T(v) = max_{x,y>=0, x²+y²<=1} min(u b x, v(c+b y))
    v_0>0,  v_{n+1}=T(v_n).                            (1)

This is the ideal quarter-disk minimax of PR 61 in the **limit** where a
`p`-row by `q`-column grid has `q -> infinity`, its normalized straight-edge
offsets are `(0,c)`, and the bounded row child has fixed coefficient u.
It is a mathematical recurrence, not an assertion that a finite-q algorithm
can apply the limit independently at every step. Here `p` may be real for
the algebra; a grid interpretation needs integer p.

**Theorem.** For every starting `v_0>0`, the iterates satisfy

    v_n -> 0,          n v_n² -> b u²,                  (2)
    1/v_{n+1}² - 1/v_n² -> 1/(b u²).                  (3)

Thus the vanishing per-step reduction accumulates to `v_n ~ u sqrt(b/n)`.
If one additionally assigns *ideal* root size `K_n=K_0 p^n`, then
`v_n ~ u sqrt(b log p / log K_n)`. This is not a 3-SAT runtime bound.

## Proof

The maximum in (1) exists by compactness. For `v>0`, it lies strictly
between 0 and v. Positivity follows by choosing x,y both positive. The
column cost is at most v; equality would require `y=1`, hence `x=0` and
zero row cost. Therefore `v_n` decreases to a nonnegative limit. The
function T is continuous, since the objective is uniformly continuous in
v on a fixed compact set; if the limit were positive it would be a positive
fixed point, contradicting `T(v)<v`. Hence `v_n -> 0`.

For sufficiently small v, `u b > v c`. Along the quarter circle
`y=sqrt(1-x²)`, the row cost `u b x` increases from zero, while the column
cost `v(c+b sqrt(1-x²))` decreases from v to `v c`; their unique intersection
`x(v)` is the maximizer. Its equation is

    u b x = v(c+b sqrt(1-x²)).                          (4)

Since `c+b=1`, equation (4) gives `x <= v/(u b)` and, by Taylor expansion
with constants depending on the fixed u and p,

    x(v) = v/(u b) + O(v³),
    T(v) = v - v³/(2 b u²) + O(v⁵).                   (5)

The Taylor remainder is uniform for v in a sufficiently small interval;
all constants are finite because `b,u>0`. Therefore

    1/T(v)² - 1/v² = 1/(b u²) + O(v²).

Applying this to the iterates proves (3), since they tend to zero. The
Cesaro mean of the increments in (3) converges to `1/(b u²)`, so
`1/v_n² ~ n/(b u²)`, proving (2).

## Why the scope matters

For finite integer p,q, PR 61 has extra offsets
`a=(p-1)/(pq-1)`, `c_q=(q-1)/(pq-1)` and
`b_q=(p-1)(q-1)/(pq-1)`. These converge to `0,c,b` as `q -> infinity`;
equation (1) discards their finite-q errors at every step. No uniform error
propagation theorem is asserted here, and taking a limit separately at each
level does not prove the outcome of any finite recursive schedule.

The objective is the worst-case *certificate* over a continuous upper
factor-cost envelope; actual crossing pieces could have smaller or correlated
costs. No rectangular grouping, leaf feasibility, branching, entries,
precision, recovery, memory, dense reduction or complete SAT algorithm is
constructed. A different interface or factor curve may change the recurrence.
The owner-accepted result, including alpha 1/2, stays unchanged.
