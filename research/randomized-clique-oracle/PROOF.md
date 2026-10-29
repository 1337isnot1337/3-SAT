# Randomized decision for the universal clique oracle

## Statement

Fix `K>=2`, `lambda>=1` and `0<=delta<1/2`. In the clique-table
point-query model of `def:achievable` in the pinned source, take Boolean
nonnegative tables and ask only whether the clique sum is positive. A
randomized algorithm may adapt its queries to answers and use arbitrarily
many random bits. Suppose for **every** input its answer is correct with
probability at least `1-delta` and at most `q` point queries are made on
every random outcome. Then

    q >= ceil(M (1-2 delta)/(1-delta)),
    M = 2^((K-1)lambda).                               (1)

This remains true if computation between queries is free. The input bound
is already forced by the restricted family in which `W_2,...,W_K` are
identically one and `W_1` is either zero everywhere or has one nonzero
entry. Thus (1) is a lower bound for a **universal table-oracle decision
interface**, not for 3-SAT or a restricted class of generated tables.

Moreover (1) is tight for that restricted zero-or-one-hot family: with
probability `delta`, output YES immediately; otherwise query a uniformly
chosen subset of size `ceil(M (1-2 delta)/(1-delta))` and output YES iff a
queried entry is one. Zero inputs are correct with probability `1-delta`;
one-hot inputs are accepted with probability at least
`delta+(1-delta)q/M >= 1-delta`. This is a finite oracle algorithm for this
family, not a general clique solver. At `delta=0` it queries all M entries.

Consequently, if `delta` is any fixed constant below 1/2, a worst-outcome
operation bound `C 2^(e K² lambda)(B+lambda)^C` valid for fixed K and all
lambda and `B=1` requires `e >= (K-1)/K²`. The same lower exponent follows
for randomized exact counting with bounded error, since on this nonnegative
family deciding whether its output is positive gives a decision algorithm.
This assumes an answer is produced within the stated worst-outcome budget.
For a flagging algorithm, map its failure flag to NO and verify separately
that the resulting decision error satisfies the given bound.

## Proof by coupling zero and one-hot inputs

Fix all tables other than `W_1` to one. Label the `M` inputs to `W_1` by z.
On the zero input, fix an algorithm's entire random tape, and record its
answer `A_0` and set `Q_0` of entries of `W_1` that it queries. The one-hot
input at z has exactly the same transcript until z is queried; hence, on
any tape for which `z` is not in `Q_0`, its final answer equals `A_0`.
This holds even for adaptive queries and for queries to the other tables.

Let `r=Pr(A_0=NO)`, so `r>=1-delta`. For each z, one-hot success implies

    Pr(A_0=NO and z in Q_0) >= r-delta.                  (2)

Indeed at most `1-r` of the successful YES outcomes can lie on tapes with
`A_0=YES`; every remaining successful YES outcome has `A_0=NO` and must
query z. Sum (2) over z. Since the zero-input query set has size at most q
on every random tape,

    q r >= E[1_{A_0=NO} |Q_0|] >= M(r-delta).

Thus `q>=M(1-delta/r) >= M(1-2delta)/(1-delta)`, because the expression
increases with r and `r>=1-delta`. Integer rounding gives (1). The proof
also yields `E[|Q_0|] >= M(1-2delta)`, but the worst-outcome statement (1)
is stronger when delta is positive.

## Scope and remaining work

The oracle assumption is essential: an algorithm given a concise promise,
structure, circuit representation or exploitable relation between table
entries is not constrained by an arbitrary-point-table adversary in this
form. The argument does not establish a probability bound for a generic
SAT fingerprint or an alpha improvement. It extends the deterministic
floor in [PR 69](https://github.com/1337isnot1337/3-SAT/pull/69); that PR's
thin-grid corollary applies to a compatible continuous cost model, not to
actual unrestricted SAT inputs. Any new recursive interface must still pay
its encoding, entry evaluations, random generation, amplification, recovery,
reductions, and space. The accepted OpenAI theorem remains selected.
