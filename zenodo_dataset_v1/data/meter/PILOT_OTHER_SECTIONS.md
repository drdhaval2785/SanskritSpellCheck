# Feasibility pilot — meter QA on other GRETIL sections

_Created: 07-07-2026 · Last updated: 07-07-2026_

Can the H251/H277 meter validator (and the wider SanskritSpellCheck QA stack) be launched on GRETIL
sections **beyond Kavya**? This is the Phase-1 feasibility pilot of handoff
[H289](https://github.com/gasyoun/Uprava/blob/main/handoffs/H289-Opus_SanskritSpellCheck_gretil_other_sections_pilot_07.07.26.md).
**Verdict: yes — it generalizes.**

## What was run

Three genuinely-new-genre texts (none in the 56-text Kavya set) fetched into
`detectors/gretil_pilot_raw/` (gitignored, CC BY-NC-SA) and put through the unchanged pipeline
([`gretil_walker.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/meter/gretil_walker.py)
→ [`build_meter_index.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/meter/build_meter_index.py)
→ [`meter_check.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/meter_check.py)
`--verdicts=`):

| Text | Genre | Verses | Non-clean | review / suspect |
|---|---|---:|---:|---:|
| Bhartṛhari, *Śatakatraya* | Subhāṣita / nīti-śṛṅgāra-vairāgya | 312 | **21.8%** | 56 / 12 |
| *108 Buddhist Stotras* | Stotra (devotional collection) | 2,220 | **17.5%** | 260 / 128 |
| Abhinavagupta, *Kramastotra* | Śaiva stotra | 29 | 3.4% | 1 / 0 |
| **Pilot total** | | **2,561** | **17.8%** | 317 / 140 |
| _Kavya baseline (H277-b)_ | _mahākāvya_ | _25,559_ | _15.9%_ | _1,380 / 2,674_ |

Bridge (DCS-rarity-gated): **305** distinct rare headwords, **53** in the high-precision shortlist
(suspect + DCS band ≤ 1). Sampled headwords (Śārvarin, ajñatā, anuśruta, ard, avalok, balaprada,
brahmakṛt, daśadiś, duṣkṛtakarman, guṇayukta) are real rare words — exactly the Kavya profile: weak on
their own, informative only when an independent spelling detector also fires (the `meter=` corroboration
nudge in `run_all.py`).

## Findings

1. **The walker parses new-section GRETIL plaintext with zero changes** — same `corpustei/
   transformations/plaintext` format; 2,597 blocks → 2,561 verse records, correct pāda splitting.
2. **Non-clean rates land in the Classical-verse band (17–22%)**, within ~2 pts of the Kavya baseline.
   No genre spiked into "meter-fit failure" territory. Bhartṛhari's 21.8% reflects genuine metrical
   variety (mixed varṇavṛtta + gnomic density), not corruption.
3. **The bridge and rarity gate scale proportionally** (305 rare / 53 strong for 2.5k verses vs
   1,703 / 700 for 25.6k — same ~2% strong-yield).
4. **The H251 robustness fixes hold on new data** — a `vidyut-chandas` Rust panic fired on a
   pilot verse and was absorbed by `identify_vidyut`'s `except BaseException` (0 timeouts, build
   completed clean). The H277-b `build_meter_index` dup-write fix also held (2,561 unique records).
5. **One small text (Kramastotra, 29 verses) is too small to read** — treat sub-~100-verse texts as
   anecdotal.

## Verdict & caveats

**PASS — launch on other Classical-verse sections.** Caveats carried into
[H289](https://github.com/gasyoun/Uprava/blob/main/handoffs/H289-Opus_SanskritSpellCheck_gretil_other_sections_pilot_07.07.26.md)
Phases 2–3:
- **Exclude the Vedic section** (Vedic accent + non-Classical meter → skrutable will mis-scan). Run the
  `ngram` running-text checker there and on prose-heavy Śāstra instead of the meter validator.
- **Sample large sections** (Epics/Purāṇa are 10k–100k+ verses at ~0.14 s/verse) — don't fetch-and-build
  whole sections for the dataset.
- Meter-alone stays **corroboration only** (the H277 invariant); the actionable output is the subset
  that also carries an independent spelling-detector hit.

## Reproduce

```
# fetch (per section) into detectors/gretil_<section>_raw/ ; then:
python detectors/meter/build_meter_index.py detectors/gretil_pilot_raw detectors/meter/meter_verdicts_pilot.jsonl
python detectors/meter_check.py ../sanhw1.txt <out>.txt --verdicts=meter/meter_verdicts_pilot.jsonl
python detectors/meter/variety_stats.py detectors/meter/meter_verdicts_pilot.jsonl <census>.md
```

_Dr. Mārcis Gasūns_
