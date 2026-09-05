_Created: 10-08-2026 · Last updated: 05-09-2026_

# AP90 correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **53 tier-A** AP90 (Apte, *The Practical Sanskrit-English
Dictionary*, **1890** edition) headwords as possible misspellings. Triaged against AP90's *own
English entry text* (from [csl-orig](https://github.com/sanskrit-lexicon/csl-orig)) with the
hybrid model split (Sonnet classify / Opus confirm / Opus review).

## The finding

> **Of 53 tier-A candidates, 0 are fileable typos.** 32 are real distinct words; **8 are
> spellings AP90 documents on purpose**; the 9 TYPO candidates were all refuted at
> source-confirmation. As with the related AP (Apte, modern edition, also 0), tier-A precision
> is **near-zero** — the do-not-file list is the product.

Across the dictionaries triaged, fileable counts are
**MW 4 · PW 2 · VCP 1 · PWG 12 · SKD 3 · WIL 3 · GST 1 · SHS 37**, everything else 0.

## The authoritative artifact

- **[AP90_wrong_readings.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/AP90/AP90_wrong_readings.txt)** — the standing **do-not-file** list (8).
- **[AP90_triaged.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/AP90/AP90_triaged.txt)** — the full six-bucket queue.
- **[AP90_file_first_sf.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/AP90/AP90_file_first_sf.txt)** — empty of fileable rows.

## Method & provenance

Driver `python triage_dict.py AP90`, English `triage_lang` profile, hybrid model split. Raw
engine output (do NOT apply): [AP90_candidates.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/AP90/AP90_candidates.txt),
[AP90_draft.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/AP90/AP90_draft.txt) — superseded by the triage.

_Dr. Mārcis Gasūns_
