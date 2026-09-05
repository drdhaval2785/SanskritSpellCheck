_Created: 10-08-2026 · Last updated: 05-09-2026_

# SanskritSpellCheck — hypothesis ledger

This project is a sequence of **testable hypotheses** about two questions: *how do you find
digitization errors in a dictionary you don't have ground truth for?* and *how do you measure
orthographic change across a multilingual lexicography corpus?* This file records each hypothesis,
how it was tested, the verdict, the evidence (with numbers), and what it opened up next — including
the **negative results**, which are as load-bearing as the confirmations.

Format per entry: **Hypothesis → Test → Verdict → Evidence → Consequence.**

Cross-refs: methodology + numbers in [ORTHO_DRIFT_FINDINGS.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/ORTHO_DRIFT_FINDINGS.md); task recipes
in [../USE_CASES.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/USE_CASES.md); per-dict triage results in
[../corrections_draft/README.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/README.md).

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
- **Caveat added 26-07-2026 ([H9](#h9-union-across-runs-materially-raises-recall-one-run-recovers-only-13-of-the-two-run-union)):**
  every count above is one stochastic draw, so they are **lower bounds**. A second run lifts SHS 37→68,
  YAT 27→61, ACC 22→27 in union. The high-vs-low split this entry rests on is unaffected; the absolute
  numbers are not the ceiling.

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

### H8 — Tied-field cross-encoding consistency (SLP1 ↔ Devanāgarī ↔ IAST) is a viable new detector shape
[Bloodgood & Strauss, arXiv 1602.07807](https://arxiv.org/abs/1602.07807) (IEEE ICSC 2016) — the
project's direct methodological ancestor for XML-dictionary anomaly detection — has one detector
shape this project lacked: **tied-field consistency**, checking that two fields expected to encode
the same content actually agree. For CDSL that is SLP1-headword ↔ its Devanāgarī rendering ↔ its
IAST rendering.
- **Test (H827, ACL roadmap rev 3 ruling D14 — full build across all 33 dicts):**
  [detectors/tied_field_check.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/tied_field_check.py) round-trips every in-alphabet
  `sanhw1.txt` headword through both SLP1→Devanāgarī→SLP1 and SLP1→IAST→SLP1 (the shared
  `sanskrit-util` package's `slp1_to_devanagari`/`deva_to_slp1` and `from_slp1`/`to_slp1`, new thin
  wrappers added to `slp1util.py`), flagging any headword whose round-trip does not return the
  original. Wired into `run_all.py` as the 11th detector family (`tied_field`, high-precision —
  alongside `phonotactic`/`charset`); `eval.py`'s filing gate still **PASS** (FP unaffected — the
  detector's own suspects file was empty, see Evidence).
- **Two round-trip asymmetries are documented PROPERTIES of the transcoders, not data errors, and
  are suppressed** (do-not-file, not filed as candidates): (1) Devanāgarī path — candrabindu `~` and
  avagraha `'` are not round-trip stable (both collapse into Devanāgarī's single nasalization /
  elision slot); (2) IAST path — IAST re-spells SLP1's single-character aspirates/diphthongs
  (K/G/C/J/W/Q/T/D/P/B, E/O) as two-letter digraphs, so a genuine plain-stop+`h` sequence at a
  compound/sandhi boundary (`vAk`+`hasta` → `vAkhasta`) or vowel hiatus (`a`+`i`) reads through IAST
  identically to the digraph and reads back as the single aspirate/diphthong — an inherent one-way
  lossiness of concatenative IAST, not a bug.
- **Verdict:** confirmed — the detector shape is real, correctly implemented, and its suppression
  rules are exact, not approximate.
- **Evidence:** full run across all **431,596** `sanhw1.txt` lines (431,568 unique in-alphabet
  headwords): **0 unsuppressed tied-field disagreements.** Every round-trip mismatch is fully
  explained by the two documented asymmetries above — 12 by candrabindu/avagraha (Devanāgarī path),
  100 by the digraph/hiatus ambiguity (IAST path) — with **zero unexplained residual** at this scale.
  This is an honest **negative finding on error discovery** (the shared `sanskrit-util` transcoder is
  round-trip consistent across the full unified headword population — itself a useful validation of
  that package at scale) but a **positive finding on methodology**: the detector correctly
  discriminates genuine defects from normalization axes, it just found no genuine defects because
  sanhw1.txt carries no independently-authored Devanāgarī/IAST field to disagree with the SLP1 it was
  derived from — only the SLP1 headword exists as stored data; the other two encodings are always
  *derived* by the same trusted transcoder, so under a correct transcoder they cannot disagree by
  construction.
- **Consequence:** ships as a real 11th detector (zero regression risk — it can only ever raise its
  hand on an actual transcoder defect or a genuinely un-derivable headword) with a documented
  do-not-file catalogue entry for the two asymmetry classes. The genuinely interesting version of
  this check — a *stored* Devanāgarī/IAST field disagreeing with SLP1 — needs a data source this repo
  doesn't currently have (e.g. an independently-keyed citation-form field); flagged as a follow-up if
  one is ever ingested.

---

### H9 — Union-across-runs materially raises recall: one run recovers only ~1/3 of the two-run union
[R3](#r3-re-running-the-body-aware-typo-pass-improves-recall) refuted *re-running* and prescribed
*unioning* instead, but the size of the gain was never measured. Roadmap ruling **D7** ordered it
measured at reduced scope — two extra runs on the three high-yield dicts (SHS/YAT/ACC) — and the line
closed either way.
- **Test:** one further independent body-aware run per dict, same pipeline and per-phase models as run 1
  (Sonnet 5 `claude-sonnet-5` classify → Opus 4.8 `claude-opus-4-8` source-confirm → Opus 4.8 adversarial
  review), from byte-identical deterministic prep. The committed packages were **never overwritten**:
  `triage_synthesize.py` would have replaced `<DICT>_file_first_sf.txt` with run 2's verdicts and
  silently destroyed run 1's finds, so [union_across_runs.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/union_across_runs.py)
  reconstructs run 2's FILE-FIRST set from the gitignored `triage_work/` verdicts using
  `triage_synthesize.py`'s own rule — `confirm.is_typo ∧ (review absent ∨ review.fileable)` — making the
  two runs comparable like for like.
- **Verdict:** **confirmed**, and the instability is far larger than R3's "a different small handful"
  suggested.
- **Evidence:** 563 candidates re-judged; agreement is *set overlap ÷ union* (Jaccard).

| dict | run 1 (committed) | run 2 | in both | **net-new** | run-1-only | union | agreement |
|---|---|---|---|---|---|---|---|
| SHS | 37 | 63 | 32 | **31** | 5 | 68 | 47% |
| YAT | 27 | 46 | 12 | **34** | 15 | 61 | 20% |
| ACC | 22 | 15 | 10 | **5** | 12 | 27 | 37% |
| **total** | **86** | **124** | **54** | **+70 (+81%)** | **32** | **156** | **35%** |

  The gap is not an artifact of a shifting candidate pool: **0** of the 86 run-1 rows have dropped out of
  today's tier A, and exactly 1 (SHS) is now settled deterministically before the LLM sees it — so 31 of
  the 32 non-reproductions are genuine run-to-run variance. Nor is the net-new set noise: **10 of 10**
  hand-checked net-new are real typos contradicted by the entry's own text — SHS `dibA`→`divA`
  (`E. div`), `pranipAta`→`praRipAta` (ṇatva; cf. adjacent `praRipAtarasa`), `jamBari`→`jamBAri`
  (`E. jamBa + ari`), `nErASyA`→`nErASya` (neuter `-SyaM`); YAT `viqbarAha`→`viqvarAha` ("a tame hog"),
  `vAbadUka`→`vAvadUka` (next entry `vAvadUkatA` "Garrulity"), `AkASabartman`→`AkASavartman`
  ("Firmament"), `avedabid`→`avedavid` ("not knowing the vedas"), `advEzwf`→`advezwf` (*dveṣṭṛ* has e,
  not ai), `nirAlamva`→`nirAlamba` ("self-supported"). **The misses run both ways:** run 2 failed to
  re-find ACC `EtareyavrAhmaRa`→`EtareyabrAhmaRa` and `SatapaTavrAhmaRa`→`SatapaTabrAhmaRa` — two
  unmistakable *Brāhmaṇa* b/v errors run 1 had caught. Neither run dominates; the union beats both.
- **Consequence:** union, never replace — now with a number attached. The union table is
  [corrections_draft/union_d7.tsv](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/union_d7.tsv) (156 rows; every net-new row
  carries its Opus confirm reason **and** its Opus review verdict + false-positive type, the adjudication
  gate D7 required for new candidates). Three consequences follow:
  1. **[H2](#h2-tier-a-precision-is-near-zero-on-mature-dictionaries-high-on-poorly-digitised-ones)'s
     per-dict counts are single-draw lower bounds, not populations.** For these three dicts the fileable
     count is ≥156, not 86 — SHS ≈68 not 37, YAT ≈61 not 27. The *ordering* (poorly-digitised ≫ mature)
     is unaffected.
  2. **The human scan-verification queue nearly doubles** for these three: the existing 109-row sheet
     (H454) is short by the 70 net-new and should be regenerated before the batch-PR switchover files
     anything.
  3. **The roadmap's "full generous-budget union across all 11 fileable dicts" non-goal deserves
     re-opening** — it was ruled out on *precision* grounds, which this does not contest; the argument
     for it is now *recall*, and it is a much stronger one. Still a human call, not an agent's.
  The residual caution is unchanged: FILE-FIRST is a triage prior, and the scan is the arbiter.

#### H9 scale-up (ruling D9, 04-08-2026) — the gain replicates, but its *size* tracks digitisation quality

Consequence 3 above ("the non-goal deserves re-opening") was ruled by MG on 26-07-2026 — funded, and
on a *contamination* argument rather than a recall one: an uncorrected typo headword flows into the
cross-dict union headword list, inflating its own attestation count and thereby helping
`run_all.py` demote it out of tier A. A typo left unfixed suppresses its own detection.
Scope call: the eight remaining fileable dicts (the 22 zero-fileable ones deliberately left to a
cheap probe). Same pipeline and prep, per-phase models Sonnet 5 (`claude-sonnet-5`) classify →
Opus 5 (`claude-opus-5`) source-confirm → Opus 5 adversarial review; 3,045 candidates re-judged.

| dict | run 1 | run 2 | both | **net-new** | r1-only | union | agreement |
|---|--:|--:|--:|--:|--:|--:|--:|
| PWG | 12 | 11 | 7 | **4** | 5 | 16 | 44% |
| WIL | 3 | 3 | 1 | **2** | 2 | 5 | 20% |
| SKD | 3 | 2 | 1 | **1** | 2 | 4 | 25% |
| GST | 1 | 1 | 0 | **1** | 1 | 2 | 0% |
| MCI | 10 | 9 | 9 | 0 | 1 | 10 | 90% |
| MW | 4 | 0 | 0 | 0 | 4 | 4 | 0% |
| PW | 2 | 0 | 0 | 0 | 2 | 2 | 0% |
| VCP | 1 | 0 | 0 | 0 | 1 | 1 | 0% |
| **total** | **36** | **26** | **18** | **+8 (+22%)** | **18** | **44** | **41%** |

- **The instability replicates** — 41% agreement here against D7's 35%, and again *none* of it is a
  pool artifact: `r1:pool` = 0 and `r1:settled` = 0 for all eight, so all 18 non-reproductions are
  genuine run-to-run variance. **8 of 8 net-new hand-verified** (the whole set, where D7 could
  only afford 10 of 70), in two checkable classes: the entry's `<lex>` gender tag contradicting the
  headword's final vowel (PWG `citrikA`→`citrika`, `kxptakIla`→`kxptakIlA`, `mAlArizwa`→`mAlArizwA`;
  SKD `mahotka`→`mahotkA`), and the entry's own derivation spelling the base differently
  (PWG `pARivanDa`→`pARibanDa`; GST `aDoGaRWA`→`aDoGaRwA`; WIL `paYcaSErizaka`→`paYcaSErIzaka`,
  `vapuzmAt`→`vapuzmat`).
- **But the magnitude is a function of digitisation quality, not a constant.** +22% here vs D7's
  +81%. That is the [H2](#h2-tier-a-precision-is-near-zero-on-mature-dictionaries-high-on-poorly-digitised-ones)
  axis reappearing inside H9: on mature dicts both runs find little, so the union adds little.
  PWG — the sole poorly-digitised source in this set — yields half the net-new off 11% of the volume.
  **So "+81%" must not be quoted as the expected union gain for a dictionary; quote it for
  poorly-digitised sources and ~+22% for mature ones.** Combined across both passes: 11 dicts,
  122 → 200 fileable (+78, +64%).
- **A single run's near-zero on a mature dict is as much noise as signal.** MW, PW and VCP each
  returned a run-2 zero against a non-zero committed count — 7 committed typos not reproduced,
  none explicable by pool movement. This *strengthens* H2's ordering while further undermining its
  per-dict counts: the ranking is stable, the numbers are draws.
- **Two silent-failure modes found in the workflow's reporting layer** (details in
  [UNION_ACROSS_RUNS_D9_SCALEUP_SCOPE_AND_RESULTS.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/UNION_ACROSS_RUNS_D9_SCALEUP_SCOPE_AND_RESULTS.md)):
  a dropped Confirm batch reads as `confirmedTypos: 0`, indistinguishable from a real zero unless
  read off disk; and a classify agent can return verdicts without writing its `body_adj_*.json`
  (MW batch 000, WIL batch 003), leaving a full-looking classified count with a hole in the
  reproducibility trail. Audit `body_batch_NNN.jsonl` ⇄ `body_adj_NNN.json` before trusting a union.
- **The scope question this left open is now CLOSED (04-08-2026, H2281): do NOT sweep the 22
  zero-fileable dicts.** Probe on the two highest-volume ones — BHS (551 candidates re-judged)
  and SCH (644) — returned **0 fileable each**, matching their committed zeros. 1,195 candidates,
  23 surviving the classify stage, **0 confirmed at source**. The pipeline was not inert: it
  produced a normal TYPO pile both times, which then failed against the full entry.
  **These zeros are structural, not stochastic**, and the two dicts fail differently: **BHS**
  carries its own critical apparatus and has already labelled its misprints (`[laṭikā, app.
  misprint for latikā (so Index)]`, `[Anantaryasamādhi, misprint in Mvy 901 … corrected in
  Index]`), so the detector re-finds what Edgerton annotated and a "correction" would destroy
  the apparatus; **SCH** corroborates the headword in its own body (`girī` a cvi-adverb,
  `samadhurA` a feminine, `yudda` = *yud+da* "battle-giving"), so the minimal-pair suggestion is
  simply wrong. Neither is a coin-flip a third run might land differently — which is precisely
  what separates this from the SHS/YAT/ACC instability measured above, and is the sharpest
  available statement of
  [H2](#h2-tier-a-precision-is-near-zero-on-mature-dictionaries-high-on-poorly-digitised-ones):
  **a zero-fileable verdict on a self-documenting or internally-corroborating lexicon is a
  property of the dictionary, not a draw.** Limit: 2 of 22 tested, deliberately the two most
  likely to yield; the other 20 are smaller and mostly the same mature/foreign-gloss/specialist
  kinds. Evidence for all 23 refutations:
  [REFUTED_TYPO_CANDIDATES_PROBE22.tsv](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/REFUTED_TYPO_CANDIDATES_PROBE22.tsv).
- **Consequence:** the scan-verification sheet is now short by these 8 as well as D7's 70;
  regenerate before the batched-PR switchover files anything. The contamination loop D9 names is
  only closed once corrections are *filed* and `HeadwordLists/union/` is rebuilt in
  [SanskritLexicography](https://github.com/gasyoun/SanskritLexicography) — which runs through the
  monthly batched csl-orig PR and its human scan gate, not through this repo.

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
- **Quantified 26-07-2026 by [H9](#h9-union-across-runs-materially-raises-recall-one-run-recovers-only-13-of-the-two-run-union)**
  (roadmap D7): the union is worth **+81%** on SHS/YAT/ACC and single-run agreement is only **35%** —
  the "different small handful" is in fact most of the set.

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

- ~~**O1 — Inline body check in the ranker.**~~ **→ refuted, now [R5](#r5-a-cheap-model-free-body-lookup-in-the-ranker-can-demote-real-word-minimal-pairs-was-o1).**
  No model-free body signal (presence/length, DCS attestation, suspect↔suggestion overlap) separates
  real-word minimal pairs from typos without an equal hit to known-error recall.
- ~~**O2 — A better attestation signal than DCS-band-0.**~~ **→ refuted, now [R6](#r6-vidyut-inflection-aware-attestation-is-a-reliable-real-word-signal-was-o2).**
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
  ([drift_dating.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/drift_dating.py)).
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
  ([extract_freem_pairs.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/extract_freem_pairs.py)).
- **O7 — Does OCR pre-verify actually help the human?** Task 1 (the CORRECTIONS umbrella issue) plans
  to pre-filter the 122 FILE-FIRST candidates with `ocr_verify` (CONFIRM/DENY/UNCERTAIN). Open
  question: is OCR of old Devanāgarī scans reliable enough to *trust as a pre-filter*, or does it
  produce too many UNCERTAIN to reduce the human scan-verification load?

_Dr. Mārcis Gasūns_
