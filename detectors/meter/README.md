# Batch chandas (meter) validator

_Created: 06-07-2026 · Last updated: 07-07-2026_

Detector #7 (`meter_check.py`, one level up) -- a pAda that breaks its
identified meter is a suspect-text signal, fed into
[`run_all.py`](../run_all.py)'s cross-detector scoring as a ranking nudge (see
that file's `DETECTORS` list and the guard comment on `HIGH_PRECISION`).
Built per [`H251`](https://github.com/gasyoun/Uprava/blob/main/handoffs/H251-Sonnet_SanskritSpellCheck_chandas_validator_q1_2027_build_06.07.26.md),
following on the pilot in
[`docs/CHANDAS_ANUPRASA_PRIOR_ART.md`](../../docs/CHANDAS_ANUPRASA_PRIOR_ART.md) §4.

## Pipeline

```
gretil_walker.py      -- parse GRETIL corpustei plaintext -> verse records
meter_ident.py         -- skrutable + chanda + vidyut-chandas 3-way vote -> verdict
build_meter_index.py   -- offline, corpus-scale: walker + ident -> meter_verdicts.jsonl
reprocess_verdicts.py  -- recompute verdicts from a built index (verdict()-only changes; no tool re-run)
variety_stats.py       -- meter / anuṣṭubh pāda-variety census -> METER_VARIETY_STATS.md
headword_bridge.py     -- word -> dictionary-headword bridge (vidyut.cheda lemmatizer)
../meter_check.py      -- reads meter_verdicts.jsonl + live sanhw1.txt -> meter_suspects.txt (+ _strong sibling)
```

Each `meter_verdicts.jsonl` record stores skrutable's **pāda-segmented text**
(`skrutable.padas` / `skrutable.pada_weights`, `\n`-split per pāda, from H277-b's
rebuild) — the 1-based keys of `problem_padas` index into it, so a future bridge can
localize lemmatization to the actually-flagged pāda without re-running skrutable.

`meter_verdicts.jsonl` stores each verse's raw `skrutable`/`chanda`/`vidyut` tool
outputs alongside its `verdict`, so a change to the VERDICT-COMPUTATION alone
(`meter_ident.verdict()`) is re-derived in seconds with
[`reprocess_verdicts.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/meter/reprocess_verdicts.py)
(dry-run prints an old→new confusion matrix; `--apply` rewrites in place) —
**no** re-invocation of skrutable/chanda/vidyut over the corpus. Only a change to
the per-verse IDENTIFICATION logic needs a full `build_meter_index.py` rerun.

`build_meter_index.py` is the only expensive step (~0.14 s/verse, ~26k verses
in the Kavya section -> ~1 hour) and is **not** re-run by `run_all.py` itself
-- rerun it by hand when the corpus changes or a tool version bumps.
`meter_check.py` is cheap (reads the cached jsonl) and runs on every
`run_all.py` invocation like the other detectors.

## Corpus fetch (not committed -- see `.gitignore`)

GRETIL's Kavya section is CC BY-NC-SA (third-party text) -- same
"don't commit external source text" rule as `external_src/` (§ root
`CLAUDE.md`). Fetch it fresh:

```sh
# 1. Discover the file list from GRETIL's own master catalogue (its directory
#    listing is 403-forbidden, but direct file fetches are fine and the
#    catalogue page itself lists every text under its <h4 id="Kavya"> section):
curl -s -A "Mozilla/5.0" https://gretil.sub.uni-goettingen.de/gretil.html -o /tmp/gretil.html
# extract hrefs between <h4 id="Kavya"> and the next <h4 id=...> heading,
# keep the .../corpustei/transformations/plaintext/*.txt links (57 texts, 06-07-2026)

# 2. Download each into detectors/gretil_kavya_raw/
mkdir -p detectors/gretil_kavya_raw
# curl -s -A "Mozilla/5.0" "https://gretil.sub.uni-goettingen.de/<path>" -o "detectors/gretil_kavya_raw/<name>.txt"

# 3. Verify no error pages landed (404s look like a tiny "<!DOCTYPE HTML ... 404 Not Found" file)
#    and no truncated UTF-8 (retry any file that fails: python -c "open(f,encoding='utf-8').read()")

# 4. Build the index (~30-90 min depending on machine load; resumable -- reruns
#    skip verses already recorded, so a kill/crash mid-run just needs a rerun)
python detectors/meter/build_meter_index.py
```

## Actual results (full corpus, recalibrated H277 07-07-2026)

25,824 verse-shaped blocks parsed (9,005 blocks skipped for having no locus
tag -- prose/commentary interleaving; 184 blocks skipped as prose by the
`MAX_VERSE_CHARS` filter below):

| Verdict | H251 (initial, 25,824 recs) | H277 (recalibrated + rebuilt, 25,559 recs) |
|---|---|---|
| clean   | 15,772 (61.1%) | **21,505 (84.1%)** |
| review  |  6,357 (24.6%) |  **1,380 (5.4%)** |
| suspect |  3,695 (14.3%) |  **2,674 (10.5%)** |

_(The H277 column is the canonical post-rebuild index — 25,559 unique verse records after
the walker prose-strip + dedup, vs H251's 25,824 which double-counted 265 repeated loci.)_

The initial H251 run's 39.1% non-clean rate was, per user review
(07-07-2026), implausibly high — "no human will check so many; in all the
Cologne dictionaries we had 120+ suspected words before". The **H277
recalibration** root-caused and fixed it (see next section): non-clean fell
to **15.9%**, and the bridge — now DCS-rarity-gated and consumed by
`run_all.py` as a corroboration nudge only — flags **1,719** distinct *rare*
headwords (`detectors/meter_suspects.txt`), of which only ~46 also carry an
independent spelling-detector signal (the informative set).

## Recalibration (H277, 07-07-2026)

The 39% non-clean rate was **over-flagging valid poetry**, not finding
corruption. Root cause, in two parts:

1. **skrutable's `is_perfect=False` is not corruption evidence.** It means "this
   is not the single most-regular sub-pattern (pathyā)", and fires on named,
   metrically valid varieties — anuṣṭubh with a *vipulā* / *asamīcīnā*, an
   *upajāti* triṣṭubh mix — which are standard Classical poetic license. ~24.7%
   of the corpus was `is_perfect=False` with an **empty `problem_padas`** (no
   localized broken syllable named).
2. **The chanda meter-identity cross-check fired on valid varieties.** skrutable's
   verbose variety labels (`upajāti triṣṭubh: indravajrā 1,2,4; upendravajrā 3`)
   are not string-comparable to chanda's per-line names, so "chanda disagrees"
   was flagged as `review` on perfectly valid verses.

**Fix** (`meter_ident.verdict()`): the only per-verse signals kept are a
**localized broken syllable** (non-empty `problem_padas`) or a **total scan
failure** (skrutable's empty / `na kiṃcid adhyavasitam` label — see
`_skrutable_scanned()`). A verse skrutable scanned to any recognized meter/variety
with no localized defect is `clean`, regardless of `is_perfect` and regardless of
a bare chanda/vidyut name disagreement. The 3-way vote still decides `suspect` vs
`review` *within* the localized-defect / scan-failure branch (contradicted or
uncorroborated → suspect; a localized defect the tools still fit → review). This
converges the non-clean set to skrutable's ~14.2% genuinely-localized cases plus
~1.7% total scan failures.

Hand-checked (per the H277 brief) against a sample of the ~964 reclassified
syllable-count-anomaly verses (`ūnākṣarā` deficient / `adhikākṣarā` excess): these
are **not** dropped/added-akṣara typos but corpus artifacts — overwhelmingly
prose intrusions the walker bundled into a verse block (speaker tags
`vallāla uvāca:` / `rājovāca:`, chapter headings `caturtho 'dhyāyaḥ`), which
inflate skrutable's syllable count. Correctly left `clean`; a future
`gretil_walker.py` improvement could strip `... uvāca:` prefixes (see Format
notes).

Two downstream precision changes rode along:
- **DCS-rarity gate** (`meter_check.py`, `RARE_BAND=2`): only *rare* headwords
  (DCS band ≤ 2) are emitted — a common word (deva, rāja, gam…) beside a metrical
  anomaly is coincidence, not signal (31,917 common-word bridge hits dropped).
- **Corroboration-nudge-only in `run_all.py`**: `meter_check` no longer joins
  `c.detectors`, so it can never lift `ndet` to 2 and promote an ordinary word to
  tier A by coincidence (23 such promotions removed; the same failure the
  `CORROB_*` block rejects). It only ranks up a candidate an independent spelling
  detector already found (`meter=suspect|review` tag).

## H277-b follow-ups (07-07-2026)

Four user-requested follow-ons to the recalibration, all landed in one corpus rebuild:

1. **Walker prose-intrusion strip** (`gretil_walker._strip_prose_prefix`) — removes the
   leading speaker tags / section headings that were inflating skrutable's syllable
   count (see Format notes). **39** verses had a prefix removed (mostly `X uvāca:`
   speaker tags); this dropped anuṣṭubh's spurious `adhikākṣarā` pāda-pairs from 592 to
   558. (The overall non-clean rate is unchanged — the recalibration already scores an
   `adhikākṣarā` verse `clean` — but the stored meter labels and the variety census are
   now more faithful.)
2. **Pāda-segmented text stored** in every jsonl record (`skrutable.padas` /
   `skrutable.pada_weights`) — see the Pipeline note. Enables per-pāda bridge
   localization later without re-scanning.
3. **Variety census** ([`variety_stats.py`](variety_stats.py) →
   [`METER_VARIETY_STATS.md`](METER_VARIETY_STATS.md)) — the *amount and frequency of
   the vipulā / meter varieties*, logged as **valid poetic variation, not a suspect
   list**: base-meter distribution (anuṣṭubh ~49%, upajāti triṣṭubh ~12%, …) and the
   anuṣṭubh per-pāda breakdown (pathyā ~78%, then na-/ma-/bha-/ra-vipulā and asamīcīnā).
4. **High-precision sibling** `meter_suspects_strong.txt` — the full
   `meter_suspects.txt` (1,703 rare headwords) is intentionally the broad list; the
   sibling is the tight "check these first" shortlist (suspect verdict + DCS band ≤ 1) —
   **700** rows. (The truly actionable set is smaller still: the **46** headwords the
   meter signal *corroborates* an independent spelling detector on, carried as a
   `meter=` tag in `combined_candidates.txt`.)

Post-rebuild verdict distribution (25,559 unique verse records): **clean 21,505 (84.1%)
· review 1,380 (5.4%) · suspect 2,674 (10.5%)** — non-clean 15.9%, unchanged from the
H277-a reprocess, confirming the recalibration is stable across a clean full rebuild.
A latent `build_meter_index` bug was fixed in passing: it never recorded a just-written
key, so the ~172 legitimately-duplicated loci were emitted twice; it now `done.add`s
each written key (one record per `(source, locus)`).

## Format notes (checked against the 57-file Kavya section, 06-07-2026)

GRETIL's mass-converted plaintext is mostly uniform (header ends at a bare
`# Text` line; verses are blank-line-separated blocks ending in a locus tag
like `KMgD_1` or `// valc_1.1 //`) but **pAda-boundary markup is NOT uniform**
-- some texts mark padas with `/` `//`, others rely entirely on the tools'
own resplit heuristics. `gretil_walker.py` does not assume `/` is present.
Known corpus-noise artifacts NOT specially handled (would need per-text
special-casing, out of scope for a first cut): an occasional invocatory
line (`oṃ namo ...`) bundled into a text's first "verse" block, and prose
commentary/tippani blocks with no locus tag (skipped -- see
`gretil_walker.walk_corpus`'s per-run skip count on stderr, not silently
dropped). **Prose speaker-tags and chapter headings** bundled into a verse
block (`vallāla uvāca:`, fused `rājovāca:`/`sakhyuvāca:`, `caturtho 'dhyāyaḥ`,
`... ucchvāsaḥ`/`... sargaḥ`) were the dominant cause of skrutable's
`adhikākṣarā` (excess-syllable) diagnostic -- surfaced by the H277 hand-check.
`gretil_walker._strip_prose_prefix` (H277-b, 07-07-2026) now strips such a
LEADING prefix (looped, so a heading+speaker stack both go; anchored at the
start only, so a real verse word merely ending in `uvāca` or a long compound is
never touched — see `PROSE_PREFIX_RE`). The per-run stderr line reports how many
verses had a prefix stripped. This required the corpus rebuild that also stores
skrutable's pāda-segmented text (below).

## Verdict scheme (3-way vote, recalibrated H277)

See `meter_ident.py`'s module docstring and `verdict()` function. The decisive
per-verse signal is skrutable's **localized `problem_padas`** (a named broken
syllable) or a **total scan failure**; a recognized irregular variety with
neither is `clean` (see Recalibration above). skrutable's silent
both-pAdas-wrong case (build task 5 in H251) is still caught: `meter_label =
"na kiṃcid adhyavasitam"` (and an empty label) are the scan-failure sentinels
(`_skrutable_scanned()` returns False), so the verse falls through to the
chanda/vidyut cross-check, converging to `suspect` unless a tool actually
corroborates a meter -- never silently dropped, unlike the raw `chanda`-only
pilot's blind spot. What changed in H277: `is_perfect=False` **alone** (empty
`problem_padas`, a recognized variety) no longer routes to suspect/review, and a
bare chanda name-mismatch no longer downgrades a verse skrutable scanned clean.

## Word -> headword bridge

See `headword_bridge.py`'s module docstring: `vidyut.cheda.Chedaka` (the
segmenter, already vendored at
`../../../WhitneyRoots/scratch/vidyut_data/`) gives a real per-token
morphological lemma from context, normalized via `slp1util.normalize_lemma`
and checked against the live `sanhw1.txt` headword set. Words the segmenter
can't resolve (long unbroken compounds are its weak spot) are a **recall**
gap, not a false-positive risk -- they are silently skipped per verse, which
is the right failure mode for a ranking-nudge evidence source.

## Guards (see H251 + root `CLAUDE.md`'s tier-promotion caution)

- `meter_check` is **not** in `run_all.py`'s `HIGH_PRECISION` set -- alone it
  stays tier C; it only helps promote a candidate to tier A in agreement with
  another detector, the same cross-agreement mechanism the other 6 detectors
  already use. No aggregation logic in `run_all.py` was changed to add this.
- vidyut-chandas is a third **vote on meter identity only** -- it has no
  documented error-localization, so `None`/no-match from it is not itself
  suspect evidence (see `verdict()`: `vid_agrees` treats an empty vidyut
  result as agreeing, never as contradicting).
- Licensing (skrutable custom share-alike, `chanda` "Other", GRETIL CC
  BY-NC-SA) is not a build-time blocker per locked decision 4 -- revisit only
  if a derived corruption-flag dataset is proposed for publication.

_Dr. Mārcis Gasūns_
