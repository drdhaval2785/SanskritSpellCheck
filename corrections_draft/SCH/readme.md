_Created: 10-08-2026 · Last updated: 05-09-2026_

# SCH correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **678 tier-A** SCH (Richard Schmidt, *Nachträge zum
Sanskrit-Wörterbuch* — the 1928 German supplement to the Böhtlingk–Roth Petersburg
dictionaries) headwords as possible misspellings. This package triages them against SCH's
*own German entry text* (from [csl-orig](https://github.com/sanskrit-lexicon/csl-orig)).

Run with a **hybrid model split**: Sonnet 4.6 classified the 644 `realword` candidates,
Opus 4.8 source-confirmed the TYPO pile, and an **Opus Review phase** ran the adversarial
false-positive gate (reviewing out all 3 confirmed candidates — see below).

## The finding

> **Of 678 tier-A candidates, 0 are fileable typos** (3 confirmed-TYPO, all reviewed out).
> 520 are real distinct words; **109 are spellings SCH documents on purpose** (wrong-reading
> 18, `v.l.` 7, in-composition 6, cross-references 3, other grammatical/Vedic notes 75); 3 are
> not in the current source; 46 need eyes (the terse Schmidt entries push more cases to
> UNSURE than the discursive dictionaries). Tier-A precision is **near-zero**.

Across the dictionaries triaged, fileable-typo counts are
**MW 4 · PW 2 · VCP 1 · PWG 12 · SKD 3 · AP 0 · MW72 0 · SCH 0**. Do **not** bulk-apply.

## The authoritative artifact

- **[SCH_wrong_readings.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/SCH/SCH_wrong_readings.txt)** — the standing **do-not-file** list
  (109 documented-intentional spellings, grouped by sub-type).
- **[SCH_triaged.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/SCH/SCH_triaged.txt)** — the full six-bucket queue.
- **[SCH_file_first_sf.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/SCH/SCH_file_first_sf.txt)** — empty of fileable rows; the 3
  reviewed-out cases are commented with `;`.

### Reviewed out (do NOT file — real words / a variant, not typos)

- **`uluka`** — entry defines it as `m. N. pr. eines Schlangendämons` (Mahāvyutpatti); the
  `Vgl. ulūka, Ulluka` is a *compare* cross-reference, not a correction to `ulūka`.
- **`ayoDana`** — `m. N. eines Fürsten`; the entry's `(oder degha-na?)` queries the *second*
  element, not the initial `a`, so it is not a typo for `AyoDana`.
- **`koSalikA`** — Schmidt gives `kosalika 'Geschenk'` with `[pw kau~]` explicitly flagging
  pw's `kausalika` as a variant spelling — a deliberate variant note, not an error.

The gate pulling all three (a snake-demon name, a prince's name, and a documented variant)
across the German supplement mirrors the SKD/`mahotka` and MW72/`ahnika` saves — evidence the
Opus false-positive review generalises across all three body languages.

## Method

Same pipeline as the other dictionaries (driver: `python triage_dict.py SCH`), with the
German `triage_lang` profile (`SCH → de`) and a hybrid model split. Deterministic markers
settled 109 intentional spellings (incl. Schmidt's `fehlerhaft`/`v.l.` apparatus) before any
LLM saw them; the body-aware pass + the Opus review handled the `realword` remainder.

## Raw engine output (provenance — do NOT apply)

- [SCH_candidates.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/SCH/SCH_candidates.txt) — the engine's 678 ranked tier-A candidates.
- [SCH_draft.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/SCH/SCH_draft.txt) — draft updateByLine change-file; **superseded** by the triage.

_Dr. Mārcis Gasūns_
