# PW correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **657 tier-A** PW (Sanskrit–German *Petersburger
Wörterbuch*, Böhtlingk–Roth) headwords as possible misspellings. This package triages
them against PW's *own German entry text* (from
[csl-orig](https://github.com/sanskrit-lexicon/csl-orig)) — a spelling-only detector
cannot tell a typo from a real word, a deliberate variant, or PW's wrong-reading
apparatus, but the entry can.

## The finding

> **Of 657 engine "tier-A" candidates, only 2 (0.3%) are body-confirmed fileable typos.**
> 369 are real distinct words; **255 are spellings PW documents on purpose** — and PW's
> wrong-reading apparatus is *explicit and dense*: **95 entries literally say
> `fehlerhaft für …`** ("erroneous for"), plus `v.l.`, `s. u.` cross-references, and
> in-composition forms. Filing a "correction" for any of these would *delete
> Böhtlingk–Roth's own scholarship*. 1 candidate is stale (absent from the current
> source); 30 need human eyes.

"Tier A" is high *engine* confidence, **not** precision. **Do not bulk-apply it.**

## The authoritative artifact

- **[PW_triaged.txt](PW_triaged.txt)** — the review queue: six ranked buckets
  (FILE-FIRST · TYPO-UNSURE · REVIEW · REAL-WORD · INTENTIONAL · UNLOCATABLE), each row
  with PW's own entry text, the judgment, the source-confirmation, and a scan link.
- **[PW_file_first_sf.txt](PW_file_first_sf.txt)** — the 2 FILE-FIRST candidates in
  CORRECTIONS standard format (`PW:wrong:right:n`). Verify on the scan, flip `n`→`y`, file.
- **[PW_wrong_readings.txt](PW_wrong_readings.txt)** — the standing **do-not-file** list:
  255 headwords PW documents on purpose (wrong-reading `fehlerhaft für` 95, `v.l.` 38,
  in-composition 18, cross-reference 16, other 88), grouped by sub-type with the entry
  text. Use it as a suppression list so future runs never re-flag them.

### The 2 FILE-FIRST candidates (still verify on the scan)

| wrong → right | PW gloss | why it's a likely typo |
|---|---|---|
| `Bagama → BagaRa` | *"der Umlauf der Gestirne"* (revolution of the stars) | the word is *bhagaṇa* (भगण, retroflex ṇ) — the gloss fixes it unambiguously |
| `hemana → hEmana` | *"Adj. von heman"* | the adjective derived from *heman* is *haimana* (vṛddhi) — but note PW's `*` (constructed headword); check the scan |

> These are **candidates**, not confirmed corrections. A digital-text typo and a faithful
> rendering of a print error look identical here; only the scanned page decides.

## Why the raw engine output over-flags

PW deliberately records many non-standard spellings. Examples the triage caught:

- `SUci → Suci` — PW: *"{#SUci#} Adj. **fehlerhaft für** {#Suci#}"* — PW's own
  wrong-reading entry. Filing it deletes the apparatus.
- `candrAyaRa → cAndrAyaRa` — *"**fehlerhaft für** {#cAndrAyaRa#}"*.
- `saMvADa → saMvAda` — *"schlechte **Lesart für** {#saMbADa#}"* (a bad reading).
- `durvala → durbala`, `dARqaka → daRqaka` — marked *"**v. l.**"* (varia lectio).
- `duHka → duHKa`, `banDU → banDu` — *"**s. u.** {#…#}"* (siehe unter = cross-reference).
- `idAm → idam` — *"Denom. von {#idam#}"* — a real denominative entry, not a typo.

## Method (pipeline) — generalises to any dictionary

```sh
cd detectors
python make_dict_package.py PW     # extract PW tier-A from combined_candidates.txt -> PW_candidates/PW_draft
python triage_enrich.py PW         # k2 / DCS / cross-dict / confusion evidence
python triage_bodies.py PW         # attach each PW entry body + classify (German markers via triage_lang.py)
python triage_body_batches.py PW   # split the 'realword' set
#  -> run the body-aware LLM workflow (German rubric; classify TYPO/REALWORD/INTENTIONAL/UNSURE + source-confirm)
python triage_synthesize.py PW     # -> PW_triaged.txt + PW_file_first_sf.txt + PW_wrong_readings.txt
```

Language profiles (English MW / German PW·PWG / Sanskrit VCP) live in
[detectors/triage_lang.py](../../detectors/triage_lang.py). The LLM layer is a *triage
prior*, not a verdict — a human confirms each kept case against the scanned page.

## Raw engine output (provenance — do NOT apply)

- [PW_candidates.txt](PW_candidates.txt) — the engine's 657 ranked tier-A candidates.
- [PW_draft.txt](PW_draft.txt) — draft updateByLine change-file for all located
  candidates. **Superseded** by the triage (~99.7% should not be filed); use
  [PW_file_first_sf.txt](PW_file_first_sf.txt) instead.
