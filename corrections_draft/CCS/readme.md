_Created: 10-08-2026 · Last updated: 05-09-2026_

# CCS correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **35 tier-A** CCS (Cappeller, *Sanskrit-Wörterbuch* —
German) headwords as possible misspellings. Triaged against CCS's *own German entry text*
(from [csl-orig](https://github.com/sanskrit-lexicon/csl-orig)) with the hybrid model split
(Sonnet classify / Opus confirm / Opus review).

## The finding

> **Of 35 tier-A candidates, 0 are fileable typos.** 20 are real distinct words; **3 are
> spellings CCS documents on purpose**; the 4 TYPO candidates were all refuted at
> source-confirmation. Tier-A precision is **near-zero**.

Across the dictionaries triaged, fileable counts are
**MW 4 · PW 2 · VCP 1 · PWG 12 · SKD 3 · WIL 3 · GST 1 · SHS 37**, everything else 0.

## The authoritative artifact

- **[CCS_wrong_readings.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/CCS/CCS_wrong_readings.txt)** — the standing **do-not-file** list (3).
- **[CCS_triaged.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/CCS/CCS_triaged.txt)** — the full six-bucket queue.
- **[CCS_file_first_sf.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/CCS/CCS_file_first_sf.txt)** — empty of fileable rows.

## Method & provenance

Driver `python triage_dict.py CCS`, German `triage_lang` profile (`CCS → de`), hybrid model
split. Raw engine output (do NOT apply): [CCS_candidates.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/CCS/CCS_candidates.txt),
[CCS_draft.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/CCS/CCS_draft.txt) — superseded by the triage.

_Dr. Mārcis Gasūns_
