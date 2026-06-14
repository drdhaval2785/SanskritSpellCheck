# MW suspects — 2026 re-run (post tail-drop fix)

Fresh faultfinder run with **MW** as the base dictionary, June 2026, after the
`for`→`foreach` coverage fix in [faultfinder3a.php](../../faultfinder3a.php). The
historical 2017 run lives in [AllvsMW/](../../AllvsMW) and is left untouched as an
audit record; this directory is the current state.

Counts: **110** raw suspects → **17 signal** (review these) + **93 noise**.
Almost all are `s…`/`h…` words — the tail of the Sanskrit alphabetical order that
the old loop never tested, so these are largely new, not "already-corrected".

## Files
- [AllvsMW.txt](AllvsMW.txt) — all 110 suspects, `X:P=Y:D` format.
- [AllvsMW-gemination.txt](AllvsMW-gemination.txt) — **highest-precision subset (5)**:
  post-repha doubling variants (`r` + doubled consonant), with clickable
  [report](AllvsMW-gemination.html). Verify these first.
- [AllvsMW-signal.txt](AllvsMW-signal.txt) — **the review list (17)**: suspects that
  appear in at least one *general* dictionary, sorted longest-word-first.
- [AllvsMW-noise.txt](AllvsMW-noise.txt) — 93 suspects found only in specialized
  dicts (Puranic/geographic/inscriptional names etc.); low priority.
- [AllvsMW_sf.txt](AllvsMW_sf.txt) — standard-format list for CORRECTIONS submission
  (`DICT:word:word:n`).
- [AllvsMW-norepeat.html](AllvsMW-norepeat.html),
  [dictwiseerrors3-table.html](dictwiseerrors3-table.html) — clickable reports with
  Cologne deep-links for verifying each word against the scans.

## Regenerate
```sh
php faultfinder3a.php      MW sanhw1.txt Allvs_2026/MW/AllvsMW.txt Allvs_2026/MW/AllvsMW_sf.txt
php faultfinder3a-html.php Allvs_2026/MW/AllvsMW.txt Allvs_2026/MW/AllvsMW-norepeat.html
php dictwisesorter-v3.php  Allvs_2026/MW/AllvsMW-norepeat.html Allvs_2026/MW/dictwiseerrors3-table.html
python triage_suspects.py Allvs_2026/MW/AllvsMW.txt Allvs_2026/MW/AllvsMW-signal.txt Allvs_2026/MW/AllvsMW-noise.txt
```
