_Created: 10-08-2026 · Last updated: 05-09-2026_

# PWG correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **497 tier-A** PWG (Sanskrit–German *Petersburger
Wörterbuch*, the **large** Böhtlingk–Roth edition) headwords as possible misspellings.
This package triages them against PWG's *own German entry text* (from
[csl-orig](https://github.com/sanskrit-lexicon/csl-orig)).

Run with a **hybrid model split**: Sonnet 4.6 classified the 306 `realword` candidates,
Opus 4.8 source-confirmed the TYPO pile, and an **Opus Review phase** ran the adversarial
false-positive gate (reviewing out the 2 below); a human spot-checks before filing.

## The finding

> **Of 497 tier-A candidates, 12 are fileable typos** (14 body-confirmed, 2 reviewed out —
> see below). That is far more than the other dictionaries triaged — because PWG (the large
> Petersburg) carries more **digitization errors**, and the strongest signal is *internal*:
> the entry's **own derivation or citation contradicts the headword spelling**. 196 are real
> words; **248 are spellings PWG documents on purpose** (wrong-reading `fehlerhaft für` 71,
> cross-references 137, `v.l.` 8, in-composition 4, other 28); 2 are not in the current
> source; ~37 need eyes.

Across all four dictionaries triaged, fileable-typo counts are
**MW 4 · PW 2 · VCP 1 · PWG 12** — still a tiny fraction of "tier A". Do **not** bulk-apply.

## The authoritative artifact

- **[PWG_file_first_sf.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/PWG/PWG_file_first_sf.txt)** — the 12 FILE-FIRST candidates in
  CORRECTIONS standard format (the 2 reviewed-out are commented with `;`). Verify each on
  the scan (for b/v cases: check व vs ब on the page), flip `n`→`y`, file.
- **[PWG_triaged.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/PWG/PWG_triaged.txt)** — the full six-bucket queue.
- **[PWG_wrong_readings.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/PWG/PWG_wrong_readings.txt)** — the standing **do-not-file** list
  (248 documented-intentional spellings, grouped by sub-type).

### The 12 FILE-FIRST candidates — each confirmed by the entry's own text

| wrong → right | class | the entry's own evidence |
|---|---|---|
| `arTavanDa → arTabanDa` | b/v | quotes `lalitArTabanDaM` (with b) |
| `paRavanDa → paRabanDa` | b/v | derivation `(paRa + ba°)`; gloss "concluding a contract" = *paṇabandha* |
| `BAvavanDana → BAvabanDana` | b/v | derivation `(BAva + ba°)` |
| `pfzwavanDu → pfzwabanDu` | b/v | gloss "his kin" = *bandhu*; `vgl. banDupfcC` |
| `Dabalapakza → Davalapakza` | b/v | gloss "Gans" = *dhavala-pakṣa* (white-winged) |
| `avakaSa → avakASa` | vowel-length | citation uses `avakASena` (long ā) |
| `tarAvalI → tArAvalI` | vowel-length | body has `tArARAM` (of stars) |
| `dIvAkIrtya → divAkIrtya` | vowel-length | derivation `(divA + kI°)` (short i) |
| `tfzitottara → tfzitottarA` | vowel-length | marked `f.` (a feminine plant name → -ā) |
| `yajYamus → yajYamuz` | sibilant | derivation `(yajYa + 2. muz)` (√muṣ) |
| `biBedayisu → biBedayizu` | sibilant | desiderative of caus. of *bhid* (→ -iṣu) |
| `duzwu → duzWu` | aspirate | derivation `(duz + sTu)` (ṣṭhu) |

> These are **candidates**, not confirmed corrections — the b/v cases especially are
> classic transcription confusions (व/ब are near-identical glyphs); the scan is the final
> arbiter, but the entry's own derivation makes them high-confidence.

### Reviewed out (do NOT file — intentional, not typos)

- **`dASaSiras`** — the entry reads `(wohl dASaSirasa von daSaSiras)`: a **vṛddhi
  derivative** (a Sāman named after *daśaśiras*), like MW's `mADu`. Correcting it would
  erase the derivation.
- **`ketunAlin`** — PWG records **both** `ketunAlin` (HARIV. 9291, 9322) and `ketumAli`
  (9313, 9327, 9329): an **attested variant** of a Dānava's name, not a typo.

## Method

Same pipeline as the other dictionaries (driver: `python triage_dict.py PWG`), with the
German `triage_lang` profile and a hybrid model split (`clsModel=sonnet`, `confModel=opus`).
The deterministic markers settled 248 intentional spellings (incl. PWG's dense
`fehlerhaft für` apparatus) before any LLM saw them; the body-aware pass + a human review
handled the `realword` remainder. The LLM/human layer is a triage prior — the scan confirms.

## Raw engine output (provenance — do NOT apply)

- [PWG_candidates.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/PWG/PWG_candidates.txt) — the engine's 497 ranked tier-A candidates.
- [PWG_draft.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/PWG/PWG_draft.txt) — draft updateByLine change-file; **superseded** by the
  triage (use [PWG_file_first_sf.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/PWG/PWG_file_first_sf.txt) instead).

_Dr. Mārcis Gasūns_
