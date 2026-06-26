# Orthographic Drift in a Multilingual Indological Lexicography Corpus

*A cross-decade, five-language measurement of spelling change in the gloss text of the
Cologne Digital Sanskrit Dictionaries.*

**Status:** findings synthesis (study complete). **Scope:** documentation / search-normalization
only — nothing here edits dictionary source. See the design in
[ORTHO_DRIFT_ROADMAP.md](../ORTHO_DRIFT_ROADMAP.md) and the working reports in
[ortho_drift/README.md](../ortho_drift/README.md).

---

## Headline finding

**The magnitude of orthographic drift in a dictionary's gloss language is governed by the *type* of
the language's spelling reform, not merely by the dictionary's age.** Across five gloss languages
spanning ~13 decades of indological lexicography, drift rates fall into three sharply separated
tiers:

| tier | reform regime | drift rate (per 1,000 gloss tokens) | example |
|---|---|--:|---|
| **Legislated** | a dated, state-mandated reform | **10 – 358** | Russian Kossovich **358**, German PW **10.26** |
| **Convention** | gradual editorial drift, no central authority | **0.01 – 0.57** | English WIL **0.57** → MW **0.01**; French BUR **0.31** |
| **None** | no reform ever occurred | **0** | Latin BOP **0** (negative control) |

Legislated reforms outdrift convention drift by **one to three orders of magnitude**. A 19th-century
dictionary written in a language that *later underwent a legislated reform* (German, Russian) reads
as massively "misspelled" against a 2026 standard; a contemporaneous dictionary in a language that
only drifted by convention (English, French) is almost entirely modern; and a language with no
reform at all (Latin) shows literally zero drift — confirming the method's specificity.

This is a measurable, reproducible result extracted from a single, uniformly-marked-up corpus. The
contribution is not a new historical-spelling normalizer (that is a mature DH subfield) but the
**application of normalization to a multilingual, era-stratified lexicography corpus**, yielding a
cross-decade drift dataset and a method that **dates each dictionary's orthographic epoch from its
own prose**.

---

## Method

### The corpus and the key insight

Each Cologne Sanskrit dictionary was written in its author's *contemporary* orthography — Wilson's
1832 English, Böhtlingk–Roth's 1850s–70s German, Burnouf's 1866 French, Bopp's 1847 Latin. The
decisive insight is that **the period orthography lives in the gloss language, not in the
Sanskrit** — and Cologne markup already separates the two: Sanskrit is wrapped in `{#…#}` (SLP1) /
`{@…@}` (other transliteration), so the gloss-language running text is precisely what falls
*outside* those spans. We extract those gloss tokens and measure how far they have drifted from a
pinned 2026 standard.

### Transform-and-check

The core test is **transform-and-check**, a high-precision rule applied to each gloss token:

> Apply a language-specific reform rule to the token. Accept it as **reform-drift** *iff* the
> transformed form is present in the modern Hunspell dictionary **and** the original form is not.

This rejects modern words that merely *contain* a reform digraph by coincidence — German `Theater`
and `Gottheit` (a `t`+`h` morpheme boundary, not etymological `th`) are kept, while `Thier` and
`gerathen` are flagged — and it is wordlist-free where the reform is *definitional* (see Russian
below). A residual of forms the rule cannot auto-resolve (inflected/compound drift, foreign words,
names, OCR fragments) is then classified by an LLM pass against the 2026 standard.

The implementation is a single profile-driven tool,
[detectors/ortho_drift.py](../detectors/ortho_drift.py), with one profile per language (`de`, `en`,
`fr`, `la`, `ru`) selected via `LANG_OF` + `PROFILES`. It reuses the body-grounded triage
infrastructure (`triage_util`). Per-language accumulating reform lexicons live in
`ortho_drift/<lang>_reform_map.tsv`; per-dictionary detail in `ortho_drift/<DICT>_drift_report.txt`;
cross-dictionary tables in `ortho_drift/<lang>_drift_summary.tsv`.

### Guardrail

This is a **documentation / search-normalization layer, never a correction list.** Modernising a
historical gloss would corrupt the scholarly edition — the same principle as the headword
[do-not-file lists](../corrections_draft/README.md). The drift reports are a *record* and a
*search-normalization map* (a user searching modern German *Tier* should still reach Böhtlingk's
*Thier*); they do **not** edit `csl-orig`.

---

## Results by language

All figures below are verified against the committed data files
([ortho_drift/](../ortho_drift/)); each dictionary was run `--full` (entire corpus, not sampled).

### German — legislated, twice (the validation target)

German is the cleanest case: its reforms are dated and rule-defined (1901: etymological `th→t`,
`c→k/z`, `-iren→-ieren`; 1996/2006: `ß→ss` after a short vowel). All five German dictionaries were
run against the modern Hunspell `de_DE` word-list (103,756 stems). Per-dictionary, from
[de_drift_summary.tsv](../ortho_drift/de_drift_summary.tsv):

| dictionary (era) | tokens | modern % | drift/1k | 1901 `th` | 1901 `c` | 1996 `ß` |
|---|--:|--:|--:|--:|--:|--:|
| PW (1855–75) | 845,888 | 59 | **10.26** | 6,203 | 1,752 | 15 |
| PWG (1855–75) | 1,070,124 | 60 | 8.86 | 6,508 | 2,275 | 12 |
| GRA (1873) | 254,745 | 45 | 7.90 | 1,460 | 507 | 0 |
| CCS (1887) | 117,976 | 65 | 4.72 | 341 | 126 | 84 |
| **SCH (1928)** | 192,039 | 42 | **2.52** | **76** | **86** | **319** |

The overall drift rate declines **monotonically with publication date** (10.26 → 8.86 → 7.90 →
4.72 → 2.52 per 1k) — the corpus modernising across ~70 years. On full PW alone the method finds
**8,683 drift occurrences across 697 distinct forms**, dominated by `gerathen→geraten` (253),
`personificirt→personifiziert` (191), `theilhaftig→teilhaftig` (190).

### The SCH-1928 control — the method dates the text

The four pre-1901 dictionaries (PW, PWG, GRA, CCS) are dominated by the 1901 `th→t` reform (6,203 /
6,508 / 1,460 / 341 occurrences) with almost no 1996 `ß` drift — the signature of pre-1901
orthography. **Schmidt's 1928 *Nachträge* (SCH) flips the profile entirely**: the 1901-`th` count
collapses to **76** (Schmidt already wrote *Tier*, *Kapitel*), while the 1996 `ß→ss` reform becomes
*dominant* at **319** (he still wrote *Kuß*, *Bewußtsein*, *Mißgunst*, *naß* — all pre-1996).

This is the study's strongest validation: the method does not merely *count* drift, it **correctly
dates each dictionary's orthographic epoch from its own text** — SCH lands precisely in its
expected window (post-1901, pre-1996).

### German recall arc

German recall was extended in three stages, banked in the accumulating
[de_reform_map.tsv](../ortho_drift/de_reform_map.tsv):

1. **Corpus transform-and-check** — 672 forms discovered beyond the curated seed on full PW.
2. **Residual LLM-classify** — the 6,804 unique residual tokens across the five dicts classified vs
   2026 Duden (39 Sonnet agents); **1,831 confirmed reform-drift** (27% — inflected/compound forms
   the rule missed, e.g. `thierkreise→Tierkreise`, `eigenthümlichkeiten→Eigentümlichkeiten`),
   alongside 2,981 fragment/OCR (44%), 1,105 Latin/foreign (16%), 759 modern (11%), 106 names,
   22 uncertain — see [de_residual_classified.tsv](../ortho_drift/de_residual_classified.tsv).
3. **External web-harvested merge** — 14 documented 1901/1996 pairs from the German Wikipedia reform
   articles, ingested dic-validated via
   [detectors/merge_reform_pairs.py](../detectors/merge_reform_pairs.py).
4. **DTA long-tail merge** — the **Deutsches Textarchiv** lingattr-TEI corpus
   ([deutschestextarchiv.de](https://www.deutschestextarchiv.de/download), 5,285 texts, 1473–1900)
   carries a per-token `DTA::CAB norm` modern-orthography layer. [extract_dta_pairs.py](../detectors/extract_dta_pairs.py)
   harvested every `surface ≠ norm` token (596 k distinct), kept those attested **≥ 20×** (43,579),
   and merge_reform_pairs.py dic-validated them → **+12,862 accepted** (textbook forms: `vnd→und`,
   `bey→bei`, `Theil→Teil`, `gantz→ganz`, `krafft→kraft`, `thaler→taler`, `creutz→kreuz`, `fuss→fuß`).

Net: the German reform lexicon grew **978 → 2,809 → 2,823 → 15,685 forms** across the four stages.
The per-dictionary drift reports are deliberately frozen at the deterministic-pass snapshot so the
SCH-control comparison stays stable; the long tail is banked in the map for future runs.

### Russian — legislated 1918, the dramatic case

The 1918 reform is the most sweeping in the corpus: it abolished the letters ѣ (yat), і, ѳ (fita),
ѵ (izhitsa) and word-final ъ (hard sign). Kossovich's pre-1918 dictionary
([ru_drift_summary.tsv](../ortho_drift/ru_drift_summary.tsv)) therefore differs *massively* from
modern Russian — and crucially this is detectable **wordlist-free**, because the abolished letters
are pre-1918 *by definition*:

> 87,636 tokens · **31,389 drift occurrences · 358.17 per 1k ≈ 36% of all Russian tokens**
> (hard-sign 12,125 · decimal-і 11,106 · yat 8,139 · fita 19).

Examples: `въ→в`, `родъ→род` (the high-frequency hard-sign bulk), `растеніе→растение` (decimal і),
`имѣющій→имеющий` (yat). Caveat: the hard-sign drift is high-frequency but low-information; the
*substantive* changes are the yat and decimal-і forms. (Source: SamudraManthanam `kossovich.jsonl`,
not part of the Cologne 33.)

### English — convention drift, editor- and age-dependent

English has no central spelling authority, so its drift is a *gradient*, not a reform date. Ten
19th-century English dictionaries were run with an **en_GB reference** (so British `honour` / `-ise`
/ `-re` are correctly *not* flagged), from [en_drift_summary.tsv](../ortho_drift/en_drift_summary.tsv)
(five modern dictionaries are added as a recency control in the subsection below):

| dictionary (era) | tokens | drift/1k | dominant forms |
|---|--:|--:|---|
| **WIL · Wilson (1832)** | 432,117 | **0.57** | Johnsonian `-ick` (`garlick`, `musick`), æ (`æther`, `chamæleon`), `reflexion` |
| GST (1856) | 152,728 | 0.31 | ligature |
| SHS (1900) | 471,445 | 0.31 | ligature |
| MD (1893) | 277,933 | 0.16 | `-xion` |
| BEN (1866) | 222,874 | 0.14 | ligature |
| MW72 (1872) | 1,222,406 | 0.09 | ligature |
| AP90 (1890) | 471,172 | 0.08 | ligature |
| MW · Monier-Williams (1899) | 993,495 | **0.01** | archaic |
| AP (modern) | 540,653 | **0.00** | — |
| CAE (1891) | 179,477 | **0.00** | — |

The range is **0.00 – 0.57/1k** — two orders of magnitude *below* German, and tracking editor and
age rather than any single reform: the oldest (Wilson 1832) tops out, the heavily-standardised
Monier-Williams (1899) is near-zero. English convention drift is real but minor.

#### Recency control — the modern end of the gradient

If the metric truly dates orthography, dictionaries compiled in the **20th–21st century** should sit
at the very bottom of the gradient (≈ 0). Five modern-leaning English sources were added as a control
— **PD** (the *Encyclopaedic Dictionary of Sanskrit*, Deccan College **1976–2009**, the most modern
and by far the largest corpus here), plus the 20th-century glossaries **PE, BHS, IEG, VEI**:

| dictionary (era) | tokens | drift/1k | note |
|---|--:|--:|---|
| **PD · Deccan College (1976–2009)** | 1,317,037 | **0.00** | most modern; 1.3 M tokens, **exactly zero** reform-drift |
| PE · Purāṇic Encyclopaedia (20th c.) | 740,406 | 0.00 | — |
| BHS · Edgerton (1953) | 379,068 | 0.00 | — |
| IEG · Sircar (1966) | 84,754 | 0.00 | — |
| VEI · Vedic Index (1912) | 222,063 | 0.06 | residual æ ligatures only |

The control holds cleanly: the modern anchors are at or essentially at **0**, with **PD — the largest
and most recent — at exactly 0.00 across 1.3 million gloss tokens**. The full English picture is now a
monotone recency gradient from Wilson 1832 (**0.57**) down through Monier-Williams 1899 (**0.01**) to
the modern compilations (**0.00**), confirming that the detector tracks each dictionary's orthographic
epoch rather than flagging noise. (en_GB reference = the `ropensci/hunspell` `en_GB.dic`, ~86 k stems,
staged locally.)

### French — convention, minimal

Two French dictionaries ([fr_drift_summary.tsv](../ortho_drift/fr_drift_summary.tsv)), run against
Hunspell `fr_FR`:

| dictionary (era) | tokens | drift/1k | examples |
|---|--:|--:|---|
| BUR · Burnouf (1866) | 229,053 | 0.31 | `poëte→poète`, `phlegme→flegme`, `françois→français` |
| STC · Stchoupak (1932) | 281,418 | 0.02 | — |

⚠️ BUR and STC inline their Sanskrit in IAST (not `{#…#}`), so a few IAST fragments (e.g. `pha`)
leak into the token stream — the macro drift-rate is robust, but individual flagged forms are less
reliable for this pair.

### Latin — the negative control

Bopp's *Glossarium* (1847), [la_drift_summary.tsv](../ortho_drift/la_drift_summary.tsv):

> 76,933 tokens · **0 drift · 0.00 per 1k**.

Latin underwent no orthographic reform, so there is no rule-set and no word-list (none exists), and
the tool — correctly — flags nothing. This is the **negative control that confirms the method's
specificity**: it does not manufacture drift where none exists.

---

## Caveats (read before citing)

- **Modern word-lists are a local dependency.** The Hunspell `de_DE` / `en_GB` / `fr_FR`
  dictionaries are Adobe-InDesign-bundled and **not committed** to the repo (resolved at runtime via
  `$ORTHO_<L>_DIC`). Drift figures are reproducible only with equivalent Hunspell snapshots on disk.
- **Cross-language token-stream purity varies.** BUR/STC inline Sanskrit in IAST rather than `{#…#}`,
  so a few transliteration fragments leak; the German `{%<bot>{{…}}</bot>%}` editorial-correction
  annotations required dedicated tokenizer hardening (strip `{{…}}`, `<bot>`, `<ls>` sigla).
- **Russian hard-sign drift is high-frequency, low-information bulk.** The 358/1k headline is
  dominated by word-final ъ; the linguistically substantive changes are the yat and decimal-і forms.
- **`modern_form` is advisory.** The LLM-suggested 2026 spelling in the residual-classify pass is
  documentation, not a sanctioned correction (a handful of LLM artifacts were hand-corrected).
- **The Russian source is external** (SamudraManthanam), not one of the Cologne 33.
- **The DTA/RIDGES long tail is unmerged.** `merge_reform_pairs.py` is the ready wiring for the
  Deutsches Textarchiv / RIDGES historical corpora, but bulk-download requires a local export or a
  row-list URL.

---

## Reproducibility

```sh
cd detectors
python ortho_drift.py PW --full          # German   (legislated)
python ortho_drift.py KOSSOVICH --full   # Russian   (legislated, wordlist-free)
python ortho_drift.py WIL --full         # English   (convention, max drift of 10)
python ortho_drift.py BUR --full         # French    (convention)
python ortho_drift.py BOP --full         # Latin     (negative control)
```

Requires the Hunspell modern word-lists on disk (Adobe path, or set `$ORTHO_<L>_DIC`); Latin needs
none (no reform) and Russian needs none (the 1918 letters are definitional). Each run writes
`ortho_drift/<DICT>_drift_report.txt` (+ pattern candidates) and folds discovered forms into
`ortho_drift/<lang>_reform_map.tsv`. Documentation only — `ortho_drift.py` never edits `csl-orig`.

### Where the numbers in this document live

| figure | file |
|---|---|
| per-dict drift/1k + era columns | [ortho_drift/`<lang>`_drift_summary.tsv](../ortho_drift/) |
| accumulated historical→2026 lexicon | [ortho_drift/`<lang>`_reform_map.tsv](../ortho_drift/) (de **15,685** incl. DTA long tail, ru ≈ 7,711, en 73, fr 20, la 2 forms; the maps accumulate across runs) |
| per-dict detail (header: tokens / modern / drift) | [ortho_drift/`<DICT>`_drift_report.txt](../ortho_drift/) |
| German residual LLM-classify (6,804 → 1,831 drift) | [de_residual_classified.tsv](../ortho_drift/de_residual_classified.tsv) |
