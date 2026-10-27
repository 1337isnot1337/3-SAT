# A precision barrier for parity-only shifted recovery

This is a scoped obstruction to the fixed-packet parity shortcut described in
the research discussion, not an audit of the accepted OpenAI theorem. The
source explicitly works with rational global coefficients and integral
shifted polynomials. The proposed shortcut incorrectly replaced the latter
by coefficientwise global integrality.

## 1. The actual diagonal polynomial

Fix `a>=1`, `L=2^a`, `alpha=2L`, and the accepted grid
`S={-L,...,L-1}`. Put

```math
 C(T)=\prod_{s\in S}(T-s),\qquad
 d_L(T)=\frac{C(T)}{C'(0)T}
       =\frac{\prod_{s\in S\setminus\{0\}}(T-s)}
                    {\prod_{s\in S\setminus\{0\}}(-s)}.
```

This is exactly `W_xx(T)` in `eq:tensor-cauchy`, for every slot `x`.
It satisfies `d_L(0)=1` and `d_L(t)=0` at every nonzero grid node.
Its leading coefficient has negative two-adic valuation: the denominator is
`(-1)^(L-1) L! (L-1)!`. Thus it is a rational polynomial, not in `Z_2[T]`.
It is even integer-valued at every integer, since

```math
 d_L(T)=(-1)^{L-1}\binom{T+L}{L}\binom{T-1}{L-1}.
```

Integer-valued polynomials need not preserve congruence modulo two.

For the specific proposed parameters `a=2`, `L=4`, `t=-2`, one has
`d_4(0)=1` and `d_4(-2)=0`. This already refutes the claimed even-node
congruence. More strongly, the coefficient of `z` in `d_4(-2+8z)` is
`-20/3`, and every coefficient is divisible by `4` in `Z_(2)`.
The odd denominator is harmless; the missing information is precision.

## 2. Exact contents of all nonzero shifted jets

For a rational polynomial define its two-adic content valuation to be the
minimum valuation of its nonzero coefficients. Fix `t` in `S` other than
zero and write `i=v_2(t)`. Then

```math
 \operatorname{content}_{v_2}\bigl(d_L(t+\alpha z)\bigr)=a+1-i.
 \tag{1}
```

To prove the lower bound, write its numerator as

```math
 \alpha z\prod_{s\in S\setminus\{0,t\}}(t-s+\alpha z).
```

Every nonzero difference has valuation at most `a`, so each linear factor
has coefficientwise valuation at least `v_2(t-s)`. The complete residue
grid gives `v_2(C'(t))=v_2(C'(0))`. Omitting the difference `t-0=t`
therefore leaves content at least
`a+1+v_2(C'(t))-v_2(t)-v_2(C'(0))=a+1-i`.

The coefficient of `z` is exactly

```math
 \frac{\alpha C'(t)}{t C'(0)},
```

whose valuation is `a+1-i`, proving equality. In particular the shifted
polynomial is integral, exactly as asserted by the accepted lemma, but all
of it vanishes modulo two. This includes every Taylor coefficient, not
only its value at `z=0`.

For every integer `q>=1`, let `G_q(T)=d_L(T)^q`. Its constant value at the
origin is one and its shifted content is exactly

```math
 \operatorname{content}_{v_2}\bigl(G_q(t+\alpha z)\bigr)
                    =q(a+1-v_2(t)).
 \tag{2}
```

Products give the lower bound. The first nonzero coefficient has degree
`q`, is the `q`th power of the preceding linear coefficient, and has
exactly this valuation. This proves equality without assuming that
cancellation cannot occur among later coefficients. Its jet coefficients
of degree less than `q` are zero even at infinite precision.

## 3. Consequence for a recovery interface

Suppose a recovery rule is given the local jets at all nonzero grid nodes,
with possibly different coefficient precisions `p_t`. If

```math
 p_t\le q(a+1-v_2(t))\quad\hbox{for every supplied node},
```

all those residues are zero for both `G_q` and the zero polynomial.
Nevertheless their origin parities are one and zero. No rule based only
on these data, the degree bound and shifted-integrality hypotheses can
always recover origin parity. This remains true with the *full* shifted
polynomials supplied rather than finite jets. Also, if every supplied jet
is truncated below degree `q`, no coefficient precision suffices for this
pair.

For all nonzero grid nodes, common precision `p<=q` is insufficient.
For just the source's retained levels `v_2(t)<u<=a`, common precision

```math
 p\le q(a+2-u)
```

is insufficient. At the proposed `a=2`, `t=-2` node the threshold is
`2q`, so even the complete polynomial modulo `2^(2q)` contains no signal
about this origin parity. These are necessary information conditions,
not sufficient recovery algorithms at one more bit.

## 4. These polynomials occur in valid bounded-degree networks

This is not merely an arbitrary rational-polynomial example. Consider a
packet with at least one real matched port, choose one such slot `x`, and
set the column unary tensors to fix `X_x=1` and all other real column
bits to zero. Set the row unary tensor at `x` to fix `Y_x=1`; at every
other real row port use `(1,1)`. All tensor values are zero or one and
all graph vertices have degree one.

In `eq:tensor-deformed-contraction`, sum over the unconstrained row bits.
Each gives `l_0(z)+l_1(z)=1`. Only the marked row remains, giving
`(W(T)X)_x=W_xx(T)=d_L(T)`. The original contraction is one. Repeating
this in `q` nonempty packets gives exactly `G_q(T)`.

More generally start with the graph of `M` independent unary-to-unary
edges. For any graph-only packing into `L`-slot packets, choose one real
matched slot in every nonempty packet and assign its unary values as above.
The packing depends on the graph, not these values. If the number of
nonempty packets is `q`, then `q>=M/L`. The resulting deformed contraction
is `G_q`, with degree at most `M(2L-1)` and all the source's shifted
integrality properties. Any empty packet contributes one.

Consequently, for **fixed** `L`, this recovery interface must sometimes
receive `Omega(M)` precision in at least one node and jets extending to
degree `Omega(M)`, even to recover one output bit. With full `L`-slot
packets, `M=qL` gives the explicit thresholds above. The construction is
uniform, with polynomial descriptions and constant-time entry routines.
It also has polynomial space and no random bits.

The examples themselves have a trivial count, so this is not a lower bound
on algorithms that inspect or simplify tensor descriptions. It is a
lower bound on the stated interpolation-data interface. It does not rule
out a tensor-aware shortcut, a different deformation, or a different
decision reduction.

## 5. A matching generic-polynomial precision obstruction

There is a stronger witness for the **generic Hermite recovery interface**.
Fix `1<=u<=a`, `M>=2u`, set `h=floor(M/(2u))`, and put

```math
 q(i)=h\max(0,u-i),\qquad D_i=L/2^i,\qquad
 H(T)=\prod_{t\in S\setminus\{0\}}
                 \left(\frac{T-t}{-t}\right)^{q(v_2(t))}.
 \tag{3}
```

One has `H(0)=1`. Its degree is

```math
 \sum_{i=0}^{u-1} D_i h(u-i)<2hLu\le ML\le M(2L-1).
```

At a node of valuation `i`, the exact content of `H(t+alpha z)` is

```math
 c_i=q(i)(a+1-i)+
       D_i\sum_{j=1}^{a-i}\frac{j}{2^j}\bigl(q(i)-q(i+j)\bigr).
 \tag{4}
```

Here is a direct derivation. The root at `t`, if present, contributes
`q(i)(a+1-i)`. Roots of lower valuation contribute zero to the content
after dividing by their normalizing `-t` factors. At each higher relative
level `j`, there are `D_i/2^j` roots of valuation `i+j`, contributing
`-j q(i+j)` each, and the same number of roots of valuation `i` at
difference valuation `i+j`, contributing `j q(i)` each. These exhaust
the remaining contributions. After factoring these powers of two, the
first nonzero Taylor coefficient, of degree `q(i)`, is a unit. Hence the
content is exact, not just a valuation bound for the node value.

For inactive levels `i>=u`, (4) is zero. At the origin, all normalized
factors of `H(alpha z)` have integral coefficients and constant one.
At active levels, every term in (4) is nonnegative. Thus `H` is integral
on **every** shifted grid disk, including the inactive nodes and origin:
it satisfies the actual hypotheses of `lem:tapered-hermite`.

Moreover, for every active level `i<u`,

```math
 \frac{M D_i}{8u}\le c_i\le\frac{4M D_i}{u}.
 \tag{5}
```

For the lower bound retain `j=1`: `q(i)-q(i+1)=h`, and
`h>=M/(4u)`. For the upper bound use
`q(i)-q(i+j)<=hj` and `sum_(j>=1) j^2/2^j=6`. Also, with
`v=a-i>=1`, `q(i)(a+1-i)<=h v(v+1)<=2h 2^v=2hD_i`.
The last elementary inequality follows by induction, or by checking
`v=1,2` and the successive ratios for `v>=2`. Consequently
`c_i<=8hD_i<=4MD_i/u`.

It follows that even recovering one output bit for arbitrary polynomials
in this interface cannot use precision uniformly below a fixed constant
times `MD_i/u` at **all** retained nodes: for instance,
`p_t<=floor(MD_i/(8u))` makes every complete active-node polynomial zero
for both `H` and the zero polynomial. The origin parities differ. Any
successful generic recovery must exceed the witness's threshold at at
least one active node; this does not require that every node individually
receive that much precision.

The source's `O(MD_i/u)` precision scale is therefore order-sharp for this
generic retained-node recovery interface, already for parity. The argument
allows arbitrary nonlinear processing of all the supplied jets: they are
identical for the two polynomials. In particular, cancellation between
separately nonzero jets cannot rescue these all-zero data.

This is stronger than optimization of a loss functional, but its scope is
still important: (3) is a realizable rational polynomial satisfying the
generic recovery assumptions; an efficient Boolean-tensor realization of
this entire growing-packet family is **not established**. Section 4 gives
the separate, actual-network witness and its `M/L` scale. An algorithm
that exploits a smaller class of deformed contractions or queries additional
valuation levels is not excluded by (5).

## 6. Full cost implication and open escape

The proposed constant choice `r=64,a=2,L=4,t=-2` does not allow the
accepted recurrence to run at precision one by discarding recovery and
modes. Locality holds at the node, but origin parity is different there.
Keeping the correct recovery interface requires growing precision and
jet order on the displayed family. For fixed `u` the accepted mode-count
envelope is `exp(O(M/sqrt(u)))=exp(O(M))`, so its existing analysis gives
no subexponential improvement, much less polynomial time. An upper
envelope is not a lower bound against a new mode algorithm.

The matching generic obstruction in Section 5 closes a reduction of the
`MD/u` scale based only on the source's degree and shifted-integrality
assumptions. The actual-network lower bound is weaker at growing `L`,
leaving a precise avenue: find a tensor-specific restriction excluding (3)
and use it for recovery with fewer bits. Correctness still needs every
mode, child call, entry, description, leaf and outer reduction charged.

No SAT improvement follows from this package. The accepted result stays
`alpha=1/2`. Valiant--Vazirani isolation cannot repair an incorrect parity
oracle; no claim about its separate reduction is needed here.

## Sources and credit

The source is OpenAI, *The Exponential Time Hypothesis is False*, revised
October 25, 2026, commit `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`.
The relevant frozen file is
[quantitative-contraction.tex](../../upstream/openai-eth-2026/build/quantitative-contraction.tex),
labels `eq:tensor-cauchy`, `eq:tensor-deformed-contraction`,
`lem:tensor-integrality`, `lem:tapered-hermite`, and
`eq:tensor-partition-count`. The claim does not reinterpret or dispute its
accepted theorem. [SOURCES.json](../../SOURCES.json) preserves attribution,
license and exact hashes.

The generic precision witness is complementary to
[PR 1](https://github.com/1337isnot1337/3-SAT/pull/1), head
`8790b8e14e08ea14f75c2bd6eecfdbc70fe97770`, which optimizes a taper loss
functional and leaves cancellation between jets open. Here actual
polynomials with complete vanishing data give an information obstruction
for arbitrary recovery within the stated generic interface. No broader
tensor-algorithm lower bound follows.

The motivating failed shortcut and its initial refutation were supplied
in the user's research transcript. This package adds the exact all-node,
all-jet content formula, its powers, network realization and recovery-data
precision bound. No priority, independent review or formal proof is claimed.
Substantial OpenAI Codex assistance; new material is Apache-2.0.
