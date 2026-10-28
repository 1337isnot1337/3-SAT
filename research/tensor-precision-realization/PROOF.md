# Shift-resistant Boolean unary packets

This is an author-checked information obstruction for a specified packet
and local-data interface. It is not an algorithmic lower bound and does not
realize the tapered polynomial in the predecessor's Section 5.

## Claim

There is a deterministic polynomial-time construction, in `L`, of a binary
word `b` of each power-of-two length `L >= 1024` such that, for every
`t in {-L,...,L-1} \ {0}`,

```
N_t = #{x in [0,L): b_x != (b_{x+t} if 0 <= x+t < L else 0)} > L/4.
```

Take `q` full `L`-slot packets, `M=qL` independent edges, and one unary
row and column tensor on each edge, both equal to the indicator of the
corresponding bit of `b`. The canonical entries are 0 or 1, all degrees
are one, and the tensor network's undeformed contraction is 1. At each
nonzero node, the entire shifted deformation polynomial is coefficientwise
divisible by `2^ceil(qL/4)` over the two-adic integers. Thus its complete
local jets at all nonzero nodes modulo that power of two coincide with
those of the zero network, although the origin parities differ. All nodes
and all jet orders are supplied; a recovery rule that sees only these
residues cannot distinguish the two networks.

The result is for this full-packet embedding. It does not assert that an
arbitrary graph-only packing produces full packets, or that a recovery
procedure inspecting tensor descriptions cannot distinguish the networks.
The claim permits any admissible full-packet embedding with these same slot
assignments, including a balanced embedding. The input values can be set
after the graph-only embedding has been fixed.

## Word construction

Choose independent uniform bits `B_x`. Extend the word by zero outside its
range. For a fixed nonzero `t`, each of the `L` disagreements has mean
`1/2`, so `E N_t=L/2`. Changing one bit affects at most two comparisons.
The bounded-difference exponential moment estimate gives, for `eta>0`,

```
E exp(-eta N_t) <= exp(-eta L/2 + eta^2 L/2).
```

This follows from the Doob martingale and Hoeffding's lemma applied to
increments with range at most 2. Put `eta=log(8/7)` and

```
Z(b) = sum_{t != 0} (8/7)^(L/4) (7/8)^N_t.
```

There are `2L-1` terms. Since `1/8 < eta < 1/7`,

```
E Z <= 2L exp(-L/32 + L/98) < 1,   L >= 1024.
```

The last inequality holds at 1024 and its left side decreases thereafter.
Assign bits in order, choosing the value with smaller conditional `E Z`.
The final `Z` is below 1, so every summand is below 1 and every `N_t>L/4`.

This is a uniform deterministic polynomial-time construction. For a fixed
`t`, the interactions connect `x` and `x+t`; their graph is a union of
paths. The weight `(7/8)^N_t` factors into binary edge weights and unary
boundary weights. A two-state transfer on each path computes the exact
conditional expectation in polynomial time. Its rational numerators and
denominators have `O(L)` bits. There are `L` choices, two trials per
choice, and fewer than `2L` shifts; a straightforward implementation uses
`O(L^3)` arithmetic operations on `O(L)`-bit integers. This construction
is evidence of uniformity, not a practical performance claim. The checker
compares this transfer with exhaustive enumeration for small paths.

## Deformation calculation

Let `C(T)=product_{s=-L}^{L-1}(T-s)` and `alpha=2L`. The source's
`W_xy(T)` is `C(T)/(C'(0)(T-(y-x)))`. For every node `t`,
`C'(t)/C'(0)` is a two-adic unit: the differences from `t` to the other
`2L-1` grid points form all the nonzero residue classes modulo `2L`, as do
the differences from 0. For every `s != t`, `v_2(t-s)<=a` with
`L=2^a`; hence `alpha/(t-s)` is even. Factoring each shifted Cauchy entry
at `t` gives

```
W_xy(t+alpha z) = 1[y-x=t] * unit + 2 Z_2[z],
```

where the displayed unit is the constant `C'(t)/C'(0)` and is odd. When
`y-x != t`, the missing root gives a factor `alpha z/(t-(y-x))`, also
coefficientwise even. This proves the congruence for the entire polynomial,
not only its value at `z=0`.

The column tensors fix `X=b`. The row tensor at `x` fixes `Y_x=b_x`,
so the packet polynomial is

```
P_b(T) = product_x l_{b_x}(sum_y W_xy(T) b_y),
 l_1(z)=z,  l_0(z)=1-z.
```

At a nonzero shifted node, each factor is an integral polynomial; if
`b_x` differs from the zero-extended `b_{x+t}`, its entire polynomial
is even. Thus `P_b(t+alpha z)` is divisible by `2^N_t`. At the origin
`W(0)=I`, so `P_b(0)=1`. The `q` independent packets multiply their
polynomials, giving divisibility by `2^(qN_t)` and hence by
`2^ceil(qL/4)`. A network with one unary tensor identically zero has
identically zero deformation and origin parity zero.

## Cost and limits

The word construction uses polynomial time and space in `L`; writing the
`2M` unary tables uses `O(M)` bits once the word is available. The
construction needs no randomness after derandomization, no dense tensor
entries, and no preprocessing exponential in `L`. Directly enumerating the
`2^M` assignments is unnecessary. These costs describe the witness,
not a proposed faster SAT algorithm. No reduction branches, queries, modes,
recursive calls, or recovery algorithm are replaced or claimed cheaper.

The predecessor's actual-network witness gives about `M/L` times a node
valuation factor; this packet construction gives at least `M/4` at every
nonzero node. For the accepted growing parameters and small valuation `i`,
the generic taper witness has `Theta(M D_i/u)` content, potentially much
larger than `M`; this result does not attain that scale. It does not show
that the specific Section 5 polynomial is tensor-realizable, does not prove
that every packing admits the same bound, and does not rule out tensor-aware
recovery or an alternative deformation.

The source is the frozen OpenAI `quantitative-contraction.tex`, labels
`eq:tensor-cauchy`, `eq:tensor-deformed-contraction` and
`lem:tensor-packets`, commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`.
The predecessor is `research/parity-recovery-precision` at base
`630041c9da3a26edb8c8f59d5f8a4132a188c8bd`. The bounded-difference estimate
and conditional expectation are standard; no novelty claim is made for them.
