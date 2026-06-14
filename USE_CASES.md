# SanskritSpellCheck — use cases

Goal-oriented guide to the toolset: pick your task, run the named tool, verify the
candidates against the scanned dictionary pages, and submit confirmed corrections to
[sanskrit-lexicon/CORRECTIONS](https://github.com/sanskrit-lexicon/CORRECTIONS/issues).

Everything operates on **SLP1** transliteration. Two input artefacts drive almost
everything:

- [`sanhw1.txt`](sanhw1.txt) — every headword across ~36 Cologne dictionaries, one
  line `headword:DICT1,DICT2,…` (regenerated server-side; treat as a fixed input).
- the per-dictionary SLP1 stem dumps [`MWslp.txt`](MWslp.txt), [`PWslp.txt`](PWslp.txt),
  [`VCPslp.txt`](VCPslp.txt), and the SLP1 corpus in [`CountVowels/`](CountVowels).

Two output conventions:

- **flagger** tools emit `X:CODE=Y:D` (headword : reason : dictionaries) — feed them
  to [`faultfinder3a-html.php`](faultfinder3a-html.php) `repeat=2` for clickable
  reports and to [`triage_suspects.py`](triage_suspects.py) to split signal/noise.
- **corrector** tools emit `DICT:wrong:right:n` — the CORRECTIONS standard format,
  ready for [`chg_nchg_sep.py`](chg_nchg_sep.py) and submission.

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

After generating any flagger output:

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
  [`nochange/nochange.txt`](nochange/nochange.txt) so it stops being flagged.
- **print differs** → digitization error → record `DICT:wrong:right:y` and file it
  at CORRECTIONS.

The post-repha doublings (`sūryya`, `varṇṇa`) are usually the faithful printed form —
treat those as an editorial-normalization question for the maintainers, not bugs.

## 10. "Submit corrections"

The corrector detectors already emit `DICT:wrong:right:n`. After a human flips
verified rows to `:y`, split and route them:

```sh
python chg_nchg_sep.py corrected_sf.txt chg.txt nchg.txt   # chg = real corrections, nchg -> whitelist
```
Submit `chg.txt` per the [CORRECTIONS](https://github.com/sanskrit-lexicon/CORRECTIONS/issues)
workflow.

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
