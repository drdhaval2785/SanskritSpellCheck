# ACC correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **174 tier-A** ACC headwords as possible misspellings. ACC is
Aufrecht's *Catalogus Catalogorum* (1891–1903) — a catalogue of Sanskrit works and authors, each
entry a normalised title/author-name with a terse manuscript-source citation (`{#argalA#} stotra.
Oppert II, 1727.`). This package triages the candidates against ACC's *own entry text* (from
[csl-orig](https://github.com/sanskrit-lexicon/csl-orig)).

## The finding

> **Of 174 engine "tier-A" candidates, 22 are body-confirmed fileable typos.** These are
> digitization errors in *normalised work-titles* — mostly a dropped long ā in well-known titles
> (`bfhannArayaRopanizad → bfhannArAyaRopanizad`, `dakziRamUrtisaMhitA → dakziRAmUrtisaMhitA`,
> `SravaRadvAdaSIvratakalpa → SrAvaRa…`), plus vr→b (`EtareyavrAhmaRa → EtareyabrAhmaRa`,
> `SatapaTavrAhmaRa → SatapaTabrAhmaRa`), retroflex ḍ (`zadftuvarRana → zaqftuvarRana`), and
> sibilant/aspirate (`gAyatrIBAsya → gAyatrIBAzya`, `kAwakopanizad → kAWakopanizad`). 68 are real
> distinct titles/names, 25 are documented-intentional, 25 need eyes, 4 are typo-unsure.

Cross-dict fileable precision: SHS 37/246 · YAT 27/247 · **ACC 22/174** · PWG 12/497 · MW 4/1954 ·
… · BHS 0/713 · PUI 0/518. ACC is mid-yield: a catalogue's normalised titles are standard enough
that a dropped diacritic is a real keying error — but still verify each on the scan.

### ⚠️ Direction + faithful-colophon caveats

The detector pairs some candidates **backwards** — the review gate caught `aBijYAnaSAkuntala`
(*Abhijñānaśākuntala*, already correct with long ā; the "suggestion" would have *shortened* it) and
excluded it. ACC also faithfully records catalogue/colophon spellings, which vary; the gate held
back redirect entries (`{{Lbody}}`), a vṛddhi ambiguity (`darSa-`/`dārśa-`), and an
empty-body/variant case. So **every FILE-FIRST row is DRAFT (`:n`)** — verify against the Aufrecht
scan before filing.

## The authoritative artifacts

- **[ACC_file_first_sf.txt](ACC_file_first_sf.txt)** — the **FILE-FIRST** queue: 22 candidates in
  CORRECTIONS standard format (`ACC:wrong:right:n`). Verify each on the scan, flip `n`→`y`, then
  `python chg_nchg_sep.py …`.
- **[ACC_wrong_readings.txt](ACC_wrong_readings.txt)** — the do-not-file list: 25 deliberate
  spellings (cross-reference 10, other 15). Folded into
  [nochange/do_not_file_suppress.txt](../../nochange/do_not_file_suppress.txt).
- **[ACC_triaged.txt](ACC_triaged.txt)** — full queue: 22 FILE-FIRST, 4 TYPO-UNSURE, 25 REVIEW
  (eyes), 68 REAL-WORD, 25 INTENTIONAL.

## Method

`detectors/triage_dict.py ACC` (package) → body-aware classification (ACC registered as English in
`triage_lang.py`) → **source-confirm + false-positive review** of every TYPO against its full ACC
entry, with explicit *direction* and *faithful-colophon* checks → `triage_dict.py ACC --finish`.
**DRAFT for human review** — never edits `csl-orig`.
