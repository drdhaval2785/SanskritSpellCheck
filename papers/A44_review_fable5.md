# A44 — referee-style review (pre-submission)

<p align="right"><sub>Created: 02-07-2026 · Last updated: 02-07-2026</sub></p>

Substantive review of
[A44_body_grounded_triage_paper.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A44_body_grounded_triage_paper.md)
by Fable 5 (`claude-fable-5`), 02-07-2026, within the Fable trial window. Target venue per the
locked split: **International Journal of Lexicography** — note the draft's frontmatter still
says DSH/Cultural Analytics/eLex and the prose is written for that NLP-leaning audience; the
biggest single revision is the IJL reframe. Fact-checking was done separately (~40 claims, one
fix); this review is argument and audience.

**Overall verdict: the inversion at the paper's heart — the do-not-file catalogue as the
principal deliverable, the typos as the by-product — is genuinely original and perfectly suited
to IJL. The draft under-exploits its own newest evidence (the 02-07 verification pass) and
speaks NLP to a lexicography audience. Fixable in two sessions plus the human IRR gate.**

## Major (must fix before submission)

1. **Reframe for IJL.** The lexicographic problem (variation-vs-error; what editorial apparatus
   *is*; why "correcting" a *v.l.* corrupts an edition) must lead; the pipeline mechanics
   (agents, model names) move to a compact method section + appendix. IJL referees are
   lexicographers: the apparatus taxonomy in §4.2 (w.r., v.l., in-composition, cross-reference,
   ṇopadeśa) deserves a *named table with per-dict counts* — it is the paper's most
   IJL-native asset and is currently one prose sentence. Update frontmatter `venue:` to IJL.
2. **Fold in the 02-07 verification pass — it is the strongest new evidence for the thesis and
   it's missing.** All 122 FILE-FIRST rows were re-verified against source
   ([VERIFICATION_2026_07.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/VERIFICATION_2026_07.md)):
   92 held as proposals, 17 demoted to scan-first, **11 (~9 %) turned out to be
   duplicate-pair/apparatus COLLISIONS** (the correct spelling already exists as its own entry —
   YAT dual-listings cross-referenced "Idem", MW `kattfRa`, PWG's errata-note `duzWu`, Böhtlingk's
   `*hemana`), 1 was already fixed upstream, 1 was ṇopadeśa notation. Three consequences to
   write in: (a) §3.2's four-way candidate taxonomy gains a **fifth class: collision** — a
   category only entry-reading can catch, which *strengthens* the body-as-arbiter thesis;
   (b) MW's headline becomes "4 triage-confirmed, of which post-verification 2 scan-first + 2
   editorial" — state it plainly, it deepens the precision-collapse story rather than weakening
   it; (c) queue decay (~0.8 %/week against live csl-orig) joins §6 limitations.
3. **Resolve the reproducibility/stochasticity tension explicitly.** §3.4 admits the typo pass is
   stochastic while the reproducibility section says every figure recomputes. Split the claims:
   deterministic layers (marker backbone, suppress list, all counts) reproduce exactly;
   the LLM pass reproduces as a floor under union-across-runs. Add the existing `eval.py`
   harness (false positives 0 vs ~31k known-good; recall vs the 3,884 historical pairs) to the
   reproducibility section — it substantiates §3.4's "doesn't over-suppress" and is currently
   uncited (fact-check finding).
4. **Model attribution inside §3.3 violates the project's own standard**: phases say bare
   "(Sonnet)"/"(Opus)". Name tier + version per phase — Sonnet 4.6 (`claude-sonnet-4-6`)
   classify, Opus 4.8 (`claude-opus-4-8`) confirm + adversarial review for the June runs; the
   02-07 verification pass Sonnet 5 (`claude-sonnet-5`) checkers + Fable 5 (`claude-fable-5`)
   adjudication — and add run dates. Reviewers increasingly require this; the repo already
   enforces it everywhere else.
5. **Related work (§2 TODO) now has two on-point citations that didn't exist when scaffolded:**
   the ISCLS 2026 "Preserving What Is Written, Not What Is Expected: The Proof-Reader Effect of
   LLMs in Sanskrit OCR" (names the exact over-correction failure mode the deterministic-marker
   backbone + adversarial gate are designed against) and the ISCLS 2024 "Contextual Spellchecking
   for Sanskrit" demo (nearest prior tool). Plus the planned axes (a)–(c) already sketched.
   See [docs/CHANDAS_ANUPRASA_PRIOR_ART.md §3](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/CHANDAS_ANUPRASA_PRIOR_ART.md).
6. **Inter-coder reliability remains the blocking human gate** (§6 admits it). For IJL this is
   likely a desk-reject risk if absent. The 02-07 spot-check (10/10 sampled PASS rows
   independently re-confirmed against source by a second model) is *supporting* evidence but not
   a substitute for the human second annotator already tracked in GTD.
7. **Abstract precision**: "all 33 dictionaries of the CDSL that carry anomaly candidates" reads
   as CDSL = 33; §3.1 has it right (33 of the merge carry tier-A candidates; the collection is
   larger). One-clause fix. Also decide the canonical headline number post-verification and
   stamp its as-of date (recommend: "122 triage-confirmed candidates, of which 92 survive
   source re-verification as unqualified proposals").

## Minor

- §4.4's TODO (worked examples per error class) — the umbrella issue
  ([CORRECTIONS#447](https://github.com/sanskrit-lexicon/CORRECTIONS/issues/447)) now contains
  polished per-row evidence lines; lift the examples from there, and cite the live issue as the
  real-world deployment of the method (reviewers love an artifact in production).
- "mythical-name index" for MCI (§4.3) — use its proper title (Mahābhārata Cultural Index).
- The YAT b/v held-back cluster (~32) deserves one sentence on *why* (Bengali print does not
  distinguish व/ब) — it's a memorable instance of print-culture awareness.
- Frontmatter `readiness:` → 3/5.

## What is genuinely strong — keep and foreground

The 0.20 % precision-collapse number is the quotable hook — keep it in sentence one of the
abstract. The inversion ("the do-not-file list is the real product") is the paper's lasting
idea; §5 argues it well. The digitisation-quality proxy (§5, filable rate) is a publishable
secondary finding on its own — do not cut it. The guardrail stance (never edits the source;
scan is final arbiter) is exactly the editorial ethics IJL wants demonstrated, and it is now
backed by a live, maintainer-facing artifact (#447).

## Priority order

(2) and (4) are text-only and use already-committed evidence — do first; (1) is the big rewrite
pass; (5) is agent-draftable + M.G. curation; (3) one paragraph + one citation; (6) is M.G.'s
human gate (schedule the second annotator now — longest lead time); (7) trivial. Realistic: two
working sessions + the annotator to reach 4/5.

<p align="right"><sub>Review: Claude Fable 5 (`claude-fable-5`) · paper: Dr. Mārcis Gasūns</sub></p>
