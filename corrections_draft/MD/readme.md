# MD correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **50 tier-A** MD (Macdonell, *A Practical Sanskrit
Dictionary*, 1893/1929) headwords as possible misspellings. Triaged against MD's *own English
entry text* (from [csl-orig](https://github.com/sanskrit-lexicon/csl-orig)) with the hybrid
model split (Sonnet classify / Opus confirm / Opus review).

## The finding

> **Of 50 tier-A candidates, 0 are fileable typos.** 48 are real distinct words; **1 is a
> spelling MD documents on purpose**; none classified as TYPO survived. Tier-A precision is
> **near-zero** — a clean, well-curated reference.

Across the dictionaries triaged, fileable counts are
**MW 4 · PW 2 · VCP 1 · PWG 12 · SKD 3 · WIL 3 · GST 1 · SHS 37**, everything else 0.

## The authoritative artifact

- **[MD_wrong_readings.txt](MD_wrong_readings.txt)** — the standing **do-not-file** list (1).
- **[MD_triaged.txt](MD_triaged.txt)** — the full six-bucket queue.
- **[MD_file_first_sf.txt](MD_file_first_sf.txt)** — empty of fileable rows.

## Method & provenance

Driver `python triage_dict.py MD`, English `triage_lang` profile, hybrid model split. Raw
engine output (do NOT apply): [MD_candidates.txt](MD_candidates.txt),
[MD_draft.txt](MD_draft.txt) — superseded by the triage.
