# detectors/ — additional Sanskrit spell-check algorithms

Six detectors that target error classes the original three tools (faultfinder,
o_vs_O, ngram) miss. They were designed from the **real** error distribution: the
[o_vs_O](../o_vs_O/o_vs_O2.txt) confusion pairs (vowel-length **75%**, aspiration
13%, sibilant 8%, diphthong 4%) and the
[CORRECTIONS](https://github.com/sanskrit-lexicon/CORRECTIONS/issues) history
(v↔b, ṛ↔ri, encoding, duplicates, misordering, anti-sandhi).

Key gap they close: the dominant errors are **skeleton-preserving substitutions**
(a↔A, k↔K, s↔S), to which faultfinder is structurally blind, and which o_vs_O only
catches when the correct variant already exists in another dictionary.

[slp1util.py](slp1util.py) is the shared module: the SLP1 alphabet, the confusion
model (`confusion_key` folds 99.2% of real confusion pairs to one key; `confusion_sub`
tests a single confusion substitution; `confusion_candidates` generates correction
neighbours), `sanskrit_sort_key`, `edit_distance`, and the lexicon/corpus/DCS/whitelist
loaders. Devanagari→SLP1 transliteration is **delegated to the shared `sanskrit-util`
package** (via [sanskrit_util.py](sanskrit_util.py), a relative-path shim) rather than
re-implemented — single source of truth. (The SLP1 alphabet/char classes stay local;
`sanskrit-util` does not expose them.)

### Corpus grounding (DCS)

Four detectors use the **DCS corpus** as ground truth via the vendored
[`dcs_lemma_summary.json`](dcs_lemma_summary.json) — 83,239 SLP1 lemmas with frequency
bands 1–5 (1 = hapax … 5 = ≥1000 occurrences). It is used two ways:

- **suppress** — a headword that is itself an attested DCS lemma is a real word, so
  `spell_correct`/`consensus`/`intra_dup` skip it (a large false-positive cut: ~4000
  for spell_correct, ~1400 each for consensus/intra_dup).
- **rank/flag** — `spell_correct` orders suggestions by the suggested lemma's band
  (very-common corrections first); `dict_vs_corpus` uses DCS as an external oracle.

Headwords are normalized to the DCS join key with `normalize_lemma()` (strip accents
`/ \ ^ ~` and trailing homonym digits; SLP1 case preserved), per the VisualDCS
consumption contract.

> **Attribution.** `dcs_lemma_summary.json` is a frequency-banded derivative of the
> **Digital Corpus of Sanskrit** (DCS-2021, © Oliver Hellwig, **CC BY**), produced by
> [VisualDCS](https://github.com/gasyoun/VisualDCS) and vendored here read-only (bands
> only, no passages/counts) as an optional enrichment.

| # | script | catches | result on sanhw1 | output |
|---|---|---|---|---|
| 1 | [spell_correct.py](spell_correct.py) | misspelling whose confusion-neighbour is a trusted (MW/PW/VCP) headword; **DCS-ranked**, DCS-attested headwords suppressed | 9173 (4001 suppressed; 704 → common DCS lemma) | `DICT:wrong:right:n` |
| 2 | [consensus.py](consensus.py) | minority spelling vs the N-way cross-dict consensus (DCS-attested minorities suppressed) | 7548 | `DICT:wrong:right:n` |
| 3 | [intra_dup.py](intra_dup.py) | one dict holding both a word and a rare confusion-variant of it (DCS-attested variants suppressed) | 8945 | `DICT:wrong:right:n` |
| 4 | [dict_vs_corpus.py](dict_vs_corpus.py) | **collective** dict errors: a form all dicts agree on but the DCS corpus contradicts (lowest precision) | 1350 (646 in ≥5 dicts) | `DICT:wrong:right:n` |
| 5 | [phonotactic_check.py](phonotactic_check.py) | hard phonotactic violations (anusvara/visarga mis-placed, double vowel) | 60 (0 false positives) | `X:PH-<rule>=…:D` |
| 6 | [charset_check.py](charset_check.py) | non-SLP1 characters (encoding errors) | 28 | `X:CHS=…:D` |
| 7 | [order_check.py](order_check.py) | headwords out of Sanskrit collation order | n/a (needs source-order input) | `X:ORD=…:line` |
| 8 | [tied_field_check.py](tied_field_check.py) | tied-field cross-encoding consistency: SLP1↔Devanāgarī↔IAST round-trip disagreement | 0 (of 431,568 unique headwords — see [docs/HYPOTHESES.md](../docs/HYPOTHESES.md) H8) | `X:TFC-DEV=…:D` / `X:TFC-IAST=…:D` |

`tied_field_check` is the **11th detector family** counting the standalone scripts in this table
alongside `meter_check` ([detectors/meter/](meter/)), `body_xref_check` (cross-reference integrity,
below) and `ortho_drift` (gloss-language drift, below) as separate families beside the original six —
see H827/H8 for why it currently reports 0 (the sanhw1.txt data model has no independently-authored
Devanāgarī/IAST field to disagree with the SLP1 it derives from; the check is real and correctly
discriminates two documented, non-error round-trip asymmetries — candrabindu/avagraha via Devanāgarī,
and the aspirate/diphthong digraph ambiguity via IAST — from a genuine defect, it just found none).

## Unified runner & review (start here)

[run_all.py](run_all.py) runs every detector, **deduplicates across them** by suspect
headword, scores each candidate, and assigns an **A/B/C tier** — cross-detector
agreement is the main signal (a word flagged by several detectors is far more likely a
real error). It emits:

- `combined_candidates.txt` — full ranked list (tier, score, suspect → suggestion, evidence)
- `combined_review.html` — accept/reject UI: per-row scan links, ✓/✗ buttons (keys
  a/r/s), decisions persisted to `localStorage`, and **Export accepted / rejected** →
  the `DICT:wrong:right:y|n` standard format for [chg_nchg_sep.py](../chg_nchg_sep.py)
- `combined_sf.txt` — standard format for the best suggestion per suspect

```sh
cd detectors && python run_all.py        # uses cached detector outputs; --rerun to regenerate
```

On `sanhw1`: **17,098** deduped candidates, **7,618** flagged by ≥2 detectors; tiers
A/B/C ≈ 7.7k / 4.7k / 4.7k. Tier A (e.g. `brahmaRa→brAhmaRa`, `jiv→jIv`, `zas→zaz`) is
flagged by several detectors at once — the verify-first queue. Outputs are gitignored
(regenerable); the review HTML shows the top 1500 by score (full list in the .txt).

## Evaluation & raw-source runs (Phase 1.4–1.6)

- [extract_csl_hw.py](extract_csl_hw.py) — pull headwords in **source order** from a
  raw csl-orig dictionary (`<k1>`/`<k2>` fields) so charset/phonotactic/**order_check**
  can run on the raw text, not just the cleaned `sanhw1.txt`:
  ```sh
  python extract_csl_hw.py ../../csl-orig/v02/ap90/ap90.txt ap90_hw.txt
  python order_check.py ap90_hw.txt ap90_order.txt   # real source-order check
  ```
  *Caveat:* order_check measures deviation from **sanhw's** collation (anusvara sorts
  as the homorganic nasal); a dictionary using a different anusvara convention shows
  many non-error deviations — verify against that dict's own ordering.
- [eval.py](eval.py) — measures the suite against local ground truth:
  - **recall** vs the 3884 historical o_vs_O pairs: union **50.6%** (spell_correct
    44.6%, consensus 25%), plus **15,152 new** candidate pairs beyond the 2017 method;
  - **false positives**: **0** against 29.5k known-good (`nochange`) words;
  - tiers of recovered known pairs: A=809 / B=245 / **C=913** (tier C still holds real
    corrections — don't discard it);
  - writes `spotcheck_sample.txt` (top-100 tier-A) for human precision verification
    (true precision needs eyes on the scans).

## Submission & tuning (Phase 2, in progress)

- [gen_confusion_weights.py](gen_confusion_weights.py) — derive empirical single-char
  confusion weights from the 3884 o_vs_O pairs → [confusion_weights.json](confusion_weights.json)
  (a/A 41%, i/I 24%, u/U 9%, s/S 8% …); `run_all` uses them to rank common confusions
  higher.
- [run_campaign.py](run_campaign.py) — **per-dictionary campaigns**: splits the
  unified suite per dictionary into `campaigns/<DICT>/{review.html,candidates.txt}` so
  you can work one dictionary's queue at a time, plus `campaigns/campaign_summary.txt`,
  a dashboard ranking dicts by tier-A count (MW 1977, PD 1045, BHS 737, SCH 678,
  PW 657 …) — campaign the biggest high-confidence queues first.
- [ocr_verify.py](ocr_verify.py) — **OCR-assisted pre-verification** (triage prior, not
  a verdict): for a candidate, resolve the Cologne `servepdf` page → fetch the scan PDF
  → text layer or OCR → compare the print to the suspect vs the suggested spelling →
  pre-label CONFIRM / DENY / UNCERTAIN, reordering the human queue. Fetch+render and the
  closest-match decision (+ Devanagari→SLP1 in slp1util) are verified here; the OCR step
  needs **tesseract + a Devanagari model** (`san`/`hin`) — without it the page image is
  cached as a review aid and the label is MANUAL. Polite by design (cached,
  rate-limited, 429 backoff) — run small batches, ideally server-side where the scans
  live. OCR of old Devanagari scans is unreliable, so a human always confirms.
- [gen_vidyut_stems.py](gen_vidyut_stems.py) → `vidyut_stems.txt` — **morphology gate**
  (Phase 3.2): the 205k vidyut pratipadika (stem) inventory. `run_all` tags `morph✓`
  when a correction's suggestion is a valid vidyut stem the suspect isn't (a
  grammatical-validity signal) and nudges its rank. **Honest caveat:** weak on
  dictionary headwords — only ~6.6% are pratipadikas (most are compounds / proper
  names / Vedic), and an inflected suspect (e.g. `rAjA`) looks "not a stem", so morph
  is a ranking nudge + informational tag, **not** a tier promoter. Regenerate where
  vidyut is installed (`gen_vidyut_stems.py`); the tag is simply off if the file is
  absent. Stems from vidyut (Arun Prasad / ambuda-org, MIT).
- [make_changefiles.py](make_changefiles.py) — turn accepted corrections
  (`accepted_sf.txt` exported from the review UI) into per-dictionary **draft**
  change-files in the CORRECTIONS updateByLine format: locates the source line in
  csl-orig and proposes the `<k1>`/`<k2>` edit. **Prep only** — never edits dictionary
  source or files an issue; verify each `new` line against the scan before submitting.
- Blocked locally: OCR-assisted verification (needs tesseract + scan fetch), full DCS
  via `dcs_full.sqlite` (the local copy is an empty placeholder — detectors use the
  vendored banded summary), and GRETIL corpus expansion (external download).

## Body-grounded triage & ortho-drift (separate pipelines in this dir)

Two larger pipelines also live here; they consume the detector output but have their own docs:

- **Body-grounded triage** — `triage_dict.py` / `triage_*.py` / `triage_util.py` /
  `triage_lang.py` + `bodyaware_workflow.js`, driven by the **`/dict-triage <DICT>`** skill. Judges
  each tier-A candidate against the dictionary's *own entry text* → a FILE-FIRST queue + a do-not-file
  list. **Done for all 33 dicts** — index + results in
  [../corrections_draft/README.md](../corrections_draft/README.md);
  `gen_do_not_file_suppress.py` folds the do-not-file lists into the detector suppression layer.
  Dictionaries not in `csl-orig` (e.g. **PD**) are staged with
  [get_external_source.py](get_external_source.py) into `external_src/` and resolved by
  `triage_util.source_file()`.
- **Ortho-drift study** — [ortho_drift.py](ortho_drift.py) + `merge_reform_pairs.py`. Checks
  gloss-language tokens (de/en/fr/la/ru) against a 2026 standard to document spelling drift; **complete
  across all 5 languages** — see [../docs/ORTHO_DRIFT_FINDINGS.md](../docs/ORTHO_DRIFT_FINDINGS.md).

## Output formats (reuse the existing pipeline)
- **Flaggers** (5, 6, 7, 8) emit faultfinder-style `X:CODE=detail:D`, so
  [../faultfinder3a-html.php](../faultfinder3a-html.php) (with the `repeat=2` arg)
  and [../triage_suspects.py](../triage_suspects.py) can render/triage them.
- **Correctors** (1, 2, 3, 4) emit the CORRECTIONS standard format `DICT:wrong:right:n`
  (issue #154), ready for [../chg_nchg_sep.py](../chg_nchg_sep.py) and submission.

## Run
```sh
cd detectors
python charset_check.py        # ../sanhw1.txt -> charset_suspects.txt
python phonotactic_check.py    # ../sanhw1.txt -> phonotactic_suspects.txt
python tied_field_check.py     # ../sanhw1.txt -> tied_field_suspects.txt
python consensus.py            # -> consensus_corrections.txt
python intra_dup.py            # -> intra_dup_corrections.txt
python spell_correct.py        # -> spell_correct_corrections.txt   (loads MW/PW/VCP + corpus)
python order_check.py --selftest
python order_check.py <dict_source_order.txt>   # real misordering check (input from csl-orig)
```
Outputs are gitignored (regenerable). Every result is a **candidate** for the
human + scan verification step, not an automatic fix — post-repha and gender/variant
forms in particular need eyes on the print.

## Precision gates / tuning knobs
- `consensus.py` / `intra_dup.py`: `MINORITY_MAX` (how rare the variant must be) and
  `MARGIN` (attestation gap) — the rarity gate is what keeps distinct real words
  (anu/aRu, pAda/pada) out of the results.
- `spell_correct.py`: trusted lexicon = MW+PW+VCP; corpus = CountVowels texts.
- All detectors skip [../nochange/nochange.txt](../nochange/nochange.txt) whitelisted words.

## How each detector works (algorithm + rationale)

**spell_correct — noisy-channel correction.** For every headword *not* in the
trusted lexicon (MW ∪ PW ∪ VCP stems), generate confusion-neighbours — one
`CONFUSION_PAIRS` substitution at each position, plus the two-character `f`↔`ri`/`ru`
vocalic-r variant — and keep any neighbour that *is* a trusted headword. Rank by
the suggestion's DCS frequency band (very-common corrections first); a headword that
is itself a DCS lemma is suppressed as a real word.
*Why:* the big scholarly dictionaries are curated ground truth and DCS frequency tells
you which correction is the common, expected word, so this
catches a spelling that is wrong across several minor dictionaries at once — which
vote-based consensus would miss. The `f`↔`ri` op is the only multi-character rule;
it expresses the `SfNg`/`SriNg` class that a same-length substitution cannot.

**consensus — N-way voting.** Group all headwords by `confusion_key` (so confusable
spellings share a bucket), take the spelling in the most dictionaries as the
consensus, and flag a near-variant that differs by exactly one `confusion_sub`, sits
in ≤ `MINORITY_MAX` dictionaries, and trails the consensus by ≥ `MARGIN`.
*Why:* `confusion_key` makes candidate grouping O(n) instead of O(n²); but it
over-merges distinct words (`ata`/`aTa`) and would treat a trailing case ending
(`aNgaH`/`aNga`) as a typo — so `confusion_sub` (one *same-length* confusion
substitution) plus the rarity/margin gates restore precision.

**intra_dup — self-contradiction.** Same grouping as consensus, but flag the rare
variant only in the dictionaries that *also* contain the consensus spelling
(set intersection non-empty). *Why:* if one dictionary holds both `kapila` and a rare
`kaPila`, it already attests the right form, so its near-variant is almost certainly
an internal typo — the highest-precision corrector, and it names the dictionary to fix.

**dict_vs_corpus — collective error detection.** For a headword absent from the DCS
lemma set (in ≥ `MIN_DICTS` dictionaries), if a confusion-neighbour is a DCS lemma of
band ≥ `MIN_BAND`, flag it; rank by dictionary count then band. *Why:* this is the
only detector that can catch an error the dictionaries make *unanimously* — there is
no cross-dict disagreement to exploit, so an external corpus is the only witness.
*Lowest precision by design* (DCS-absence is a weak signal): the output mixes genuine
collective errors with distinct real word-pairs (`guha`/`guhA`), ī/i citation
differences (`sUcI`/`sUci`), and rare lexicon DCS omits — treat it as a ranked
exploration list, not a correction feed.

**phonotactic — absolute rules.** Per-character checks: anusvara/visarga/candrabindu
must sit on a vowel; an anusvara may not precede a vowel; identical vowels may not be
adjacent. *Why:* the statistical faultfinder only knows "absent from a base"; these
rules catch forms that are *impossible* even when they appear in the base dictionary.
Only near-certain rules are used, so the false-positive rate is ~0.

**charset — structural validity.** Flag any character outside the SLP1 alphabet and
categorise it (Latin-diacritic, Greek, Devanāgarī, digit, whitespace, danda).
*Why:* nothing else validates the character set; it needs no base dictionary and can
run on raw dictionary text before it ever reaches `sanhw1.txt`.

**order_check — collation.** Walk a *source-order* headword list and flag any pair
where `sanskrit_sort_key(cur) < sanskrit_sort_key(prev)`. The key mirrors `sanhw1.py`
(SLP1 sort alphabet + anusvara-before-varga sorting as the homorganic nasal), verified
by reporting 0 violations on the 431 k already-sorted `sanhw1` headwords.

**tied_field_check — cross-encoding consistency.** Round-trips every SLP1 headword through
Devanāgarī (`slp1_to_devanagari` → `devanagari_to_slp1`) and IAST (`slp1_to_iast` → `iast_to_slp1`,
all via the shared `sanskrit-util` package); a headword that does not return unchanged is flagged,
*unless* the mismatch is fully explained by one of two documented transcoder asymmetries (candrabindu
`~`/avagraha `'` not round-trip stable via Devanāgarī; plain-stop+`h`/vowel-hiatus reading back as an
aspirate/diphthong via IAST — both are properties of the transliteration schemes themselves, not
errors). *Why:* this is the "tied-field consistency" detector shape from Bloodgood & Strauss (arXiv
1602.07807) the project lacked — it checks that fields *expected* to agree actually do, distinct from
every other detector here (which compare a headword against other headwords or a corpus). See H8 in
[docs/HYPOTHESES.md](../docs/HYPOTHESES.md) for why it currently reports 0 real flags.

### Shared design principles
- One confusion model in [slp1util.py](slp1util.py) — no per-detector copies (the
  bug the code-review caught in the original tools).
- `confusion_key` for cheap grouping, `confusion_sub` for precise confirmation:
  group loosely, then verify strictly.
- Rarity + attestation gates over raw similarity — similarity alone flags distinct
  real words.
- Everything is a **candidate** for human + scan verification, never an auto-fix.
