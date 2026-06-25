# HANDOFF — roadmap for SanskritSpellCheck

Paste-ready briefs for a **fresh chat** (no memory of the prior session) to pick up a task, ordered
by priority. The headword-triage handoff (for re-runs) is separate:
[corrections_draft/HANDOFF.md](corrections_draft/HANDOFF.md).

> **State (changelog up to `[1.40.0]` + Unreleased):** headword triage is **COMPLETE — all 33/33
> dictionaries**; the **ortho-drift study is COMPLETE across all 5 gloss languages**
> ([docs/ORTHO_DRIFT_FINDINGS.md](docs/ORTHO_DRIFT_FINDINGS.md)); the do-not-file **suppression layer**
> is at 33 dicts / 2,297 unique, `eval.py` false-positives 0. The big deliverables are done — the work
> below is *realizing the value* (filing the corrections) and *active-development* refinements.

## Roadmap (prioritized)

| # | Task | Type | Ready? |
|--:|---|---|---|
| **1** | **Draft the CORRECTIONS umbrella issue** (122 FILE-FIRST typos → one OCR-prefiltered issue) | lexicographic payoff | ⚠️ needs tesseract + `san` model for the OCR pre-verify |
| **2** | **Tier-C ranking calibration** (`run_all.py`) | engineering | ✅ no external data |
| ~~3~~ | ~~Ortho-drift within-EN recency control~~ | study extension | ✅ **DONE** (PD/PE/BHS/IEG = 0.00, VEI 0.06; en_GB.dic staged) |
| **4** | **German DTA/RIDGES long-tail merge** (`merge_reform_pairs.py`) | study extension | ⚠️ needs a DTA/RIDGES export or row-list URL |
| — | Cleanup / low-priority + blocked-on-external | — | see bottom |

## Shared context

- **Repo:** SanskritSpellCheck — a QA/error-detection toolset for the Cologne Digital Sanskrit
  Dictionaries (not a dictionary). Python 3 / PHP 8. `csl-orig` is a **sibling** checkout
  (`../csl-orig`). Default branch `master`; push is allowed (it's `drdhaval2785/SanskritSpellCheck`).
- **Conventions:** every Python script does `sys.stdout/stderr.reconfigure(encoding='utf-8')`
  (or `triage_util.reconfigure_stdio()`); write files as UTF-8 **without BOM**; commit with the
  `ai-wip:` prefix and the trailer `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`;
  keep maintainer-facing noise low; render paths/URLs as clickable links. Update `changelog.md`
  (dated `## [x.y.z]` entries, newest first) and `.ai_state.md` as you go (document-first).
- **Triage status:** ALL 33/33 dicts done (index:
  [corrections_draft/README.md](corrections_draft/README.md)) — 122 fileable typos across 11 dicts.

---

## Task 1 (LEAD) — Draft the CORRECTIONS umbrella issue

**Goal:** turn the **122 FILE-FIRST candidate typos** (across the 11 dicts with fileable > 0) into a
**single, evidence-rich umbrella issue** ready to post to
[sanskrit-lexicon/CORRECTIONS](https://github.com/sanskrit-lexicon/CORRECTIONS/issues), **OCR-prefiltered**
so the maintainer reviews a clean list. This realizes the value of the whole triage effort. The
Cologne maintainers are **sensitive to bot noise** → **one** issue (not 11), no auto-applying, and the
**scan is the final arbiter** (a human confirms each before it is applied to `csl-orig`).

**The 122, by dict (biggest first):** SHS 37 · YAT 27 · ACC 22 · PWG 12 · MCI 10 · MW 4 · SKD 3 ·
WIL 3 · PW 2 · VCP 1 · GST 1. Each lives in `corrections_draft/<DICT>/<DICT>_file_first_sf.txt`
(`DICT:wrong:right:n` rows; `;`-comment lines = the header + auto-commented "REVIEWED-OUT" false
positives — **skip them**). Per-candidate in-entry evidence is already written in each
`corrections_draft/<DICT>/readme.md` FILE-FIRST table.

**Data prerequisite (for the OCR pre-verify gate):** **tesseract + a Devanagari model (`san`)** plus
`pip install pytesseract pymupdf pillow`. `detectors/ocr_verify.py` fetches each candidate's Cologne
scan and labels it **CONFIRM** (print shows the suggested form → real typo) / **DENY** (print shows the
current form → faithful, drop it) / **UNCERTAIN** (the common case on noisy old scans). Without
tesseract it still runs but only **prefetches the scan image** as a review aid (label MANUAL). It is a
*triage prior, never a verdict*; fetches are rate-limited (run per-dict, not all at once).

**Paste this into a new chat (after `tesseract --version` and `python -c "import pytesseract,fitz"` both work):**
> In `SanskritSpellCheck`, draft a single **umbrella CORRECTIONS issue** for the 122 FILE-FIRST
> candidate typos, OCR-prefiltered. **Pilot on SHS first to lock the format, then scale to the other 10.**
>
> **Pilot (SHS, 37 candidates):**
> 1. From `detectors/`, run the OCR pre-verify on SHS:
>    `python ocr_verify.py ../corrections_draft/SHS/SHS_file_first_sf.txt 40 --lang san`
>    (it skips its own work past the cache; verdicts CONFIRM/DENY/UNCERTAIN). Note any **DENY** — those
>    drop out of the filing (the print is faithful).
> 2. Build the draft change-files: `python make_changefiles.py ../corrections_draft/SHS/SHS_file_first_sf.txt ../../csl-orig changefiles`
>    → `changefiles/SHS_draft.txt` (updateByLine `old`/`new` editing only the `<k1>`/`<k2>` key field;
>    it already skips `;`-comment lines and non-alphanumeric dict codes). Flag any candidate whose
>    *entry body* also contains the wrong spelling (make_changefiles only edits the key field).
> 3. Assemble the **SHS section** of the issue body: a markdown table `wrong → right | in-entry evidence
>    (from corrections_draft/SHS/readme.md) | OCR | scan-link` (scan = the `servepdf.php?dict=SHS&key=<wrong>`
>    URL, also in the readme). **Show the SHS section to the user and confirm the format before scaling.**
>
> **Scale:** repeat steps 1–3 for YAT, ACC, PWG, MCI, MW, SKD, WIL, PW, VCP, GST. Then **assemble ONE
> umbrella issue body** grouped by dict (a section per dict, biggest first), `corrections_draft/CORRECTIONS_umbrella_issue.md`,
> with a header that states: total candidates, that they are tier-A triage drafts OCR-prefiltered, that
> **each must be scan-verified before it is applied to `csl-orig`**, and that OCR is a prior not a verdict.
> Put **OCR-DENY** rows in a separate "likely faithful — not proposing" appendix (don't silently drop them).
>
> **Do NOT open the issue or push anything yet** — write the issue body to the file and show it to the
> user; they post it (or explicitly authorize `gh issue create --repo sanskrit-lexicon/CORRECTIONS`).
> The `changefiles/` drafts are gitignored intermediates. Commit only the assembled
> `corrections_draft/CORRECTIONS_umbrella_issue.md` + a changelog note (`ai-wip:` + the trailer).

**Lessons to carry in:**
- **The scan is the final arbiter.** OCR-CONFIRM ≠ apply; every kept candidate is still a draft a human
  verifies on the page (b/v: check व vs ब). UNCERTAIN is expected and fine — it stays in the list flagged.
- **One issue, evidence-rich, never auto-applied** — the maintainers dislike bot noise and never want
  `csl-orig` edited by a bot. make_changefiles is **prep, not submission**.
- The high-yield dicts (SHS 1900, YAT 1846, ACC) are poorly-digitised → most real; the mature dicts
  (MW/PW/VCP) contribute 1–4 each. The b/v (व/ब) and vowel-length classes are the highest-confidence.

**Where the pieces are:**
- `corrections_draft/<DICT>/<DICT>_file_first_sf.txt` — the 122 (skip `;`-comments); per-dict evidence
  in the sibling `readme.md` FILE-FIRST table.
- `detectors/make_changefiles.py` — sf → updateByLine draft change-files (now comment-safe; locates the
  source line in `csl-orig`, edits `<k1>`/`<k2>`).
- `detectors/ocr_verify.py` — the OCR pre-verify (`[candidates] [n] [--lang san]`); cached + rate-limited.

---

## Task 2 — Tier-C ranking calibration

**Goal:** improve the detector engine's **tier-C** ranking. `eval.py` shows tier C still recovers
~**911 historically-real** o_vs_O pairs (single-detector recoveries that the cross-detector-agreement
score parks in C). Boost the ones with independent corpus/DCS signal so true errors surface higher,
without inflating the false-positive rate (which must stay ~0 against `nochange.txt`).

**Paste this into a new chat:**
> In `SanskritSpellCheck/detectors`, calibrate the tier-C ranking in `run_all.py`. Today a candidate
> found by a single detector lands in C (`dict_vs_corpus`-alone is C by rule; `consensus`/`intra_dup`
> alone is B; everything else single-detector is C). Using the committed DCS frequency bands
> (`dcs_lemma_summary.json`, via `slp1util.load_dcs_lemmas`/`normalize_lemma`) and the data-driven
> confusion weights (`confusion_weights.json`, via `slp1util.confusion_weight`), promote a
> single-detector C-candidate toward B **only** when it carries strong independent signal — e.g. the
> *suggestion* is an attested DCS lemma (band ≥ 4) **and** the suspect is not, and the suspect→suggestion
> edit is a high-weight confusion class. Measure before/after with `python eval.py`: tier-C recall of
> the 911 known pairs should rise into B, the **false-positive count must stay 0**, and the tier-A
> count must not balloon. Keep it a tunable, well-named promotion rule (not magic numbers); document
> the threshold choice. Commit.

**Where the pieces are:**
- `detectors/run_all.py` `score_tier()` — the scoring + A/B/C assignment (lines ~117–141); the DCS
  band (`best_band`), high-precision-flagger flag (`hpf`), and confusion weight (`cw`) are already
  computed there.
- `detectors/eval.py` — the recall-vs-known-pairs + false-positive-vs-`nochange` + tier-distribution
  harness; re-run it to measure. It reads the cached `*_corrections.txt`; pass `--rerun` to
  `run_all.py` only if you change a *detector*, not just the scorer.
- `detectors/slp1util.py` — `load_dcs_lemmas`, `normalize_lemma`, `load_confusion_weights`,
  `confusion_weight`.

---

## Task 3 — Ortho-drift within-EN recency control — ✅ DONE (2026-06-25)

> **Complete.** PD/PE/BHS/IEG/VEI registered `en` in `LANG_OF`; en_GB reference = `ropensci/hunspell`
> `en_GB.dic`, staged at `external_src/hunspell/` (gitignored; `_dic()` falls back there). Result:
> **PD (1976–2009, 1.32 M tokens) = 0.00 drift/1k**, PE/BHS/IEG 0.00, VEI 0.06 — modern end of the
> gradient ≈ 0; written up in [docs/ORTHO_DRIFT_FINDINGS.md](docs/ORTHO_DRIFT_FINDINGS.md). Brief kept
> below for reference. To re-run: `python ortho_drift.py <DICT> --full` from `detectors/`.

**Goal (done):** extend the completed ortho-drift study with a **recency control**. The study showed English
drift is convention-driven and **editor/age-dependent** (WIL 1832 = 0.57 per 1k → MW 1899 ≈ 0.01 →
AP/CAE ≈ 0). Test that prediction at the *modern* end: run the same detector on dictionaries compiled
late, which should show **≈ 0 drift** — confirming the method dates orthography rather than flagging
noise. New anchors not yet in the EN cluster: **PD** (Deccan College, 1976–2009 — the most modern
English dict in the corpus, now staged in `external_src/`), plus the modern-leaning glossaries
**BHS / IEG / PE / VEI**. Expectation: PD lands at or below MW (lowest drift of all), tightening the
WIL→…→PD recency gradient.

**Data prerequisite (must be on disk first — this is why it isn't a no-setup task):**
- The **`en_GB` Hunspell dictionary** the EN profile checks against, pointed to by the env var
  **`$ORTHO_EN_DIC`** (it's the Adobe-InDesign-bundled dic, a **local dep, not committed**). The EN
  method is *transform-and-check against this wordlist*, so without it recall collapses to the small
  curated map + definitional rules. Confirm it resolves before running:
  `python -c "import os; p=os.environ.get('ORTHO_EN_DIC'); print(p, os.path.exists(p or ''))"`.

**Paste this into a new chat (after `$ORTHO_EN_DIC` points at the en_GB Hunspell dic):**
> In `SanskritSpellCheck/detectors`, extend the ortho-drift study with an English **recency control**.
> Register **PD, BHS, IEG, PE, VEI** as `en` in `ortho_drift.py`'s `LANG_OF` map (they currently
> default to German). Confirm `$ORTHO_EN_DIC` points at the `en_GB` Hunspell dic
> (`load_wordlist` returns None and recall collapses without it). Then run
> `python ortho_drift.py <DICT> --full` for each of the five (PD reads from `external_src/pd/pd.txt`
> automatically via `triage_util.source_file()`; the others from `csl-orig`). Read each
> `ortho_drift/en_drift_summary.tsv` row and compare against the existing 10-dict EN cluster
> (WIL 0.57 → MW 0.01 → AP/CAE 0). The hypothesis: the modern dicts — **PD (1976–2009) especially** —
> sit at the bottom of the drift gradient (≈ 0 per 1k), confirming the method tracks orthographic
> epoch. Do **not** re-run the 10 existing dicts (keeps the published table stable); fold any new
> en reform-map forms the runs surface. Update `docs/ORTHO_DRIFT_FINDINGS.md` with the recency-control
> row + a one-line interpretation, bump `changelog.md`, and commit (`ai-wip:` + the Co-Authored-By
> trailer).

**Lessons to carry in:**
- `ortho_drift.py` **degrades gracefully** if the dic is absent (map + rules only) — but for EN that
  means near-zero recall, so the run is meaningless without `$ORTHO_EN_DIC`. Check it first.
- It is a **documentation / search-normalization layer, never a correction list** — it does not edit
  any source. Doc-only deliverable.
- Keep the existing 5-language outputs and the 10-dict EN table **stable** — only *add* the new rows.

---

## Task 4 — German DTA/RIDGES long-tail merge (needs a corpus export/URL)

**Goal:** grow the German reform lexicon (`ortho_drift/de_reform_map.tsv`, ≈ 2,825 forms) by merging
**documented 1901/1996 old→new pairs** harvested from the DTA / RIDGES historical corpora into the map.
`detectors/merge_reform_pairs.py` is the **ready, dic-validated** ingest (accept a pair iff old ∉ dic &
new ∈ dic → filters hallucinations / dual-spellings / rejected proposals); it has already absorbed 14
Wikipedia-sourced pairs. The blocker is data acquisition only.

**Data prerequisite:** a **local DTA/RIDGES export** (or a row-list URL) of old→new German spelling
pairs. `WebFetch` reaches the web but **can't bulk-download** these corpora (it summarises via a small
model), so the export must be dropped on disk or provided as an explicit pair list.

**Where the pairs actually live (RIDGES / DTA).** These corpora carry a **normalization layer** that
maps each historical token to its modern spelling — that layer *is* the pair source, not the
documentation page:
- **RIDGES** (HU Berlin diachronic scientific German, ~1482–1914): the token tiers include `dipl`
  (diplomatic) / `clean` / **`norm`** (modern-normalized). Export the corpus from the **Laudatio
  repository** (or an ANNIS query) with the `dipl`/`clean` + `norm` columns; the `(historical, norm)`
  pairs where they differ are the input. The documentation page only *describes* these layers + the
  download route — it is **not itself the data** (and it's behind an Anubis anti-bot wall, so it
  can't be fetched programmatically).
- **DTA** (Deutsches Textarchiv): the **DTA::CAB** `orig`→`norm` normalization is the same idea on a
  much larger, general corpus — likely a broader pair list than RIDGES (which is domain-specific).
- **Caveat:** `norm` normalizes *all* historical variation (early-modern spelling, OCR, etc.), not
  just the 1901/1996 reforms — but `merge_reform_pairs.py`'s dic-validation (accept iff old ∉ de_DE
  dic & new ∈ dic) filters it to genuine historical→modern pairs, which is exactly what we want.
- **To hand off:** drop a TSV/CSV of `old<TAB>new` rows (extracted from the `norm` layer, differing
  pairs only) on disk, or a direct Laudatio/ANNIS export — then the brief below merges it.

**Paste this into a new chat (after the export is on disk):**
> In `SanskritSpellCheck/detectors`, merge the supplied DTA/RIDGES old→new German reform-pair export
> into `ortho_drift/de_reform_map.tsv` with `python merge_reform_pairs.py <export> de` (it is
> dic-validated against the `de_DE` Hunspell dic — set `$ORTHO_DE_DIC`; pairs failing old∉dic & new∈dic
> are rejected, report how many). Report the map size before/after and a sample of newly-merged forms,
> then `docs/ORTHO_DRIFT_FINDINGS.md` + `changelog.md`, and commit.

---

## Cleanup / low-priority (active-dev backlog)

- **Record SanskritSpellCheck as a `sanskrit-util` consumer** in the org `SHARED_CODE.md` migration
  queue (the detectors' `sanskrit_util.py` shim already delegates `devanagari_to_slp1`).
- `codecs.open(...)` → `open(..., encoding=...)` cleanup (cosmetic DeprecationWarnings on 3.14).
- `order_check` source-order list + the ported `sanhw1/2.py` vs the server scan trees (not runnable
  locally — needs the `<CODE>Scan/<year>/pywork` siblings).

## Blocked-on-external / human (not a no-setup fresh AI chat)

- **PD second source** — optional; register it as a 2nd tuple in `detectors/get_external_source.py`
  `SOURCES['PD']`, re-stage, re-run `/dict-triage PD`. Refines PD's 116-entry do-not-file list only.
- **Phase 2 installs** — OCR (`tesseract` + `san`, unblocks Task 1's gate), full DCS `dcs_full.sqlite`
  (VisualDCS release), GRETIL corpus download.
- **Applying corrections to `csl-orig`** — the human-eyes-on-scans step after Task 1's issue is filed;
  follow the csl-orig correction workflow in the org `CLAUDE.md`. Never bot-applied.
