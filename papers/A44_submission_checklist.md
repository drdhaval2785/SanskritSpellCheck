# A44 — *IJL* submission checklist

_Created: 10-08-2026 · Last updated: 10-08-2026_

Venue requirements for **A44**, [A44_body_grounded_triage_paper.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A44_body_grounded_triage_paper.md)
("The Dictionary Body as Ground Truth"), target **International Journal of Lexicography**
(Oxford University Press). Assembled under [H2407](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2407-Fable_SanskritSpellCheck_a44-plus5-camera-ready-pack_07.08.26.md)
via [/paper-submission-pack](https://github.com/gasyoun/claude-config/blob/main/commands/paper-submission-pack.md).

**Guidelines sources.** Two, and the second is the load-bearing one:

1. [academic.oup.com/ijl/pages/General_Instructions](https://academic.oup.com/ijl/pages/General_Instructions),
   fetched **10-08-2026** — the OUP-wide policies (APA 7, alt text, funding, licensing).
2. **`IJL Stylesheet 2024.docx`**, from the **Author Pack** (`IJL_Author_Pack.zip`,
   downloaded and read **10-08-2026**; also contains `IJL Main Document.dotx` and
   `IJL Title Page.docx`). This is where every journal-specific number lives — none of it is
   on the public page. Refetch with
   [Uprava/tools/fetch_ijl_author_pack.py](https://github.com/gasyoun/Uprava/blob/main/tools/fetch_ijl_author_pack.py).

**All four previously ❓ UNVERIFIED rows are now resolved from the stylesheet, and three of
the four are worse than the public page allowed us to assume** — the abstract cap is 150 (not
250), review is explicitly double-blind, and the article ceiling counts appendices. See rows
2–5.

## Status legend

✅ satisfied · ⚠️ needs work · 🔴 blocker · ⟦MG⟧ human decision

## Manuscript requirements

| # | Requirement | Status | Where / what remains |
|---|---|---|---|
| 1 | **Reference style: APA 7th edition** — "The reference style for the journal is APA (7th edition)." | ⚠️ | The 15 References entries are in a house author–date form close to APA but not verified item-by-item against APA 7 (title casing, `&` vs "and", DOI-as-URL form, journal-issue punctuation). One mechanical conversion pass needed. |
| 2 | **Article length: 4,000–8,000 words**, "including any appendices to accompany the article (but excluding any Supplementary Online Material, where there is no word limit)" | ✅ | Measured **5,889 words** in the *IJL* counting scope (body + abstract + appendix + data section, excluding the 501-word reference list); 6,390 for the whole file. Comfortably inside the band, with ~2,100 words of headroom — so the trims below are free, and material cut from the abstract can move into the body. Note the band has a **floor**: gutting the paper is not an option. |
| 3 | **Abstract: one paragraph, upper limit 150 words**, impersonal style ("it has been demonstrated…"), same text pasted into the ScholarOne box | 🔴 | The abstract is **329 words — 2.2× the cap**, and the limit is *150*, not the 250 this checklist first assumed from OUP-wide norms. It needs to lose ~180 words, which is a rewrite rather than a trim. It is also currently **multi-paragraph and partly first-person in register**, against the stylesheet's one-paragraph impersonal requirement. Since the article has word-count headroom (row 2), displaced detail belongs in §1. |
| 4 | **Keywords: below the Abstract, prefixed "Keywords: ", semicolon-separated, regular capitalization.** Authors *select from ScholarOne's own area-keyword and language lists first*, adding unlisted terms only if those lists fit poorly | ⚠️ | The manuscript still has **no keywords line**. The format is now known exactly, but the *content* is half-gated: the controlled list is only visible inside ScholarOne at submission time, so the local line should be provisional and reconciled against the platform's list. Provisional: `Keywords: Error detection; Sanskrit; Digital dictionaries; Dictionary criticism; Large language models; Inter-annotator agreement`. |
| 5 | **Double-blind review — anonymity is mandatory** | 🔴 | Confirmed, and it is the pack's most consequential find: *"Please remove any self-identifying information from the document text to ensure anonymity during our double-blind review process."* The submission is **two files**: a **Title Page** (title, names, affiliations, countries, emails) and a **main file** with title + abstract + keywords **but no authors**. A44 currently fails this three ways — (a) frontmatter `author:` with name, ORCID and email; (b) ~40 in-text links to `github.com/drdhaval2785` and `gasyoun/`, which identify the author as surely as a byline; (c) the draft-status notes naming per-pass model tiers and internal handoff IDs. Also explicit: **do not** replace names with "Author" — "this usually identifies you". Self-citation is allowed "when justified, but not in a way that could identify them". |
| 5b | **British English spelling and typographical conventions** | ⚠️ | New requirement, absent from the public page. The manuscript is mixed — e.g. *digitised/digitized* both appear, *catalogue* is already British. One consistency pass needed. |
| 6 | **File format: Word preferred, ODF allowed; use the supplied template's predefined paragraph styles** | ⚠️ | Templates in hand: `IJL Main Document.dotx` (numbered `IJL H1` headings in Arial 12, Notes-before-References, optional `A. Dictionaries` / `B. Other literature` split) and `IJL Title Page.docx`. The manuscript is **Markdown**, so it needs conversion into the `.dotx` with styles applied — `pandoc --reference-doc` gets partway, but the numbered-heading and endnote conventions want a manual pass. Verify the **ScholarOne PDF preview** faithfully represents the submission; if conversion breaks, upload a self-generated PDF as the main document with the original attached as a supplementary file. |
| 6b | **Endnotes, not footnotes** — a numbered block headed *Notes* (Arial 12, `IJL H1`, unnumbered) between main text and References; notes sparingly, never for references | ✅ n/a | The manuscript uses no footnotes or endnotes at all, so nothing to convert. If any are added during revision, they must be endnotes in that block. |
| 6c | **Headings: numbered from 1** (not 0), three levels, no all-content-word capitals; first paragraph flush left after a section heading, run-on after a sub-subsection heading | ✅ mostly | A44 already numbers §1–§7 with sentence-case headings. Cosmetic alignment happens during the template conversion. |
| 6d | **Tables: number + caption *above*; figures: number + caption *below*** ("Table 1. …", "Figure 1. …"); avoid "in the table above" phrasing | ⚠️ | A44's tables are Markdown without numbered captions. Add `Table N.` captions above each during conversion, and check no prose says "the table above" — final position shifts in typesetting. |
| 6e | **Typography: italics for cited linguistic forms, bold for dictionary headwords** (small caps permitted for headwords); non-IPA phonetic characters need an accompanying equivalence list | ⚠️ | A44 cites Sanskrit forms constantly (`girī`, `samadhurA`, b/v pairs). Convention needs one deliberate pass: cited forms italic, dictionary headwords bold. It uses IAST/SLP1 rather than IPA, so no IPA list is owed. |
| 6f | **Quotation marks:** double for quotes, single for glosses/translations; block quotes ("Long quote" style) beyond five lines; avoid slashes and "s/he" | ⚠️ | Gloss convention matters here — the paper glosses dictionary senses frequently and should use single quotes for them. Slashes appear in `b/v`, but as a linguistic notation for the letter pair, not as an "and/or" shortcut; that is the stylesheet's target, so it is defensible. Flag for the author, do not mass-replace. |
| 6g | **Numbers:** spell out up to 100 and vague quantities; figures for statistics, precise values, measurements, and anything above 100 | ✅ mostly | A44 is statistics-dense and already uses figures for all counts and percentages. A pass should catch stray spelled-out precise values ("seventeen rows" → "17 rows"). |
| 7 | **Figures — mandatory alt text** | ✅ n/a | The paper has no figures or images; all quantitative content is in Markdown tables. No alt text obligation arises. If any table is converted to a figure during typesetting, alt text becomes mandatory, placed beneath the legend prefixed "Alt text:". |
| 8 | **Third-party permissions** | ✅ | No prose extract approaches OUP's thresholds (>400 words single, >800 cumulative, ≥¼ of a work); quoted dictionary entries are short and from public-domain 19th–20th-c. editions. |
| 9 | **Funding statement** | 🔴 ⟦MG⟧ | **Required**: "authors are required to name their funding sources in the manuscript." The manuscript has **no funding statement**. Blocker until ⟦MG⟧ confirms the wording (presumed "no external funding"). |
| 10 | **Data availability** | ✅ | Strongly encouraged, not mandated. Satisfied in substance by the *Data and reproducibility* section, which names every artifact with a resolvable URL plus the exact commands that regenerate the headline figures. |
| 11 | **Dataset references** | ⚠️ ⟦MG⟧ | If the artifacts are cited as data rather than shipped as supplements, each needs a reference-list entry in the DataCite-minimum form `[dataset]* Authors, Year, Title, Publisher (repository), Identifier` — which requires minting a DOI (e.g. Zenodo). ⟦MG⟧ decision #2 in the cover letter. |
| 12 | **Ethics / competing interests / AI-usage declaration** | ✅ | None required on the *IJL* general page. Competing interests are declared nil in the cover letter; AI usage is documented in the method as per-phase model attribution — a strength here, since LLM triage is the paper's subject. |
| 13 | **Copyright / licence** | ✅ post-acceptance | Copyright assignment to OUP is a condition of publication; the online licence-to-publish form is completed **after acceptance**. Optional paid open access is selectable then, possibly covered by a Read-and-Publish agreement. Nothing to do at submission. |
| 14 | **Preprint policy** | ✅ | Preprints permitted and do not block submission; if one is posted it must be updated with the published DOI after acceptance. |
| 15 | **Submission portal + account** | ✅ | ScholarOne: [mc.manuscriptcentral.com/ijlex](https://mc.manuscriptcentral.com/ijlex) (the stylesheet gives the `https` form). Authors must **create an account and reuse it for subsequent submissions**, and keep *all* editor interaction inside ScholarOne — so no direct email to the Editor. The cover letter is therefore pasted into the platform, not sent. |
| 16 | **Optional pre-submission AI check** | — | Paperpal Preflight is offered, tailored to the journal; "this is not mandatory and suggested corrections are optional." |
| 17 | **Colour figures** | ✅ n/a | Colour is free in PDF/HTML; **£350 per figure** for colour in print. A44 has no figures. If any are added, ensure the greyscale rendering still makes its distinctions. |
| 18 | **Book reviews are commissioned** | ✅ n/a | Not applicable — A44 is a research article. Noted only so a future session does not mistake the reviews route (`ijlreviews@gmail.com`, prior arrangement required) for the article route. |

## Remaining work, ranked

The order changed once the stylesheet was read: the abstract moved from "likely trim" to a
**rewrite**, and anonymization from an open question to a **confirmed two-file restructure**.

1. 🔴 **Anonymize for double-blind review** (#5) — the largest single task, and the one most
   easily missed because the public page never mentions it. Produce **two files**: a Title Page
   from `IJL Title Page.docx`, and an anonymized main file. Anonymizing means more than the
   byline: ~40 in-text `github.com/drdhaval2785` / `gasyoun/` links identify the author, and
   the draft-status notes name internal handoffs. Do **not** substitute "Author" for the name.
   A blinded variant of the *Data and reproducibility* section is the delicate part — the
   artifacts must stay verifiable without naming their owner (anonymized-repo or
   supplementary-file route).
2. 🔴 **Rewrite the abstract to ≤150 words**, one paragraph, impersonal register (#3). It is
   currently 329 words, so this is a rewrite, not a trim. Row 2 gives ~2,100 words of headroom,
   so displaced content can move into §1 rather than being lost.
3. 🔴 ⟦MG⟧ **Funding statement** (#9) — one mandatory line, blocked only on wording.
4. ⚠️ **Convert to `IJL Main Document.dotx`** with its paragraph styles (#6), then verify the
   **ScholarOne PDF preview** matches intent. Carries the table captions (#6d), typography
   (#6e), and heading conventions (#6c) with it. Markdown stays canonical.
5. ⚠️ **APA 7 conversion of the References** (#1) — ~15 entries; the stylesheet supplies
   worked examples per type, including the `[dataset]`/software form and the optional
   `A. Dictionaries` / `B. Other literature` split, which suits this paper well.
6. ⚠️ **Add the keywords line** (#4), then reconcile against ScholarOne's controlled list at
   submission time.
7. ⚠️ **British English consistency pass** (#5b) — *digitised* vs *digitized* currently mixed.
8. ⟦MG⟧ **Supplement-vs-dataset decision** (#11) and the standing **author read-through**
   recorded in [SIGNOFF_A44_author_pass.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/SIGNOFF_A44_author_pass.md).

## Already discharged (do not re-open)

- Both References defects flagged in the signoff — the dangling *Artstein & Poesio (2008)*
  entry and the unverifiable *ISCLS (2026)* citation — were **fixed under H825** (12-07-2026);
  every References URL was resolved and title/author-checked on that date.
- The reliability gate is discharged by §4.6's blind second-annotator study; the
  cross-family run remains tooled-but-unrun (no `LLM_API_KEY` on the host) and is
  **acknowledged in §6 as a limitation**, not presented as complete — see
  [HUMAN_ANCHOR_NEEDED.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/irr/HUMAN_ANCHOR_NEEDED.md).

_Dr. Mārcis Gasūns_
