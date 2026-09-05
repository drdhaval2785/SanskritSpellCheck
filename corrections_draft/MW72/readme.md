_Created: 10-08-2026 · Last updated: 05-09-2026_

# MW72 correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **360 tier-A** MW72 (Monier-Williams, the **1872 first
edition**) headwords as possible misspellings. This package triages them against MW72's *own
English entry text* (from [csl-orig](https://github.com/sanskrit-lexicon/csl-orig)). It is the
sibling of the already-triaged MW (1899) — the same dictionary, 27 years earlier.

Run with a **hybrid model split**: Sonnet 4.6 classified the 294 `realword` candidates,
Opus 4.8 source-confirmed the TYPO pile, and an **Opus Review phase** ran the false-positive
gate (reviewing out the 1 below).

## The finding

> **Of 360 tier-A candidates, 0 are fileable typos** (1 confirmed-TYPO, reviewed out — see
> below). 231 are real distinct words; **77 are spellings MW72 documents on purpose**
> (cross-references 36, wrong-reading 2, `v.l.` 1, in-composition 1, other 37); **42 are not
> in the current source** (the 1872 edition's keys differ from the digitised text more than
> the later dictionaries — the highest UNLOCATABLE share so far); 10 need eyes. Tier-A
> precision is **near-zero**, as with MW (4/1954).

Across the dictionaries triaged, fileable-typo counts are
**MW 4 · PW 2 · VCP 1 · PWG 12 · SKD 3 · AP 0 · MW72 0 · SCH 0**. Do **not** bulk-apply.

## The authoritative artifact

- **[MW72_wrong_readings.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/MW72/MW72_wrong_readings.txt)** — the standing **do-not-file** list
  (77 documented-intentional spellings, grouped by sub-type).
- **[MW72_triaged.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/MW72/MW72_triaged.txt)** — the full six-bucket queue.
- **[MW72_file_first_sf.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/MW72/MW72_file_first_sf.txt)** — empty of fileable rows; the 1
  reviewed-out case is commented with `;`.

### Reviewed out (do NOT file — a real word, not a typo)

- **`ahnika`** — the entry reads `{%Ahnika, as, ā, am,%} … as last member of a compound
  {%= ahan%}` (e.g. *dvy-ahnika* "lasting two days"). `ahnika` is a genuine compound-final
  form, not a misspelling of `Ahnika`. (The gate working on English, mirroring SKD's
  `mahotka` on Sanskrit.)

## Method

Same pipeline as the other dictionaries (driver: `python triage_dict.py MW72`), English
`triage_lang` profile, hybrid model split. Deterministic markers settled 77 intentional
spellings; the body-aware pass + the Opus review handled the `realword` remainder.

## Raw engine output (provenance — do NOT apply)

- [MW72_candidates.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/MW72/MW72_candidates.txt) — the engine's 360 ranked tier-A candidates.
- [MW72_draft.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/MW72/MW72_draft.txt) — draft updateByLine change-file; **superseded** by the triage.

_Dr. Mārcis Gasūns_
