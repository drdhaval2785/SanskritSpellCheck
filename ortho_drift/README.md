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
| **reform-drift** | **8,683 occurrences · 697 distinct forms** |
| &nbsp;&nbsp;discovered by transform-and-check, beyond the curated seed | **672 forms** (first run) |
| residual candidates (→ LLM pass) | 2,171 distinct |

The **transform-and-check** is high-precision — each old form is *absent* from the 2026 dic and a
reform transform lands *in* it (so `Theater`/`Gottheit` are rejected; `Thier`/`gerathen` kept). On
the first run it discovered **672 forms** beyond the curated seed; **once those are folded into the
accumulating reform map, later runs attribute all 8,683 occurrences to the map** — the 8,683 total
and the 697-form set are stable, only the dic-vs-map label migrates by design (so the committed
[PW_drift_report.txt](PW_drift_report.txt) now shows `dic 0 / map 8,683`). Top forms:
`gerathen→geraten` (253), `personificirt→personifiziert` (191), `theilhaftig→teilhaftig` (190),
`theilen→teilen` (164), `ceremonie→zeremonie` (138), `thätigkeit→tätigkeit` (102),
`mittheilen→mitteilen` (95), `reichthum→reichtum` (81), `casus→kasus` (76).

**PW's German is pervasively pre-1901, confirmed at scale** — 697 distinct drift forms across the
dictionary, dominated by 1901 `th→t` and `c→k/z`. They are persisted to
**[de_reform_map.tsv](de_reform_map.tsv)** — a German reform lexicon that, after the whole cluster,
holds **978 forms** (2,809 after the residual classify below, **2,823** after merging documented
reform pairs) and accumulates across runs; it is the expandable container for DTA/RIDGES pairs.

## German cluster — drift across dictionaries, and the SCH-1928 control

All five German dictionaries run (`ortho_drift.py <DICT> --full`); per-dict drift-by-era in
[de_drift_summary.tsv](de_drift_summary.tsv):

| dict (era) | tokens | modern % | drift/1k | 1901 `th` | 1901 `c` | 1996 `ß` |
|---|--:|--:|--:|--:|--:|--:|
| PW (1855–75) | 845,888 | 59 | **10.26** | 6203 | 1752 | 15 |
| PWG (1855–75) | 1,070,124 | 60 | 8.86 | 6508 | 2275 | 12 |
| GRA (1873) | 254,745 | 45 | 7.90 | 1460 | 507 | 0 |
| CCS (1887) | 117,976 | 65 | 4.72 | 341 | 126 | 84 |
| **SCH (1928)** | 192,039 | 42 | **2.52** | **76** | **86** | **319** |

**The control works.** The four pre-1901 dictionaries are dominated by the 1901 `th→t` reform
(6203 / 6508 / 1460 / 341) with almost no 1996 `ß` drift — the signature of pre-1901 orthography.
**SCH (Schmidt's 1928 *Nachträge*) flips the profile**: 1901-`th` collapses to 76 (Schmidt
already wrote *Tier*, *Kapitel*), while the 1996 `ß→ss` reform becomes *dominant* at 319 (he
still wrote *Kuß*, *Bewußtsein*, *Mißgunst*, *naß* — all pre-1996). So the method doesn't merely
find drift; it **correctly dates each dictionary's orthographic epoch from its own text**. The
overall drift rate also declines monotonically with publication date (10.26 → 8.86 → 7.90 → 4.72
→ 2.52 per 1k) — the corpus modernising across ~70 years.

## Residual classification (recall harvest)

The transform-and-check + curated map leave a residual per dict (forms the rule couldn't auto-
resolve: inflected/compound drift, foreign words, names, OCR fragments). Deduped across the five
dicts, that residual is **6,804 unique tokens**, each classified vs 2026 Duden by 39 Sonnet agents
([de_residual_classified.tsv](de_residual_classified.tsv)):

| category | count | share |
|---|--:|--:|
| fragment / OCR (`rtha`, `tha`, transliteration bits) | 2,981 | 44% |
| **reform-drift** (inflected/compound forms the rule missed) | **1,831** | 27% |
| Latin / foreign (botanical, abbrev) | 1,105 | 16% |
| modern (incl. `t+h` boundaries) | 759 | 11% |
| proper-noun | 106 | 2% |
| uncertain | 22 | <1% |

The **1,831 confirmed reform-drift** (e.g. `thierkreise→Tierkreise`, `abtheilung→Abteilung`,
`commentars→Kommentars`, `eigenthümlichkeiten→Eigentümlichkeiten`) were folded into
[de_reform_map.tsv](de_reform_map.tsv), growing it **978 → 2,809 forms** — a recall gain banked
for future runs. (`modern_form` is advisory — a few LLM artifacts, e.g. one `Gestikulaion` typo.)
The per-dict drift reports above are left as the deterministic-pass snapshot, so the SCH-control
comparison stays stable; re-running any dict now would reclassify its share of these 1,831 from
*residual* into *drift*.

## Cross-language — English, French, Latin, Russian

The same profile-driven tool applied to the corpus's other gloss languages (per-language
`<lang>_reform_map.tsv` + `<lang>_drift_summary.tsv`). All **five** gloss languages, 1832–2009:

| dictionary (era) | gloss lang | tokens | drift/1k | reform regime |
|---|---|--:|--:|---|
| **Kossovich** (pre-1918) | Russian | 87,636 | **358** | 1918 — radical (ѣ/і/ѳ/ѵ + word-final ъ abolished) |
| PW (1855–75) | German | 845,888 | 10.26 | 1901 + 1996 — moderate, legislated |
| **WIL · Wilson** (1832) | English | 432,117 | **0.57** | convention — most archaic of 10 (`-ick`, æ) |
| BUR · Burnouf (1866) | French | 229,053 | 0.31 | convention — minor |
| MW · Monier-Williams (1899) | English | 993,495 | 0.01 | convention — heavily standardised (min of 10) |
| BOP · Bopp (1847) | Latin | 76,933 | **0.00** | none — stable |

**Drift magnitude is a function of reform *type*** — across five languages it falls into three
tiers: **legislated** reform (Russian 358, German 10) ≫ **convention** drift (English ≤0.57,
French ≤0.31) ≫ **none** (Latin 0). Legislated reforms outdrift convention by 1–3 orders of magnitude.

- **Russian (Kossovich)** — the dramatic case: **31,389 drift occurrences (358/1k ≈ 36% of all
  Russian tokens)**, detected **wordlist-free** because the 1918-abolished letters (ѣ/і/ѳ/ѵ) and
  word-final ъ are pre-1918 by definition: `въ→в`, `родъ→род` (hard-sign — the high-frequency bulk),
  `растеніе→растение` (decimal і), `имѣющій→имеющий` (yat). The most sweeping reform in the corpus.
  Source: SamudraManthanam `kossovich.jsonl` (not csl-orig).
- **English (10 dicts, en_GB reference)** — convention-drift, **editor/age-dependent, not a single
  reform date**. Wilson (1832, oldest) tops at 0.57/1k with classic Johnsonian forms (`garlick→garlic`,
  `musick`, `æther→ether`, `chamæleon→chameleon`); the heavily-standardised MW (1899) ≈ 0.01 and
  AP/CAE = 0. Range across 10: 0.00–0.57/1k. (Reference = **en_GB**, so British `honour`/`-ise`/`-re`
  are correctly *not* flagged.)
- **French (Burnouf 1866, Stchoupak 1932)** — minimal: 0.31 / 0.02 /1k (`poëte→poète`,
  `phlegme→flegme`, `françois→français`). ⚠️ BUR/STC inline their Sanskrit in IAST (not `{#…#}`), so a
  few IAST fragments (`pha`) leak — the macro-rate is robust, individual forms less so.
- **Latin (Bopp 1847)** — the **negative control: 0 drift.** Latin had no orthographic reform, so
  there is no rule-set and the tool (correctly) flags nothing — confirming the method's specificity.

Hunspell `de_DE`/`fr_FR`/`en_GB` are wired as membership filters; Latin has no word-list (none exists)
and Russian needs none (the 1918 letters are definitional). Documentation only.

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
   a local dependency) as the deterministic filter + transform-and-check drift detector → 697
   distinct drift forms on full PW (672 discovered beyond the curated seed). The residual LLM
   target is 2,171 candidates.
3. ✅ **Reform map externalized + expanded** → [de_reform_map.tsv](de_reform_map.tsv): **715
   forms** (366 `1901-th`, 224 `1901-c`, 84 `-iren`, 21 `c-iren`, 12 `1996-ss`, 5 `ey`), seeded
   from the curated pairs + the full-PW transform/dic-confirmed drift. `ortho_drift.py` loads it
   at startup and folds each run's discoveries back in, so it accumulates across dictionaries and
   works even without the Hunspell dic. **External pairs (DTA/RIDGES / web-harvested) merge via a
   dic-validated tool** — `detectors/merge_reform_pairs.py <lang> <pairs.tsv>` accepts a pair only
   if `old∉dic & new∈dic` (filtering hallucinations / dual-spellings / rejected proposals). First
   real input: **14 documented 1901/1996 reform pairs** harvested from the German Wikipedia reform
   articles ([de_reform_web_candidates.tsv](de_reform_web_candidates.tsv)) → **de map 2,809 → 2,823**
   (`cigarre→zigarre`, `guitarre→gitarre`, `liqueur→likör`, `schloß→schloss`, `rauh→rau`…). WebFetch
   reaches the web but can't bulk-download the DTA/RIDGES corpora through its summariser — drop a
   local DTA/RIDGES export or give a row-list URL to merge the long tail.
4. ✅ **German cluster done + SCH-1928 control validated** (see the comparison above). SCH's
   profile flips to 1996-`ß`-dominant (319) with 1901-`th` collapsed (76) — confirming the method
   dates orthography from the text. Reform map: 978 → 2,809 (residual classify) → 2,823 (external merge).
