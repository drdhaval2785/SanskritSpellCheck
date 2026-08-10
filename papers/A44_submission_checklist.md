# A44 — *IJL* submission checklist

_Created: 10-08-2026 · Last updated: 10-08-2026_

Venue requirements for **A44**, [A44_body_grounded_triage_paper.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A44_body_grounded_triage_paper.md)
("The Dictionary Body as Ground Truth"), target **International Journal of Lexicography**
(Oxford University Press). Assembled under [H2407](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2407-Fable_SanskritSpellCheck_a44-plus5-camera-ready-pack_07.08.26.md)
via [/paper-submission-pack](https://github.com/gasyoun/claude-config/blob/main/commands/paper-submission-pack.md).

**Guidelines source:** [academic.oup.com/ijl/pages/General_Instructions](https://academic.oup.com/ijl/pages/General_Instructions),
fetched **10-08-2026**. Journal-specific numeric limits (word count, abstract length, keyword
count) and the review model are **not stated on that public page** — OUP keeps them in the
downloadable Author Pack / style sheet. Those rows below are marked **UNVERIFIED**; they are
not guesses dressed as requirements. Resolve them by downloading the Author Pack from the
journal page before submitting.

## Status legend

✅ satisfied · ⚠️ needs work · 🔴 blocker · ❓ UNVERIFIED (requirement not published) · ⟦MG⟧ human decision

## Manuscript requirements

| # | Requirement | Status | Where / what remains |
|---|---|---|---|
| 1 | **Reference style: APA 7th edition** — "The reference style for the journal is APA (7th edition)." | ⚠️ | The 15 References entries are in a house author–date form close to APA but not verified item-by-item against APA 7 (title casing, `&` vs "and", DOI-as-URL form, journal-issue punctuation). One mechanical conversion pass needed. |
| 2 | **Article length** | ❓ | Manuscript is **~6,475 words** (whole file incl. front matter and apparatus; body proper is shorter). Limit not published on the general page — confirm from the Author Pack. |
| 3 | **Abstract length** | ❓ | Current abstract is **~331 words**, which exceeds the common OUP humanities cap of 250. Confirm the *IJL* limit; if 250, the abstract needs a trim of roughly 80 words. |
| 4 | **Keywords** | ⚠️ ❓ | The manuscript has **no keywords list**. Count/format unpublished; add a keyword line regardless (suggested: *lexicography; error detection; Sanskrit; digital dictionaries; grammatical error detection; large language models; inter-annotator agreement*). |
| 5 | **Anonymization / review model** | ❓ | Not stated publicly whether review is double-anonymous. The manuscript currently carries a **named byline plus ORCID and email in the frontmatter**, and cites the author's own project repositories by full URL throughout — if review is anonymous, both are disclosure defects requiring a blinded copy. Resolve before upload. |
| 6 | **File format / template** | ⚠️ | OUP supplies MS Word and ODF templates ("use the paragraph styles from the template"); LaTeX is supported. The manuscript is **Markdown** — a Word or LaTeX conversion is required. Full style compliance is relaxed at first submission: "it is not essential to follow these guidelines in every detail." |
| 7 | **Figures — mandatory alt text** | ✅ n/a | The paper has no figures or images; all quantitative content is in Markdown tables. No alt text obligation arises. If any table is converted to a figure during typesetting, alt text becomes mandatory, placed beneath the legend prefixed "Alt text:". |
| 8 | **Third-party permissions** | ✅ | No prose extract approaches OUP's thresholds (>400 words single, >800 cumulative, ≥¼ of a work); quoted dictionary entries are short and from public-domain 19th–20th-c. editions. |
| 9 | **Funding statement** | 🔴 ⟦MG⟧ | **Required**: "authors are required to name their funding sources in the manuscript." The manuscript has **no funding statement**. Blocker until ⟦MG⟧ confirms the wording (presumed "no external funding"). |
| 10 | **Data availability** | ✅ | Strongly encouraged, not mandated. Satisfied in substance by the *Data and reproducibility* section, which names every artifact with a resolvable URL plus the exact commands that regenerate the headline figures. |
| 11 | **Dataset references** | ⚠️ ⟦MG⟧ | If the artifacts are cited as data rather than shipped as supplements, each needs a reference-list entry in the DataCite-minimum form `[dataset]* Authors, Year, Title, Publisher (repository), Identifier` — which requires minting a DOI (e.g. Zenodo). ⟦MG⟧ decision #2 in the cover letter. |
| 12 | **Ethics / competing interests / AI-usage declaration** | ✅ | None required on the *IJL* general page. Competing interests are declared nil in the cover letter; AI usage is documented in the method as per-phase model attribution — a strength here, since LLM triage is the paper's subject. |
| 13 | **Copyright / licence** | ✅ post-acceptance | Copyright assignment to OUP is a condition of publication; the online licence-to-publish form is completed **after acceptance**. Optional paid open access is selectable then, possibly covered by a Read-and-Publish agreement. Nothing to do at submission. |
| 14 | **Preprint policy** | ✅ | Preprints permitted and do not block submission; if one is posted it must be updated with the published DOI after acceptance. |
| 15 | **Submission portal** | ✅ | ScholarOne: [mc.manuscriptcentral.com/ijlex](http://mc.manuscriptcentral.com/ijlex). |
| 16 | **Optional pre-submission AI check** | — | Paperpal Preflight is offered, tailored to the journal; "this is not mandatory and suggested corrections are optional." |

## Remaining work, ranked

1. 🔴 **Funding statement** (#9) — the one published, mandatory requirement the manuscript
   currently fails. ⟦MG⟧ wording, then a one-line insertion.
2. ❓ **Download the Author Pack** and close #2/#3/#4/#5 with real numbers. The abstract at
   ~331 words is the likeliest casualty; the anonymization question is the likeliest to force a
   second, blinded manuscript file.
3. ⚠️ **APA 7 conversion of the References** (#1) — mechanical, ~15 entries.
4. ⚠️ **Add a keywords line** (#4) — safe regardless of the unpublished count.
5. ⚠️ **Convert to the OUP Word/ODF template or LaTeX** (#6) — from the Markdown source, which
   stays canonical (`pandoc papers/A44_body_grounded_triage_paper.md -o A44_submission.docx`).
6. ⟦MG⟧ **Supplement-vs-dataset decision** (#11) and the standing **author read-through**
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
