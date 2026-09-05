_Created: 10-08-2026 · Last updated: 05-09-2026_

# PWG suspects — 2026 re-run (post tail-drop fix)

Fresh faultfinder run with **PWG** as the base dictionary, June 2026, after the
`for`→`foreach` coverage fix in [faultfinder3a.php](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/faultfinder3a.php). The
historical 2017 run is in [AllvsPWG/](../../AllvsPWG) (left untouched as audit record).

Counts: **256** raw → **107 signal** + **149 noise**; the 107 signal split into
**99 priority** (non-rcc, verify first) and **8 post-repha** (low priority).
Mostly `s…`/`h…` alphabet-tail words the old loop never tested, with the recurring
gemination signature (`-uttra-`, `-aRna-`, `-arRRa-`, `-ArdDi-`) plus some long
proper-name compounds.

## Files
- [AllvsPWG.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/Allvs_2026/PWG/AllvsPWG.txt) — all 256 suspects (`X:P=Y:D`).
- [AllvsPWG-priority.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/Allvs_2026/PWG/AllvsPWG-priority.txt) — **verify-first list (99)**: the
  non-rcc anomalies, with clickable [report](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/Allvs_2026/PWG/AllvsPWG-priority.html). **Start here.**
- [AllvsPWG-signal.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/Allvs_2026/PWG/AllvsPWG-signal.txt) — full review pool (107) = priority +
  post-repha; all suspects in ≥1 general dictionary.
- [AllvsPWG-gemination.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/Allvs_2026/PWG/AllvsPWG-gemination.txt) — **post-repha subset (8)**:
  `r`+doubled-consonant variants ([report](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/Allvs_2026/PWG/AllvsPWG-gemination.html)). **Low priority**
  — usually the faithful printed form, not an error.
- [AllvsPWG-noise.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/Allvs_2026/PWG/AllvsPWG-noise.txt) — 149 specialized-dict-only suspects.
- [AllvsPWG_sf.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/Allvs_2026/PWG/AllvsPWG_sf.txt) — standard format for CORRECTIONS submission.
- [AllvsPWG-norepeat.html](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/Allvs_2026/PWG/AllvsPWG-norepeat.html),
  [dictwiseerrors3-table.html](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/Allvs_2026/PWG/dictwiseerrors3-table.html) — clickable Cologne-link
  reports for verifying against the scans.

## Regenerate
```sh
php faultfinder3a.php      PWG sanhw1.txt Allvs_2026/PWG/AllvsPWG.txt Allvs_2026/PWG/AllvsPWG_sf.txt
php faultfinder3a-html.php Allvs_2026/PWG/AllvsPWG.txt Allvs_2026/PWG/AllvsPWG-norepeat.html
php dictwisesorter-v3.php  Allvs_2026/PWG/AllvsPWG-norepeat.html Allvs_2026/PWG/dictwiseerrors3-table.html
python triage_suspects.py Allvs_2026/PWG/AllvsPWG.txt Allvs_2026/PWG/AllvsPWG-signal.txt Allvs_2026/PWG/AllvsPWG-noise.txt  # also writes -priority.txt and -gemination.txt
php faultfinder3a-html.php Allvs_2026/PWG/AllvsPWG-priority.txt   Allvs_2026/PWG/AllvsPWG-priority.html   2  # 3rd arg 2 = render all rows
php faultfinder3a-html.php Allvs_2026/PWG/AllvsPWG-gemination.txt Allvs_2026/PWG/AllvsPWG-gemination.html 2
```

_Dr. Mārcis Gasūns_
