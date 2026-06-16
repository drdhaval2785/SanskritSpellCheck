# Handoff — review another dictionary in a new chat

Open a new chat **in the SanskritSpellCheck repo, on Opus**, then either invoke the skill or
paste the self-contained prompt below. Swap `<DICT>` for a pending code (see the
[index](README.md) — highest tier-A first: `BHS` 737 · `SCH` 678 · `PUI` 518 · `SKD` 412 ·
`MW72` 360 …). Avoid `PD` (no csl-orig source) and the done ones (`MW`/`PW`/`VCP`/`PWG`/`SNP`).

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
workflow's Sonnet/Opus split is pinned internally). The TYPO pass is STOCHASTIC — do NOT re-run an
already-triaged dict (MW/PW/VCP/PWG/SNP); a fresh run can lose verified typos. Tier-A precision is
near-zero on mature dicts — the do-not-file list is the real deliverable, not the few typos.
```

## What you get

A `corrections_draft/<DICT>/` package: a pre-curated `<DICT>_file_first_sf.txt` (FILE-FIRST typos +
auto-commented false positives), a `<DICT>_wrong_readings.txt` do-not-file list, a `<DICT>_triaged.txt`
six-bucket queue, and a `readme.md` with the finding. Verify each kept case on the scan before filing
to [CORRECTIONS](https://github.com/sanskrit-lexicon/CORRECTIONS/issues).
