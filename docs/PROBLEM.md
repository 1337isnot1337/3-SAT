# Problem and comparison rules

The target is the [Big O Speedrun 3-SAT problem](https://bigospeedrun.com/3sat),
as read on October 26, 2026. This page records our working contract; refresh
the external rules before making an external submission.

An input is a CNF on `n` declared variables and `m` clauses, with at most three
literals per clause. Literals may be positive or negative. Unused variables,
repeated literals, tautologies, empty clauses, and the empty formula must have
their usual semantics. Decide whether an assignment satisfies all clauses.
The accepted baseline additionally computes the exact number of assignments,
including the choices of every declared unused variable.

One uniform algorithm must handle all `n,m`. Count bit operations on a standard
encoding. The site's equivalent word-RAM formulation has word length
`O(log(n+m))`; arbitrary-precision operations are not free. The notation `O*`
hides only a fixed polynomial in `n+m`. Input normalization must therefore be
charged. Bounded small inputs may use an explicit exhaustive fallback.

For randomized algorithms, each bit is independent and uniform and costs one
operation to read. Each fixed input must be answered correctly with probability
at least `2/3`. The time bound must hold for every random outcome. An expectation
over runtime or over an input distribution does not meet this contract.
Amplification and its cost must be explicit. Deterministic algorithms qualify.
The site does not require polynomial space; state any space usage being claimed.

The comparison parameter is alpha in

```math
 O^*(2^{n/(\log n)^{\alpha-o(1)}}).
```

For every fixed positive epsilon, this means an eventual bound with exponent
`n/(log n)^(alpha-epsilon)`, up to the permitted polynomial factor. Larger
alpha is better. Fixed powers of `log log n` and constant multipliers in the
exponent are absorbed by this notation, so the full running time must also be
reported. Constant-base `c^n` algorithms have alpha zero in this comparison.
For example, the site's historical Jiang--Cai 2026 reference is
`O*(1.307031578^n)` ([preprint v1](https://arxiv.org/abs/2607.10697v1)).

The selected OpenAI theorem gives alpha `1/2`. Its general-density exponent is
`O(n log log n / sqrt(log n))`; its fixed-density exponent is
`O_D(n / sqrt(log n))`. These are not interchangeable guarantees. A decision-only
or randomized successor is allowed if it meets the same input and time rules.

The source uses natural logarithms in its main statement and switches to
base-two logarithms in the contraction proof. Fixed logarithm bases do not
change alpha; parameter formulas and finite computations must retain their
declared bases. Dense inputs cannot be replaced with `m=O(n)` without a paid
reduction.
