# GST correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **48 tier-A** GST (Goldstücker, *A Dictionary, Sanskrit
and English*, 1856 — left incomplete) headwords as possible misspellings. This package triages
them against GST's *own English entry text* (from
[csl-orig](https://github.com/sanskrit-lexicon/csl-orig)).

Run with a **hybrid model split**: Sonnet 4.6 classified the 43 `realword` candidates,
Opus 4.8 source-confirmed the TYPO pile, Opus reviewed the result.

## The finding

> **Of 48 tier-A candidates, 1 is a fileable typo.** 22 are real words; **22 are spellings GST
> documents on purpose** (Goldstücker's discursive entries carry an unusually high share of
> documented variants/cross-references); ~3 need eyes.

The one fileable case:

| wrong → right | class | the entry's own evidence |
|---|---|---|
| `aprakaraRika → aprAkaraRika` | vowel length | the entry's own etymology `E. a (neg.) and prAkaraRika` and its quoted Kāvyaprakāśa example `aprAkaraRikasyābhidhānena…` both use long **ā** |

> Verify on the scan, then flip `n`→`y` in [GST_file_first_sf.txt](GST_file_first_sf.txt).

## The authoritative artifact

- **[GST_file_first_sf.txt](GST_file_first_sf.txt)** — the 1 FILE-FIRST candidate.
- **[GST_wrong_readings.txt](GST_wrong_readings.txt)** — the standing **do-not-file** list (22).
- **[GST_triaged.txt](GST_triaged.txt)** — the full six-bucket queue.

## Method

Same pipeline as the other dictionaries (driver: `python triage_dict.py GST`), English
`triage_lang` profile, hybrid model split.

## Raw engine output (provenance — do NOT apply)

- [GST_candidates.txt](GST_candidates.txt) — the engine's 48 ranked tier-A candidates.
- [GST_draft.txt](GST_draft.txt) — draft updateByLine change-file; **superseded** by the triage.
