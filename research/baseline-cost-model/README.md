# Accepted baseline cost bookkeeping

Status: scoped checks of an exact symbolic model. No bound improvement.
Task: `complete-cost`. Prepared with OpenAI Codex assistance.

The [general-density model](../../certificates/models/general.json) and
[fixed-density model](../../certificates/models/fixed-density.json) transcribe
the accepted Appendix D cost envelopes. Sources are frozen by
[SOURCES.json](../../SOURCES.json) at OpenAI commit
`7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`. Source labels are attached to each
model. The OpenAI theorem is accepted as true, not checked by this tool.

An exponent envelope has exact rational powers `(a,b,c)`, representing
`n^a (log n)^b (log log n)^c` inside `2^O(...)`. For finitely many paid terms,
lexicographic order compares their eventual growth. A contraction with saving
`theta` on network size `s = Theta(n^a (log n)^b (log log n)^c)`, with fixed
`a>0`, has envelope `(a,b-theta,c)`. Polynomial factors and fixed constants do
not alter this exponent comparison. The models use conservative asymptotic
upper envelopes, not estimates of actual runtime or lower bounds.

The tool assumes the supplied list contains all exponential costs. It cannot
check realizability, uniformity, omitted work, or whether an upper envelope is
sharp. A rejection means the supplied ledger does not certify a better bound;
it is not a lower-bound theorem against a new algorithm. Unspecified constants
and finite cutoffs prevent finite-performance conclusions.

```sh
python3 -m satbounds.cost certificates/models/general.json
python3 -m satbounds.cost certificates/models/fixed-density.json
python3 -B -m unittest discover -s tests -p test_cost.py -v
```

The general model returns `(1,-1/2,1)` and alpha `1/2`; the fixed-density model
returns `(1,-1/2,0)` and the same alpha. Failure controls cover:

- Removing an iterated logarithm improves the full envelope without changing alpha.
- A hypothetical better contraction saving remains limited by unchanged outer costs.
- Extra logarithmic wire growth can erase a hypothetical contraction improvement.
- A sufficiently expensive entry routine can dominate every logarithmic saving.

Open next questions: give one new realizable mode family, recursive schedule,
encoding, or decision primitive, then replace the relevant assumptions and add
its full overheads. A better result from edited JSON is not a theorem. The next
scientific obligation is a proof of the changed construction, not a reproof of
the accepted OpenAI baseline.
