# MW suspects — 2026 re-run (post tail-drop fix)

Fresh faultfinder run with **MW** as the base dictionary, June 2026, after the
`for`→`foreach` coverage fix in [faultfinder3a.php](../../faultfinder3a.php). The
historical 2017 run lives in [AllvsMW/](../../AllvsMW) and is left untouched as an
audit record; this directory is the current state.

Counts: **110** raw → **17 signal** + **93 noise**; the 17 signal split into
**12 priority** (non-rcc, verify first) and **5 post-repha** (low priority).
Almost all are `s…`/`h…` words — the tail of the Sanskrit alphabetical order that
the old loop never tested, so these are largely new, not "already-corrected".

## Files
- [AllvsMW.txt](AllvsMW.txt) — all 110 suspects, `X:P=Y:D` format.
- [AllvsMW-priority.txt](AllvsMW-priority.txt) — **verify-first list (12)**: the
  non-rcc anomalies (genuinely unusual clusters), with clickable
  [report](AllvsMW-priority.html). **Start here.**
- [AllvsMW-signal.txt](AllvsMW-signal.txt) — full review pool (17) = priority +
  post-repha; all suspects in ≥1 general dictionary.
- [AllvsMW-gemination.txt](AllvsMW-gemination.txt) — **post-repha subset (5)**:
  `r`+doubled-consonant variants ([report](AllvsMW-gemination.html)). **Low priority**
  — usually the faithful printed form (the generator's `rcc()` excludes it by default),
  not an error; review only for a normalization-policy call.
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
python triage_suspects.py Allvs_2026/MW/AllvsMW.txt Allvs_2026/MW/AllvsMW-signal.txt Allvs_2026/MW/AllvsMW-noise.txt  # also writes -priority.txt and -gemination.txt
php faultfinder3a-html.php Allvs_2026/MW/AllvsMW-priority.txt   Allvs_2026/MW/AllvsMW-priority.html   2  # 3rd arg 2 = render all rows
php faultfinder3a-html.php Allvs_2026/MW/AllvsMW-gemination.txt Allvs_2026/MW/AllvsMW-gemination.html 2
```
