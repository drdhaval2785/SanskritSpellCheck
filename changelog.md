# Changelog

All notable changes to SanskritSpellCheck are documented here.

This repository does not currently publish versioned release notes. Entries use
dated maintenance snapshots; keep upcoming work under [Unreleased] until it is
ready for a dated entry.

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
