# PE correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **158 tier-A** PE headwords as possible misspellings. PE is
Mani's *Purāṇic Encyclopaedia* — an encyclopaedia of proper names (deities, sages, kings, demons,
places) drawn from the Purāṇas and epics, glossed in English. Triaged against PE's *own entry text*
(from [csl-orig](https://github.com/sanskrit-lexicon/csl-orig)).

## The finding

> **Of 158 engine "tier-A" candidates, 0 are body-confirmed fileable typos.** 138 are real,
> distinct named entities (each with its own description and Purāṇa/epic citation), 13 are spellings
> PE documents on purpose (cross-references and explicit dual-spelling headwords like
> "VAKANAKHA (BAKANAKHA)"), 1 is unlocatable.

Expected for a *proper-name encyclopaedia*: the ALL-CAPS headword the entry describes is the
attested name itself, not a misspelling of a commoner word.

Cross-dict fileable precision: SHS 37/246 · YAT 27/247 · ACC 22/174 · … · BHS 0/713 · PUI 0/518 ·
IEG 0/162 · INM 0/161 · **PE 0/158**.

## The authoritative artifacts

- **[PE_wrong_readings.txt](PE_wrong_readings.txt)** — the **do-not-file** list: 13 deliberate
  spellings (cross-reference 10, other 3). Folded into
  [nochange/do_not_file_suppress.txt](../../nochange/do_not_file_suppress.txt).
- **[PE_triaged.txt](PE_triaged.txt)** — full queue: 138 REAL-WORD + 13 INTENTIONAL.
- **[PE_file_first_sf.txt](PE_file_first_sf.txt)** — **empty** (0 fileable).

## Method

`detectors/triage_dict.py PE` (package; PE registered as English in `triage_lang.py`) → body-aware
classification → `--finish`. 0 TYPO → no source-confirm/review pile. **DRAFT; never edits `csl-orig`.**
