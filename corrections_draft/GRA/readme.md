# GRA correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **45 tier-A** GRA (Grassmann, *Wörterbuch zum Rig-Veda*,
1873 — German, Vedic) headwords as possible misspellings. Triaged against GRA's *own German
entry text* (from [csl-orig](https://github.com/sanskrit-lexicon/csl-orig)) with the hybrid
model split (Sonnet classify / Opus confirm / Opus review).

## The finding

> **Of 45 tier-A candidates, 0 are fileable typos** (1 confirmed-TYPO, reviewed out). 28 are
> real distinct words; **7 are spellings GRA documents on purpose**; 9 are not in the current
> source. Tier-A precision is **near-zero**.

Across the dictionaries triaged, fileable counts are
**MW 4 · PW 2 · VCP 1 · PWG 12 · SKD 3 · WIL 3 · GST 1 · SHS 37**, everything else 0.

### Reviewed out (do NOT file)

- **`pradakzinit`** — pulled by the Opus review as not a clean fileable typo for the
  suggested correction.

## The authoritative artifact

- **[GRA_wrong_readings.txt](GRA_wrong_readings.txt)** — the standing **do-not-file** list (7).
- **[GRA_triaged.txt](GRA_triaged.txt)** — the full six-bucket queue.
- **[GRA_file_first_sf.txt](GRA_file_first_sf.txt)** — empty of fileable rows (1 reviewed-out, commented).

## Method & provenance

Driver `python triage_dict.py GRA`, German `triage_lang` profile (`GRA → de`), hybrid model
split. Raw engine output (do NOT apply): [GRA_candidates.txt](GRA_candidates.txt),
[GRA_draft.txt](GRA_draft.txt) — superseded by the triage.
