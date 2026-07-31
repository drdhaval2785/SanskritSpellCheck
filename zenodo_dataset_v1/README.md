# SanskritSpellCheck derived-data package — Zenodo release v1

_Created: 27-07-2026 · Last updated: 27-07-2026_

This is the FAIR data package for the **first Zenodo dataset release** of the analytical
layer built on top of [SanskritSpellCheck](https://github.com/drdhaval2785/SanskritSpellCheck)
— a QA / error-detection toolset for the
[Cologne Digital Sanskrit Dictionaries](http://www.sanskrit-lexicon.uni-koeln.de/) (CDSL),
originated by Dr. Dhaval Patel. It packages the six derived-data assets named in
[ROADMAP_2026_2027.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ROADMAP_2026_2027.md)
Q4 2026 item 3, staged for a human to upload to Zenodo — see `DOI: pending` below and the
`@DO` row this release adds to `Uprava/GTD_NEXT_ACTIONS.md`.

**This package ships derived analytical data only** — headword-pair confusions, statistics,
whitelists, and verdict indices. It does **not** reproduce any dictionary's full entry text,
and it deliberately **excludes** the per-dictionary `*_wrong_readings.txt` files that quote
dictionary entries verbatim (several of those are sourced from CC BY-NC-SA material — see
"Excluded / not in this package" below). All Sanskrit text throughout is **SLP1**
transliteration.

## What's in `data/`

| File(s) | What it is | Rows/entries | Source pipeline |
|---|---|---:|---|
| `o_vs_O_evaluation_pairs.txt` | Minimal-pair headword confusions across CDSL dictionaries (format `word1:word2-dict1:dict2`), the output of the [o_vs_O](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/o_vs_O/readme.md) detector after removing >1-letter-difference, y/Y/r/R-only, <4-letter, same-dictionary, and `nochange.txt`-whitelisted pairs | **3,884** | `php o_vs_O.php` → `o_vs_O2.txt` |
| `confusion_weights.json` | Per-character-pair substitution weights (e.g. `Aa`: vowel-length confusion) mined from the 3,884 evaluation pairs above, plus raw counts | 20 weighted pairs, `n_pairs=3884` | [`detectors/gen_confusion_weights.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/gen_confusion_weights.py) over `o_vs_O2.txt` |
| `do_not_file_suppress.txt` | The deduplicated, headword-only suppression list: SLP1 headwords across CDSL that *look* like misspellings but are documented-intentional (wrong-reading apparatus, v.l., sandhi/in-composition forms, cross-references) — collected from the body-grounded triage of all 33 CDSL dictionaries in `sanhw1.txt` | **2,297** unique headwords | [`detectors/gen_do_not_file_suppress.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/gen_do_not_file_suppress.py) |
| `do_not_file_counts_by_dict.tsv` | Per-dictionary raw do-not-file counts (before cross-dict dedup) — the ~2,549-entry figure quoted in the roadmap is the **sum of this table** (2,549 exactly); the dedup in `do_not_file_suppress.txt` above is smaller because some headwords repeat across dictionaries | 33 dicts, Σ = **2,549** | counted directly from `corrections_draft/<DICT>/<DICT>_wrong_readings.txt` (counts only — entry text excluded, see below) |
| `file_first_verified.tsv` | The FILE-FIRST verified-correction candidate set from the first triage pass over all 33 dicts: `dict\twrong\tright\tverdict\tnote`, mechanically verified against `csl-orig` entry text (Sonnet 5) and adjudicated (Fable 5) | **122** rows (92 PASS + 17 SCAN-FIRST + 11 EDITORIAL + 1 DNF + 1 DROP) | `corrections_draft/file_first_verified.tsv`, 2026-07-02 |
| `union_d7.tsv` | **The union-across-runs FILE-FIRST set** (roadmap ruling D7): a second independent body-aware triage pass on the three high-yield dicts (SHS/YAT/ACC), unioned against the first pass. Single-run agreement is only 35% (Jaccard) — the union lifts SHS 37→68, YAT 27→61, ACC 22→27, a **+81%** recall gain. `status` ∈ {BOTH_RUNS, NET_NEW, RUN1_ONLY_LLM_VARIANCE, RUN1_ONLY_SETTLED_MISSING}; `opus_review`=`fileable` for 124/156 rows | 156 rows (68 SHS + 61 YAT + 27 ACC) | `corrections_draft/union_d7.tsv`, H1471, 26-07-2026; measurement: [docs/HYPOTHESES.md § H9](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/HYPOTHESES.md#h9--union-across-runs-materially-raises-recall-one-run-recovers-only-13-of-the-two-run-union) |
| `reform_maps/{de,ru,fr,en,la}_reform_map.tsv` | Per-gloss-language orthographic reform maps (old spelling → 2026-standard spelling, with frequency) for the German/Russian/French/English/Latin gloss tokens found inside CDSL entry bodies | de 15,685 · ru 7,709 · fr 18 · en 76 · la 0 (header-adjusted; see `docs/ORTHO_DRIFT_FINDINGS.md`) | [`detectors/ortho_drift.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/ortho_drift.py) |
| `meter/GRETIL_TEXT_TYPOS.md` | Candidate list of 124 loci flagged by MW∩PW headword-bigram screening over ~101k tokens of GRETIL Kavya-section text | 124 candidate loci | [`detectors/meter/ngram_corpus_check.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/meter/ngram_corpus_check.py) |
| `meter/GRETIL_UPSTREAM_REPORT.md` | Hand-verified GRETIL e-text corrections report: **60 verified error loci across 7 texts** (2 systematic classes + 11 anomalous), 53 documented false positives | 60 verified / 124 screened | H456, Fable 5 hand-verification, 10-07-2026 |
| `meter/METER_VARIETY_STATS*.md` (5 files) | Meter/pāda-variety census per GRETIL section (overall, epic, purana, smrti, subhasita) | 5 section reports | [`detectors/meter/variety_stats.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/meter/variety_stats.py) |
| `meter/SECTIONS_DATASET.md` | The 5-section GRETIL Kavya corpus manifest (57 texts, ~26k verses) underlying the meter index | corpus manifest | [`detectors/meter/build_section_dataset.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/meter/build_section_dataset.py) |
| `meter/MULTISECTION_ERROR_CANDIDATES.md` + `.tsv` | Headwords whose meter-corroboration signal recurs across multiple GRETIL sections | 21 rows | [`detectors/meter/multisection_error_candidates.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/meter/multisection_error_candidates.py) |
| `meter/ngram_typos_{epic,pilot,purana,smrti,subhasita}.tsv` | Per-section bigram-screen typo candidates that feed `GRETIL_TEXT_TYPOS.md` | 123 rows total | `detectors/meter/ngram_corpus_check.py` |
| `meter/PILOT_OTHER_SECTIONS.md` | The pilot report extending the meter validator from the epic section to purana/smrti/subhasita | pilot report | H277-b |

Every file's SHA-256 checksum is in [`checksums.sha256`](checksums.sha256) (sha256sum format,
verify with `sha256sum -c checksums.sha256` from this directory). Checksums are computed on
the LF-normalized (git-blob) content — the form a `git clone`, GitHub zipball, or the
Zenodo–GitHub integration archive actually delivers. A local Windows checkout with
`core.autocrlf=true` will show CRLF line endings and therefore **different** local hashes
than this file — that's an expected checkout-time transform, not a corrupted download.

## Excluded / not in this package

- **Per-dictionary `*_wrong_readings.txt` files** ([`corrections_draft/`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/README.md)) —
  several quote dictionary entry text verbatim as evidence for each do-not-file verdict.
  `PD` ([Deccan College *Encyclopaedic Dictionary*](https://sanskrit-lexicon.uni-koeln.de/scans/PDScan/2020/web/index.php))
  is **CC BY-NC-SA and not committed to the source repo at all** per its own `CLAUDE.md`
  policy — its 116-entry do-not-file list is counted (not quoted) in
  `do_not_file_counts_by_dict.tsv` above. This package ships the safe, headword-only,
  cross-dictionary aggregate (`do_not_file_suppress.txt`) instead of the per-dict files.
- **`meter_verdicts.jsonl`** (the raw per-verse meter identification index, ~26k verses) —
  gitignored and regenerable (`detectors/meter/build_meter_index.py`, ~1 hour offline,
  needs `skrutable`/`chanda`/`vidyut-chandas`); not an already-built, already-committed
  artifact. The committed **summary** deliverables (`METER_VARIETY_STATS*.md`,
  `MULTISECTION_ERROR_CANDIDATES.*`, `SECTIONS_DATASET.md`) are included instead.
- The full GRETIL raw corpus text (also CC BY-NC-SA, local-only per repo convention) — not
  reproduced; only the curated typo/verdict summaries derived from it.

## Derivation pipeline

All source scripts live in [drdhaval2785/SanskritSpellCheck](https://github.com/drdhaval2785/SanskritSpellCheck)
at the commit this release was cut from (see `metadata.yaml` → `source_commit`). The
top-level methodology: `sanhw1.txt` (merged CDSL headword list) → `o_vs_O.php` / `faultfinder3a.php`
(pattern/pair detectors) → `detectors/*` (confusion model, body-grounded LLM triage,
orthographic-drift, meter validator) → this package. Full method description:
[README.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/README.md) "Logic"
section and [CLAUDE.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/CLAUDE.md).

## Known caveats

- The body-grounded LLM triage pass is **stochastic** — do-not-file/FILE-FIRST counts are a
  snapshot as of the commit this release is cut from, not a fixed ground truth; re-running
  the triage can surface additional (not fewer) do-not-file entries.
- Tier-A LLM-triage precision is **near-zero on mature, much-corrected dictionaries** (MW,
  PW, VCP …) — the do-not-file lists are the durable value there, not the handful of real
  typos. See [`corrections_draft/README.md`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/README.md).
  Real-typo yield concentrates in poorly-digitised sources (SHS 15%, YAT 11%, PWG 2.4%).
  Full source: [SanskritLexicography/FINDINGS.md](https://github.com/gasyoun/SanskritLexicography/blob/master/FINDINGS.md).
  Sensitivity note: the 15%/11%/2.4% figures are per-word tier-A rates for SHS/YAT/PWG
  respectively — read the linked table before citing a bare percentage.
- The orthographic reform maps are a **documentation / search-normalization layer**, not a
  spelling-correction list — see [docs/ORTHO_DRIFT_FINDINGS.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/ORTHO_DRIFT_FINDINGS.md).
- The GRETIL upstream report's 11 "anomalous" loci are listed **without** a proposed fix —
  the correct reading is genuinely uncertain there.
- `reform_maps/la_reform_map.tsv` and `fr_reform_map.tsv` are near-empty by design (Latin
  shows ~0 drift, French convention drift is low) — this is a measured result, not missing data.

## How to cite

See [`CITATION.cff`](CITATION.cff). `DOI: pending` — this package is staged for upload;
Zenodo DOI minting is a human `@DO` (needs a Zenodo-account-holder's login/API token), tracked
in `Uprava/GTD_NEXT_ACTIONS.md`. A paper citing this dataset should not ship to a venue while
the DOI is pending.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) for the derived data in this
package — see [`LICENSE-DATA`](LICENSE-DATA). This is a data license, distinct from the
parent repository's code license (none formally declared at the repo root as of this
release — see [drdhaval2785/SanskritSpellCheck](https://github.com/drdhaval2785/SanskritSpellCheck)).
Underlying CDSL dictionary headwords are hosted at
[sanskrit-lexicon.uni-koeln.de](http://www.sanskrit-lexicon.uni-koeln.de/); this package
does not reproduce their entry text (see "Excluded" above).

_Dr. Mārcis Gasūns_
