# Changelog

All notable changes to SanskritSpellCheck are documented here.

This repository does not currently publish versioned release notes. Entries use
dated maintenance snapshots; keep upcoming work under [Unreleased] until it is
ready for a dated entry.

## [1.10.0] - 2026-06-16

### Added
- **Multilingual body-grounded triage + applied to PW.** The triage now handles
  dictionaries whose entry bodies are not English:
  - `triage_lang.py` — per-dictionary language profiles (MW=English, PW/PWG=German,
    VCP=Sanskrit) for the documented-intentional markers (wrong-reading / varia-lectio /
    in-composition / cross-reference). `triage_bodies.py` + `triage_synthesize.py` select
    markers by dict; the body-aware workflow uses a language-specific rubric.
  - `make_dict_package.py <DICT>` — one command to build any dict's tier-A package from
    `combined_candidates.txt` (extract tier-A rows + `make_changefiles` draft).
- **PW** ([corrections_draft/PW/](corrections_draft/PW)): the full pipeline run on the
  Sanskrit–German Petersburger Wörterbuch (Böhtlingk–Roth). German markers
  (`fehlerhaft für`, `v.l.`, `Lesart`, `s. u.`, `vgl.`) drive the classification.

### Notes
- **PW FINDING: of 657 tier-A candidates, only 2 (0.3%) are body-confirmed fileable typos**
  (`Bagama→BagaRa` "der Umlauf der Gestirne" = *bhagaṇa*; `hemana→hEmana` "Adj. von heman").
  369 are real words; **255 are documented-intentional** — notably **95 explicit
  `fehlerhaft für` wrong-readings** (PW's apparatus is denser/more explicit than MW's
  45); 1 stale; 30 need eyes. Bulk-applying tier-A would delete 95 of Böhtlingk–Roth's
  own wrong-reading cross-references.
- The per-dict `<DICT>_wrong_readings.txt` do-not-file list (a user convention) is now
  produced for every dictionary triaged, grouped by sub-type in the body's language.

## [1.9.0] - 2026-06-15

### Added
- **Body-grounded precision triage** for the engine's tier-A correction candidates —
  four new tools under [detectors/](detectors) that judge each candidate against the
  dictionary's *own entry text*, not spelling alone:
  - `triage_enrich.py` — attach deterministic evidence per candidate (the `<k2>`
    accent/hyphen field, DCS frequency band of the suggestion, cross-dict count,
    confusion class + empirical weight, historical-pair flag) → `<DICT>_evidence.jsonl`.
  - `triage_bodies.py` — build a headword→entry-body index from csl-orig and classify
    each candidate's MW body: `wr` / `variant` / `xref` (MW documents the spelling on
    purpose), `realword` (a real gloss), `thin`, `missing` (not in the current source).
  - `triage_body_batches.py` — split the `realword` set into body-aware batches.
  - `triage_synthesize.py` — combine deterministic + LLM + source-confirmation into a
    six-bucket ranked review queue (`<DICT>_triaged.txt`), the FILE-FIRST candidates in
    CORRECTIONS standard format (`<DICT>_file_first_sf.txt`), and a standing **do-not-file
    list** `<DICT>_wrong_readings.txt` — every spelling the dictionary documents on purpose
    (wrong-reading apparatus / `v.l.` / in-composition / cross-reference), grouped by
    sub-type, emitted for every dictionary triaged so future runs never re-flag them.
- Applied to **MW** ([corrections_draft/MW/](corrections_draft/MW)): the body-aware
  triage was run via a two-stage multi-agent workflow (adjudicate → adversarial verify,
  then body-aware classify → source-confirm).

### Notes
- **FINDING: of 1,954 MW tier-A candidates, only 4 (0.2%) are body-confirmed fileable
  typos.** 1,161 are real distinct words; 630 are spellings MW documents deliberately
  (`w.r. for…`, `v.l.`, `in comp. for…`, cross-refs) where a "fix" would *corrupt* MW;
  11 are stale (absent from current source); 148 need human eyes. Tier-A is high *engine*
  confidence, not precision — do not bulk-apply it.
- The engine's **vowel-length** flags (≈77% of tier-A) are almost all false (Sanskrit
  uses vowel length lexically); the rarer **consonant-class** flags (retroflex/sibilant/
  aspirate) are far higher-precision (3 of the 4 confirmed: ṇatva, `aṃśa` morpheme,
  `voḍhavya` sandhi).
- The adversarial/body-aware design caught false positives that spelling- and
  memory-based passes confirmed: `marga→mArga` (MW marks `marga` as `w.r. for mArga`),
  `muka→mUka` (MW glosses `muka` "the smell of cow-dung"), `vinAsa→vinASa`
  (`vi-nāsa` "noseless" is real). The original MW draft readme's worked examples were
  corrected accordingly.
- Triage intermediates (`<DICT>_evidence.jsonl`, `triage_work/`) are gitignored; the
  committed artifacts are `<DICT>_triaged.txt` and `<DICT>_file_first_sf.txt`.

## [1.8.2] - 2026-06-15

### Fixed
- **Retroflex `ळ` (U+0933) regression in `detectors/slp1util.devanagari_to_slp1`** introduced by
  the 1.8.1 dedup. The 1.8.1 form `to_slp1(deva_to_iast(s))` mis-mapped `ळ` to SLP1 `x` (vocalic
  ḷ) instead of `L`: `deva_to_iast` renders both `ळ` and vocalic `ऌ` as IAST `ḷ` (U+1E37), so the
  retroflex/vocalic distinction was lost before `to_slp1` ran and could not be recovered. Fixed at
  the source: `sanskrit-util` gains a direct `deva_to_slp1` (makes the `ळ`→`L` decision before the
  IAST step; vocalic `ऌ`/`◌ॢ` stay `x`), and `devanagari_to_slp1` now calls it. The danda /
  double-danda→space post-step is unchanged, and output is byte-identical to 1.8.1 on every input
  **except** those containing `ळ` (e.g. RV 1.1.1 `अग्निमीळे` → `agnimILe`, was `agnimIxe`; Marathi
  `खेळ` → `KeLa`, was `Kexa`). Impact was low — `devanagari_to_slp1` is used only by `ocr_verify`'s
  fuzzy comparison and `ळ` is rare — but it was a real correctness regression vs the pre-1.8.1 map.
  (The 1.8.1 "behavior unchanged" claim below held for the tested agni/kapila/Darma words but not
  for `ळ`.) Requires the `sanskrit-util` sibling at ≥ the commit adding `deva_to_slp1`.

## [1.8.1] - 2026-06-15

### Changed
- Cross-repo dedup: `detectors/slp1util.devanagari_to_slp1` now **delegates to the shared
  `sanskrit-util` package** (via `detectors/sanskrit_util.py`, a relative-path shim
  mirroring WhitneyRoots) instead of carrying its own Devanagari→SLP1 maps — single
  source of truth for transliteration. Behavior unchanged (verified equivalent on
  agni/kapila/Darma, and the danda→space step from 1.7.0 is preserved as a post-step).
  The SLP1 alphabet/char-classes stay local (sanskrit-util does not expose them). The
  shim raises a clear error only if the sibling is absent *and* the OCR path is used.

## [1.8.0] - 2026-06-14

### Added
- `detectors/gen_vidyut_stems.py` + vidyut morphology signal (Phase 3.2): generate the
  205k vidyut pratipadika (stem) inventory; `run_all` tags `morph✓` and nudges rank when
  a correction's suggestion is a valid vidyut stem the suspect isn't. `slp1util` gains
  `load_vidyut_stems`. Stems from vidyut (ambuda-org, MIT).

### Notes
- Honest finding: vidyut-stem validation is **weak on dictionary headwords** — only
  ~6.6% are pratipadikas, and an inflected suspect (`rAjA`) looks non-stem — so morph is
  a ranking nudge + tag, **not** a tier promoter (an `or morph` tier-A trigger
  over-promoted A 7717→11220, including inflection non-errors like `rAjA→rAja`).
  `vidyut_stems.txt` is gitignored (opt-in regenerate; the tag is off if absent).

## [1.7.0] - 2026-06-14

### Added
- `detectors/ocr_verify.py` (Phase 2.1) — OCR-assisted pre-verification pipeline:
  resolve the Cologne `servepdf` page → fetch the scan PDF → PDF text layer or OCR →
  closest-match compare the print to the suspect vs suggested spelling →
  CONFIRM/DENY/UNCERTAIN triage label. Fetch+render, the closest-match decision, and
  `slp1util.devanagari_to_slp1` are verified here; the OCR step is pluggable and needs
  tesseract + a Devanagari model (`san`/`hin`). Polite: cached, rate-limited, 429
  backoff — small batches, ideally server-side. Triage prior, not a verdict (a human
  always confirms against the scan).

## [1.6.0] - 2026-06-14

### Added
- `detectors/run_campaign.py` (Phase 2.4) — per-dictionary campaigns: splits the
  unified detector suite per dictionary into `campaigns/<DICT>/{review.html,
  candidates.txt}` and a tier-A-ranked dashboard `campaign_summary.txt` (MW 1977,
  PD 1045, BHS 737, SCH 678, PW 657 …), so corrections can be worked one dictionary
  at a time (matching the per-dict CORRECTIONS issue layout). Reuses run_all's
  aggregation/scoring/review-HTML. Outputs gitignored.

## [1.5.0] - 2026-06-14

### Added
- `detectors/gen_confusion_weights.py` + `confusion_weights.json` (Phase 2.6) —
  data-driven single-char confusion weights from the 3884 o_vs_O pairs (a/A 41%,
  i/I 24%, u/U 9%, s/S 8% …); `run_all` ranks common confusions higher.
- `detectors/make_changefiles.py` (Phase 2.5) — submission-prep: turns accepted
  corrections into per-dictionary **draft** change-files in the CORRECTIONS
  updateByLine format, locating the source line in csl-orig and proposing the
  `<k1>`/`<k2>` edit (both key fields). Prep only — no source edits, no auto-filing.

### Notes
- Phase 2 items blocked on external deps: OCR-assisted verification (tesseract +
  scan fetch), full DCS via `dcs_full.sqlite` (local copy is an empty placeholder),
  GRETIL corpus expansion (external download).

## [1.4.0] - 2026-06-14

### Added
- `detectors/extract_csl_hw.py` (Phase 1.4) — extract source-order headwords from a raw
  csl-orig dictionary (`<k1>`/`<k2>`), so charset/phonotactic/**order_check** run on the
  raw text, not just the cleaned sanhw1.txt. (order_check on raw sources measures
  deviation from sanhw's collation — verify against the dict's own anusvara convention.)
- `detectors/eval.py` (Phase 1.5–1.6) — evaluation harness: **recall** vs the 3884
  historical o_vs_O pairs (union 50.6%; spell_correct 44.6%, consensus 25%) and **15,152
  new** candidate pairs; **0** false positives vs ~30k known-good (nochange) words; tier
  distribution of recovered pairs (A=809/B=245/C=913); and a top-100 tier-A
  `spotcheck_sample.txt` for human precision verification.

## [1.3.0] - 2026-06-14

### Added
- `detectors/run_all.py` — unified runner (roadmap Phase 1.1–1.3): runs every
  detector, **deduplicates across them** by suspect headword, scores each candidate
  and assigns an **A/B/C tier** (cross-detector agreement is the main signal). Emits
  `combined_candidates.txt` (ranked), `combined_sf.txt` (CORRECTIONS standard format),
  and `combined_review.html` — an accept/reject review UI with per-row scan links,
  localStorage, and export of accepted/rejected rows to the `:y`/`:n` standard format.
  On sanhw1: 17,098 deduped candidates, 7,618 flagged by ≥2 detectors.
- `ROADMAP.md` (phased plan).

## [1.2.0] - 2026-06-14

### Added
- DCS corpus grounding: vendored `detectors/dcs_lemma_summary.json` (83,239 SLP1
  lemmas + frequency bands 1–5; DCS-2021, Oliver Hellwig, CC-BY, via VisualDCS).
  `slp1util.py` gains `load_dcs_lemmas`, `normalize_lemma` (DCS join key), and a shared
  `confusion_candidates`.
- New detector `dict_vs_corpus.py` — catches **collective** dictionary errors (a form
  every dictionary agrees on but the DCS corpus contradicts). Lowest-precision /
  exploratory by design.

### Changed
- `spell_correct.py` ranks suggestions by DCS frequency band and **suppresses**
  headwords that are attested DCS lemmas (9921→9173 flagged, 4001 real words
  suppressed, 704 suggest a band-≥4 DCS lemma); refactored onto shared
  `confusion_candidates`.
- `consensus.py` / `intra_dup.py` suppress minority/variant spellings that are
  attested DCS lemmas (consensus 8918→7548, intra_dup 10443→8945).

## [1.1.0] - 2026-06-14

### Added
- `detectors/` package — six additional spell-check algorithms grounded in the real
  CORRECTIONS error distribution, sharing one confusion model in `slp1util.py`:
  `spell_correct.py` (noisy-channel vs MW/PW/VCP + corpus), `consensus.py` (N-way
  cross-dict voting), `intra_dup.py` (intra-dictionary self-contradiction),
  `phonotactic_check.py` (anti-sandhi rules), `charset_check.py` (encoding),
  `order_check.py` (collation). See [detectors/readme.md](detectors/readme.md).
- `USE_CASES.md` — goal-oriented guide mapping tasks to tools and the verify→submit path.
- `triage_suspects.py` — splits a suspect list into noise / priority (non-rcc,
  verify-first) / gemination (post-repha, low priority).
- `Allvs_2026/{MW,PW,PWG,MW72}/` — fresh review packages (2017 `AllvsXX/` kept as audit trail).
- Repo-specific `CLAUDE.md`; deepened `README.md` (methods + real-error distribution).

### Changed
- Modernized every script to **Python 3 + PHP 8** (the only runtimes here): `print()`,
  `str.maketrans`/`str.translate`, `functools.cmp_to_key`, `html.parser`, `-1` preg_split.
- `faultfinder3a.php` check loop `for`→`foreach` — a deliberate, additive coverage
  change (VCP 6856→7411; the new hits are the s…/h… alphabet tail).

### Fixed
- `faultfinder3a.php` tail-drop: the `for ($j<count)` loop silently skipped surviving
  headwords past the survivor count (the alphabet tail); plus the PHP 8 `array_diff`
  key-gap warnings and `preg_match(null)` deprecation.
- `faultfinder3a-html.php` `repeat=2` (rCC report) was dead code — never stored or
  destructured records.
- `triage_suspects.py` robustness: malformed-line guard, filename-token-only `derive`,
  empty-dict lines no longer buried in noise; `ngramspellcheck.py` stdout/stderr utf-8.
- Stopped tracking `ngram/data/error.txt` (run output).

## [1.0.0] - 2026-06-13

### Added
- Added this changelog so repository-level changes have a stable home.
- Recorded the current repository purpose: SanskritSpellCheck ==================

### Recent Git History
- 2026-05-29 ai-wip: add .pre-commit-config.yaml (python+yaml)
- 2026-05-29 ai-wip: add .github/dependabot.yml for GitHub Actions auto-updates
- 2026-05-29 ai-wip: add CODE_OF_CONDUCT.md (Contributor Covenant 2.1)
- 2017-09-07 AllvsVCP ready
- 2017-09-07 issue 365 change made
