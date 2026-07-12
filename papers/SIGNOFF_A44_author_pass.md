# SIGNOFF — A44 author-voice pass

_Created: 10-07-2026 · Last updated: 10-07-2026_

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

_Dr. Mārcis Gasūns_
