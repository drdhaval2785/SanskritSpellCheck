_Created: 10-08-2026 · Last updated: 05-09-2026_

# INM correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **161 tier-A** INM headwords as possible misspellings. INM is
Sörensen's *Index to the Names in the Mahābhārata* — a proper-name index (persons, deities,
peoples, places, rivers) glossed in English with parva/verse references. Triaged against INM's *own
entry text* (from [csl-orig](https://github.com/sanskrit-lexicon/csl-orig)).

## The finding

> **Of 161 engine "tier-A" candidates, 0 are body-confirmed fileable typos.** 123 are real,
> distinct Mahābhārata named entities (each with its own gloss and reference), 16 are spellings INM
> documents on purpose, 12 are unlocatable.

Expected for a *proper-name index*: the `suspect` is a legitimate Mahābhārata name in its attested
spelling. Where a variant exists, Sörensen cites it explicitly as a B./C./BR. recension note while
keeping the suspect as headword — and he even **indexes known wrong readings on purpose** ("error
in C. for Vaṭadhāna", "erratum for Danāyus"), which are do-not-file by definition.

Cross-dict fileable precision: SHS 37/246 · YAT 27/247 · ACC 22/174 · … · BHS 0/713 · PUI 0/518 ·
IEG 0/162 · **INM 0/161**.

## The authoritative artifacts

- **[INM_wrong_readings.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/INM/INM_wrong_readings.txt)** — the **do-not-file** list: 16 deliberate
  spellings (cross-reference 4, other 12). Folded into
  [nochange/do_not_file_suppress.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/nochange/do_not_file_suppress.txt).
- **[INM_triaged.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/INM/INM_triaged.txt)** — full queue: 123 REAL-WORD + 16 INTENTIONAL.
- **[INM_file_first_sf.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/INM/INM_file_first_sf.txt)** — **empty** (0 fileable).

## Method

`detectors/triage_dict.py INM` (package; INM registered as English in `triage_lang.py`) →
body-aware classification → `--finish`. 0 TYPO → no source-confirm/review pile. **DRAFT; never edits
`csl-orig`.**

_Dr. Mārcis Gasūns_
