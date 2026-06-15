# Changelog

All notable changes to SanskritSpellCheck are documented here.

This repository does not currently publish versioned release notes. Entries use
dated maintenance snapshots; keep upcoming work under [Unreleased] until it is
ready for a dated entry.

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
