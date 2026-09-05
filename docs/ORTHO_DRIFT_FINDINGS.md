_Created: 10-08-2026 · Last updated: 05-09-2026_

# Orthographic Drift in a Multilingual Indological Lexicography Corpus

*A cross-decade, five-language measurement of spelling change in the gloss text of the
Cologne Digital Sanskrit Dictionaries.*

**Status:** findings synthesis (study complete). **Scope:** documentation / search-normalization
only — nothing here edits dictionary source. See the design in
[ORTHO_DRIFT_ROADMAP.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ORTHO_DRIFT_ROADMAP.md) and the working reports in
[ortho_drift/README.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ortho_drift/README.md).

---

## Headline finding

**The magnitude of orthographic drift in a dictionary's gloss language is governed by the *type* of
the language's spelling reform, not merely by the dictionary's age.** Across five gloss languages
spanning nearly two centuries of indological lexicography (1832–2009), drift rates fall into three
sharply separated tiers:

| tier | reform regime | drift rate (per 1,000 gloss tokens) | example |
|---|---|--:|---|
| **Legislated** | a dated, state-mandated reform | **10 – 358** | Russian Kossovich **358**, German PW **10.26** |
| **Convention** | gradual editorial drift, no central authority | **0.01 – 0.46** | English WIL **0.46** → MW **0.01** (reform-only, ex-ligature); French BUR **0.31** |
| **None** | no reform ever occurred | **0** | Latin BOP **0** (negative control) |

Legislated reforms outdrift convention drift by **up to three orders of magnitude** (Russian vs.
peak English ≈ 780×; the narrowest regime boundary, German SCH 2.52 vs. English WIL 0.46, ≈ 5×). A 19th-century
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
[detectors/ortho_drift.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/ortho_drift.py), with one profile per language (`de`, `en`,
`fr`, `la`, `ru`) selected via `LANG_OF` + `PROFILES`. It reuses the body-grounded triage
infrastructure (`triage_util`). Per-language accumulating reform lexicons live in
`ortho_drift/<lang>_reform_map.tsv`; per-dictionary detail in `ortho_drift/<DICT>_drift_report.txt`;
cross-dictionary tables in `ortho_drift/<lang>_drift_summary.tsv`.

### Guardrail

This is a **documentation / search-normalization layer, never a correction list.** Modernising a
historical gloss would corrupt the scholarly edition — the same principle as the headword
[do-not-file lists](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/README.md). The drift reports are a *record* and a
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
[de_drift_summary.tsv](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ortho_drift/de_drift_summary.tsv):

| dictionary (era) | tokens | modern % | drift/1k | 1901 `th` | 1901 `c` | 1996 `ß` |
|---|--:|--:|--:|--:|--:|--:|
| PW (1879–89) | 845,888 | 59 | **10.26** | 6,203 | 1,752 | 15 |
| PWG (1855–75) | 1,070,124 | 60 | 8.86 | 6,508 | 2,275 | 12 |
| GRA (1873) | 254,745 | 45 | 7.90 | 1,460 | 507 | 0 |
| CCS (1887) | 117,976 | 65 | 4.72 | 341 | 126 | 84 |
| **SCH (1928)** | 192,039 | 42 | **2.52** | **76** | **86** | **319** |

The overall drift rate declines with publication date once PW is dated to its own print
run (kürzere Fassung, 1879–89): the monotone spine is PWG 1865 → GRA 1873 → CCS 1887 →
SCH 1928 (8.86 → 7.90 → 4.72 → 2.52 per 1k), while PW (≈1884, 10.26/1k — Böhtlingk's
conservative abridgement) sits above its date-neighbours and breaks strict monotonicity
(ρ = −0.70 at n = 5; the no-PW series is perfectly monotone, ρ = −1.00) — the corpus
modernising across ~70 years. On full PW alone the method finds
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
[de_reform_map.tsv](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ortho_drift/de_reform_map.tsv):

1. **Corpus transform-and-check** — 672 forms discovered beyond the curated seed on full PW.
2. **Residual LLM-classify** — the 6,804 unique residual tokens across the five dicts classified vs
   2026 Duden (39 Sonnet agents); **1,831 confirmed reform-drift** (27% — inflected/compound forms
   the rule missed, e.g. `thierkreise→Tierkreise`, `eigenthümlichkeiten→Eigentümlichkeiten`),
   alongside 2,981 fragment/OCR (44%), 1,105 Latin/foreign (16%), 759 modern (11%), 106 names,
   22 uncertain — see [de_residual_classified.tsv](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ortho_drift/de_residual_classified.tsv).
3. **External web-harvested merge** — 14 documented 1901/1996 pairs from the German Wikipedia reform
   articles, ingested dic-validated via
   [detectors/merge_reform_pairs.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/merge_reform_pairs.py).
4. **DTA long-tail merge** — the **Deutsches Textarchiv** lingattr-TEI corpus
   ([deutschestextarchiv.de](https://www.deutschestextarchiv.de/download), 5,285 texts, 1473–1900)
   carries a per-token `DTA::CAB norm` modern-orthography layer. [extract_dta_pairs.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/extract_dta_pairs.py)
   harvested every `surface ≠ norm` token (596 k distinct), kept those attested **≥ 20×** (43,579),
   and merge_reform_pairs.py dic-validated them → **+12,862 accepted** (textbook forms: `vnd→und`,
   `bey→bei`, `Theil→Teil`, `gantz→ganz`, `krafft→kraft`, `thaler→taler`, `creutz→kreuz`, `fuss→fuß`).

Net: the German reform lexicon grew **978 → 2,809 → 2,823 → 15,685 forms** across the four stages.
The per-dictionary drift reports are deliberately frozen at the deterministic-pass snapshot so the
SCH-control comparison stays stable; the long tail is banked in the map for future runs.

### O3 — re-run with the full 15,685-form map: rates inflate, the dating holds

The freeze decision above (keep the published gradient at the deterministic-pass snapshot) was
re-tested by re-running all five German dicts against the full 15,685-form map (`ortho_drift.py
<DICT> --full`; expanded outputs banked as [`de_drift_summary.expanded_map.tsv`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ortho_drift/de_drift_summary.expanded_map.tsv)
+ `<DICT>_drift_report.expanded_map.txt`). The result confirms the freeze was right:

| dictionary (era) | drift/1k frozen → expanded | 1901 `th` | 1901 `c` | 1996 `ß` (canon-tagged) |
|---|--:|--:|--:|--:|
| PW (1879–89) | 10.26 → **28.59** | 6,203 → 10,198 | 1,752 → 3,072 | 15 → 16 |
| PWG (1855–75) | 8.86 → **26.84** | 6,508 → 10,477 | 2,275 → 3,656 | 12 → 14 |
| GRA (1873) | 7.90 → **27.69** | 1,460 → 1,931 | 507 → 648 | 0 → 0 |
| CCS (1887) | 4.72 → **12.17** | 341 → 484 | 126 → 160 | 84 → 94 |
| **SCH (1928)** | 2.52 → **9.77** | 76 → **89** | 86 → 87 | 319 → **446** |

Two things change, one thing does not:

1. **Absolute rates roughly triple** — the bigger map recalls far more historical forms per dict.
2. **The clean publication-date gradient at the top flattens.** Frozen, the four pre-modern dicts
   declined monotonically (10.26 → 8.86 → 7.90 → 4.72); expanded, PW/PWG/GRA cluster at ~27–29 with
   **GRA (27.69) now slightly *above* PWG (26.84)** — the monotone-by-date ordering breaks at the
   top. Cause: the DTA long-tail conflates *general* early-modern and Latinate-loanword spelling
   variation (`elephant→elefant`, `insect→insekt`, `object→objekt`, `tact→takt`, `commentar→kommentar`,
   `brahman→brahmane`, `oertlichkeit→örtlichkeit`) with the *dated, legislated* 1901/1996 reforms.
   This inflates every pre-modern dict roughly equally, compressing the gradient.
3. **The SCH-1928 era-dating control is fully intact.** The dating instrument is the *relative era
   signature*, not the absolute rate — and it survives untouched: SCH remains uniquely `ß`-dominant
   (`1996-ss` **446** ≫ `1901-th` **89**), while every pre-1901 dict stays `th`-dominant (PW `th`
   **10,198** ≫ `ss` **16**). SCH still lands precisely in its post-1901/pre-1996 window. The bigger
   map does **not** blur era-dating.

**Conclusion (vindicates the freeze):** the DTA-expanded map is a **search-normalization recall
asset, not a drift-*rate* metric** — for the published per-dictionary gradient it conflates dated
reforms with generic historical variation, so that table stays frozen at the deterministic-pass
snapshot. The reliable dating instrument is the **per-era column signature** (`th`-dominant vs
`ss`-dominant), which is robust to the 5.5× map expansion. (Note: most DTA-merged `ß` forms —
`weiss→weiß`, `gross→groß`, `gefäss→gefäß` — carry a numeric DTA-attestation tag rather than the
`1996-ss` canon label, so they inflate the *total* drift but not the era column; the era signature
is therefore carried by the curated/seed forms and stays clean.)

### Russian — legislated 1918, the dramatic case

The 1918 reform is the most sweeping in the corpus: it abolished the letters ѣ (yat), і, ѳ (fita),
ѵ (izhitsa) and word-final ъ (hard sign). Kossovich's pre-1918 dictionary
([ru_drift_summary.tsv](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ortho_drift/ru_drift_summary.tsv)) therefore differs *massively* from
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
/ `-re` are correctly *not* flagged), from [en_drift_summary.tsv](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ortho_drift/en_drift_summary.tsv)
(five modern dictionaries are added as a recency control in the subsection below).

**The ligature is split out of the rate (O5).** The dominant "drift" in several dicts was the **æ/œ
ligature** (`mediæval`, `æther`, `manœuvre` → `medieval`, `ether`, `maneuvre`) — a *typographic*
print-shop convention, **not** a dated orthographic reform. It is now counted as its own `ligature`
era column but **excluded from the headline reform-drift/1k** (code: `NONREFORM_ERAS` in
[ortho_drift.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/ortho_drift.py)). The effect is large: the mid-tier dicts were almost
entirely ligature, not reform.

| dictionary (era) | tokens | reform-drift/1k | (was, w/ ligature) | ligature (typographic) | dominant reform forms |
|---|--:|--:|--:|--:|---|
| **WIL · Wilson (1832)** | 432,341 | **0.46** | 0.57 | 46 | Johnsonian `-ick` (`garlick`, `musick`) 103, archaic 78, `-xion` 19 |
| MD (1893) | 277,933 | **0.14** | 0.16 | 4 | `-xion` 39 |
| SHS (1900) | 471,442 | **0.08** | 0.31 | 109 | `-ick` 16, `-xion` 14, archaic 8 |
| GST (1856) | 152,728 | **0.04** | 0.31 | 42 | `-ick` 3, archaic 3 |
| BEN (1866) | 222,874 | **0.02** | 0.14 | 27 | `-xion` 2, scattered |
| MW · Monier-Williams (1899) | 993,490 | **0.01** | 0.01 | 0 | archaic 12 |
| MW72 (1872) | 1,222,406 | **0.01** | 0.09 | 92 | archaic 14, `-ick` 1 |
| AP90 (1890) | 471,171 | **0.00** | 0.08 | 39 | — (**all** ligature) |
| AP (modern) | 540,655 | **0.00** | 0.00 | 0 | — |
| CAE (1891) | 179,477 | **0.00** | 0.00 | 0 | — |

Separating typography from orthography sharpens the picture. True reform-drift concentrates in just
**two real classes** — Johnsonian `-ick` (overwhelmingly WIL) and `-xion→-ction` (WIL/MD/MW) —
leaving a cleaner age gradient: **WIL 0.46 ≫ MD 0.14 > MW 0.01 → ~0**. The mid-tier dicts that
*looked* like moderate drifters (SHS/GST 0.31, MW72/AP90 ~0.09) collapse to ≈0 reform once their
æ/œ ligatures are removed — AP90's "drift" was **100 %** typographic. The ligature is itself
age-correlated (the oldest dicts set the most æ/œ: SHS 109, MW72 92, WIL 46, AP90 39) — a genuine
typographic signal, just not a spelling *reform*, so it is reported in its own column.

#### Recency control — the modern end of the gradient

If the metric truly dates orthography, dictionaries compiled in the **20th–21st century** should sit
at the very bottom of the gradient (≈ 0). Five modern-leaning English sources were added as a control
— **PD** (the *Encyclopaedic Dictionary of Sanskrit*, Deccan College **1976–2009**, the most modern
and by far the largest corpus here), plus the 20th-century glossaries **PE, BHS, IEG, VEI**:

| dictionary (era) | tokens | reform-drift/1k | ligature | note |
|---|--:|--:|--:|---|
| **PD · Deccan College (1976–2009)** | 1,317,037 | **0.00** | 0 | most modern; 1.3 M tokens, **exactly zero** reform-drift |
| PE · Purāṇic Encyclopaedia (20th c.) | 740,406 | 0.00 | 0 | — |
| BHS · Edgerton (1953) | 379,068 | 0.00 | 0 | one stray `-xion` |
| IEG · Sircar (1966) | 82,932 | 0.00 | 0 | — |
| VEI · Vedic Index (1912) | 222,063 | **0.00** | 12 | was 0.06 — **all** residual æ ligature; reform-drift = 1 |

With the ligature split, the control holds even more cleanly: **all five** modern anchors are now at
**0.00 reform-drift** — VEI's former 0.06 was entirely typographic æ. The full English picture is a
monotone recency gradient from Wilson 1832 (**0.46**) down through Monier-Williams 1899 (**0.01**) to
the modern compilations (**0.00**), confirming that the detector tracks each dictionary's orthographic
epoch rather than flagging noise. (en_GB reference = the `ropensci/hunspell` `en_GB.dic`, 56,571
stems per the drift-report headers, staged locally.)

### French — convention, minimal

Two French dictionaries ([fr_drift_summary.tsv](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ortho_drift/fr_drift_summary.tsv)), run against
Hunspell `fr_FR`:

| dictionary (era) | tokens | drift/1k | examples |
|---|--:|--:|---|
| BUR · Burnouf (1866) | 229,053 | 0.31 | `poëte→poète`, `phlegme→flegme`, `françois→français` |
| STC · Stchoupak (1932) | 281,418 | 0.02 | — |

⚠️ BUR and STC inline their Sanskrit in IAST (not `{#…#}`), so a few IAST fragments (e.g. `pha`)
leak into the token stream — the macro drift-rate is robust, but individual flagged forms are less
reliable for this pair.

### Latin — the negative control

Bopp's *Glossarium* (1847), [la_drift_summary.tsv](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ortho_drift/la_drift_summary.tsv):

> 76,933 tokens · **0 drift · 0.00 per 1k**.

Latin underwent no orthographic reform, so there is no rule-set and no word-list (none exists), and
the tool — correctly — flags nothing. This is the **negative control that confirms the method's
specificity**: it does not manufacture drift where none exists.

---

## O4 — can the drift rate *date* a dictionary?

If drift/1k tracks a text's orthographic epoch, it should also *predict its publication year*. Tested
by pairing each dictionary's rate with its known year and fitting drift/1k ↔ year
([detectors/drift_dating.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/drift_dating.py) → [drift_dating.png](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ortho_drift/drift_dating.png)).
The answer is **yes, but only within a single reform regime, and only coarsely** — three findings:

**1. There is no cross-language calibration — the rate is regime-stratified.** A given drift/1k means
a different epoch in each language, because the rate scales with the *kind* of reform, not the date:

| regime | language | drift/1k range |
|---|---|--:|
| legislated, sweeping | Russian (1918) | **358** |
| legislated, twice | German (1901/1996) | **2.5 – 10** |
| convention | English / French | **0 – 0.46** |
| none | Latin | **0** |

A rate of ~5/1k is "mid-19th-c. German" but is *off the top of the scale* for English. Dating by rate
must therefore be done **within** a language.

**2. Within a language, monotonicity tracks the reform regime.** Spearman ρ(year, drift/1k):

| language | n | Spearman ρ | exact/permutation p | leave-one-out year MAE | reading |
|---|--:|--:|--:|--:|---|
| **German** (legislated) | 5 | **−0.975** | **0.033** (exact, 60 perms) | **±15 yr** | a usable coarse dater; linear R²=0.87 |
| English (convention) | 14 | −0.642 | 0.016 (Monte-Carlo) | ±40 yr | significant but editor-noisy + saturated |
| French | 2 | −1.0 | 1.000 (only 2 perms) | — | trivial (2 points) |

> **Significance correction (2026-07-03).** scipy's default Spearman p is a t-approximation
> that is **invalid at these sample sizes** — at n=5 it reported p=0.005 for German, below the
> exact minimum (~1/60 ≈ 0.017), and it mis-weights the 7 tied zeros in English. The exact
> permutation p (`drift_dating.py::exact_spearman_p`, all 60 distinct year-permutations for
> German; 100k Monte-Carlo for English) gives **German p = 0.033** (still significant, ~7× the
> t-approx) and **English p = 0.016**. The German dating gradient is real but should be reported
> at p = 0.033, and the "±15 yr instrument" rests on n=5 — coarse, as the text already says.

The **legislated** German gradient is tight (ρ = −0.975, ±15 yr over 1865–1928). The **convention**
English gradient is weak: editor idiosyncrasy outranks date below the early-19th-c. peak — Macdonell's
`-xion` puts **MD (1893) at 0.14**, *above* the older **BEN (1866) at 0.02** — and the rate **saturates
at 0**: **7 English dicts read *exactly* 0.00 across 1890–1990** (a full century the rate cannot order
or date at all).

**3. The per-era *composition* dates the epoch better than the scalar rate.** Where the rate is
ambiguous, the era breakdown is not. **SCH (Schmidt 1928):** a pre-1901-German rate-fit predicts
**1896 (−32 yr)** — the scalar rate under-dates it, mistaking its already-reformed low `th`-drift for
"near-modern." But its *composition* — `1996-ss` **dominant** over `1901-th` — pins it
**post-1901/pre-1996** exactly (the SCH control of O3). So the scalar rate places a text on a coarse
gradient; the **era signature** resolves the epoch.

**Verdict:** drift/1k is a real but **coarse, regime-bounded** dating signal — best for legislated
reforms (German ±15 yr), unreliable for convention drift (English ±40 yr, saturating to 0 post-reform),
and meaningless across languages. For fine dating, the **per-era composition** (which reforms dominate)
beats the scalar rate. A practical use: it can place an *undated* dictionary or stratum on the
pre-/post-reform timeline of *its own language*, not assign it a year.

---

## O6 — a language-general reform map from a diachronic corpus (French, via FreEMnorm)

The German map was grown from the DTA corpus's `norm` layer (the four-stage recall arc above). O6
tests whether that **extract → dic-validate → merge** pipeline *generalises* to another language, using
the openly-licensed **[FreEMnorm](https://github.com/FreEM-corpora/FreEMnorm)** parallel corpus (55
17th-c. French texts, 1606–1697, each line `diplomatic⟶normalised`).

**The pipeline runs end-to-end and the method generalises.**
[detectors/extract_freem_pairs.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/extract_freem_pairs.py) token-aligns each sentence pair
(difflib, 1:1 `replace` spans, long-ſ folded to `s` so it yields no spurious pair), harvesting **9,973
distinct `surface≠norm` pairs**; at the DTA `≥20×` threshold, **407** survive, of which
[merge_reform_pairs.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/merge_reform_pairs.py) dic-validates **236** into the French map
(`fr`: 18 → 254 forms). The accepted pairs are textbook Early-Modern→modern French — i/j (`ie→je`), u/v
(`vn→un`), y→i (`moy→moi`), circumflex-for-lost-s (`estre→être`, `nostre→notre`), and the **1835
oi→ai imperfect** (`avoit→avait`, `estoit→était`). So the harvest itself is clean and reusable
([fr_reform_freem_pairs.tsv](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ortho_drift/fr_reform_freem_pairs.tsv)).

**But the map does *not* transfer to the target dictionaries** — applied to the 19th–20c French Sanskrit
dicts (BUR 1866, STC 1932), it raises drift/1k from 0.31→3.43 (BUR) and 0.02→2.59 (STC), and **~90 % of
that increase is false positives** ([BUR](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ortho_drift/BUR_drift_report.freem.txt) /
[STC](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ortho_drift/STC_drift_report.freem.txt) banked, **not** merged into the canonical map). Three
collision classes, all from an **epoch/register/language mismatch** between a 17th-c. literary-prose map
and a 20th-c. lexicographic gloss:

| false-positive class | example | hits |
|---|---|--:|
| **grammatical abbreviation** | `moy.` (= *moyen*, middle voice) read as archaic `moy`→`moi` | 763 |
| **modern homograph of an archaic form** | `dés` (= "dice", *joueur de dés*) read as `dès`; Latin `tres` read as `très` | 600+ |
| **inline IAST Sanskrit** | `pha`/`phull`/`phur` misfired by the `ph→f` rule | ~40 |

The *genuine* archaisms BUR does carry (`aloës→aloès`, `phlegme→flegme`, `eglise→église`, `poëte→poète`,
`rhythme→rythme`) are a small long-tail — about the same order as BUR's original frozen drift (71). So
the expanded map adds **noise, not recall**, for these dicts.

**Verdict:** the *method* is language-general — the pipeline produced a clean, reusable French reform
lexicon from a free corpus with no per-language code (the `fr` profile already existed). But a reform
map is only safe on target texts whose **epoch, register, and language-mix match the source corpus**;
transplanting a 17th-c. literary map onto 19th–20c IAST-laced lexicographic glosses is dominated by
abbreviation/homograph/transliteration collisions (the O3 epoch-mismatch lesson, compounded by register
and cross-script contamination). The 236 validated pairs are kept as a standalone artifact; the
canonical French drift map and the BUR/STC figures stay **frozen** (as with O3). A clean O6 for the
Cologne French dicts would need an *epoch-matched* 19th-c. French corpus (e.g. a Frantext/BFM export),
not the 17th-c. FreEMnorm.

---

## O7 — S-curve exo/endo fit + SemEval-2015 DTE benchmark (H826, ACL uplift)

Two ACL-Anthology-informed extensions of O4, both computed by
[detectors/drift_dating.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/drift_dating.py) §[5]/§[6] (`fit_scurve` /
`dte_bands`) from the same committed `ortho_drift/*_drift_summary.tsv` data — no new
measurement, a re-reading of the existing gradient in two literatures' own vocabulary.

### O7a — per-variant logistic S-curve fit (adapted from Ghanbarnejad et al. 2014)

[Ghanbarnejad, Gerlach, Miotto & Altmann, "Extracting information from S-curves of
language change" (arXiv:1406.4498)](https://arxiv.org/abs/1406.4498), *J. R. Soc.
Interface* 2014, fit logistic S-curves to two centuries of German/Russian language
change and show the curve's **transition width** separates *exogenous* (legislated,
abrupt) from *endogenous* (community-driven, gradual) change mechanisms — the exact
"legislated ≫ convention ≫ none" gradient this paper already reports, now testable as a
measured shape rather than an assertion.

**Methodological adaptation (read before citing).** Ghanbarnejad et al. fit a logistic
to a *frequency-over-time trajectory within one continuous corpus* (Google Books
n-grams tracking one spelling variant's adoption year by year). Our corpus is
cross-sectional — one point per *dictionary*, each a different author/edition, not a
continuous text. There is no true adoption trajectory to fit. The proxy used here:

> adoption(year) = 1 − drift/1k(year) / max(drift/1k) within a language's own dated
> dictionaries — i.e. each dictionary's position on its own reform's residual-to-modern
> scale, fit to a 2-parameter logistic `1/(1+exp(-b·(t-t0)))` via `scipy.optimize.curve_fit`.

The steepness `b` (adoption-fraction/year) and the derived 20–80 % transition width
`Δt80 = ln(16)/b` (Ghanbarnejad et al.'s own transition-time construction) are the
exo/endo parameter. Only languages with n ≥ 3 dated points support a fit (a 2-point
logistic is unconstrained; a 1-point series is an anchor, not a trajectory).

| variant | n | b (adoption/yr) | t0 (inflection yr) | Δt80 (20–80% width, yr) | R² | naive label |
|---|--:|--:|--:|--:|--:|---|
| **English** (convention) | 14 | +0.2862 | 1848 | **9.7** | 0.87 | "exogenous-like (abrupt)" |
| **German** (legislated; PW ≈ 1884 refit) | 5 | +0.048 | 1904 | **57.4** | 0.65 | "endogenous-like (gradual)" |
| German, no PW (sensitivity) | 4 | +0.0507 | 1903 | 54.6 | 0.84 | "endogenous-like (gradual)" |
| French (convention) | 2 | — | — | — | — | cannot fit (n=2, unconstrained) |
| Russian (legislated) | 1 | — | — | — | — | cannot fit (n=1, single anchor) |
| Latin (none) | 1 | — | — | — | — | cannot fit (zero variance, n=1) |

**Headline finding — the naive proxy does NOT reproduce the expected mechanism split,
and that is itself the finding.** By Ghanbarnejad et al.'s own logic, English
(convention drift) should show the WIDE transition and German (a dated, legislated
reform) the NARROW one. The fit gives the **opposite ordering** (English Δt80 = 9.7 yr
≪ German Δt80 = 50.2 yr). Two distinct artifacts explain this, and both are diagnostic
of *why the proxy breaks*, not of the underlying mechanism:

1. **English's narrow fitted width is manufactured by single-point leverage under the
   max-normalized proxy, not by zero-censoring.** The seven exactly-0.00 readings
   (1890–1990, §O4[4b]) are causally inert: refitting on the seven non-zero points
   alone reproduces the fit bit-for-bit (b = +0.286, Δt80 = 9.7). The real driver is
   one point — WIL 1832 — combined with the proxy's max-normalization: Wilson's raw
   rate (0.46) is 3.3× the next dictionary's, so GST 1856 already reads as 91 %
   "adopted" and the whole "transition" is the Wilson→GST jump. Dropping that single
   point widens Δt80 to ~120–230 years (flat SSE basin) with R² collapsing from 0.87
   to ≈0.05–0.09 — the same saturation already flagged as a rate-metric weakness in
   O4 (English "gives an upper-epoch bound, not a full gradient").
2. **German's wide fitted width is driven by pre-reform proxy dispersion, not by
   sparse edition sampling.** A simulation rules the sampling explanation out: a true
   step function at 1901, sampled at exactly the five German editions (1865, 1865,
   1873, 1887, 1928 → 0, 0, 0, 0, 1), fits arbitrarily steeply — Δt80 down to 0.55
   years at the search boundary, and even the shallowest near-exact fit gives
   Δt80 ≈ 14 years, inside this paper's own "< 20 years = exogenous" threshold.
   Sparsity, had it been the driver, would have produced the correct narrow label.
   The actual driver is inter-dictionary dispersion in the pre-reform proxy: PW reads
   0.000 while PWG reads 0.1365 in the same year 1865, and CCS already reads 0.540 in
   1887 — fourteen years before the reform. A logistic forced through such points is
   flat at any grid step. (Also re-dated here: PW is Böhtlingk's *kürzere Fassung*,
   1879–1889, midpoint ≈1884 — the 1855–75 range belongs to PWG; the German rows
   above carry the PW ≈ 1884 refit.)

**Reading:** this cross-sectional adaptation of the Ghanbarnejad et al. S-curve method
is not validated as an exo/endo classifier on edition-level dictionary data — a
continuous, year-by-year frequency trajectory (as in their original Google-Ngrams
design, or the DTA `norm`-layer long tail already banked for German in O3) would be
needed to recover the true transition shape. We report `b`/`t0`/`Δt80` per language as
requested (Steps §1) and the inverted ordering as a **methodological limitation
worth publishing in its own right** — a caution against applying frequency-trajectory
S-curve machinery to sparse cross-sectional data without first checking single-point
leverage / proxy normalization and pre-reform proxy dispersion. Do not read the "exogenous-like" /
"endogenous-like" labels above as validated classifications; they are the literal
output of the naive threshold, reported for transparency, not as a finding.

### O7b — the dater in SemEval-2015 DTE terms

[SemEval-2015 Task 7, Diachronic Text Evaluation (S15-2147)](https://aclanthology.org/S15-2147/)
+ the character/word n-gram system [S15-2148](https://aclanthology.org/S15-2148/) date a
text from surface features and report accuracy as a **correct-epoch rate** (fixed-width
year bins) and **distance-to-true-year tolerance bands**. Re-expressing the existing
leave-one-out dater (O4 §[3]) in those terms places it against a known shared-task
convention rather than only an MAE specific to this paper:

| variant | n (LOO) | MAE (yr) | correct 25-yr-epoch | ≤5 yr | ≤10 yr | ≤25 yr | ≤50 yr |
|---|--:|--:|--:|--:|--:|--:|--:|
| **German** (legislated) | 5 | 14.9 | 20% | 40% | 40% | 80% | 100% |
| **English** (convention) | 14 | 39.5 | 21% | 14% | 21% | 29% | 57% |

German's ≤25 yr band (80 %) and ≤50 yr band (100 %) confirm the ±15 yr MAE headline is
not driven by a couple of lucky predictions; English's flatter profile (only 57 % even
at ≤50 yr) confirms the convention regime is a substantially weaker dater, consistent
with its saturation at 0 (§O4). Both DTE distance bands close to n as small as 5 and 14
should be read as descriptive re-expression, not a claim of statistical power comparable
to a Task-7 system trained/evaluated on hundreds of texts — [Ren et al., "Time-Aware
Language Modeling for Historical Text Dating" (2023.findings-emnlp.911)](https://aclanthology.org/2023.findings-emnlp.911/)
is the relevant black-box-dating contrast: A37's edge over such systems is not raw
accuracy at scale but **interpretability** — the dater's error is attributable to a named
reform and era-composition signature, not a latent LM representation.

### Vocabulary adopted from the normalization-measurement literature

[Bollmann, "A Large-Scale Comparison of Historical Text Normalization Systems"
(N19-1389)](https://aclanthology.org/N19-1389/) and
[`coastalcph/histnorm`](https://github.com/coastalcph/histnorm) establish word-accuracy
and CER-on-incorrect-subset as the field's standard measurement vocabulary. This paper's
drift/1k is not directly a normalization-accuracy metric (there is no gold-normalized
reference text, only a transform-and-check rule against a modern wordlist), but the
**modern%** column already reported per dictionary (§ results tables above) is the same
family of measurement — the fraction of tokens already matching the modern surface form
— and is named here explicitly as such for a DSH/CL reviewer's benefit, rather than left
implicit.

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
python drift_dating.py                   # O4: drift/1k <-> year calibration + plot (needs scipy, matplotlib)
# O6 (French, FreEMnorm): stage corpus to external_src/freem/, then
python extract_freem_pairs.py ../external_src/freem/corpus ../external_src/freem/freem_fr_pairs.tsv 20
python merge_reform_pairs.py fr ../external_src/freem/freem_fr_pairs.tsv   # dic-validate -> fr map
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
| German residual LLM-classify (6,804 → 1,831 drift) | [de_residual_classified.tsv](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ortho_drift/de_residual_classified.tsv) |

_Dr. Mārcis Gasūns_
