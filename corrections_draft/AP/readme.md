# AP correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **152 tier-A** AP (Apte, *The Practical Sanskrit-English
Dictionary*) headwords as possible misspellings. This package triages them against AP's *own
English entry text* (from [csl-orig](https://github.com/sanskrit-lexicon/csl-orig)).

Run with a **hybrid model split**: Sonnet 4.6 classified the 144 `realword` candidates,
Opus 4.8 source-confirmed the TYPO pile, and an **Opus Review phase** ran the false-positive
gate.

## The finding

> **Of 152 tier-A candidates, 0 are fileable typos.** Apte is a clean, much-curated modern
> reference: the engine's flags resolve to 109 real distinct words, **32 spellings AP
> documents on purpose** (cross-references 8, other grammatical/Vedic notes 24), 2 classified-
> TYPO-but-source-refuted, 6 that need eyes, and 3 not in the current source. Like MW (4/1954),
> PW (2/657) and VCP (1/563), tier-A precision is **near-zero** — the durable deliverable is
> the do-not-file list, not corrections.

Across the dictionaries triaged, fileable-typo counts are
**MW 4 · PW 2 · VCP 1 · PWG 12 · SKD 3 · AP 0**. Do **not** bulk-apply tier A.

## The authoritative artifact

- **[AP_wrong_readings.txt](AP_wrong_readings.txt)** — the standing **do-not-file** list
  (32 documented-intentional spellings, grouped by sub-type).
- **[AP_triaged.txt](AP_triaged.txt)** — the full six-bucket queue (start with bucket 2/3 if
  you want to eyeball the borderline cases).
- **[AP_file_first_sf.txt](AP_file_first_sf.txt)** — empty of fileable rows (0 confirmed).

## Method

Same pipeline as the other dictionaries (driver: `python triage_dict.py AP`), English
`triage_lang` profile, hybrid model split. Deterministic markers + a body-aware LLM pass +
the Opus review settled every candidate; none survived as a clean fileable typo.

## Raw engine output (provenance — do NOT apply)

- [AP_candidates.txt](AP_candidates.txt) — the engine's 152 ranked tier-A candidates.
- [AP_draft.txt](AP_draft.txt) — draft updateByLine change-file; **superseded** by the triage.
