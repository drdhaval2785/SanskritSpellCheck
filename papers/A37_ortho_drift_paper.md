_Created: 10-08-2026 · Last updated: 06-09-2026_

---
paper_id: A37
title: "Reading the Reform off the Gloss: Orthographic Drift as a Dater of 19th–20th-Century Indological Dictionaries"
status: author passes executed 2026-07-11 and 2026-09-06, pending MG read-and-sign (SIGNOFF_A37_author_pass.md)
readiness: 4/5
venue: "Digital Scholarship in the Humanities (DSH) — per the locked venue split"
author: "**Mārcis Gasūns**, independent scholar ([ORCID 0000-0003-4513-884X](https://orcid.org/0000-0003-4513-884X)), gasyoun@ya.ru"
data_source: "docs/ORTHO_DRIFT_FINDINGS.md (study complete; figures verified against ortho_drift/*.tsv)"
---

# Reading the Reform off the Gloss: Orthographic Drift as a Dater of 19th–20th-Century Indological Dictionaries

> **Draft status (2026-06-26; referee fixes applied 2026-07-03, author-voice pass
> 2026-07-11, both Fable 5
> `claude-fable-5`, per [A37_review_fable5.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A37_review_fable5.md)
> and [SIGNOFF_A37_author_pass.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/SIGNOFF_A37_author_pass.md)).**
> Second author-voice pass 06-09-2026 ([SIGNOFF_A37_author_pass.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/SIGNOFF_A37_author_pass.md), Pass 2 section; Fable 5.1 `claude-fable-5-1`).
> Manuscript built directly on the completed
> study in [`docs/ORTHO_DRIFT_FINDINGS.md`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/ORTHO_DRIFT_FINDINGS.md). All
> numerical claims below are transcribed from that synthesis and recompute from the
> committed [`ortho_drift/`](https://github.com/drdhaval2785/SanskritSpellCheck/tree/master/ortho_drift) TSVs;
> significance values use the exact/permutation correction of 2026-07-03. The byline
> is the canonical author identity (name, independent-scholar affiliation, ORCID,
> gasyoun@ya.ru — as used for the A25 submission). **Open
> before submission (author-only):** MG read-through + sign-off per the signoff
> document. The
> Russian/Kossovich
> material is folded in as §7 — it absorbs the former standalone
> "Kossovich pre-1918 digitisation protocol" idea and is framed as the extreme-regime
> case study. **ACL Anthology uplift (2026-07-13, H826, Sonnet 5
> `claude-sonnet-5`, ruling D15):** §2 gains three related-work paragraphs (Ghanbarnejad
> et al.'s S-curve method, SemEval-2015 DTE, ZfS graphemic variation); new §4.8 reports
> the S-curve exo/endo fit as a **negative methodological result** (the naive
> cross-sectional proxy inverts the expected mechanism ordering — read the caveat before
> citing); §5 gains the DTE distance-band re-expression. An [LChange short-paper
> companion](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A37_lchange_companion.md)
> drafts the S-curve finding as a standalone submission to the venue that community lives
> in. DSH remains the primary journal target for this manuscript.

## Abstract

Each historical bilingual dictionary is written twice over: once in the headword
language it describes, and once in the *metalanguage* of its glosses, prefaces, and
definitions. We show that the second of these — the gloss prose — carries a datable
orthographic fingerprint, and that the **magnitude and composition of orthographic
drift in the gloss language are governed by the *type* of that language's spelling
reform, not merely by the dictionary's age.** Measured against a pinned 2026
standard across five gloss languages and nearly two centuries of sources (1832–2009),
the Cologne Digital Sanskrit Dictionaries and one external pre-revolutionary
Russian source, drift rates fall into three sharply separated tiers: **legislated**
reform (Russian 1918 ≈ 358 / 1 000 gloss tokens; German 1901/1996 ≈ 2.5–10), **convention**
drift (English / French ≈ 0–0.46), and **none** (Latin = 0, a negative control). The
tiers span nearly three orders of magnitude between regime extremes and narrow to
roughly five-fold at the closest regime boundary. We further show that the *per-era
composition* of the drift (which reform's forms dominate) dates a dictionary's
orthographic epoch from its own prose more reliably than the scalar rate: Schmidt's
1928 supplement flips from a `th`-dominant (pre-1901) to an `ß`-dominant (pre-1996)
signature, landing it precisely in its true window. The contribution is the application of an existing, mature technique,
historical-spelling normalisation, to a multilingual, era-stratified *lexicographic*
corpus, yielding a reproducible cross-decade drift dataset and a metalanguage-dating
method; no new normaliser is proposed.

## 1. Introduction

Historical lexicography is usually dated by its title page. We ask whether a
dictionary's *text* — specifically its gloss metalanguage — can date itself, and
what governs how strongly it can. The Cologne Digital Sanskrit Dictionaries are an
unusually clean testbed: a single, uniformly marked-up corpus of 33 dictionaries
(the fits and dated series draw on 24 of the 33, plus one external Russian
source, Kossovich; the per-language n values are given below)
whose authors wrote in four European metalanguages across nearly two centuries
(1832–2009) —
Wilson's 1832 English, Böhtlingk–Roth's 1850s–70s German, Burnouf's 1866 French,
Bopp's 1847 Latin — plus 20th- and 21st-century compilations. Because Cologne markup wraps the
Sanskrit object-language in `{#…#}` / `{@…@}` spans, the European gloss text is
exactly what falls *outside* those spans and can be isolated and measured.

Our claims:

1. **A three-regime stratification.** Drift magnitude is stratified by reform
   *regime* (legislated ≫ convention ≫ none), not by raw age.
2. **A dating instrument.** Within a regime the rate tracks date coarsely; the
   per-era *composition* dates the orthographic epoch finely and language-internally.
3. **A method, not a corrector.** The output is a documentation / search-normalisation
   layer; it never edits the scholarly source. (This is the same do-not-modify
   principle as the headword do-not-file lists in the host project.)

## 2. Related work

**Historical-spelling normalisation is a mature DH subfield, and we build on it
rather than extend it.** Interactive and rule-based normalisers exist for every
gloss language in our corpus: VARD 2 for early-modern English (Baron and Rayson
2008), the Norma tool and its successors for historical German (Bollmann 2012),
the Deutsches Textarchiv's CAB canonicalisation layer (Jurish 2012), and the
FreEM resources for early-modern French (Bawden et al. 2022) — with Bollmann
(2019) providing the cross-system comparison that establishes the subfield's
maturity. All of these normalise the *object text* of an edition or archive. None,
to our knowledge, has been pointed at the **gloss metalanguage of bilingual
dictionaries** — the channel measured here.

**Dating a text from its language is likewise established** — stylochronometry
orders an author's works by stylistic development (Stamou 2008), and computational
approaches rank and date texts from lexical and morphological features (Niculae et
al. 2014). These methods date by *style and lexis*; ours dates by the **reform
signature of the spelling system itself**, which is why it works on the highly
formulaic, stylistically flat prose of dictionary glosses where stylometry has
little purchase — and why its resolution is bounded by the reform calendar rather
than by corpus size.

**The "legislated ≫ convention ≫ none" gradient (§1, §4.7) is itself a published
parameter of language change, not merely an assertion of this paper.** Ghanbarnejad,
Gerlach, Miotto and Altmann (2014) fit logistic S-curves to two centuries of German and
Russian language change — our exact two legislated-reform languages — and show the
curve's *transition shape* separates exogenous (centrally imposed) from endogenous
(community-driven) change mechanisms. We adapt their S-curve fit to our cross-sectional
dictionary data (§4.8; the adaptation is imperfect and the result is reported as a
methodological limitation, not a confirmation — see the caveat there). We also
re-express the leave-one-out dater (§5) in the terms of a known shared task, **SemEval-2015
Task 7, Diachronic Text Evaluation** (Popescu and Strapparava 2015; the character/word
n-gram system of Szymanski and Lynch 2015), so the accuracy is placeable against a
convention (correct-epoch rate, distance-to-true-year bands) rather than only an
MAE specific to this paper. Ren, Wang, Zhao and Ren (2023), a black-box
language-model dater, is cited as the contrast: against it, this paper's
interpretability (an error attributable to a named reform, not a latent
representation) is the relative advantage, not raw accuracy at scale. Graphemic variation as a datable signal
in its own right is discussed generally in Lüschow (2021, *Zeitschrift für
Sprachwissenschaft* 40(3)), which quantifies graphemic variation across large corpora
and frames orthographic variation as a structural property of writing systems rather
than error — the frame this paper's "drift is regime-governed, not merely
age-governed" claim (§1) sits inside.

**The reforms themselves are well documented as historical events** — the German
reforms of 1901 and 1996 and their politics (Johnson 2005), the Russian reform of
1918 (Comrie, Stone and Polinsky 1996) — but the historiography treats them as
objects of study, not as instruments. Lexicographic theory has long
recognised the definition/gloss language as a distinct structural layer of the
dictionary (Hausmann and Wiegand 1989), yet treats it qualitatively.

The contribution of this paper is therefore the *application*: a multilingual,
era-stratified, uniformly marked-up **lexicographic gloss corpus** as the measured
object; the **reform-regime stratification** of drift magnitude; and the
**per-era composition** (not the scalar rate) as the dating instrument — none of
which requires, or offers, a new normaliser.

Finally, spellchecking of the Sanskrit **object language** is its own, separate
line of work — most comprehensively Prasanna (2022), a Paninian word-and-paradigm
Hunspell dictionary with an online interface (the 10-07-2026 survey in
[docs/PRIOR_ART.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/PRIOR_ART.md) surveys that work). It shares this
paper's Hunspell tooling family — our drift measurements run against Hunspell
reference dictionaries for the gloss languages (de_DE, en_GB) — but targets the
opposite channel: the headword language, not the gloss metalanguage measured here.

## 3. Data and method

### 3.1 Corpus and the measured channel
The period orthography lives in the gloss language, not in the Sanskrit. Cologne
markup already separates the two, so we extract gloss tokens (outside `{#…#}` /
`{@…@}`) and measure how far they have drifted from a pinned 2026 standard.

### 3.2 Transform-and-check
For each gloss token we apply a language-specific reform rule and accept it as
**reform-drift** only if the transformed form is in the modern Hunspell dictionary
**and** the original is not. This rejects coincidental modern digraphs (German
`Theater`, `Gottheit` kept; `Thier`, `gerathen` flagged) and is wordlist-free where
the reform is definitional (Russian, below). A residual the rule cannot resolve
(inflected/compound drift, foreign words, names, OCR fragments) is classified by an
LLM pass against the 2026 standard. The implementation is a single profile-driven tool,
[`detectors/ortho_drift.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/ortho_drift.py), with one profile per language
(`de/en/fr/la/ru`).

**Denominator comparability.** The "modern %" column below swings 42–65 % across
the German five because differently-edited dictionaries shed different material
before the reform test: proper names, Latin botanical binomials, inline
transliteration fragments, and OCR debris all fall out of the checkable-token
denominator. The drift/1k rate is nonetheless comparable across dictionaries
because the *numerator* is reform-specific (a `th`/`c`/`ß` transform validated
against the modern wordlist) and the excluded material is reform-inert — a name or
a botanical term carries no 1901/1996 signature either way; the exclusion shrinks
the denominator for all dictionaries in the same reform-blind manner. The per-era
*composition* (§4.2, §5) is unaffected entirely, being a ratio among the
numerator's own parts.

### 3.3 Guardrail
This is a documentation / search-normalisation layer, **never a correction list**:
modernising a historical gloss would corrupt the scholarly edition. The drift reports
are a record and a search map (a user searching modern German *Tier* should still
reach Böhtlingk's *Thier*); `ortho_drift.py` never edits `csl-orig`.

## 4. Results by language

### 4.1 German — legislated, twice (the validation target)
Five German dictionaries against modern Hunspell `de_DE` (103 756 stems). Dating PW to
its own print run — Böhtlingk's *kürzere Fassung*, 1879–1889 (midpoint ≈1884; the
1855–75 range belongs to PWG) — the deterministic-pass drift rate falls across the
series (10.26 → 2.52 per 1k), but no longer **strictly monotonically**: the pre-1901
line PWG 1865 (8.86) → GRA 1873 (7.90) → CCS 1887 (4.72) → SCH 1928 (2.52) is
monotone, while PW (≈1884) reads **10.26** — above its date-neighbours, as expected
for Böhtlingk's conservative abridgement:

| dictionary (era) | tokens | modern % | drift/1k | 1901 `th` | 1901 `c` | 1996 `ß` |
|---|--:|--:|--:|--:|--:|--:|
| PW (1879–89) | 845 888 | 59 | **10.26** | 6 203 | 1 752 | 15 |
| PWG (1855–75) | 1 070 124 | 60 | 8.86 | 6 508 | 2 275 | 12 |
| GRA (1873) | 254 745 | 45 | 7.90 | 1 460 | 507 | 0 |
| CCS (1887) | 117 976 | 65 | 4.72 | 341 | 126 | 84 |
| **SCH (1928)** | 192 039 | 42 | **2.52** | **76** | **86** | **319** |

### 4.2 The SCH-1928 control — the method dates the text
The four pre-1901 dictionaries are `th`-dominated (the 1901 signature). Schmidt's
1928 *Nachträge* **flips the profile**: 1901-`th` collapses to **76** (he already
wrote *Tier*), while the 1996 `ß→ss` reform becomes *dominant* at **319** (he still
wrote *Kuß*, *naß* — pre-1996). Beyond counting drift, the method correctly dates each dictionary's orthographic
epoch from its own text. Figure 1 shows the
flip as per-era composition shares.

![Figure 1. Per-era composition of German reform drift across the five dictionaries; Schmidt's 1928 supplement flips from th-dominant (pre-1901 signature) to ß-dominant (post-1901, pre-1996).](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ortho_drift/drift_composition.png)

### 4.3 Russian — legislated 1918, the extreme case *(see also §7)*
Kossovich's pre-1918 dictionary, measured **wordlist-free** (the abolished letters
are pre-1918 by definition): 87 636 tokens · **31 389 drift · 358.17 / 1k ≈ 36 %**
(hard-sign 12 125 · decimal-і 11 106 · yat 8 139 · fita 19). The source is SamudraManthanam's
`kossovich.jsonl`, external to the Cologne 33.

### 4.4 English — convention drift, editor- and age-dependent
Fifteen English dictionaries — fourteen dated (the n = 14 of §5's correlation), plus
the undated modern Apte held out
as a test case — against `en_GB` (so British `honour`/`-ise`/`-re` are not
flagged). The æ/œ **ligature is split out** of the reform rate as a *typographic*
convention. True reform-drift then declines with recency at the early end — **WIL
1832 (0.46) ≫ MD 1893 (0.14) > MW 1899 (0.01)** — and then **saturates at zero**: a
recency control of five 20th–21st-c.
sources — PD (Deccan College 1976–2009, 1.3 M tokens), PE, BHS, IEG, VEI — all read
**0.00** reform-drift, as do seven English dictionaries spanning 1890–1990 (§5).
Under a convention regime, English drift therefore gives an **upper-epoch bound**
(non-zero drift ⇒ early), not a full gradient.

### 4.5 French — convention, minimal
BUR (Burnouf 1866) **0.31** (`poëte→poète`, `françois→français`); STC (1932) **0.02**.

### 4.6 Latin — the negative control
Bopp's *Glossarium* (1847): 76 933 tokens · **0 drift**. No reform ever occurred, so
the tool, correctly, manufactures none, which confirms the method's specificity.

### 4.7 The three-regime stratification

| tier | reform regime | drift/1k | example |
|---|---|--:|---|
| **Legislated** | dated, state-mandated | **10 – 358** | Russian 358, German PW 10.26 |
| **Convention** | gradual editorial, no authority | **0.01 – 0.46** | English WIL 0.46 → MW 0.01 |
| **None** | no reform | **0** | Latin BOP 0 |

### 4.8 S-curve exo/endo fit (O7a) — a negative methodological result

Ghanbarnejad et al. (2014) fit each language variant's adoption trajectory to a
logistic S-curve `1/(1+exp(-b·(t-t0)))` and read the transition width `Δt80 =
ln(16)/b` (time from 20% to 80% adoption) as a mechanism signature: narrow ⇒
exogenous/legislated, wide ⇒ endogenous/convention. We adapt this to our data by
treating each dictionary's `1 − drift/1k ÷ max(drift/1k)` (within its own language) as
an adoption fraction and fitting the same logistic
([`detectors/drift_dating.py::fit_scurve`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/drift_dating.py)):

| variant | n | b (adoption/yr) | t0 | Δt80 (yr) | R² | naive label |
|---|--:|--:|--:|--:|--:|---|
| English (convention) | 14 | +0.286 | 1848 | **9.7** | 0.87 | "abrupt" |
| German (legislated; PW ≈ 1884 refit) | 5 | +0.048 | 1904 | **57.4** | 0.65 | "gradual" |
| German, no PW | 4 | +0.051 | 1903 | 54.6 | 0.84 | "gradual" |
| French / Russian / Latin | ≤2 | — | — | — | — | cannot fit (n too small / zero-variance) |

**This inverts the expected mechanism ordering, and we report the inversion as the
finding rather than force the expected label.** Adversarial refits sharpen the
diagnosis: English's narrow width is manufactured by single-point leverage under the
max-normalized proxy — Wilson 1832 hands the fit its whole transition (refitting on
the non-zero points alone is bit-identical; dropping Wilson widens Δt80 to ~120–230
years) — while German's wide width is driven by pre-reform proxy dispersion (PW 0.000
vs PWG 0.1365 in the same year 1865; CCS 0.540 already in 1887), since a true 1901
step sampled at these five editions would fit arbitrarily steeply (Δt80 ≤ 14 years).
A cross-sectional adaptation of a *frequency-trajectory* S-curve method is therefore
**not validated as an exo/endo classifier** on edition-level lexicographic data without
first checking single-point leverage / proxy normalization and pre-reform proxy
dispersion. We report this as a transferable caution for anyone applying
Ghanbarnejad-style S-curves to non-continuous corpora, alongside the parameter values
themselves. Full derivation and caveats: [O7a in
`docs/ORTHO_DRIFT_FINDINGS.md`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/ORTHO_DRIFT_FINDINGS.md#o7a--per-variant-logistic-s-curve-fit-adapted-from-ghanbarnejad-et-al-2014).

## 5. Can drift date a dictionary? (O4, O7b)

There is **no cross-language calibration**: the rate is regime-stratified (a ~5/1k
rate is mid-19th-c. German but off-scale for English).

**Within a language, monotonicity tracks the regime, with one retraction.** German
(legislated): an earlier version of this analysis reported Spearman ρ(year, drift/1k)
= **−0.975** (exact permutation p = 0.033, n = 5) and a strictly monotone decline;
that series was computed with PW mis-dated to 1865 (PWG's range). With PW dated to
its own print run (kürzere Fassung 1879–1889, midpoint ≈1884) the five-point
correlation drops to ρ = **−0.70** (exact permutation p = 0.23) and strict
monotonicity fails (PW 10.26 sits above its 1873/1887 neighbours); the five-point
fit itself refits to b = +0.048, t0 = 1904, Δt80 = 57.4, R² = 0.65. The defensible
German series is the **no-PW line** (n = 4, strictly monotone, ρ = −1.00,
Δt80 = 54.6, R² = 0.84), since PW is both the double-counted point (Böhtlingk's
abridgement of PWG, same lexicographer, overlapping gloss prose) and the one that
breaks monotonicity. All §5 statistics remain **case-study-scale, not corpus-scale
inference**. English (convention): ρ = −0.642 (Monte-Carlo permutation p = 0.016,
n = 14), ±40 yr, and saturates — **7 English dicts read exactly 0.00 across
1890–1990** — so under a convention regime the rate is an upper-epoch bound (§4.4),
not a dater. The German calibration is plotted in the committed
[drift_dating.png](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ortho_drift/drift_dating.png)
(Figure 2).

**Per-era composition beats the scalar rate.** A pre-1901 rate-fit mis-dates SCH to
1896; its `ss`-dominant composition pins it post-1901/pre-1996 exactly.

- **Re-reported in SemEval-2015 Diachronic Text Evaluation terms (O7b)**, so the dater
  is placeable against a known shared-task convention rather than only an MAE specific
  to this paper: German's leave-one-out predictions land within **±25 yr for 80 %** and
  **±50 yr for 100 %** of held-out dictionaries (correct-25-yr-epoch rate 20 %,
  n = 5); English's flatter, saturation-limited profile reaches only **57 % even at
  ±50 yr** (n = 14). These bands are a descriptive re-expression of the same LOO fit
  above, not a claim of Task-7-scale statistical power at n = 5/14. Full table: [O7b in
  `docs/ORTHO_DRIFT_FINDINGS.md`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/ORTHO_DRIFT_FINDINGS.md#o7b--the-dater-in-semeval-2015-dte-terms).

**In sum:** drift/1k is a real but coarse, regime-bounded dating signal; for fine
dating the **per-era composition** is the instrument that holds: it survives a 5.5× recall-map
expansion intact, whereas the scalar gradient flattens (the DTA long tail conflates
generic early-modern variation with the dated reforms).

## 6. Does the method generalise? French via FreEMnorm

The *method* generalises: the `extract → dic-validate → merge` pipeline produced a
clean, reusable French reform lexicon (236 validated pairs) from the openly-licensed
FreEMnorm 17th-c. corpus with no per-language code. But a reform *map* is only safe on
target texts whose **epoch, register, and language-mix match the source**: transplanted
onto the 19th–20th-c. IAST-laced French gloss, ~90 % of the added flags are
abbreviation/homograph/transliteration collisions. Generality is a property of the
pipeline, not of any one map.

## 7. The Kossovich case: pre-1918 Russian and a digitisation protocol
*(folds the former standalone "Орфография как датирующий признак" idea)*

Russia's 1918 reform is the corpus's most sweeping, and Kossovich's dictionary is its
purest specimen: 31 389 reform-drift tokens, of which the linguistically *substantive*
changes are the yat (8 139) and decimal-і (11 106) forms (the 12 125 hard-signs are
high-frequency, low-information bulk). This single case carries two transferable
results: (a) the reform signature dates a pre-revolutionary Orientalist source from its
gloss alone, and (b) it defines a reproducible normalisation protocol for digitising
such sources **without corrupting the Sanskrit transliteration** — the abolished
letters are definitional, so detection needs no wordlist. We deliberately keep §7 a
single tight case study — the extreme-regime instance of the §4–§5 stratification,
cited rather than re-derived; generalising the protocol to further pre-1918 Russian
sources is downstream digitisation work, not part of this paper's claim.

## 8. Discussion

The gloss metalanguage is an under-used dating channel in historical lexicography. The
three-regime stratification explains why some 19th-c. dictionaries read as
"misspelled" to a modern
eye while exact contemporaries read as modern: the difference is the reform regime of
the metalanguage, not the scholarship. For digital editions the practical payoff is a
search-normalisation map and an epoch label, both derived without touching the source.

## 9. Limitations

- **Regime and language-vitality are confounded at the "none" tier.** Latin's zero
  is overdetermined: Latin had no spelling reform, but it also had no living
  orthographic community that could have drifted. The negative control therefore
  shows the tool manufactures no drift where none exists — which is its job — but
  cannot by itself separate "no reform" from "no living usage"; only a reformless
  *living* language could, and the corpus contains none.
- **Two regime cells rest on one language each** (legislated-extreme: Russian,
  n = 1 dictionary; none: Latin, n = 1), which is why we report a stratification
  observed on this corpus, not a law.
- **Modern word-lists are an uncommitted local dependency** (Hunspell `de_DE`/`en_GB`/`fr_FR`,
  resolved at runtime); figures reproduce only with equivalent snapshots on disk —
  see the data-availability statement below for the snapshot identities.
- The **dating instrument is the per-era composition**, not the absolute rate, which
  the DTA long-tail map inflates without improving era resolution.
- Token-stream purity varies (BUR/STC inline IAST, leaking a few fragments).
- The Russian source is external to the Cologne 33; the æ/œ ligature is typographic,
  reported in its own column and excluded from the reform rate.

## 10. Conclusion

A dictionary's gloss prose dates itself, and how strongly it does so is governed by
the kind of spelling reform its metalanguage underwent. Across five languages the signal separates
into legislated, convention, and no-reform tiers, and the per-era composition resolves
the orthographic epoch from the text alone — a reproducible result extracted from a
single, uniformly marked-up lexicographic corpus.

## Data and reproducibility

Study synthesis, every figure, and the per-language reproduction commands live in
[`docs/ORTHO_DRIFT_FINDINGS.md`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/ORTHO_DRIFT_FINDINGS.md); tool in
[`detectors/ortho_drift.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/ortho_drift.py); committed tables and figures in
[`ortho_drift/`](https://github.com/drdhaval2785/SanskritSpellCheck/tree/master/ortho_drift). The work is documentation / search-normalisation
only — it never edits `csl-orig`.

**Data-availability statement.** All drift tables, the detector, and the study
synthesis are committed in the repository. The modern reference word-lists are a
**local runtime dependency, not committed** (licensing): German = Hunspell `de_DE`
(103,756 stems), English = the `ropensci/hunspell` `en_GB.dic` snapshot (56,571
stems), French = Hunspell `fr_FR`. Reported figures reproduce exactly against these
snapshot identities; a different wordlist release may shift raw counts slightly but
does not affect the regime stratification or the per-era composition (validated
against a 5.5× recall-map expansion, §5). The Russian detection is wordlist-free
(the abolished letters are definitional). The pinned modern standard is 2026.

## References (draft — author to finalise)

Baron, Alistair, and Paul Rayson. 2008. "VARD2: A Tool for Dealing with Spelling
Variation in Historical Corpora." In *Proceedings of the Postgraduate Conference in
Corpus Linguistics.* Birmingham: Aston University.

Bawden, Rachel, Jonathan Poinhos, Eleni Kogkitsidou, Philippe Gambette, Benoît
Sagot, and Simon Gabay. 2022. "Automatic Normalisation of Early Modern French." In
*Proceedings of the 13th Language Resources and Evaluation Conference (LREC 2022),*
3354–3366. Marseille: European Language Resources Association.

Bollmann, Marcel. 2012. "(Semi-)Automatic Normalization of Historical Texts Using
Distance Measures and the Norma Tool." In *Proceedings of the Second Workshop on
Annotation of Corpora for Research in the Humanities (ACRH-2).* Lisbon.

Bollmann, Marcel. 2019. "A Large-Scale Comparison of Historical Text Normalization
Systems." In *Proceedings of NAACL-HLT 2019,* 3885–3898. Minneapolis: Association
for Computational Linguistics. See also the accompanying [`coastalcph/histnorm`](https://github.com/coastalcph/histnorm)
benchmark repository, which fixes word-accuracy and CER-on-incorrect-subset as the
field's standard measurement vocabulary (§O7b/data-and-method).

Comrie, Bernard, Gerald Stone, and Maria Polinsky. 1996. *The Russian Language in
the Twentieth Century.* 2nd ed. Oxford: Clarendon Press.

Ghanbarnejad, Fakhteh, Martin Gerlach, Jose M. Miotto, and Eduardo G. Altmann.
2014. "Extracting Information from S-curves of Language Change." *Journal of the
Royal Society Interface* 11 (101): 20141044.
[`arxiv.org/abs/1406.4498`](https://arxiv.org/abs/1406.4498).

Hausmann, Franz Josef, and Herbert Ernst Wiegand. 1989. "Component Parts and
Structures of General Monolingual Dictionaries: A Survey." In Hausmann, Reichmann,
Wiegand and Zgusta (eds.), *Wörterbücher / Dictionaries / Dictionnaires,* vol. 1
(HSK 5.1), 328–360. Berlin and New York: Walter de Gruyter.

Johnson, Sally. 2005. *Spelling Trouble? Language, Ideology and the Reform of
German Orthography.* Clevedon: Multilingual Matters.

Jurish, Bryan. 2012. *Finite-State Canonicalization Techniques for Historical
German.* PhD dissertation, Universität Potsdam.

Lüschow, Hanna. 2021. "Quantifying Graphemic Variation via Large Text Corpora."
*Zeitschrift für Sprachwissenschaft* 40 (3): 349–378.
[`doi.org/10.1515/zfs-2021-2038`](https://doi.org/10.1515/zfs-2021-2038).

Niculae, Vlad, Marcos Zampieri, Liviu P. Dinu, and Alina Maria Ciobanu. 2014.
"Temporal Text Ranking and Automatic Dating of Texts." In *Proceedings of EACL
2014,* 17–21. Gothenburg: Association for Computational Linguistics.

Popescu, Octavian, and Carlo Strapparava. 2015. "SemEval 2015, Task 7: Diachronic
Text Evaluation." In *Proceedings of the 9th International Workshop on Semantic
Evaluation (SemEval 2015),* 870–878. Denver: Association for Computational
Linguistics. [`aclanthology.org/S15-2147`](https://aclanthology.org/S15-2147/).

Prasanna, S. 2022. "Spellchecker for Sanskrit: The Road Less Taken." In
*Proceedings of the 19th International Conference on Natural Language Processing
(ICON 2022),* 290–299. New Delhi: NLP Association of India.
[`aclanthology.org/2022.icon-main.35`](https://aclanthology.org/2022.icon-main.35/).

Ren, Han, Hai Wang, Yajie Zhao, and Yafeng Ren. 2023. "Time-Aware Language
Modeling for Historical Text Dating." In *Findings of the Association for
Computational Linguistics: EMNLP 2023,* 13646–13656. Singapore: Association for
Computational Linguistics. [`aclanthology.org/2023.findings-emnlp.911`](https://aclanthology.org/2023.findings-emnlp.911/).

Stamou, Constantina. 2008. "Stylochronometry: Stylistic Development, Sequence of
Composition, and Relative Dating." *Literary and Linguistic Computing* 23 (2):
181–199.

Szymanski, Terrence, and Gerard Lynch. 2015. "UCD: Diachronic Text Classification
with Character, Word, and Syntactic N-grams." In *Proceedings of the 9th
International Workshop on Semantic Evaluation (SemEval 2015),* 879–883. Denver:
Association for Computational Linguistics. [`aclanthology.org/S15-2148`](https://aclanthology.org/S15-2148/).

**Primary digital source.** Cologne Digital Sanskrit Dictionaries (CDSL).
Institute of Indology and Tamil Studies, University of Cologne.
[`sanskrit-lexicon.uni-koeln.de`](https://www.sanskrit-lexicon.uni-koeln.de/).

_Dr. Mārcis Gasūns_
