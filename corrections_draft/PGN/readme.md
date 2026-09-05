_Created: 10-08-2026 · Last updated: 05-09-2026_

# PGN correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **21 tier-A** PGN headwords as possible misspellings. PGN is an
index of proper names from inscriptions (Gupta-period and related), glossed in English with
inscription reference numbers. Triaged against PGN's *own entry text* (from
[csl-orig](https://github.com/sanskrit-lexicon/csl-orig)).

## The finding

> **Of 21 engine "tier-A" candidates, 0 are body-confirmed fileable typos.** 8 are real attested
> names (each with its own inscription reference), 1 is documented-intentional.

Expected for a *proper-name index*: each flagged form is the attested inscriptional reading in its
own spelling (e.g. `Baṭṭasvāmin`, glossed via Bhaṭṭa but keyed as the inscription has it). The
detector's "suggestions" were near-spelling neighbours, not corrections.

## The authoritative artifacts

- **[PGN_wrong_readings.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/PGN/PGN_wrong_readings.txt)** — do-not-file: 1 (other). Folded into
  [nochange/do_not_file_suppress.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/nochange/do_not_file_suppress.txt).
- **[PGN_triaged.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/PGN/PGN_triaged.txt)** — full queue: 8 REAL-WORD + 1 INTENTIONAL.
- **[PGN_file_first_sf.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/PGN/PGN_file_first_sf.txt)** — **empty** (0 fileable).

## Method

`detectors/triage_dict.py PGN` (English) → body-aware classification → `--finish`. 0 TYPO → no
confirm/review pile. **DRAFT; never edits `csl-orig`.**

_Dr. Mārcis Gasūns_
