# SHS correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **246 tier-A** SHS (*Śabda-Sāgara*, a Sanskrit-English
dictionary, 1900) headwords as possible misspellings. This package triages them against SHS's
*own English entry text* (from [csl-orig](https://github.com/sanskrit-lexicon/csl-orig)).

Run with a **hybrid model split**: Sonnet 4.6 classified the 226 `realword` candidates,
Opus 4.8 source-confirmed the TYPO pile, and an **Opus Review phase** ran the adversarial
false-positive gate (reviewing out the 2 below).

## The finding — the highest-yield dictionary so far

> **Of 246 tier-A candidates, 37 are fileable typos** (~15%, vs MW 0.2% or PWG 2.4%) — 39
> source-confirmed, 2 reviewed out. 122 are real words; **31 are spellings SHS documents on
> purpose**; 19 are not in the current source; ~11 need eyes.

This outlier is **genuine, not over-acceptance.** Śabda-Sāgara is a smaller, far less-corrected
digitisation than MW/Apte, so many OCR/transcription errors survive — **and** nearly every SHS
entry carries an explicit etymology (`E. <components>`) and an inflectional paradigm, which is
the strongest possible internal check. Every one of the 37 is contradicted by the entry's *own*
etymology or inflection — this is the body-grounded method's ideal case. Each was confirmed by
Opus against the full entry, then survived a second adversarial Opus review.

Across all dictionaries triaged, fileable-typo counts are
**MW 4 · PW 2 · VCP 1 · PWG 12 · SKD 3 · WIL 3 · GST 1 · SHS 37** (AP/MW72/SCH/CAE/AP90/MD/GRA/BEN/CCS 0).

### The error classes among the 37 (all confirmed by the entry's own text)

| class | examples | the entry's own evidence |
|---|---|---|
| **b/v** (व/ब) | `kzIraballI→kzIravallI`, `BadraballI→BadravallI`, `SilAbalkA→SilAvalkA`, `divaspfTibI→divaspfTivI`, `drabaja→dravaja`, `svarRabalkala→svarRavalkala`, `jAmbabat→jAmbavat` | etymology spells the element with **v** (`E. … vallI a creeper`, `valka bark`, `pfTivI earth`) |
| **retroflex w→W** (ट/ठ↔ष्ट) | `kARqapfzwa→kARqapfzWa`, `laGizwa→laGizWa`, `padazwIva→padazWIva`, `kAzwakuddAla→kAzWakuddAla` | inflections are `-zWaH-zWA-zWaM`; superlative `izWan`; `azWIvat` |
| **vowel length** | `murali→muralI`, `vAcanIka→vAcanika`, `ditisUta→ditisuta`, `jAmbunadamaya→jAmbUnadamaya`, `jalarupa→jalarUpa`, … (17 total) | the entry's gender/affix/etymology fixes the length (`f.(-lI)`, `Wak aff.`→short i, `E. … suta a son`) |
| **sibilant / nasal / other** | `hastisuRqA→hastiSuRqA`, `pratyupaveza→pratyupaveSa`, `vizamaSIla`/`viSamaSIla`, `BUnaya→BUmaya`, `ninittakAla→nimittakAla`, `paNKagrAha→paNkagrAha`, `pratipaTan→pratipaTam` | gloss/etymology requires the corrected consonant |

> **⚠️ This is by far the largest file-first set — prioritise the human scan-verification here.**
> Each is high-confidence (entry-contradicted), but 37 corrections is a real review load; work
> down [SHS_file_first_sf.txt](SHS_file_first_sf.txt), confirm on the scan, flip `n`→`y`.

### Reviewed out (do NOT file — attested variants)

- **`SreRiBUta`** — base `SreRi` (short i) is the dictionary lemma; the whole family
  (`SreRi`/`SreRika`/`SreRiDarma`) is short-i. Intentional, not a typo for `SreRIBUta`.
- **`Sabdakoza`** — `koza`/`koSa` (and `kosa`) are both standard attested spellings of the
  word for "treasury/lexicon"; a variant, not an error.

## The authoritative artifact

- **[SHS_file_first_sf.txt](SHS_file_first_sf.txt)** — the 37 FILE-FIRST candidates in
  CORRECTIONS standard format (the 2 reviewed-out are commented with `;`).
- **[SHS_triaged.txt](SHS_triaged.txt)** — the full six-bucket queue (each FILE-FIRST row
  carries the entry text + the etymological evidence).
- **[SHS_wrong_readings.txt](SHS_wrong_readings.txt)** — the standing **do-not-file** list (31).

## Method

Same pipeline as the other dictionaries (driver: `python triage_dict.py SHS`), English
`triage_lang` profile, hybrid model split (`clsModel=sonnet`, `confModel=opus`, `revModel=opus`).
The LLM/human layer is a triage prior — the scan confirms.

## Raw engine output (provenance — do NOT apply)

- [SHS_candidates.txt](SHS_candidates.txt) — the engine's 246 ranked tier-A candidates.
- [SHS_draft.txt](SHS_draft.txt) — draft updateByLine change-file; **superseded** by the triage.
