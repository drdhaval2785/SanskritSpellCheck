# A37 — ARR Responsible NLP + reproducibility checklist

_Created: 10-08-2026 · Last updated: 10-08-2026_

Filled per the checklist gate in
[/paper-submission-pack](https://github.com/gasyoun/claude-config/blob/main/commands/paper-submission-pack.md)
Phase 3.5, under [H2406](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2406-Fable_SanskritSpellCheck_a37-plus5-camera-ready-pack_07.08.26.md).

**Checklist source — a caveat on provenance.** [aclrollingreview.org/responsibleNLPresearch](http://aclrollingreview.org/responsibleNLPresearch/)
was **not reachable from this host on 10-08-2026** (the fetch layer refused both that domain
and `aclanthology.org`). The item families and codes below are therefore taken from the
version last confirmed in this org on **11-07-2026** — page marked *"updated for the ARR
October 2024 cycle"*, as recorded in the skill and in the A44 sibling checklist. The A–E
structure has been stable across cycles, but **re-verify the item wording against the live
page before this file is attached to any ARR-family submission**; do not treat the codes here
as freshly fetched.

**Subject:** [A37_ortho_drift_paper.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A37_ortho_drift_paper.md),
readiness 4/5, target **Digital Scholarship in the Humanities**; and its companion short paper
[A37_lchange_companion.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A37_lchange_companion.md)
("When the S-curve Lies"), readiness 2/5, target the **LChange** workshop.

**Venue calibration.** DSH is not ARR-governed, so for the main manuscript this file is an
**internal quality bar, not a submission artifact**. It matters much more for the
**companion**: LChange is an ACL-workshop venue in the ARR world, so when that paper goes out
this checklist becomes a *formal* attachment. The rows below therefore state both papers'
positions where they differ. Note that LChange's timing is not in this pack's control —
[ACL_METHOD_OPPORTUNITIES_SANSKRIT_2026.md](https://github.com/gasyoun/Uprava/blob/main/ACL_METHOD_OPPORTUNITIES_SANSKRIT_2026.md)
has LChange'27 at CfP-expected ~Oct–Dec 2026, `@WAITING`.

## A. For every submission

| Item | Status | Pointer |
|---|---|---|
| A1. Limitations | **yes**, both papers | A37 has a dedicated **§9 Limitations** with six substantive items, and they are real constraints rather than hedges: regime and language-vitality are **confounded at the "none" tier** (Latin's zero cannot separate "no reform" from "no living usage"); **two regime cells rest on one language each** (Russian n=1, Latin n=1), which is why the paper claims a stratification observed on this corpus and not a law; the modern word-lists are an **uncommitted local dependency**; the dating instrument is the per-era composition, not the absolute rate; token-stream purity varies (BUR/STC inline IAST); the Russian source is external to the Cologne 33 and the æ/œ ligature is typographic, reported separately and excluded from the reform rate. The companion has its own **§7** (small n — German n=5, 4 after the PW/PWG independence correction, English n=14; it does not construct the corrected continuous-trajectory fit; two of five language cells cannot be fit at all). |
| A2. Risks | **yes**, and low by construction | The data is 19th–20th-century public-domain dictionary prose: no personal data, no fairness or privacy surface, no dual-use concern. The one real risk is **methodological harm from over-reading the instrument**, and both papers address it head-on: A37 §5 states the scalar rate is the weak instrument and the per-era composition the strong one, and §4.8 reports the S-curve mechanism inference as a **negative result** rather than a finding. The companion exists specifically to stop others applying a frequency-trajectory model to cross-sectional data and drawing a mechanism conclusion. Also relevant to this family: the project **never edits `csl-orig`** — the work is documentation and search-normalisation only, stated in the Data and reproducibility section. |

## B. Scientific artifacts

Artifacts **used**: the Cologne Digital Sanskrit Dictionaries editions, one external
pre-revolutionary Russian source, the Deutsches Textarchiv `norm` layer, FreEMnorm, and the
Hunspell `de_DE` / `en_GB` / `fr_FR` word-lists. Artifacts **created**: the per-language
drift tables in `ortho_drift/`, the detector, and the drift-dating tool.

| Item | Status | Pointer |
|---|---|---|
| B1. Citation of creators | **yes** | The CDSL editions are named per dictionary with source identifiers; the comparison literature (VARD2, FreEMnorm/Bawden et al., Ghanbarnejad et al., SemEval-2015 DTE, the DTA) is cited in §2 and §6. All eleven in-text citations resolve to References entries and back, checked both directions in the author-voice pass over a list written from verified literature in the [H125 referee pass](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A37_review_fable5.md). **Version/URL specificity is the residual gap**, and it doubles as DSH checklist #4: the Hunspell word-lists are identified by **stem count** (`de_DE` 103,756 stems; the `ropensci/hunspell` `en_GB.dic` snapshot 56,571 stems; `fr_FR`) rather than by release tag or URL. Stem counts are an honest fingerprint, but a release identifier would be better. |
| B2. Licenses / terms | **no** — the same real gap as A44 | Two halves. **Inputs:** no licence statement for the CDSL editions read as input, and the Hunspell word-lists are **deliberately not redistributed for licensing reasons** — correctly handled in substance (the Data availability statement says so plainly) but never stated as a licence *term*. **Created artifacts:** the `ortho_drift/` tables and the detector carry no declared licence, and the repository declares none (see the README "License status"), which is why the `CITATION.cff` drafted for A44 under [H2407](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2407-Fable_SanskritSpellCheck_a44-plus5-camera-ready-pack_07.08.26.md) can state no SPDX identifier truthfully. Since the drift tables are offered for reuse, they should carry an explicit licence. **Remaining work — resolve together with A44's B2 and the `CITATION.cff` gap; it is one decision, not three.** |
| B3. Intended use | **yes** | §3.2's transform-and-check design and §3.3's guardrail state the intended use precisely: the drift measurement is a **dating instrument over gloss metalanguage**, not a corrector of the dictionaries and not a general-purpose historical normaliser (§2 disclaims that subfield explicitly). Consistent with scholarly use of public-domain lexicographic text. |
| B4. Personal info / offensive content | n/a | Historical dictionary prose; no personal data, no human-subject content. |
| B5. Artifact documentation | **yes** | Languages covered are the five gloss metalanguages plus Sanskrit headwords; domain is lexicography; per-dictionary provenance and the full study synthesis live in [docs/ORTHO_DRIFT_FINDINGS.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/ORTHO_DRIFT_FINDINGS.md), with per-language reproduction commands. Demographics are not applicable. The one documentation asymmetry is B1's: inputs are documented by count, not by release identifier. |
| B6. Dataset statistics | **yes** | Exact figures with an explicit pinned standard (2026) throughout: 1832–2009 span; five gloss languages; the Cologne 33 plus one external Russian source; Russian ≈ 358 drifted forms / 1,000 gloss tokens, German ≈ 2.5–10, English/French ≈ 0–0.46, Latin = 0; the SCH-1928 `th`→`ß` composition flip; a 5.5× recall-map expansion used as a robustness check; the S-curve fit's 9.7 yr (English) vs 50.2 yr (German) transition widths. Per-language n is given where it is small (German n=5→4, English n=14, Russian n=1, Latin n=1). |

## C. Computational experiments

The important thing to state here, because it inverts the usual ARR expectation: **A37's
measurement chain contains no model at all.** It is a deterministic detector over committed
text with committed outputs. Language models appear only in the *manuscript's* drafting and
review history, which is family E, not family C.

| Item | Status | Pointer |
|---|---|---|
| C1. Model / infra details | **n/a for the measurement, yes for what exists** | No trained or inferred model, no parameters, no compute budget: the pipeline is [detectors/ortho_drift.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/ortho_drift.py) and [detectors/drift_dating.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/drift_dating.py) run over dictionary text against Hunspell word-lists. Compute is negligible and unremarkable. State this as a property of the setting rather than leaving C1 blank — the honest answer is that the reproducibility burden here falls on **data pinning** (B1) rather than on model reporting. |
| C2. Experimental setup | **yes** | §3.2 defines the transform-and-check procedure and its acceptance criterion; §3.3 states the guardrail; §5 defines the dating test and the DTE distance-band re-expression; §4.8 and companion §2.2 specify the logistic fit and its cross-sectional proxy. No hyperparameter search exists to report — there are no hyperparameters. |
| C3. Descriptive statistics | **yes, and the honesty is load-bearing** | Significance uses the **exact/permutation correction of 2026-07-03** rather than an asymptotic test — the appropriate choice at these n. Robustness is reported against a **5.5× recall-map expansion** (§5). And the headline negative result is itself a statistics-discipline statement: §4.8 reports the S-curve fit as an artifact of cross-sectional sampling, not a mechanism finding, with the caveat placed before the number rather than after it. Residual gap: **no confidence intervals** on the per-language rates, which at n=1 in two cells would be uninformative anyway — say that rather than adding decorative intervals. |
| C4. Package / tool versions | **partial** | The two detector scripts are committed and named with the exact reproduction commands in [docs/ORTHO_DRIFT_FINDINGS.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/ORTHO_DRIFT_FINDINGS.md). Two things would close this fully: **pin a Python version** in the reproducibility section, and **pin the Hunspell word-list releases** (B1) — the latter is the only dependency whose drift could actually move a published number, and the paper already says a different release may shift raw counts without affecting the regime stratification. |

## D. Human annotators and research participants

| Item | Status | Pointer |
|---|---|---|
| D1–D3, D5 | n/a | No annotators, no crowdworkers, no recruited participants, no annotator population. Nothing in either paper rests on human judgement collected as data — the drift measurement is mechanical and the dictionary dates come from title pages. |
| D4. Ethics review | n/a | No human-subjects data collection; nothing to approve or exempt. |

Unlike A44 — whose deferred human-anchor study would activate this whole family if it were
ever run — A37 has **no latent human-subjects component at all**. There is nothing here to
over-claim.

## E. AI assistants

| Item | Status | Pointer |
|---|---|---|
| E1. Disclosure of AI use | **yes in substance, not yet in the manuscript** | The record is unusually complete: the [H125 referee-fix pass](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A37_review_fable5.md), the author-voice pass ([SIGNOFF_A37_author_pass.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/SIGNOFF_A37_author_pass.md), Fable 5 `claude-fable-5`, 11-07-2026, with all thirteen voice calls itemised and vetoable), and the ACL uplift (H826, Sonnet 5 `claude-sonnet-5`, 13-07-2026) are each attributed by tier and exact version in the draft-status blockquote. The author-voice pass additionally verified **mechanically** — numeral and citation-token multiset diff against `origin/master` — that no number, claim, or citation changed. **But** the draft-status blockquote is on the strip-at-submission list, and DSH requires a formal end-matter **AI Disclosure Statement** (its checklist #9). So the disclosure currently lives in scaffolding that is due to be removed: it must be **rewritten as a proper statement** naming tools and versions, describing purpose and extent, separating model-assisted drafting from the model-free measurement chain, and confirming the author verified all generated content. |

## Verdict

**No blocker in the A-family** — A1 and A2 are both properly discharged, and the failure mode
this gate exists to catch (a missing Limitations section) does not apply to either paper.

Remaining work, in order:

1. **B2 — licence declaration**, for the CDSL/Hunspell inputs and, more importantly, for the
   created `ortho_drift/` tables and detector offered for reuse. The only outright `no`, and it
   is the same decision as A44's B2 and the missing `license:` key in the `CITATION.cff` that
   arrives with the A44 pack — one ruling covers all three.
2. **E1 → a real AI Disclosure Statement** in the end matter (also DSH #9), since the current
   disclosure sits in a blockquote scheduled for removal at submission.
3. **B1 / C4 — pin the Hunspell releases and a Python version.** The word-lists are the only
   dependency that could move a published figure; stem counts are a fingerprint, not a version.
4. **C1 / C3 — state the no-model, no-CI position explicitly** rather than leaving the rows to
   look unanswered. Both are properties of the setting, and saying so is stronger than filling
   them with something decorative.
5. **Before any LChange submission:** re-verify the item wording against the live ARR page
   (unreachable from this host today), and confirm the companion's own open gates — venue
   confirmation against the current call, and the author read-through.

_Dr. Mārcis Gasūns_
