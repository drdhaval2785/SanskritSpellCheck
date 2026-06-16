# Cologne dictionary triage — index

Body-grounded **hybrid triage** status across all **33 Cologne dictionaries** in the
SanskritSpellCheck dataset (the dicts merged into [sanhw1.txt](../sanhw1.txt)). Each dict's
tier-A spelling candidates can be turned into a verified **FILE-FIRST** queue + a standing
**do-not-file** list by judging each candidate against the dictionary's *own entry text* —
run it with the **[`/dict-triage <DICT>`](../.claude/commands/dict-triage.md)** skill
(Sonnet classifies, Opus source-confirms, a human verifies).

**5 of 33 triaged** (MW · PW · VCP · PWG, plus SNP as the Review-phase validation dict).
Headline finding: tier-A precision is
**near-zero** on these mature dictionaries — the durable deliverable is the do-not-file list
and *preventing bad bulk edits*, not the handful of real typos.

| triaged | tier-A | fileable typos | do-not-file | combined precision |
|---|--:|--:|--:|--:|
| MW (English) | 1954 | **4** | 630 | 0.2% |
| PW (German) | 657 | **2** | 255 | 0.3% |
| VCP (Sanskrit) | 563 | **1** | 408 | 0.2% |
| PWG (German) | 497 | **12** | 248 | 2.4% |

## Status — all 33 dictionaries (by tier-A volume)

`tier-A` = engine tier-A candidate count (per-dict, from `combined_candidates.txt`). The dict
code links to its [csl-orig](https://github.com/sanskrit-lexicon/csl-orig) source (the entry
text the triage reads); **PD has no csl-orig source, so it cannot be body-triaged here.**

| dictionary | tier-A | triage status |
|---|--:|---|
| [MW](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/mw) — Monier-Williams (1899) | 1954 | ✅ **4 fileable · 630 do-not-file** — [readme](MW/readme.md) · [file-first](MW/MW_file_first_sf.txt) · [do-not-file](MW/MW_wrong_readings.txt) · [queue](MW/MW_triaged.txt) |
| PD | 1045 | ⛔ no csl-orig source — not body-triageable here |
| [BHS](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/bhs) — Edgerton, Buddhist Hybrid Sanskrit | 737 | — pending |
| [SCH](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/sch) — Schmidt, Nachträge | 678 | — pending |
| [PW](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/pw) — Böhtlingk–Roth, Petersburg | 657 | ✅ **2 fileable · 255 do-not-file** — [readme](PW/readme.md) · [file-first](PW/PW_file_first_sf.txt) · [do-not-file](PW/PW_wrong_readings.txt) · [queue](PW/PW_triaged.txt) |
| [VCP](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/vcp) — Vācaspatyam | 563 | ✅ **1 fileable · 408 do-not-file** — [readme](VCP/readme.md) · [file-first](VCP/VCP_file_first_sf.txt) · [do-not-file](VCP/VCP_wrong_readings.txt) · [queue](VCP/VCP_triaged.txt) |
| [PUI](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/pui) | 518 | — pending |
| [PWG](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/pwg) — Großes Petersburger Wörterbuch | 497 | ✅ **12 fileable · 248 do-not-file** — [readme](PWG/readme.md) · [file-first](PWG/PWG_file_first_sf.txt) · [do-not-file](PWG/PWG_wrong_readings.txt) · [queue](PWG/PWG_triaged.txt) |
| [SKD](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/skd) — Śabdakalpadruma | 412 | — pending |
| [MW72](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/mw72) — Monier-Williams (1872) | 360 | — pending |
| [YAT](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/yat) | 247 | — pending |
| [SHS](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/shs) | 246 | — pending |
| [ACC](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/acc) | 174 | — pending |
| [BUR](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/bur) — Burnouf | 162 | — pending |
| [IEG](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/ieg) — Sircar, Indian Epigraphical Glossary | 162 | — pending |
| [INM](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/inm) | 161 | — pending |
| [PE](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/pe) | 158 | — pending |
| [AP](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/ap) — Apte, Practical | 152 | — pending |
| [STC](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/stc) | 111 | — pending |
| [WIL](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/wil) — Wilson | 108 | — pending |
| [CAE](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/cae) | 89 | — pending |
| [AP90](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/ap90) — Apte (1890) | 53 | — pending |
| [MD](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/md) — Macdonell | 50 | — pending |
| [GST](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/gst) | 48 | — pending |
| [KRM](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/krm) | 47 | — pending |
| [GRA](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/gra) — Grassmann, Wörterbuch zum Rig-Veda | 45 | — pending |
| [BEN](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/ben) — Benfey | 43 | — pending |
| [VEI](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/vei) | 43 | — pending |
| [BOP](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/bop) — Bopp, Glossarium | 39 | — pending |
| [CCS](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/ccs) — Cappeller, Sanskrit-English | 35 | — pending |
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

### Ready to run — the 27 pending dictionaries (highest tier-A first)

Type any line into Claude Code (a slash-command is run by typing, not by clicking):

```
/dict-triage BHS
/dict-triage SCH
/dict-triage PUI
/dict-triage SKD
/dict-triage MW72
/dict-triage YAT
/dict-triage SHS
/dict-triage ACC
/dict-triage BUR
/dict-triage IEG
/dict-triage INM
/dict-triage PE
/dict-triage AP
/dict-triage STC
/dict-triage WIL
/dict-triage CAE
/dict-triage AP90
/dict-triage MD
/dict-triage GST
/dict-triage KRM
/dict-triage GRA
/dict-triage BEN
/dict-triage VEI
/dict-triage BOP
/dict-triage CCS
/dict-triage MCI
/dict-triage PGN
```

That accounts for all 33: **already triaged** (5, re-runs are stochastic — don't blindly
overwrite): `MW` `PW` `VCP` `PWG` `SNP`; **no csl-orig source** (1, not body-triageable here): `PD`.

