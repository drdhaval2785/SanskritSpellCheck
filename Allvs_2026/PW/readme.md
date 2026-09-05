_Created: 10-08-2026 · Last updated: 05-09-2026_

# PW suspects — 2026 re-run (post tail-drop fix)

Fresh faultfinder run with **PW** as the base dictionary, June 2026, after the
`for`→`foreach` coverage fix in [faultfinder3a.php](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/faultfinder3a.php). The
historical 2017 run is in [AllvsPW/](../../AllvsPW) (left untouched as audit record).

Counts: **183** raw → **58 signal** + **125 noise**; the 58 signal split into
**52 priority** (non-rcc, verify first) and **6 post-repha** (low priority).
Mostly `s…`/`h…` alphabet-tail words the old loop never tested, with the recurring
gemination signature (`-uttra-`, `-aRna-`, `-artti-`, `-urdda-`, `-fRRA-`).

## Files
- [AllvsPW.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/Allvs_2026/PW/AllvsPW.txt) — all 183 suspects (`X:P=Y:D`).
- [AllvsPW-priority.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/Allvs_2026/PW/AllvsPW-priority.txt) — **verify-first list (52)**: the
  non-rcc anomalies, with clickable [report](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/Allvs_2026/PW/AllvsPW-priority.html). **Start here.**
- [AllvsPW-signal.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/Allvs_2026/PW/AllvsPW-signal.txt) — full review pool (58) = priority +
  post-repha; all suspects in ≥1 general dictionary.
- [AllvsPW-gemination.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/Allvs_2026/PW/AllvsPW-gemination.txt) — **post-repha subset (6)**:
  `r`+doubled-consonant variants ([report](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/Allvs_2026/PW/AllvsPW-gemination.html)). **Low priority**
  — usually the faithful printed form, not an error.
- [AllvsPW-noise.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/Allvs_2026/PW/AllvsPW-noise.txt) — 125 specialized-dict-only suspects.
- [AllvsPW_sf.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/Allvs_2026/PW/AllvsPW_sf.txt) — standard format for CORRECTIONS submission.
- [AllvsPW-norepeat.html](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/Allvs_2026/PW/AllvsPW-norepeat.html),
  [dictwiseerrors3-table.html](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/Allvs_2026/PW/dictwiseerrors3-table.html) — clickable Cologne-link
  reports for verifying against the scans.

## Regenerate
```sh
php faultfinder3a.php      PW sanhw1.txt Allvs_2026/PW/AllvsPW.txt Allvs_2026/PW/AllvsPW_sf.txt
php faultfinder3a-html.php Allvs_2026/PW/AllvsPW.txt Allvs_2026/PW/AllvsPW-norepeat.html
php dictwisesorter-v3.php  Allvs_2026/PW/AllvsPW-norepeat.html Allvs_2026/PW/dictwiseerrors3-table.html
python triage_suspects.py Allvs_2026/PW/AllvsPW.txt Allvs_2026/PW/AllvsPW-signal.txt Allvs_2026/PW/AllvsPW-noise.txt  # also writes -priority.txt and -gemination.txt
php faultfinder3a-html.php Allvs_2026/PW/AllvsPW-priority.txt   Allvs_2026/PW/AllvsPW-priority.html   2  # 3rd arg 2 = render all rows
php faultfinder3a-html.php Allvs_2026/PW/AllvsPW-gemination.txt Allvs_2026/PW/AllvsPW-gemination.html 2
```

_Dr. Mārcis Gasūns_
