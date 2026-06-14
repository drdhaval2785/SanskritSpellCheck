# PWG suspects — 2026 re-run (post tail-drop fix)

Fresh faultfinder run with **PWG** as the base dictionary, June 2026, after the
`for`→`foreach` coverage fix in [faultfinder3a.php](../../faultfinder3a.php). The
historical 2017 run is in [AllvsPWG/](../../AllvsPWG) (left untouched as audit record).

Counts: **256** raw suspects → **107 signal** (review these) + **149 noise**.
Mostly `s…`/`h…` alphabet-tail words the old loop never tested, with the recurring
gemination signature (`-uttra-`, `-aRna-`, `-arRRa-`, `-ArdDi-`) plus some long
proper-name compounds.

## Files
- [AllvsPWG.txt](AllvsPWG.txt) — all 256 suspects (`X:P=Y:D`).
- [AllvsPWG-signal.txt](AllvsPWG-signal.txt) — **review list (107)**: appears in ≥1
  general dictionary, sorted longest-word-first.
- [AllvsPWG-noise.txt](AllvsPWG-noise.txt) — 149 specialized-dict-only suspects.
- [AllvsPWG_sf.txt](AllvsPWG_sf.txt) — standard format for CORRECTIONS submission.
- [AllvsPWG-norepeat.html](AllvsPWG-norepeat.html),
  [dictwiseerrors3-table.html](dictwiseerrors3-table.html) — clickable Cologne-link
  reports for verifying against the scans.

## Regenerate
```sh
php faultfinder3a.php      PWG sanhw1.txt Allvs_2026/PWG/AllvsPWG.txt Allvs_2026/PWG/AllvsPWG_sf.txt
php faultfinder3a-html.php Allvs_2026/PWG/AllvsPWG.txt Allvs_2026/PWG/AllvsPWG-norepeat.html
php dictwisesorter-v3.php  Allvs_2026/PWG/AllvsPWG-norepeat.html Allvs_2026/PWG/dictwiseerrors3-table.html
python triage_suspects.py Allvs_2026/PWG/AllvsPWG.txt Allvs_2026/PWG/AllvsPWG-signal.txt Allvs_2026/PWG/AllvsPWG-noise.txt
```
