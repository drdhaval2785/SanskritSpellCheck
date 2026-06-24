# VEI correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **43 tier-A** VEI headwords as possible misspellings. VEI is
Macdonell–Keith's *Vedic Index of Names and Subjects* — proper names and Vedic technical terms,
glossed in English with Vedic-text references. Triaged against VEI's *own entry text* (from
[csl-orig](https://github.com/sanskrit-lexicon/csl-orig)).

## The finding

> **Of 43 engine "tier-A" candidates, 0 are body-confirmed fileable typos.** 34 are real attested
> Vedic names/terms (each its own lemma with gloss and citation), 2 are documented-intentional.

Expected for a Vedic name/term index: the detector reacted to near-spelling neighbours
(`pajrA`/`pajra`, `dityavAh`/`dityavah`) that VEI legitimately records as distinct attested entries.

## The authoritative artifacts

- **[VEI_wrong_readings.txt](VEI_wrong_readings.txt)** — do-not-file: 2 (cross-reference 1, other 1).
  Folded into [nochange/do_not_file_suppress.txt](../../nochange/do_not_file_suppress.txt).
- **[VEI_triaged.txt](VEI_triaged.txt)** — full queue: 34 REAL-WORD + 2 INTENTIONAL.
- **[VEI_file_first_sf.txt](VEI_file_first_sf.txt)** — **empty** (0 fileable).

## Method

`detectors/triage_dict.py VEI` (English) → body-aware classification → `--finish`. 0 TYPO → no
confirm/review pile. **DRAFT; never edits `csl-orig`.**
