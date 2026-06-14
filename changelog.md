# Changelog

All notable changes to SanskritSpellCheck are documented here.

This repository does not currently publish versioned release notes. Entries use
dated maintenance snapshots; keep upcoming work under [Unreleased] until it is
ready for a dated entry.

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
