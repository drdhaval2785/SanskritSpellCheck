# SanskritSpellCheck — hypothesis ledger

This project is a sequence of **testable hypotheses** about two questions: *how do you find
digitization errors in a dictionary you don't have ground truth for?* and *how do you measure
orthographic change across a multilingual lexicography corpus?* This file records each hypothesis,
how it was tested, the verdict, the evidence (with numbers), and what it opened up next — including
the **negative results**, which are as load-bearing as the confirmations.

Format per entry: **Hypothesis → Test → Verdict → Evidence → Consequence.**

Cross-refs: methodology + numbers in [ORTHO_DRIFT_FINDINGS.md](ORTHO_DRIFT_FINDINGS.md); task recipes
in [../USE_CASES.md](../USE_CASES.md); per-dict triage results in
[../corrections_draft/README.md](../corrections_draft/README.md).

---

## ✅ Confirmed

### H1 — The dictionary's *own entry text* is ground truth for "typo vs. real word"
A spelling/corpus detector cannot tell a typo from a real word, an intentional variant, or editorial
apparatus; the **entry body** can.
- **Test:** body-grounded hybrid triage (`/dict-triage`): classify each tier-A candidate against the
  csl-orig entry text (Sonnet), source-confirm the TYPO pile (Opus), adversarial review (Opus).
- **Verdict:** confirmed, decisively. Run on **all 33 dictionaries**.
- **Evidence:** the body pass caught false positives that spelling+corpus had "confirmed" — MW
  `marga` = a `w.r.` apparatus entry, `muka` = "smell of cow-dung" (a real word), `vinAsa` =
  "noseless". The Opus review gate held back every borderline b/v and vṛddhi case (PW `dASaSiras`,
  PWG `ketunAlin`, STC `bibhīṣaṇa`).
- **Consequence:** the body is the arbiter the rest of the pipeline defers to (see R1).

### H2 — Tier-A precision is near-zero on mature dictionaries, high on poorly-digitised ones
The engine's "tier A" is high *engine confidence*, not precision; precision depends on the source.
- **Test:** count body-confirmed fileable typos per dict across all 33.
- **Verdict:** confirmed, with a sharp split.
- **Evidence:** mature/much-corrected: **MW 4/1954, PW 2/657, VCP 1/563, BHS 0/713, PD 0/1007**.
  Poorly-digitised: **SHS (1900) 37/246 ≈ 15%, YAT (1846) 27/247 ≈ 11%, ACC 22/174, PWG 12/497 ≈
  2.4%** — each error confirmed by the entry's *own* etymology/citation.
- **Consequence:** triage effort should target poorly-digitised sources for real typos; on mature
  dicts the value is elsewhere (H3).

### H3 — The durable deliverable is the *do-not-file* list, not the handful of typos
Preventing bad bulk edits is worth more than the few corrections.
- **Test:** synthesize a per-dict `*_wrong_readings.txt` (documented-intentional spellings, grouped
  by sub-type) and fold it into the detector whitelist; measure false-positives.
- **Verdict:** confirmed.
- **Evidence:** **122 fileable typos vs ~2,549 documented-intentional spellings** across the 33 dicts.
  The do-not-file headwords became a **2,297-word suppression layer** (`gen_do_not_file_suppress.py` →
  `nochange/do_not_file_suppress.txt`), and `eval.py` false-positives are **0** for all four
  correctors after `run_all.py --rerun`. PD alone contributed 116 (66 v.l. + 16 w.r.).
- **Consequence:** every future detector run is permanently cleaner; the lists are the asset.

### H4 — Orthographic-drift magnitude is a function of reform *type*, not merely age
- **Test:** `ortho_drift.py` transform-and-check on gloss tokens vs a 2026 reference, across five
  gloss languages (de/en/fr/la/ru).
- **Verdict:** confirmed — 1–3 orders of magnitude, tracking *how* a language reformed.
- **Evidence:** **legislated** (Russian 1918 ≈ 358/1k; German 1901/96) **≫ convention** (English
  ≤ 0.57/1k, French ≤ 0.31) **≫ none** (Latin = 0, the negative control).
- **Consequence:** drift is a *documentation/search-normalization* signal, never a correction list.

### H5 — The drift metric dates a dictionary's orthographic *epoch* (it isn't flagging noise)
- **Test:** two controls — the **SCH-1928** internal control, and a **recency control** (modern dicts
  should be ≈ 0).
- **Verdict:** confirmed by both.
- **Evidence:** SCH (1928) flips from 1901-`th` dominance to 1996-`ß` dominance, correctly dating it
  post-1901. Recency control: **PD (1976–2009, 1.32 M tokens) = 0.00/1k**, PE/BHS/IEG = 0.00, VEI
  0.06 — yielding a monotone gradient **WIL 1832 (0.57) → MW 1899 (0.01) → modern (0.00)**.
- **Consequence:** opens O4 (drift-rate as a *dating* tool).
- **Significance (2026-07-03, exact test):** the *scalar-rate* dater is real but weaker than the
  t-approximation implied — German ρ=−0.975 is significant at **exact permutation p=0.033** (not
  scipy's invalid-at-n=5 p=0.005), English at p=0.016 (Monte-Carlo). So H5's fine dating rests on
  the SCH-style **per-era composition**, not the n=5 scalar gradient. See `drift_dating.py::exact_spearman_p`.

### H6 — A diachronic corpus's normalization layer yields valid reform pairs after dic-validation + frequency thresholding
- **Test:** harvest `surface ≠ DTA::CAB-norm` pairs from the Deutsches Textarchiv lingattr-TEI corpus
  (`extract_dta_pairs.py`), keep frequency ≥ 20×, dic-validate (`merge_reform_pairs.py`: old ∉ de_DE
  & new ∈ de_DE).
- **Verdict:** confirmed — clean, large yield.
- **Evidence:** 596 k distinct pairs → ≥ 20× (43,579) → **+12,862 accepted**, growing
  `de_reform_map.tsv` **2,823 → 15,685 forms**. Accepted set is textbook (`vnd→und`, `bey→bei`,
  `Theil→Teil`, `krafft→kraft`, `thaler→taler`, `creutz→kreuz`); the ≥20× cut removes OCR singletons
  (`aaal→all`), which dic-validation alone could not (both pass `old∉dic & new∈dic`).
- **Consequence:** frequency is the precision lever the dictionary itself lacks; opens O3, O6.

### H7 — A dictionary outside the csl-orig merge can be triaged via an external-source shim
- **Test:** stage PD (Deccan College *Encyclopaedic Dictionary*, CC BY-NC-SA, 107,630 entries) in a
  gitignored `external_src/`, resolved by `triage_util.source_file()` (external override → csl-orig
  fallback); run the standard pipeline.
- **Verdict:** confirmed — behaviour-preserving for every existing dict (25/25 tests, MW unchanged),
  PD fully triageable (1007 tier-A, 0 unlocatable).
- **Consequence:** the same shim takes any future non-csl-orig source (incl. PD's optional 2nd).

---

## ❌ Refuted / failed (the negative results)

### R1 — Corpus + confusion signal can promote a tier-C candidate to B
*Hypothesis:* lift a single-detector C-candidate to B when the suggestion is a frequent DCS lemma
(band ≥ 4), the suspect is unattested, and the edit is a high-weight confusion class — surfacing true
errors higher.
- **Test:** implemented the promotion in `run_all.score_tier`; measured with `eval.py`.
- **Verdict:** **refuted as unsafe.** The promotion's headline metrics looked fine (602 candidates
  C→B, tier-A unchanged, FP = 0), but the promoted set is wrong.
- **Evidence:** it surfaces **real Sanskrit minimal pairs as if typos** — `patra` (leaf) vs `pAtra`
  (vessel); `vata` and `rAtrI` are **real MW headwords** (`<L>185376`, `<L>177124`). Two root causes:
  (a) vowel-length pairs are exactly where spelling+corpus *cannot* adjudicate — that is H1's whole
  reason; (b) `suspect_band == 0` is unreliable (DCS coverage gaps make common words look unattested).
  And the single-detector pairs the corpus *can* vouch for (band ≥ 3) are **already tier B**, so the
  C-stuck known o_vs_O pairs (99 % single-`spell_correct`, band 0–2) gain ≈ nothing.
- **Consequence:** reverted the tier change; kept corroboration only as a within-tier **ranking
  nudge** (`CORROB_*`). Opens O1, O2. **Do not re-attempt corpus-based tier-C promotion** — it is a
  ceiling, not a tuning problem.

### R2 — A vidyut morphology check is a reliable tier *promoter*
*Hypothesis:* if the suggestion is a valid vidyut stem and the suspect is not, promote it.
- **Verdict:** refuted / demoted. Only ~6.6 % of dictionary headwords are pratipadikas, and inflected
  suspects (`rAjA`) look "not a stem", so an `or morph` tier-A trigger over-promoted inflection
  non-errors (`rAjA→rAja`).
- **Consequence:** kept as an informational **tag + ranking nudge**, never a tier promoter — the same
  shape R1 later arrived at independently.

### R3 — Re-running the body-aware TYPO pass improves recall
- **Verdict:** refuted for single runs. The TYPO pass is **stochastic**: re-runs surface a different
  small handful and can *lose* genuine typos (an MW re-run once refuted 4 verified typos).
- **Consequence:** never blindly overwrite a committed package; for recall, *union across runs*. The
  deterministic marker layer (apparatus/redirect detection) is the stable backbone.

### R4 — The base DTA TEI carries the reform normalization
- **Verdict:** refuted by a cheap probe (downloaded the 274 MB base subset first). The base DTABf TEI
  has only `<sic>/<corr>` printer-error corrections (`Bort→Brot`), **not** the systematic `@norm`
  reform layer — those are typos, not 1901/96 drift.
- **Consequence:** confirmed the 2.5 GB lingattr-TEI was required *before* paying for it; saved a
  wrong 2.5 GB download. The lesson: probe the cheapest artifact for the signal first.

### R5 — A cheap, model-free body lookup in the ranker can demote real-word minimal pairs (was O1)
*Hypothesis:* R1 mis-ranks `patra`/`pAtra` because the engine lacks the body. Wire a *deterministic*
per-candidate `EntryIndex` body lookup into `score_tier` — if the suspect has its own real definition,
demote it — to fix R1 without a full LLM triage. Goal: fewer real-word candidates in tier A/B, no loss
of known o_vs_O pairs.
- **Test:** probed every candidate body signal against the 3,884 known o_vs_O pairs (the real errors
  that must stay) vs the rest, in tiers A/B, before changing any code.
- **Verdict:** **refuted — no model-free body signal separates the two classes.** Three independent
  signals all fail:
  1. **Body presence/length** — known *real errors* carry substantive glosses at the **same** rate as
     everything else (tier A: 83 % vs 82 % at >= 40 chars; tier B: 78 % vs 79 %). A typo'd headword in
     a poorly-digitised dict has a full definition too — presence cannot tell it from a real word.
  2. **DCS attestation of the suspect** — the real words it must protect are themselves band-0:
     `patra`, `vata` are **absent from DCS-2021** (band 0) while `pAtra`/`vAta`/`deva` are band 5. So
     "suspect attested => real word" misses exactly the words R1 cares about (R1's coverage-gap cause).
  3. **Suspect-vs-suggestion body overlap** — both classes have low overlap (tier A: known <= 0.1 =
     89 % vs other 90 %); in tier B it **inverts** (known 88 % vs other 49 %), so demoting low-overlap
     would drop *more* known errors than candidates.
  - **Tightest conjunction** (the exact `patra` signature: tier-B, single-detector, `best_band >= 3`-
    promoted, body >= 40 chars) still demotes **60 known real errors** (20 % of tier-B known pairs) to
    catch 244 *unverified* others — and since tier-A/B precision is already near-zero on mature dicts
    (H2), most of those 244 are likely real errors too. No clean win exists.
- **Consequence:** **made no change to `score_tier`** — any deterministic demotion trades known-error
  recall 1-for-<=4 against unverified precision. The body must be *read* (the LLM body-grounded
  triage), not measured; R1's gap is a semantic ceiling, not a ranker-tuning problem. Confirms H1 from
  the ranker side. Do not re-attempt a deterministic body/attestation gate in the scorer.

### R6 — vidyut inflection-aware attestation is a reliable "real word" signal (was O2)
*Hypothesis:* R1/R5 failed partly because DCS band-0 mislabels real words (`patra`, `vata`) as
unattested. A morphologically-aware oracle — the vidyut **Kosha** (`get()` = is this a valid *pada*),
plus the vendored 205 k pratipadika **stems** — should recognise those real words, making
"suspect-not-attested" reliable enough to promote (or "attested" reliable enough to demote).
- **Test:** `vidyut.kosha.Kosha.get` + `vidyut_stems.txt`, on the tier-A/B suspects, known o_vs_O
  real-errors vs the rest (vidyut 0.4.0 + kosha data both on disk).
- **Verdict:** **refuted — attestation cross-cuts the real-word/typo distinction.** It fails in *both*
  directions:
  1. **Still misses real words.** `patra` is unattested by every oracle (DCS 0, stem ✗, pada ✗) — the
     kosha lacks the bare neuter stem just as DCS did. (`vata` *is* rescued — partial, not reliable.)
  2. **Over-attests real errors.** **34 % of tier-A and 47 % of tier-B known real-error suspects are
     valid vidyut stems/padas** — in a richly inflected language a misspelling frequently lands on a
     coincidentally-valid form. In tier B attestation fires *more* on errors (47 %) than on others
     (39 %). A "demote if vidyut-attested" rule would drop **~404 known real errors** (266 A + 138 B) —
     far worse than R5's body rule (60); "promote if not-attested" would promote `patra` and miss
     ~40 % of real errors.
- **Consequence:** **no change to the scorer.** vidyut attestation answers "is this string a valid
  Sanskrit form?", which is **orthogonal** to "is this entry a typo?" — most typos are valid forms of
  *something*. Confirms R5/H1 from the morphology side: surface attestation (DCS *or* vidyut) cannot
  replace reading the body. vidyut stays a display/PPP-validation aid + ranking nudge (R2), not an
  attestation gate. Do not re-attempt corpus/morphology attestation as a tier signal.

---

## 🔭 Open / newly-raised

- ~~**O1 — Inline body check in the ranker.**~~ **→ refuted, now [R5](#r5--a-cheap-model-free-body-lookup-in-the-ranker-can-demote-real-word-minimal-pairs-was-o1).**
  No model-free body signal (presence/length, DCS attestation, suspect↔suggestion overlap) separates
  real-word minimal pairs from typos without an equal hit to known-error recall.
- ~~**O2 — A better attestation signal than DCS-band-0.**~~ **→ refuted, now [R6](#r6--vidyut-inflection-aware-attestation-is-a-reliable-real-word-signal-was-o2).**
  vidyut Kosha/stem attestation still misses real words (`patra`) AND over-attests real errors (34–47 %
  of known typos are valid forms) — surface attestation is orthogonal to typo-vs-real. The R5 caveat
  held.
- ~~**O3 — Re-run German with the 15,685-form map.**~~ **✅ done (2026-06-26).** Rates ~triple and the
  top-of-gradient monotone ordering flattens (GRA > PWG), but the SCH-1928 era-dating control is fully
  intact — vindicates freezing the per-dict gradient. See `ORTHO_DRIFT_FINDINGS.md` "O3".
- ~~**O4 — Drift-rate as a dating tool.**~~ **✅ done (2026-06-26) — confirmed but coarse.** drift/1k
  *is* a dating signal, but **regime-bounded**: no cross-language calibration (rate stratifies by
  reform type — RU 358 ≫ DE 2.5–10 ≫ EN/FR ≤0.46 ≫ LA 0); within a language the **legislated** German
  gradient is tight (Spearman −0.975, leave-one-out **±15 yr**) while the **convention** English one is
  editor-noisy and saturates to 0 (−0.642, ±40 yr; 7 dicts at exactly 0.00 across 1890–1990). The
  per-era *composition* out-dates the scalar rate (the SCH-1928 control). So it places a text on its
  own language's pre-/post-reform timeline, not a year. See `ORTHO_DRIFT_FINDINGS.md` "O4"
  ([drift_dating.py](../detectors/drift_dating.py)).
- ~~**O5 — Separate ligatures from reform.**~~ **✅ done (2026-06-26).** Added `NONREFORM_ERAS` so the
  æ/œ ligature is its own column, excluded from reform-drift/1k; mid-tier EN dicts (ligature-dominated)
  collapse to ≈0 reform. See `ORTHO_DRIFT_FINDINGS.md` EN section.
- ~~**O6 — Language-general reform maps.**~~ **✅ done for French (2026-06-26) — method yes, map
  epoch-bound.** The `extract → dic-validate → merge` pipeline generalised with no per-language code:
  the free 17th-c. [FreEMnorm](https://github.com/FreEM-corpora/FreEMnorm) corpus yielded 236
  dic-validated EMF→modern French pairs (`fr` map 18→254). But the resulting map is **not** safe on the
  19th–20c French Cologne dicts (BUR/STC): ~90 % false positives from epoch/register/language mismatch
  (abbreviation `moy.`=*moyen*, homograph `dés`=dice / Latin `tres`, inline-IAST `pha`/`phull`). A
  reform map needs a source corpus matched in epoch + register + script to the target. Validated pairs
  kept as an artifact; canonical fr map frozen (O3 pattern). See `ORTHO_DRIFT_FINDINGS.md` "O6"
  ([extract_freem_pairs.py](../detectors/extract_freem_pairs.py)).
- **O7 — Does OCR pre-verify actually help the human?** Task 1 (the CORRECTIONS umbrella issue) plans
  to pre-filter the 122 FILE-FIRST candidates with `ocr_verify` (CONFIRM/DENY/UNCERTAIN). Open
  question: is OCR of old Devanāgarī scans reliable enough to *trust as a pre-filter*, or does it
  produce too many UNCERTAIN to reduce the human scan-verification load?
