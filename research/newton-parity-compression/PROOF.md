# Scalar parity lifts with a sharper degree cutoff

Status: research proof, AI assisted, not independently reviewed. The accepted
OpenAI theorem is used as a theorem. This changes its sparse-query encoding;
it does not audit that theorem or claim a better SAT time exponent.

## 1. Setup and exact scalar lift

Let `P_i` be a polynomial over `F_2` given by squarefree monomials of degree
at most `k`, with duplicates cancelled. A constant monomial is allowed.
On a branch, give each test-variable pair its own Boolean incidence variable
`z_iv`, exactly as in the frozen source's `lem:tensor-sparse-query`. Write
the resulting monomials of one test as `m_1,...,m_t`. Work in the Boolean
polynomial ring `Z[z]/(z_v^2-z_v)` and put

```math
 Q_i(z)=\frac{1+\prod_{j=1}^{t}(1-2m_j(z))}{2}
       =1+\sum_{\varnothing\ne R\subseteq[t]}
            (-1)^{|R|}2^{|R|-1}\prod_{j\in R}m_j(z).
```

The displayed expansion proves that every coefficient is an integer, so the
division by two is performed over `Z`, before reduction; it is never inversion
of two in a residue ring. An empty list gives `Q_i=1`. At any Boolean input
each factor `1-2m_j` is `(-1)^{m_j}`, so `Q_i` is exactly the indicator
`[P_i=0]`, including when the list contains the constant monomial. This is
the elementary-symmetric / Newton expansion of parity in the monomial values.

Fix a precision `p>=1`. Terms with `|R|>p` have coefficients divisible by
`2^p` and may be discarded coefficient by coefficient, even before Boolean
multilinearization. There is no auxiliary variable `V` or coefficient-sum
map. We use only `Z/2^p Z`, i.e. truncation parameter `ell=1` in the accepted
Boolean tensor contraction theorem.

## 2. Coefficient valuations and a sharp product cutoff

For a nonempty incidence support `S`, let `rho_i(S)` be the smallest number
of listed monomials whose union of variable supports is exactly `S`. Put
`rho_i(S)=infinity` if there is no such subfamily. Every summand contributing
to `[z_S]Q_i` then has a factor `2^(rho_i(S)-1)`. In particular,

```math
 v_2([z_S]Q_i)\ \ge\ \rho_i(S)-1
                 \ \ge\ \lceil |S|/k\rceil-1.
```

Here `v_2(0)=infinity`. The empty coefficient is integral and has nonnegative
valuation. The covering number is a theoretical strengthening, not an
assumed polynomial-time subroutine.

Give different tests disjoint incidence variables and form `F=prod_i Q_i`
for `a` tests. A global incidence monomial is uniquely the union of its
supports `S_i` in the tests, so its coefficient is `prod_i [z_(S_i)]Q_i`.
If this coefficient survives modulo `2^p`, each factor is nonzero and

```math
 \sum_{i:S_i\ne\varnothing}(\rho_i(S_i)-1)\le p-1.
```

Let `b` be the number of nonempty `S_i`. Consequently its degree satisfies

```math
 \sum_i |S_i|\le k\sum_{i:S_i\ne\varnothing}\rho_i(S_i)
              \le k(b+p-1)\le K_{\rm scalar}:=k(a+p-1).
```

This is a coefficientwise congruence in the Boolean incidence ring, rather
than a statement requiring evaluation on original assignments. Thus all
incidence monomials of larger degree may be omitted before contraction.

For comparison, `eq:sharp-incidence-degree` in the accepted source uses
`K_source=k(a+2(p-1))` with `ell=p`. The new bound is smaller by `k(p-1)`.
For exact counting at `p=n+1`, these are `k(a+n)` and `k(a+2n)`.
This is an explicit cutoff improvement, not a comparison of unknown runtime
constants.

The scalar cutoff is sharp for this coefficientwise model. Choose integers
`r_i>=1` with `sum_i(r_i-1)=p-1` and let test `i` be the parity of `r_i`
pairwise disjoint degree-`k` monomials. Its full-support coefficient is
`(-1)^r_i 2^(r_i-1)`. Their product is nonzero modulo `2^p` at degree
`k(a+p-1)`. These are distinct incidences across tests; the original variables
may be reused between tests. In the exact-counting regime one may take
`a=n`, `p=n+1`, `r_i=2`, and `n>=2k`, so every test uses only `2k<=n`
original variables. This is sharpness of the incidence cutoff, not a lower
bound on runtime or a claim that all the resulting contributions avoid
cancellation after identifying incidences.

## 3. Encoding, entries and complete cost

Retain the source's normalization and high-incidence branching. Write
`lambda=ceil(log_2 n)`, `nu=ceil(log_2 lambda)`, and use its threshold
`D_*=max(1,ceil(N_0/n))*ceil(sqrt(lambda))`. At most `n/sqrt(lambda)`
variables exceed that threshold. Normalization after substitution is still
valid because the scalar lift applies to every normalized branch polynomial.
Constant-one tests give zero; no remaining tests gives the direct count of
free variables. These cases need no network.

For a nontrivial branch group the tests and free variables separately into
`J=ceil(n^(1/4))` groups. For each group pair let `N_gh` be its incidence
count, and enumerate degree arrays `0<=d_gh<=N_gh` with sum at most
`K_scalar`. For that array use `ceil(log_2 binom(N_gh,d_gh))` wires with the
source's lexicographic subset decoder and invalid-index zero rule. Thus

```math
 M\le J^2+\log_2\binom{N+K_{\rm scalar}}{K_{\rm scalar}}
       =O_{k,c}(n\log\log n).
```

This uses the same stars-and-bars upper bound as the source. It also gives
a smaller explicit upper bound when `N` and the grouping are held fixed.
The exact per-array formula is unchanged; a smaller cutoff excludes some
arrays, and does not decrease the wire count of a retained fixed array.
There are at most `(K_scalar+1)^(J^2)=2^O(sqrt(n) log n)` arrays. Both their
counter descriptions and binomial decoding have polynomial bit cost.

At a test group the entry is the product, modulo `2^p`, of the indicated
coefficients of the `Q_i`. A single coefficient has the independent formula

```math
 [z_S]Q_i=\sum_{T\subseteq S}(-1)^{|S|-|T|}
                     [P_i(1_T)=0].
```

This is Boolean Mobius inversion, with every variable outside `T` set to
zero. Each summand is obtained by evaluating the listed `F_2` polynomial;
it does not require constructing all monomial subfamilies or the exact
covering number. Since `|S|<=k lambda^c`, it costs
`2^(lambda^O_(k,c)(1))` bit operations and polynomial space, accumulated
modulo `2^p`. Multiply the group coefficients with scalar modular arithmetic.

At a variable group, the entry remains `2^(number of untouched free variables)`
modulo `2^p`. Every indicated monomial occurs in exactly one array and has
one valid code per group pair. Identifying equal original variables and
summing all assignments gives the sum of these contractions, because the
omitted coefficients are zero modulo `2^p`. Declared unused variables are
included in the variable-group count. The constant monomial and all-zero
degree arrays are included. Isolated vertices are scalar factors.

At `p=n+1`, the sum over branches is the original count modulo `2^(n+1)`;
its least nonnegative residue is the exact count in `[0,2^n]`. The maximum
group degree remains `n^(3/4) lambda^O_(k,c)(1)`. Descriptions have polynomial
length. With `s=n nu` all degree, description, entry-time and precision
hypotheses of the accepted `thm:tensor-contraction` therefore hold for all
sufficiently large `n`; `P_0=p=n+1=O(s)` and `ell=1`.

The complete sparse-query budget is:

| Component | Bound or treatment |
| --- | --- |
| Normalization and descriptions | Polynomial in the listed input size |
| High-incidence branches | At most `2^(n/sqrt(lambda))` |
| Degree arrays per branch | `2^O_(k,c)(sqrt(n) log n)` |
| Wires | `O_(k,c)(n nu)`, with the improved explicit degree cutoff above |
| Original entry computation | `2^(lambda^O_(k,c)(1))` time, polynomial space |
| Precision and algebra | `p=n+1` scalar bits; `ell=1` |
| Modes, recursion, leaves, recovery | Accepted contraction theorem at size `s=n nu` |
| Final decoding | Sum scalar residues, no coefficient-sum map |
| Exceptional bounded sizes | Direct enumeration with a fixed cutoff |
| Randomness, amplification | None |

The resulting sparse-query and general-density time envelopes remain
`poly(n+m) 2^O_k(n log log n/sqrt(log n))`, with polynomial space.
For general CNF use the accepted sparsification and greedy hash reduction
without changing which queries are answered: all selected **and rejected**
candidates are covered by this sparse-query interface. Sparsification has
`2^O_k(n/sqrt(log n))` leaves and the total per-leaf query construction and
multiplicity is `2^((log n)^O_k(1))`. Both are absorbed in the same envelope.
For fixed density keep the accepted clause-network route, with its sharper
`poly(n+m) 2^O_(k,D)(n/sqrt(log n))` guarantee. Normalization handles arbitrary
input clause counts in polynomial input time. Finite exceptional cases of the
modified interface and unchanged outer reduction use exhaustive counting.

## 4. Why actual nonzero support alone still costs log log n

Here is a realizable nonlinear family, not an unrestricted formal partition
model. Fix `k>=2`, let `t=floor(log_2 n)`, and suppose `kt<n`. Index original
variables by `Z/nZ`; use `a=n` equations

```math
 P_i(x)=\bigoplus_{j=0}^{t-1}\prod_{u=0}^{k-1}x_{i+kj+u},
       \qquad i\in\mathbb Z/n\mathbb Z.
```

Each row consists of `t` disjoint degree-`k` monomials. Its scope is a cyclic
interval of size `kt`. These intervals, and hence the equations, are distinct
since `kt<n`. Every original variable occurs in exactly `kt` scopes, so
`N_0=nkt` and no variable exceeds the specified high-incidence threshold.
These satisfy the sparse-query assumptions, for example with any fixed
`c>=1` that also allows `a=n`.

In the scalar incidence lift, choosing any one of the `t` monomials from
each equation gives `t^n` different incidence monomials of degree `kn`.
Each coefficient is exactly `(-1)^n`: within a test no other subfamily of
its disjoint listed monomials has that support. They all survive modulo
`2^(n+1)` and the sharper cutoff `k(a+p-1)=2kn`.

Under the fixed grouping there are at most
`(K_scalar+1)^(J^2)=2^O(sqrt(n) log n)` degree arrays. Hence at least one array
contains at least

```math
 t^n/(K_{\rm scalar}+1)^{J^2}
```

of these actual nonzero monomials. Any binary wire code that assigns a
distinct valid wire assignment to each retained incidence monomial in that
array needs at least

```math
 M\ge n\log_2 t-J^2\log_2(K_{\rm scalar}+1)
   =\Omega(n\log\log n).
```

The source's one-monomial-per-code architecture is such a code. Even an
oracle that removes all zero coefficients cannot uniformly reduce its wire
order while retaining this representation. This is an information bound on
that encoding, not on SAT algorithms, tensor contraction, or compressed
aggregate representations. It does not rule out cancellations after
identifying copies of a variable, regrouping that changes the representation,
row operations, a special algorithm for these examples, or a different kernel.

## 5. Remaining research obligation

The positive result simplifies the coefficient algebra and sharpens the
cutoff. An improvement to the full asymptotic bound still needs a changed
representation: aggregate incidence monomials before coding them, exploit
cancellation after variable identification, or avoid these sparse queries.
The cyclic family is a required regression for a claim based only on fewer
nonzero incidence coefficients. A proof for special easy equations would
not close the uniform sparse-query or general-SAT problem.

The identities and comparison to OpenAI are not a claim of priority. Sources,
pins, finite check coverage, and the actual handoff are in [README.md](README.md).
