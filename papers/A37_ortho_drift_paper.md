---
paper_id: A37
title: "Reading the Reform off the Gloss: Orthographic Drift as a Dater of 19th–20th-Century Indological Dictionaries"
status: draft (skeleton, 2/5) — scaffolded 2026-06-26
readiness: 2/5
venue: "Digital Scholarship in the Humanities (DSH) / International Journal of Lexicography; alt. Journal of Historical Pragmatics"
author: "M. Gasūns (byline to finalise)"
data_source: "docs/ORTHO_DRIFT_FINDINGS.md (study complete; figures verified against ortho_drift/*.tsv)"
---

# Reading the Reform off the Gloss: Orthographic Drift as a Dater of 19th–20th-Century Indological Dictionaries

> **Draft status (2026-06-26).** Manuscript skeleton built directly on the completed
> study in [`docs/ORTHO_DRIFT_FINDINGS.md`](../docs/ORTHO_DRIFT_FINDINGS.md). All
> numerical claims below are transcribed from that synthesis and recompute from the
> committed [`ortho_drift/`](../ortho_drift/) TSVs. **Open before submission:**
> (1) write §2 Related work; (2) finalise byline; (3) state the Hunspell-wordlist
> local-dependency caveat in the data-availability statement. The Russian/Kossovich
> material is folded in as §7 (see note there) — it absorbs the former standalone
> "Kossovich pre-1918 digitization protocol" idea.

## Abstract

Each historical bilingual dictionary is written twice over: once in the headword
language it describes, and once in the *metalanguage* of its glosses, prefaces, and
definitions. We show that the second of these — the gloss prose — carries a datable
orthographic fingerprint, and that the **magnitude and composition of orthographic
drift in the gloss language is governed by the *type* of that language's spelling
reform, not merely by the dictionary's age.** Measuring drift against a pinned 2026
standard across five gloss languages and ~13 decades of the Cologne Digital Sanskrit
Dictionaries, drift rates fall into three sharply separated tiers — **legislated**
reform (Russian 1918 ≈ 358 / 1 000 gloss tokens; German 1901/1996 ≈ 2.5–10), **convention**
drift (English / French ≈ 0–0.46), and **none** (Latin = 0, a negative control) —
separated by one to three orders of magnitude. We further show that the *per-era
composition* of the drift (which reform's forms dominate) dates a dictionary's
orthographic epoch from its own prose more reliably than the scalar rate: Schmidt's
1928 supplement flips from a `th`-dominant (pre-1901) to an `ß`-dominant (pre-1996)
signature, landing it precisely in its true window. The contribution is not a new
historical-spelling normaliser — that is a mature subfield — but the application of
normalisation to a multilingual, era-stratified *lexicographic* corpus, yielding a
reproducible cross-decade drift dataset and a metalanguage-dating method.

## 1. Introduction

Historical lexicography is usually dated by its title page. We ask whether a
dictionary's *text* — specifically its gloss metalanguage — can date itself, and
what governs how strongly it can. The Cologne Digital Sanskrit Dictionaries are an
unusually clean testbed: a single, uniformly marked-up corpus of ~36 dictionaries
whose authors wrote in four European metalanguages across the long 19th century —
Wilson's 1832 English, Böhtlingk–Roth's 1850s–70s German, Burnouf's 1866 French,
Bopp's 1847 Latin — plus 20th-century compilations. Because Cologne markup wraps the
Sanskrit object-language in `{#…#}` / `{@…@}` spans, the European gloss text is
exactly what falls *outside* those spans and can be isolated and measured.

Our claims:

1. **A three-tier law.** Drift magnitude is stratified by reform *regime*
   (legislated ≫ convention ≫ none), not by raw age.
2. **A dating instrument.** Within a regime the rate tracks date coarsely; the
   per-era *composition* dates the orthographic epoch finely and language-internally.
3. **A method, not a corrector.** The output is a documentation / search-normalisation
   layer; it never edits the scholarly source. (This is the same do-not-modify
   principle as the headword do-not-file lists in the host project.)

## 2. Related work  *(TODO — to be written)*

Position against: historical-spelling normalisation in DH (VARD, Norma, the
Deutsches Textarchiv `CAB` layer, FreEMnorm for French); reform historiography
(German 1901/1996; Russian 1918); and metalanguage / definition-language studies in
historical lexicography. The novelty claim is the **application to a multilingual,
era-stratified lexicographic gloss corpus** and the metalanguage-as-dater result —
not a new normaliser.

## 3. Data and method

### 3.1 Corpus and the key insight
The period orthography lives in the gloss language, not in the Sanskrit. Cologne
markup already separates the two, so we extract gloss tokens (outside `{#…#}` /
`{@…@}`) and measure how far they have drifted from a pinned 2026 standard.

### 3.2 Transform-and-check
For each gloss token we apply a language-specific reform rule and accept it as
**reform-drift** *iff* the transformed form is in the modern Hunspell dictionary
**and** the original is not. This rejects coincidental modern digraphs (German
`Theater`, `Gottheit` kept; `Thier`, `gerathen` flagged) and is wordlist-free where
the reform is definitional (Russian, below). A residual the rule cannot resolve
(inflected/compound drift, foreign words, names, OCR fragments) is classified by an
LLM pass against the 2026 standard. Implementation: one profile-driven tool,
[`detectors/ortho_drift.py`](../detectors/ortho_drift.py), one profile per language
(`de/en/fr/la/ru`).

### 3.3 Guardrail
This is a documentation / search-normalisation layer, **never a correction list** —
modernising a historical gloss would corrupt the scholarly edition. The drift reports
are a record and a search map (a user searching modern German *Tier* should still
reach Böhtlingk's *Thier*); `ortho_drift.py` never edits `csl-orig`.

## 4. Results by language

### 4.1 German — legislated, twice (the validation target)
Five German dictionaries against modern Hunspell `de_DE` (103 756 stems). The
deterministic-pass drift rate declines **monotonically with publication date**:

| dictionary (era) | tokens | modern % | drift/1k | 1901 `th` | 1901 `c` | 1996 `ß` |
|---|--:|--:|--:|--:|--:|--:|
| PW (1855–75) | 845 888 | 59 | **10.26** | 6 203 | 1 752 | 15 |
| PWG (1855–75) | 1 070 124 | 60 | 8.86 | 6 508 | 2 275 | 12 |
| GRA (1873) | 254 745 | 45 | 7.90 | 1 460 | 507 | 0 |
| CCS (1887) | 117 976 | 65 | 4.72 | 341 | 126 | 84 |
| **SCH (1928)** | 192 039 | 42 | **2.52** | **76** | **86** | **319** |

### 4.2 The SCH-1928 control — the method dates the text
The four pre-1901 dictionaries are `th`-dominated (the 1901 signature). Schmidt's
1928 *Nachträge* **flips the profile**: 1901-`th` collapses to **76** (he already
wrote *Tier*), while the 1996 `ß→ss` reform becomes *dominant* at **319** (he still
wrote *Kuß*, *naß* — pre-1996). The method does not merely count drift; it correctly
dates each dictionary's orthographic epoch from its own text.

### 4.3 Russian — legislated 1918, the dramatic case *(see also §7)*
Kossovich's pre-1918 dictionary, measured **wordlist-free** (the abolished letters
are pre-1918 by definition): 87 636 tokens · **31 389 drift · 358.17 / 1k ≈ 36 %**
(hard-sign 12 125 · decimal-і 11 106 · yat 8 139 · fita 19). Source: SamudraManthanam
`kossovich.jsonl` — external to the Cologne 33.

### 4.4 English — convention drift, editor- and age-dependent
Ten 19th-c. dictionaries against `en_GB` (so British `honour`/`-ise`/`-re` are not
flagged). The æ/œ **ligature is split out** of the reform rate as a *typographic*
convention. True reform-drift then forms a clean recency gradient: **WIL 1832 (0.46)
≫ MD 1893 (0.14) > MW 1899 (0.01) → 0**. A recency control of five 20th–21st-c.
sources — PD (Deccan College 1976–2009, 1.3 M tokens), PE, BHS, IEG, VEI — all read
**0.00** reform-drift.

### 4.5 French — convention, minimal
BUR (Burnouf 1866) **0.31** (`poëte→poète`, `françois→français`); STC (1932) **0.02**.

### 4.6 Latin — the negative control
Bopp's *Glossarium* (1847): 76 933 tokens · **0 drift**. No reform ever occurred, so
the tool — correctly — manufactures none. This confirms the method's specificity.

### 4.7 The three-tier law

| tier | reform regime | drift/1k | example |
|---|---|--:|---|
| **Legislated** | dated, state-mandated | **10 – 358** | Russian 358, German PW 10.26 |
| **Convention** | gradual editorial, no authority | **0.01 – 0.46** | English WIL 0.46 → MW 0.01 |
| **None** | no reform | **0** | Latin BOP 0 |

## 5. Can drift date a dictionary? (O4)

- **No cross-language calibration** — the rate is regime-stratified (a ~5/1k rate is
  mid-19th-c. German but off-scale for English).
- **Within a language, monotonicity tracks the regime.** German (legislated):
  Spearman ρ(year, drift/1k) = **−0.975** (p = 0.005), leave-one-out year MAE
  **±15 yr**, linear R² = 0.87. English (convention): ρ = −0.642 (p = 0.013), ±40 yr,
  and saturates — **7 English dicts read exactly 0.00 across 1890–1990**.
- **Per-era composition beats the scalar rate.** A pre-1901 rate-fit mis-dates SCH to
  1896; its `ss`-dominant composition pins it post-1901/pre-1996 exactly.

**Verdict:** drift/1k is a real but coarse, regime-bounded dating signal; for fine
dating the **per-era composition** is the robust instrument and survives a 5.5× recall-map
expansion intact, whereas the scalar gradient flattens (the DTA long tail conflates
generic early-modern variation with the dated reforms).

## 6. Does the method generalise? (O6 — French via FreEMnorm)

The *method* generalises: the `extract → dic-validate → merge` pipeline produced a
clean, reusable French reform lexicon (236 validated pairs) from the openly-licensed
FreEMnorm 17th-c. corpus with no per-language code. But a reform *map* is only safe on
target texts whose **epoch, register, and language-mix match the source**: transplanted
onto the 19th–20th-c. IAST-laced French gloss, ~90 % of the added flags are
abbreviation/homograph/transliteration collisions. Generality is a property of the
pipeline, not of any one map.

## 7. The Kossovich case: pre-1918 Russian and a digitization protocol
*(folds the former standalone "Орфография как датирующий признак" idea)*

Russia's 1918 reform is the corpus's most sweeping, and Kossovich's dictionary is its
purest specimen: 31 389 reform-drift tokens, of which the linguistically *substantive*
changes are the yat (8 139) and decimal-і (11 106) forms (the 12 125 hard-signs are
high-frequency, low-information bulk). This single case carries two transferable
results: (a) the reform signature dates a pre-revolutionary Orientalist source from its
gloss alone, and (b) it defines a reproducible normalisation protocol for digitising
such sources **without corrupting the Sanskrit transliteration** — the abolished
letters are definitional, so detection needs no wordlist. *(Open: either generalise the
protocol to a second pre-1918 Russian source or frame §7 tightly as a Kossovich case
study; cite the cross-language law of §4–§5 rather than re-deriving it.)*

## 8. Discussion

The gloss metalanguage is an under-used dating channel in historical lexicography. The
three-tier law explains why some 19th-c. dictionaries read as "misspelled" to a modern
eye while exact contemporaries read as modern: the difference is the reform regime of
the metalanguage, not the scholarship. For digital editions the practical payoff is a
search-normalisation map and an epoch label, both derived without touching the source.

## 9. Limitations

- **Modern word-lists are an uncommitted local dependency** (Hunspell `de_DE`/`en_GB`/`fr_FR`,
  resolved at runtime); figures reproduce only with equivalent snapshots on disk.
- The **dating instrument is the per-era composition**, not the absolute rate, which
  the DTA long-tail map inflates without improving era resolution.
- Token-stream purity varies (BUR/STC inline IAST, leaking a few fragments).
- The Russian source is external to the Cologne 33; the æ/œ ligature is typographic,
  reported in its own column and excluded from the reform rate.

## 10. Conclusion

A dictionary's gloss prose dates itself, and how strongly is governed by the kind of
spelling reform its metalanguage underwent. Across five languages the signal separates
into legislated, convention, and no-reform tiers, and the per-era composition resolves
the orthographic epoch from the text alone — a reproducible result extracted from a
single, uniformly marked-up lexicographic corpus.

## Data and reproducibility

Study synthesis, every figure, and the per-language reproduction commands live in
[`docs/ORTHO_DRIFT_FINDINGS.md`](../docs/ORTHO_DRIFT_FINDINGS.md); tool in
[`detectors/ortho_drift.py`](../detectors/ortho_drift.py); committed tables in
[`ortho_drift/`](../ortho_drift/). The work is documentation / search-normalisation
only — it never edits `csl-orig`.
