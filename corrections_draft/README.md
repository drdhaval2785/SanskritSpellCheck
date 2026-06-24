# Cologne dictionary triage — index

Body-grounded **hybrid triage** status across all **33 Cologne dictionaries** in the
SanskritSpellCheck dataset (the dicts merged into [sanhw1.txt](../sanhw1.txt)). Each dict's
tier-A spelling candidates can be turned into a verified **FILE-FIRST** queue + a standing
**do-not-file** list by judging each candidate against the dictionary's *own entry text* —
run it with the **[`/dict-triage <DICT>`](../.claude/commands/dict-triage.md)** skill
(Sonnet classifies, Opus source-confirms, a human verifies).

**ALL 33 triaged — 122 fileable typos across 11 dicts; ~2,549 documented-intentional spellings catalogued.**
The last one, **PD** (Deccan College *Encyclopaedic Dictionary*, English, 107,630 entries, wired in via
`external_src/`), triaged 2026-06-24 on its first source — **0 fileable** but the **richest do-not-file
list at 116** (66 v.l., 16 w.r.). A second PD source is expected; re-running it later only refines that
list. The three cross-language dicts **BUR** / **STC** (French) and **BOP** (Latin) also came in
**0 fileable**, as expected for mature foreign-gloss lexica.
Tier-A precision stays **near-zero** on mature, much-corrected dictionaries — the durable
deliverable is the do-not-file list and *preventing bad bulk edits*, not the handful of real
typos. The exception is **poorly-digitised sources**: SHS (15%), YAT (11%) and PWG (2.4%) carry many
real OCR/keying errors, each confirmed by the entry's own etymology/inflection.

| triaged (fileable > 0) | tier-A | fileable typos | do-not-file |
|---|--:|--:|--:|
| SHS (English, 1900) | 246 | **37** | 31 |
| YAT (English, 1846) | 247 | **27** | 1 |
| ACC (Catalogus Cat., 1891) | 174 | **22** | 25 |
| PWG (German) | 497 | **12** | 248 |
| MCI (mythical-name index) | 41 | **10** | 3 |
| MW (English, 1899) | 1954 | **4** | 630 |
| SKD (Sanskrit) | 412 | **3** | 103 |
| WIL (English, 1832) | 108 | **3** | 17 |
| PW (German) | 657 | **2** | 255 |
| VCP (Sanskrit) | 563 | **1** | 408 |
| GST (English, 1856) | 48 | **1** | 22 |
| _18 others_ — AP · MW72 · SCH · AP90 · MD · CAE · GRA · BEN · CCS · SNP · BHS · PUI · IEG · INM · PE · VEI · PGN · KRM | — | **0** | 655 |

## Status — all 33 dictionaries (by tier-A volume)

`tier-A` = engine tier-A candidate count (per-dict, from `combined_candidates.txt`). The dict
code links to its [csl-orig](https://github.com/sanskrit-lexicon/csl-orig) source (the entry
text the triage reads); **PD is not in `csl-orig`, but two external sources exist (to be
provided) — it becomes triageable once they are wired into the pipeline.**

| dictionary | tier-A | triage status |
|---|--:|---|
| [MW](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/mw) — Monier-Williams (1899) | 1954 | ✅ **4 fileable · 630 do-not-file** — [readme](MW/readme.md) · [file-first](MW/MW_file_first_sf.txt) · [do-not-file](MW/MW_wrong_readings.txt) · [queue](MW/MW_triaged.txt) |
| [PD](https://sanskrit-lexicon.uni-koeln.de/scans/PDScan/2020/web/index.php) — Encyclopaedic Dict. of Sanskrit (Deccan College, 1976–2009) | 1007 | ✅ **0 fileable · 116 do-not-file** (source 1; richest apparatus: 66 v.l./16 w.r.) — [readme](PD/readme.md) · [do-not-file](PD/PD_wrong_readings.txt) · [queue](PD/PD_triaged.txt) |
| [BHS](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/bhs) — Edgerton, Buddhist Hybrid Sanskrit | 713 | ✅ **0 fileable · 294 do-not-file** — [readme](BHS/readme.md) · [do-not-file](BHS/BHS_wrong_readings.txt) · [queue](BHS/BHS_triaged.txt) |
| [SCH](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/sch) — Schmidt, Nachträge (German, 1928) | 678 | ✅ **0 fileable · 109 do-not-file** — [readme](SCH/readme.md) · [do-not-file](SCH/SCH_wrong_readings.txt) · [queue](SCH/SCH_triaged.txt) |
| [PW](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/pw) — Böhtlingk–Roth, Petersburg | 657 | ✅ **2 fileable · 255 do-not-file** — [readme](PW/readme.md) · [file-first](PW/PW_file_first_sf.txt) · [do-not-file](PW/PW_wrong_readings.txt) · [queue](PW/PW_triaged.txt) |
| [VCP](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/vcp) — Vācaspatyam | 563 | ✅ **1 fileable · 408 do-not-file** — [readme](VCP/readme.md) · [file-first](VCP/VCP_file_first_sf.txt) · [do-not-file](VCP/VCP_wrong_readings.txt) · [queue](VCP/VCP_triaged.txt) |
| [PUI](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/pui) — Purāṇic Index (names) | 518 | ✅ **0 fileable · 21 do-not-file** — [readme](PUI/readme.md) · [do-not-file](PUI/PUI_wrong_readings.txt) · [queue](PUI/PUI_triaged.txt) |
| [PWG](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/pwg) — Großes Petersburger Wörterbuch | 497 | ✅ **12 fileable · 248 do-not-file** — [readme](PWG/readme.md) · [file-first](PWG/PWG_file_first_sf.txt) · [do-not-file](PWG/PWG_wrong_readings.txt) · [queue](PWG/PWG_triaged.txt) |
| [SKD](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/skd) — Śabdakalpadruma (Sanskrit) | 412 | ✅ **3 fileable · 103 do-not-file** — [readme](SKD/readme.md) · [file-first](SKD/SKD_file_first_sf.txt) · [do-not-file](SKD/SKD_wrong_readings.txt) · [queue](SKD/SKD_triaged.txt) |
| [MW72](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/mw72) — Monier-Williams (1872, 1st ed) | 360 | ✅ **0 fileable · 77 do-not-file** — [readme](MW72/readme.md) · [do-not-file](MW72/MW72_wrong_readings.txt) · [queue](MW72/MW72_triaged.txt) |
| [YAT](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/yat) — Yates, Sanskrit-English (1846) | 247 | ✅ **27 fileable · 1 do-not-file** (+32 b/v held for scan) — [readme](YAT/readme.md) · [file-first](YAT/YAT_file_first_sf.txt) · [do-not-file](YAT/YAT_wrong_readings.txt) · [queue](YAT/YAT_triaged.txt) |
| [SHS](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/shs) — Śabda-Sāgara (English, 1900) | 246 | ✅ **37 fileable · 31 do-not-file** — [readme](SHS/readme.md) · [file-first](SHS/SHS_file_first_sf.txt) · [do-not-file](SHS/SHS_wrong_readings.txt) · [queue](SHS/SHS_triaged.txt) |
| [ACC](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/acc) — Aufrecht, Catalogus Catalogorum | 174 | ✅ **22 fileable · 25 do-not-file** — [readme](ACC/readme.md) · [file-first](ACC/ACC_file_first_sf.txt) · [do-not-file](ACC/ACC_wrong_readings.txt) · [queue](ACC/ACC_triaged.txt) |
| [BUR](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/bur) — Burnouf, Dict. classique sanscrit-français (1866) | 162 | ✅ **0 fileable · 20 do-not-file** — [readme](BUR/readme.md) · [do-not-file](BUR/BUR_wrong_readings.txt) · [queue](BUR/BUR_triaged.txt) |
| [IEG](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/ieg) — Sircar, Indian Epigraphical Glossary | 162 | ✅ **0 fileable · 40 do-not-file** — [readme](IEG/readme.md) · [do-not-file](IEG/IEG_wrong_readings.txt) · [queue](IEG/IEG_triaged.txt) |
| [INM](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/inm) — Sörensen, Index of Names (Mahābhārata) | 161 | ✅ **0 fileable · 16 do-not-file** — [readme](INM/readme.md) · [do-not-file](INM/INM_wrong_readings.txt) · [queue](INM/INM_triaged.txt) |
| [PE](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/pe) — Mani, Purāṇic Encyclopaedia | 158 | ✅ **0 fileable · 13 do-not-file** — [readme](PE/readme.md) · [do-not-file](PE/PE_wrong_readings.txt) · [queue](PE/PE_triaged.txt) |
| [AP](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/ap) — Apte, Practical (English) | 152 | ✅ **0 fileable · 32 do-not-file** — [readme](AP/readme.md) · [do-not-file](AP/AP_wrong_readings.txt) · [queue](AP/AP_triaged.txt) |
| [STC](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/stc) — Stchoupak–Nitti–Renou, Dict. Sanscrit-Français (1932) | 111 | ✅ **0 fileable · 9 do-not-file** — [readme](STC/readme.md) · [do-not-file](STC/STC_wrong_readings.txt) · [queue](STC/STC_triaged.txt) |
| [WIL](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/wil) — Wilson (English, 1832) | 108 | ✅ **3 fileable · 17 do-not-file** — [readme](WIL/readme.md) · [file-first](WIL/WIL_file_first_sf.txt) · [do-not-file](WIL/WIL_wrong_readings.txt) · [queue](WIL/WIL_triaged.txt) |
| [CAE](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/cae) — Cappeller, Sanskrit-English (1891) | 89 | ✅ **0 fileable · 8 do-not-file** — [readme](CAE/readme.md) · [do-not-file](CAE/CAE_wrong_readings.txt) · [queue](CAE/CAE_triaged.txt) |
| [AP90](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/ap90) — Apte (1890) | 53 | ✅ **0 fileable · 8 do-not-file** — [readme](AP90/readme.md) · [do-not-file](AP90/AP90_wrong_readings.txt) · [queue](AP90/AP90_triaged.txt) |
| [MD](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/md) — Macdonell (1893) | 50 | ✅ **0 fileable · 1 do-not-file** — [readme](MD/readme.md) · [do-not-file](MD/MD_wrong_readings.txt) · [queue](MD/MD_triaged.txt) |
| [GST](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/gst) — Goldstücker (English, 1856) | 48 | ✅ **1 fileable · 22 do-not-file** — [readme](GST/readme.md) · [file-first](GST/GST_file_first_sf.txt) · [do-not-file](GST/GST_wrong_readings.txt) · [queue](GST/GST_triaged.txt) |
| [KRM](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/krm) — Kramadīśvara dhātupāṭha (Sanskrit) | 47 | ✅ **0 fileable · 6 do-not-file** — [readme](KRM/readme.md) · [do-not-file](KRM/KRM_wrong_readings.txt) · [queue](KRM/KRM_triaged.txt) |
| [GRA](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/gra) — Grassmann, Wörterbuch zum Rig-Veda (German, 1873) | 45 | ✅ **0 fileable · 7 do-not-file** — [readme](GRA/readme.md) · [do-not-file](GRA/GRA_wrong_readings.txt) · [queue](GRA/GRA_triaged.txt) |
| [BEN](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/ben) — Benfey (English, 1866) | 43 | ✅ **0 fileable · 14 do-not-file** — [readme](BEN/readme.md) · [do-not-file](BEN/BEN_wrong_readings.txt) · [queue](BEN/BEN_triaged.txt) |
| [VEI](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/vei) — Macdonell–Keith, Vedic Index | 43 | ✅ **0 fileable · 2 do-not-file** — [readme](VEI/readme.md) · [do-not-file](VEI/VEI_wrong_readings.txt) · [queue](VEI/VEI_triaged.txt) |
| [BOP](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/bop) — Bopp, Glossarium Sanscritum (Latin, 1847) | 39 | ✅ **0 fileable · 6 do-not-file** — [readme](BOP/readme.md) · [do-not-file](BOP/BOP_wrong_readings.txt) · [queue](BOP/BOP_triaged.txt) |
| [CCS](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/ccs) — Cappeller, Sanskrit-German | 35 | ✅ **0 fileable · 3 do-not-file** — [readme](CCS/readme.md) · [do-not-file](CCS/CCS_wrong_readings.txt) · [queue](CCS/CCS_triaged.txt) |
| [MCI](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/mci) — mythical-name index | 41 | ✅ **10 fileable · 3 do-not-file** — [readme](MCI/readme.md) · [file-first](MCI/MCI_file_first_sf.txt) · [do-not-file](MCI/MCI_wrong_readings.txt) · [queue](MCI/MCI_triaged.txt) |
| [PGN](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/pgn) — proper-name index (inscriptions) | 21 | ✅ **0 fileable · 1 do-not-file** — [readme](PGN/readme.md) · [do-not-file](PGN/PGN_wrong_readings.txt) · [queue](PGN/PGN_triaged.txt) |
| [SNP](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/snp) | 4 | ✅ **0 fileable · 3 do-not-file** (Review-phase validation dict) — [readme](SNP/readme.md) · [do-not-file](SNP/SNP_wrong_readings.txt) · [queue](SNP/SNP_triaged.txt) |

> Names are given where well-established (per the CDSL catalogue); uncertain ones show the
> code only. ~10 further csl-orig dictionaries (abch, acph, acsj, ae, armh, bor, lan, lrv,
> mwe, pwkvn) are not in the `sanhw1` merge and have no tier-A candidates here.

## How to triage a pending dictionary

> **Handing off to a new chat?** Paste-ready prompt + the one-line form in **[HANDOFF.md](HANDOFF.md)**.

```sh
# from the repo root (csl-orig must be a sibling):
cd detectors && python triage_dict.py <DICT>     # build package + emit hybrid launch args
#   -> launch detectors/bodyaware_workflow.js with the printed args (Sonnet classify / Opus confirm)
python triage_dict.py <DICT> --finish            # synthesize the package
#   -> human-verify each FILE-FIRST candidate against the entry, then commit
```

Or just run the **[`/dict-triage <DICT>`](../.claude/commands/dict-triage.md)** skill, which
drives the whole sequence (incl. the source-verification rubric and the do-not-file list).

### All 33 dictionaries triaged

**Every dict in the dataset is now triaged.** PD was the last — runnable once its first source was
staged in `external_src/pd/` (the body-grounded triage reads it exactly like a `csl-orig` dict).

**PD's second source is still expected.** When it arrives, register its URL as a second tuple under
`PD` in [../detectors/get_external_source.py](../detectors/get_external_source.py), re-stage, and
re-run `/dict-triage PD`. Re-runs are **stochastic** and PD's 0-fileable finding is robust, so a
re-run only refines the 116-entry do-not-file list — don't blindly overwrite the committed package.

```sh
python detectors/get_external_source.py PD   # (re)stage PD's sources on a fresh clone
/dict-triage PD                              # re-run once source 2 is registered
```

See [PD/readme.md](PD/readme.md) for the source list, license, and second-source slot.

## Planned: orthographic-drift study

A second axis on the same pipeline — checking the **gloss-language tokens** (German / English /
French / Latin / Russian) inside entry bodies against a **2026 standard**, to document how 19th-c.
spelling has drifted (German reformed 1901 + 1996; English convention drift; Russian 1918). It is
a **documentation / search-normalization layer, not a correction list**. Design:
**[../ORTHO_DRIFT_ROADMAP.md](../ORTHO_DRIFT_ROADMAP.md)**.

