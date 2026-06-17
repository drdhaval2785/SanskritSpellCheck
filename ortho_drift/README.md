# Orthographic-drift pilot — Phase 0 (PW / German)

Pilot for the [orthographic-drift study](../ORTHO_DRIFT_ROADMAP.md): does the body-grounded
method extend from Sanskrit headwords to the **gloss language**? This is the **PW-vs-Duden**
German slice (the cleanest case — German's reforms are legislated and rule-defined).

> **Documentation only.** This never edits `csl-orig`. It is a search-normalization /
> historical-linguistics layer; see the roadmap's guardrail.

## Result — full PW (Hunspell-wired)

`detectors/ortho_drift.py PW --full` against the modern **Hunspell `de_DE` 2006** word-list
(103,756 stems; Adobe InDesign's bundled dic — a **local dependency, not committed**; override
via `$ORTHO_DE_DIC`). Across **all 170,556 PW entries / 845,888 German gloss tokens**:

| | |
|---|--:|
| already-2026-modern (filtered by the dic) | **502,882 (59%)** |
| **reform-drift** | **8,683 occurrences** |
| &nbsp;&nbsp;• dic-confirmed (reform transform → lands in the modern dic) | 6,352 in **672 distinct forms** |
| &nbsp;&nbsp;• curated map (incl. inflected forms) | 2,331 in 25 forms |
| residual candidates (→ LLM pass) | 2,171 distinct |

The **dic-confirmed** list is high-precision — each old form is *absent* from the 2026 dic and a
reform transform lands *in* it (so `Theater`/`Gottheit` are rejected; `Thier`/`gerathen` kept).
Top: `gerathen→geraten` (253), `personificirt→personifiziert` (191), `theilhaftig→teilhaftig`
(190), `theilen→teilen` (164), `ceremonie→zeremonie` (138), `thätigkeit→tätigkeit` (102),
`mittheilen→mitteilen` (95), `reichthum→reichtum` (81), `casus→kasus` (76),
`constellation→konstellation` (67). Full list → [PW_drift_report.txt](PW_drift_report.txt).

**PW's German is pervasively pre-1901, confirmed at scale** — 672 distinct drift forms across
the dictionary, dominated by 1901 `th→t` and `c→k/z`. These (plus the curated seed) are persisted
to **[de_reform_map.tsv](de_reform_map.tsv)** — a 715-form German reform lexicon that accumulates
across runs and is the expandable container for DTA/RIDGES pairs.

## Pilot validation (sampled + LLM) — how the method was proven first

`detectors/ortho_drift.py PW` on **every 68th PW entry (2,509 of 170,556)**, 12,917 German
gloss tokens scanned:

| signal | result |
|---|--:|
| **CONFIRMED reform-drift** (curated map, high precision) | **48 occurrences · 13 distinct forms** |
| pattern candidates (need a 2026 wordlist / the LLM to confirm) | 163 distinct tokens |

The 13 confirmed forms — genuine pre-1901/1996 German, each mapped to its 2026 spelling and
found in real PW glosses ([PW_drift_report.txt](PW_drift_report.txt)):

`Thier→Tier` (10) · `Theil→Teil` (6) · `Noth→Not` (5) · `thun→tun` (5) · `Thiere→Tiere` (4) ·
`Werth→Wert` (3) · `Roth→Rot` (3) · `Vocal→Vokal` (3) · `Blüthe→Blüte` (3) · `theils→teils` (2) ·
`gethan→getan` (2) · `Vocale→Vokale` (1) · `Thor→Tor` (1). Eras: 1901 `th→t`, 1901 `c→k`,
archaic `ey→ei`, 1996 `ß→ss`.

### Candidates classified vs 2026 Duden (Sonnet as the Duden oracle)

The 163 pattern-candidates ([PW_drift_classified.txt](PW_drift_classified.txt)):

| category | count | meaning |
|---|--:|---|
| **reform-drift** | **114** | real pre-reform German — 75× `1901 th→t`, 27× `1901 c→k/z`, 12× `1901 -iren→-ieren` (e.g. `gerathen→geraten`, `eigenthümlich→eigentümlich`, `commentar→Kommentar`, `recitiren→rezitieren`) |
| modern | 19 | already 2026-correct — incl. the `t+h` boundaries (`enthaltend`, `Gottheit`) the patterns over-flagged |
| latin-or-foreign | 15 | Latin / botanical / English (`curcuma`, `clitoris`, `lexicon`) — not German |
| fragment-or-ocr | 13 | transliteration fragments / garble (`rtha`, `tha`) |
| proper-noun | 2 | names |

**So in the 2,509-entry sample, 127 distinct reform-drift forms** (13 map + 114 classified) — PW's
German is **pervasively pre-1901**; extrapolated, thousands of drift instances across the full
text. The noise buckets (Latin / proper-noun / fragment / `t+h`-boundary) worked as designed,
confirming the proper-noun strategy. `modern_form` is advisory (documentation, not correction);
two LLM artifacts were hand-corrected (`Kokossnussbaum→Kokosnussbaum`, `Konstant→konstant`).

## What the pilot established

1. **The method works on the gloss language.** Real, era-correct German drift is found and
   normalised to 2026 forms, with the entry as context — exactly as for Sanskrit headwords.
2. **The false-positive sources are now concrete** (empirically answering the roadmap's
   proper-noun question). The recall patterns over-flag, dominated by:
   - **Latin** — botanical species (`curcuma`, `clitoris`, `aphrodisiacum`) and grammatical
     abbreviations (`Caus.`, `Comm.`, `Compar.`);
   - **`t+h` morpheme boundaries** that are *not* etymological `th` (`enthaltend` = ent+haltend,
     `Gottheit` = Gott+heit) — modern German, not drift;
   - **transliteration fragments** (`rtha`, `tha`) and **proper nouns**.
   → so the production filter needs the 2026 Duden/Hunspell wordlist + the LLM classify bucket
   (decisions: proper-noun strategy = **LLM-label + sigla stop-list**; capitalisation is useless
   for German). The patterns also catch much *real* drift (`gerathen`, `theilen`, `rothe`,
   `wasserthier`, `getheilt`, `verrathen`, `recitiren`, `multiplicirt`) — recall is good; the
   wordlist/LLM supplies precision.
3. **A tokenizer-hardening requirement, discovered live.** PW glosses embed editorial-correction
   records `{%<bot>{{old->new||date|editor|github-url|}}</bot>%}`, leaking `github`, editor names
   (`Thomas` Malten) and botanical Latin into the token stream. The tokenizer now strips
   `{{…}}` annotations, `<bot>…</bot>` Latin spans, `<ls>` sigla, and filters abbreviations
   case-insensitively. (This also flags that the same annotations sit in the data the headword
   triage reads — useful cross-finding.)

## Decisions recorded

- **2026 standard = Duden** (operationally the Hunspell `de_DE` Frami word-list, which tracks
  Duden) — to be wired as the candidate filter.
- **Sampled** for testing (default ~2,500 entries by stride; `--full` for all).
- **Proper-noun strategy** = LLM classify-bucket + sigla/abbrev stop-list (a)+(b).
- **Documentary only**, never a correction list now; the *OCR-error* subset *only* could later
  graduate behind a human sign-off gate (reform-drift never).

## Run it

```sh
cd detectors
python ortho_drift.py PW            # sampled (~2,500 entries)
python ortho_drift.py PW --full     # every entry
#   -> ortho_drift/PW_drift_report.txt + PW_pattern_candidates.txt
```

## Next (to finish Phase 0 → Phase 1)

1. ✅ **LLM classify the 163 candidates vs 2026 Duden** — done: **114 reform-drift** confirmed,
   noise correctly bucketed → [PW_drift_classified.txt](PW_drift_classified.txt).
2. ✅ **Wired the Hunspell `de_DE` word-list** (2006/Duden, 103,756 stems — Adobe's bundled dic,
   a local dependency) as the deterministic filter + transform-and-check drift detector → 672
   dic-confirmed drift forms on full PW. The residual LLM target is now 2,171 candidates.
3. ✅ **Reform map externalized + expanded** → [de_reform_map.tsv](de_reform_map.tsv): **715
   forms** (366 `1901-th`, 224 `1901-c`, 84 `-iren`, 21 `c-iren`, 12 `1996-ss`, 5 `ey`), seeded
   from the curated pairs + the full-PW transform/dic-confirmed drift. `ortho_drift.py` loads it
   at startup and folds each run's discoveries back in, so it accumulates across dictionaries and
   works even without the Hunspell dic. **DTA/RIDGES** historical→modern pairs are online and
   this environment has no outbound internet — merge them into this file when reachable (or drop
   the files locally, like the Hunspell dic).
4. **Run the rest of the German cluster** — PWG / GRA / CCS, and **SCH (1928) as the internal
   control** (should show 1996-era drift but little 1901-era, unlike pre-1901 PW).
