# Residue-class witnesses for shifted parity recovery

This is an information obstruction for a specific recovery interface. It is
not a lower bound for counting or SAT algorithms, which can inspect these
particularly simple tensor inputs. The accepted theorem is a premise, not an
object of review. The construction uses its Cauchy deformation and canonical
Boolean lifts, from `eq:tensor-cauchy`, `eq:tensor-deformed-contraction`, and
`lem:tensor-integrality` in the frozen quantitative contraction source.

## Claim

Let `a >= 1`, `L=2^a`, `1 <= u <= a`, `alpha=2L`, and let `M >= 1` real
matched edges be assigned arbitrary packet slots in `0,...,L-1`. Each real
edge has one row and one column endpoint in the same slot. Suppose packet
`j` has occupied slot set `P_j` of size `m_j`. Put

```math
 K=\sum_j \max_{0\le r<2^u}|\{x\in P_j:x\equiv r\pmod {2^u}\}|.
```

There is a graph of `M` independent unary-to-unary edges, with canonical
`0/1` tensor entries chosen after this graph-only packet assignment, whose
unshifted contraction is `1` and whose deformed contraction `F` satisfies,
for every `t` in `{-L,...,L-1}` with `i=v_2(t)<u`,

```math
 F(t+2Lz)\in 2^{K(a+1-i)} z^K \mathbb Z_{(2)}[z].
```

In particular `K >= ceil(M/2^u)`. The zero network produces identical full
shifted data modulo `2^{p_t}` at all such nodes whenever
`p_t <= K(a+1-i)`, although its original contraction has opposite parity.
This remains true for any recovery rule, linear or nonlinear, using only
those data. Even infinite coefficient precision cannot distinguish the pair
if all jets are cut off strictly below degree `K`.

The statement is conditional on the specified packet assignment. The
construction works for **every** assignment, including sparse and empty
packets, provided the assignment is independent of the unary table values.
It does not assume that an implementation packs every slot. It does not say
that an algorithm with access to the original tensors cannot distinguish the
inputs, or that the shifted data alone are sufficient for recovery above the
stated precision.

## Proof

For each packet choose a most populated slot residue class modulo `2^u`,
and let `R_j` be the occupied slots in that class. On every column endpoint
in `R_j`, use the unary tensor that fixes the bit to one; on all other real
column endpoints fix it to zero. On each row endpoint in `R_j`, fix the bit
to one; at every other real row endpoint use the unary table `(1,1)`.
The original contraction is exactly one: each real edge matches its row and
column bit. All tensor entries are canonical zero or one, and each vertex
has degree one.

With `W_xy(T)` as in the source, column assignments are fixed to the
indicator of `R_j`. Summation over each unconstrained row bit gives
`l_0(z)+l_1(z)=1`. Therefore

```math
 F(T)=\prod_j\prod_{x\in R_j}\left(\sum_{y\in R_j} W_{xy}(T)\right).
 \tag{1}
```

There are `K` factors. At `T=0`, `W(0)=I`, so each is one. Since the
`2^u` residue classes partition each occupied set, the largest has at least
`ceil(m_j/2^u)` slots. Summing gives `K >= ceil(M/2^u)`.

Fix a retained node `t` and let `i=v_2(t)<u`. If `x,y` are in the same
chosen class, `s=y-x` is divisible by `2^u`; hence `s != t` and
`v_2(t-s)=i`. The expression

```math
 W_{xy}(T)=\frac{\prod_{q\in S\setminus\{s\}}(T-q)}{C'(0)}
```

has a factor `T-t`. The grid is a complete residue system modulo `2L`;
the valuations of `C'(t)` and `C'(0)` agree. In the polynomial
`W_xy(t+2Lz)`, each factor other than `T-t` is coefficientwise divisible
by its value at `t` in the two-adic valuation. Removing the `s` factor
from `C'(t)` therefore gives

```math
 W_{xy}(t+2Lz)\in 2^{a+1-i}z\,\mathbb Z_{(2)}[z].
```

This divisibility also follows directly from the source's integrality
proof; the linear coefficient has precisely valuation `a+1-i`. Every
summand in each row factor in (1) has the displayed divisibility. Products
of the `K` row factors prove the claim; cancellation can only increase
the divisibility. The zero network may be formed by changing one unary
column table to `(0,0)`, leaving the graph and packet assignment fixed.
Its deformed polynomial vanishes identically. The two complete shifted
polynomials are consequently equal at the stated precisions, while their
origin parities differ. Their first `K` jet coefficients are all zero.

## Comparison and limits

The predecessor `parity-recovery-precision/PROOF.md`, Sections 3--5,
selects one row per nonempty packet. For a full packing of `M/L` packets,
that witness supplies a simultaneous per-node threshold
`(M/L)(a+1-i)`. Here each full packet supplies `L/2^u` selected rows,
so the threshold is `(M/2^u)(a+1-i)`, larger by `L/2^u`. For arbitrary
packing compare the stated `K` with its number of nonempty packets; no
particular gain is asserted when all packets contain only one edge.

The generic-polynomial predecessor has a threshold on the order of
`M D_i/u`, with `D_i=L/2^i`. Our universally guaranteed threshold is
`ceil(M/2^u)(a+1-i)`, which does **not** in general match that scale.
We do not realize the generic tapered polynomial, prove its tensor
realizability, or rule out tensor-aware recovery. The precise content of
(1) can be larger due to cancellation; no exactness of the lower bound is
claimed. The construction works already for one packet, but the active-call
parameter constraints and actual cost of the whole recursive algorithm are
separate; it gives no new SAT time bound or alpha.

Descriptions consist of degree-one Boolean tensor tables and the slot
choices. Given a graph-only packing, selecting the largest residue class
takes polynomial time and space; no random choices, numerical
approximations, oracle calls, or noncanonical coefficients are used. The
finite verifier is a separate small exact rational calculation and does not
prove the all-size statement.
