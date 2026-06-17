# CAE correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **89 tier-A** CAE (Cappeller, *A Sanskrit-English
Dictionary*, 1891) headwords as possible misspellings. Triaged against CAE's *own English
entry text* (from [csl-orig](https://github.com/sanskrit-lexicon/csl-orig)) with the hybrid
model split (Sonnet classify / Opus confirm / Opus review).

## The finding

> **Of 89 tier-A candidates, 0 are fileable typos.** 67 are real distinct words; **8 are
> spellings CAE documents on purpose**; the 9 TYPO candidates were all refuted at
> source-confirmation. Tier-A precision is **near-zero**, as on the other curated dictionaries —
> the durable deliverable is the do-not-file list.

Across the dictionaries triaged, fileable counts are
**MW 4 · PW 2 · VCP 1 · PWG 12 · SKD 3 · WIL 3 · GST 1 · SHS 37**, everything else 0.

## The authoritative artifact

- **[CAE_wrong_readings.txt](CAE_wrong_readings.txt)** — the standing **do-not-file** list (8).
- **[CAE_triaged.txt](CAE_triaged.txt)** — the full six-bucket queue.
- **[CAE_file_first_sf.txt](CAE_file_first_sf.txt)** — empty of fileable rows.

## Method & provenance

Driver `python triage_dict.py CAE`, English `triage_lang` profile, hybrid model split. Raw
engine output (do NOT apply): [CAE_candidates.txt](CAE_candidates.txt),
[CAE_draft.txt](CAE_draft.txt) — superseded by the triage.
