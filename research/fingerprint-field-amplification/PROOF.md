# Field size versus fingerprint amplification

This is an author-checked component argument, not an independent review or a
new 3-SAT bound. It builds on the weighted characteristic-two decision
interface in `research/characteristic-two-decision/PROOF.md`; the accepted
OpenAI theorem is a premise.

## Uniform evaluation of multilinear polynomials

Let F be a field of q elements, q >= 2, and let P be a nonzero multilinear
polynomial in N variables over F. For independent uniform R_i in F,

    Pr[P(R) != 0] >= (1 - 1/q)^N.                         (1)

Proof by induction on N: write P=A+X_N B. If B=0, apply induction to A.
Otherwise B is nonzero and, with probability at least (1-1/q)^(N-1), its
value is nonzero. Conditional on that event, at most one of the q choices
of R_N makes A+R_N B zero. This proves (1). For N=0, the probability is 1.

For the solution-set fingerprint Z_S = sum_{x in S} product_{i:x_i=1} R_i,
S nonempty implies Z_S is nonzero. Bound (1) is exactly tight among such
fingerprints: S={0,1}^N gives Z_S=product_i(1+R_i), which is nonzero at
exactly (q-1)^N of the q^N points. These are free variables and can be removed
by a decision preprocessor; the next example addresses that limitation.

## A constrained family and the independent-sample barrier

Take N=2k variables in k disjoint equality constraints x_i=y_i, expressible
as the 2-CNF clauses (not x_i or y_i) and (x_i or not y_i). Every variable
occurs in two clauses. Its solution fingerprint is

    Z(R,S) = product_{i=1}^k (1 + R_i S_i).

In characteristic two each factor is zero exactly when R_i S_i=1. Of the
q^2 ordered pairs, precisely q-1 satisfy this equation, so an independent
uniform evaluation succeeds with exact probability

    p_k(q) = (1 - (q-1)/q^2)^k.                          (2)

For q>=2, (q-1)/q^2 is between 1/(2q) and 1/q. Hence
-log p_k(q)=Theta(k/q), uniformly in k and q. If t independent evaluations
are ORed, success is 1-(1-p_k)^t; reaching 2/3 requires t>=2/(3p_k)
by the union bound. Thus t=exp(Omega(N/q)) is necessary on this family for
that fixed sampling procedure. The family is easy: equality elimination
solves it or exposes free variables. This is not a lower bound on SAT, on
adaptive preprocessing, on arbitrary fingerprints, or on correlated or
nonuniform evaluations. The free-variable example also shows that (1) is
the exact uniform all-solution-set bound before such preprocessing.

## Amplification and the existing full wrapper

For an arbitrary nonempty S, sample t independent uniform field points and OR
the nonzero results. With p0=(1-1/q)^N and 0<delta<1, take

    t = ceil(ln(1/delta)/p0),

or any integer upper bound at least that large. Then the false-negative
probability is at most exp(-t p0)<=delta; empty S always returns zero.
For q>=2, log t = O(N/q + log(1+log(1/delta))). An implementation can use a
conservative integer bound t=ceil(ln(1/delta) * 4^ceil(N/q)), since
(1-1/q)^(-N) <= 4^(N/q). It uses a fixed bounded number of samples and
random bits, and its counter needs O(N/q+log log(1/delta)) bits. In
particular, no rejection sampling or random runtime is hidden.

Use q=2^e with e>=1. The existing decision wrapper works with N<=n original
Boolean variables per sparsification leaf. Keep its random sparse hashes and
initial checks unchanged; condition on all hash choices. A satisfiable leaf
still has a nonempty solution set, so independent weights give conditional
false-negative probability <=1/6. On an unsatisfiable input, ORing repeated
fingerprints creates no new false positive unless the hashes admit a false
assignment: the existing union bound on that event is unchanged. Run samples
sequentially, preserving polynomial space. The source's formula reduction,
high-incidence branches, degree arrays, tensor-entry computation, recursion,
precision, recovery, and field postprocessing are repeated or charged as in
the predecessor. The field construction is polynomial for the choices below;
the predecessor's field-to-truncated-ring embedding remains valid, with
ell=number_of_vertices*(e-1)+1, and no missing field arithmetic is assumed.

For q a power of two between 2 and poly(n), the whole general-density
worst-run bound becomes

    poly(input) * 2^{O_k(n log log n / sqrt(log n) + n/q)}.  (3)

Here t is charged once per fingerprint, not assumed free, and N<=n. In
particular choose a power of two q=Theta(sqrt(log n)/log log n) for all
sufficiently large n, with bounded small inputs handled directly. The extra
n/q term fits the baseline exponent. Taking q asymptotically larger than
sqrt(log n)/log log n but still poly(n) makes that extra exponent lower
order. This is a smaller field than the predecessor's q>=6N, but it does not
improve the asymptotic time or alpha. The predecessor's explicit fixed-density
fallback to the accepted counter is unchanged; no fixed-density improvement
is asserted. Parameter floors and logarithm bases only affect constants.

The equality family proves only the worst-case amplification order for
independent uniform evaluations; it does not show the entire wrapper has a
matching running-time lower bound. Different sampling, deterministic choices,
preprocessing, or a different decision interface require their own argument.

## Finite evidence and limits

`verify.py` exhausts all nonempty Boolean solution sets for N=4 over GF(2)
and N=3 over GF(4), and checks equality families over GF(2), GF(4), and GF(8).
It counts every field point and checks the factorization and exact counts.
These finite checks test the statement and arithmetic, not the induction,
the asymptotic cost, or the accepted contraction theorem. All-size arguments
above have not received independent review.
