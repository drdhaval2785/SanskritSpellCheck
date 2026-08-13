# A37 submission pack — start here

_Created: 10-08-2026 · Last updated: 10-08-2026_

Submission pack for **A37**, one of the five PLUS5 prestige papers selected 29-07-2026
(«A44, A37, A13, A17, A61» — see [ARTICLES.md](https://github.com/gasyoun/Uprava/blob/main/ARTICLES.md)).
Assembled under [H2406](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2406-Fable_SanskritSpellCheck_a37-plus5-camera-ready-pack_07.08.26.md)
by Fable 5 (`claude-fable-5`) via [/paper-submission-pack](https://github.com/gasyoun/claude-config/blob/main/commands/paper-submission-pack.md).

**Note on the handoff title.** It says "camera-ready pack", but A37 is **not accepted
anywhere** — a true camera-ready pass is post-acceptance work
([/paper-camera-ready](https://github.com/gasyoun/claude-config/blob/main/commands/paper-camera-ready.md)).
What the goal line actually asks for is byline + checklist + cover-letter skeleton per venue,
which is the *submission* pack. That is what this is.

## The pack

| File | What it is |
|---|---|
| [validate_a37_pack.py](https://github.com/gasyoun/SanskritSpellCheck/blob/master/papers/validate_a37_pack.py) | Selftest (twin of `validate_a44_pack.py`): pack files present, byline consistent across manuscript/companion/letter, the checklist's measured numbers still true, no invented DOI. It already caught one real defect — see *Corrections* below. |
| [A37_cover_letter.md](https://github.com/gasyoun/SanskritSpellCheck/blob/master/papers/A37_cover_letter.md) | Letter to the *DSH* editors — contribution, venue fit, the negative result stated up front, scope caveats, no-dual-submission line, AI-use note. Six ⟦MG⟧ decisions listed at the foot. |
| [A37_submission_checklist.md](https://github.com/gasyoun/SanskritSpellCheck/blob/master/papers/A37_submission_checklist.md) | 20 *DSH* requirements against the manuscript as measured, with a ranked remaining-work list. Guidelines fetched 10-08-2026. |
| [A37_checklist.md](https://github.com/gasyoun/SanskritSpellCheck/blob/master/papers/A37_checklist.md) | ARR Responsible-NLP + reproducibility checklist (A1–E1). Internal quality bar for *DSH*; a **formal attachment** when the LChange companion goes out. |

## Venue split (unchanged by this pack)

- **Primary: *Digital Scholarship in the Humanities*** (OUP) for
  [A37_ortho_drift_paper.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A37_ortho_drift_paper.md),
  readiness 4/5. Rolling submission, no deadline.
- **Companion: LChange** for
  [A37_lchange_companion.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A37_lchange_companion.md)
  ("When the S-curve Lies"), readiness 2/5 — a companion, **not** a replacement. CfP for
  LChange'27 expected ~Oct–Dec 2026, `@WAITING` per
  [ACL_METHOD_OPPORTUNITIES_SANSKRIT_2026.md](https://github.com/gasyoun/Uprava/blob/main/ACL_METHOD_OPPORTUNITIES_SANSKRIT_2026.md).

## The four blockers, in one place

Full detail and 20 rows of context in the submission checklist; this is the short version of
what stands between the manuscript and the portal.

1. **Structured abstract.** DSH mandates five sub-headings (Purpose; Design/methodology/approach;
   Findings; Originality; Contribution to the field of Digital Humanities) within 250 words. The
   current abstract is one **246-word** narrative paragraph — inside the cap, so the failure is
   *structure*, not length. Sub-headings themselves cost words, so budget a ~30–50-word prose cut
   to stay under 250 once they are added. The only item that touches the manuscript's prose
   substantively.
2. **AI Disclosure Statement.** Mandatory DSH end-matter section, and it does not exist. The
   disclosure currently lives in the draft-status blockquote — which is on the
   strip-at-submission list, so today's compliance disappears exactly when the paper is
   submitted. Must separate model-assisted *drafting* from the model-free *measurement* chain.
3. **Funding section** — mandatory, absent, ⟦MG⟧ wording.
4. **Figure 1 at ≥300 dpi + "Alt text:" line.** `ortho_drift/drift_composition.png` is
   1420×812 at **200 dpi**; the floor is 300 and TIFF/EPS are the accepted formats. Regenerate
   from the plotting source — a 200-dpi raster cannot be upscaled honestly. Alt text is
   mandatory for all images and must sit beneath the legend prefixed `Alt text:`.

One requirement is unresolvable from the public page and should be settled **before** upload:
whether DSH review is anonymous (checklist #13). The manuscript carries a named byline with
ORCID and email and cites the author's own repositories by full URL throughout — if review is
anonymous, that is a disclosure defect needing a separate blinded file.

## Corrections to the first pass (both found after it shipped)

Recorded here rather than quietly rewritten, because both were wrong *claims*, not typos.

1. **The pack was pushed to the wrong remote.** The first attempt opened
   [PR #102](https://github.com/drdhaval2785/SanskritSpellCheck/pull/102) against upstream
   `drdhaval2785/SanskritSpellCheck`, where it sat awaiting a third-party maintainer with no
   stake in this org's paper apparatus. Submission-pack files are the author's own editorial
   scaffolding, so they belong on the `gasyoun` fork — which is exactly the route the A44 pack
   took ([v1.59.0](https://github.com/gasyoun/SanskritSpellCheck/releases/tag/v1.59.0)). This
   branch is the re-land; #102 is closed as wrongly targeted.
2. **The abstract was reported as 251 words, over DSH's 250 cap. It is 246 — inside it.** The
   original count included the two Markdown heading lines. `validate_a37_pack.py` caught this on
   its first run. The blocker itself survives, but for the right reason: the abstract is
   **unstructured**, missing DSH's five mandatory sub-headings. Length was never the failure, and
   describing it as "over by 1 word" pointed the remaining work at the wrong fix.

The second one is the reason the validator exists: a pack whose headline numbers cannot be
re-derived from the repository is a pack that will drift silently.

## What this pack did not touch

- **The manuscript.** No number, claim, citation, or section was edited. The pack measures and
  reports; it does not revise.
- **The byline.** Already correct and already discharged as a gate —
  [SIGNOFF_A37_author_pass.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/SIGNOFF_A37_author_pass.md) §1
  records that the frontmatter matches [AUTHOR.md](https://github.com/gasyoun/Uprava/blob/main/AUTHOR.md)
  verbatim (Mārcis Gasūns, independent scholar, ORCID 0000-0003-4513-884X, gasyoun@ya.ru).
  Confirm on read-through; do not re-derive.
- **`CITATION.cff`.** Deliberately not touched: the A44 pack
  ([H2407](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2407-Fable_SanskritSpellCheck_a44-plus5-camera-ready-pack_07.08.26.md),
  [v1.59.0](https://github.com/gasyoun/SanskritSpellCheck/releases/tag/v1.59.0)) already added one
  at the repository root, and it carries the same canonical identity A37 needs. Its `preferred-citation`
  names A44 because A44 got there first — if A37 reaches submission before it, that block is the
  thing to revisit, not the identity fields. Its missing `license:` key is the same B2 gap both
  checklists report, and is one ruling for both papers.
- **The 5/5 bump.** A37 stays at 4/5. The open gate is the author read-through, which is human
  and non-fabricable; the pack cannot close it.

_Dr. Mārcis Gasūns_
