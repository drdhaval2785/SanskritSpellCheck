# Cologne dictionary triage — index

Body-grounded **hybrid triage** status across all **33 Cologne dictionaries** in the
SanskritSpellCheck dataset (the dicts merged into [sanhw1.txt](../sanhw1.txt)). Each dict's
tier-A spelling candidates can be turned into a verified **FILE-FIRST** queue + a standing
**do-not-file** list by judging each candidate against the dictionary's *own entry text* —
run it with the **[`/dict-triage <DICT>`](../.claude/commands/dict-triage.md)** skill
(Sonnet classifies, Opus source-confirms, a human verifies).

**23 of 33 triaged — 112 fileable typos across 10 dicts; ~2,357 documented-intentional spellings catalogued.**
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
| MW (English, 1899) | 1954 | **4** | 630 |
| SKD (Sanskrit) | 412 | **3** | 103 |
| WIL (English, 1832) | 108 | **3** | 17 |
| PW (German) | 657 | **2** | 255 |
| VCP (Sanskrit) | 563 | **1** | 408 |
| GST (English, 1856) | 48 | **1** | 22 |
| _13 others_ — AP · MW72 · SCH · AP90 · MD · CAE · GRA · BEN · CCS · SNP · BHS · PUI · IEG | — | **0** | 617 |

## Status — all 33 dictionaries (by tier-A volume)

`tier-A` = engine tier-A candidate count (per-dict, from `combined_candidates.txt`). The dict
code links to its [csl-orig](https://github.com/sanskrit-lexicon/csl-orig) source (the entry
text the triage reads); **PD is not in `csl-orig`, but two external sources exist (to be
provided) — it becomes triageable once they are wired into the pipeline.**

| dictionary | tier-A | triage status |
|---|--:|---|
| [MW](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/mw) — Monier-Williams (1899) | 1954 | ✅ **4 fileable · 630 do-not-file** — [readme](MW/readme.md) · [file-first](MW/MW_file_first_sf.txt) · [do-not-file](MW/MW_wrong_readings.txt) · [queue](MW/MW_triaged.txt) |
| PD | 1045 | ⏳ source not in csl-orig — **two external sources to be provided**, then triageable |
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
| [BUR](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/bur) — Burnouf | 162 | — pending |
| [IEG](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/ieg) — Sircar, Indian Epigraphical Glossary | 162 | ✅ **0 fileable · 40 do-not-file** — [readme](IEG/readme.md) · [do-not-file](IEG/IEG_wrong_readings.txt) · [queue](IEG/IEG_triaged.txt) |
| [INM](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/inm) | 161 | — pending |
| [PE](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/pe) | 158 | — pending |
| [AP](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/ap) — Apte, Practical (English) | 152 | ✅ **0 fileable · 32 do-not-file** — [readme](AP/readme.md) · [do-not-file](AP/AP_wrong_readings.txt) · [queue](AP/AP_triaged.txt) |
| [STC](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/stc) | 111 | — pending |
| [WIL](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/wil) — Wilson (English, 1832) | 108 | ✅ **3 fileable · 17 do-not-file** — [readme](WIL/readme.md) · [file-first](WIL/WIL_file_first_sf.txt) · [do-not-file](WIL/WIL_wrong_readings.txt) · [queue](WIL/WIL_triaged.txt) |
| [CAE](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/cae) — Cappeller, Sanskrit-English (1891) | 89 | ✅ **0 fileable · 8 do-not-file** — [readme](CAE/readme.md) · [do-not-file](CAE/CAE_wrong_readings.txt) · [queue](CAE/CAE_triaged.txt) |
| [AP90](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/ap90) — Apte (1890) | 53 | ✅ **0 fileable · 8 do-not-file** — [readme](AP90/readme.md) · [do-not-file](AP90/AP90_wrong_readings.txt) · [queue](AP90/AP90_triaged.txt) |
| [MD](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/md) — Macdonell (1893) | 50 | ✅ **0 fileable · 1 do-not-file** — [readme](MD/readme.md) · [do-not-file](MD/MD_wrong_readings.txt) · [queue](MD/MD_triaged.txt) |
| [GST](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/gst) — Goldstücker (English, 1856) | 48 | ✅ **1 fileable · 22 do-not-file** — [readme](GST/readme.md) · [file-first](GST/GST_file_first_sf.txt) · [do-not-file](GST/GST_wrong_readings.txt) · [queue](GST/GST_triaged.txt) |
| [KRM](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/krm) | 47 | — pending |
| [GRA](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/gra) — Grassmann, Wörterbuch zum Rig-Veda (German, 1873) | 45 | ✅ **0 fileable · 7 do-not-file** — [readme](GRA/readme.md) · [do-not-file](GRA/GRA_wrong_readings.txt) · [queue](GRA/GRA_triaged.txt) |
| [BEN](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/ben) — Benfey (English, 1866) | 43 | ✅ **0 fileable · 14 do-not-file** — [readme](BEN/readme.md) · [do-not-file](BEN/BEN_wrong_readings.txt) · [queue](BEN/BEN_triaged.txt) |
| [VEI](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/vei) | 43 | — pending |
| [BOP](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/bop) — Bopp, Glossarium | 39 | — pending |
| [CCS](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/ccs) — Cappeller, Sanskrit-German | 35 | ✅ **0 fileable · 3 do-not-file** — [readme](CCS/readme.md) · [do-not-file](CCS/CCS_wrong_readings.txt) · [queue](CCS/CCS_triaged.txt) |
| [MCI](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/mci) | 24 | — pending |
| [PGN](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/pgn) | 10 | — pending |
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

### Ready to run — the 14 pending dictionaries (highest tier-A first)

Type any line into Claude Code (a slash-command is run by typing, not by clicking):

```
/dict-triage BHS
/dict-triage PUI
/dict-triage YAT
/dict-triage ACC
/dict-triage BUR
/dict-triage IEG
/dict-triage INM
/dict-triage PE
/dict-triage STC
/dict-triage KRM
/dict-triage VEI
/dict-triage BOP
/dict-triage MCI
/dict-triage PGN
```

That accounts for all 33: **already triaged** (18, re-runs are stochastic — don't blindly
overwrite): `MW` `PW` `VCP` `PWG` `SNP` `SKD` `AP` `MW72` `SCH` `SHS` `WIL` `GST` `CAE` `AP90`
`MD` `GRA` `BEN` `CCS`; **source not in csl-orig** (1): `PD` — two external sources to be
provided, then triageable.

## Planned: orthographic-drift study

A second axis on the same pipeline — checking the **gloss-language tokens** (German / English /
French / Latin / Russian) inside entry bodies against a **2026 standard**, to document how 19th-c.
spelling has drifted (German reformed 1901 + 1996; English convention drift; Russian 1918). It is
a **documentation / search-normalization layer, not a correction list**. Design:
**[../ORTHO_DRIFT_ROADMAP.md](../ORTHO_DRIFT_ROADMAP.md)**.

