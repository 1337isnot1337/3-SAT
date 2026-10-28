# Checkpoint

The all-size `u=1` factorization and finite-precision lift are in PROOF.md.
The construction needs prescribed packets and nonnegative integer tensor
entries; it does not show actual balanced packing, Boolean tables, or the
generic precision scale at equal port count. PR #52's quadratic construction
may beat independent one-packet copies for larger powers.

For `u>1`, the same divided-difference proof provides only a smaller known
power of `(z-1)` in the shift polynomial; a one-packet realization requires
an additional factorization into two 2-integral polynomials of degree below
`L`, with the constant normalized via the zero column. Check live issues
before pursuing this explicit factorization question. Selected alpha is 1/2.
