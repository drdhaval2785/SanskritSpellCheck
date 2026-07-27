_Created: 27-07-2026 · Last updated: 27-07-2026_

# Monthly detection loop (H1533)

State for [`.github/workflows/monthly-detection-loop.yml`](../../.github/workflows/monthly-detection-loop.yml),
driven by [`detectors/monthly_loop.py`](../monthly_loop.py) — a monthly cron
(1st of the month, plus `workflow_dispatch` for manual runs) that re-runs
`run_all.py`'s full detector suite, applies the existing suppression layer
(`nochange.txt` ∪ `do_not_file_suppress.txt`, already filtered inside
`run_all.aggregate()`), and diffs the resulting tier-A candidates against the
committed baseline here to surface what's genuinely NEW since last cycle.

- **`tier_a_baseline.txt`** — the full tier-A candidate set as of the last
  run, in `run_all.py`'s native row format (`A\t<score>\t<suspect> ->
  <suggestion>\t[detectors]\t[dicts]...`). Overwritten each cycle; this is
  what the next cycle diffs against, not a hand-curated list.
- **`reports/<YYYY-MM>.md`** — one dated delta report per cycle: counts, the
  new tier-A candidates (capped at 200 rows inline; the full set is always in
  `tier_a_baseline.txt`), and anything that dropped out of tier A since the
  prior cycle (suppressed, corrected upstream, or re-tiered).

When a cycle's report shows a non-empty delta, the workflow opens/updates a
PR with the refreshed baseline + report — that PR is the trigger point for a
human/agent triage session (e.g. [`/dict-triage`](../../.claude/commands/dict-triage.md)-style
review of the new candidates) per [ROADMAP_2026_2027.md](../../ROADMAP_2026_2027.md)
Q4 item 5. No PR is opened when nothing changed.

_Dr. Mārcis Gasūns_
