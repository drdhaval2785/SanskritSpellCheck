# SIGNOFF — A37 author-voice pass

_Created: 11-07-2026 · Last updated: 11-07-2026_

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

_Dr. Mārcis Gasūns_
