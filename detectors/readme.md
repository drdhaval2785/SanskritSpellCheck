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
tests a single confusion substitution), `sanskrit_sort_key`, `edit_distance`, and the
lexicon/corpus/whitelist loaders.

| # | script | catches | result on sanhw1 | output |
|---|---|---|---|---|
| 1 | [spell_correct.py](spell_correct.py) | misspelling whose confusion-neighbour is a trusted (MW/PW/VCP) headword; ranked by corpus attestation | 9921 (906 corpus-corroborated) | `DICT:wrong:right:n` |
| 2 | [consensus.py](consensus.py) | minority spelling vs the N-way cross-dict consensus | 8918 | `DICT:wrong:right:n` |
| 3 | [intra_dup.py](intra_dup.py) | one dict holding both a word and a rare confusion-variant of it | 10443 | `DICT:wrong:right:n` |
| 4 | [phonotactic_check.py](phonotactic_check.py) | hard phonotactic violations (anusvara/visarga mis-placed, double vowel) | 60 (0 false positives) | `X:PH-<rule>=…:D` |
| 5 | [charset_check.py](charset_check.py) | non-SLP1 characters (encoding errors) | 28 | `X:CHS=…:D` |
| 6 | [order_check.py](order_check.py) | headwords out of Sanskrit collation order | n/a (needs source-order input) | `X:ORD=…:line` |

## Output formats (reuse the existing pipeline)
- **Flaggers** (4, 5, 6) emit faultfinder-style `X:CODE=detail:D`, so
  [../faultfinder3a-html.php](../faultfinder3a-html.php) (with the `repeat=2` arg)
  and [../triage_suspects.py](../triage_suspects.py) can render/triage them.
- **Correctors** (1, 2, 3) emit the CORRECTIONS standard format `DICT:wrong:right:n`
  (issue #154), ready for [../chg_nchg_sep.py](../chg_nchg_sep.py) and submission.

## Run
```sh
cd detectors
python charset_check.py        # ../sanhw1.txt -> charset_suspects.txt
python phonotactic_check.py    # ../sanhw1.txt -> phonotactic_suspects.txt
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
corpus support: the suggestion appears in the SLP1 corpus and the headword does not.
*Why:* the big scholarly dictionaries are curated ground truth and the corpus
(inflected MBh/Rāmāyaṇa/Veda forms) confirms the suggestion is a real word, so this
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

### Shared design principles
- One confusion model in [slp1util.py](slp1util.py) — no per-detector copies (the
  bug the code-review caught in the original tools).
- `confusion_key` for cheap grouping, `confusion_sub` for precise confirmation:
  group loosely, then verify strictly.
- Rarity + attestation gates over raw similarity — similarity alone flags distinct
  real words.
- Everything is a **candidate** for human + scan verification, never an auto-fix.
