# VCP correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **563 tier-A** VCP (*Vācaspatyam*, a Sanskrit–Sanskrit
thesaurus) headwords as possible misspellings. This package triages them against VCP's
*own Sanskrit entry text* (from
[csl-orig](https://github.com/sanskrit-lexicon/csl-orig)) — a spelling-only detector
cannot tell a typo from a real word, a verbal root, or a deliberate variant cross-reference,
but the entry can.

## The finding

> **Of 563 engine "tier-A" candidates, just 1 is a body-confirmed fileable typo**
> (`camIkara → cAmIkara` "gold"). 153 are real distinct words or **verbal roots** (dhātus);
> **408 are spellings VCP documents on purpose** — chiefly **362 `{{Lbody=…}}` redirects**:
> variant-spelling headwords that VCP deliberately cross-references to the canonical entry
> (e.g. `vrAhmaRa` → the body of `brAhmaRa`). Filing a "correction" for any of those would
> *break VCP's cross-reference web*.

The Vācaspatyam is the clearest case yet that spelling-pattern "tier A" is **not** a list
of typos: it is a Sanskrit thesaurus that (a) systematically lists variant spellings as
redirects and (b) contains thousands of real roots/derivatives that merely *resemble*
commoner words. Across the three dictionaries triaged, fileable-typo precision is tiny —
**MW 4/1954 · PW 2/657 · VCP 1/563** — do **not** bulk-apply tier-A. (The body-aware
TYPO pass is stochastic and low-yield; the durable deliverable is the do-not-file list.)

## The authoritative artifact

- **[VCP_triaged.txt](VCP_triaged.txt)** — the review queue: the 155 REAL-WORD entries (with
  VCP's own derivation/gloss and why each is a distinct word) and the 408 INTENTIONAL ones.
- **[VCP_wrong_readings.txt](VCP_wrong_readings.txt)** — the standing **do-not-file** list:
  408 deliberate spellings (cross-reference/redirect **362**, other 43, `v.l.` 2,
  in-composition 1), grouped by sub-type. Use it as a suppression list so future runs never
  re-flag them.
- **[VCP_file_first_sf.txt](VCP_file_first_sf.txt)** — the 1 body-confirmed candidate
  (`camIkara → cAmIkara`): VCP glosses `camIkara` with gold terms (*kṛtasvara*, *svarṇa*),
  but the word for gold is *cāmīkara* (long ā) — verify on the scan, flip `n`→`y`, file.

## Why every candidate is safe (worked examples)

- **`{{Lbody=N}}` redirects (362)** — `Ajana → ajana`, `AmAtIsAra → AmAtisAra`,
  `vrAhmaRa → brAhmaRa`: the headword's body is *just* `{{Lbody=N}}`, i.e. VCP points it at
  another entry. These are intentional variant cross-references.
- **Verbal roots (dhātu)** — `garba` is the root √garb (`gatO`/`darpe`, with conjugation
  `garbati agarbIt jagarba`), a real word distinct from `garBa` "womb"; likewise `yuza`
  (√yuṣ), `Bila` (√bil), `Guqa` (√guḍ). The dhātu shape (meaning + gaṇa + pada + seṭ +
  conjugation) proves a real root, not a typo of a similar noun.
- **Real derivatives** — `nUtra` "new" (≠ `mUtra` "urine"); `Amanda` "cutter of the
  Āma-disease, epithet of Vāsudeva" (≠ `Ananda`); `DavalA` (fem. of *dhavala* "white").

## Method (pipeline)

```sh
cd detectors
python make_dict_package.py VCP    # extract VCP tier-A from combined_candidates.txt
python triage_enrich.py VCP        # k2 / DCS / cross-dict / confusion evidence
python triage_bodies.py VCP        # attach each VCP entry body + classify (Sanskrit markers via triage_lang.py)
python triage_body_batches.py VCP  # split the 'realword' set
#  -> run the body-aware LLM workflow (Sanskrit rubric: dhatu/abbreviation conventions, {{Lbody}} redirects)
python triage_synthesize.py VCP    # -> VCP_triaged.txt + VCP_wrong_readings.txt
```

The decisive VCP-specific signal is **`{{Lbody=N}}`** (a redirect headword), tuned into the
Sanskrit profile in [detectors/triage_lang.py](../../detectors/triage_lang.py). The LLM
layer (a triage prior, not a verdict) reads VCP's abbreviated Sanskrit — roots, derivations,
gender/POS marks — to separate real words from any misspelled key.

## Raw engine output (provenance — do NOT apply)

- [VCP_candidates.txt](VCP_candidates.txt) — the engine's 563 ranked tier-A candidates.
- [VCP_draft.txt](VCP_draft.txt) — draft updateByLine change-file. **Superseded:** the triage
  finds 0 fileable typos; do not apply it.
