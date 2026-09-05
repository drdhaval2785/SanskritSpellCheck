_Created: 10-08-2026 · Last updated: 05-09-2026_

# PUI correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **518 tier-A** PUI headwords as possible misspellings. PUI is
the *Purāṇic Index* — an index of proper names (deities, sages, kings, rivers, tīrthas, śaktis,
nāgas, tribes, places) drawn from the Purāṇas, glossed in English. This package triages the
candidates against PUI's *own entry text* (from
[csl-orig](https://github.com/sanskrit-lexicon/csl-orig)).

## The finding

> **Of 518 engine "tier-A" candidates, 0 are body-confirmed fileable typos.** 467 are real,
> distinct named entities (each with its own description and Purāṇa citation), 21 are spellings
> PUI documents on purpose (cross-references / parenthetical variants), and 6 are unlocatable.

This is the expected outcome for a *proper-name index*. The `suspect` flagged against a
normal-Sanskrit baseline is almost always a legitimate Purāṇic name in its own attested spelling —
`Brahmaṇa` (a Kādraveya Nāga, *not* a misspelling of brāhmaṇa), `Narā` (daughter of Suyajña),
`Saineya` (= Sātyaki) — so a one-letter "anomaly" is the name itself, not a slip. The 21
do-not-file cases carry explicit apparatus: cross-references (`See Indra`, `= Sātyaki`, `see
Sarpās`) and parenthetical variant readings (`Bab(h)ruvāhana`, `(also Prahlāda)`, `(Sarya?)`).

Cross-dict fileable precision on tier A stays near-zero: MW 4/1954 · PW 2/657 · VCP 1/563 ·
PWG 12/497 · SHS 37/246 · BHS 0/713 · **PUI 0/518**.

## The authoritative artifacts

- **[PUI_wrong_readings.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/PUI/PUI_wrong_readings.txt)** — the standing **do-not-file** list: 21
  deliberate spellings (cross-reference 7, other-intentional 14). Folded into
  [nochange/do_not_file_suppress.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/nochange/do_not_file_suppress.txt) by
  [detectors/gen_do_not_file_suppress.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/gen_do_not_file_suppress.py).
- **[PUI_triaged.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/PUI/PUI_triaged.txt)** — the full review queue: 467 REAL-WORD named entities + 21
  INTENTIONAL.
- **[PUI_file_first_sf.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/PUI/PUI_file_first_sf.txt)** — **empty** (0 fileable). Nothing to file.

## Method

`detectors/triage_dict.py PUI` (package) → body-aware classification of the 488 locatable candidates
against PUI's own entries (TYPO / REALWORD / INTENTIONAL / UNSURE; PUI registered as English in
`detectors/triage_lang.py`) → `triage_dict.py PUI --finish`. With 0 TYPO classifications there was
no source-confirm / review pile. **DRAFT for human review; never edits `csl-orig`.** The do-not-file
list is the deliverable.

_Dr. Mārcis Gasūns_
