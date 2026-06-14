# SanskritSpellCheck — roadmap

Phased plan for where the toolset goes next. The questions below were left open, so
this uses defaults — **override any of them and the plan re-shapes**:

| decision | default taken | alternatives |
|---|---|---|
| primary goal | **ship more corrections**, with *productize the toolset* as the enabler | research/publication; live Cologne integration |
| horizon | **phased** (weeks → a quarter → long-range) | near-term only; one quarter; vision-only |
| verify bottleneck | **prioritize + a review workflow** first, OCR-assist later | OCR-first; ranking-only; fully autonomous |
| submission policy | **auto-prepare, human-approve** (band-5 drafted as change-files, a human merges) | always human-gate; auto-submit band-5 |

These defaults reflect the project's purpose (feed [CORRECTIONS](https://github.com/sanskrit-lexicon/CORRECTIONS/issues))
and the maintainers' low tolerance for bot noise — so everything stays human-gated at
the submission boundary, batched, and low-noise.

## Where we are (baseline, June 2026)

Modernized to Python 3 + PHP 8. Ten detection methods: faultfinder, o_vs_O, ngram +
the seven in [detectors/](detectors), several DCS-grounded. The pipeline is
**candidate → human verify against scans → CORRECTIONS**. The candidate side is
strong; the **bottleneck is human verification**, and candidates are scattered across
ten tools with no unified, deduplicated, confidence-ranked view.

## Guiding principles

- Candidates, never silent auto-fixes; a human gates the submission.
- Precision over volume *at the submission boundary* (recall stays high upstream).
- Reuse the existing formats (`X:CODE=Y:D`, `DICT:wrong:right:n`) so new work plugs in.
- Cross-detector agreement is the cheapest confidence signal we are not yet using.

---

## Phase 1 — near-term (weeks): consolidate & sharpen

1. **Unified runner** `detectors/run_all.py` — run all detectors, **dedup across
   them**, and merge into one list. A word flagged by several detectors (e.g. both
   consensus and spell_correct) is far more likely a real error — surface that.
2. **One confidence score + tiers (A/B/C)** per candidate from: DCS band, number of
   detectors agreeing, dictionary count/margin, and the confusion-type prior (the
   measured 75/13/8/4 distribution). One ranked report instead of ten.
3. **Review workflow** — an accept/reject HTML over the ranked list: clickable scan
   link per row, keyboard accept/reject, emits the `:y`/`:n` standard format straight
   into [chg_nchg_sep.py](chg_nchg_sep.py) → a submission file. Tracks progress so a
   reviewer can stop and resume.
4. **Run charset / phonotactic / order on raw csl-orig sources** (they validate raw
   text, not just the merged `sanhw1.txt`) — wire them to the dictionary source repo.
5. **Precision spot-check** — hand-verify ~100 band-5 `spell_correct` rows to get a
   real precision number and calibrate the tiers.
6. **Eval harness** — replay the detectors against the **historical** corrections
   (the 2017 `AllvsXX_sf` files + the CORRECTIONS issue history) to measure each
   detector's recall/precision on known fixes.

## Phase 2 — one quarter: scale the verify loop & coverage

1. **OCR-assisted pre-verification** — fetch the scanned page (`servepdf`), OCR the
   headword region, compare to the digital spelling, and pre-label each candidate
   confirm/deny. This is the single biggest lever on the bottleneck. *Caveat:* OCR on
   old Devanāgarī scans is itself error-prone — use it as a triage prior that reorders
   the human queue, never as the final verdict.
2. **Full DCS via `dcs_full.sqlite`** — exact counts (not just bands), inflected-form
   attestation, and POS/morphology to validate stems and disambiguate homonyms
   (sharpening `spell_correct` and especially `dict_vs_corpus`).
3. **Corpus expansion** — add GRETIL / Vedic / more texts so "unattested" is a
   stronger signal and the false-positive rate from corpus gaps drops.
4. **Per-dictionary campaigns** — systematically run the 2026 review-package model
   ([Allvs_2026/](Allvs_2026)) across all general dictionaries.
5. **Submission automation (human-approved)** — turn accepted rows into CORRECTIONS
   change-files / PRs automatically, batched per dictionary; a maintainer merges.
6. **Data-driven confusion model** — recalibrate the edit weights from the actual
   accepted-correction history instead of the o_vs_O priors.

## Phase 3 — long-range vision

1. **Continuous detection** — run the suite on every `sanhw1.txt` refresh / dictionary
   update and surface only the *new* candidates (live Cologne integration).
2. **Morphological-analyzer gate** — wire in **vidyut** (already used in sibling
   projects) to confirm a headword/correction is a well-formed stem: a high-precision
   phonotactic + morphology check beyond the current rules.
3. **Canonical-lemma layer** — align all dictionaries onto canonical lemmas (ties into
   csl-atlas), so a correction propagates across dicts and Patel-convention variants
   resolve once.
4. **Method writeup / open dataset** — the detection methods, the real error taxonomy,
   and the DCS grounding as a citable contribution + a released evaluation set.
5. **Generalize** — extract a reusable Sanskrit spell-check library/CLI usable by
   other Cologne dictionaries and lexicographic projects.

---

## Risks & constraints

- **Maintainer bot-noise sensitivity** → human-gated, batched, low-noise submissions;
  no chatty per-word issues.
- **DCS coverage gaps** → corpus absence is a weak signal; always combine with a
  high-band neighbour (see `dict_vs_corpus` caveats).
- **OCR reliability** on old scans → triage prior, not a verdict.
- **`sanhw1.txt` is regenerated server-side** → treat as a fixed input; coordinate
  refreshes rather than regenerating locally.
- **Some detectors need csl-orig source** (raw dictionary text), which is not in this
  repo — Phase 1.4 depends on access to it.

## Immediate next step

Phase 1.1–1.3 (unified runner → confidence tiers → review workflow) is the highest
leverage: it turns ten scattered candidate streams into one ranked, deduplicated,
reviewable queue and makes the human verification loop fast — which is what actually
gates corrections shipping.
