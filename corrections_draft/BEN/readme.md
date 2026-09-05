_Created: 10-08-2026 · Last updated: 05-09-2026_

# BEN correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **43 tier-A** BEN (Benfey, *A Sanskrit-English
Dictionary*, 1866) headwords as possible misspellings. Triaged against BEN's *own English
entry text* (from [csl-orig](https://github.com/sanskrit-lexicon/csl-orig)) with the hybrid
model split (Sonnet classify / Opus confirm / Opus review).

## The finding

> **Of 43 tier-A candidates, 0 are fileable typos.** 25 are real distinct words; **14 are
> spellings BEN documents on purpose** (Benfey's entries carry a high share of documented
> variants/cross-references); none classified as TYPO. Tier-A precision is **near-zero**.

Across the dictionaries triaged, fileable counts are
**MW 4 · PW 2 · VCP 1 · PWG 12 · SKD 3 · WIL 3 · GST 1 · SHS 37**, everything else 0.

## The authoritative artifact

- **[BEN_wrong_readings.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/BEN/BEN_wrong_readings.txt)** — the standing **do-not-file** list (14).
- **[BEN_triaged.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/BEN/BEN_triaged.txt)** — the full six-bucket queue.
- **[BEN_file_first_sf.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/BEN/BEN_file_first_sf.txt)** — empty of fileable rows.

## Method & provenance

Driver `python triage_dict.py BEN`, English `triage_lang` profile, hybrid model split. Raw
engine output (do NOT apply): [BEN_candidates.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/BEN/BEN_candidates.txt),
[BEN_draft.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/BEN/BEN_draft.txt) — superseded by the triage.

_Dr. Mārcis Gasūns_
