# Changelog

All notable changes to SanskritSpellCheck are documented here.

This repository does not currently publish versioned release notes. Entries use
dated maintenance snapshots; keep upcoming work under [Unreleased] until it is
ready for a dated entry.

## [Unreleased]
### Added
- **A37 submission pack for *Digital Scholarship in the Humanities* (H2406, 10-08-2026,
  Fable 5 `claude-fable-5`).** Sibling of the A44 *IJL* pack in 1.59.0 — the second of the five
  PLUS5 prestige papers to get one. Start at
  [papers/A37_PACK_README.md](https://github.com/gasyoun/SanskritSpellCheck/blob/master/papers/A37_PACK_README.md):
  [cover letter](https://github.com/gasyoun/SanskritSpellCheck/blob/master/papers/A37_cover_letter.md)
  (6 ⟦MG⟧ decisions), a [20-row DSH venue checklist](https://github.com/gasyoun/SanskritSpellCheck/blob/master/papers/A37_submission_checklist.md),
  a [filled ARR checklist](https://github.com/gasyoun/SanskritSpellCheck/blob/master/papers/A37_checklist.md),
  and [validate_a37_pack.py](https://github.com/gasyoun/SanskritSpellCheck/blob/master/papers/validate_a37_pack.py).
  - **Unlike *IJL*, DSH publishes its numbers**, so 18 of 20 rows are verified rather than
    UNVERIFIED. Only two are genuinely unpublished: the **peer-review anonymity model** and ORCID
    handling. Anonymity is the one that bites — the manuscript carries a named byline with ORCID
    plus self-citing repo URLs throughout, so anonymous review would force a second blinded file.
  - **Four blockers, and length is not among them**: the body is ~3,143 words against a 9,000-word
    limit. What fails is form — a **structured abstract** (DSH mandates five sub-headings; the
    current abstract is a 246-word narrative paragraph, *inside* the cap but unstructured), a
    missing **Funding** section, a missing **AI Disclosure Statement**, and Figure 1 at **200 dpi
    against a 300 dpi floor** with no `Alt text:` line.
  - **The AI-disclosure gap is the subtle one.** A37's model-assisted history is documented
    unusually well — but only inside the draft-status blockquote, which is on the
    strip-at-submission list, so today's compliance would vanish at the exact moment the paper is
    submitted. It has to become real end-matter separating model-assisted *drafting* from the
    **model-free measurement chain** (a deterministic detector; no model touches the numbers).
  - **B2 (licences) is the one outright `no`** on the ARR checklist — the same gap A44 reports, and
    the reason [CITATION.cff](https://github.com/gasyoun/SanskritSpellCheck/blob/master/CITATION.cff)
    can declare no `license:` truthfully. One ruling closes A37's B2, A44's B2, and the CFF key.
  - **Two self-corrections recorded in the pack README:** the first push targeted the upstream
    `drdhaval2785` repo (wrong home for author scaffolding; that PR is closed and this is the
    re-land on the fork), and the abstract was first reported as 251 words — the count had
    included two heading lines. The new validator caught the latter on its first run.
  - Manuscript **unedited**: no number, claim, citation, or section changed. A37 stays **4/5** —
    the author read-through is the gate.

## [1.60.0] - 2026-08-10
### Fixed
- **The four UNVERIFIED A44 venue requirements are now resolved from the gated IJL
  Author Pack — and three are worse than v1.59.0 could assume (H2407 follow-up,
  Fable 5 `claude-fable-5`, [PR #6](https://github.com/gasyoun/SanskritSpellCheck/pull/6)).**
  `IJL_Author_Pack.zip` (`IJL Stylesheet 2024.docx` + `IJL Main Document.dotx` +
  `IJL Title Page.docx`) is where every journal-specific number lives; none of it is on
  OUP's public instructions page.
  - **Abstract cap is 150 words, not the 250 inferred from OUP-wide humanities norms.**
    A44's abstract is 329 words — 2.2× over — so this is a rewrite, not a trim, and it
    must also become one paragraph in impersonal register.
  - **Review is double-blind**, which the public page never states: *"remove any
    self-identifying information … to ensure anonymity."* Submission is **two files**
    (Title Page + anonymized main file). A44 fails three ways — frontmatter
    author/ORCID/email, ~40 in-text `drdhaval2785`/`gasyoun` links that identify the
    author as surely as a byline, and draft notes naming internal handoff IDs. The
    stylesheet also forbids the obvious workaround: do *not* replace names with "Author".
    Now the top-ranked task, and it creates a real tension — the paper's credibility rests
    on artifacts whose links are exactly what anonymization removes (⟦MG⟧ decision #5).
  - **Article band is 4,000–8,000 words including appendices** (Supplementary Online
    Material is unlimited). Measured **5,889** in that scope — passes, with ~2,100 words of
    headroom, so abstract cuts can move into §1. The band has a floor, so shortening the
    paper is not a free move.
  - **Keywords** format is now exact (below the Abstract, `Keywords: `, semicolons), but the
    controlled vocabulary is only visible inside ScholarOne, so the local line is provisional.
  - Nine further requirements the public page never mentioned: British English, endnotes not
    footnotes, table captions above / figure captions below, italics-for-forms +
    bold-for-headwords, gloss quoting, number style, £350 per print-colour figure,
    commissioned-only book reviews, and **all editor contact inside ScholarOne** — so the
    cover letter is pasted, not emailed (corrected, along with its word count).
  - The selftest now guards the real caps so a later edit cannot restore the wrong ones, and
    asserts no requirement row is left marked ❓. Refetch tooling lives in Uprava
    ([PR #1766](https://github.com/gasyoun/Uprava/pull/1766)).

## [1.59.0] - 2026-08-10
### Added
- **A44 submission pack for the *International Journal of Lexicography* (H2407,
  10-08-2026, Fable 5 `claude-fable-5`).** The paper sat at 4/5 with no packaging
  artifacts; this adds the four the venue and the internal gate require:
  [papers/A44_cover_letter.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A44_cover_letter.md)
  (IJL-addressed, 4 ⟦MG⟧ decisions isolated in a table),
  [papers/A44_submission_checklist.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A44_submission_checklist.md)
  (16 requirements off the OUP general instructions, fetched 10-08-2026),
  [papers/A44_checklist.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A44_checklist.md)
  (ARR Responsible NLP, A1/A2 both discharged — no blocker in the family that gate
  exists to catch), and a repo-first
  [CITATION.cff](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/CITATION.cff).
  - **One published mandatory requirement is failed and named as a blocker:** *IJL*
    requires funding sources in the manuscript and A44 has no funding statement.
  - **Four requirements are recorded as UNVERIFIED, not guessed** — word limit, abstract
    length, keyword count and the anonymous-review question are absent from OUP's public
    page and live in the gated Author Pack. Measured against common caps, the ~331-word
    abstract is the likely casualty and the named byline plus self-citing repo URLs would
    be disclosure defects under anonymous review.
  - **B2 is the one outright `no`:** neither the CDSL inputs nor the created do-not-file
    artifacts carry a licence declaration, and the repo itself declares none — so
    `CITATION.cff` deliberately ships *without* a `license:` key rather than inventing
    redistribution terms, and with no DOI rather than a placeholder.
  - [papers/validate_a44_pack.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/validate_a44_pack.py)
    guards the pack: canonical identity tokens, no fabricated licence or DOI, byline
    agreement, the no-figures claim behind IJL's mandatory alt text, and regression of the
    two References defects H825 fixed.

## [1.58.0] - 2026-07-31
### Added
- **SHS entry-body deterministic detector pilot (H1535, roadmap Q3 item 6).**
  [detectors/entry_body_pilot.py](detectors/entry_body_pilot.py) extends
  `charset_check`/`phonotactic_check`/the bigram `ngram` checker from headwords
  into SHS entry-body text (209k `{#...#}` spans → 162,814 clean body words after
  excluding two SHS notation conventions found along the way: `-` stem-elision
  and `0` as a period-substitute abbreviation-dot). Full human-verified precision
  on the 25 charset+phonotactic candidates: **16.0%** — in-band with SHS's own
  headword-level triage precision (~15%). The dominant false-positive class
  (~84%) is Pāṇinian grammatical-citation notation (bare affix-name citations,
  parenthetical variant-reading shorthand) that ordinary phonotactic rules
  aren't designed for — documented with concrete suppression rules for scale-up.
  9 genuine candidates flagged for future scan-verification, none filed. See
  [corrections_draft/SHS/body_pilot/README.md](corrections_draft/SHS/body_pilot/README.md).
- **Monthly detection-loop GitHub Actions cron (H1533, roadmap Q4 item 5).**
  `.github/workflows/monthly-detection-loop.yml` runs on the 1st of each month
  (and via `workflow_dispatch`) re-running the full `run_all.py` detector
  suite against the committed `sanhw1.txt`, then `detectors/monthly_loop.py`
  diffs the resulting tier-A candidates against a committed baseline
  (`detectors/monthly_loop/tier_a_baseline.txt`) to compute what's genuinely
  NEW since the previous cycle (the suppression layer itself is already
  applied inside `run_all.aggregate()`). Emits a dated delta report
  (`detectors/monthly_loop/reports/<YYYY-MM>.md`), uploads
  `combined_candidates.txt`/`_sf.txt`/`_review.html` + the report as run
  artifacts every cycle, and opens/updates a PR with the refreshed baseline +
  report only when the cycle found a delta — a quiet month makes no noise.
  See `detectors/monthly_loop/README.md`. (Follow-up: the workflow now installs
  `requirements.txt` before running the suite — its first `workflow_dispatch`
  verification failed with `ModuleNotFoundError: sanskrit_util`, since
  `meter_check.py`'s transcoder import needs the pip-installed package that
  `ci.yml` already installs but this workflow initially didn't.)

### Fixed
- **`run_all.py` could never complete `--rerun` on a fresh checkout.** PR #45's
  cache-manifest hardening treated ANY zero-byte detector output as a crash,
  but two detectors legitimately produce one: `meter_check` when its offline
  GRETIL corpus index (gitignored, ~1hr build) is absent — true on every fresh
  clone — and `tied_field_check`, which currently finds zero disagreements
  against `sanhw1.txt`. Neither detector swallows exceptions, so a non-zero
  `returncode` already reliably signals a real failure; `_regenerate_outputs`
  and `_output_hashes` now trust that instead of also gating on output size.
  Found while building the monthly-loop workflow above, whose first
  `--rerun` invocation hard-failed with "meter_check produced no detector
  output" on a stock checkout.

## [1.57.0] - 2026-07-27

### Added
- **[zenodo_dataset_v1/](zenodo_dataset_v1/) — Zenodo dataset release v1 package (H1534,
  Sonnet 5 `claude-sonnet-5`)** — staged FAIR data package for the roadmap's Q4 2026 item 3:
  the 3,884 `o_vs_O` evaluation pairs + confusion-weight model, the 2,297-headword
  do-not-file suppression list (2,549 raw entries across 33 dicts, per-dict counts table),
  the 122-row first-pass FILE-FIRST set plus the 156-row D7 union-across-runs FILE-FIRST
  set, the five gloss-language orthographic reform maps (de 15,685 / ru 7,709 / fr 18 /
  en 76 / la 0), and the meter-verdict + GRETIL-typo summary indices. `README.md` +
  `metadata.yaml` + `CITATION.cff` + `LICENSE-DATA` (CC BY 4.0) + `checksums.sha256` (27
  files, sha256). Deliberately excludes the per-dict `*_wrong_readings.txt` files (several
  quote entry text verbatim; `PD`'s is CC BY-NC-SA) and the gitignored/regenerable
  `meter_verdicts.jsonl`. **DOI minting stays a human `@DO`** (needs a Zenodo-account
  login/API token) — tracked in `Uprava/GTD_NEXT_ACTIONS.md`.

## [1.56.0] - 2026-07-26

### Added
- **Union-across-runs recall harvest (roadmap ruling D7, H1471).** A second
  independent body-aware triage run on SHS/YAT/ACC, unioned with the committed
  packages rather than replacing them: `detectors/union_across_runs.py` (the
  measurement tool, which reconstructs a run's FILE-FIRST set from the
  `triage_work/` verdicts using `triage_synthesize.py`'s own survival rule) and
  `corrections_draft/union_d7.tsv` (156 rows — 54 in both runs, 70 net-new, 32
  run-1-only, each net-new carrying its Opus confirm reason and Opus review
  verdict). Measured gain **+70 fileable candidates (+81%)** over the committed
  86; single-run agreement is only **35%**. Recorded as `docs/HYPOTHESES.md`
  **H9 — confirmed**, with R3 quantified and H2's per-dict counts re-labelled as
  single-draw lower bounds. No committed package was overwritten.
- Reproducible core, development, and optional-analysis dependency manifests,
  with CI coverage for Python 3.11/3.14 and PHP 8.2/8.3.
- Verified detector caching via `detectors/.run_all_cache.json`; both unified
  and campaign runs reject stale or altered output unless the warning-bearing
  `--allow-stale-cache` override is explicit.

### Fixed
- Unified and campaign review pages now embed script-safe JSON, initialize it
  before JavaScript consumes it, and export corrections only for dictionaries
  supported by the selected corrector and campaign.
- `faultfinder3a.php` now enforces its four-argument contract and reports input
  and output-path errors before processing.
- The `sanskrit-util` compatibility layer now prefers the installed package
  without module-name shadowing, while retaining the sibling-checkout fallback;
  optional Vidyut chandas data has an environment override and graceful warning.

### Documentation
- **MG ruling D9 (26-07-2026): the union-across-runs scale-up is funded**, lifting
  the "full generous-budget union across all 11 fileable dicts" non-goal. The
  deciding argument is contamination rather than recall — an uncorrected typo
  headword propagates into the cross-dict union headword list, which `run_all.py`
  reads to demote broadly-attested suspects, so a typo left unfixed inflates its
  own attestation and helps suppress its own detection. Recorded in
  `ROADMAP_2026_2027.md` (D9 + the lifted non-goal); execution is handoff H1709.
- Recorded the installation split and the fact that the project currently
  declares no license; license selection remains a maintainer decision.

## [1.55.0] - 2026-07-13

### Added
- **H827: tied-field cross-encoding consistency detector.** New 11th detector family
  [detectors/tied_field_check.py](detectors/tied_field_check.py) — the "tied-field
  consistency" shape from [Bloodgood & Strauss, arXiv 1602.07807](https://arxiv.org/abs/1602.07807)
  (IEEE ICSC 2016), the project's direct methodological ancestor, missing until now: checks
  that SLP1-headword, its Devanāgarī rendering, and its IAST rendering are mutually
  derivable, by round-tripping every `sanhw1.txt` headword through both encodings via the
  shared `sanskrit-util` package (three new thin wrappers added to
  [detectors/slp1util.py](detectors/slp1util.py): `slp1_to_devanagari`, `slp1_to_iast`,
  `iast_to_slp1`). Wired into [detectors/run_all.py](detectors/run_all.py) as a
  high-precision flagger (`X:TFC-DEV=…:D` / `X:TFC-IAST=…:D`); `detectors/eval.py`'s filing
  gate stays **PASS**.
  Full run across all **431,596** lines / 431,568 unique in-alphabet headwords: **0
  unsuppressed disagreements** — every round-trip mismatch is explained by one of two
  documented, non-error transcoder asymmetries (candrabindu/avagraha via Devanāgarī: 12
  instances; the aspirate/diphthong digraph ambiguity inherent to concatenative IAST — e.g.
  a genuine `k`+`h` compound boundary reading back as the aspirate `K` — via IAST: 100
  instances), with zero unexplained residual. An honest **negative finding on error
  discovery** (the shared transcoder is round-trip consistent at full scale — itself a
  useful validation) alongside a **positive finding on methodology** (the detector correctly
  discriminates a genuine defect from a documented normalization axis; it just found no
  genuine defects because `sanhw1.txt` stores only the SLP1 headword, with no
  independently-authored Devanāgarī/IAST field to disagree with it). New hypothesis entry
  H8 in [docs/HYPOTHESES.md](docs/HYPOTHESES.md); detector table + prose in
  [detectors/readme.md](detectors/readme.md).

## [1.54.0] - 2026-07-13

### Added
- **H826 (ACL uplift): A37 S-curve exo/endo fit + SemEval-2015 DTE benchmark + LChange
  companion.** Ruling D15 from the ACL Anthology roadmap interview (revision 3):
  - [detectors/drift_dating.py](detectors/drift_dating.py) extended with
    `fit_scurve()` (a per-variant logistic S-curve fit adapted from Ghanbarnejad,
    Gerlach, Miotto and Altmann's "Extracting Information from S-curves of Language
    Change," arXiv:1406.4498) and `dte_bands()` (re-expresses the existing
    leave-one-out dater in SemEval-2015 Task 7 Diachronic Text Evaluation terms —
    correct-25-yr-epoch rate + distance-to-true-year tolerance bands, per S15-2147/
    S15-2148). Results persisted to
    [docs/ORTHO_DRIFT_FINDINGS.md](docs/ORTHO_DRIFT_FINDINGS.md) §O7a/§O7b.
  - **Honest negative finding, not forced into the expected direction:** the naive
    cross-sectional S-curve fit **inverts** the expected exo/endo mechanism ordering —
    English (convention/endogenous) fits a narrow 9.7-yr transition; German
    (legislated/exogenous, 1901/1996) fits a wide 50.2-yr one. Diagnosed as two
    distinct sampling artifacts (English's zero-censoring saturation; German's sparse
    edition-spacing around the true 1901 reform date), not evidence about either
    language's actual change mechanism — see §O7a's full caveat before citing the
    per-language `b`/`Δt80` numbers.
  - [papers/A37_ortho_drift_paper.md](papers/A37_ortho_drift_paper.md) §2 gains three
    related-work paragraphs (Ghanbarnejad et al., SemEval-2015 DTE, Lüschow 2021 ZfS
    graphemic variation); new §4.8 reports the S-curve finding as a methodological
    limitation; §5 gains the DTE distance-band re-expression. References section grows
    by five verified citations (Ghanbarnejad et al. 2014; Popescu and Strapparava
    2015; Szymanski and Lynch 2015; Ren, Wang, Zhao and Ren 2023; Lüschow 2021).
  - New [papers/A37_lchange_companion.md](papers/A37_lchange_companion.md) — a
    standalone LChange short-paper draft ("When the S-curve Lies") that isolates the
    inversion finding as a transferable methodological caution for anyone applying
    Ghanbarnejad-style S-curve mechanism classification to cross-sectional (edition-
    level, non-Ngram) corpora, with a 4-point diagnostic checklist (§5). DSH stays the
    primary journal target for A37 itself; this is an additional companion, not a
    replacement.
  - No change to SanskritSpellCheck detection logic — this is A37 paper scholarship
    only (no LOCKED/REFUTED contact).

## [1.53.0] - 2026-07-12

### Added
- **H825 (ACL uplift): GEC/GED reframe, detection-level eval metrics, cross-family
  annotator tooling.** Ruling D9/D10/D11 from the ACL Anthology roadmap interview:
  - [detectors/gold_corrections.tsv](detectors/gold_corrections.tsv)
    ([detectors/build_gold_set.py](detectors/build_gold_set.py)) — a held-out
    detection-level gold set derived from `corrections_draft/file_first_verified.tsv`
    (109 POSITIVE fileable-typo rows / 13 HARM collision-apparatus-stale rows).
  - [detectors/eval.py](detectors/eval.py) extended with detection-level
    precision/recall/**F0.5** (β=0.5, Grundkiewicz-style), **FPR** against the
    nochange whitelist, and a **harm metric** (fraction of the 13 HARM rows a
    corrector wrongly proposes to "fix") — plus a real FP=0 filing gate (nonzero
    exit code on violation, previously print-only). Measured result: the
    underlying detectors flag 77–100% of the exact collision/apparatus/stale rows
    the do-not-file catalogue exists to protect — direct evidence for A44's own
    "do-not-file catalogue is the real product" thesis.
  - [detectors/irr_cross_family.py](detectors/irr_cross_family.py) — a
    cross-family blind second-annotator script (non-Anthropic judge via any
    OpenAI-compatible endpoint, e.g. DeepSeek) for the IRR sample, addressing the
    self-enhancement-bias confound in the existing Sonnet/Opus (same-family) IRR
    design. Built and dry-run verified; the actual annotation run is pending an
    `LLM_API_KEY` (none configured on the host that built this).
  - [detectors/irr_agreement.py](detectors/irr_agreement.py) generalized to report
    a cross-family agreement section alongside the existing within-family one
    (degrades gracefully when the cross-family run hasn't happened yet); regression
    checked against the existing κ=0.336/0.663 figures.
  - [corrections_draft/irr/HUMAN_ANCHOR_NEEDED.md](corrections_draft/irr/HUMAN_ANCHOR_NEEDED.md)
    — flags the outstanding gate: both existing kappas are LLM-only inter-rater
    comparisons, not yet licensed against an independent human-labelled seed set.
    A human should decide whether to produce that ~30-row seed before submission.
  - [papers/A44_body_grounded_triage_paper.md](papers/A44_body_grounded_triage_paper.md)
    reframed on the GEC/GED/confusion-set spine (Fable 5, `claude-fable-5`,
    register adjudication per ruling D1), with the related-work citations above
    added and the two live References defects (missing Artstein & Poesio,
    fabricated ISCLS 2026) resolved.

## [1.52.0] - 2026-07-12

### Added
- **[docs/WEB_SUGGESTER_SPEC.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/WEB_SUGGESTER_SPEC.md)
  (H828, rulings D1/D6/D13)** — the design spec for the Q1-2027 web spellchecker's suggestion
  engine: an [Oflazer 1996](https://aclanthology.org/J96-1003.pdf) error-tolerant FST traversal
  (turning the vendored Vidyut kosha/stems from a *validator* into a *suggestion generator*) over
  the 431,596-headword union trie, ranked by a [Brill & Moore 2000](https://aclanthology.org/P00-1037/)
  noisy-channel model (string-edit channel × DCS frequency prior × the measured
  [confusion_weights.json](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/confusion_weights.json)),
  with the do-not-file catalogue as a variant-aware accept list. Reuse map (in-repo assets vs the
  two ACL algorithms + app to build), differentiators, licensing guards (Vidyut MIT embeddable; do
  NOT ingest LibreOffice/GPL wordlists), the ISCLS demo hook, an 8-item build breakdown, and 5
  parked open questions. **Spec only — no build** (D13 defers it past the ≥300-corrections
  north-star). Authored by Opus 4.8 (`claude-opus-4-8`).

## [1.51.0] - 2026-07-10

### Added
- **[detectors/meter/GRETIL_UPSTREAM_REPORT.md](detectors/meter/GRETIL_UPSTREAM_REPORT.md)
  (H456, ruling D8)** — the verified GRETIL corrections report: all 124 bigram-screen loci
  hand-checked against the raw e-texts → **60 verified error loci across 7 texts** (incl. two
  systematic classes: ḥ-for-vowel conversion corruption in the Vālmīki-Rāmāyaṇa southern-2 +
  108-buddhist-stotras, and an *agrya*→*agyra* transposition family across 7 loci in two
  files), 11 anomalous lines reported without a proposed fix, 53 flags documented as false
  positives (mantra bījas, BHS orthography, apparatus sigla, valid rare forms). Verification
  reversed two earlier guesses: `'hbiṣekṣyati` is a real e-text transposition (not a walker
  artifact) and `skmsauka`/`pvpadyā` are apparatus citation sigla (not corruption). The
  Göttingen email is drafted UNSENT in the Uprava outreach queue; M.G. sends.

## [1.50.0] - 2026-07-10

### Added
- **H454 scan-verification gate tooling (ruling D3 prep)** — the batched-PR switchover found
  **zero `y`-flipped rows in all 11 FILE-FIRST queues**, so change-file generation is gated on
  the human scan pass. Shipped the gate as one sitting instead of a file-editing chore:
  [detectors/gen_scanverify_sheet.py](detectors/gen_scanverify_sheet.py) generates an
  interactive voting sheet over all 109 fileable rows (entry-body evidence + verification note +
  Cologne scan deep-link per row; keyboard voting; localStorage persistence; decisions.json
  export), and [corrections_draft/apply_scanverify_decisions.py](corrections_draft/apply_scanverify_decisions.py)
  folds the votes back (`--apply` flips approved rows `n`→`y`, lists rejected rows for
  do-not-file routing; dry-run by default). `review/` gitignored. Change files, queue parking,
  and the #447 follow-up comment deliberately NOT produced — they require verified rows.

## [1.49.0] - 2026-07-10

### Added
- **A44 blind LLM second-annotator agreement study (H453, ruling D2)** — replaces the deferred
  human-IRR gate. All 122 [file_first_verified.tsv](corrections_draft/file_first_verified.tsv)
  rows re-annotated blind by Opus 4.8 (`claude-opus-4-8`, 10 parallel agents, fresh prompt,
  entry-body evidence only); **κ = 0.336 five-way, 99.2 % binary defect recognition (κ = 0.663)**,
  zero corrections rejected as wrong, EDITORIAL class reproduced at perfect recall. All 50
  disagreements decompose into collision-threshold (33) and evidence-threshold (16) *policy*
  differences + 1 decisiveness reversal — no misread evidence. The blind pass independently
  reproduced the editor's 02-07 PASS→SCAN-FIRST audit on 4 of the 5 downgraded SHS rows. New:
  [detectors/irr_build_inputs.py](detectors/irr_build_inputs.py),
  [detectors/irr_agreement.py](detectors/irr_agreement.py) (stdlib, exact rational arithmetic),
  [corrections_draft/irr/](corrections_draft/irr/) (blind annotations + generated stats). New
  paper section §4.6 + honest limitations rewrite; A44 3/5 → 4/5.

### Fixed
- **A44 stale verdict counts**: §4.5/abstract/data-statement printed the pre-audit 97/12 split;
  the committed TSV (and MG's 02-07 audit commit `ce8f4f7`) says **92 PASS / 17 SCAN-FIRST** —
  corrected everywhere, with the audit now described in §4.5. (The H453 handoff's guard cited
  the numbers in the reverse direction; the artifact governs.)

## [1.48.0] - 2026-07-10

### Added
- **[docs/PRIOR_ART.md](docs/PRIOR_ART.md)** — the H452 prior-art scan (roadmap Q3 item 1, ruling
  D1: Fable 5 `claude-fable-5` judgment gate). 12+ Sanskrit spellchecking tools/surfaces
  characterized with the five-column verdict (approach · data · license · maintenance ·
  reuse-or-avoid), every claim fetch-backed. Headlines: the netlify spellchecker identified as
  **Prasanna S., ICON 2022** ([2022.icon-main.35](https://aclanthology.org/2022.icon-main.35/),
  source unpublished, dormant); **LibreOffice bundles a 543,758-entry `sa_IN` Hunspell pair since
  01-2025** with formally unsettled licensing (eval baseline only — no ingest); no maintained
  flag-and-suggest Sanskrit spellchecker exists — the Q1-2027 web app's niche is unoccupied.

### Fixed
- **A44 mis-citation** ([papers/A44_body_grounded_triage_paper.md](papers/A44_body_grounded_triage_paper.md)
  §2 + References): the "contextual spell-checker for Sanskrit demonstrated at ISCLS 2024" does not
  exist in that volume; corrected to Prasanna (ICON 2022) with the over-flagging/precision-collapse
  contrast made explicit. A37 §2 gained the object-language delimiting paragraph + reference.

### Changed
- [ROADMAP_2026_2027.md](ROADMAP_2026_2027.md) Q3 item 1 ticked ✅ (done 10-07-2026, H452).

## [1.47.0] - 2026-07-10

### Changed
- **[ROADMAP_2026_2027.md](ROADMAP_2026_2027.md) — revision 2**, re-interviewed with M.G. after
  eight days of execution diverged from revision 1 ([PR #25](https://github.com/drdhaval2785/SanskritSpellCheck/pull/25)).
  Eight rulings (D1–D8), each recorded with its rationale:
  **D1** Fable 5 (`claude-fable-5`) is scoped to **judgment gates only** (paper referee/author passes,
  prior-art synthesis, triage adjudication); Sonnet 5 (`claude-sonnet-5`) classifies, Opus 4.8
  (`claude-opus-4-8`) confirms, mechanical build work is Sonnet's — supersedes the expired
  "until 08-07-2026" window.
  **D2** A44's blocking human-IRR gate is replaced by an **LLM second-annotator agreement study**
  (Cohen's κ + disagreement taxonomy), reported as part of the paper's contribution; keeps the
  31-12-2026 IJL submission. The human-annotator recruit stays deferred.
  **D3** Corrections delivery switches from [CORRECTIONS#447](https://github.com/sanskrit-lexicon/CORRECTIONS/issues/447)
  (posted 02-07, **eight days with zero comments**) to **monthly consolidated PRs** of XML-validated
  `updateByLine` change files. `csl-orig` stays read-only to agents.
  **D4** The over-delivered meter track (5 GRETIL sections, [SECTIONS_DATASET.md](detectors/meter/SECTIONS_DATASET.md),
  [GRETIL_TEXT_TYPOS.md](detectors/meter/GRETIL_TEXT_TYPOS.md)) **folds into A47** as a joint
  sound/metre paper rather than becoming a separate publication.
  **D5** Anuprāsa stays Q1 2027, so **A47 drafts Q2 2027 and submits Q3 2027** — past this roadmap's
  horizon, opening the 2027–2028 plan.
  **D6** All four product shapes kept, sequenced cheapest-first: Zenodo dataset → PyPI package →
  web app → Cologne integration.
  **D7** The union-across-runs recall harvest drops from "generous budget" to **three dicts**
  (SHS/YAT/ACC), with the recall gain **measured** rather than assumed — tier-A precision is
  near-zero on mature dictionaries.
  **D8** The typos found in GRETIL's *own* e-texts are **reported upstream immediately**, not held
  back for A47's publication priority.
- Roadmap now carries an explicit **non-goals** section (what was considered and ruled out), so
  future sessions stop re-proposing the closed paths, and its banned HTML dated-header/byline is
  converted to plain Markdown per the authored-MD contract.

### Added
- Four executable handoffs wired into the Uprava registry and GTD:
  **H452** prior-art scan → `docs/PRIOR_ART.md` (the lead Q3 item — it unblocks the web-app design
  *and* the related-work sections of both A37 and A44) · **H453** the A44 agreement study ·
  **H454** the batched-PR switchover · **H456** the GRETIL typo report.

## [1.46.0] - 2026-07-02

### Added
- **Fable 5 referee reviews of both papers** —
  [papers/A37_review_fable5.md](papers/A37_review_fable5.md) and
  [papers/A44_review_fable5.md](papers/A44_review_fable5.md): substantive pre-submission
  reviews (argument/framing/venue-fit, prioritized fix lists) by Fable 5 (`claude-fable-5`)
  within the trial window. A37 headline risks: empty related-work vs stylochronometry,
  "law" overclaim (Latin zero overdetermined), PW/PWG non-independence in the n=5 correlation,
  §4.4 gradient-vs-saturation inconsistency. A44 headline: reframe for IJL, fold in the 02-07
  verification (collision = a new fifth candidate class), fix bare model attributions, cite
  eval.py; IRR remains the blocking human gate. Estimated two sessions each to 4/5.
- **Judge spot-check recorded in [VERIFICATION_2026_07.md](corrections_draft/VERIFICATION_2026_07.md):**
  10/10 seeded cross-dict sample of checker-PASS rows re-confirmed against `csl-orig` by
  Fable 5 after posting #447; side-flag: `YAT zazWimatta` likely carries the same `zW→zw`
  defect (future batch).

## [1.45.0] - 2026-07-02

### Changed
- **The umbrella issue is LIVE:**
  [sanskrit-lexicon/CORRECTIONS#447](https://github.com/sanskrit-lexicon/CORRECTIONS/issues/447),
  posted 02-07-2026 with M.G.'s explicit authorization — the payoff milestone of the whole
  triage effort (roadmap §Q3 items 1–2 complete). The committed
  [CORRECTIONS_umbrella_issue.md](corrections_draft/CORRECTIONS_umbrella_issue.md) now carries
  the POSTED banner and remains the source of record for the issue body. Next: human
  scan-verification (SHS → YAT → ACC) and maintainer follow-up on the issue; change-file drafts
  on request; `csl-orig` application stays human-gated.

## [1.44.0] - 2026-07-02

### Added
- **[corrections_draft/CORRECTIONS_umbrella_issue.md](corrections_draft/CORRECTIONS_umbrella_issue.md)**
  — the complete umbrella-issue body for the verified queue, M.G.-approved format: per-dict
  sections (biggest first), each with Proposed / Scan-first / Editorial (merge-vs-respell)
  tables, in-entry evidence and scan links per row, DROP+DNF audit appendix. **92 proposed +
  17 scan-first + 11 editorial across 11 dicts** (the 5 weak-evidence SHS rows were reclassified
  PASS→SCAN-FIRST per M.G., TSV updated). NOT posted — M.G. posts to
  [sanskrit-lexicon/CORRECTIONS](https://github.com/sanskrit-lexicon/CORRECTIONS/issues).

### Fixed
- **Model-attribution erratum (same-day):** today's research/verification subagents ran on the
  `sonnet` alias, which resolves to **Sonnet 5 (`claude-sonnet-5`)** in the current environment —
  earlier 1.42.0/1.43.0 entries and docs said "Sonnet 4.6" from a stale alias→version mapping.
  Corrected in place across changelog/docs/TSV/roadmap/.ai_state (June triage runs remain
  Sonnet 4.6 — correct for their date). Lesson encoded in the roadmap model-budget row: resolve
  the alias against the CURRENT env mapping at run time, never from memory.

## [1.43.0] - 2026-07-02

### Added
- **[docs/CHANDAS_ANUPRASA_PRIOR_ART.md](docs/CHANDAS_ANUPRASA_PRIOR_ART.md)** — survey grounding
  the planned **batch chandas validator** (new detector family: meter breaks = suspect-text
  signal over GRETIL/DCS verse corpora) and the reuse of the UoHyd **Anuprāsa Identifier**
  (ISCLS 2024; code unpublished, algorithm fully specified → clean-room SLP1 reimplementation).
  Converged recommendation: **skrutable** (has a "Scan GRETIL" batch mode + per-pāda
  `problem_syllables` diagnostics) primary, **`chanda`/Chandojñānam** (per-syllable Levenshtein
  edit-ops, 98.2 % on corrupted verses) as cross-validator; both licenses need clarification;
  no public UoHyd chandas tool exists — the student code is acquired via direct contact.
  Roadmap updated: tiny skrutable+chanda pilot **now** (Q3), full detector + anuprāsa
  reimplementation in Q1 2027. Also flags ISCLS items to track (2024 "Contextual Spellchecking
  for Sanskrit" demo; 2026 "Proof-Reader Effect of LLMs in Sanskrit OCR"; Patel & Kulkarni
  word-sense alignment; HANSEL; CHANDOMITRA; varṇacitra).

## [1.42.0] - 2026-07-02

### Added
- **FILE-FIRST verification gate ([corrections_draft/file_first_verified.tsv](corrections_draft/file_first_verified.tsv)
  + [VERIFICATION_2026_07.md](corrections_draft/VERIFICATION_2026_07.md)).** All 122 candidates
  re-verified against the `csl-orig` entry text (4 Sonnet 5 `claude-sonnet-5` checker agents; Fable 5 adjudicated
  the 28 flags): **97 PASS · 12 SCAN-FIRST · 11 EDITORIAL · 1 DNF · 1 DROP**. Key discoveries:
  ~9 % of candidates are *collisions* (the right spelling already exists as its own entry — YAT
  dual-listings, MW `kattfRa`, PWG's `duzWu` errata note, PW's `*hemana`) needing a merge-vs-respell
  editorial decision, not a respell; `SHS kARqapfzwa` already fixed upstream (queue decays ~0.8 %/wk);
  `YAT RiS→niS` is ṇopadeśa notation → do-not-file. The umbrella issue gains a third,
  editorial-decision section. MW's "4 of 1,954" restates as 2 scan-first + 2 editorial.

### Fixed
- **Paper fact-check corrections** (Sonnet 5 `claude-sonnet-5` fact-checkers vs committed data, ~75 claims
  verified): A44 "largest do-not-file contributors" list was missing third-place BHS (294);
  A37 + [docs/ORTHO_DRIFT_FINDINGS.md](docs/ORTHO_DRIFT_FINDINGS.md): en_GB dic is 56,571 stems
  (was "~86 k"), corpus is the Cologne 33 (was "~36"), "one to three orders of magnitude" →
  "up to three" with the honest ~5× floor at the German–English boundary, "~13 decades" →
  1832–2009, "ten 19th-c. dictionaries" → nine dated + the undated Apte held out.

## [1.41.0] - 2026-07-02

### Added
- **[ROADMAP_2026_2027.md](ROADMAP_2026_2027.md) — the 1-year plan (July 2026 → June 2027).**
  Decided in an interview with M.G. (02-07-2026): file the 122 FILE-FIRST typos NOW without the
  OCR gate (one umbrella issue, human posts/verifies); ≥300 corrections filed by 30-06-2027;
  both papers (A44→IJL, A37→DH venue) submitted by Q4 2026; productize in four shapes (PyPI,
  web app in a new GH-Pages repo, Cologne integration, Zenodo dataset); entry-body pilots
  (deterministic SHS, then LLM MW-citations); union-across-runs recall; quarterly-deep +
  monthly-light cadence (CI detects, agent triages). Fable 5 (`claude-fable-5`) judges until
  08-07-2026, then Sonnet 5/Opus 4.8 hybrid. [ROADMAP.md](ROADMAP.md) marked superseded as
  the forward plan.

### Fixed
- **Restored the detailed changelog** — commit `78cc59d` (30-06-2026) had replaced this file's
  entire 1.0.0–1.40.0 history (967 lines, the repo's audit trail) with a generic 18-line
  "0.1.0" stub. Restored from the last good revision (`4a80062`) and promoted the pending
  [Unreleased] work to this 1.41.0 entry.

### Added (pre-roadmap engine + study work, formerly [Unreleased])
- **Ortho-drift O6 — language-general reform map from a diachronic corpus (French, via FreEMnorm).**
  New [detectors/extract_freem_pairs.py](detectors/extract_freem_pairs.py) harvests historical→modern
  French pairs from the openly-licensed [FreEMnorm](https://github.com/FreEM-corpora/FreEMnorm) parallel
  corpus (55 texts, 1606–1697; staged gitignored under `external_src/freem/`). The DTA pipeline
  **generalises**: token-align → 9,973 pairs → ≥20× → 407 → `merge_reform_pairs.py fr` dic-validates
  **236** into the French map (18→254), all textbook EMF→modern (`ie→je`, `vn→un`, `estre→être`,
  `avoit→avait`). **But the map doesn't transfer to the target dicts:** on BUR (1866) / STC (1932) it
  raises drift 0.31→3.43 / 0.02→2.59, **~90 % false positives** — `moy.` (=*moyen* abbrev.) read as
  `moy→moi` (763), `dés` (="dice") / Latin `tres` read as `dès`/`très`, IAST `pha`/`phull` misfired by
  `ph→f`. Epoch/register/language mismatch (17th-c. literary prose vs 20th-c. IAST-laced glosses).
  Method language-general; map epoch-bound — kept the validated pairs
  ([fr_reform_freem_pairs.tsv](ortho_drift/fr_reform_freem_pairs.tsv)) + banked the BUR/STC FreEM runs
  (`*_drift_report.freem.txt`), but **froze** the canonical fr map/figures (as with O3). Written up in
  `docs/ORTHO_DRIFT_FINDINGS.md` ("O6"). Closes O6 in `H008-Opus_SanskritSpellCheck_NEXT_23.06.26.md`.
- **Ortho-drift O4 — drift-rate as a dating tool.** New [detectors/drift_dating.py](detectors/drift_dating.py)
  calibrates drift/1k ↔ publication year across the five languages (Spearman + leave-one-out year
  prediction + a symlog scatter, `ortho_drift/drift_dating.png`). Finding: drift/1k is a **coarse,
  regime-bounded** dater. (1) No cross-language calibration — the rate is regime-stratified (Russian
  358 ≫ German 2.5–10 ≫ English/French 0–0.46 ≫ Latin 0). (2) Within a language, the **legislated**
  German gradient is tight (Spearman −0.975, LOO **±15 yr**, R²=0.87) but the **convention** English
  one is editor-noisy and saturated (−0.642, ±40 yr; **7 dicts read exactly 0.00 across 1890–1990**;
  Macdonell's `-xion` puts MD 1893 above BEN 1866). (3) The **per-era composition** out-dates the
  scalar rate: a pre-1901 rate-fit mis-dates SCH-1928 to 1896 (−32 yr), but its `ss`-dominant
  composition pins it post-1901/pre-1996 (the O3 control). Written up in `docs/ORTHO_DRIFT_FINDINGS.md`
  ("O4" section). Closes O4 in `H008-Opus_SanskritSpellCheck_NEXT_23.06.26.md`.

### Changed
- **`ocr_verify.py` — admin-free easyocr OCR backend (O7 prep).** tesseract is admin-gated on some
  machines (choco/conda need elevation); added an **easyocr** fallback (neural Devanagari, `['hi']`,
  no system binary) used when tesseract is absent — verified `EASYOCR_OK=True`, Reader inits + `readtext`
  runs. Docstring notes the Cologne `servepdf.php` IP-throttle (429). **O7 measurement still pending:**
  the pilot ran end-to-end except the scan fetch, which 429s hard on this IP (persists at 20 s spacing +
  browser UA) — deferred until the server cooldown; rerun `python ocr_verify.py <DICT>_file_first_sf.txt N`
  then read the CONFIRM/DENY/UNCERTAIN split. See O7 in `H008-Opus_SanskritSpellCheck_NEXT_23.06.26.md`.

### Investigated (no code change)
- **O2 / R6 — vidyut inflection-aware attestation is not a reliable "real word" signal.** With vidyut
  0.4.0 + kosha data on disk, tested whether `Kosha.get` (pada lookup) + the 205 k vendored pratipadika
  stems could mark real words as attested where DCS band-0 failed. **Refuted both ways:** it still
  misses real words (`patra`: DCS 0, stem ✗, pada ✗) and it over-attests real errors — **34 % of
  tier-A and 47 % of tier-B known o_vs_O real-error suspects are valid vidyut stems/padas** (a
  misspelling often coincidentally lands on a valid form; in tier B attestation fires *more* on errors
  than on others). A "demote if attested" rule would drop ~404 known real errors (vs R5's 60). **No
  scorer change** — surface attestation (DCS *or* vidyut) is orthogonal to typo-vs-real; only the body
  settles it. Written up as R6 in `docs/HYPOTHESES.md`. Closes O2 in `H008-Opus_SanskritSpellCheck_NEXT_23.06.26.md`.
- **O1 / R5 — a model-free body lookup in the ranker cannot demote real-word minimal pairs.**
  Tested whether a cheap deterministic `EntryIndex` body check could close R1's gap (the engine
  mis-ranking `patra`/`pAtra`) without an LLM triage. Probed every candidate body signal against the
  3,884 known o_vs_O pairs (the real errors that must stay) in tiers A/B **before** changing code —
  all three fail: (1) body presence/length doesn't discriminate (known errors carry full glosses at
  83 % vs 82 %); (2) DCS attestation can't mark real words — `patra`/`vata` are band-0 *real* words
  DCS-2021 omits; (3) suspect↔suggestion body overlap doesn't separate (89 % vs 90 %, inverted in
  tier B). The tightest `patra`-signature rule still demotes 60 known real errors (20 % of tier-B
  known pairs) for 244 unverified others. **Made no change to `score_tier`** — the body must be read
  (LLM triage), not measured; R1 is a semantic ceiling. Written up as R5 in `docs/HYPOTHESES.md`
  (O1 refuted). Closes O1 in `H008-Opus_SanskritSpellCheck_NEXT_23.06.26.md`.

### Changed
- **Ortho-drift O5 — split the typographic æ/œ ligature out of the reform-drift rate.**
  `detectors/ortho_drift.py` gains a `NONREFORM_ERAS = {'ligature'}` set; the `ligature` class
  (`mediæval→medieval`, `æther→ether`) is still counted as its own era column but **excluded from
  the headline reform-drift/1k** — it's a print-shop convention, not a dated reform. Effect is large:
  the mid-tier EN dicts were almost all ligature. SHS 0.31 → **0.08**, GST 0.31 → **0.04**, MW72/AP90
  ~0.09 → **0.01/0.00** (AP90 was 100 % ligature), VEI 0.06 → **0.00**; WIL 0.57 → **0.46** (its drift
  is real Johnsonian `-ick`/`-xion`, not ligature). True EN reform-drift now concentrates in two real
  classes (`-ick`, `-xion`) on a cleaner gradient (WIL 0.46 ≫ MD 0.14 > MW 0.01 → ~0), and **all five**
  modern recency-control anchors read 0.00. Re-ran all 15 EN dicts (per-era columns reproduce the
  frozen values exactly; `en_reform_map.tsv` byte-identical); updated `docs/ORTHO_DRIFT_FINDINGS.md`
  (EN tables + the tier summary) and `ortho_drift/en_drift_summary.tsv`. Non-EN summaries unaffected
  (no ligature era). Closes O5 in `H008-Opus_SanskritSpellCheck_NEXT_23.06.26.md`.

### Added
- **Ortho-drift O3 — re-ran the German cluster (PW/PWG/GRA/CCS/SCH) against the full 15,685-form
  `de_reform_map.tsv`** (was 2,823 at the frozen deterministic-pass snapshot). Finding: absolute
  drift/1k roughly triples (PW 10.26 → 28.59, SCH 2.52 → 9.77) and the monotone publication-date
  gradient at the top flattens (GRA 27.69 now edges above PWG 26.84) — the DTA long-tail conflates
  generic early-modern/loanword variation with the dated 1901/1996 reforms. **But the SCH-1928
  era-dating control is fully intact**: SCH stays uniquely `ß`-dominant (1996-ss 446 ≫ 1901-th 89),
  pre-1901 dicts stay `th`-dominant — the relative era signature is robust to the 5.5× expansion.
  This **vindicates the freeze**: the per-dict gradient stays at the deterministic-pass snapshot;
  the expanded map is a search-normalization recall asset, not a drift-rate metric. Expanded-run
  outputs banked as `ortho_drift/de_drift_summary.expanded_map.tsv` +
  `ortho_drift/<DICT>_drift_report.expanded_map.txt`; the committed frozen reports are unchanged.
  Written up in `docs/ORTHO_DRIFT_FINDINGS.md` (new "O3" subsection). Closes O3 in `H008-Opus_SanskritSpellCheck_NEXT_23.06.26.md`.
- **`docs/HYPOTHESES.md` — project hypothesis ledger.** Documents in detail every testable
  hypothesis behind the toolset, with verdicts and evidence: **7 confirmed** (body = ground truth;
  tier-A precision near-zero on mature dicts; do-not-file is the deliverable; drift = f(reform type);
  the metric dates a dict's epoch; corpus-norm + frequency yields clean reform pairs; external-source
  shim), **4 refuted** (corpus/confusion tier-C promotion surfaces real minimal pairs; vidyut as a
  tier promoter; re-running improves recall; base DTA TEI carries the reform layer), and **7 open**
  (inline body check in the ranker, drift-rate as a dating tool, ligature-vs-reform split,
  language-general reform maps, …). **USE_CASES.md** gains §11–§14 (body-grounded triage, external
  sources, ortho-drift, reform-pair harvest) + table/links.

### Fixed
- **Campaign mode regression:** `detectors/run_campaign.py` now matches the current
  `run_all.score_tier()` signature, preserves the shared row tuple order used by
  review HTML, and has a lightweight regression check for the campaign row shape.
- **`make_changefiles.py` mis-parsed FILE-FIRST sf comment lines.** Feeding a
  `<DICT>_file_first_sf.txt` directly manufactured junk "dicts" from its `;`-comment
  header + auto-commented `REVIEWED-OUT` lines. Now skips `;`/`#` lines and requires an
  alphanumeric dict code — so the FILE-FIRST queues feed straight into the CORRECTIONS
  draft-changefile prep (unblocks the umbrella-issue handoff, Task 1).

### Added
- **DTA long-tail merge (Task 4) — German reform map 2,823 → 15,685 forms.** The Deutsches Textarchiv
  `lingattr-TEI` corpus (5,285 texts, 1473–1900; `<w … norm="MODERN">surface</w>` with the DTA::CAB
  normalization layer) was harvested by the new [detectors/extract_dta_pairs.py](detectors/extract_dta_pairs.py)
  (streams the 2.5 GB zip, skips corrupt members): **596 k** distinct `surface≠norm` pairs → kept those
  attested **≥ 20×** (43,579) → `merge_reform_pairs.py` dic-validated (`old ∉ de_DE & new ∈ de_DE`) →
  **+12,862 accepted** (`vnd→und`, `bey→bei`, `Theil→Teil`, `gantz→ganz`, `krafft→kraft`, `thaler→taler`,
  `fuss→fuß`, `october→oktober`; the ≥20× cut drops OCR singletons like `aaal→all`). The corpus zip +
  extracted TSV stay gitignored under `external_src/`; only the grown `de_reform_map.tsv` is committed.
  Per-dict drift reports left frozen (recall banked in the map). Closes the ortho-drift long-tail item.
- **Tier-C ranking calibration (Task 2) — negative result + ranking nudge.** Tested the proposed
  corpus+confusion tier-C→B promotion (suggestion DCS band ≥ 4, suspect band 0, high-weight confusion):
  it lifts 602 `dict_vs_corpus`-alone candidates C→B but **surfaces real Sanskrit minimal pairs as typos**
  (`patra`=leaf vs `pAtra`=vessel; `vata`/`rAtrI` are real MW headwords `<L>185376`/`<L>177124`) —
  vowel-length pairs only the body-grounded triage can adjudicate, and `suspect_band==0` is unreliable
  (DCS gaps). The corpus-attested single-detector pairs (band ≥ 3) are **already tier B**, so the
  C-stuck known o_vs_O pairs (99 % `spell_correct`, band 0–2) don't benefit. **Rejected the tier
  promotion**; kept a documented `CORROB_*` **score nudge** (rank corroborated candidates higher
  within their tier). Tiers unchanged (A=5371/B=4693/C=4688), `eval.py` FP=0. Write-up in Task 2 of
  [H008-Opus_SanskritSpellCheck_NEXT_23.06.26.md](H008-Opus_SanskritSpellCheck_NEXT_23.06.26.md).
- **Ortho-drift within-EN recency control (Task 3 done).** Registered the five modern-leaning English
  dicts **PD / PE / BHS / IEG / VEI** as `en` in `ortho_drift.py`'s `LANG_OF` and ran them against the
  `en_GB` reference (`ropensci/hunspell` `en_GB.dic`, staged at `external_src/hunspell/`, gitignored;
  `_dic()` now falls back there when the Adobe bundle is absent). Result: **PD (1976–2009, 1.32 M gloss
  tokens) = 0.00 drift/1k**, PE/BHS/IEG = 0.00, VEI 0.06 (residual æ ligatures) — the modern end of the
  gradient sits at ≈ 0, confirming the metric dates orthography. Full English picture is now a monotone
  recency gradient WIL 1832 (0.57) → MW 1899 (0.01) → modern (0.00). Written up in
  [docs/ORTHO_DRIFT_FINDINGS.md](docs/ORTHO_DRIFT_FINDINGS.md); 10-dict table left stable, 5 rows added.
- **Handoff roadmap rewritten** ([H008-Opus_SanskritSpellCheck_NEXT_23.06.26.md](H008-Opus_SanskritSpellCheck_NEXT_23.06.26.md)) as a prioritized 4-task
  roadmap: (1) draft the CORRECTIONS umbrella issue for the 122 FILE-FIRST typos (OCR-prefiltered,
  pilot-SHS-then-scale), (2) tier-C calibration, (3) ortho-drift recency control, (4) DTA/RIDGES
  long-tail merge — each with a paste-ready fresh-chat brief + its data prerequisite.

## [1.40.0] - 2026-06-24

### Added
- **PD triaged on source 1 — ALL 33 dicts done.** The Deccan College *Encyclopaedic Dictionary*
  (English, 107,630 entries): 1,007 tier-A → **0 fileable typos**, 888 real words, **116
  documented-intentional** — the **richest do-not-file list of any dict** (varia-lectio 66,
  wrong-reading 16, cross-reference 22, other 12). As a historical-principles lexicon PD deliberately
  records non-standard attested spellings with full citations + an explicit verdict (`agneyI` "w. r.
  for *āgneyī*", `aGni` v.l. `aGniya`), so filing any would corrupt its editorial record. The lone
  typo-unsure (`akzAMsa`) was source-refuted (own `[MW]` headword); 0 unlocatable. Package +
  [readme](corrections_draft/PD/readme.md) under [corrections_draft/PD/](corrections_draft/PD/).
  A second PD source is still expected — a re-run later only refines the do-not-file list.

### Changed
- **Suppression list → 33 dicts, 2297 unique** (PD +116 do-not-file headwords). Re-ran
  `run_all.py --rerun`; `eval.py` false-positives back to **0** for all four correctors (tier-C
  known-pair recall steady: A=690, B=243, C=918).

## [1.39.0] - 2026-06-24

### Added
- **PD wired in via an external-source mechanism — now triageable.** PD (the Deccan College
  *Encyclopaedic Dictionary of Sanskrit on Historical Principles*, English, 1976–2009) is the one
  Cologne-listed dict **not in the `csl-orig` merge**, which blocked its body-grounded triage. New
  `triage_util.source_file(dict_code)` resolver prefers a gitignored `external_src/<dict>/<dict>.txt`
  staging file and falls back to `csl-orig/v02/<dict>/<dict>.txt` — behaviour-preserving for every
  existing dict (`csl_dict_file` and `build_entry_index` both route through it; test_triage.py 25/25,
  MW still resolves to csl-orig). PD registered `en` in `triage_lang.py`.
- **`detectors/get_external_source.py`** — fetch + unzip a non-csl-orig dict source into
  `external_src/`. First source: PD's `pdtxt.zip` from the
  [PDScan 2020 edition](https://sanskrit-lexicon.uni-koeln.de/scans/PDScan/2020/web/index.php)
  (`pd.txt`, 55 MB, **107,630 entries**). The script has a slot for PD's **expected second source**.
- **`external_src/` gitignored** — the PD text is CC BY-NC-SA 3.0 (© The Sanskrit Library / Thomas
  Malten); this repo hosts QA tooling + do-not-file lists, not third-party dictionary text. Re-stage
  on a fresh clone with `python detectors/get_external_source.py PD`.
- **Verified ready:** `triage_dict.py PD` builds the package — **1,007 tier-A, 920 to body-judge, 0
  unlocatable** (every PD headword resolves in the source). The triage run itself is **held for PD's
  second source** so it isn't redone; documented in [corrections_draft/PD/readme.md](corrections_draft/PD/readme.md).

## [1.38.0] - 2026-06-24

### Added
- **BUR + STC + BOP triage — 32/33 dicts (only PD remains).** The three cross-language dictionaries,
  all **0 fileable typos** — the expected result for mature foreign-gloss lexica:
  - **BUR** (Burnouf, *Dict. classique sanscrit-français*, 1866, `fr`): 162 tier-A → 147 located → 0
    fileable, 123 real words, **20 do-not-file** (17 root cross-references `cf.`, 3 other). All 4
    classified TYPOs were **reviewed out** by the Opus gate — two because the entry's own gloss spells
    the suspect (`aśunya`, `kamaṭa`), two as vṛddhi derivatives (`smāśānika`←śmaśāna, `viṣṭala`←sthala).
  - **STC** (Stchoupak–Nitti–Renou, *Dict. Sanscrit-Français*, 1932, `fr`): 111 tier-A → 93 located →
    0 fileable, 75 real words, **9 do-not-file**. The Opus review held back the b/v (`bibhīṣaṇa-` =
    Vibhīṣaṇa) and d/ḍ (`pra-dīna-`) candidates **for the scan** rather than filing them.
  - **BOP** (Bopp, *Glossarium Sanscritum*, Latin, 1847, `la`): 39 tier-A → 32 located → 0 fileable,
    24 real words, **6 do-not-file**. Latin = the study's negative control (no orthographic reform);
    most flags are feminine `-ā` entries (`kalaSA`, `argalā`) or A-grade derivatives BOP gives own entries.
  - Packages + per-dict `readme.md` under [corrections_draft/](corrections_draft/).
- **`fr`/`la` profiles got test coverage + a missing STC marker.** Added BUR/STC/BOP marker cases to
  `detectors/test_triage.py` (now **25 checks**). The cases surfaced a gap: STC writes its correction
  directive as **`lire <form>`** (infinitive), which the `fr` `wrong-reading` regex (only `\blisez\b`)
  missed — added `\blire\s+[{˚]` (anchored on a following form-marker so plain glosses like "action de
  lire" don't match). Re-synthesis regroups STC's `valmi`/`vinivarhaṇa` under wrong-reading (2 of 9).

### Changed
- **Suppression list → 32 dicts, 2181 unique** (BUR +20, STC +9, BOP +6 do-not-file headwords folded
  into `nochange/do_not_file_suppress.txt`). Re-ran `run_all.py --rerun` so the correctors re-filter
  against the grown whitelist; `eval.py` false-positives back to **0** for all four correctors
  (tier-C known-pair recall steady: A=696, B=248, C=907).

## [1.37.0] - 2026-06-24

### Added
- **VEI + MCI + PGN + KRM triage — 29/33 dicts.** Four small dicts:
  - **MCI** (mythical-name index, en): 41 tier-A → **10 fileable typos** + 11 real + 3 do-not-file.
    Unusually clean — each fileable is a headword keying error contradicted by the entry's *own
    repeated citations* (`Mahānadi` lemma but "mahānadī" in prose; `Dakṣināpatha` but
    "dakṣiṇāpathavāsin"; `Brahmopanisad` but "brahmopaniṣadaṃ"). Confirm+Review run; source-verified.
  - **VEI** (Macdonell–Keith Vedic Index, en): 43 → 0 fileable, 2 do-not-file, 34 attested terms.
  - **PGN** (inscription proper-name index, en): 21 → 0 fileable, 1 do-not-file, 8 names.
  - **KRM** (Kramadīśvara dhātupāṭha, `sa`): 47 → 0 fileable, 6 do-not-file, 37 roots. The ṇ-/ṣ-initial
    upadeśa-form roots (`Riji`, `zarja`) are deliberate Pāṇinian notation, not typos.
  - Packages under [corrections_draft/](corrections_draft/).

### Changed
- **Suppression list → 29 dicts** (VEI +2, MCI +3, PGN +1, KRM +6 do-not-file). `eval.py` false-positives stay **0**.

## [1.36.0] - 2026-06-24

### Added
- **INM + PE triage — 25/33 dicts.** Two proper-name indices, both **0 fileable typos**:
  - **INM** (Sörensen, *Index to the Names in the Mahābhārata*, en): 161 tier-A → 0 fileable,
    16 do-not-file, 123 named entities, 12 unlocatable. Includes Sörensen's deliberately-indexed
    wrong readings ("error in C. for…").
  - **PE** (Mani, *Purāṇic Encyclopaedia*, en): 158 tier-A → 0 fileable, 13 do-not-file, 138 named
    entities, 1 unlocatable. Dual-spelling headwords ("VAKANAKHA (BAKANAKHA)") = intentional.
  - Packages: [corrections_draft/INM/](corrections_draft/INM/), [corrections_draft/PE/](corrections_draft/PE/).

### Changed
- **Suppression list → 25 dicts** (INM +16, PE +13 do-not-file). `eval.py` false-positives stay **0**.

## [1.35.0] - 2026-06-24

### Added
- **IEG triage — 23/33 dicts.** Body-grounded triage of Sircar's *Indian Epigraphical Glossary*
  (registered `IEG: 'en'`). Of **162 tier-A**: **0 fileable typos**, 40 documented-intentional
  (cross-reference 21, other 19), 101 attested epigraphic terms, 3 unlocatable. Expected near-zero
  precision — IEG deliberately records inscriptional spellings (Prakrit doubling, retroflex/dental
  shifts, vowel/anusvāra variation) and cross-references Prakrit terms to their Sanskrit equivalents
  (`dāṇa` "same as dāna"). Package: [corrections_draft/IEG/](corrections_draft/IEG/).

### Changed
- **Suppression list → 23 dicts** (IEG adds 40 do-not-file). `eval.py` false-positives stay **0**.

## [1.34.0] - 2026-06-24

### Added
- **ACC triage — 22/33 dicts (22 fileable).** Body-grounded triage of Aufrecht's *Catalogus
  Catalogorum* (registered `ACC: 'en'`). Of **174 tier-A**: **22 body-confirmed fileable typos** in
  normalised work-titles (dropped long ā, vr→b, retroflex ḍ, sibilant/aspirate), 68 real titles/names,
  25 do-not-file, 25 eyes, 4 typo-unsure. Ran Confirm + Review via subagent with explicit *direction*
  and *faithful-colophon* checks — the gate excluded a reversed-direction pair (`aBijYAnaSAkuntala`,
  already correct) and redirect/vṛddhi/variant entries. Package: [corrections_draft/ACC/](corrections_draft/ACC/).
  - FILE-FIRST is DRAFT — verify each on the Aufrecht scan before filing.

### Changed
- **Suppression list → 22 dicts** (ACC adds 25 do-not-file). `eval.py` false-positives stay **0**.

## [1.33.0] - 2026-06-23

### Added
- **YAT triage — 21/33 dicts; a high-yield outlier (27 fileable).** Body-grounded triage of Yates'
  *Sanskrit-English Dictionary* (Calcutta, 1846; registered `YAT: 'en'`). Of **247 tier-A**: **27
  body-confirmed fileable typos (10.9%)** — second only to SHS — plus **32 b↔v pairs held for scan**,
  123 real roots/words, 13 eyes, 15 unlocatable, 1 do-not-file. Like SHS, a poorly-digitised
  19th-c. Bengal source: each fileable typo is fixed by the entry's own citation form (dental-n vs
  retroflex-ṇ, sibilant, aspiration, vowel-length). Ran the full **Confirm (source) + Review
  (false-positive gate)** phases via subagents. Package: [corrections_draft/YAT/](corrections_draft/YAT/).
  - ⚠️ **b↔v caveat:** Bengali orthography doesn't distinguish व/ब, so the 32 b/v candidates may be
    faithful to the print — held in TYPO-UNSURE, NOT filed, pending scan verification (व vs ब).
  - Cross-dict precision: SHS 37/246 · YAT 27/247 · PWG 12/497 · MW 4/1954 · … · BHS 0/713 · PUI 0/518.

### Changed
- **Suppression list → 21 dicts** (YAT adds 1 do-not-file). `eval.py` false-positives stay **0**.

## [1.32.0] - 2026-06-23

### Added
- **PUI triage — 20/33 dicts.** Body-grounded triage of the *Purāṇic Index* (proper names;
  registered `PUI: 'en'`). Of **518 tier-A** candidates: **0 fileable typos**, 21 documented-intentional
  (cross-reference 7, other 14), 467 real named entities, 6 unlocatable. Expected near-zero precision
  for a proper-name index — the flagged forms are attested Purāṇic names in their own spelling
  (`Brahmaṇa` = a Nāga, not brāhmaṇa). Package: [corrections_draft/PUI/](corrections_draft/PUI/).
  - Registered the remaining index dicts in `triage_lang._LANG` in one edit (PUI/INM/PE/YAT/ACC/IEG/
    MCI/PGN/VEI = en, KRM = sa) ahead of triaging them.

### Changed
- **Suppression list → 20 dicts**, [nochange/do_not_file_suppress.txt](nochange/do_not_file_suppress.txt)
  **2,020 → 2,041** unique. `eval.py` false-positives stay **0**.

## [1.31.0] - 2026-06-23

### Added
- **BHS triage — 19/33 dicts.** Body-grounded triage of Edgerton's *Buddhist Hybrid Sanskrit
  Dictionary* (registered `BHS: 'en'` in `triage_lang._LANG`). Of **713 tier-A** candidates:
  **0 fileable typos**, 294 documented-intentional (do-not-file: cross-reference 138, varia-lectio
  81, other 67, wrong-reading 6, in-composition 2), 415 real BHS words, 4 unsure. The expected
  near-zero precision for a specialized hybrid-Sanskrit lexicon — the flagged forms are deliberate
  hybrid/MIndic/metri-causa spellings or proper names Edgerton records on purpose. Package:
  [corrections_draft/BHS/](corrections_draft/BHS/) (readme + do-not-file + queue).
  - Cross-dict fileable precision: MW 4/1954 · PW 2/657 · VCP 1/563 · PWG 12/497 · SHS 37/246 · **BHS 0/713**.

### Changed
- **Suppression list refreshed to 19 dicts** — [nochange/do_not_file_suppress.txt](nochange/do_not_file_suppress.txt)
  grew **1,726 → 2,020** unique headwords (BHS's 294 folded in via `gen_do_not_file_suppress.py`).
  Verified: `eval.py` false-positives stay **0**; 0 suppressed headwords survive as candidates
  (unified candidates 15,323 → 15,029).

## [1.30.0] - 2026-06-23

### Added
- **Orthographic-drift findings write-up — the publishable capstone.** New
  [docs/ORTHO_DRIFT_FINDINGS.md](docs/ORTHO_DRIFT_FINDINGS.md) synthesises the completed 5-language
  ortho-drift study (German, English, French, Latin, Russian) into one standalone, citable artifact
  for a lexicography / DH audience: headline finding, method (transform-and-check), per-language
  results with the data tables, the SCH-1928 control, caveats, and a reproducibility note. Every
  figure verified against the committed `ortho_drift/*.tsv` / `*_drift_report.txt` data files before
  writing. Documentation only — never edits `csl-orig`.
  - **Headline:** drift magnitude = f(reform *type*) — legislated (Russian Kossovich 358/1k, German
    PW 10.26/1k) ≫ convention (English WIL 0.57 → MW 0.01, French BUR 0.31) ≫ none (Latin BOP 0),
    1–3 orders of magnitude between tiers.

## [1.29.0] - 2026-06-23

### Added
- **Do-not-file suppression layer — the durable triage deliverable, wired into the detectors.**
  The body-grounded triage emits, per dictionary, a `<DICT>_wrong_readings.txt` (the standing
  do-not-file list of spellings the dictionary documents *on purpose* — `w.r.`/`v.l.` apparatus,
  in-composition/sandhi forms, cross-references, grammatical/Vedic notes). New
  [detectors/gen_do_not_file_suppress.py](detectors/gen_do_not_file_suppress.py) collects the
  headword (left column) from all **18** triaged `*_wrong_readings.txt`, dedups, and writes
  [nochange/do_not_file_suppress.txt](nochange/do_not_file_suppress.txt) (**1,726 unique** of
  ~1,976 rows — the rest are cross-dict duplicates). Regenerate after triaging more dicts.

### Changed
- **`slp1util.load_whitelist()` now unions `nochange.txt` with the sibling
  `do_not_file_suppress.txt`** (if present), so all four correctors
  (`spell_correct`/`consensus`/`intra_dup`/`dict_vs_corpus`) self-suppress the documented-intentional
  forms. Provenance stays separate from the human-curated `nochange.txt`.
- **`run_all.py` aggregation filters the whitelist at the single choke point**, covering the
  **flaggers** too (`phonotactic`/`charset` never consulted the whitelist — e.g. the charset-flagged
  Vedic headword `arI|a` "not licked" leaked through). Unified candidates 15,377 → **15,323**.

### Verified
- `eval.py` false-positive check stays **0** for every corrector (whitelist grew 30,887 → 31,272).
- 0 of the 1,726 suppressed headwords survive in `combined_candidates.txt`.
- `do_not_file_suppress.txt` written UTF-8 **without BOM**. Documentation/tooling only — never edits `csl-orig`.

## [1.28.0] - 2026-06-17

### Added
- **External reform-pair merge (DTA/RIDGES-style ingest), dic-validated.** New
  `detectors/merge_reform_pairs.py` ingests any external historical→modern pair file
  (`old<TAB>new[<TAB>era]`) into `ortho_drift/<lang>_reform_map.tsv`, accepting a pair only if
  `old∉dic & new∈dic & old≠new` — the same transform-and-check guard, so hallucinations,
  dual-spellings and rejected proposals are filtered out.
  - First input: **14 documented 1901/1996 German reform pairs** harvested via WebFetch from the
    German Wikipedia reform articles (`ortho_drift/de_reform_web_candidates.tsv`) → de reform map
    **2,809 → 2,823** (`cigarre→zigarre`, `guitarre→gitarre`, `liqueur→likör`, `schloß→schloss`,
    `rauh→rau`, `stengel→stängel`, `redacteur→redakteur`, `desinficieren→desinfizieren`, …).
    9 correctly rejected (7 already mapped; `compagnie` is still a valid modern German word;
    `soziale` is an inflected non-stem).
  - WebFetch reaches the web but **can't bulk-download the DTA/RIDGES corpora** through its
    summariser — the tool is the ready wiring: drop a local DTA/RIDGES export (or give a row-list
    URL) to merge the long tail. Documentation only; never edits the sources.

## [1.27.0] - 2026-06-17

### Added
- **Phase 2: English orthographic-drift — the 10-dict cluster.** Added the `en` profile to
  `ortho_drift.py` (reference = **en_GB**, so British `honour`/`-ise`/`-re` are correctly *not*
  flagged; the tokenizer now strips `<s>…</s>` Sanskrit, which MW-family dicts use instead of
  `{#…#}`). Ran MW/MW72/AP/AP90/WIL/BEN/GST/CAE/MD/SHS (`en_drift_summary.tsv`, 71-form `en_reform_map.tsv`).
  - English drift is **convention-based and editor/age-dependent** (no legislated reform): Wilson
    (1832, oldest) tops at **0.57/1k** with Johnsonian `-ick` (`garlick→garlic`, `musick`, `aquatick`),
    the æ ligature (`æther→ether`, `chamæleon→chameleon`) and `reflexion→reflection`; the
    heavily-standardised MW (1899) ≈ **0.01** and AP/CAE = **0**. Range 0.00–0.57/1k.
  - **Completes the 5-language picture. Drift magnitude is a function of reform _type_:** legislated
    (Russian 358, German 10 /1k) ≫ convention (English ≤0.57, French ≤0.31) ≫ none (Latin 0) — 1–3
    orders of magnitude between tiers. German/French/Latin/Russian outputs untouched. Documentation only.

## [1.26.0] - 2026-06-17

### Added
- **Cross-language orthographic-drift — French, Latin, Russian.** Generalized `ortho_drift.py`
  into a profile-driven multi-language tool (`de`/`fr`/`la`/`ru`; the German profile reproduces
  prior behaviour verbatim — verified, German outputs untouched). Ran:
  - **Russian (Kossovich, pre-1918)** — 87,636 gloss tokens, **31,389 drift (358/1k ≈ 36% of
    tokens)**, detected **wordlist-free** (the 1918-abolished letters ѣ/і/ѳ/ѵ and word-final ъ are
    pre-1918 by definition): `въ→в`, `родъ→род`, `растеніе→растение` (і), `имѣющій→имеющий` (yat).
    The most sweeping reform in the corpus. Source: SamudraManthanam `kossovich.jsonl` (not csl-orig).
  - **French (BUR Burnouf 1866 / STC Stchoupak 1932)** — **0.31 / 0.02 drift/1k**
    (`poëte→poète`, `phlegme→flegme`, `françois→français`); Hunspell `fr_FR` membership. Romance
    convention-drift is ~30–1,500× below German legislated reform. (⚠️ BUR/STC inline Sanskrit in
    IAST, not `{#…#}` braces, so a few IAST fragments leak — macro-rate robust, forms less so.)
  - **Latin (BOP Bopp 1847)** — the **negative control: 0 drift** (no reform, no word-list exists),
    confirming the method's specificity (no drift manufactured where none exists).
  - **The drift rate tracks reform scope:** Russian 1918 (radical) ≫ German 1901/1996 (moderate) ≫
    French (minor) ≫ Latin (none). Per-language `<lang>_reform_map.tsv` / `<lang>_drift_summary.tsv`.
    Documentation only; never edits the sources.

## [1.25.0] - 2026-06-17

### Added
- **LLM-classified the German ortho-drift residuals — recall harvest.** Deduped the 9,482 residual
  candidates across PW/PWG/GRA/CCS/SCH to **6,804 unique tokens** and classified each against 2026
  Duden (39 Sonnet agents, deduped because classification is language-level). Breakdown:
  **1,831 reform-drift (27%)**, 2,981 fragment/OCR (44%), 1,105 Latin/foreign (16%), 759 modern
  (incl. `t+h` boundaries, 11%), 106 proper-noun, 22 uncertain.
  - The 1,831 confirmed drift are the inflected/compound forms the rule-based transform missed
    (`thierkreise→Tierkreise`, `abtheilung→Abteilung`, `commentars→Kommentars`,
    `eigenthümlichkeiten→Eigentümlichkeiten`). Folded into `ortho_drift/de_reform_map.tsv`, growing
    it **978 → 2,809 forms** — recall banked for future runs. Verdicts in
    `ortho_drift/de_residual_classified.tsv`.
  - `modern_form` is advisory (a few LLM artifacts). Documentation only. The per-dict drift reports
    are left as the deterministic-pass snapshot so the SCH-control comparison stays stable.

## [1.24.0] - 2026-06-17

### Fixed
- **Documentation-accuracy pass** — fact-checked the ortho-drift docs (changelog 1.20–1.23 +
  `ortho_drift/README.md` + `.ai_state.md`) against the committed data files (87 numeric claims).
  Corrected:
  - reform-map count **981 → 978** (a `wc -l` had counted the file's 3 comment lines as forms);
  - the **dic-vs-map attribution** in the full-PW result — the transform-and-check *discovers* 672
    drift forms, which then fold into the accumulating reform map, so the committed
    `PW_drift_report.txt` now reads `dic 0 / map 8,683`. The stable facts are **8,683 occurrences
    across 697 distinct forms**; only the dic-vs-map label migrates by design. (The earlier docs
    quoted the first-run `6,352 dic / 2,331 map` split as if permanent.)
  - the 715-form seed breakdown (added the 3 misc-era forms so the components sum to 715);
  - removed a self-referential commit hash from `.ai_state.md`'s WIP note.
  - Confirmed **2,171** residual candidates is correct (deduped; per-category counts sum higher
    only because a token can match more than one pattern). Documentation only.

## [1.23.0] - 2026-06-17

### Added
- **German-cluster orthographic-drift + the SCH-1928 control.** Ran PWG / GRA / CCS / SCH
  (`ortho_drift.py <DICT> --full`); the reform map accumulated to **978 forms**, and per-dict
  drift-by-era is written to `ortho_drift/de_drift_summary.tsv`.
  - **Control validated.** The four pre-1901 dictionaries are 1901-`th→t`-dominated
    (PW 6203, PWG 6508, GRA 1460, CCS 341) with almost no 1996-`ß` drift. **SCH (Schmidt 1928)
    flips the profile** — 1901-`th` collapses to 76 while the 1996-`ß` reform dominates at 319
    (`Kuß→Kuss`, `Bewußtsein→Bewusstsein`, `Mißgunst→Missgunst`). The method correctly dates each
    dictionary's orthographic epoch from its own text; drift/1k declines monotonically with
    publication date (10.26 → 8.86 → 7.90 → 4.72 → 2.52).
  - Added a per-era occurrence summary to each report + the cross-dictionary `de_drift_summary.tsv`.
  - Documentation only; never edits csl-orig.

## [1.22.0] - 2026-06-17

### Added
- **Externalized + expanded the German reform map** → `ortho_drift/de_reform_map.tsv`.
  `ortho_drift.py` now loads it at startup (merged with the curated seed) and folds each run's
  transform+dic-confirmed drift back into it, so the lexicon **accumulates across dictionaries**
  and works even without the Hunspell dic. Seeded from the full-PW run: **715 forms** (366
  `1901-th`, 224 `1901-c`, 84 `1901-iren`, 21 `1901-c-iren`, 12 `1996-ss`, 5 `archaic-ey`, 3 misc)
  — up from ~40 inline pairs.
  - This is the achievable equivalent of "expand from DTA/RIDGES": those are online research
    resources and this environment has **no outbound internet** (PyPI/pip unreachable), so the
    map is seeded from the corpus' own validated drift instead. `de_reform_map.tsv` is the
    expandable container — DTA/RIDGES historical→modern pairs merge straight in (or drop the
    files locally, like the Hunspell dic). Documentation only; never edits csl-orig.

## [1.21.0] - 2026-06-17

### Added
- **Wired Hunspell `de_DE` + ran the full PW orthographic-drift scan.** `detectors/ortho_drift.py`
  now loads the modern German Hunspell word-list (Adobe InDesign's bundled `de_DE` 2006,
  103,756 stems — a **local dependency**, overridable via `$ORTHO_DE_DIC`, **not committed**) and
  detects drift by **transform-and-check**: apply a reform rule to a flagged token and accept it
  as drift *iff the transformed form is in the modern dic and the original is not*.
  - **Full PW** (170,556 entries / **845,888 German tokens**): 502,882 (59%) filtered as already-
    2026-modern; **8,683 reform-drift occurrences across 697 distinct forms** — the transform-and-check
    discovered 672 beyond the curated seed (high-precision; `Theater`/`Gottheit` rejected); 2,171
    residual candidates for the LLM. (Once those 672 fold into the accumulating map, later reports
    attribute all 8,683 to the map — total stable, attribution migrates.) Top: `gerathen→geraten`
    (253), `personificirt→personifiziert` (191), `theilhaftig→teilhaftig` (190), `ceremonie→zeremonie`
    (138). **PW's German is pervasively pre-1901, confirmed at scale.**
  - Transform-and-check deterministically rejects the `t+h`-boundary / Greek-loan false positives
    (`Theater`, `Gottheit`) that the sampled LLM pass had to catch — so the dic-confirmed list is
    high-precision without the LLM.
  - Finding: the Adobe `1901/1996/2006` variants are *modern* dicts differing only in the 1996
    ss-rule (not 19th-c. word-lists), so era set-diff captures only the ß-reform — hence
    transform-and-check, not diff. Degrades gracefully (map + patterns) if the dic is absent.
  - **Documentation only; never edits csl-orig.**

## [1.20.0] - 2026-06-17

### Added
- **Orthographic-drift pilot — Phase 0 (PW / German)** ([`detectors/ortho_drift.py`](detectors/ortho_drift.py),
  outputs in [`ortho_drift/`](ortho_drift/README.md)). First slice of the
  [orthographic-drift study](ORTHO_DRIFT_ROADMAP.md): extend the body-grounded method from
  Sanskrit headwords to the **gloss language**, checking German tokens against 2026 Duden.
  - On a 2,509-entry PW sample (12,917 German tokens): **48 confirmed reform-drift occurrences
    in 13 forms** (`Thier→Tier`, `Theil→Teil`, `Noth→Not`, `thun→tun`, `Vocal→Vokal`, …; eras
    1901 `th→t`/`c→k`, archaic `ey`, 1996 `ß→ss`) + 163 pattern-candidates for the LLM/wordlist.
  - **vs-Duden classification** (Sonnet oracle) of the 163 candidates: **114 more reform-drift**
    (75 `th→t`, 27 `c→k/z`, 12 `-iren→-ieren`), 19 modern (`t+h` boundaries), 15 Latin/foreign,
    13 fragments, 2 proper-nouns → **127 distinct reform-drift forms in the sample**; PW's German
    is pervasively pre-1901. Verdicts in `ortho_drift/PW_drift_classified.txt`.
  - Reuses `triage_util` (entry index, paths, stdio); a curated reform map (high precision) +
    recall patterns. **Documentation only — never edits csl-orig.**
  - **Tokenizer-hardening discovered live:** PW glosses embed editorial-correction records
    `{%<bot>{{old->new||date|editor|github-url|}}</bot>%}` — leaking `github`, editor names and
    botanical Latin. The tokenizer now strips `{{…}}`, `<bot>…</bot>`, `<ls>` sigla, and filters
    abbreviations case-insensitively.
  - Decisions recorded: 2026 = Duden (Hunspell `de_DE`); sampled by default; proper-noun
    strategy = LLM-bucket + sigla stop-list (capitalisation is useless for German); documentary
    now, OCR-error subset only could graduate to a sign-off-gated correction queue later.

## [1.19.0] - 2026-06-17

### Added
- **Tier-2 dictionary triage runs** — the 19th-c. European-language cluster (9 dicts), taking
  coverage from 9/33 to **18/33**. All hybrid (Sonnet classify / Opus confirm / Opus review):
  - **SHS** (*Śabda-Sāgara*, English 1900, 246 tier-A) — **37 fileable** (~15%, the highest-yield
    dictionary so far), 31 do-not-file, 2 reviewed out. A genuine outlier: Śabda-Sāgara is a
    poorly-digitised source, and nearly every entry carries an explicit `E. <etymology>` /
    inflectional paradigm that confirms the correct spelling — the body-grounded method's ideal
    case. The 37 are b/v, retroflex w/W, vowel-length and sibilant errors, each contradicted by
    the entry's own text.
  - **WIL** (Wilson, English 1832, 108) — **3 fileable** (`boDidruna→boDidruma`,
    `jAmbabat→jAmbavat`, `kaNkalodya→kaNkaloqya`), 17 do-not-file, 1 reviewed out.
  - **GST** (Goldstücker, English 1856, 48) — **1 fileable** (`aprakaraRika→aprAkaraRika`,
    confirmed by the entry's own etymology + quoted example), 22 do-not-file.
  - **CAE / AP90 / MD / GRA / BEN / CCS** — **0 fileable** each (8/8/1/7/14/3 do-not-file;
    GRA reviewed out `pradakzinit`). Well-curated or small.
  - Registered all 9 in `triage_lang._LANG` (CAE/AP90/MD/SHS/WIL/GST/BEN→en, GRA/CCS→de) — a
    one-line edit.
- **Cumulative: 18/33 triaged, 63 fileable typos across 8 dicts, ~1,976 documented-intentional
  spellings catalogued.** Confirms the thesis: tier-A precision is near-zero on mature dicts;
  the do-not-file list is the deliverable. The exceptions are poorly-digitised sources
  (SHS 15%, PWG 2.4%), where the entry's own etymology makes each error high-confidence.

## [1.18.0] - 2026-06-17

### Added
- **Tier-1 dictionary triage runs** — 4 dictionaries, taking the body-grounded triage from
  5/33 to **9/33**. All hybrid (Sonnet classify / Opus confirm / Opus review):
  - **SKD** (*Śabdakalpadruma*, Sanskrit, 412 tier-A) — **3 fileable** (`hitAbalI→hitAvalI`,
    `pUzaBAzA→pUzaBAsA`, `vfzaBAzA→vfzaBAsA`, each contradicted by the entry's own *vyutpatti*),
    103 do-not-file, 1 reviewed out (`mahotka`, a real bahuvrīhi).
  - **AP** (Apte *Practical*, English, 152) — **0 fileable**, 32 do-not-file.
  - **MW72** (Monier-Williams **1872** 1st ed, English, 360) — **0 fileable**, 77 do-not-file,
    1 reviewed out (`ahnika`); 42 unlocatable (1872 keys diverge from the current source).
  - **SCH** (Schmidt *Nachträge*, German 1928, 678) — **0 fileable**, 109 do-not-file, 3
    reviewed out (`uluka`/`ayoDana`/`koSalikA` — two proper-noun names + a pw variant).
  - Registered the four in `triage_lang._LANG` (`SKD/SCH→sa/de`, `MW72/AP→en`) — a one-line
    edit, the payoff of the 1.17.0 single-registration-point refactor.
  - The **Opus review gate** pulled every confirmed typo in AP/MW72/SCH (and 1 in SKD),
    validated across all three body languages (Sanskrit `mahotka`, English `ahnika`, German ×3).

### Fixed
- `triage_synthesize.py`: genericized the remaining hardcoded **"MW"** in the `*_triaged.txt`
  header prose and the bucket-5/6 titles (they now use the dict code). Regenerated
  `PWG_triaged.txt` (header-only change, all data rows + counts identical). PW/VCP keep their
  cosmetic stale "MW" header — their on-disk `triage_work` had diverged from the committed run,
  so re-synthesis was **not** safe and was reverted (don't regenerate a committed package from
  drifted verdicts).

## [1.17.0] - 2026-06-16

### Changed
Lower-severity cleanup from the same code review -- a behavior-preserving refactor of the
triage pipeline (the committed MW/PW/VCP/PWG packages are byte-identical after it):
- **Shared boilerplate consolidated into `triage_util.py`** (the stdlib-only triage core):
  `HERE`/`ROOT`/`GITHUB`, `reconfigure_stdio()`, `dict_arg()`, `package_dir()`/`work_dir()`,
  and `csl_root()`/`csl_dict_file()`. Removes the path triple + UTF-8 stdio preamble + the
  `argv[1] ... else 'MW'` idiom that were copy-pasted across all seven `triage_*.py` steps,
  and unifies the **three divergent ways `csl-orig` was located** (`GITHUB/csl-orig`,
  `ROOT/../csl-orig`, `HERE/../../csl-orig` -- all the same dir, expressed three ways).
- **Magic numbers named.** `BATCH_SIZE = 30` (was duplicated in `triage_enrich` and
  `triage_body_batches`), the `INTENTIONAL_KINDS` / `NEEDS_JUDGMENT` body-kind tuples, and the
  `SCAN_URL` deep-link template now live once in `triage_util`; the body-classifier thresholds
  (`_XREF_MAX_CHARS` / `_REALWORD_MIN_CHARS` / `_THIN_MAX_CHARS` / `_BODY_TEXT_CAP`) and
  `triage_synthesize`'s display widths are named module constants.
- **Single source for language config.** The wrong-readings sub-type order is now
  `triage_lang.subtype_order()` (was a hardcoded list re-stated in `triage_synthesize`).
  `lang()` already defaults an unknown dict code to English, so the `_LANG` map stays the one
  place a dictionary's language is registered.
- Dropped dead imports (`re`/`glob` in `triage_synthesize`; `sys` in `triage_bodies` /
  `triage_body_batches` / `triage_enrich`).
- Verified: `py_compile` + 17 unit checks + PWG re-synthesizes byte-identical (12 fileable /
  248 do-not-file) + the full deterministic feeder chain
  (`make_dict_package` -> `enrich` -> `bodies` -> `body_batches`) re-runs clean on a throwaway
  dictionary, touching no committed package.

## [1.16.0] - 2026-06-16

### Fixed
Correctness fixes from a recall-focused multi-agent code review of the triage pipeline:
- **Review gate is now fail-loud** (`triage_synthesize.py`): a confirmed typo with no Opus
  review verdict (missing/unloadable `body_review_*.json`) was silently filed to FILE-FIRST —
  the false-positive gate could no-op invisibly. Synthesize now warns on stderr (count, and
  whether any `body_review` files were found at all).
- **`load_verdicts` no longer swallows errors** (`triage_util.py`): the `except Exception: pass`
  that silently dropped a malformed/unreadable verdict file now prints a WARNING per file
  (silent verdict loss skews the buckets and can disable the review gate).
- **Non-greedy JSON fallback** (`triage_util.load_json_array`): the greedy `\[.*\]` (first `[`
  to last `]`) over-captured when an agent wrapped its array in prose containing other brackets;
  it now scans `[` candidates with `JSONDecoder.raw_decode` and returns the first valid array.
- **`EntryIndex.bodies()` ↔ `first()` consistency** (`triage_util.py`): `bodies()` read only
  `by_k1` while `first()` falls back to `by_k2`, so a k2-only headword silently got an empty body
  (→ mis-classified `missing`). `bodies()` now mirrors the k1→k2 fallback.
- **Unguarded file reads** use context managers (`triage_util`, `triage_bodies`, `triage_body_batches`).
- `test_triage.py`: +2 checks (k2-fallback, prose-tolerant JSON) → 17. Behavior-preserving —
  PWG re-synthesizes to the same 12 fileable / 248 do-not-file. (Lower-severity cleanup findings —
  duplicated boilerplate, magic numbers, the hardcoded `_LANG`/INTENTIONAL-tuple — left as-is.)

## [1.15.0] - 2026-06-16

### Added
- **Opus-pinned Review phase** — a 4th phase in `bodyaware_workflow.js` (after Confirm): an
  adversarial false-positive gate that re-reads each *confirmed* TYPO from the source and drops
  intentional forms (vṛddhi derivatives, attested variants, wrong-reading/correction apparatus,
  redirects, real distinct words). Pinned to `revModel` (default **opus**) **regardless of the
  session model**, so the highest-judgment step no longer depends on what the operator's session
  is running. `triage_synthesize.py` consumes `body_review_*.json` (review-rejected candidates
  are excluded from FILE-FIRST and **auto-commented** into the `_file_first_sf.txt` as
  `; REVIEWED-OUT (vrddhi|variant|apparatus|redirect|realword): …`), automating the per-dict
  human false-positive review. Driver emits `revModel=opus`; skill step 4 is now a spot-check.

### Notes
- **Validated** by resuming the PWG run (classify+confirm served from cache) over its 14 confirmed
  typos: the automated Opus Review **reproduced the manual curation exactly** — kept the same 12,
  reviewed out the same 2 (`dASaSiras` vṛddhi `(wohl dASaSirasa von daSaSiras)`, `ketunAlin`
  variant `Auch ketumAli`). PWG regenerated via the automated review.
- **SNP** triaged as the validation dictionary (4 tier-A, 0 fileable) — 5 of 33 dicts now done.

## [1.14.0] - 2026-06-16

### Added
- **`/dict-triage <DICT>` skill** ([.claude/commands/dict-triage.md](.claude/commands/dict-triage.md)) —
  packages the full hybrid body-grounded triage as a repeatable repo command: build the package
  (`triage_dict.py <DICT>`) → launch `bodyaware_workflow.js` with hybrid models (Sonnet classify /
  Opus confirm) → synthesize → human-verify each FILE-FIRST candidate against the entry → write the
  package → commit. Encodes the judgment rubric (KEEP when the entry's own derivation/citation
  confirms the suggestion; DROP wrong-reading/redirect/vṛddhi/variant apparatus) and the hard-won
  lessons (the TYPO pass is stochastic — don't blindly re-run a verified package; tier-A precision
  is near-zero; extend `triage_lang` markers when apparatus leaks). Includes a "new language" recipe.

## [1.13.0] - 2026-06-16

### Added
- **PWG** ([corrections_draft/PWG/](corrections_draft/PWG)): the large Sanskrit–German
  Petersburger Wörterbuch triaged via a **hybrid model split** — Sonnet 4.6 classified the
  306 `realword` candidates, Opus 4.8 source-confirmed the TYPO pile, and a human reviewed
  every confirmed candidate against the PWG entry.
- `bodyaware_workflow.js` per-phase model pinning (`clsModel` / `confModel`, defaulting to
  sonnet/opus via `triage_dict.py`) — the hybrid is set in the script, no manual model
  toggling. Discover+Classify run on `clsModel`, Confirm on `confModel`.

### Fixed
- `triage_synthesize.py` file-first-sf header hardcoded `MW's` → now the actual dict code.

### Notes
- **PWG FINDING: 12 fileable typos of 497 tier-A** (14 body-confirmed; 2 reviewed out —
  `dASaSiras` is a vṛddhi derivative `(wohl dASaSirasa von daSaSiras)`, `ketunAlin` is an
  attested HARIV. variant of `ketumAli`). The genuine 12 are mostly **b/v (व/ब)** and
  vowel-length errors, each confirmed by the **entry's own derivation/citation** (e.g.
  `arTavanDa` is quoted as `lalitArTabanDaM`; `paRavanDa` has derivation `(paRa + ba°)`).
  248 are documented-intentional (71 `fehlerhaft für`); 196 real words; 2 stale.
- 4-dictionary fileable-typo counts: **MW 4 · PW 2 · VCP 1 · PWG 12** — PWG (the large
  Petersburg) genuinely carries more digitization errors. The **hybrid tiering worked**:
  Sonnet's bulk classification + Opus's source-confirm + human review caught the real typos
  *and* the 2 vṛddhi/variant false positives, at ~40% lower model cost on the bulk phase.

## [1.12.0] - 2026-06-16

### Changed
- **Unified + deduplicated the triage pipeline** (the "improve the scripts" pass, guided
  by a 4-dimension multi-agent review of the MW/PW/VCP runs, with each proposal
  adversarially verified against the code — 15 confirmed, 2 refuted):
  - `triage_util.py` — ONE tolerant JSON loader + ONE csl-orig `EntryIndex` (were
    duplicated across triage_bodies/body_batches/synthesize + make_changefiles), with an
    L-number→headword map that resolves VCP `{{Lbody=N}}` redirects to the target headword
    in the wrong-readings list (`vrAhmaRa → (redirect -> brAhmaRa)`).
  - `bodyaware_workflow.js` — ONE canonical body-aware workflow (was copy-pasted per
    dictionary). It **discovers its batch count at runtime** (no `nbatch` arg, so the
    args-undefined→0-agents failure mode is gone) and builds its language rubric from
    `triage_lang.marker_hint()`.
  - `triage_dict.py` — single driver running the four deterministic steps and emitting the
    workflow args; `--finish` synthesizes.
  - `test_triage.py` — 15 marker unit checks across en/de/sa.
  - Removed dead code (enrich `provisional` `dcs_suspect_band`/`known_real` branches; the
    legacy MW-only first-pass cross-check in triage_bodies; duplicated regex literals).
  - `triage_synthesize` prints the correct dict code (was a hardcoded `MW:` label).

### Added
- `triage_lang` markers: PW correction-note apparatus `Richtig {#X#}` / `lies {#X#}` is now
  classified INTENTIONAL — the headword is the form-as-found and X is PW's noted correct
  form (apparatus, do NOT file: e.g. `veRatawa`, `helarAja`, `SAraRa`). Cross-reference
  markers made separator-independent so `q.v.`/`See`/`=` cross-refs sub-type correctly.

### Notes
- VCP: a re-run on the unified workflow surfaced a genuine typo `camIkara → cAmIkara`
  ("gold") — VCP FILE-FIRST 0→1.
- **HONEST FINDING: the body-aware TYPO pass is STOCHASTIC and low-yield.** Re-runs surface
  a different small handful of candidates (across runs MW 4↔0, PW 2↔0, VCP 0↔1) and
  re-running is NOT idempotent — it can *lose* genuine typos (an MW re-run refuted the 4
  verified ones). So the committed MW/PW packages were KEPT (their verified candidates beat
  a fresh draw); only VCP was updated (its re-run strictly added the genuine `camIkara`).
  The DETERMINISTIC layers (do-not-file lists, intentional/realword/redirect separation)
  are stable and are the durable deliverable. Proper recall fix = union across runs (future).
- The adversarial review REFUTED, and we dropped, two proposals: a confusion-class re-rank
  (vowel-length is 75% of *confirmed* historical corrections — down-weighting it is wrong)
  and a bodies-before-enrich reorder (k2 already comes from the package-time draft).

## [1.11.0] - 2026-06-16

### Added
- **VCP** ([corrections_draft/VCP/](corrections_draft/VCP)): the body-grounded triage run on
  the *Vācaspatyam* (Sanskrit–Sanskrit thesaurus). The Sanskrit `triage_lang.py` profile was
  tuned to VCP's conventions — chiefly the **`{{Lbody=N}}` redirect** marker (a variant-spelling
  headword pointing to the canonical entry) — and the body-aware workflow used a Sanskrit rubric
  (dhātu/root shape, gender/POS abbreviations).

### Fixed
- `triage_synthesize.py` printed a hardcoded `MW:` body label for every dictionary; it now uses
  the actual dict code (regenerated PW_triaged.txt; VCP correct from the start).

### Notes
- **VCP FINDING: of 563 tier-A candidates, 0 are fileable typos.** 155 are real distinct words /
  verbal roots (e.g. `garba` = √garb, distinct from `garBa` "womb"; `nUtra` "new" ≠ `mUtra`);
  **408 are documented-intentional — 362 of them `{{Lbody=}}` redirects** (variant spellings VCP
  cross-references, e.g. `vrAhmaRa` → `brAhmaRa`). Bulk-applying tier-A would break VCP's
  cross-reference web.
- Across the three dictionaries triaged, spelling-pattern tier-A fileable-typo precision is
  **MW 4/1954 (0.2%) · PW 2/657 (0.3%) · VCP 0/563 (0.0%)** — the body-grounded triage's value is
  preventing bad bulk edits and producing the per-dict do-not-file lists, not the handful of typos.

## [1.10.0] - 2026-06-16

### Added
- **Multilingual body-grounded triage + applied to PW.** The triage now handles
  dictionaries whose entry bodies are not English:
  - `triage_lang.py` — per-dictionary language profiles (MW=English, PW/PWG=German,
    VCP=Sanskrit) for the documented-intentional markers (wrong-reading / varia-lectio /
    in-composition / cross-reference). `triage_bodies.py` + `triage_synthesize.py` select
    markers by dict; the body-aware workflow uses a language-specific rubric.
  - `make_dict_package.py <DICT>` — one command to build any dict's tier-A package from
    `combined_candidates.txt` (extract tier-A rows + `make_changefiles` draft).
- **PW** ([corrections_draft/PW/](corrections_draft/PW)): the full pipeline run on the
  Sanskrit–German Petersburger Wörterbuch (Böhtlingk–Roth). German markers
  (`fehlerhaft für`, `v.l.`, `Lesart`, `s. u.`, `vgl.`) drive the classification.

### Notes
- **PW FINDING: of 657 tier-A candidates, only 2 (0.3%) are body-confirmed fileable typos**
  (`Bagama→BagaRa` "der Umlauf der Gestirne" = *bhagaṇa*; `hemana→hEmana` "Adj. von heman").
  369 are real words; **255 are documented-intentional** — notably **95 explicit
  `fehlerhaft für` wrong-readings** (PW's apparatus is denser/more explicit than MW's
  45); 1 stale; 30 need eyes. Bulk-applying tier-A would delete 95 of Böhtlingk–Roth's
  own wrong-reading cross-references.
- The per-dict `<DICT>_wrong_readings.txt` do-not-file list (a user convention) is now
  produced for every dictionary triaged, grouped by sub-type in the body's language.

## [1.9.0] - 2026-06-15

### Added
- **Body-grounded precision triage** for the engine's tier-A correction candidates —
  four new tools under [detectors/](detectors) that judge each candidate against the
  dictionary's *own entry text*, not spelling alone:
  - `triage_enrich.py` — attach deterministic evidence per candidate (the `<k2>`
    accent/hyphen field, DCS frequency band of the suggestion, cross-dict count,
    confusion class + empirical weight, historical-pair flag) → `<DICT>_evidence.jsonl`.
  - `triage_bodies.py` — build a headword→entry-body index from csl-orig and classify
    each candidate's MW body: `wr` / `variant` / `xref` (MW documents the spelling on
    purpose), `realword` (a real gloss), `thin`, `missing` (not in the current source).
  - `triage_body_batches.py` — split the `realword` set into body-aware batches.
  - `triage_synthesize.py` — combine deterministic + LLM + source-confirmation into a
    six-bucket ranked review queue (`<DICT>_triaged.txt`), the FILE-FIRST candidates in
    CORRECTIONS standard format (`<DICT>_file_first_sf.txt`), and a standing **do-not-file
    list** `<DICT>_wrong_readings.txt` — every spelling the dictionary documents on purpose
    (wrong-reading apparatus / `v.l.` / in-composition / cross-reference), grouped by
    sub-type, emitted for every dictionary triaged so future runs never re-flag them.
- Applied to **MW** ([corrections_draft/MW/](corrections_draft/MW)): the body-aware
  triage was run via a two-stage multi-agent workflow (adjudicate → adversarial verify,
  then body-aware classify → source-confirm).

### Notes
- **FINDING: of 1,954 MW tier-A candidates, only 4 (0.2%) are body-confirmed fileable
  typos.** 1,161 are real distinct words; 630 are spellings MW documents deliberately
  (`w.r. for…`, `v.l.`, `in comp. for…`, cross-refs) where a "fix" would *corrupt* MW;
  11 are stale (absent from current source); 148 need human eyes. Tier-A is high *engine*
  confidence, not precision — do not bulk-apply it.
- The engine's **vowel-length** flags (≈77% of tier-A) are almost all false (Sanskrit
  uses vowel length lexically); the rarer **consonant-class** flags (retroflex/sibilant/
  aspirate) are far higher-precision (3 of the 4 confirmed: ṇatva, `aṃśa` morpheme,
  `voḍhavya` sandhi).
- The adversarial/body-aware design caught false positives that spelling- and
  memory-based passes confirmed: `marga→mArga` (MW marks `marga` as `w.r. for mArga`),
  `muka→mUka` (MW glosses `muka` "the smell of cow-dung"), `vinAsa→vinASa`
  (`vi-nāsa` "noseless" is real). The original MW draft readme's worked examples were
  corrected accordingly.
- Triage intermediates (`<DICT>_evidence.jsonl`, `triage_work/`) are gitignored; the
  committed artifacts are `<DICT>_triaged.txt` and `<DICT>_file_first_sf.txt`.

## [1.8.2] - 2026-06-15

### Fixed
- **Retroflex `ळ` (U+0933) regression in `detectors/slp1util.devanagari_to_slp1`** introduced by
  the 1.8.1 dedup. The 1.8.1 form `to_slp1(deva_to_iast(s))` mis-mapped `ळ` to SLP1 `x` (vocalic
  ḷ) instead of `L`: `deva_to_iast` renders both `ळ` and vocalic `ऌ` as IAST `ḷ` (U+1E37), so the
  retroflex/vocalic distinction was lost before `to_slp1` ran and could not be recovered. Fixed at
  the source: `sanskrit-util` gains a direct `deva_to_slp1` (makes the `ळ`→`L` decision before the
  IAST step; vocalic `ऌ`/`◌ॢ` stay `x`), and `devanagari_to_slp1` now calls it. The danda /
  double-danda→space post-step is unchanged, and output is byte-identical to 1.8.1 on every input
  **except** those containing `ळ` (e.g. RV 1.1.1 `अग्निमीळे` → `agnimILe`, was `agnimIxe`; Marathi
  `खेळ` → `KeLa`, was `Kexa`). Impact was low — `devanagari_to_slp1` is used only by `ocr_verify`'s
  fuzzy comparison and `ळ` is rare — but it was a real correctness regression vs the pre-1.8.1 map.
  (The 1.8.1 "behavior unchanged" claim below held for the tested agni/kapila/Darma words but not
  for `ळ`.) Requires the `sanskrit-util` sibling at ≥ the commit adding `deva_to_slp1`.

## [1.8.1] - 2026-06-15

### Changed
- Cross-repo dedup: `detectors/slp1util.devanagari_to_slp1` now **delegates to the shared
  `sanskrit-util` package** (via `detectors/sanskrit_util.py`, a relative-path shim
  mirroring WhitneyRoots) instead of carrying its own Devanagari→SLP1 maps — single
  source of truth for transliteration. Behavior unchanged (verified equivalent on
  agni/kapila/Darma, and the danda→space step from 1.7.0 is preserved as a post-step).
  The SLP1 alphabet/char-classes stay local (sanskrit-util does not expose them). The
  shim raises a clear error only if the sibling is absent *and* the OCR path is used.

## [1.8.0] - 2026-06-14

### Added
- `detectors/gen_vidyut_stems.py` + vidyut morphology signal (Phase 3.2): generate the
  205k vidyut pratipadika (stem) inventory; `run_all` tags `morph✓` and nudges rank when
  a correction's suggestion is a valid vidyut stem the suspect isn't. `slp1util` gains
  `load_vidyut_stems`. Stems from vidyut (ambuda-org, MIT).

### Notes
- Honest finding: vidyut-stem validation is **weak on dictionary headwords** — only
  ~6.6% are pratipadikas, and an inflected suspect (`rAjA`) looks non-stem — so morph is
  a ranking nudge + tag, **not** a tier promoter (an `or morph` tier-A trigger
  over-promoted A 7717→11220, including inflection non-errors like `rAjA→rAja`).
  `vidyut_stems.txt` is gitignored (opt-in regenerate; the tag is off if absent).

## [1.7.0] - 2026-06-14

### Added
- `detectors/ocr_verify.py` (Phase 2.1) — OCR-assisted pre-verification pipeline:
  resolve the Cologne `servepdf` page → fetch the scan PDF → PDF text layer or OCR →
  closest-match compare the print to the suspect vs suggested spelling →
  CONFIRM/DENY/UNCERTAIN triage label. Fetch+render, the closest-match decision, and
  `slp1util.devanagari_to_slp1` are verified here; the OCR step is pluggable and needs
  tesseract + a Devanagari model (`san`/`hin`). Polite: cached, rate-limited, 429
  backoff — small batches, ideally server-side. Triage prior, not a verdict (a human
  always confirms against the scan).

## [1.6.0] - 2026-06-14

### Added
- `detectors/run_campaign.py` (Phase 2.4) — per-dictionary campaigns: splits the
  unified detector suite per dictionary into `campaigns/<DICT>/{review.html,
  candidates.txt}` and a tier-A-ranked dashboard `campaign_summary.txt` (MW 1977,
  PD 1045, BHS 737, SCH 678, PW 657 …), so corrections can be worked one dictionary
  at a time (matching the per-dict CORRECTIONS issue layout). Reuses run_all's
  aggregation/scoring/review-HTML. Outputs gitignored.

## [1.5.0] - 2026-06-14

### Added
- `detectors/gen_confusion_weights.py` + `confusion_weights.json` (Phase 2.6) —
  data-driven single-char confusion weights from the 3884 o_vs_O pairs (a/A 41%,
  i/I 24%, u/U 9%, s/S 8% …); `run_all` ranks common confusions higher.
- `detectors/make_changefiles.py` (Phase 2.5) — submission-prep: turns accepted
  corrections into per-dictionary **draft** change-files in the CORRECTIONS
  updateByLine format, locating the source line in csl-orig and proposing the
  `<k1>`/`<k2>` edit (both key fields). Prep only — no source edits, no auto-filing.

### Notes
- Phase 2 items blocked on external deps: OCR-assisted verification (tesseract +
  scan fetch), full DCS via `dcs_full.sqlite` (local copy is an empty placeholder),
  GRETIL corpus expansion (external download).

## [1.4.0] - 2026-06-14

### Added
- `detectors/extract_csl_hw.py` (Phase 1.4) — extract source-order headwords from a raw
  csl-orig dictionary (`<k1>`/`<k2>`), so charset/phonotactic/**order_check** run on the
  raw text, not just the cleaned sanhw1.txt. (order_check on raw sources measures
  deviation from sanhw's collation — verify against the dict's own anusvara convention.)
- `detectors/eval.py` (Phase 1.5–1.6) — evaluation harness: **recall** vs the 3884
  historical o_vs_O pairs (union 50.6%; spell_correct 44.6%, consensus 25%) and **15,152
  new** candidate pairs; **0** false positives vs ~30k known-good (nochange) words; tier
  distribution of recovered pairs (A=809/B=245/C=913); and a top-100 tier-A
  `spotcheck_sample.txt` for human precision verification.

## [1.3.0] - 2026-06-14

### Added
- `detectors/run_all.py` — unified runner (roadmap Phase 1.1–1.3): runs every
  detector, **deduplicates across them** by suspect headword, scores each candidate
  and assigns an **A/B/C tier** (cross-detector agreement is the main signal). Emits
  `combined_candidates.txt` (ranked), `combined_sf.txt` (CORRECTIONS standard format),
  and `combined_review.html` — an accept/reject review UI with per-row scan links,
  localStorage, and export of accepted/rejected rows to the `:y`/`:n` standard format.
  On sanhw1: 17,098 deduped candidates, 7,618 flagged by ≥2 detectors.
- `ROADMAP.md` (phased plan).

## [1.2.0] - 2026-06-14

### Added
- DCS corpus grounding: vendored `detectors/dcs_lemma_summary.json` (83,239 SLP1
  lemmas + frequency bands 1–5; DCS-2021, Oliver Hellwig, CC-BY, via VisualDCS).
  `slp1util.py` gains `load_dcs_lemmas`, `normalize_lemma` (DCS join key), and a shared
  `confusion_candidates`.
- New detector `dict_vs_corpus.py` — catches **collective** dictionary errors (a form
  every dictionary agrees on but the DCS corpus contradicts). Lowest-precision /
  exploratory by design.

### Changed
- `spell_correct.py` ranks suggestions by DCS frequency band and **suppresses**
  headwords that are attested DCS lemmas (9921→9173 flagged, 4001 real words
  suppressed, 704 suggest a band-≥4 DCS lemma); refactored onto shared
  `confusion_candidates`.
- `consensus.py` / `intra_dup.py` suppress minority/variant spellings that are
  attested DCS lemmas (consensus 8918→7548, intra_dup 10443→8945).

## [1.1.0] - 2026-06-14

### Added
- `detectors/` package — six additional spell-check algorithms grounded in the real
  CORRECTIONS error distribution, sharing one confusion model in `slp1util.py`:
  `spell_correct.py` (noisy-channel vs MW/PW/VCP + corpus), `consensus.py` (N-way
  cross-dict voting), `intra_dup.py` (intra-dictionary self-contradiction),
  `phonotactic_check.py` (anti-sandhi rules), `charset_check.py` (encoding),
  `order_check.py` (collation). See [detectors/readme.md](detectors/readme.md).
- `USE_CASES.md` — goal-oriented guide mapping tasks to tools and the verify→submit path.
- `triage_suspects.py` — splits a suspect list into noise / priority (non-rcc,
  verify-first) / gemination (post-repha, low priority).
- `Allvs_2026/{MW,PW,PWG,MW72}/` — fresh review packages (2017 `AllvsXX/` kept as audit trail).
- Repo-specific `CLAUDE.md`; deepened `README.md` (methods + real-error distribution).

### Changed
- Modernized every script to **Python 3 + PHP 8** (the only runtimes here): `print()`,
  `str.maketrans`/`str.translate`, `functools.cmp_to_key`, `html.parser`, `-1` preg_split.
- `faultfinder3a.php` check loop `for`→`foreach` — a deliberate, additive coverage
  change (VCP 6856→7411; the new hits are the s…/h… alphabet tail).

### Fixed
- `faultfinder3a.php` tail-drop: the `for ($j<count)` loop silently skipped surviving
  headwords past the survivor count (the alphabet tail); plus the PHP 8 `array_diff`
  key-gap warnings and `preg_match(null)` deprecation.
- `faultfinder3a-html.php` `repeat=2` (rCC report) was dead code — never stored or
  destructured records.
- `triage_suspects.py` robustness: malformed-line guard, filename-token-only `derive`,
  empty-dict lines no longer buried in noise; `ngramspellcheck.py` stdout/stderr utf-8.
- Stopped tracking `ngram/data/error.txt` (run output).

## [1.0.0] - 2026-06-13

### Added
- Added this changelog so repository-level changes have a stable home.
- Recorded the current repository purpose: SanskritSpellCheck ==================

### Recent Git History
- 2026-05-29 ai-wip: add .pre-commit-config.yaml (python+yaml)
- 2026-05-29 ai-wip: add .github/dependabot.yml for GitHub Actions auto-updates
- 2026-05-29 ai-wip: add CODE_OF_CONDUCT.md (Contributor Covenant 2.1)
- 2017-09-07 AllvsVCP ready
- 2017-09-07 issue 365 change made
