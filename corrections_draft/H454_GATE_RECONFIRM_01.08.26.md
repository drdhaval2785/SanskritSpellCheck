# H454 gate reconfirm — 01-08-2026

_Created: 01-08-2026 · Last updated: 01-08-2026_

**Model:** Grok 4.5 (`grok-4.5`) — override dual-run of Sonnet-locked
[H454](https://github.com/gasyoun/Uprava/blob/main/handoffs/H454-Sonnet_SanskritSpellCheck_corrections-batched-pr-switchover_10.07.26.md)
(MG override "run"). Prior Fable 5 (`claude-fable-5`) attempt 10-07-2026 shipped
scan-verify sheet tooling (PR #29 / v1.50.0).

## Independent measurement (this pass)

| Metric | Value |
|---|---|
| FILE-FIRST queue files scanned | all `corrections_draft/*/*_file_first_sf.txt` |
| Total `:y` (scan-approved) | **0** |
| Total `:n` (not yet approved) | **122** |
| Per-dict non-zero | SHS 37 · YAT 27 · ACC 22 · PWG 12 · MCI 10 · MW 4 · SKD 3 · WIL 3 · PW 2 · VCP 1 · GST 1 |
| decisions.json from scan sheet | **none** on disk under repo / review / Downloads |
| Sheet HTML present | `review/sanskritspellcheck-filefirst-scanverify_109rows_review.html` (gitignored, regenerable) |

Reproduce:

```text
python corrections_draft/h454_gate_census.py
```

Exit code `2` = gate closed (zero `:y`).

## What this pass did (and did not)

**Did**

1. Reconfirmed the absolute H454 guard: change files must not start without `:y`.
2. Hardened [detectors/make_changefiles.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/make_changefiles.py)
   so trailing `:n` / unknown flags are skipped (previously any
   `DICT:wrong:right[:flag]` row entered drafts — silent gate bypass if a queue
   file was passed as input).
3. Added this census script + durable report.

**Did not** (guard / handoff non-goals)

- Invent or auto-flip any `:n` → `:y`
- Generate batch-1 change files
- Open a `csl-orig` PR
- Post a false "prepared" comment on [CORRECTIONS#447](https://github.com/sanskrit-lexicon/CORRECTIONS/issues/447)

## Resume after human votes

1. Vote sheet: open `review/sanskritspellcheck-filefirst-scanverify_109rows_review.html`
   (regenerate: `python detectors/gen_scanverify_sheet.py`).
2. `python corrections_draft/apply_scanverify_decisions.py <decisions.json> --apply`
3. `python corrections_draft/h454_gate_census.py` → expect GATE OPEN
4. Concatenate approved queues / pass `:y` lines into `make_changefiles.py`
5. XML-validate → `/cologne-correction-queue` → batch 1 report for MG auth
6. One factual follow-up on #447 only after real change files exist

_Dr. Mārcis Gasūns_
