# MW correction candidates — DRAFT for human review

The unified detector engine ([detectors/run_all.py](../../detectors/run_all.py))
applied to **MW**: the **1,954 tier-A** correction candidates (cross-detector
agreement / DCS-frequency / high-precision flaggers), with **1,943 located** in the
csl-orig source as ready-to-file change-file lines.

> **These are CANDIDATES, not confirmed corrections.** Tier A means *high engine
> confidence*, not *verified*. The list mixes genuine typos with **legitimate variant
> / inflected forms** the engine cannot distinguish without the printed page. Verify
> every case against the scan before filing anything. **Do not bulk-apply.**

Worked examples of the judgment required:
- `marga → mArga` — looks like a real typo (mārga "path"). ✓ likely file.
- `atrA → atra`, `vAcas → vacas`, `pARI → pARi` — `atrā` / `vācas` / `pāṇī` may be
  legitimate inflected/variant headwords; **probably leave**.
- `prAvft → pravft` — the entry's own `<k2>` is `prA-vft`, i.e. the dictionary
  *intends* prā-; the "correction" is likely **wrong**. Always read `<k2>`.

## Files
- [MW_candidates.txt](MW_candidates.txt) — ranked candidates: `score · wrong → right ·
  detectors · morph`. The evidence view (which detectors agreed, vidyut morph tag).
- [MW_draft.txt](MW_draft.txt) — updateByLine change-file (CORRECTIONS format): per
  case a `; Case` comment with a scan link, then the located `old`/`new` source lines
  editing the `<k1>`/`<k2>` key. **Drafts** — verify, prune, then file.

## How to review → file
1. Open a case's scan link (`servepdf.php?dict=MW&key=<wrong>`); read the printed headword.
2. Print matches the suggestion → it's a real typo → keep the case; flip its line to `:y`.
3. Print matches the current (suspect) spelling, or `<k2>` shows it's intentional → drop the case.
4. File the kept cases per the [CORRECTIONS](https://github.com/sanskrit-lexicon/CORRECTIONS/issues)
   workflow (one issue per dictionary).

## Regenerate
```sh
cd detectors && python run_all.py ../sanhw1.txt          # -> combined_candidates.txt
# extract MW tier-A rows -> mw_sf.txt (MW:wrong:right:n), then:
python make_changefiles.py mw_sf.txt ../../csl-orig ../corrections_draft/MW
```
Provenance: unified engine over sanhw1.txt; detectors = spell_correct (DCS-ranked),
consensus, intra_dup, dict_vs_corpus, phonotactic, charset; tiering in run_all.
