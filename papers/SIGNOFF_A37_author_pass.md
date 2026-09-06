# SIGNOFF — A37 author-voice pass

_Created: 11-07-2026 · Last updated: 06-09-2026_

Author-voice pass over [`papers/A37_ortho_drift_paper.md`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A37_ortho_drift_paper.md)
("Reading the Reform off the Gloss"), executed under handoff
[H678](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H678-Fable_SanskritSpellCheck_a37-ortho-drift-author-pass_11.07.26.md)
by Fable 5 (`claude-fable-5`) via the [`/paper-author-pass`](https://github.com/gasyoun/claude-config/blob/main/commands/paper-author-pass.md) skill.

This document exists so the bump to 5/5 costs a ~30-minute read rather than a full
reread. **No number, claim, or citation was changed in this pass** — verified
mechanically against `origin/master` (numeral and citation-token multiset diff; every
residual difference is the status-date bookkeeping, the two stripped internal heading
codes V9, or digits inside newly-added full URLs). Unlike the
[A44 pass](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/SIGNOFF_A44_author_pass.md),
**no substantive defect surfaced**: all eleven in-text citations resolve to References
entries and every References entry is cited in the text (checked both directions), and
the References list was already written from verified literature in the
[H125 referee-fix pass](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A37_review_fable5.md).

---

## 1. The byline gate — discharged, confirm on read-through

The draft-status note listed "finalise byline" as an open author-only gate. The
frontmatter byline already matches the canonical author identity **verbatim** —
Mārcis Gasūns, independent scholar, [ORCID 0000-0003-4513-884X](https://orcid.org/0000-0003-4513-884X),
gasyoun@ya.ru — the same identity block used for the A25 submission. The pass
therefore rewrote the gate list to leave **read-through + sign-off as the only open
gate**. Nothing to fix; confirm the byline stands when you sign.

---

## 2. Voice calls made in this pass — each may be vetoed

All are register/typography/alignment only. Locations reference the post-pass file.

| # | Location | Change | Rationale |
|---|---|---|---|
| V1 | Frontmatter | `status` → "author pass executed 2026-07-11, pending MG read-and-sign" | Bookkeeping sync; readiness stays 4/5 — the bump to 5/5 waits for the sign-off. |
| V2 | Draft-status note | Gate list rewritten: byline gate recorded as discharged (§1 above); remaining gate = read-through + sign-off | The note still requested byline finalisation already satisfied by the frontmatter. |
| V3 | Abstract | "magnitude and composition … **is** governed" → "**are** governed"; "Measuring drift …, drift rates fall" → "Measured against …, drift rates fall"; scope now reads "— the Cologne Digital Sanskrit Dictionaries and one external pre-revolutionary Russian source —" | Two grammar fixes (compound subject; dangling modifier), and an abstract/body alignment: the abstract placed all five gloss languages inside Cologne, while §4.3 and §9 state the Russian source is external to the Cologne 33. All figures verbatim. |
| V4 | §3.1 heading | "Corpus and the key insight" → "Corpus and the measured channel" | Self-promotional heading; now echoes §2's own phrase "the channel measured here". |
| V5 | §3.2 | "*iff*" → "only if" | Mathematical shorthand out of register for DSH prose; the sentence states an acceptance criterion, so the one-directional "only if" is also the more precise word. |
| V6 | §4.3 heading | "the dramatic case" → "the extreme case" | Journalistic; aligns with §7's own "extreme-regime instance" framing. |
| V7 | §5 | "Two caveats keep this honest:" → "Two caveats qualify this:" | Self-attributed honesty (the A44-pass precedent: cut "honestly"/"celebrated"). |
| V8 | §5 | "**Verdict:**" → "**In sum:**" | Referee-register word inside the author's own results section. |
| V9 | §5/§6 headings | Internal objective codes "(O4)" / "(O6 — …)" stripped | Study-plan IDs from [docs/ORTHO_DRIFT_FINDINGS.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/ORTHO_DRIFT_FINDINGS.md), unexplained to a DSH referee; the codes survive in the findings doc, so traceability is not lost. |
| V10 | §7 heading + draft-status note | "digitization" → "digitisation" | Spelling consistency — the manuscript is otherwise uniformly -ise- (normalisation, digitising). |
| V11 | §2 | "most completely Prasanna (2022)" → "most comprehensively" | Idiom; citation untouched. |
| V12 | §10 | "how strongly is governed" → "how strongly it does so is governed" | Grammar. |
| V13 | §2, §3.2 | Two relative links (`../docs/PRIOR_ART.md`, `../detectors/ortho_drift.py`) → full blob URLs | Committed-Markdown link contract; the rest of the paper already uses full URLs. |

**Considered and declined:**

- **Editorial "we" for the sole-author byline.** Same call as the A44 pass: DSH prints
  both, "we" is idiomatic in the DH literature this paper cites, and a 20-instance flip
  is a bigger register change than a voice pass should impose unasked. Raise it if you
  want first-person singular.
- **Title's "19th–20th-Century" vs the 1832–2009 span.** Every dictionary the method
  actually *dates* (non-zero drift) is 19th–early-20th-century; the 21st-century sources
  enter only as zero-drift recency controls (§4.4). The title is accurate about the
  dated objects, so it stands.
- **Bold markup inside the abstract.** Submission typesetting will strip it; not worth
  churn now.

---

## 3. Standing flags carried over (not raised by this pass)

Strip-at-submission scaffolding — none of it blocks the read-through:

- The **draft-status blockquote** under the title (internal status record).
- The **"(draft — author to finalise)"** marker on the References heading. The list was
  written from verified literature (H125) and re-checked both directions in this pass;
  after your read-through a human should decide the marker has served its purpose and drop it.
- The **§7 provenance parenthetical** "*(folds the former standalone «Орфография как
  датирующий признак» idea)*" — workflow history, not manuscript text.

No action needed on the Hunspell local-dependency caveat — §9 and the
data-availability statement already state it honestly.

---

## 4. Read-and-sign

1. Skim **§2** and veto any voice call you dislike.
2. Read the manuscript once end-to-end for DSH register (~30 min).
3. Confirm the byline (§1) stands.
4. On sign-off, bump A37 to **5/5** in
   [`Uprava/ARTICLES.md`](https://github.com/gasyoun/Uprava/blob/main/ARTICLES.md) and
   strip the §3 scaffolding at submission.

No true blockers — steps 1–3 are register; step 4 is the bump itself.

---

## Pass 2 — 06-09-2026 (Fable 5.1 `claude-fable-5-1`)

Second author-voice pass over [`papers/A37_ortho_drift_paper.md`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A37_ortho_drift_paper.md) under
handoff [H3857](https://github.com/gasyoun/Uprava/blob/main/handoffs/H3857-Fable_Uprava_all-articles-author-voice-pass-workflow_01.09.26.md) (Fable 5.1 `claude-fable-5-1`, 06-09-2026), on top of the
pass-1 calls above, which stand. Voice, register and framing only; no number, claim
or citation altered; mechanical drift gate CLEAN (`voice_drift_check.py --git
origin/master`: numbers 437 = 437, URLs 23 = 23, DOIs 2 = 2, citations 6 = 6, IAST
4 = 4, headings 25 = 25, table rows 18 = 18). What this pass found was mostly
residue of the 13-07-2026 ACL-Anthology uplift (H826), which landed after pass 1
and re-introduced several of the patterns pass 1 had removed.

### 1. Voice calls made — each may be vetoed

Locations reference the post-pass file.

| # | Location | Call | Rationale |
|---|---|---|---|
| P2-1 | Abstract | Four-em-dash sentence ("… (1832–2009) — the Cologne … — drift rates fall into three sharply separated tiers — **legislated** … — spanning …") split: commas around the corpus apposition, a colon before the three tiers, and "spanning … narrowing" made its own sentence ("The tiers span … and narrow to …") | Em-dash chain; the reader lost the main clause. Every figure verbatim. |
| P2-2 | Abstract | "The contribution is not a new historical-spelling normaliser — that is a mature subfield — but the application of …" → "The contribution is the application of an existing, mature technique, historical-spelling normalisation, to a … corpus, … ; no new normaliser is proposed." | The "not X, but Y" frame; the positive contribution now leads. Same claim, same scope. |
| P2-3 | §1 | "(the fits and dated series consume 24 of the 33 plus one external Russian, Kossovich — see the per-language n values)" → "(… draw on 24 of the 33, plus one external Russian source, Kossovich; the per-language n values are given below)" | Telegram parenthetical ("consume", a dangling "see"). |
| P2-4 | §2, ¶3 | "… — and cite Ren, Wang, Zhao and Ren (2023) … against which A37's interpretability … is the relative advantage" → new sentence: "Ren, Wang, Zhao and Ren (2023), a black-box language-model dater, is cited as the contrast: against it, this paper's interpretability … is the relative advantage, not raw accuracy at scale." | The manuscript referred to itself by its internal registry ID "A37" — a referee cannot read that; and the 90-word sentence was a run-on. Citation untouched. |
| P2-5 | §2, ¶3–4 | "Finally, graphemic variation …" → "Graphemic variation …"; "Lexicographic theory, finally, has long …" → "Lexicographic theory has long …" | Three "finally" in one section (the third, opening the Prasanna paragraph, is the real last and stays). |
| P2-6 | §2, ¶6 | "maps that landscape" → "surveys that work" | "landscape" is on the de-AI list; date and link untouched. |
| P2-7 | §3.2 | "Implementation: one profile-driven tool, …, one profile per language" → "The implementation is a single profile-driven tool, …, with one profile per language" | Telegram syntax, dropped verb. |
| P2-8 | §3.3 | "**never a correction list** — modernising …" → "**never a correction list**: modernising …" | Em-dash as copula. |
| P2-9 | §4.2 | "The method does not merely count drift; it correctly dates …" → "Beyond counting drift, the method correctly dates …" | "not merely X; Y" frame. |
| P2-10 | §4.3 | "Source: SamudraManthanam `kossovich.jsonl` — external to the Cologne 33." → "The source is SamudraManthanam's `kossovich.jsonl`, external to the Cologne 33." | Telegram syntax. |
| P2-11 | §4.6 | "the tool — correctly — manufactures none. This confirms the method's specificity." → "the tool, correctly, manufactures none, which confirms the method's specificity." | Em-dash parenthetical around a single adverb. |
| P2-12 | §4.8 heading, §5 heading, §5 SemEval lead | ~~Internal objective codes "(O7a)", "(O4, O7b)", "(O7b)" stripped from the headings and the run-in lead~~ — **reverted after adversarial verify:** provenance tags to [ORTHO_DRIFT_FINDINGS.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/ORTHO_DRIFT_FINDINGS.md) are references, not voice. All three restored verbatim: "### 4.8 S-curve exo/endo fit (O7a) — …", "## 5. Can drift date a dictionary? (O4, O7b)", and the SemEval lead "… terms (O7b)**, so the dater …". No other O-code tag had been removed. | Same call as pass-1 V9; the codes came back with the H826 uplift. Three independent verifiers read the tags as observation-ID cross-references to the pinned data source, so their removal is a substance change, not a register change. Heading count unchanged (25 = 25). |
| P2-13 | §4.8 | "… pre-reform proxy dispersion — we surface this as a transferable caution …" → "… pre-reform proxy dispersion. We report this as a transferable caution …"; the stray one-word line "A" rejoined to its sentence | Run-on joined by an em-dash; "surface" is workflow jargon. |
| P2-14 | §5 | The four-bullet results list re-set as four prose paragraphs; bold run-in leads kept as topic sentences; "**no cross-language calibration** — the rate …" → "There is **no cross-language calibration**: the rate …"; "…, Δt80 = 54.6, R² = 0.84) — PW is both …" → "…), since PW is both …" | A results section written as a bullet sheet, each bullet a paragraph long; DSH prints prose. Every number, p-value and n verbatim; the (Figure 2) reference and both links in place. **Partially reverted after adversarial verify:** the fourth item (the SemEval-2015 re-report) is restored verbatim in its original bullet form, "(O7b)" tag, "so the dater" wording and colon included, because the P2-12 revert covers that span; the first three items stay as prose. |
| P2-15 | §5, ¶2 | "the earlier print claimed Spearman ρ … = −0.975" → "an earlier version of this analysis reported Spearman ρ … = −0.975" | "print" is wrong (nothing was printed) and "claimed" over-dramatises a recomputation. The retraction itself is untouched — see flag 3 below. |
| P2-16 | §5, "In sum" | "the **per-era composition** is the robust instrument and survives a 5.5× …" → "is the instrument that holds: it survives a 5.5× …" | "robust" is on the de-AI list. |
| P2-17 | Frontmatter `status`, draft-status note, header | `status` → "author passes executed 2026-07-11 and 2026-09-06, pending MG read-and-sign"; one line added to the draft-status blockquote naming this pass and this section; `Last updated` → 06-09-2026 | Bookkeeping sync; readiness stays 4/5. |

**Considered and declined (again):**

- **Editorial "we" → "I".** Declined in pass 1 and left alone here for the same reason: a
  20-plus-instance register flip is not a voice-pass call to make unasked. The handoff's
  preference for first-person singular is noted; a human should decide, and if the
  answer is yes the flip is a fifteen-minute mechanical pass.
- **Bold run-in sentences opening each §2 paragraph.** Typesetting will strip them; not
  worth the churn.
- **§9 Limitations as a bullet list.** Acceptable in DSH; the §5 list was the defect
  (results, not caveats).

### 2. Substance flags carried (not fixed)

None of these was touched — each is a claim, a token or a reference entry, so under
the pass rules it is a flag, not a fix.

1. **§4.8 still argues with the old PW date.** The adversarial-refit sentence reads
   "PW 0.000 vs PWG 0.1365 in the same year 1865", while the table row above it says
   "PW ≈ 1884 refit" and §4.1/§5 re-date PW to its own 1879–1889 print run. Either the
   sentence describes the pre-refit run (then say so) or the dispersion argument needs
   restating on the ≈1884 dating. A referee who reads §4.1 and §4.8 together will see it.
2. **§4.2 "ß-dominant" vs §5 "`ss`-dominant".** The same SCH-1928 signature is named by
   the drifted form in one place and by the modern target in the other. One name should
   win; the §4.1 column header is "1996 `ß`".
3. **§5 carries its own revision history.** The −0.975 → −0.70 retraction narrative
   ("an earlier version of this analysis reported …") is a changelog inside a results
   section. A human should decide whether the manuscript reports only the corrected
   series (with the PW dependence argument, which is the substantive point) and moves
   the retraction to the findings doc, or keeps it as a transparency note.
4. **§5 German LOO bands (80 % within ±25 yr, n = 5) include PW**, which the same
   section calls the indefensible point; no n = 4 leave-one-out figure is reported.
   Minor, but the two statements sit ten lines apart.
5. **Bollmann 2019 reference entry** carries an internal aside, "(§O7b/data-and-method)",
   and a sentence about the histnorm repository that belongs in the body or nowhere.
   Reference entries are untouchable for this pass; strip at finalisation.
6. **§1 "four European metalanguages" vs abstract "five gloss languages".** Consistent
   once the reader knows Russian is external to Cologne, which §1 says only in a
   parenthesis. Consider "four European metalanguages within Cologne, five with the
   external Russian source".
7. **§4.5 French is one line.** A DSH referee may ask for a sentence of context on
   why two dictionaries suffice for a "convention, minimal" verdict.
8. **Carried from pass 1, unchanged:** the draft-status blockquote; the References
   heading marker "(draft — author to finalise)"; the §7 provenance parenthetical
   "*(folds the former standalone «Орфография как датирующий признак» idea)*". All
   strip-at-submission.

### 3. Read-and-sign

1. Skim the P2 table above and veto any call you dislike (~10 min).
2. Rule on flags 1–3 (~15 min); 4–7 are optional polish.
3. Read the abstract, §2 and §5 once end-to-end for DSH register (~10 min).
4. Proposed readiness: **stays 4/5** until the sign-off; the bump to 5/5 is the sign-off
   itself (propose only). Venue: **DSH stays** — nothing in this pass argues against the
   locked split; the LChange companion covers the S-curve finding separately.
5. No submission action until the 2026-11-01 freeze lifts.

_Dr. Mārcis Gasūns_
