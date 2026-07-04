# A37 — referee-style review (pre-submission)

_Created: 02-07-2026 · Last updated: 03-07-2026_

Substantive review of
[H042-Fable_SanskritSpellCheck_ortho_drift_26.06.26_paper.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/H042-Fable_SanskritSpellCheck_ortho_drift_26.06.26_paper.md)
by Fable 5 (`claude-fable-5`), 02-07-2026, within the Fable trial window — the highest-judgment
gate the roadmap assigns to this period. Target venue per the locked split: **DSH** (Digital
Scholarship in the Humanities). Fact-checking was done separately (02-07, ~35 claims, 5 fixes);
this review is about argument, framing, and what a DSH referee will attack.

**Overall verdict: strong core result, submittable to DSH after the fixes below — the design
(negative control + era-flip validation + honest negative results in §5–§6) is better than most
DSH method papers. The exposure points are overclaim words ("law"), sample independence, and the
empty related-work section.**

## Major (must fix before submission)

1. **§2 Related work is empty, and for THIS paper it is load-bearing.** The novelty claim
   ("application, not a new normalizer") only stands if the section demonstrates command of the
   normalization literature (VARD, Norma, DTA::CAB, FreEMnorm) **and** — currently missing
   entirely — **stylochronometry / text-dating**. Dating texts from language features is an
   established field; a referee who knows it will write "dating from orthography is not new."
   The true novelty must be stated against it: (a) the *gloss metalanguage of dictionaries* as
   the dated channel (nobody dates the *definition language*), (b) the reform-regime
   stratification, (c) the composition-beats-rate instrument. ~1 session of agent-draftable work
   + M.G. curation.
2. **"Three-tier law" overclaims from the sample.** Two of three regime cells contain one
   language each (RU n=1 dictionary; LA n=1), and the Latin zero is **overdetermined** — Latin is
   a fixed learned language, so its 0 is consistent with "no reform" but also with "no living
   orthographic community at all." The control shows the tool doesn't manufacture drift (good —
   keep that claim); it cannot by itself separate regime from language-vitality. Recommend:
   rename "law" → "three-regime stratification" throughout; add 3–4 lines in §9 naming the
   confound. Cheap fix, removes the paper's biggest attack surface.
3. **PW and PWG are not independent data points.** PW is Böhtlingk's abridgement of PWG — same
   lexicographer, same era, overlapping gloss text — yet both sit in the German gradient and in
   the ρ = −0.975 (n=5) correlation. A statistically-minded referee will catch this. Fix: state
   the dependence, report the correlation with and without PW (n=4), and frame all §5 statistics
   as case-study-scale, not corpus-scale inference.
4. **§4.4 "clean recency gradient" contradicts §5's own saturation finding** (7 English dicts at
   exactly 0.00 across 1890–1990). §5 is right; §4.4 oversells. Align: English gives an
   *upper-epoch bound* (nonzero drift ⇒ early), not a gradient — that's still a usable claim and
   it's honest.
5. **Denominator comparability.** "modern %" swings 42–65 % across the German five, so drift/1k
   is computed over differently-filtered token populations. One paragraph in §3.2 on what falls
   out of the denominator (names, Latin botanicals, fragments) and why the rate is nonetheless
   comparable — or a sensitivity note — is needed.
6. **No figures.** DSH expects visual argument. Two suffice: the existing
   [drift_dating.png](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ortho_drift/drift_dating.png)
   calibration plot, and a per-era composition stacked-bar (PW→SCH) that *shows* the era-flip —
   the paper's single most persuasive result, currently only a table.
7. **§7 must be resolved, and the right answer is the tight Kossovich case study.** Generalizing
   the pre-1918 protocol to a second Russian source is scope creep that delays Q4 submission for
   marginal gain; frame §7 as the extreme-regime case study and move on.

## Minor

- Abstract is ~200 words over a typical DSH cap once §2 exists; the "780× / 5×" parenthesis is
  referee-bait phrased as precision — consider "spanning nearly three orders of magnitude between
  regime extremes, narrowing to ~5× at the closest boundary."
- "long 19th century" (§1) now sits oddly against the corrected 1832–2009 span; adjust.
- Data-availability: the Hunspell local-dependency caveat is flagged in the header TODO — write
  the actual statement (incl. the 56,571-stem en_GB snapshot identity).
- Frontmatter venue line still lists IJL/JHP alternates; per the locked split this goes to DSH —
  update `venue:` and `readiness:` (now 3/5).

## What is genuinely strong — keep and foreground

The SCH-1928 era-flip (§4.2) is a textbook internal validation and should appear in the abstract
(it does) *and* as the closing figure. The honesty artifacts — the O3 map-expansion stress test
(rate inflates, composition survives), the O6 negative transfer result — are what will get this
past review; do not trim them for length. The guardrail framing (documentation layer, never a
corrector) will land well with DSH's digital-editions readership.

## Priority order

(1) → (2) → (4) are text-only and unblock submission; (3) and (5) each need one recomputation;
(6) needs one plotting session; (7) is a framing decision (recommended: case study). Realistic:
two working sessions + M.G. read-through to reach 4/5.

## Fixes applied (03-07-2026, Fable 5 `claude-fable-5`, H125/S15)

All agent-doable findings above were applied in one pass ([H125](https://github.com/gasyoun/Uprava/blob/main/handoffs/H125-Fable_SanskritSpellCheck_a37_fable_polish_03.07.26.md)):

- **Major 1** — §2 Related work WRITTEN, from verified literature only: normalisation
  (Baron & Rayson 2008 VARD2; Bollmann 2012 Norma; Bollmann 2019 survey; Jurish 2012
  DTA::CAB; Bawden et al. 2022 FreEM), stylochronometry/text-dating (Stamou 2008;
  Niculae et al. 2014), reform historiography (Johnson 2005; Comrie, Stone & Polinsky
  1996), metalanguage layer (Hausmann & Wiegand 1989). A full References section added
  (the paper had none). The FABLE-index comparanda suggestions "Haaf 2014 / Clérice
  2016 / Romanov 2019" could not be verified as apt and were NOT cited.
- **Major 2** — "three-tier law" renamed **three-regime stratification** throughout;
  the Latin regime-vs-vitality confound and the n=1 regime cells named in §9.
- **Major 3** — PW/PWG dependence stated in §5 with the without-PW sensitivity
  (n = 4, perfectly monotone, ρ = −1.00) and case-study-scale framing; the stale
  t-approximation p-values replaced by the exact/permutation values from the merged
  [#14](https://github.com/drdhaval2785/SanskritSpellCheck/pull/14) correction
  (German p = 0.033 exact; English p = 0.016 Monte-Carlo).
- **Major 4** — §4.4 reframed as an upper-epoch bound; the saturation is now stated
  in §4.4 itself, consistent with §5.
- **Major 5** — denominator-comparability paragraph added to §3.2.
- **Major 6** — figures wired: new committed
  [drift_composition.png](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ortho_drift/drift_composition.png)
  (per-era composition stacked bars, the SCH era-flip; generated from the §4.1 table,
  CVD-checked, grayscale-safe) as Figure 1 in §4.2, and the existing
  [drift_dating.png](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ortho_drift/drift_dating.png)
  referenced as Figure 2 in §5.
- **Major 7** — §7 fixed as the tight Kossovich case study (the open alternative
  removed).
- **Minors** — abstract "780×/5×" precision-bait rephrased; "long 19th century"
  aligned to the 1832–2009 span; data-availability statement written with the
  wordlist snapshot identities (de_DE 103,756 · ropensci en_GB 56,571 · fr_FR);
  frontmatter venue locked to DSH, readiness → 4/5.

Remaining gates are **author-only**: byline finalisation and the MG read-through.

_Review: Claude Fable 5 (`claude-fable-5`) · paper: Dr. Mārcis Gasūns_
