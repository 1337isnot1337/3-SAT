# Weighted decision and sparse parity queries

This changes an interface in the accepted construction. It does not audit the
OpenAI theorem and does not claim a better full 3-SAT exponent. The all-size
arguments below are author-checked, without independent review.

## 1. A nonzero polynomial for a nonempty solution set

Let `S` be a set of Boolean assignments on `N` variables, and let `F` be a field
of characteristic two. Define

```math
 Z_S(R_1,\ldots,R_N)=\sum_{x\in S}\prod_{v:x_v=1}R_v.
```

Distinct assignments give distinct monomials. Thus `Z_S` is identically zero
if and only if `S` is empty, and its degree is at most `N`. If `|F|=Q` and the
weights are independent and uniform, a nonzero polynomial of degree at most
`N` vanishes with probability at most `N/Q`.

For completeness, induct on the number of variables for this last bound.
Write a nonzero polynomial as a polynomial of degree `d` in its last variable,
with nonzero leading coefficient of total degree at most `D-d`. The leading
coefficient vanishes with probability at most `(D-d)/Q`. Otherwise there are
at most `d` roots of the last-variable polynomial. A union bound gives `D/Q`.

Choose `Q=2^e>=6N`. Exactly `eN` independent uniform bits specify the weights;
there is no rejection loop. The resulting detector has no false positive for
an empty `S` and false-negative probability at most `1/6`. Variables absent
from all equations can first be discarded for decision. The empty system is
immediately satisfiable, and a constant-one equation immediately unsatisfiable.

For equations `P_i(x)=0` over F2, their Boolean solution indicator is exactly

```math
 \prod_{i=1}^a(1+P_i(x))
```

over `F`. This uses no integer parity lift, large precision or truncation in
the original indicator. Each factor has degree at most `k`.

## 2. Incidence encoding with degree ka

Normalize monomials to squarefree support and cancel duplicates over F2.
Give each test-variable incidence its own symbol `z_iv`; then set
`C_i(z_i)=1+P_i(z_i)`. Incidences belonging to different tests are disjoint,
so `prod_i C_i` is multilinear in the incidence symbols and has degree at
most `K=ka`.

The source's subset-index network works with this product. Enumerate the
pairwise selected-incidence counts `d_gh`; for a group pair use
`ceil(log2 binom(N_gh,d_gh))` wires. Invalid codes contribute zero. Test-group
entries multiply coefficients `[z_i,S_i] C_i`, each of which is a 0/1 lookup
in the supplied monomial list. Variable-group entries are now

```math
 \prod_{v:b_v>0}r_v\prod_{v:b_v=0}(1+r_v),
 \qquad b_v=|\{i:v\in S_i\}|.
```

This follows by summing `r_v^{x_v} x_v^{b_v}` over `x_v=0,1`. Hence the sum
of the encoded contractions equals `Z_S(r)` exactly. The wire bound is

```math
 M\le J^2+K\log_2\!\left(\frac{\mathrm e(N_0+K)}K\right),
```

with `N_0` the total incidence count. The changed degree and coefficient
lookup are real interface savings. They do not eliminate the entropy term.

## 3. Fit the finite field into the accepted ring without enlarging s

The accepted theorem is stated for
`(Z/2^P0 Z)[V]/(V^ell)`, not arbitrary finite-field inputs. Use `P0=1`.
Let `f(V)` be the irreducible degree-e polynomial defining `F`. In a network
with `v` vertices, replace each field-valued tensor entry by its canonical
polynomial representative of degree below `e`, separately for that entry.
Run the contraction over

```math
 (\mathbb Z/2\mathbb Z)[V]/(V^\ell),
 \qquad \ell=v(e-1)+1.
```

Every product of `v` entries has degree below `ell`, so truncation loses
nothing. Reduce the resulting polynomial modulo `f` after contraction.
Since reduction modulo `f` is a ring homomorphism, this gives the exact field
contraction. This argument does not suppose canonical entry lifts are ring
homomorphisms. In the application `v=O(J)` and `e=O(log a)`, so
`ell=O(J log a)=O(s)` for the parameters below.

An irreducible degree-e polynomial can be found deterministically by enumerating
the `2^e` monic candidates and testing divisibility by monic polynomials of
degree at most `e/2`. Here `2^e` is polynomial in the active input size, so
this construction and all field arithmetic have polynomial bit cost.

## 4. A constraint-parameter evaluator

Fix `k`. Suppose there are at most `a` equations, each of degree at most `k`
and with at most `T` monomials, where `1<=T<=a^(1/10)`. All declared variables
are Boolean, and absent variables are discarded for decision. The number of
active variables is at most `kaT`. For weights in a characteristic-two field
with `e=O_k(log a)` bits per element, the weighted partition function is
computable deterministically in

```math
 \operatorname{poly}_k(\text{input})\,
 2^{O_k(a\log(T+2)/\sqrt{\log a})}
```

bit operations and polynomial space, for all sufficiently large `a`. The
following explicit fallback makes the procedure uniform: if the numerical
conditions required by the contraction theorem fail, enumerate the at most
`kaT` active Boolean variables. With fixed `k` and `T<=a^(1/10)`, only a
bounded range of `a` fails the asymptotic conditions.

Here is the full construction and cost argument. Let
`J=ceil(a^(1/4))`, `D*=ceil(T a^(1/20))`, and
`s=ceil(a log2(T+2))`. Fix in all ways every variable occurring in more than
`D*` tests. There are at most `kaT/D*<=k a^(19/20)` such variables.
Each branch contributes its fixed-variable weight times its free-variable
partition function. Substitute, normalize, and remove trivial equations.
Continue using the original `a,T` as upper bounds.

Partition tests greedily into `J` groups by incidence load, and do the same for
free variables. A greedy least-loaded-bin assignment makes each test-group
load at most `N_0/J+kT` and each variable-group load at most `N_0/J+D*`.
Thus both are `O_k(a^(3/4)T+T a^(1/20))=O_k(a^(17/20))`.
Use the incidence construction from Section 2. Its maximum tensor degree is
at most that load, hence eventually at most `ceil(s^(9/10))`.
Its number of wires is `O_k(a log(T+2))=O_k(s)`.

There are at most `(ka+1)^(J^2)` degree arrays. Their logarithmic cost is
`O_k(sqrt(a) log a)`. Tensor entries and combinatorial decoding are polynomial
time: direct monomial lookup on the test side, field products on the variable
side. Descriptions have polynomial length. Section 3 uses `2J` vertices and
`ell=O_k(a^(1/4) log a)=O_k(s)`. The accepted contraction theorem therefore
applies, with exponent `O_k(s/sqrt(log s))`. Since `T<=a^(1/10)`,
`log s=Theta(log a)`.

The branch and array exponents `O_k(a^(19/20)+sqrt(a) log a)` are lower order
than `a/sqrt(log a)`. Field construction, weights, entries and postprocessing
are polynomial. Traverse branches and arrays sequentially to preserve
polynomial space. This proves the evaluator statement.

Applying Section 1 gives a one-sided randomized decision algorithm for these
sparse polynomial systems with the same worst-run time. For the source's
`a=O(n)`, `T=(log n)^O_k(1)` queries, retain an `O(n)` value of `a` even if
fewer rows happen to remain. The resulting envelope is still
`2^{O_k(n log log n/sqrt(log n))}`.

## 5. A sparse-hash decision wrapper without greedy count queries

Take a sparsified CNF leaf with `n` variables and `m` nontrivial clauses.
Use the accepted `lem:sparse-checks` to obtain the initial check matrix and
its guarantee: any nonzero violation vector surviving those checks has weight
at least `m/P`, with `P` polylogarithmic in `n` in the source regime.

Pad the index universe to `m'=2^ceil(log2 m)` with zero violation coordinates.
Each extra row is generated by `2P` independent uniform indices in `[m']`
and independent uniform coefficient bits. Each index uses exactly
`ceil(log2 m)` random bits. Since `m'<=2m`, a surviving nonzero vector is hit
with probability at least `1-(1-1/(2P))^(2P)>1/2`; conditional on a hit,
one independent coefficient makes the row parity uniform. Thus each row
rejects that vector with probability at least `1/4`.

Index the sparsification leaves by `j=1,2,...`, and put
`b_j=ceil(log2(j+1))`. Append

```math
 t_j=8(n+b_j+1)
```

independent rows. Every true satisfying assignment always survives. For a
fixed leaf, a union bound over at most `2^n` assignments bounds the probability
that any false assignment survives by

```math
 2^n(3/4)^{t_j}
 < 2^{-2n-3}2^{-3b_j}
 \le 2^{-2n-3}(j+1)^{-3},
```

using `(3/4)^8<1/8`. For `n>=1`, summing over every leaf is less than `1/32`.
The source's sparsification bound implies `log j=O_k(n)` at every leaf, so
`t_j=O_k(n)`. The equations still have fixed degree and polylogarithmic
monomial counts. All random-bit reads and row expansion have worst-case
polynomial cost per leaf. There is no unbounded rejection sampling.

Evaluate the weighted fingerprint of the resulting system using a field of
size at least six times its active variable count, and OR the answers over
leaves. On an unsatisfiable formula the probability of any false positive is
less than `1/32`, since a false positive requires a surviving false assignment.
For a satisfiable formula, fix any one satisfiable leaf independently of the
randomness. Hashing never deletes its true solutions, and, conditional on
the chosen hashes, its weighted polynomial is nonzero. Independent weights
miss it with probability at most `1/6`. Thus the full algorithm meets the
per-input success requirement and has the stated worst-run time.

This replaces all greedy candidate count queries with one randomized weighted
evaluation per leaf. It does not replace the accepted initial sparse-code
construction or the sparsification tree. Both remain charged, as do the
high-incidence branches, degree arrays, field embedding and contraction.
Their full composition retains the accepted general exponent and alpha.

## Open objective

To improve the bound, the entropy in the monomial wire encoding or the
contraction exponent must fall. Grouping equations might reduce the number
of incidences, but can raise coefficient-evaluation cost and maximum tensor
degree. Those are explicit obligations for the next step, not assumptions
silently included in this checkpoint.
