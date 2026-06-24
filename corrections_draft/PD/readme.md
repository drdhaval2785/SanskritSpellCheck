# PD — source staged, triage pending a second source

**PD** is the *Encyclopaedic Dictionary of Sanskrit on Historical Principles* (A. M. Ghatage et al.,
Deccan College, Poona, 1976–2009; **English** glosses) — the one Cologne-listed dictionary that is
**not in the `csl-orig` merge**, so its body-grounded triage was blocked until its source was wired in.

## Status (2026-06-24)

**Source 1 of 2 is now staged and the dictionary is fully triageable.** A **second PD source is
expected** (to be provided); the triage is held until it lands so the run isn't redone.

- **Source 1:** `pdtxt.zip` → `pd.txt` from the Cologne PDScan 2020 edition
  ([web index](https://sanskrit-lexicon.uni-koeln.de/scans/PDScan/2020/web/index.php) ·
  [downloads](https://sanskrit-lexicon.uni-koeln.de/scans/PDScan/2020/web/webtc/download.html)).
  **55 MB, 107,630 entries.** Digitization with corrections; same `{#SLP1#}` / English-gloss markup
  family as the other dictionaries.
- **Staged at** (gitignored, not committed here): `external_src/pd/pd.txt`. Re-fetch on a clean
  clone with `python detectors/get_external_source.py PD`.
- **Source 2:** TBD — register its URL as a second tuple under `PD` in
  [detectors/get_external_source.py](../../detectors/get_external_source.py), then re-stage.

## License

Digital edition © 2014 **The Sanskrit Library and Thomas Malten**, **CC BY-NC-SA 3.0**
(non-commercial reuse with attribution + share-alike). The source text is therefore *not* committed
to this repo — only the do-not-file / FILE-FIRST lists produced from it would be.

## Wiring (how PD plugs into the existing pipeline)

`detectors/triage_util.py` resolves a dictionary's entry text through `source_file(dict_code)`:
an `external_src/<dict>/<dict>.txt` staging file wins, otherwise `csl-orig/v02/<dict>/<dict>.txt`.
PD is registered `en` in `triage_lang.py`. Everything else (the four-phase hybrid workflow, the
do-not-file synthesis, the suppression layer) is unchanged.

**Verified ready:** `python detectors/triage_dict.py PD` builds the package — **1,007 tier-A
candidates**, 87 settled deterministically as documented-intentional, **920 to body-judge, 0
unlocatable** (every PD headword resolved in the source).

## To run the triage (once source 2 is in, or now if desired)

```sh
cd detectors && python triage_dict.py PD          # build package + print workflow launch args
#   -> launch detectors/bodyaware_workflow.js with the printed args (Sonnet classify / Opus confirm/review)
python triage_dict.py PD --finish                 # synthesize PD_triaged.txt / PD_file_first_sf.txt / PD_wrong_readings.txt
cd detectors && python gen_do_not_file_suppress.py && python eval.py   # fold do-not-file into the suppression layer; FP must stay 0
```

Or just the **[`/dict-triage PD`](../../.claude/commands/dict-triage.md)** skill.
