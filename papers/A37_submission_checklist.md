# A37 — *DSH* submission checklist

_Created: 10-08-2026 · Last updated: 10-08-2026_

Venue requirements for **A37**, [A37_ortho_drift_paper.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A37_ortho_drift_paper.md)
("Reading the Reform off the Gloss"), target **Digital Scholarship in the Humanities**
(Oxford University Press). Assembled under [H2406](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2406-Fable_SanskritSpellCheck_a37-plus5-camera-ready-pack_07.08.26.md)
via [/paper-submission-pack](https://github.com/gasyoun/claude-config/blob/main/commands/paper-submission-pack.md).

**Guidelines source:** [academic.oup.com/dsh/pages/General_Instructions](https://academic.oup.com/dsh/pages/General_Instructions),
fetched **10-08-2026**. Unlike the *IJL* page used for A44 (pack in flight under
[H2407](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2407-Fable_SanskritSpellCheck_a44-plus5-camera-ready-pack_07.08.26.md)),
DSH publishes its numeric limits, so almost every row below is verified rather than
UNVERIFIED. The two exceptions (peer-review anonymity model, ORCID handling) are genuinely
absent from the page and are marked ❓ — not guessed.

## Status legend

✅ satisfied · ⚠️ needs work · 🔴 blocker · ❓ UNVERIFIED (requirement not published) · ⟦MG⟧ human decision

## Measured against the manuscript

| Metric | Value | Limit | Verdict |
|---|---|---|---|
| Body (Abstract → §10 + Data availability) | **3,143 words** | 9,000 (full paper), "exclusive of notes and references" | ✅ well inside |
| Whole file incl. frontmatter, draft blockquote, References | 4,053 words | — | — |
| Abstract | **246 words** | **250 max** | ⚠️ inside the cap, but **unstructured** — the real failure is #2 |
| References | 18 entries, ~484 words | not counted toward the limit | ✅ |
| Figures | **1** (`ortho_drift/drift_composition.png`, 1420×812 px, 200 dpi) | ≥300 dpi | 🔴 under-resolution (see #5) |
| Tables | 15 Markdown table rows across the results sections | — | typesetting only |
| Keywords | **none** | up to 12 | ⚠️ (see #3) |

## Manuscript requirements

| # | Requirement | Status | Where / what remains |
|---|---|---|---|
| 1 | **Word limit** — full papers "normally up to 9,000 words, exclusive of notes and references"; shorter articles 5,000 | ✅ | Body is ~3,143 words. Length is a non-issue; if anything the paper is short for the full-paper class — see ⟦MG⟧ decision #4 in the [cover letter](https://github.com/gasyoun/SanskritSpellCheck/blob/master/papers/A37_cover_letter.md). |
| 2 | **Structured abstract, 250 words max, five mandatory sub-headings** — Purpose; Design/methodology/approach; Findings; Originality; Contribution to the field of Digital Humanities | 🔴 | The current abstract is a **single 246-word narrative paragraph with no sub-headings**. Length is *not* the problem — it is 4 words inside the cap. The problem is structure: it must be rewritten into the five mandatory sections. Since sub-headings themselves consume words, budget a ~30–50-word prose cut to stay under 250 once they are added. Three optional sub-headings (research limitations/implications, practical, social) may follow. |
| 3 | **Keywords — up to 12 short keywords** | ⚠️ | The manuscript has no keywords line. Add one; the in-house team may substitute matching terms for discoverability. Suggested: *historical spelling variation; orthographic reform; spelling normalisation; metalanguage; historical lexicography; Sanskrit dictionaries; Cologne Digital Sanskrit Dictionaries; corpus dating; German orthographic reform; Russian orthographic reform 1918; digital philology*. |
| 4 | **Reference style — "Oxford HUMSOC style"** (downloadable style checklist on the journal page); LaTeX uses author–year via `\bibliographystyle{abbrvnat}`; data and software **cited in the reference list**; end-matter order Notes → References → Appendices | ⚠️ | The 18 References entries are in a house author–date form close to but not verified against HUMSOC (title casing, publisher/place punctuation, DOI form). One mechanical conversion pass needed against the downloadable checklist. Separately: the detector, the drift tables, and the Hunspell word-lists are currently cited only in prose and full URLs — HUMSOC wants **data and software in the reference list**, so they need proper entries. |
| 5 | **Figures ≥300 dpi**, uploaded as **separate files** (embedded figures are "for peer review purposes only"), EPS for vector / TIFF for bitmap, captions as a separate grouped list not typed on the artwork, "Figure" contracted to *Fig.*, DOS-style filenames (`figure1.tif`) | 🔴 | `ortho_drift/drift_composition.png` is **1420×812 px at 200 dpi — below the 300 dpi floor**, and it is a PNG referenced inline by URL, which is not an accepted artwork format. Regenerate from the plotting source at ≥300 dpi (photographic content 300; line art with grey 600 is the journal's optimum for this figure type), export TIFF, rename `figure1.tif`, upload separately, and move the caption into a grouped caption list. |
| 6 | **Alt text — mandatory for all images**, placed in the main manuscript file directly beneath the figure legend, prefixed "Alt text:" | 🔴 | Figure 1 has a descriptive Markdown alt attribute but **no "Alt text:" line beneath the legend** in the journal's required form. Mechanical to add; mandatory, so it is a blocker rather than a note. |
| 7 | **Funding statement** — own end-matter section headed "Funding", opening "This work was supported by …", full official funder names, grant numbers in square brackets | 🔴 ⟦MG⟧ | The manuscript has **no Funding section**. Blocker until ⟦MG⟧ confirms the wording (presumed no external funding). Same gap as A44 checklist #9. |
| 8 | **Data availability — mandatory** end-matter statement under "Data availability", describing access and linking to the data or giving a unique identifier | ⚠️ | Substance is already there and unusually strong: the *Data and reproducibility* section names the synthesis doc, the detector, the committed `ortho_drift/` tables, the exact Hunspell snapshot identities, and states honestly that the modern word-lists are an uncommitted local dependency for licensing reasons. What remains is **formal**: rename the section to the journal's exact heading "Data availability", place it in the end matter in the prescribed order, and decide whether to give a unique identifier (DOI) — see #12. |
| 9 | **AI Disclosure Statement — required** in the end matter *and* a note in the cover letter; name tool and version, describe purpose and extent, confirm the authors verified all generated content; AI tools cannot be authors | 🔴 | **No AI Disclosure Statement exists in the manuscript.** This is a hard requirement and A37 unambiguously triggers it: the referee-fix, author-voice, and ACL-uplift passes were model-executed and are recorded in [A37_review_fable5.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A37_review_fable5.md) and [SIGNOFF_A37_author_pass.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/SIGNOFF_A37_author_pass.md). The statement must distinguish drafting/revision (model-assisted) from the measurements (deterministic detector, no model involved) — that distinction is the paper's credibility, so state it precisely. The cover-letter half is already drafted. |
| 10 | **Permissions** for any third-party material — no word threshold given; needed for quotes, tables, figures, images, data, **and software** | ⚠️ | No prose extract is substantial and the dictionary sources are public-domain 19th–20th-c. editions, so quotation raises nothing. The live question is the **Hunspell word-lists**: they are third-party software/data read as input and deliberately not redistributed. Confirm that citing without redistributing needs no grant (it should not, as nothing is reproduced in the article), and keep the non-redistribution reasoning visible in the Data availability statement. |
| 11 | **File format** — Word `.doc` preferred; `.pdf`, `.rtf`, `.ps` accepted; LaTeX welcome with the OUP general template (article class, Modern design, Medium page size, double column, `numsec`, author–year) plus a PDF for review; **no page or line numbers** (the system adds them) | ⚠️ | The manuscript is Markdown. Convert (`pandoc papers/A37_ortho_drift_paper.md -o A37_submission.docx`) or typeset in the OUP LaTeX template; the Markdown stays canonical. Text and figures upload as **separate** files. |
| 12 | **Dataset / software references** + optional unique identifier for the data statement | ⚠️ ⟦MG⟧ | HUMSOC wants data and software in the reference list (#4), and the mandatory data statement invites a unique identifier. Both point the same way: minting a Zenodo DOI for the `ortho_drift/` tables plus detector would satisfy them cleanly. That is a ⟦MG⟧ decision — it commits to a DOI and changes the reference list. A placeholder DOI is never supplied. |
| 13 | **Peer-review anonymity model** | ❓ | **Not stated on the instructions page** — the page describes editor and reviewer comments but names no single- or double-anonymous model. This matters concretely: the manuscript carries a **named byline with ORCID and email in the frontmatter** and cites the author's own repositories by full URL throughout, so if review turns out to be anonymous, both are disclosure defects requiring a separate blinded file. Resolve from the ScholarOne submission form or by asking the editorial office **before** upload. |
| 14 | **ORCID** | ❓ | Not mentioned anywhere on the instructions page. The byline carries [0000-0003-4513-884X](https://orcid.org/0000-0003-4513-884X) per [AUTHOR.md](https://github.com/gasyoun/Uprava/blob/main/AUTHOR.md); supply it in the ScholarOne profile if the form offers the field. Nothing to fix. |
| 15 | **Conflict of interest** | ✅ | No general COI section on the page (only Letters/Responses are asked to disclose). Declared nil in the cover letter. |
| 16 | **Copyright / licence** | ✅ post-acceptance | Publication is conditional on assigning an exclusive licence to OUP; the online form is completed after the accepted manuscript reaches Oxford Journals, where the open-access choice (and any Read-and-Publish coverage) is also made. Nothing to do at submission. |
| 17 | **Colour figures** | ✅ | £350 per figure in print; **online-only colour with black-and-white print is free**, selected during submission. Figure 1 is a composition chart — take the free online-colour option, and check it remains legible in greyscale. |
| 18 | **Language** | ✅ | English only; language editing at the author's expense. The manuscript is uniformly -ise- British spelling (V10 in the signoff). |
| 19 | **Submission portal** | ✅ | ScholarOne: [mc.manuscriptcentral.com/dsh](http://mc.manuscriptcentral.com/dsh) — submit from the corresponding author's own account; do not create a duplicate. Before starting, have ready: manuscript file, image files, supplementary material, abstract text, author names and emails. |
| 20 | **Proofs** | ✅ FYI | Corrections due within **three days** of the emailed proof link. Post-acceptance, noted so it is not a surprise. |

## Remaining work, ranked

1. 🔴 **Structured abstract** (#2) — rewrite into DSH's five mandatory sub-headings under 250
   words. The only item that changes the manuscript's prose substantively.
2. 🔴 **AI Disclosure Statement** (#9) — mandatory end-matter section, and A37's model-assisted
   drafting history makes it non-optional. Must separate model-assisted drafting from the
   deterministic measurement chain.
3. 🔴 **Funding section** (#7) — ⟦MG⟧ wording, then a one-line insertion.
4. 🔴 **Figure 1 at ≥300 dpi as TIFF** (#5) + **"Alt text:" line** (#6) — regenerate from the
   plotting source; the committed PNG is 200 dpi and cannot be upscaled honestly.
5. ⚠️ **HUMSOC reference conversion** (#4) — ~18 entries, plus new reference-list entries for
   the detector, the drift tables, and the Hunspell word-lists.
6. ⚠️ **Keywords line** (#3) and **"Data availability" heading rename + end-matter ordering** (#8).
7. ⚠️ **Convert to `.docx` or the OUP LaTeX template** (#11), text and figures as separate files.
8. ❓ **Resolve the anonymity model** (#13) before upload — it decides whether a blinded copy is
   needed at all.
9. ⟦MG⟧ **Zenodo DOI decision** (#12) and the standing **author read-through** recorded in
   [SIGNOFF_A37_author_pass.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/SIGNOFF_A37_author_pass.md).

## Already discharged (do not re-open)

- **The byline gate.** [SIGNOFF_A37_author_pass.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/SIGNOFF_A37_author_pass.md) §1
  records it as discharged: the frontmatter byline already matches [AUTHOR.md](https://github.com/gasyoun/Uprava/blob/main/AUTHOR.md)
  verbatim (Mārcis Gasūns, independent scholar, ORCID, gasyoun@ya.ru). Confirm on read-through; do not re-derive.
- **References integrity.** All eleven in-text citations resolve to References entries and every
  entry is cited, checked both directions in the author-voice pass, on a list written from
  verified literature in the [H125 referee pass](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A37_review_fable5.md).
  The HUMSOC work (#4) is *formatting*, not verification.
- **Numbers and claims.** The author-voice pass changed no number, claim, or citation — verified
  mechanically against `origin/master` by numeral and citation-token multiset diff.
- **Strip-at-submission scaffolding** is already inventoried in the signoff §3 (the draft-status
  blockquote, the "(draft — author to finalise)" References marker, the §7 provenance
  parenthetical). Use that list rather than re-deriving it.

_Dr. Mārcis Gasūns_
