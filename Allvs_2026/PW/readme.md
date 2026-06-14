# PW suspects — 2026 re-run (post tail-drop fix)

Fresh faultfinder run with **PW** as the base dictionary, June 2026, after the
`for`→`foreach` coverage fix in [faultfinder3a.php](../../faultfinder3a.php). The
historical 2017 run is in [AllvsPW/](../../AllvsPW) (left untouched as audit record).

Counts: **183** raw suspects → **58 signal** (review these) + **125 noise**.
Mostly `s…`/`h…` alphabet-tail words the old loop never tested, with the recurring
gemination signature (`-uttra-`, `-aRna-`, `-artti-`, `-urdda-`, `-fRRA-`).

## Files
- [AllvsPW.txt](AllvsPW.txt) — all 183 suspects (`X:P=Y:D`).
- [AllvsPW-gemination.txt](AllvsPW-gemination.txt) — **highest-precision subset (6)**:
  post-repha doubling variants (`r` + doubled consonant), with clickable
  [report](AllvsPW-gemination.html). Verify these first.
- [AllvsPW-signal.txt](AllvsPW-signal.txt) — **review list (58)**: appears in ≥1
  general dictionary, sorted longest-word-first.
- [AllvsPW-noise.txt](AllvsPW-noise.txt) — 125 specialized-dict-only suspects.
- [AllvsPW_sf.txt](AllvsPW_sf.txt) — standard format for CORRECTIONS submission.
- [AllvsPW-norepeat.html](AllvsPW-norepeat.html),
  [dictwiseerrors3-table.html](dictwiseerrors3-table.html) — clickable Cologne-link
  reports for verifying against the scans.

## Regenerate
```sh
php faultfinder3a.php      PW sanhw1.txt Allvs_2026/PW/AllvsPW.txt Allvs_2026/PW/AllvsPW_sf.txt
php faultfinder3a-html.php Allvs_2026/PW/AllvsPW.txt Allvs_2026/PW/AllvsPW-norepeat.html
php dictwisesorter-v3.php  Allvs_2026/PW/AllvsPW-norepeat.html Allvs_2026/PW/dictwiseerrors3-table.html
python triage_suspects.py Allvs_2026/PW/AllvsPW.txt Allvs_2026/PW/AllvsPW-signal.txt Allvs_2026/PW/AllvsPW-noise.txt
```
