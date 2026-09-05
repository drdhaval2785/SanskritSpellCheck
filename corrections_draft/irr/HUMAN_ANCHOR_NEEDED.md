# Human-labelled seed anchor — outstanding gate (H825, ruling D9)

_Created: 12-07-2026 · Last updated: 12-07-2026_

## The gap

A44's inter-rater reliability currently rests on two (soon three) **LLM annotators**
judging the same 122-row IRR sample (`irr_inputs.tsv`) against the five-way taxonomy
PASS / SCAN-FIRST / EDITORIAL / DNF / DROP:

- Annotator A — the FILE-FIRST verification pass (Sonnet 5 mechanical, Fable 5
  adjudication of flags): [`file_first_verified.tsv`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/file_first_verified.tsv)
- Annotator B — within-family blind second pass (Opus 4.8): [`second_annotations.tsv`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/irr/second_annotations.tsv), κ=0.336 five-way / 0.663 binary
- Annotator C — cross-family blind pass (non-Anthropic judge, H825/D9): [`cross_family_annotations.tsv`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/irr/cross_family_annotations.tsv),
  produced by [`detectors/irr_cross_family.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/irr_cross_family.py)
  — **not yet run on this host: no `LLM_API_KEY`/DeepSeek credential was configured
  when H825 executed (12-07-2026); the script is ready, just needs a key.**

Ruling D9 swaps the judge *family* to remove the self-enhancement-bias confound
(same-family judges systematically over-rate same-family output — Zheng MT-Bench
[2306.05685](https://arxiv.org/abs/2306.05685); Self-Preference Bias
[2410.21819](https://arxiv.org/abs/2410.21819)). But A-vs-B and A-vs-C are **both
still LLM-only comparisons.** Two (or three) annotators agreeing — even across
model families — is evidence of *consistency*, not of *correctness against the
physical scan*. A referee can still ask "how do you know any of these three
annotators is right?", and nothing in the current design answers that.

## What's needed

A genuine **human-labelled seed set, even as small as ~30 rows**, drawn from the
same 122-row `irr_inputs.tsv` sample, labelled by a person (Dr. Gasūns or another
qualified reviewer) against the same five-way taxonomy, working from the same
blind evidence (dict / wrong / right / entry text only — no verdicts). This is
**not something an agent session can produce**: fabricating "human" labels would
be worse than leaving the gap explicit, and the whole point of the anchor is that
it is independent of the LLM annotators being validated.

Once the seed exists:
1. Compute human-vs-A, human-vs-B, human-vs-C kappa the same way
   `detectors/irr_agreement.py` computes A-vs-B/A-vs-C (reuse `kappa()`/
   `binary_kappa()` — the same exact-fraction machinery, no scipy).
2. If human-vs-{A,B,C} kappa is comparable to A-vs-B/A-vs-C kappa, that licenses
   citing the LLM-only figures as validated inter-annotator reliability in the
   paper. If it is not comparable, the paper should report the discrepancy rather
   than the higher LLM-only number.

## Status

**a human should decide** whether to produce this seed set now (before A44 goes to
referees) or accept the current LLM-only κ with an explicit caveat in the paper —
this trade-off is recorded in A44's Limitations section pending that call. Not
blocking the eval-harness (step 2) or reframe (step 3) work in this handoff.

_Dr. Mārcis Gasūns_
