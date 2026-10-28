# Simultaneous compression of low-weight zero modes

This is a written, author-checked component argument. It is not an
independent review, a complete crossing factorization, or a SAT speedup. The
charged normal-ordering definitions are those of `charged-operator-moments`;
the moment-to-zero-mode argument is the one used in concurrent PR #89, pinned
at `431477efe926c611e693804f323c50ac76969192`. The accepted OpenAI theorem
is a premise, not the subject of this argument.

## 1. A codebook for all modes up to weight d

Fix E>=1, integer charge q, and d>=1. Let V_E have the partition basis of
energy E. For each partition a of total weight at most d, let O_a be the
energy-preserving zero mode of its charged Heisenberg field. The empty
partition gives the identity. Let

    M = sum_{j=0}^d p(j),
    B = ((2E+1)(E+d)(E^2+|q|+1))^d,
    Delta = 2 M (2E+1)^d.

There is an explicitly constructible nonempty subset W of the partition basis
such that every O_a compresses to a scalar on W and

    |W| >= p(E) / ((2B+1)^M (Delta+1)).                 (1)

Here compression means `P_W O_a P_W = c_a P_W`; W is not claimed invariant.

For a=(a_1,...,a_l), l<=d, expand its normal-ordered zero mode as the sum of
products of l modes D_i with indices adding to zero. A term contributing to
an energy-E matrix entry has all indices in [-E,E]: a positive mode larger
than E annihilates the input, and any negative mode with magnitude larger
than E would create more total energy than the output contains. There are at
most (2E+1)^d index tuples. Each field coefficient is the integer
`binom(-i-1,a_j-1)`; its absolute value is at most (E+d)^(a_j-1), so their
product is at most (E+d)^d. An annihilator k partial_(t_k) contributes at
most E^2 on a partition of energy E, and a zero mode contributes |q|. This
bounds every entry by B, even after summing tuples. Every fixed index tuple
maps an input partition to at most one output partition, and conversely an
output has at most one possible input for that tuple. Thus, in the undirected
union of off-diagonal transitions of all M operators, each vertex has degree
at most Delta. Potential cancellations only reduce the graph.

Give each state its M-tuple of diagonal entries. Every coordinate is an
integer in [-B,B], so there are at most (2B+1)^M signatures. Select a largest
signature class, and greedily select an independent set of its induced graph.
An independent set of a graph with maximum degree Delta has at least its
vertex count divided by Delta+1. Every selected state has the same diagonal for
every O_a, and no selected pair has an off-diagonal transition for any O_a.
This proves (1) and the simultaneous scalar compression. ∎

The selection is deterministic: enumerate partitions in a fixed order, compute
all M operator vectors and signatures, choose the largest signature class with
a fixed tie break, and scan it greedily. Direct normal ordering provides a
uniform exact implementation. It takes at most
`p(E) * M * (2E+1)^d * poly(E,d,log(|q|+2))` arithmetic/bit overhead, up to
polynomial factors for output data structures and coefficients. This bound
allows exponential-in-sqrt(E) storage; no polynomial-space implementation is
claimed.

## 2. A growing family with leading output capacity

For fixed q, take

    d(E) = max(1, floor((ln E)^2 / 144)).

The elementary partition bound `p(j)<=exp(3 sqrt(j))` follows by setting
`t=1/sqrt(j)` in the Euler product and using
`log product_m (1-exp(-tm))^-1 <= pi^2/(6t)`; p(0)=1. Hence

    M <= (d+1) exp(3 sqrt(d)) <= (d+1) E^(1/4)

for all sufficiently large E. With this d, the logarithm of the denominator
in (1) is `O(E^(1/4) polylog(E)) = o(sqrt(E))`. Together with the standard
partition asymptotic this gives

    |W| >= exp(pi sqrt(2E/3) - o(sqrt(E))).               (2)

The construction bound above is `exp(O(sqrt(E)))`: the extra factors have
logarithm `O(d log E + sqrt(d) + polylog(E))=o(sqrt(E))`. At the crossing
scale E=h=Theta(lambda^2), this is `2^O(lambda)` time and space. Equation
(2) means that to supply N=2^lambda output labels one may choose h with the
same leading sqrt(h) coefficient as the full partition space, allowing a
subleading adjustment. It does not establish a matching input-label rank.

## 3. Consequence for charged filters

The charged moment argument pinned above says that, for any source labels
and any j<=d, `sum_s s^j Q_s` lies in the span of the O_a of weight at most j.
It follows from the normal-ordering expansion: each uncontracted field of
weight r has a factor `(z1-z2)^r`, and j logarithmic derivatives leave
weight at most j. The scalar coefficient of each O_a is independent of the
output partition basis state. Consequently the same W compresses *every*
polynomial moment of degree at most d to a label-dependent scalar.

For r=floor((d-1)/2), take

    w(s) = s product_{j=1}^r (s^2-j^2).

Its degree is at most d and w(s)=0 for |s|<=r. Therefore the charged crossing
pieces weighted by w have scalar output compression on W and remove a
central interval with r=Theta((log E)^2). Their integer weights have
poly(log E) bit length for source shifts |s|=O(E+h), and there are only
polynomially many shifts. Entries can be generated with the predecessor
piece generator plus the stated codebook construction.

This is a growing but **sublinear** central interval: r/h tends to zero
at E=h. It does not achieve the fixed-fraction removal required by the
existing conditional rho improvement. More decisively, the scalar
input-label pairing might be singular, zero, or too small in rank; no
normalizer or valid crossing identity follows from output compression alone.
The codebook proof does not establish such a rank. Both directional ranks,
input and output capacity simultaneously, bit/prime transfer, recursion,
precision, recovery, and full reduction costs must be proved before any SAT
bound follows. Generic dense construction here uses exponential space in
lambda; it does not inherit the accepted polynomial-space result.
