# Validation scope

A clean `git archive` export of commit
`94af82e7e3767a221f33a3f71ee2a32dbff843a0`, tree
`b6047e851cac979e888bee003a4e3124d22a270d`, replayed the frozen certificate,
direct factor/code checks, coarse R=1..12 screen and refined R=1..5 screen.
All four JSON outputs were byte-identical to their saved reports at that
commit. `make verify` passed the source/metadata/link checks and 17 tests.
The export path was `/tmp/3sat-macro-check-O7NwTH` on the authoring host.

The broader b=1..5 search was executed in the working checkout and its
hash-bound output retained. It was not repeated in the clean export; the
frozen certificate replay does not need that search. No historical heavy
research checks or full external SAT algorithm were run.

The follow-up adds this receipt and clarifies the tensorization lemma's
already-used sign-target assumption. Its certificate report is refreshed
to bind the clarified proof text. No code, seed or mathematical numerical
identity changes. These are author replays using Codex, not independent
review, human review, a Lean proof or a selected-result promotion.
