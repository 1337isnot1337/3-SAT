# Charge-polynomial scalar filters

Status: `scoped_checked` finite constructions and complete finite negative
certificates. No all-size filter, smaller rho, larger SAT alpha or selected-
result change is claimed.

The package lifts the charged normal-order recurrence over Z[q] and classifies
scalar-output combinations by exact rational nullspaces and determinant
polynomials. It includes the original raw-charge screen, the inverse-length
contraction-deficit reindexing, and a new length-amplified local rescaling.

At `lambda=2,h=6`, the completed raw boundary admits cutoff 4 but not 5. The
new `q^(len(mu)+len(nu))` space admits cutoff 5, constructing an actual crossing
with every shift `-5,...,5` removed, but not cutoff 6. See [METHOD.md](METHOD.md)
for exact scope and costs and [REGISTERED.md](REGISTERED.md) for the distinct
rescaling premises.

Reproduce the improved witness and its raw controls with:

```sh
python3 -I -B research/charge-polynomial-filter/generalized.py
make verify
```

Finite positive cases do not supply a uniform selector or asymptotic capacity.
Negative cases cover the complete stated finite scalar matrix space, not every
possible codebook or rescaling.
