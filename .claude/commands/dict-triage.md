_Created: 10-08-2026 · Last updated: 05-09-2026_

---
description: Body-grounded HYBRID triage of one Cologne dictionary's tier-A spell-check candidates — Sonnet classifies, Opus source-confirms, a human verifies against the entry text. Produces a FILE-FIRST queue + a do-not-file list. Arg = dict code (MW, PW, PWG, VCP, SCH, PD, ...).
argument-hint: <DICT>  (e.g. SCH)
---

# Hybrid body-grounded dictionary triage — `$ARGUMENTS`

Turn the engine's tier-A spelling candidates for **$ARGUMENTS** into a verified, prioritized
**FILE-FIRST** queue plus a standing **do-not-file** list, by judging each candidate against
the dictionary's **own entry text** (from `csl-orig`), not spelling alone. The LLM layer is a
*triage prior*; the dictionary entry (and ultimately the scan) is the truth.

## Why this exists (read once)
A spelling-only detector cannot tell a typo from a real word, an intentional variant, or
editorial apparatus. The entry can. Empirically, tier-A precision is **near zero** on mature
dictionaries (MW 4/1954 · PW 2/657 · VCP 1/563 · PWG 12/497) — so the durable deliverable is
the **do-not-file list** and *preventing bad bulk edits*, not the handful of real typos.

## Prerequisites
- Run from the **SanskritSpellCheck repo root**. `csl-orig` must be a sibling; the source is
  `csl-orig/v02/<dict>/<dict>.txt`.
- `detectors/combined_candidates.txt` must exist. If not: `cd detectors && python run_all.py ../sanhw1.txt`.
- If `$ARGUMENTS`'s body language is **not** English/German/Sanskrit, add a profile first —
  see **New language** at the bottom.

## Steps

1. **Build the package + get the launch args.** From the repo:
   ```sh
   cd detectors && python triage_dict.py $ARGUMENTS
   ```
   This runs make_dict_package → triage_enrich → triage_bodies → triage_body_batches and
   prints a `{scriptPath, args}` JSON. The args carry the body-language `hint` and the hybrid
   models `clsModel=sonnet` / `confModel=opus`. Note the body_kind split it reports (how many
   `realword` go to the LLM vs how many were settled intentional/unlocatable deterministically).

2. **Launch the body-aware workflow** with the printed args **verbatim** — call the **Workflow**
   tool with `scriptPath` = `detectors/bodyaware_workflow.js` and `args` = the printed object.
   Four phases, models pinned per-phase (no manual toggling): self-discover batches →
   **classify on Sonnet** → **source-confirm the TYPO pile on Opus** → **review the confirmed pile
   on Opus** (an adversarial false-positive gate — `revModel=opus`, regardless of your session
   model). It writes `body_adj_*.json` / `body_conf_*.json` / `body_review_*.json` into
   `corrections_draft/$ARGUMENTS/triage_work/`. Wait for completion.

3. **Synthesize** the package:
   ```sh
   python triage_dict.py $ARGUMENTS --finish
   ```
   → `$ARGUMENTS_triaged.txt`, `$ARGUMENTS_file_first_sf.txt`, `$ARGUMENTS_wrong_readings.txt`.

4. **Spot-check, then scan-confirm.** The Opus **Review** phase already ran the false-positive
   gate on every confirmed candidate, and `--finish` auto-comments the rejected ones in
   `$ARGUMENTS_file_first_sf.txt` (`; REVIEWED-OUT (vrddhi|variant|apparatus|redirect|realword): …`),
   so FILE-FIRST is pre-curated. Your job:
   - **Spot-check** a sample of the FILE-FIRST survivors *and* the reviewed-out lines by grepping
     `<k1>SUSPECT<` in `csl-orig/v02/<dict>/<dict>.txt`. The keep/drop rubric the review applied:
     **KEEP** only when the entry's *own* derivation/citation confirms the suggestion (e.g.
     `arTavanDa` quoted as `lalitArTabanDaM`; derivation `(paRa + ba°)`; **b/v (व/ब)** and
     **vowel-length** are the highest-yield classes). **DROP** for wrong-reading
     (`w.r.`/`fehlerhaft für`/`Richtig`/`v.l.`/`aSudDa`), redirect (`{{Lbody}}`/`See`/`s.`/`= X`),
     **vṛddhi** (`X von Y` / `Vṛddhi form of Y`), **attested variant** (both forms cited), or a
     **real distinct word**. If you disagree with a review verdict, flip the line by hand.
   - If apparatus is **systematically leaking into FILE-FIRST**, a deterministic marker is missing
     — add it to `triage_lang.py` (+ a `test_triage.py` case), then re-run `triage_bodies` + `--finish`.
   - **The scan is the final arbiter** — before filing, open the servepdf scan for each kept case
     (b/v: check व vs ब on the page). This step is irreducible.

5. **Write `corrections_draft/$ARGUMENTS/readme.md`** (model it on `corrections_draft/PW/readme.md`
   or `PWG/readme.md`): the finding (N fileable / tier-A), a FILE-FIRST table with **each
   candidate's in-entry evidence**, the reviewed-out false positives with reasons, the
   do-not-file sub-type counts, and the method.

6. **Commit** (`ai-wip:` prefix, with the Co-Authored-By trailer) the package files + any
   `triage_lang.py` / `test_triage.py` additions. Push only if asked. Gitignored (don't commit):
   `$ARGUMENTS_evidence.jsonl`, `triage_work/`.

## Key lessons — do NOT relearn these
- **The body-aware TYPO pass is STOCHASTIC.** Re-runs surface a different small handful and can
  *lose* genuine typos (an MW re-run once refuted 4 verified typos). **Never blindly overwrite a
  committed, verified package** with a fresh run. For recall, union across runs; otherwise keep
  the verified one.
- **The deterministic markers settle apparatus/redirects before the LLM** — that's the precision
  backbone and it's model-independent. Trust it; extend it when apparatus leaks.
- **Hybrid economics:** Sonnet on the bulk classify is ~40% cheaper; Opus only on the small
  confirm pass. Keep that split unless a dict's classify is unusually subtle.
- **Source-verify, don't trust the agent's "confirmed".** The confirm pass reads the source but
  has missed apparatus before (PW `Richtig`, MW `muka` glossed "smell of cow-dung"). Your grep of
  the entry is the gate.

## New language (dict body not en/de/sa)
In `detectors/triage_lang.py`: add the dict→lang mapping in `_LANG`, a `MARKERS[lang]` entry with
that gloss-language's wrong-reading / varia-lectio / in-composition / cross-reference regexes
(keep them **separator-independent** — body_text strips `¦`), and a `_HINT[lang]` paragraph for
the workflow rubric. Add a `test_triage.py` case (e.g. assert the wrong-reading marker classifies
`wr`). Then run steps 1–6.

_Dr. Mārcis Gasūns_
