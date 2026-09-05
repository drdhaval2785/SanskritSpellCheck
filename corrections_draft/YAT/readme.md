_Created: 10-08-2026 · Last updated: 05-09-2026_

# YAT correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **247 tier-A** YAT headwords as possible misspellings. YAT is
Yates' *Dictionary in Sanscrit and English* (Calcutta, Baptist Mission Press, **1846**) — a
verbal-root–rich Sanskrit–English lexicon. This package triages the candidates against YAT's *own
entry text* (from [csl-orig](https://github.com/sanskrit-lexicon/csl-orig)).

## The finding

> **Of 247 engine "tier-A" candidates, 27 are body-confirmed fileable typos (10.9%)** — a
> **high-yield outlier**, like SHS (Śabda-Sāgara, also 1900/Bengal). Each is a clean,
> non-b/v digitization error whose **own entry citation/gloss** proves the correct spelling. A
> further **32 are b↔v pairs held back for scan verification** (see caveat), 123 are real distinct
> roots/words, 13 need eyes, 15 are unlocatable, 1 is documented-intentional.

YAT, like SHS, is a **poorly-digitised 19th-century Bengal-region source**, so — unlike mature
dictionaries (MW 4/1954, PW 2/657) — its tier-A carries many real OCR/keying errors, each made
high-confidence by the entry's own evidence: a root whose conjugation form fixes the consonants
(`{#RaB#}` keyed but conjugated `{#naBati#}` → √nabh), a gloss that names the word
(`saNGati` glossed "a collecting" = saṅgati), or an internal declension that contradicts the key
(`avasfzWa` with body declension `(zwaH-zwA-zwaM)` → the key's `W` should be `w`).

### ⚠️ The b↔v caveat (why 32 candidates are NOT in FILE-FIRST)

Yates (1846) was printed in Bengal, where **Bengali orthography does not distinguish व (va) from
ब (ba)** — both are written ব. So the ~32 `b`↔`v` candidates the detector flagged (`agniballaBa` →
agnivallabha, `daSavala` → daśabala, `netrAmvu` → netrāmbu, …) **may be faithful to the printed
page**, not digitization errors — exactly analogous to the post-repha gemination that
`faultfinder` deliberately excludes. The text alone cannot tell a keying error from a faithful
Bengali-convention spelling; **only the original scan can.** These sit in `YAT_triaged.txt`'s
TYPO-UNSURE bucket (do **not** bulk-file them) and a human should check each Devanāgarī scan
(व vs ब on the page) before deciding.

Cross-dict fileable precision: SHS 37/246 · **YAT 27/247** · PWG 12/497 · MW 4/1954 · SKD 3/412 ·
WIL 3/108 · PW 2/657 · VCP 1/563 · GST 1/48 · BHS 0/713 · PUI 0/518 — the high-yield cases are all
poorly-digitised sources.

## The authoritative artifacts

- **[YAT_file_first_sf.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/YAT/YAT_file_first_sf.txt)** — the **FILE-FIRST** queue: 27 body-confirmed,
  review-survived typos in CORRECTIONS standard format (`YAT:wrong:right:n`). **Verify each on the
  scan, flip the trailing `n`→`y`, then** `python chg_nchg_sep.py …`. Error classes: dental-n vs
  retroflex-ṇ (`RaB→naB`, `Rij→nij`, `drAvana→drAvaRa`, `AparAhnika→AparAhRika`,
  `pakzipARIyaSAlikA→pakzipAnIyaSAlikA`, `prAkPAlguRa→prAkPAlguna`), sibilant (`arsasa→arSasa`,
  `pratisidDa→pratizidDa`, `asaMSakta→asaMsakta`, `pAradfzvan→pAradfSvan`), aspiration
  (`duzwu→duzWu`, `vizwABU→vizWABU`, `cInapizWa→cInapizwa`, `saNGati→saNgati`, `gaDABft→gadABft`,
  `lakzmIpala→lakzmIPala`, `avasfzWa→avasfzwa`, `prAyopavizWa→prAyopavizwa`, `zazWihAyana→zazwihAyana`,
  `vESizWya→vESizwya`), vowel-length (`mayAvin→mAyAvin`, `mahAmayA→mahAmAyA`, `aSanayA→aSanAyA`,
  `hantAkAra→hantakAra`, `AkzadyUta→akzadyUta`, `ambukfta→ambUkfta`).
- **[YAT_triaged.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/YAT/YAT_triaged.txt)** — full queue: 27 FILE-FIRST, 40 TYPO-UNSURE (the b/v +
  uncertain), 13 REVIEW (eyes), 123 REAL-WORD, 1 INTENTIONAL, 15 unlocatable.
- **[YAT_wrong_readings.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/YAT/YAT_wrong_readings.txt)** — the do-not-file list (only 1 here; YAT
  carries little apparatus). Folded into [nochange/do_not_file_suppress.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/nochange/do_not_file_suppress.txt).

## Method

`detectors/triage_dict.py YAT` (package) → body-aware classification (TYPO/REALWORD/INTENTIONAL/
UNSURE; YAT registered as English in `triage_lang.py`) → **source-confirm** of every TYPO against
its full YAT entry → **false-positive review** (the gate that held back the b/v cluster and the
mis-paired ṇ→m suggestions) → `triage_dict.py YAT --finish`. **DRAFT for human review** — the
27 FILE-FIRST must each be scan-verified before filing to CORRECTIONS; never edits `csl-orig`.

_Dr. Mārcis Gasūns_
