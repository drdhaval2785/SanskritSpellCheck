---
paper_id: A37-LChange
title: "When the S-curve Lies: Why Frequency-Trajectory Language-Change Models Misclassify Change Mechanism on Cross-Sectional Lexicographic Data"
status: "draft, new (2026-07-13, H826 ACL uplift, ruling D15)"
readiness: 2/5
venue: "LChange — Workshop on Computational Approaches to Historical Language Change (companion to A37; not a replacement — DSH stays the primary journal target)"
author: "**Mārcis Gasūns**, independent scholar (ORCID 0000-0003-4513-884X), gasyoun@ya.ru"
data_source: "docs/ORTHO_DRIFT_FINDINGS.md §O7a (study complete; figures verified against ortho_drift/*.tsv and detectors/drift_dating.py)"
parent_paper: "papers/A37_ortho_drift_paper.md (Reading the Reform off the Gloss, DSH target)"
---

# When the S-curve Lies: Why Frequency-Trajectory Language-Change Models Misclassify Change Mechanism on Cross-Sectional Lexicographic Data

> **Draft status (2026-07-13, Sonnet 5 `claude-sonnet-5`, H826 ACL Anthology uplift,
> [ROADMAP_2026_2027.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ROADMAP_2026_2027.md)
> revision 3, ruling D15).** This is a **companion short paper** to
> [A37 "Reading the Reform off the Gloss"](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A37_ortho_drift_paper.md)
> (DSH target), not a replacement for it. It isolates one result from A37 §4.8/O7a — the
> S-curve exo/endo fit — and reframes it as a **methodological caution**, which is the
> shape LChange short papers reward and DSH reviewers would find a distraction inside the
> main dating study. **Open before submission:** MG read-through; venue confirmation
> against the current [2024.lchange-1](https://aclanthology.org/volumes/2024.lchange-1/)
> call (or its successor year); a co-author decision if any is wanted for the
> methodology framing.

## Abstract

Ghanbarnejad, Gerlach, Miotto and Altmann (2014) showed that fitting a logistic S-curve
to a language variant's frequency-over-time trajectory recovers a mechanism signature:
a narrow transition width indicates an *exogenous*, centrally-imposed change (a
legislated spelling reform); a wide one indicates *endogenous*, community-driven drift.
Their method assumes a **continuous corpus tracking one text tradition's frequency
year by year** (Google Books n-grams, in their case). We apply the same logistic fit to
a **cross-sectional** corpus — one data point per historical dictionary edition, each a
different author working in a different decade — using orthographic-reform drift rates
from five European gloss languages in the Cologne Digital Sanskrit Dictionaries
(1832–2009). The fit **inverts the expected ordering**: English, whose 1830s–1990s
spelling drift is uncontroversially a *gradual, endogenous* convention shift, fits a
**narrow** 9.7-year transition; German, whose 1901 and 1996 reforms are textbook
*exogenous*, legislated, single-year events, fits a **wide** 50-year transition. We show
both results are sampling artifacts — English's narrowness is manufactured by
zero-censoring (a full century of dictionaries reading exactly 0.00 drift) and German's
width by sparse edition-spacing around the true reform date — rather than evidence
about either language's actual change mechanism. We conclude that Ghanbarnejad-style
S-curve mechanism classification requires validating corpus continuity and sampling
density *before* interpreting the fitted transition width, and offer this as a
transferable diagnostic checklist for computational historical linguists applying
S-curve models to any non-Ngram-style, edition-level, or otherwise cross-sectionally
sampled corpus — a corpus type common in the digital humanities (dictionary editions,
manuscript witnesses, periodical volumes) but not the continuous running-text corpora
S-curve methods were designed for.

## 1. Introduction

The S-curve is one of historical linguistics' most productive borrowed tools:
introduced to the field via lexical diffusion and grammaticalization studies, and
given a rigorous frequency-domain treatment by Ghanbarnejad et al. (2014), who fit
logistic curves to two centuries of German and Russian orthographic and grammatical
change tracked in Google Books n-grams and showed the curve's *shape* — not just its
midpoint — encodes whether a change was imposed from outside the speech community
(a reform decree) or negotiated within it (usage drift). This is an attractive result
for anyone working with historically dated text: it promises to recover *why* a
language changed, not just *when*, from nothing more than a frequency series.

The temptation to apply it beyond Ngram corpora is obvious, and we give in to it: the
companion paper to this one, A37 ("Reading the Reform off the Gloss," Gasūns 2026),
measures reform-drift rates in the *gloss metalanguage* of 33 historical Sanskrit
dictionaries across five European languages and finds drift magnitude stratified by
reform regime (legislated ≫ convention ≫ none). Each dictionary is one dated data
point. Fitting an S-curve to a language's dated dictionaries and reading off the
transition width seemed a natural extension — turning the qualitative
"legislated vs. convention" label into the same measured parameter Ghanbarnejad et al.
use. We ran the fit. It gave the wrong answer, in an informative way, and this short
paper is a report of *why*.

## 2. Data and method

### 2.1 The corpus (shared with A37)

Five gloss languages, each dictionary a separately-authored, separately-dated edition:
German (5 dictionaries, 1865–1928, reforms dated 1901 and 1996), English (14
dictionaries, 1832–1990, no legislated reform — convention drift only), French (2
dictionaries), Russian (1 dictionary, pre-1918), Latin (1 dictionary, no reform ever).
Each dictionary's reform-drift/1,000 gloss tokens is measured by transform-and-check
against a modern reference wordlist (A37 §3.2); full method and all figures are
committed and reproducible ([`detectors/ortho_drift.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/ortho_drift.py),
[`ortho_drift/`](https://github.com/drdhaval2785/SanskritSpellCheck/tree/master/ortho_drift)).

### 2.2 The cross-sectional S-curve proxy

Ghanbarnejad et al. fit `f(t) = 1/(1+exp(-b(t-t0)))` to the *frequency of the new
variant* at each year `t` in a continuous corpus. We have no such trajectory — only
discrete editions. Our proxy: for each language, take
`adoption(year) = 1 − drift/1k(year) ÷ max(drift/1k)` across that language's own dated
dictionaries (each dictionary's position on its own reform's residual-to-modern
scale), and fit the same two-parameter logistic via `scipy.optimize.curve_fit`
([`detectors/drift_dating.py::fit_scurve`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/drift_dating.py)).
We read off `b` (steepness, adoption-fraction per year) and the derived **20–80%
transition width** `Δt80 = ln(16)/b`, Ghanbarnejad et al.'s own transition-time
construction. A language variant needs at least 3 dated points for the 2-parameter fit
to be constrained; fewer gives an unconstrained or undefined fit and is reported as
such rather than forced.

## 3. Results

| variant | regime (ground truth) | n | b (adoption/yr) | t0 | Δt80 (yr) | R² | naive S-curve label |
|---|---|--:|--:|--:|--:|--:|---|
| **English** | convention (endogenous) | 14 | +0.286 | 1848 | **9.7** | 0.87 | "abrupt / exogenous" |
| **German** | legislated (exogenous) | 5 | +0.055 | 1895 | **50.2** | 0.84 | "gradual / endogenous" |
| German, no PW (sensitivity) | legislated (exogenous) | 4 | +0.051 | 1903 | 54.6 | 0.84 | "gradual / endogenous" |
| French | convention (endogenous) | 2 | — | — | — | — | cannot fit (n=2, unconstrained) |
| Russian | legislated (exogenous) | 1 | — | — | — | — | cannot fit (n=1, single anchor) |
| Latin | none | 1 | — | — | — | — | cannot fit (zero variance) |

By ground truth, English should show the WIDE transition (a centuries-long,
authority-free drift) and German the NARROW one (two dated, state-mandated switches).
**The fit gives the exact opposite ordering.** This is the paper's central result:
not that the S-curve method is wrong in general, but that its cross-sectional
adaptation here manufactures a confidently-labelled, precisely-quantified, and
**completely inverted** classification.

## 4. Why the fit inverts: two distinct artifacts

**English's narrow width is a zero-censoring artifact.** Seven of the fourteen English
dictionaries read *exactly* 0.00 reform-drift, spanning 1890–1990 (a full century of
ties at the ceiling of "adoption"). The two-parameter logistic, forced through this
long saturated plateau plus a handful of non-zero points clustered at the early end
(Wilson 1832 → Macdonell 1893), finds the steepest curve that clears the transition
before the plateau begins. This is a **property of the sample's saturation**, not a
measurement of how fast English orthographic convention actually changed — the
underlying process is well attested as gradual, editor-by-editor drift over more than
a century, the textbook endogenous case.

**German's wide width is a sparse-sampling artifact around a genuine point event.**
The German reforms are dated to a single year each (1901, 1996) — as centrally imposed
and abrupt a mechanism as exists. But the corpus samples only **five discrete
editions** across 1865–1928, and none falls densely enough around 1901 to resolve a
switch that, historically, was comparably fast (state-mandated, enforced in schools
within a few years). The fitted 50-year width reflects the **gap between the available
editions**, not the reform's real-world adoption speed.

Both artifacts share a root cause: **Ghanbarnejad et al.'s method assumes a
continuous, densely-sampled frequency trajectory. Cross-sectional, edition-level data —
common across the digital humanities (dictionary editions, manuscript witnesses,
periodical print runs, successive census categories) — violates that assumption in two
opposite-looking but equally fatal ways: censoring at the boundary (English) and
under-sampling near the true switch point (German).** A fitted `b`/`Δt80` from such data
is not diagnostic of mechanism until both failure modes are ruled out.

## 5. A diagnostic checklist

Before reading a fitted S-curve's transition width as an exo/endo mechanism signature
on cross-sectional (non-Ngram, edition-level) data, we recommend checking:

1. **Boundary saturation.** Does a substantial share of points sit at exactly the
   floor or ceiling of the measured quantity? If so, the fit is dominated by the
   plateau, not the transition (§4, English).
2. **Sampling density around any known switch date.** If the change has a documented
   date (a reform decree, a standardization event), are there data points within a
   few years of it on both sides? If not, the fitted width reflects edition spacing,
   not adoption speed (§4, German).
3. **Independence of points.** Are any two "dictionaries" or "editions" the same
   underlying text at different remove (an abridgement, a reprint)? A37 already flags
   this for German (PW is Böhtlingk's abridgement of PWG); we report the sensitivity
   check (Table, row 3) for transparency, though it does not change the inversion.
4. **A priori regime knowledge, held out.** Where the true mechanism is independently
   known (as here, from reform historiography — Johnson 2005; Comrie, Stone and
   Polinsky 1996), check the fitted label against it before publishing the label as a
   discovery. We did this deliberately as a validation step and it failed; we report
   the failure rather than searching for a proxy that would have passed.

## 6. Related work

Ghanbarnejad, Gerlach, Miotto and Altmann (2014) is the source method (§1). Our
corpus and its reform-regime stratification is the companion paper, A37 (Gasūns
2026), which this short paper does not restate beyond §2. The historiography of the
specific reforms — German (Johnson 2005) and Russian (Comrie, Stone and Polinsky
1996) — supplies the ground-truth mechanism labels §4 checks the fit against.
Lüschow (2021) quantifies graphemic variation across large corpora and frames
orthographic variation as a structural property of writing systems, the frame this
paper's cross-sectional-vs-continuous distinction sits inside. More generally, this
short paper's contribution is adjacent to the growing literature on **when
computational proxies fail silently** rather than a new language-change finding in
its own right — its closest methodological kin is critique-of-metric work in
historical NLP evaluation (Bollmann 2019 on normalization-system comparison
pitfalls) rather than a new S-curve application.

## 7. Limitations

- **n is small.** German n=5 (4 after the PW/PWG independence correction), English
  n=14. This short paper claims the *inversion is real and diagnosable*, not that the
  effect sizes are precisely estimated; a larger, denser corpus could still show a
  correctly-ordered S-curve once the two artifacts are corrected for.
- **We do not here construct the corrected, continuous-trajectory fit.** The Deutsches
  Textarchiv `norm`-layer long tail already banked for German in A37's O3 is the
  natural candidate for a true year-by-year frequency trajectory in a follow-up; this
  short paper's scope is the diagnosis, not the fix.
- **Two of five language cells cannot be fit at all** (Russian, Latin: n=1 each), which
  is itself consistent with our thesis — a single dated point is definitionally
  insufficient for any frequency-trajectory method, cross-sectional or continuous.

## 8. Conclusion

An S-curve fit that returns a confident, precisely-parameterized answer is not
evidence the answer is right. Applied naively to cross-sectional, edition-level
lexicographic data, the Ghanbarnejad et al. (2014) transition-width diagnostic
inverts the known exo/endo mechanism ordering for two languages with independently
documented reform histories. The failure is explicable, diagnosable in advance
(§5's checklist), and — we suspect — not unique to this corpus: any digital-humanities
dataset sampled by *edition* rather than by *year* (dictionaries, census categories,
successive print runs) is exposed to the same pair of artifacts. We publish the
inversion rather than a corrected-but-quieter result because the negative finding is
the transferable one.

## References

Bollmann, Marcel. 2019. "A Large-Scale Comparison of Historical Text Normalization
Systems." In *Proceedings of NAACL-HLT 2019,* 3885–3898. Minneapolis: Association
for Computational Linguistics.

Comrie, Bernard, Gerald Stone, and Maria Polinsky. 1996. *The Russian Language in
the Twentieth Century.* 2nd ed. Oxford: Clarendon Press.

Gasūns, Mārcis. 2026. "Reading the Reform off the Gloss: Orthographic Drift as a
Dater of 19th–20th-Century Indological Dictionaries." Manuscript in preparation
(target: *Digital Scholarship in the Humanities*).
[`papers/A37_ortho_drift_paper.md`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A37_ortho_drift_paper.md).

Ghanbarnejad, Fakhteh, Martin Gerlach, Jose M. Miotto, and Eduardo G. Altmann.
2014. "Extracting Information from S-curves of Language Change." *Journal of the
Royal Society Interface* 11 (101): 20141044.
[`arxiv.org/abs/1406.4498`](https://arxiv.org/abs/1406.4498).

Johnson, Sally. 2005. *Spelling Trouble? Language, Ideology and the Reform of
German Orthography.* Clevedon: Multilingual Matters.

Lüschow, Hanna. 2021. "Quantifying Graphemic Variation via Large Text Corpora."
*Zeitschrift für Sprachwissenschaft* 40 (3): 349–378.
[`doi.org/10.1515/zfs-2021-2038`](https://doi.org/10.1515/zfs-2021-2038).

## Data and reproducibility

All figures in this short paper are computed by
[`detectors/drift_dating.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/drift_dating.py)
§[5] (`fit_scurve`), reading the same committed
[`ortho_drift/*_drift_summary.tsv`](https://github.com/drdhaval2785/SanskritSpellCheck/tree/master/ortho_drift)
tables as A37. Full derivation, both artifacts' diagnosis, and the caveat this short
paper is built on live in
[`docs/ORTHO_DRIFT_FINDINGS.md` §O7a](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/ORTHO_DRIFT_FINDINGS.md#o7a--per-variant-logistic-s-curve-fit-adapted-from-ghanbarnejad-et-al-2014).
No new data collection; this is a re-analysis of A37's committed corpus.

---

_Dr. Mārcis Gasūns_
