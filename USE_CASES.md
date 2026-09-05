_Created: 10-08-2026 · Last updated: 05-09-2026_

# SanskritSpellCheck — use cases

Goal-oriented guide to the toolset: pick your task, run the named tool, verify the
candidates against the scanned dictionary pages, and submit confirmed corrections to
[sanskrit-lexicon/CORRECTIONS](https://github.com/sanskrit-lexicon/CORRECTIONS/issues).

Everything operates on **SLP1** transliteration. Two input artefacts drive almost
everything:

- [`sanhw1.txt`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/sanhw1.txt) — every headword across ~36 Cologne dictionaries, one
  line `headword:DICT1,DICT2,…` (regenerated server-side; treat as a fixed input).
- the per-dictionary SLP1 stem dumps [`MWslp.txt`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/MWslp.txt), [`PWslp.txt`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/PWslp.txt),
  [`VCPslp.txt`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/VCPslp.txt), and the SLP1 corpus in [`CountVowels/`](CountVowels).

Two output conventions:

- **flagger** tools emit `X:CODE=Y:D` (headword : reason : dictionaries) — feed them
  to [`faultfinder3a-html.php`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/faultfinder3a-html.php) `repeat=2` for clickable
  reports and to [`triage_suspects.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/triage_suspects.py) to split signal/noise.
- **corrector** tools emit `DICT:wrong:right:n` — the CORRECTIONS standard format,
  ready for [`chg_nchg_sep.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/chg_nchg_sep.py) and submission.

Every result is a **candidate**, never an automatic fix. The final step is always a
human comparing the digital spelling to the printed page (see *Verify against scans*).

---

## 1. "Find suspect headwords in dictionary X" (pattern anomalies)

The original method: take X as a presumed-correct base, learn its vowel/consonant
cluster inventory, flag headwords in *other* dictionaries with a cluster X never uses.

```sh
sh faultfinder_regen.sh MW          # -> AllvsMW/{AllvsMW.txt,_sf.txt,-norepeat.html,dictwiseerrors3-table.html}
python triage_suspects.py AllvsMW/AllvsMW.txt AllvsMW/sig.txt AllvsMW/noise.txt
```

Best for **impossible clusters** (`SCC`, `CCCC-End`, etc.). Blind to
skeleton-preserving substitutions (a↔A, k↔K) — use §2 for those. The 2026 re-runs
live in [`Allvs_2026/`](Allvs_2026); the historical 2017 runs in `AllvsXX/`.

## 2. "Find the dominant errors — vowel-length, aspiration, sibilant" (~96% of real fixes)

These preserve the V/C skeleton, so the pattern detector cannot see them. Two
complementary detectors:

```sh
cd detectors
python consensus.py        # minority spelling vs the cross-dictionary majority
python spell_correct.py    # spelling whose neighbour is a trusted MW/PW/VCP form, ranked by corpus
```

- **consensus** is best when the correct form is attested in many dictionaries (it
  votes). Output ranked by attestation margin.
- **spell_correct** is best when a word is wrong in several *minor* dictionaries at
  once (it checks a curated MW+PW+VCP lexicon and the corpus, not vote counts).
  Start with its **corpus-corroborated** tier — the suggested form appears in real
  Mahābhārata/Rāmāyaṇa/Veda text.

## 3. "A dictionary contradicts itself"

```sh
cd detectors && python intra_dup.py
```
Flags a single dictionary that holds both a word and a rare confusion-variant of it
(the "compounds stated twice" class). Highest precision — it names the offending
dictionary and the word already proves the dictionary knows the right spelling.

## 3b. "Find an error every dictionary shares" (corpus-grounded)

```sh
cd detectors && python dict_vs_corpus.py
```
Uses the **DCS corpus** as an external witness: flags a headword absent from DCS whose
confusion-neighbour is a common DCS lemma, ranked by how many dictionaries carry the
suspect form. The only detector that can catch an error the dictionaries make
*unanimously* (there is no cross-dict disagreement to exploit). **Lowest precision** —
the list mixes real collective errors with distinct word-pairs (`guha`/`guhA`) and ī/i
citation differences; filter heavily.

DCS also strengthens the §2/§3 detectors: `spell_correct` ranks suggestions by DCS
frequency band (very-common corrections first), and all three correctors **suppress**
any headword that is itself an attested DCS lemma (a real word, not a typo).

## 4. "Validate encoding / charset"

```sh
cd detectors && python charset_check.py [path]
```
Flags any non-SLP1 character (Latin-with-diacritic, Greek, stray Devanagari, digits,
whitespace, danda). Point it at a raw dictionary file to catch the Ç/ç, Greek-numeral
and IAST-leak classes before they reach `sanhw1.txt`.

## 5. "Find phonotactically impossible forms"

```sh
cd detectors && python phonotactic_check.py [path]
```
Rule-based and absolute (unlike the statistical faultfinder): anusvara/visarga must
sit on a vowel, anusvara cannot precede a vowel, identical vowels cannot be adjacent.
Very high precision; catches violations even inside the base dictionary.

## 6. "Check a dictionary's alphabetic ordering"

```sh
cd detectors
python order_check.py --selftest
python order_check.py <dict_headwords_in_source_order.txt>
```
Needs the dictionary's headwords in *source* order (extract from the csl-orig text;
the `HeadwordLists/` here are pre-sorted). Reports adjacent pairs out of Sanskrit
collation order.

## 7. "Find errors in running text" (not headwords)

```sh
cd ngram && python ngramspellcheck.py data/test.txt data/error.txt 2
```
Flags words whose bigrams are absent from MW∩PW. Use `n=2`; trigrams over-flag.

## 8. "Build a review package for a human"

**Easiest — the unified runner.** [detectors/run_all.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/run_all.py) runs
every detector, dedups across them, tiers each candidate A/B/C (cross-detector
agreement = higher tier), and writes an accept/reject **review UI** plus the standard
format:

```sh
cd detectors && python run_all.py        # --rerun to regenerate detector outputs
# -> combined_review.html (open it: ✓/✗ per row, scan links, Export accepted/rejected)
#    combined_candidates.txt (full ranked list)   combined_sf.txt (DICT:wrong:right:n)
```
The exported `accepted_sf.txt` (rows flipped to `:y`) feeds [chg_nchg_sep.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/chg_nchg_sep.py)
(use case §10). Tier A = flagged by several detectors at once — verify those first.

**Per dictionary (campaign mode).** [detectors/run_campaign.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/run_campaign.py)
splits the suite per dictionary into `campaigns/<DICT>/review.html` + a dashboard
ranking dicts by tier-A count — work one dictionary's queue at a time, then
`make_changefiles.py` for that dict (§10).

**Per-detector / faultfinder route.** For a single flagger output:

```sh
php faultfinder3a-html.php  suspects.txt  suspects.html  2      # clickable Cologne links (repeat=2 renders every row)
php dictwisesorter-v3.php   suspects.html suspects-table.html   # grouped by dictionary
python triage_suspects.py  suspects.txt  sig.txt noise.txt     # -> also sig -priority.txt / -gemination.txt
```
`triage_suspects.py` splits **noise** (specialized-dict-only), **priority** (non-rcc
anomalies — verify first), and **gemination** (post-repha `r`+doubled-consonant —
usually faithful print, low priority).

## 9. "Verify against scans" (the human step)

Open the report; each word links to
`…/scans/awork/apidev/servepdf.php?dict=<D>&key=<word>`, the scanned page of the
printed dictionary. Compare the printed spelling to the digital one:

- **print matches digital** → faithful, *not* an error → add to
  [`nochange/nochange.txt`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/nochange/nochange.txt) so it stops being flagged.
- **print differs** → digitization error → record `DICT:wrong:right:y` and file it
  at CORRECTIONS.

The post-repha doublings (`sūryya`, `varṇṇa`) are usually the faithful printed form —
treat those as an editorial-normalization question for the maintainers, not bugs.

**Pre-triage with OCR (optional).** [detectors/ocr_verify.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/ocr_verify.py)
fetches each scan and (with tesseract + a Devanagari model installed) pre-labels
candidates CONFIRM/DENY/UNCERTAIN to reorder the queue — and even without OCR it
pre-caches the scan image next to each candidate. It is a triage prior only; a human
still confirms. Run small batches (the server rate-limits).

## 10. "Submit corrections"

The review UI (§8) exports `accepted_sf.txt` (verified rows as `DICT:wrong:right:y`).
Turn it into per-dictionary **draft change-files** in the CORRECTIONS updateByLine
format — each case's source line located in csl-orig with a proposed `<k1>`/`<k2>` edit:

```sh
cd detectors && python make_changefiles.py accepted_sf.txt   # -> changefiles/<DICT>_draft.txt
```
These are **drafts** — verify each `new` line against the scan, then file per the
[CORRECTIONS](https://github.com/sanskrit-lexicon/CORRECTIONS/issues) workflow. (Older
route: `python chg_nchg_sep.py corrected_sf.txt chg.txt nchg.txt` splits real
corrections from false positives, the latter feeding the whitelist.)

`make_changefiles.py` reads any `DICT:wrong:right` file and **skips `;`/`#` comment lines**, so you
can feed a `corrections_draft/<DICT>/<DICT>_file_first_sf.txt` (the triage FILE-FIRST queue, §11)
directly — its header and `; REVIEWED-OUT …` annotations are ignored.

## 11. "Decide which tier-A candidates are *real* — body-grounded triage"

A spelling detector can't tell a typo from a real word; the dictionary's **own entry** can. The
triage judges each tier-A candidate against the csl-orig entry text and emits a verified **FILE-FIRST**
queue + a standing **do-not-file** list. Hybrid models, driven by a skill:

```sh
/dict-triage <DICT>          # e.g. /dict-triage SHS  -- Sonnet classify, Opus confirm + review, you scan-verify
```

→ `corrections_draft/<DICT>/`: `<DICT>_file_first_sf.txt` (real typos), `<DICT>_wrong_readings.txt`
(do-not-file, grouped by w.r./v.l./in-comp./xref), `<DICT>_triaged.txt` (full bucketed queue),
`readme.md` (the finding). All **33 dicts are done** (index:
[corrections_draft/README.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/README.md)). Then fold the new do-not-file list into
the detector whitelist so nothing is re-flagged:

```sh
cd detectors && python gen_do_not_file_suppress.py   # -> nochange/do_not_file_suppress.txt (2,297 unique)
python eval.py                                        # false-positives must stay 0
```

⚠️ The LLM TYPO pass is **stochastic** — don't blindly re-run a verified package (a re-run can *lose*
typos). Tier-A precision is near-zero on mature dicts; the **do-not-file list is the real deliverable**
(see [docs/HYPOTHESES.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/HYPOTHESES.md) H1–H3).

## 12. "Triage a dictionary that isn't in csl-orig"

Some dicts have headwords in `sanhw1.txt` but no `csl-orig` source (e.g. **PD**, the Deccan College
*Encyclopaedic Dictionary*, CC BY-NC-SA). Stage the source once; the pipeline reads it transparently:

```sh
python detectors/get_external_source.py PD     # fetch+unzip -> external_src/pd/pd.txt (gitignored)
/dict-triage PD                                # then exactly as §11
```

`triage_util.source_file()` prefers `external_src/<dict>/<dict>.txt`, else `csl-orig` — so every
other dict is unaffected. Add a new source as a tuple in `get_external_source.py` `SOURCES`.

## 13. "Measure orthographic drift in the gloss languages (a second axis)"

Not an error list — a documentation layer: how far the 19th-c. gloss spelling (German/English/French/
Latin/Russian) has drifted from a 2026 standard. **Complete across 5 languages** — read
[docs/ORTHO_DRIFT_FINDINGS.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/ORTHO_DRIFT_FINDINGS.md).

```sh
cd detectors && python ortho_drift.py <DICT> --full     # de/en/fr/la per LANG_OF; KOSSOVICH = ru (jsonl)
```

Needs the language's modern **Hunspell `.dic`** (`$ORTHO_<L>_DIC`, or staged at
`external_src/hunspell/<lang>.dic` — e.g. `en_GB.dic` from `ropensci/hunspell`); without it, EN/DE
recall collapses to the curated map. To add a dictionary to a cluster (e.g. a modern-EN **recency
control**), register it in `LANG_OF` and run — the result is a row in `ortho_drift/<lang>_drift_summary.tsv`.
Finding: drift tracks the dictionary's *epoch* (WIL 1832 = 0.57/1k → MW 1899 = 0.01 → PD 1976 = 0.00).

## 14. "Grow the reform-pair lexicon from a diachronic corpus"

The reform map (`ortho_drift/<lang>_reform_map.tsv`) recognises drift forms. Extend it from a corpus
with a normalization layer — e.g. the **Deutsches Textarchiv** lingattr-TEI (`<w norm="MODERN">surface</w>`):

```sh
# 1. harvest surface != norm pairs from the corpus zip (streams it; skips corrupt members)
cd detectors && python extract_dta_pairs.py ../external_src/dta/dta_lingattr.zip ../external_src/dta/dta_de_pairs.tsv 20
# 2. dic-validated merge (accept iff old NOT in de_DE & new IN de_DE) -- filters OCR/dual-spellings
python merge_reform_pairs.py de ../external_src/dta/dta_de_pairs.tsv
```

The frequency floor (≥ 20×) is the precision lever — it drops OCR singletons (`aaal→all`) that
dic-validation alone passes. This grew `de_reform_map.tsv` **2,823 → 15,685** clean pairs (`vnd→und`,
`Theil→Teil`, `creutz→kreuz`). Any `old<TAB>new` TSV works (RIDGES, Wikipedia, hand-curated).

---

## End-to-end example (MW, vowel-length focus)

```sh
cd detectors
python spell_correct.py ../sanhw1.txt mw_corr.txt          # 906 corpus-corroborated of 9921
grep '^MW:' mw_corr.txt > mw_only.txt                       # just MW rows
# -> build a clickable report for review, verify each against the MW scan,
#    flip confirmed rows to :y, then chg_nchg_sep.py -> submit.
```

## Choosing the right tool

| You have… | Use |
|---|---|
| a base dictionary you trust | faultfinder (§1) |
| the dominant macron/aspiration/sibilant errors | consensus + spell_correct (§2) |
| a dictionary suspected of internal dupes | intra_dup (§3) |
| a raw file with possible encoding junk | charset_check (§4) |
| structurally-impossible forms | phonotactic_check (§5) |
| a source-order headword list | order_check (§6) |
| running text, not a headword list | ngram (§7) |
| tier-A candidates and need *which are real* | body-grounded triage (§11) |
| a dictionary not in csl-orig | external-source staging (§12) |
| a question about gloss-language spelling change | ortho-drift (§13) |
| a diachronic corpus with a normalization layer | reform-pair harvest (§14) |

For the project's confirmed / refuted / open hypotheses (incl. *why* corpus-based tier-C promotion
was rejected), see **[docs/HYPOTHESES.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/HYPOTHESES.md)**.

_Dr. Mārcis Gasūns_
