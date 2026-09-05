# Grammar-example audit prototype — csl-kale (H4154, Lane A)

_Created: 05-09-2026 · Last updated: 05-09-2026_

Port of the [bashspell](https://github.com/AigizK/bashspell) grammar-audit pattern
(`tools/audit_grammar_reference.py`, report `reports/grammar-audit-2026-09-05.md`) to the
Sanskrit estate. Tool: [tools/audit_grammar_examples.py](../../tools/audit_grammar_examples.py).
Context: [bashspell lessons](../bashspell-lessons-2026-09-05.md) §3.

**The framing is the point: every reject below is a CANDIDATE FOR LINGUISTIC REVIEW,
NOT a confirmed defect.** Grammar sources cite stem/citation forms, sandhi-rule sides,
metalanguage and historical forms; the bashspell baseline measured 1,461 rejects ≠ 1,461
defects. No dictionary was edited, nothing was promoted into eval.py (red lines, H4154).

## Sources chosen

Survey verdict (handoff asked: survey, then pick 1–2 machine-extractable sources):

| Candidate | Verdict |
|---|---|
| **csl-kale** `disp/files1/kale*.txt` | **CHOSEN.** Page-anchored lines (`kale_Page_NNN …`) with Sanskrit example words in `<span class="san">…</span>`, estate-standard SLP1, 18 chapter files. |
| csl-whitroot / WhitneyRoots Whitney material | Not machine-extractable now: `whitscans.txt` is a scan-JPG list; Warnemyr HTML (WhitneyRoots/1885) is romanized prose + `<b>` paradigm heads in a non-SLP1 scheme — needs a romanization map before it can join the audit (follow-up). |
| KocherginaUchebnik_1998 | `Kochergina_unicode.mdx` is Unicode prose (Russian + Devanagari examples in running text) — extraction is a NLP job, not a span-crawl; its `LessonPacks/srs_aggregate.json` is a synthetic learner-data fixture, not grammar examples. Follow-up lane. |
| Elizarenkova_2004 | Single Russian PDF; pdftotext blanks Cyrillic (estate danger fact) — excluded. |

### SHA-256 manifest — source files (csl-kale disp/files1, chrome excluded: kalefiles.txt, kaletop.txt)

| File | sha256 (16) | File | sha256 (16) |
|---|---|---|---|
| kale00.txt | a706db24d23b7f42 | kale09.txt | 61f65a458035af58 |
| kale01.txt | 821554d4805dc06b | kale10.txt | decde66bfd1078f2 |
| kale02.txt | 315886697ad3bbfc | kale11.txt | bd926fc153ec3c64 |
| kale03.txt | deda90e39a4e928e | kale12.txt | 7bb2cba71e1a08b7 |
| kale04.txt | 282b8382878304d8 | kale13.txt | 6cbe65ea53dfae00 |
| kale05.txt | 6feed72e15f9dbae | kale14.txt | 0a7623dc649f998a |
| kale06.txt | 939a2c779ba3abde | kale15.txt | 5ed76bfe4dff007b |
| kale07.txt | b6990837974ff28c | kaleDK.txt | 21d0a38c9a979ccb |
| kale08.txt | 76e3c0c2c1984515 | kalePR.txt | 3cbeae7990619f9c |

Full hashes + per-file charset/line stats: `scan.json` → `sources`.

### SHA-256 manifest — dictionaries and analyzer oracle used

| Resource | sha256 (16) | Entries |
|---|---|---|
| sanhw1.txt | 13dd58122174517e | 431,596 headword→dict rows |
| MWslp.txt | 88ca00d7e6f6f328 | 193,978 |
| PWslp.txt | 5005f153b69fff27 | 131,918 |
| VCPslp.txt | 20dcb23ea01e573d | 47,107 |
| detectors/vidyut_stems.txt (untracked in main tree; see note) | 2bf14948de9fb177 | 205,233 |
| vidyut-data/sandhi/rules.csv (compound-split evidence) | f691868cdf76da8c | — |

vidyut attribution: stems from [vidyut](https://github.com/ambuda-org/vidyut) (ambuda-org,
MIT) via `detectors/gen_vidyut_stems.py`; vote mode here: `full` (stems + sandhi/compound
split check). Reproduce: `python tools/audit_grammar_examples.py --vidyut-stems <stems.txt>`.

## Counts

| Metric | Value |
|---|---|
| Source files crawled | 18 |
| Pages (page anchors, incl. contentless markers) | 730 |
| Unique example words (post-filter) | 139 |
| Accepted (exact match in sanhw1) | 133 (95.7%) |
| Review candidates (not in sanhw1) | **6** — tier A 0 · tier B 4 · tier C 2 |
| Unparsable pieces / lines (recorded, never dropped) | 0 / 0 |
| Single-letter spans skipped (counted filter: vowels/letters as examples) | 65 |

Checks per example: (a) sanhw1 membership + MW/PW/VCP membership; (b) vidyut vote
(stem-exact → proven compound-split → conservative ending-strip → unparsed). SLP1
validation via sanskrit-util alphabet; length guard ≤40; multi-token spans split;
single-letter spans counted, not candidates; BOM/charset sniff with recorded fallback
(all sources decoded utf-8 cleanly).

## Review candidates (the entire reject list)

| word | source page(s) | dict hits (MW/PW/VCP) | vidyut vote | tier | reading |
|---|---|---|---|---|---|
| kamal | kale_Page_068 | — | compound-split ka+mal | B | §88 base `kamal` — citation form of **kamala** (in sanhw1+MW); split evidence is a false parse of a real word. Review: citation-form normalization, not a defect. |
| sarvak | kale_Page_070 | — | compound-split sarv+ak | B | §90 consonant-base illustration `sarvak`. Likely deliberate final-k declension example. |
| mahatat | kale_Page_085 | — | compound-split mahat+at | B | `mahat+at` illustration — not a lexicon word; example metalanguage. |
| puzan | kale_Page_089 | — | compound-split puz+an | B | पूषन् pūṣán — genuinely absent from sanhw1+MW/PW/VCP headwords and the vidyut stem list; the strongest possible dictionary-gap candidate of this run. |
| Iyas | kale_Page_095, kale_Page_125 | — | unparsed | C | §125/ comparative-suffix examples `Iyas`/`yas` — suffix metalanguage, not lexicon words. |
| viSvarAw | kale_Page_074 | — | unparsed | C | viśvarāṭ-style form; unparsed+unattested — needs eyes. |

Machine verdict rows: `review-candidates.tsv` / `.csv` (identical, dual export);
`review-payload.json` carries the same rows in the `combined_review.html` payload schema
(`{w, s, tier, score, dets, dicts, reason}`, `:y`/`:n` export standard) — drop-in for the
existing review flow. Two-pass κ annotation is a follow-up handoff; the file layout is
designed for it.

## Spot-check (27 of 139 examples, by eye against source lines)

Each sampled word was grepped back into `csl-kale/disp/files1/kale*.txt` and confirmed to
appear verbatim inside `<span class="san">…</span>` on exactly the page the audit
recorded: `rAma jYAna gopA hari mati Denu vAri Suci strI pitf DAtf kamal nadI asmad
yuzmad tad kim svaBU saKi se glO arDasamavftta avayAj asmat Iyas aH AH` — **27/27 pass**.
The `aH`/`AH` cases are sandhi-rule sides (§47–48 `aH → o`); both rule sides enter the
pool — see known limitations.

## Known limitations (documented, not hidden)

1. **Compound-split false evidence**: the proven-split vote fires on arbitrary stem-pair
   bisections of unattested words (`kamal → ka+mal` is linguistically wrong). Tiering
   keeps these at B (review, never auto-verdict), but a future walker (bashspell
   full-parse lane) should replace bisection with rule-attributed parses.
2. **Citation-form class**: grammar books cite bases (`kamal`) whose lexicon form differs
   (`kamala`); a stem-equivalence layer (bashspell lesson 1) would separate this class
   from true gaps.
3. Rule-side spans (`aH`, `AH`) enter the pool — extraction is span-driven, not
   semantics-driven; recorded honestly as candidates.
4. Register/period tags: the source states none in these files; the tag column exists and
   fires on Vedic/Classical/epic mentions (0 hits this run).
5. `detectors/vidyut_stems.txt` is currently **untracked** in the main tree (generated
   artifact); its SHA-256 is recorded in scan.json for reproducibility. Committing the
   vendored stems (like `dcs_lemma_summary.json`) is a recommended follow-up.

## Reproduce

```
python tools/audit_grammar_examples.py \
  --vidyut-stems detectors/vidyut_stems.txt
# -> reports/grammar-examples-audit-2026-09-05/
python -m unittest discover -s tests    # 24 tests green (46 with pytest, whole repo)
```

_Dr. Mārcis Gasūns_
