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

---

## 🔭 Open / newly-raised

- **O1 — Inline body check in the ranker.** R1 showed the engine mis-ranks minimal pairs because it
  lacks the body. Could a *cheap per-candidate body lookup* (the `EntryIndex` already exists) gate the
  ranker so the engine itself never elevates a `patra`/`pAtra` pair — closing the tier-C gap without
  a full LLM triage?
- **O2 — A better attestation signal than DCS-band-0.** The tier-C promotion failed partly on DCS
  coverage gaps. Would an inflection-aware attestation (vidyut-expanded) or a larger corpus make
  `suspect-not-attested` reliable enough to promote safely?
- **O3 — Re-run German with the 15,685-form map.** The DTA long tail now dwarfs the dictionaries' own
  drift forms. Re-running the German cluster would reclassify residuals as known drift — does German
  drift-*recall* rise materially, and does the SCH-1928 control still hold (does the bigger map blur
  the era-dating)?
- **O4 — Drift-rate as a dating tool.** The monotone WIL 0.57 → PD 0.00 gradient suggests drift/1k ↔
  year is calibratable. Could the metric *date* an undated/anonymous dictionary, edition, or textual
  stratum from its drift rate alone?
- **O5 — Separate ligatures from reform.** The dominant "drift" in several English dicts is the æ/œ
  ligature (SHS 109, MW72 92, VEI 12), which is *typographic*, not orthographic reform. Splitting a
  `ligature` class from `reform` would stop it inflating the reform signal.
- **O6 — Language-general reform maps.** The transform-and-check + corpus-norm-merge pipeline (H4+H6)
  is language-agnostic. Could it build reform maps for English (EEBO/ECCO), French (Frantext), etc.,
  from their diachronic corpora — turning the study into a reusable method, not a one-corpus result?
- **O7 — Does OCR pre-verify actually help the human?** Task 1 (the CORRECTIONS umbrella issue) plans
  to pre-filter the 122 FILE-FIRST candidates with `ocr_verify` (CONFIRM/DENY/UNCERTAIN). Open
  question: is OCR of old Devanāgarī scans reliable enough to *trust as a pre-filter*, or does it
  produce too many UNCERTAIN to reduce the human scan-verification load?
