# FILE-FIRST verification pass — July 2026

<p align="right"><sub>Created: 02-07-2026 · Last updated: 02-07-2026</sub></p>

Pre-filing verification of all **122 FILE-FIRST candidates** against the `csl-orig` entry
text, run 02-07-2026 as the Fable-window gate from
[ROADMAP_2026_2027.md §Q3](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ROADMAP_2026_2027.md).
Mechanical verification: four Sonnet 4.6 (`claude-sonnet-4-6`) agents (locate → evidence-quote →
direction → collision checks, reusing `triage_util.EntryIndex`). Adjudication of all 28 flags:
Fable 5 (`claude-fable-5`). Full per-row verdicts:
[file_first_verified.tsv](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/file_first_verified.tsv).

## Outcome

| Verdict | n | Meaning for the umbrella issue |
|---|--:|---|
| **PASS** | 97 | propose as corrections (still scan-checked by the human, as always) |
| **SCAN-FIRST** | 12 | propose, explicitly marked "grammar-certain but entry-internal evidence silent — the scan is decisive" |
| **EDITORIAL** | 11 | present as **duplicate-pair / apparatus-collision decisions** (merge vs respell vs leave), NOT as plain corrections |
| **DNF** | 1 | `YAT RiS→niS` — likely Dhātupāṭha ṇopadeśa root notation; moved toward the do-not-file class |
| **DROP** | 1 | `SHS kARqapfzwa` — already fixed upstream since triage |

Per dict: SHS 34+2sf (−1 stale) · YAT 17+4sf+5ed+1dnf · ACC 17+4sf+1ed · PWG 10+2ed ·
MCI 10 · MW 2sf+2ed · SKD 3 · WIL 3 · PW 1+1ed · VCP 1 · GST 1.

## What changed vs the triage-era picture

1. **A third category is required.** The biggest correction to the plan: 11 candidates are not
   "wrong headword → fix" but **collisions** — the right spelling already exists as its own
   entry (YAT dual-listings cross-referenced "Idem"; MW `kattfRa` L42680; PWG's `duzWu` errata
   note; PW's `*hemana` constructed form). A silent `<k1>` respell would create duplicate
   headwords or clobber apparatus. The umbrella issue gets three sections per dict:
   *propose* / *scan-first* / *editorial decisions*.
2. **MW's headline number honestly restated:** the triage's celebrated "4 fileable of 1,954"
   is, after source re-verification, **2 solid-but-scan-first + 2 editorial duplicates**. Worth
   one sentence in A44 (the 4 remain the *triage output*; this is a downstream gate).
3. **Corrections propagate:** 1 of 122 (SHS `kARqapfzwa`) was already fixed upstream between
   triage (June) and now — re-verify against live `csl-orig` immediately before filing.
4. **Judge-vs-checker division held:** the Sonnet checkers over-flagged where evidence is
   *morphological* rather than literal (ṣatva/ṇatva-certain forms like `biBedayizu`,
   `AparAhnika`, `yajYamuz` — all restored to PASS by adjudication) and under no case found a
   reversed pair the triage had missed. Grammar-exceptionless rules count as evidence; a
   `k2` that merely mirrors `k1` does not count as counter-evidence.

## Process cautions (for the next verification run)

- Readme evidence cells are often **class-level templates, not verbatim quotes** — naive
  substring matching produced ~33 spurious flags across two agents before entry-reading
  resolved them. Never string-match evidence; read the entry.
- Unicode trap: worklist `°` (U+00B0) vs source `˚` (U+02DA) breaks exact matching.
- 31 rows (SHS 15, ACC 15, YAT 1) had no per-row readme evidence at all (class-group prose
  only); their evidence was recovered directly from the entry bodies this pass and is now in
  the TSV — the umbrella issue should quote it from there.

<p align="right"><sub>Dr. Mārcis Gasūns</sub></p>
