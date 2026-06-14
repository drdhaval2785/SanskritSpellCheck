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
