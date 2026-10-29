# Active charge-filter continuation

Goal ACTIVE and INCOMPLETE: work indefinitely on a mathematical improvement;
commit/push often; owner has authorized merges. No subagents. Do not stop
or mark complete after this finite checkpoint. Selected alpha still 1/2;
upstream and selected record remain unchanged.

Branch `research/charge-polynomial-filter`, base
`630041c9da3a26edb8c8f59d5f8a4132a188c8bd`. PR 19 is merged and its
full report replayed byte-for-byte on fresh main; all 17 tests passed.
The predecessors supply actual asymmetric first-moment pieces and the
rational odd-prime transfer. Check main, all branches and PRs again at
the next pivot/submission. Other open work last seen: PR 18 aggregate
packing and PR 12 README docs.

First registered screen completed. The exact polynomial recurrence passes
560 primitive comparisons, 744 piece evaluations and 186 coefficientwise
order checks. Full raw-charge spans were classified at lambda=1 (h=4)
and lambda=2 (h=6), over every charge coefficient, with exact determinant
polynomials. At lambda=2, cutoffs T=0,1,2 have an invertible scalar pairing;
T=5,11 do not. At lambda=1, T=0,1,3 work and T=7 does not. Unlisted cutoffs
are unknown. Positive witnesses are actual finite filtered crossings,
not an asymptotic bound. No alpha improvement is established.

Important codebook order: the pinned partition generator starts with
ones, NOT the largest part. For lambda=2, row labels are
(1^6),(2,2,1,1),(2,2,2),(3,3); columns are
(2,1^4),(2,2,2),(3,3),(6); outputs are
(1^6),(2,1^4),(2,2,1,1),(2,2,2). Maximum charge degree is eleven.
Do not reason from an assumed reversed partition order.

Next changed premise: rescale each raw entry by
`q^(-length(mu)-length(nu))` before taking charge combinations, using q!=0.
This is a local diagonal change on x and v, so both ranks are preserved
at each charge. With z=1/q it becomes a polynomial whose coefficient
of z^e is obtained by reindexing the raw coefficient d via
`e=length(mu)+length(nu)-d` separately at each label pair. It records
nonzero-current/contraction deficit rather than the old absolute charge
degree. The old raw-charge finite negative certificate does not cover
this charge-dependent local rescaling, nor does the earlier high-charge
support lemma apply unchanged. Register this premise BEFORE testing.

Use the same two codebooks and same cutoffs for comparison, not a larger
blind grade scan. All operator polynomials can be built once, and the
new tensors are obtained by exact reindexing, so there is no need to
sample many extra charge values. Keep the raw evidence and hashes; a
new combined report must distinguish the two spaces. Verify all scalar
off-diagonal and diagonal-block constraints, not a trace or one entry.

Analytic question if a filtered candidate appears: does a scalar filter
on contraction deficits extend uniformly while keeping
`exp(kappa sqrt(h)-O(log h))` label AND output capacity? Generic coefficient
interpolation costs only polynomial factors. An all-size existence proof,
not a finite minor or symbolic determinant at N<=4, remains essential.
Raw high-charge coefficient extraction has the long-row/long-column
capacity bound in PR 19 NEXT.md; charge-dependent normalization changes
that premise. A genuine successor must still pay every rank/entry/query
and random-outcome cost through PR 17.
