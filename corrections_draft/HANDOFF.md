_Created: 10-08-2026 · Last updated: 05-09-2026_

# Handoff — (re)triage a dictionary in a new chat

> **All 33 dictionaries are already triaged** (see the [index](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/README.md)). There is **no pending
> dict left to triage for the first time.** This handoff now serves **re-runs** — most usefully
> **PD once its optional second source is wired in** (register it in
> [../detectors/get_external_source.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/get_external_source.py) `SOURCES['PD']`, re-stage,
> re-run). PD is read from a staged external source (`external_src/pd/`), not `csl-orig`.

Open a new chat **in the SanskritSpellCheck repo, on Opus**, then either invoke the skill or paste
the self-contained prompt below, swapping `<DICT>` for the code to re-run. **⚠️ The TYPO pass is
stochastic — a fresh run can *lose* verified typos, so don't blindly overwrite a committed package;**
re-run only with reason (a new/second source, or to extend recall by unioning across runs).

## Shortest form — if the `/dict-triage` command is loaded

```
/dict-triage BHS
```

The skill carries the whole procedure, the Sonnet/Opus split, and the guardrails.

## Self-contained prompt — works even if the command list hasn't loaded

```
I'm in the SanskritSpellCheck repo (drdhaval2785/SanskritSpellCheck; csl-orig is a sibling
clone). Triage the Cologne dictionary <DICT> with the body-grounded pipeline and produce its
correction package.

Follow the canonical procedure in .claude/commands/dict-triage.md (the /dict-triage skill) —
read it and the index corrections_draft/README.md first. Then: from the repo root run
`cd detectors && python triage_dict.py <DICT>` (it prints the Workflow launch args), launch
detectors/bodyaware_workflow.js via the Workflow tool with those args (4 phases — Sonnet
classify, Opus confirm, Opus review — pinned), wait, then `python triage_dict.py <DICT> --finish`.
If combined_candidates.txt is missing, first run `python run_all.py ../sanhw1.txt`.

Then spot-check a few FILE-FIRST survivors AND the auto-commented "REVIEWED-OUT" lines against
the source entries (grep "<k1>SUSPECT<" in csl-orig/v02/<dict>/<dict>.txt) per the skill's
keep/drop rubric; write corrections_draft/<DICT>/readme.md (model it on PWG/readme.md); update
the index corrections_draft/README.md (mark <DICT> triaged with results, drop it from the pending
list), changelog.md and .ai_state.md; then commit (ai-wip: prefix + the
"Co-Authored-By: Claude Opus 4.8 (1M context)" trailer) and push.

Guardrails: keep this session on OPUS (orchestration + spot-check run on the session model; the
workflow's Sonnet/Opus split is pinned internally). The TYPO pass is STOCHASTIC — all 33 dicts are
already triaged, so re-run one ONLY with reason (a new/second source, or to union across runs for
recall); a fresh run can lose verified typos, so don't blindly overwrite the committed package. Tier-A
precision is near-zero on mature dicts — the do-not-file list is the real deliverable, not the few typos.
```

## What you get

A `corrections_draft/<DICT>/` package: a pre-curated `<DICT>_file_first_sf.txt` (FILE-FIRST typos +
auto-commented false positives), a `<DICT>_wrong_readings.txt` do-not-file list, a `<DICT>_triaged.txt`
six-bucket queue, and a `readme.md` with the finding. Verify each kept case on the scan before filing
to [CORRECTIONS](https://github.com/sanskrit-lexicon/CORRECTIONS/issues).

_Dr. Mārcis Gasūns_
