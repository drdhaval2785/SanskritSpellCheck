# WIL correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **108 tier-A** WIL (H. H. Wilson, *A Dictionary,
Sanscrit and English*, 1832 — the earliest major Sanskrit-English dictionary) headwords as
possible misspellings. This package triages them against WIL's *own English entry text* (from
[csl-orig](https://github.com/sanskrit-lexicon/csl-orig)).

Run with a **hybrid model split**: Sonnet 4.6 classified the 106 `realword` candidates,
Opus 4.8 source-confirmed the TYPO pile, and an **Opus Review phase** ran the false-positive
gate (reviewing out the 1 below).

## The finding

> **Of 108 tier-A candidates, 3 are fileable typos** (4 confirmed, 1 reviewed out). 80 are
> real words; **17 are spellings WIL documents on purpose**; ~8 need eyes. As the oldest and
> least-corrected of the Sanskrit-English dictionaries, Wilson surfaces a few residual errors —
> each confirmed by the entry's own etymology/inflection.

Across the dictionaries triaged, fileable-typo counts are
**MW 4 · PW 2 · VCP 1 · PWG 12 · SKD 3 · WIL 3 · GST 1 · SHS 37**. Do **not** bulk-apply.

### The 3 FILE-FIRST candidates — each confirmed by the entry's own text

| wrong → right | class | the entry's own evidence |
|---|---|---|
| `boDidruna → boDidruma` | n/m | gloss "the holy fig tree", inflection `-maH`, etymology `E. boDi … druma a tree` — `druna` contradicts its own derivation |
| `jAmbabat → jAmbavat` | b/v | inflection `-vAn`, cross-ref "also `jAmbuvat`", etymology `jAmba + matup` → `jAmbavat`; `b` in the key is the error |
| `kaNkalodya → kaNkaloqya` | d/q (dental→retroflex) | paradigm `-qyaM` (retroflex q) contradicts the headword's dental `d` |

> Candidates, not confirmed corrections — verify each on the scan (1832 typography), then flip
> `n`→`y` in [WIL_file_first_sf.txt](WIL_file_first_sf.txt).

### Reviewed out (do NOT file)

- **`zaYca`** — pulled by the Opus review as not a clean typo for the suggested correction.

## The authoritative artifact

- **[WIL_file_first_sf.txt](WIL_file_first_sf.txt)** — the 3 FILE-FIRST candidates (1
  reviewed-out, commented).
- **[WIL_triaged.txt](WIL_triaged.txt)** — the full six-bucket queue.
- **[WIL_wrong_readings.txt](WIL_wrong_readings.txt)** — the standing **do-not-file** list (17).

## Method

Same pipeline as the other dictionaries (driver: `python triage_dict.py WIL`), English
`triage_lang` profile, hybrid model split. The LLM/human layer is a triage prior — the scan confirms.

## Raw engine output (provenance — do NOT apply)

- [WIL_candidates.txt](WIL_candidates.txt) — the engine's 108 ranked tier-A candidates.
- [WIL_draft.txt](WIL_draft.txt) — draft updateByLine change-file; **superseded** by the triage.
