# KRM correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **47 tier-A** KRM headwords as possible misspellings. KRM is a
*dhātupāṭha* — a list of Sanskrit verbal roots in the Kramadīśvara grammatical tradition, each
entry quoting a root with its meaning and gaṇa/class in Sanskrit. Triaged against KRM's *own entry
text* (from [csl-orig](https://github.com/sanskrit-lexicon/csl-orig)).

## The finding

> **Of 47 engine "tier-A" candidates, 0 are body-confirmed fileable typos.** 37 are real distinct
> roots (each defined with its own meaning and gaṇa), 6 are documented-intentional, 4 of which are
> the ṇ-/ṣ-**upadeśa** convention.

Expected for a *dhātupāṭha*: the detector flagged legitimate distinct roots and, crucially, the
grammatical convention by which **ṇ-initial / ṣ-initial roots are listed in their upadeśa form**
(`Riji`, `Risi`, `zarja`, `zivi`) even though they conjugate with dental n / dental s — this is
deliberate Pāṇinian notation (ṇopadeśa/ṣopadeśa), not a typo. Anubandha and citation-vowel markers
(final-Ṇ/Ñ, long-vowel citation forms) likewise distinguish real roots.

## The authoritative artifacts

- **[KRM_wrong_readings.txt](KRM_wrong_readings.txt)** — do-not-file: 6 (wrong-reading 1, other 5).
  Folded into [nochange/do_not_file_suppress.txt](../../nochange/do_not_file_suppress.txt).
- **[KRM_triaged.txt](KRM_triaged.txt)** — full queue: 37 REAL-WORD + 6 INTENTIONAL.
- **[KRM_file_first_sf.txt](KRM_file_first_sf.txt)** — **empty** (0 fileable).

## Method

`detectors/triage_dict.py KRM` (Sanskrit, `sa`) → body-aware classification with the ṇ/ṣ-upadeśa
convention treated as intentional → `--finish`. 0 TYPO → no confirm/review pile. **DRAFT; never
edits `csl-orig`.**
