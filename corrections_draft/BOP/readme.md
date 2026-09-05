_Created: 10-08-2026 · Last updated: 05-09-2026_

# BOP correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **39 tier-A** BOP headwords as possible misspellings. BOP is
Bopp's *Glossarium Sanscritum* (1847) — a Sanskrit lexicon glossed in **Latin**, with grammatical
derivations (`r. <root> praef. <prefix> s. <suffix>`) and classical-text citations. This package
triages the candidates against BOP's *own entry text* (from
[csl-orig](https://github.com/sanskrit-lexicon/csl-orig/tree/main/v02/bop)).

## The finding

> **Of 32 located engine "tier-A" candidates, 0 are body-confirmed fileable typos.** 24 are real,
> distinct words (each with its own Latin gloss and derivation), 6 are spellings BOP documents on
> purpose, 1 needs the printed page, 1 is not in the current source.

This is the expected outcome for a mature 19th-century scholarly lexicon, and BOP is also the
study's **Latin negative control**: Latin orthography saw no modern reform, so the gloss language
introduces no spelling drift (matching the ortho-drift result LA = 0). Nearly every flagged form is
either a genuine distinct word — most often a **feminine in `-ā`** that BOP gives its own entry
(`kalaSA`/`argalA`/`preraRA` "f. id.", `anuyAtrA` "comitatus", `niravadyA` "pulchritudo"), an
**A-grade derivative** (`Ardita` "vexatus", `Ardana` "vexator" ← r. `ard`), or a **long-vowel
root** (`lUp` "occidere; furari", cl. 10) — or an explicit Latin cross-reference (`vAhu` *v.*
`bAhu`, `dUz` *v.* `duz`). The detector's one-letter "suggestions" (e.g. `Ced`→ced, a palatal-ch
root) repeatedly merge two distinct words, confirming no real digitization error surfaced.

Cross-dict fileable precision: SHS 37/246 · YAT 27/247 · ACC 22/174 · … · BHS 0/713 · PUI 0/518 ·
IEG 0/162 · **BOP 0/39**.

## The authoritative artifacts

- **[BOP_wrong_readings.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/BOP/BOP_wrong_readings.txt)** — the **do-not-file** list: 6 deliberate
  spellings (cross-reference 4, other 2). Folded into
  [nochange/do_not_file_suppress.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/nochange/do_not_file_suppress.txt).
- **[BOP_triaged.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/BOP/BOP_triaged.txt)** — full queue: 24 REAL-WORD distinct words + 6 INTENTIONAL +
  1 REVIEW (`BAgiraTI`, short-i derivation `ab BAgiraTa`, internally consistent — left for the scan)
  + 1 UNLOCATABLE.
- **[BOP_file_first_sf.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/BOP/BOP_file_first_sf.txt)** — **empty** (0 fileable).

## Method

`detectors/triage_dict.py BOP` (package) → body-aware HYBRID classification (BOP registered as
**Latin** in `triage_lang.py`: `vitiose`/`male pro`/`lege` = wrong-reading, `vide`/`cf.` =
cross-reference) → source-confirm the TYPO pile on Opus → `triage_dict.py BOP --finish`. The classify
pass returned 0 TYPO, so the confirm/review piles were empty. **DRAFT for human review; never edits
`csl-orig`.**

_Dr. Mārcis Gasūns_
