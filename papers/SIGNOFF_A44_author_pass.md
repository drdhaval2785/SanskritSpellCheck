# SIGNOFF — A44 author-voice pass

_Created: 10-07-2026 · Last updated: 06-09-2026_

Author-voice pass over [`papers/A44_body_grounded_triage_paper.md`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A44_body_grounded_triage_paper.md)
("The Dictionary Body as Ground Truth"), executed under handoff
[H047](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H047-Opus_SanskritSpellCheck_body_grounded_triage_26.06.26.md)
by Opus 4.8 (`claude-opus-4-8`) via the [`/paper-author-pass`](https://github.com/gasyoun/claude-config/blob/main/commands/paper-author-pass.md) skill.

This document exists so the bump to 5/5 costs a ~30-minute read rather than a full
reread. **No number, claim, or citation was changed in this pass** — verified
mechanically (every headline figure and all four in-text citations are token-identical
to `origin/master`). Everything substantive found mid-pass is parked below rather than
silently fixed.

---

## 1. Must-fix before submission — the References gate

The paper's own heading already says the References were drafted agent-side and need a
verification pass. That pass has now been *started*, not finished, and it surfaced two
defects. **Both are substance, so they were deliberately left in place for a human
ruling.**

### 1.1 🔴 Dangling citation — Artstein and Poesio 2008

§4.6 cites *"the category-definition effect the agreement literature warns about
(Artstein and Poesio 2008)"*, but **no such entry exists in the References list.** The
reference was present when the section was first drafted — the review memo
[`A44_review_fable5.md`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A44_review_fable5.md)
records a References section containing Artstein & Poesio 2008, Zgusta 1971,
Hausmann & Wiegand 1989, Atkins & Rundell 2008, and Patel & Kulkarni 2024. §2 was later
rewritten by the H452 prior-art scan and the list was pruned alongside it, stranding the
§4.6 citation.

Verified bibliographic entry, ready to paste:

> Artstein, R. and Poesio, M. (2008). Survey Article: Inter-Coder Agreement for
> Computational Linguistics. *Computational Linguistics* 34(4), 555–596.
> [https://doi.org/10.1162/coli.07-034-R2](https://doi.org/10.1162/coli.07-034-R2) ·
> [https://aclanthology.org/J08-4004/](https://aclanthology.org/J08-4004/)

**A human should decide** whether to restore only this entry (the minimum that makes the
paper internally consistent) or also the three lexicography references the review memo
lists (Zgusta 1971; Hausmann & Wiegand 1989; Atkins & Rundell 2008) — those are *not*
cited in the current text, so restoring them would require adding in-text citations too,
which is a substantive §2 edit outside a voice pass.

### 1.2 🔴 Citation to proceedings that do not yet exist — ISCLS 2026

The current entry reads:

> ISCLS (2026). Preserving what is written, not what is expected: the proof-reader
> effect of LLMs in Sanskrit OCR. *Proceedings of the International Sanskrit
> Computational Linguistics Symposium.* *(exact author list to be verified — ibid.)*

Two problems, both load-bearing for §2(b), which leans on this source for the
proof-reader-effect argument:

- The paper could not be located in any index. A targeted search returned nothing under
  the title, the phrase "proof-reader effect", or the ISCLS venue.
- **ISCLS 2026 has not happened.** The symposium was still issuing its
  [call for demos](https://iscls.github.io/cfd.html) as of this pass, so there are no
  2026 proceedings to cite. Citing them in an IJL submission is a referee-visible defect,
  and it is the *same class of error* the H452 prior-art scan already caught once in this
  paper (the "ISCLS 2024 contextual spellchecker" that did not exist — see
  [`docs/PRIOR_ART.md`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/PRIOR_ART.md) §7c).

Note that §2(b)'s *argument* does not depend on this particular paper — LLM
over-correction in historical-document OCR is independently documented, e.g.
[*OCR Error Post-Correction with LLMs in Historical Documents: No Free Lunches*](https://arxiv.org/abs/2502.01205)
(arXiv 2502.01205). **A human should decide** among: (a) substitute a real, published
citation for the claim; (b) keep the ISCLS item only if it is a real submission known to
the author, and cite it as *forthcoming* with an author list; (c) drop the citation and
state the proof-reader effect as this paper's own observation.

> ⚠️ Until 1.1 and 1.2 are ruled on, A44 is **not submittable**, regardless of readiness
> score. Neither defect affects any result: both sit in the related-work and
> discussion framing, not in the data path.

---

## 2. Voice calls made in this pass — each may be vetoed

All are register/typography only. Line references are to the post-pass file.

| # | Location | Change | Rationale |
|---|---|---|---|
| V1 | Frontmatter | `status`/`readiness` `3/5` → `4/5` | Bookkeeping sync: the file still declared 3/5 after §4.6 (the blind-annotator study) landed. [ARTICLES.md](https://github.com/gasyoun/Uprava/blob/main/ARTICLES.md) has recorded A44 as 4/5 since H453 merged. |
| V2 | Draft-status note | Rewrote the gate list | It numbered the References gate "(1)" and then called something else "the former gate (1)" — self-contradictory. Now: gates (1) References, (2) read-through; the discharged reliability gate is described in prose. |
| V3 | §4.6 | `**121/122 (99.2 %, binary κ = 0.663** … marginal**)**` → `**121/122 (99.2 %)**, with a binary κ of 0.663 …` | The bold delimiters nested illegally, so `κ = 0.663` rendered bold and the parenthetical broke. Typography; both numbers unchanged. |
| V4 | §4.2 | "— the paper's most lexicography-native result" (cut) | Coinage; the table's importance is argued two paragraphs later without it. |
| V5 | §4.2 | "Both numbers are reported deliberately" → "reported because they answer different questions"; "lexicographically telling" → "repays attention" | De-agentified; "deliberately" invited the reading that the two totals are an inconsistency being pre-excused. |
| V6 | §4.5 | "the triage's **celebrated** '4 fileable of 1,954'" → drops "celebrated"; "MW's headline restated **honestly**" → "restated" | Self-congratulation, and "honestly" implies the earlier statement was not. |
| V7 | §4.6 | "Two findings **earn their place in the contribution**." → "Two findings follow." | LLM-flavored framing. |
| V8 | throughout (5×) | `filable` → `fileable` | Not standard English; the spelling used in the handoff, the registry, and ARTICLES.md. Includes the §4.3 heading. |

**Considered and declined:** flipping the editorial "we" to first-person singular for the
sole-author byline. IJL prints both; "we" is idiomatic in the lexicography and CL
literature this paper sits in, and a 20-instance flip is a bigger register change than a
voice pass should impose unasked. Raise it if you want it.

---

## 3. Standing flags carried over (not raised by this pass)

- **§4.6 "pre-registered binary collapse."** The word *pre-registered* is a claim about
  study design. If the binary collapse was specified before the blind run, it is a
  strong claim worth keeping and worth stating where it was registered; if it was
  chosen after seeing the five-way confusion matrix, a referee will treat "pre-registered"
  as overreach. Untouched — outside a voice pass.
- **The `*(References drafted agent-side …)*` markers** in the §2 tail and the References
  heading are workflow scaffolding, not manuscript text. Strip both at submission.
- **§6 limitation stands as written:** the reliability figure is model-vs-model, not human
  IRR. That is per ruling D2 and is already stated honestly; no action.

---

## 4. Read-and-sign

1. Rule on **§1.1** (restore Artstein & Poesio; decide on the three lexicography refs).
2. Rule on **§1.2** (substitute / mark forthcoming / drop the ISCLS 2026 citation).
3. Skim **§2** and veto any voice call you dislike.
4. Read the manuscript once end-to-end for IJL register.
5. On sign-off, bump A44 to **5/5** in
   [`Uprava/ARTICLES.md`](https://github.com/gasyoun/Uprava/blob/main/ARTICLES.md) and
   strip the scaffolding markers in §3.

Steps 1–2 are the only true blockers; 3–4 are register.

---

## Pass 2 — 06-09-2026 (Fable 5.1 `claude-fable-5-1`)

Second author-voice pass over [`papers/A44_body_grounded_triage_paper.md`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A44_body_grounded_triage_paper.md)
under handoff [H3857](https://github.com/gasyoun/Uprava/blob/main/handoffs/H3857-Fable_Uprava_all-articles-author-voice-pass-workflow_01.09.26.md) (all-articles author-voice pass workflow), Fable 5.1
(`claude-fable-5-1`), 06-09-2026. Scope: voice, register and framing only; no
number, claim or citation altered; mechanical drift gate
([`voice_drift_check.py`](https://github.com/gasyoun/Uprava/blob/main/tools/voice_drift_check.py)
against `origin/master`) **CLEAN** — 456 numbers, 66 URLs, 2 bracketed citations,
21 IAST and 9 Devanagari tokens, 24 headings and 50 table rows count-identical.
Pass-1 calls V1–V8 above were found applied and are untouched; this section lists
only what pass 2 changed or found.

### 1. Voice calls made — each may be vetoed

| # | Location | Call | Rationale |
|---|---|---|---|
| P2-1 | Abstract | "the system detects and triages, it does not auto-correct" → "detects and triages but does not auto-correct" | Comma splice; the clause already sits after a semicolon. Same claim, same strength. |
| P2-2 | §1, GED paragraph | "And the system reported here sits squarely on the *detection* side" → "The system reported here sits on the *detection* side" | Sentence-initial "And" plus the filler intensifier "squarely"; the sentence is a direct claim and reads as one without either. |
| P2-3 | §2(a) | "No tool in the surveyed landscape models…" → "No tool in the survey models…" | "landscape" is on the de-AI list; the survey is the named document ([docs/PRIOR_ART.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/PRIOR_ART.md)), so the plain noun is also more exact. |
| P2-4 | §2 | One 66-line paragraph split into four at the existing bold run-in labels **(a)**–**(d)** | Paragraph breaks only; no word changed. A single-paragraph related-work section is hard to referee in the IJL two-column proof. Heading count unchanged (labels stay run-in bold, not headings). |
| P2-5 | §2(d) | "it flags and triages, it never auto-corrects" → "it flags and triages but never auto-corrects" | Comma splice inside an em-dash parenthetical; "never" kept. |
| P2-6 | §4.6 | "the position argued for annotator label variation generally by Plank (2022)" → "the position Plank (2022) argues for annotator label variation generally" | Word order; the passive with a trailing agent read as a machine sentence. Citation form unchanged. |
| P2-7 | §4.6 | "never once rejected" → "never rejected" | Intensifier; "never" carries the full strength. |
| P2-8 | §4.7 | "A naive auto-apply pipeline **celebrating** its 99 % recall" → "reporting 99 % recall" | Same fix pass 1 made in §4.5 (V6, "celebrated"): a personified pipeline is decoration; the number and the consequence clause are unchanged. |
| P2-9 | §5 run-in heading | "**Filable rate** as a digitisation-quality signal" → "**Fileable rate**" | Pass 1's V8 normalised `filable` → `fileable` five times but missed this bold run-in heading; the sentence under it already says "fileable rate". |
| P2-10 | §1, §4.5 | "naïvely" / "naïve" → "naively" / "naive" | §4.7 already uses the undotted form twice; one spelling throughout. |
| P2-11 | §6, second bullet | Continuation line "agreement — the binary κ is not printed…" given the bullet's two-space indent | Markdown hygiene: the line broke out of the list item in some renderers. No text changed. |
| P2-12 | §4.2, Data and reproducibility (4×) | "artifact(s)" → "artefact(s)" | The paper is otherwise in Oxford spelling (digitised, catalogue, labelled, analogue, modelling); IJL is an OUP journal. Easily vetoed if the author prefers the American form. |
| P2-13 | Header, frontmatter `status`, draft-status note | `Last updated` → 06-09-2026; "author-voice pass 2 2026-09-06 (SIGNOFF_A44_author_pass.md)" prepended to `status`; one blockquote paragraph naming this pass and linking this signoff | Bookkeeping the brief requires; no other note added anywhere. |

**Considered and declined (still open for a ruling).**

1. Editorial "we" → "I". Seven instances remain ("We report", "We quantify", "Our claims", "We are not aware", "We have observed", "we state them separately", "we print the raw count"). Pass 1 declined the flip and asked for a ruling; none is recorded, so pass 2 leaves it. IJL prints both forms for single-author papers; the flip is a five-minute mechanical edit once ruled.
2. §4.7 "This is not a separate result from the paper's thesis; it is that thesis measured." The "not X; it is Y" pattern is on the de-AI list, but here it is the paper's own claim stated at full strength; rewriting it would touch framing, not register.
3. §4.6 "are not noise but signal" — same pattern, but it paraphrases Plank (2022)'s title thesis exactly; left.

### 2. Substance flags carried (not fixed)

1. **YAT rate inconsistency.** The Abstract, claim 3 in §1 and §7 all say "YAT ≈ 11 %", but the §4.3 table gives YAT 27 / 219 = 12.3 %. The ≈ 11 % survives from the earlier denominator (27 / 247 = 10.9 %) that §4.3 itself retires as "not reproducible from anything committed". A human should decide whether the three prose figures become ≈ 12 % (matching the pinned denominator) — a number change, outside a voice pass.
2. **§5 "precision and harm rise together".** Table 4 shows the union's *recall* (99.1 %) and harm (13/13) rising together; the union's precision (89.2 %) is below `spell_correct`'s (91.2 %). "precision" here looks like a slip for "recall". A one-word substance fix, flagged not made.
3. **§4.7 "range across the seven flag-raising detectors".** Table 4 lists three flag-raising detectors plus the union (and the degenerate `dict_vs_corpus`); the text never says where "seven" comes from. Either the table is a subset of `eval.py`'s detector list (say so in the caption) or the count is stale.
4. **Table numbering.** The manuscript captions only Table 2a, Table 2b and Table 4; the §4.1, §4.3 and §4.5 tables carry no caption and no number, and there is no Table 1 or Table 3. IJL will want a full sequence. Table references are untouchable in a voice pass.
5. **Header `_Created: 10-08-2026_`** postdates the paper's own history (H047 first draft 26-06-2026; review 02-07-2026; pass 1 10-07-2026). Dates are a hard limit for this pass; a human should correct the creation date.
6. **Relative links that die outside the repo tree.** §3.2 `[detectors/combined_candidates.txt](../detectors/combined_candidates.txt)` points at a file §4.3 says is gitignored; §4.6 `../corrections_draft/irr/`, Appendix A `../detectors/` and `../corrections_draft/` are relative paths. URLs are a hard limit for this pass; they need full blob URLs (or removal) before the anonymised pack is built.
7. **Scaffolding still in the manuscript body** (carried from pass 1 §3): the §2 tail parenthetical "*(Every References URL was resolved…)*", the parenthetical in the References heading, the "*(Removed 12-07-2026: …)*" note after the References, the "*(Verified 10-07-2026 by the H452 prior-art scan…)*" note inside the Prasanna entry, and the whole draft-status blockquote. All are workflow text, not manuscript text; strip at submission.
8. **Forward-looking promises that age.** §4.6 "pending an API credential; its κ will be reported as obtained" and §6 "soon two model *families*, once the pending cross-family run of §4.6 completes" have stood since 12-07-2026. Either the cross-family run lands before submission or these become plain "future work" sentences.
9. **Pass 1 flag on "pre-registered binary collapse" is resolved** — the word no longer appears in §4.6; nothing to carry.
10. **Derived submission pack.** The anonymised IJL pack (`A44_ijl_*.md`, cover letter) is generated from this manuscript by `build_a44_anonymous.py` and was deliberately not touched; it must be regenerated after this branch merges, or the pack and the manuscript diverge on P2-1…P2-12. (Neither the pack files nor the build script are on `origin/master` at the time of this pass — they live in another checkout; whoever holds them re-runs the build.)

### 3. Read-and-sign

About 30 minutes: skim the thirteen calls in §1 and veto any; rule on flags 1–3 (each is a one-token substance fix a voice pass may not make); strip the scaffolding in flag 7 at submission time. Proposed readiness: **stays 4/5** — the manuscript is voice-clean, but flags 1–3 are referee-visible arithmetic and the "we/I" question is unruled; the 5/5 bump is the author's to make after those. Venue: no change recommended — IJL remains the right home (the do-not-file inversion and the apparatus taxonomy are its native material). Submission itself stays frozen until 2026-11-01 per the standing rule.

_Dr. Mārcis Gasūns_
