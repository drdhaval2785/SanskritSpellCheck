# Union-across-runs scale-up (ruling D9) — scope call and measured results

_Created: 04-08-2026 · Last updated: 04-08-2026_

Handoff [H1709](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1709-Opus_SanskritSpellCheck_union-across-runs-scale-up-d9_26.07.26.md)
— executed by Claude Code, Opus 5 (`claude-opus-5`), 04-08-2026. Successor to
[H1471](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1471-Opus_SanskritSpellCheck_union-across-runs-recall-harvest-d7_22.07.26.md)
(ruling D7, measured in
[HYPOTHESES H9](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/HYPOTHESES.md)).

## Why this is funded — contamination, not recall

D7's measured gain (+70 net-new fileable typos, +81%, 35% single-run agreement over
SHS/YAT/ACC) reopened the standing "full union across the 11 fileable dicts" non-goal,
which had been ruled out on precision grounds. MG ruled it funded 26-07-2026 on a
different basis:

> *"Otherwise the bad headwords will spoil the general headword list."*

An uncorrected typo headword does not stay inside its own dictionary's FILE-FIRST
queue. It flows into the cross-dict union headword list
([detectors/union_attestation.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/union_attestation.py),
`HeadwordLists/union/union_headwords.tsv` in
[SanskritLexicography](https://github.com/gasyoun/SanskritLexicography)), whose
attestation tag `run_all.py` reads to demote broadly-attested suspects out of tier A.
So a typo never corrected inflates its own attestation count and thereby helps
**suppress its own detection** — a self-reinforcing loop that degrades every other
consumer of the shared list. The payoff is protecting a shared asset, not the handful
of corrections a mature dictionary yields.

## Step 0 — the scope call (made 04-08-2026, in writing, before any run)

**Call: the 11 fileable dicts.** Second independent body-aware run on the eight not
covered by D7 — PWG · MCI · MW · SKD · WIL · PW · VCP · GST — unioned against their
committed packages. SHS/YAT/ACC were already done by D7.

**The 22 zero-fileable dicts are deliberately NOT swept in this pass**, and are handed
back as a separate, evidence-led question rather than assumed either way. The
contamination logic genuinely points at the wider scope — a 0-fileable verdict is
itself one stochastic draw, and the D7 measurement says a single draw recovers only
~1/3 of a two-run union. But that argument is cheap to *test* and expensive to *assume*:
the handoff's own recommendation is to re-run two of the 22 and see whether either
yields anything. That probe is scoped as follow-on work (see "Open" below), not folded
into this pass, so the 11-dict number lands clean and is not held hostage to a
much larger run.

Rationale for taking the narrower reading first: it is exactly the non-goal D9 lifted,
so the decision behind it is already made; the wider reading needs a fresh
cost/benefit that the probe supplies for two dicts' worth of budget instead of 22.

## Method

Identical to D7, and deliberately so — the two runs must be comparable like for like.

- Deterministic prep only: `triage_enrich.py` → `triage_bodies.py` →
  `triage_body_batches.py`. **`make_dict_package.py` was not run** (it rewrites the
  committed package) and **`triage_dict.py --finish` was not run** (`triage_synthesize.py`
  overwrites `<DICT>_file_first_sf.txt` with the new run's verdicts and destroys run 1's
  finds — the trap H1471 had to route around).
- One body-aware run per dict via
  [detectors/bodyaware_workflow.js](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/bodyaware_workflow.js):
  Sonnet 5 (`claude-sonnet-5`) classify → Opus 5 (`claude-opus-5`) source-confirm →
  Opus 5 adversarial false-positive review. Per-phase attribution per ruling D1.
- Union + measurement with
  [detectors/union_across_runs.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/union_across_runs.py),
  which reconstructs run 2's FILE-FIRST set from the gitignored `triage_work/` verdicts
  using `triage_synthesize.py`'s own survival rule
  (`confirm.is_typo ∧ (review absent ∨ review.fileable)`).
- All work in a session-unique worktree off `origin/master`; committed packages never
  overwritten.

## Results

3,045 candidates re-judged across the eight dicts (4,280 tier-A, of which 1,235 were settled
deterministically before the LLM). Agreement is set overlap ÷ union (Jaccard).

| dict | run 1 (committed) | run 2 | in both | **net-new** | run-1-only | union | agreement |
|---|--:|--:|--:|--:|--:|--:|--:|
| PWG | 12 | 11 | 7 | **4** | 5 | 16 | 44% |
| WIL | 3 | 3 | 1 | **2** | 2 | 5 | 20% |
| SKD | 3 | 2 | 1 | **1** | 2 | 4 | 25% |
| GST | 1 | 1 | 0 | **1** | 1 | 2 | 0% |
| MCI | 10 | 9 | 9 | 0 | 1 | 10 | 90% |
| MW | 4 | 0 | 0 | 0 | 4 | 4 | 0% |
| PW | 2 | 0 | 0 | 0 | 2 | 2 | 0% |
| VCP | 1 | 0 | 0 | 0 | 1 | 1 | 0% |
| **total** | **36** | **26** | **18** | **+8 (+22%)** | **18** | **44** | **41%** |

Union table: [corrections_draft/union_d9.tsv](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/union_d9.tsv)
(44 rows; every net-new row carries its Opus confirm reason **and** its Opus review verdict +
false-positive type).

**The pool is not the explanation.** `r1:pool` = 0 and `r1:settled` = 0 for every dict: not one
of the 36 committed run-1 rows has dropped out of today's tier A or become settled
deterministically. All 18 non-reproductions are genuine run-to-run LLM variance.

**8 of 8 net-new hand-verified** against the entry text (the whole set, not a sample — D7 could
only afford 10 of 70). All eight fall into two checkable classes:

| class | cases | evidence in the entry |
|---|---|---|
| the `<lex>` gender tag contradicts the headword's final vowel | PWG `citrikA`→`citrika` (`m.` = `cEtrika`), `kxptakIla`→`kxptakIlA` (`f.`), `mAlArizwa`→`mAlArizwA` (`f.`); SKD `mahotka`→`mahotkA` (`strI`, `yasyAH`, gloss `vidyut`) | the entry's own gender marking |
| the entry's own derivation/inflection spells the base differently | PWG `pARivanDa`→`pARibanDa` (`{#pA˚#} + {#ba˚#}`, and it sorts in the b slot beside `pARiBuj`); GST `aDoGaRWA`→`aDoGaRwA` (`({#-RwA#})`, `E. {#aDas#} and {#GaRwA#}`); WIL `paYcaSErizaka`→`paYcaSErIzaka` (`E. {#paYca#}, and {#SirIza#}` — long ī, cf. WIL's own `SirIza` L38344), `vapuzmAt`→`vapuzmat` (`({#-zmAn-zmantI-zmat#})`) | etymology / inflection line |

### What this changes about D7's number

D7 measured **+81%** on SHS/YAT/ACC; this pass measures **+22%** on the other eight. The gap is
the H2 axis, not a contradiction: D7's three dicts are the poorly-digitised outliers, where both
runs have plenty to find and diverge on much of it. The eight here are mature and much-corrected,
so both runs find little and the union adds proportionally less. **PWG — the one poorly-digitised
source in this set — supplies half the net-new (4 of 8) off 11% of the candidate volume.**

Across both passes the combined picture is **11 dicts, 122 → 200 fileable (+78 net-new, +64%)**.
The instability itself replicates cleanly at 41% agreement here against D7's 35%.

**Three dicts (MW, PW, VCP) returned run-2 zeros against non-zero committed counts** — 7 committed
typos that a second full run did not reproduce, none of them explicable by pool movement. On a
mature dictionary a single run's near-zero yield is evidently as much noise as signal, which
strengthens rather than weakens H2's ordering claim: the *count* is unstable, the *ranking* is not.

### Run hygiene — two failure modes worth recording

Both were caught by auditing on-disk artifacts against the workflow's own return values, and
neither is visible in the return value alone.

1. **A dropped Confirm batch reads as `confirmedTypos: 0`.** VCP's single confirm agent died
   mid-response twice; the summary reported 0 confirmed both times. It had in fact written all 13
   verdicts to disk and failed only in the return channel — all 13 genuinely refuted (mostly VCP's
   parenthetical variant convention, `PeRa(na)vAhin` with a `{{Lbody=}}` redirect twin). The
   number was recoverable because `union_across_runs.py` reads `triage_work/`, not the summary.
   **A per-dict zero taken off a workflow summary is untrustworthy; one taken off disk is real.**
2. **A classify agent can return verdicts without writing its `body_adj_*.json`.** MW batch 000
   (30 candidates) and WIL batch 003 (16) reported full classified counts — 1554 and 106 — with
   no file on disk. Those verdicts still reached Confirm in memory, so no candidate went unjudged
   and no net-new row lost its suggestion; the cost is a hole in the reproducibility trail. A
   coverage check (`body_batch_NNN.jsonl` ⇄ `body_adj_NNN.json`, per dict) should run before any
   union is trusted.

Nine of the fourteen workflow launches needed at least one resume (`resumeFromRunId`) for
connection-drop or stalled-stream failures. Resume replays cached agents, so the retry cost is
confined to the failed batch — but the Review phase re-batches over the *new* confirmed set, and
that legitimately changes verdicts: SKD's resume reversed two earlier survivors
(`pUzaBAzA`, `vfzaBAzA`) once the adversarial gate saw the full pile.

## Open

- ~~**The 22 zero-fileable dicts.** Cheap probe: re-run two of the highest-volume ones
  (BHS 713 tier-A, SCH 678) and see whether either yields a single fileable typo.~~
  **✅ ANSWERED 04-08-2026 ([H2281](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2281-Opus_SanskritSpellCheck_zero-fileable-dicts-rerun-probe_04.08.26.md)) — do NOT sweep the 22.**
  Both re-runs returned **0 fileable**, matching their committed zeros: BHS 551 candidates
  re-judged (15 classified TYPO, all refuted at source-confirm), SCH 644 (8 classified TYPO,
  all refuted). 1,195 candidates, 23 survivors of the classify stage, **0 confirmed**.
  The pipeline was not inert — it produced a normal-looking TYPO pile both times; the pile
  simply did not survive contact with the full entry.

  **The reason matters more than the number: these zeros are STRUCTURAL, not stochastic**, and
  the two dicts fail in two different ways —

  | dict | why every candidate died |
  |---|---|
  | **BHS** (Edgerton) | the dictionary carries its **own critical apparatus** and has already labelled its misprints: `[laṭikā, app. misprint for latikā (so Index)]`, `[Anantaryasamādhi, misprint in Mvy 901 for Ānant˚; corrected in Index]`, `[adhyāśana, (probably error) for Skt. adhyāsana]`. The detector re-finds what the lexicographer annotated — and "correcting" it would destroy the apparatus. |
  | **SCH** (Schmidt) | the **body corroborates the headword**: key and gloss agree, so the minimal-pair suggestion is simply wrong — `girī` a distinct cvi-adverb, `samadhurā` a feminine, `yudda` = *yud+da* "battle-giving", `Kalindī` short-*a* in the body too. |

  Neither mechanism is a coin-flip that a third run might land differently, which is exactly
  what distinguishes this from the SHS/YAT/ACC instability H9 measured. A dictionary whose zero
  comes from *self-documenting apparatus* or from *internal corroboration* will keep returning
  zero. **Generalisation, stated as the limit it is:** 2 of 22 tested, chosen as the highest-volume
  cases and therefore the most likely to yield something. They did not. Extending the sweep to the
  other 20 — smaller, and mostly the same mature/foreign-gloss/specialist-index kinds — is not
  supported by this evidence. Refutation evidence for all 23:
  [REFUTED_TYPO_CANDIDATES_PROBE22.tsv](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/REFUTED_TYPO_CANDIDATES_PROBE22.tsv).
- **The scan-verification sheet is short by 78 rows, and regenerating it will not fix that.**
  [detectors/gen_scanverify_sheet.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/gen_scanverify_sheet.py)
  builds the sheet from `corrections_draft/file_first_verified.tsv`, taking the rows whose
  `verdict` is `PASS` or `SCAN-FIRST` — 109 of its 122 rows. Those 122 are the **run-1**
  population. D7's 70 net-new and this pass's 8 are not in that file at all and carry no
  verdict, so re-running the generator today reproduces the same 109 rows.
  The real prerequisite is upstream and is **not** an agent's call: the 78 net-new need a
  verdict assigned into `file_first_verified.tsv` (PASS / SCAN-FIRST / EDITORIAL / DROP / DNF)
  before the sheet can cover the queue. Until that happens the human gate silently covers
  ~58% of the fileable population. Both union tables carry the evidence each row needs —
  [union_d7.tsv](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/union_d7.tsv)
  and [union_d9.tsv](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/union_d9.tsv).
- **The union headword list rebuild** in
  [SanskritLexicography](https://github.com/gasyoun/SanskritLexicography)
  `HeadwordLists/union/` is what closes the contamination loop D9 names — it depends on
  corrections actually being *filed*, which runs through the monthly batched csl-orig PR
  with its human scan-verification gate, not through this repo.

_Dr. Mārcis Gasūns_
