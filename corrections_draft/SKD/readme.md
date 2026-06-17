# SKD correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **412 tier-A** SKD (*Śabdakalpadruma*, the great
Sanskrit→Sanskrit encyclopaedic lexicon) headwords as possible misspellings. This package
triages them against SKD's *own Sanskrit (SLP1) entry text* (from
[csl-orig](https://github.com/sanskrit-lexicon/csl-orig)) — the second Sanskrit-body
dictionary triaged, after VCP.

Run with a **hybrid model split**: Sonnet 4.6 classified the 391 `realword` candidates,
Opus 4.8 source-confirmed the TYPO pile, and an **Opus Review phase** ran the adversarial
false-positive gate (reviewing out the 1 below); a human spot-checks before filing.

## The finding

> **Of 412 tier-A candidates, 3 are fileable typos** (4 source-confirmed, 1 reviewed out —
> see below). 290 are real distinct words; **103 are spellings SKD documents on purpose**
> (cross-references 14, `v.l.` 3, other grammatical/Sanskrit notes 86); 3 are not in the
> current source; ~13 need eyes. As with every Sanskrit-body dictionary, the decisive signal
> is *internal*: the entry's **own Sanskrit derivation (vyutpatti) contradicts the headword
> spelling**.

Across the dictionaries triaged, fileable-typo counts are
**MW 4 · PW 2 · VCP 1 · PWG 12 · SKD 3 · AP 0** — a tiny fraction of "tier A". Do **not** bulk-apply.

## The authoritative artifact

- **[SKD_file_first_sf.txt](SKD_file_first_sf.txt)** — the 3 FILE-FIRST candidates in
  CORRECTIONS standard format (the reviewed-out one is commented with `;`). Verify each on
  the scan, flip `n`→`y`, file.
- **[SKD_triaged.txt](SKD_triaged.txt)** — the full six-bucket queue.
- **[SKD_wrong_readings.txt](SKD_wrong_readings.txt)** — the standing **do-not-file** list
  (103 documented-intentional spellings, grouped by sub-type).

### The 3 FILE-FIRST candidates — each confirmed by the entry's own derivation

| wrong → right | class | the entry's own evidence |
|---|---|---|
| `hitAbalI → hitAvalI` | b/v | derivation `(hitAnAM AvalI yatra.)` uses **v**; the Hindi gloss `hiyAvalI` is **v** too — the headword `b` contradicts its own derivation |
| `pUzaBAzA → pUzaBAsA` | ṣ/s (sibilant) | derivation `(… BAsa + ac . wAp.)` derives it from √*bhās* (palatal **s**); headword `z` (retroflex ṣ) contradicts it |
| `vfzaBAzA → vfzaBAsA` | ṣ/s (sibilant) | derivation `(… BAsa + ac . striyAM wAp.)` again from √*bhās* (palatal **s**); headword `z` contradicts it |

> These are **candidates**, not confirmed corrections — the scan is the final arbiter, but
> each headword is contradicted by the *vyutpatti printed in its own entry*, so they are
> high-confidence.

### Reviewed out (do NOT file — a real word, not a typo)

- **`mahotka`** — the Opus review re-read the entry `(mahAn utkaH darSanotsuko loko yasyAH.)
  vidyut` and recognised a genuine **bahuvrīhi**: a name of lightning whose stem is
  *mahat + utka* (the `utkaH` appears in the derivation), not `mahotkA`. The Confirm pass had
  read the `strI` tag as demanding an `-ā` stem; the review caught that the feminine is the
  bahuvrīhi's, not the stem's. (A clean demonstration of the false-positive gate working on
  Sanskrit, not just on the European-language dictionaries.)

## Method

Same pipeline as the other dictionaries (driver: `python triage_dict.py SKD`), with the
Sanskrit `triage_lang` profile (`SKD → sa`) and a hybrid model split (`clsModel=sonnet`,
`confModel=opus`, `revModel=opus`). The deterministic markers settled 103 intentional
spellings before any LLM saw them; the body-aware pass + the Opus review handled the
`realword` remainder. The LLM layer is a triage prior — the scan confirms.

## Raw engine output (provenance — do NOT apply)

- [SKD_candidates.txt](SKD_candidates.txt) — the engine's 412 ranked tier-A candidates.
- [SKD_draft.txt](SKD_draft.txt) — draft updateByLine change-file; **superseded** by the
  triage (use [SKD_file_first_sf.txt](SKD_file_first_sf.txt) instead).
