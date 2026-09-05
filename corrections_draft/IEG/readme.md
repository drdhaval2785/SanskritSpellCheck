_Created: 10-08-2026 · Last updated: 05-09-2026_

# IEG correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **162 tier-A** IEG headwords as possible misspellings. IEG is
Sircar's *Indian Epigraphical Glossary* — technical terms attested in Indian inscriptions, glossed
in English with inscription sigla (CII, EI, IE, SII, …). This package triages the candidates
against IEG's *own entry text* (from [csl-orig](https://github.com/sanskrit-lexicon/csl-orig)).

## The finding

> **Of 162 engine "tier-A" candidates, 0 are body-confirmed fileable typos.** 101 are real,
> attested epigraphic terms (each with its own gloss and inscription siglum), 40 are spellings IEG
> documents on purpose, 3 are unlocatable.

This is the expected outcome for an *epigraphical glossary*. IEG deliberately records inscriptional
spellings — Prakrit doubling, retroflex/dental shifts (ṭ/t, ḍ/d, ṇ/n), ś/s, vowel-length and
anusvāra variation are normal epigraphic phenomena, not typos. A flagged form is almost always
either a genuine attested term in its own right (`yugā` "a voucher", CII 4) or an explicit
cross-reference to its Sanskrit equivalent (`dāṇa` "same as dāna", `ṭāṅk` "same as ṭaṅka",
`valīvarda` "variant spelling of balīvarda") — the hallmark IEG pattern. Several detector
"suggestions" are unrelated words (`nakara`→makara, `kAnuka`→kāmuka), confirming the one-letter
heuristic surfaced no real digitization errors here.

Cross-dict fileable precision: SHS 37/246 · YAT 27/247 · ACC 22/174 · … · BHS 0/713 · PUI 0/518 ·
**IEG 0/162**.

## The authoritative artifacts

- **[IEG_wrong_readings.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/IEG/IEG_wrong_readings.txt)** — the **do-not-file** list: 40 deliberate
  spellings (cross-reference 21, other 19). Folded into
  [nochange/do_not_file_suppress.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/nochange/do_not_file_suppress.txt).
- **[IEG_triaged.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/IEG/IEG_triaged.txt)** — full queue: 101 REAL-WORD attested terms + 40 INTENTIONAL.
- **[IEG_file_first_sf.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/IEG/IEG_file_first_sf.txt)** — **empty** (0 fileable).

## Method

`detectors/triage_dict.py IEG` (package) → body-aware classification (IEG registered as English in
`triage_lang.py`) → `triage_dict.py IEG --finish`. With 0 TYPO classifications there was no
source-confirm / review pile. **DRAFT for human review; never edits `csl-orig`.**

_Dr. Mārcis Gasūns_
