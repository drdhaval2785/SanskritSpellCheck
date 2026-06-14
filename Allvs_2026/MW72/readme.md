# MW72 suspects — 2026 re-run (medium base → gemination-filtered)

Faultfinder run with **MW72** (Monier-Williams 1872) as base, June 2026.

MW72 turned out to be a **medium** base, not a large one: it matches 51,152 headwords
vs MW's 193,895. A smaller base has a narrower pattern inventory, so it over-flags —
**15,402** raw suspects, **8,496** after dropping specialized-dict-only noise, and even
that signal is dominated by *legitimate* long compounds (e.g.
`SrIvatsamuktikanandyAvartalakzitapARipAdatalatA`) the base simply never saw. Length
ranking is useless here.

So the review list is the **post-repha gemination subset** (see
[triage_suspects.py](../../triage_suspects.py)): only **9** suspects, all clear
orthographic variants (`r` + doubled consonant: varṇa→varṇṇa, durda→durdda,
-rya→-ryya, ūrma→ūrmma), all in general dictionaries (VCP/SHS/WIL/YAT/SKD).

## Files
- [AllvsMW72-gemination.txt](AllvsMW72-gemination.txt) — **the review list (9)**:
  post-repha variants, with clickable [report](AllvsMW72-gemination.html). Note these
  are usually the faithful printed form (the generator's `rcc()` excludes them by
  default), so they're low-confidence-as-errors — mostly a normalization-policy
  question. (MW72's non-rcc signal is the 8.5k-row noise, so there's no useful
  priority list for this base — unlike MW/PW/PWG.)
- [AllvsMW72.txt](AllvsMW72.txt) — full raw 15,402-suspect list, kept so the triage
  can be re-run with a different filter without re-running PHP.

The full signal/noise lists and the 15k-row HTML reports are **not** committed (low
precision, multi-MB). Regenerate them with:
```sh
php faultfinder3a.php      MW72 sanhw1.txt Allvs_2026/MW72/AllvsMW72.txt Allvs_2026/MW72/AllvsMW72_sf.txt
python triage_suspects.py Allvs_2026/MW72/AllvsMW72.txt Allvs_2026/MW72/AllvsMW72-signal.txt Allvs_2026/MW72/AllvsMW72-noise.txt
# -> also writes AllvsMW72-gemination.txt
php faultfinder3a-html.php Allvs_2026/MW72/AllvsMW72-gemination.txt Allvs_2026/MW72/AllvsMW72-gemination.html 2  # 3rd arg 2 = render rCC words
```
