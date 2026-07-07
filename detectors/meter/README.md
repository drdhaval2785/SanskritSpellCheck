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
headword_bridge.py     -- word -> dictionary-headword bridge (vidyut.cheda lemmatizer)
../meter_check.py      -- reads meter_verdicts.jsonl + live sanhw1.txt -> meter_suspects.txt
```

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

## Actual results (full corpus, 07-07-2026)

25,824 verse-shaped blocks parsed (9,005 blocks skipped for having no locus
tag -- prose/commentary interleaving; 184 blocks skipped as prose by the
`MAX_VERSE_CHARS` filter below), 25,705 scored:

| Verdict | Count | Share |
|---|---|---|
| clean | 15,772 | 61.4% |
| review | 6,357 | 24.7% |
| suspect | 3,695 | 14.4% |

`meter_check.py` bridges 10,052 non-clean verses to 7,925 distinct
headwords (`detectors/meter_suspects.txt`). The combined review+suspect
rate (39.1%) is much higher than the single-text pilot's 1.8% -- expected,
since the pilot used one clean mandākrāntā edition and this corpus spans 57
texts of far more variable meter families and markup quality (per the
locked decision 2's own warning) -- but **a human should decide** whether
the `review` threshold (chanda fuzzy cost≤2/similarity≥0.9) needs
recalibrating against a larger hand-checked sample before this signal is
trusted for anything beyond its current ranking-nudge role in `run_all.py`.

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
dropped).

## Verdict scheme (3-way vote, extends the pilot's 2-tool scheme)

See `meter_ident.py`'s module docstring and `verdict()` function. skrutable's
silent both-pAdas-wrong case (build task 5 in H251) is handled locally, not
patched upstream: when skrutable returns no diagnostic (`meter_label = "na
kiṃcid adhyavasitam"`), `is_perfect` is treated as unknown/false and the
verse falls through to the chanda/vidyut cross-check, converging to
`suspect` unless another tool actually corroborates a meter -- i.e. it is
never silently dropped, unlike the raw `chanda`-only pilot's blind spot.

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
