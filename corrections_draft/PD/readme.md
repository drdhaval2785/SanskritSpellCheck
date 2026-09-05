_Created: 10-08-2026 · Last updated: 05-09-2026_

# PD correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **1,007 tier-A** PD headwords as possible misspellings. PD is the
*Encyclopaedic Dictionary of Sanskrit on Historical Principles* (A. M. Ghatage et al., Deccan College,
Poona, 1976–2009; **English** glosses) — the one Cologne-listed dictionary **not in the `csl-orig`
merge**. Its first source (the [PDScan 2020 edition](https://sanskrit-lexicon.uni-koeln.de/scans/PDScan/2020/web/index.php),
55 MB, 107,630 entries) is staged at `external_src/pd/` (gitignored; CC BY-NC-SA 3.0 © The Sanskrit
Library / Thomas Malten). This package triages the candidates against PD's *own entry text*.

> **Triaged on source 1 (2026-06-24).** A second PD source is expected; re-running it against the
> merged source later would only refine the do-not-file list — the 0-fileable finding is robust.

## The finding

> **Of 920 body-judged tier-A candidates, 0 are body-confirmed fileable typos.** 888 are real,
> distinct words, **116 are spellings PD documents on purpose**, 1 was a classified typo that
> source-confirm refuted, 2 need the printed page. (87 more of the 1,007 were settled deterministically
> as apparatus before the LLM; 0 unlocatable — every PD headword resolved in the source.)

This is the expected outcome for a modern, meticulously-edited historical-principles dictionary — and
PD has by far the **richest documented-intentional apparatus** of any dictionary triaged so far. As a
*historical* lexicon it deliberately records non-standard attested spellings with full citations and
an explicit editorial verdict:

- **66 varia-lectio** (`v. l.`) — e.g. `aGni` (v.l. `aGniya`, TaiPrāti.), `anAdfzwi` (v.l. `ºdf`).
- **16 wrong-reading** (`w. r. for`) — `aGAra` "[w. r. for `AGAra`]", `agneyI` "(w. r. for *āgneyī*)",
  `akzoWa` "[w. r. for *akṣoṭa*] walnut" — each a real entry PD prints *because* it documents the error.
- **22 cross-reference** + **12 other** grammatical/Vedic notes.

Filing a "correction" for any of these would corrupt PD's editorial record. The lone typo-unsure
case (`akzAMsa`→akṣāṃśa) was correctly held: PD defines it as its own `[MW]`-sourced headword, not as
apparatus. The 2 review items (`atiTya`, `aDovARa` — a v/b proper-noun) need the scan.

Cross-dict fileable precision: SHS 37/246 · YAT 27/247 · ACC 22/174 · … · BHS 0/713 · BUR 0/162 ·
**PD 0/1007** (largest tier-A set; richest do-not-file list at 116).

## The authoritative artifacts

- **[PD_wrong_readings.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/PD/PD_wrong_readings.txt)** — the **do-not-file** list: 116 deliberate
  spellings (varia-lectio 66, wrong-reading 16, cross-reference 22, other 12). Folded into
  [nochange/do_not_file_suppress.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/nochange/do_not_file_suppress.txt) (suppression list →
  33 dicts / 2,297 unique; `eval.py` false-positives 0 after `run_all.py --rerun`).
- **[PD_triaged.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/PD/PD_triaged.txt)** — full queue: 888 REAL-WORD + 116 INTENTIONAL + 1 TYPO-UNSURE
  + 2 REVIEW.
- **[PD_file_first_sf.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/PD/PD_file_first_sf.txt)** — **empty** (0 fileable).

## Source & method

- **Source 1:** `external_src/pd/pd.txt` — re-fetch with `python detectors/get_external_source.py PD`.
  **Source 2:** TBD — register its URL as a second tuple under `PD` in
  [detectors/get_external_source.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/get_external_source.py), then re-stage and re-run.
- `detectors/triage_dict.py PD` (package; reads PD via `triage_util.source_file()` → `external_src/`)
  → body-aware HYBRID classification (PD registered `en`) → source-confirm the TYPO pile on Opus →
  **Opus false-positive review** → `triage_dict.py PD --finish`. **DRAFT for human review; never edits
  the source.**

_Dr. Mārcis Gasūns_
