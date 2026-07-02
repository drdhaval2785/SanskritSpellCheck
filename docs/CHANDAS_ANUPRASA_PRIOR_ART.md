# Chandas validation + Anuprāsa analysis — prior-art survey

<p align="right"><sub>Created: 02-07-2026 · Last updated: 02-07-2026</sub></p>

Survey run 02-07-2026 (four Sonnet 5 `claude-sonnet-5` research agents; Fable 5
`claude-fable-5` synthesis) to ground the **batch chandas (meter) validator** — a planned
SanskritSpellCheck detector over verse corpora (GRETIL first) — and the reuse assessment of the
UoHyd **Anuprāsa Identifier**. M.G. decisions locked the same day: the meter validator lives
**here as a detector family** (meter breaks = error signal feeding the existing tier/review
pipeline); build on **open tools now, UoHyd student code later** when acquired; anuprāsa serves
**corpus annotation + SanskritKaraoke enrichment + a paper angle**; timing = **tiny pilot now,
full work in Q1 2027** per
[ROADMAP_2026_2027.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ROADMAP_2026_2027.md).

## 1. The Anuprāsa Identifier and Classifier (ISCLS 2024)

**Barbadikar, Amruta & Amba Kulkarni (UoHyd, Dept. of Sanskrit Studies), "Anuprāsa Identifier
and Classifier: A computational tool to analyze Sanskrit figure of sound",** ISCLS 2024
proceedings pp. 102–112, [aclanthology.org/2024.iscls-1.8.pdf](https://aclanthology.org/2024.iscls-1.8.pdf).
Sister paper: Yamaka identifier (Barbadikar & Kulkarni 2023).

- **Method:** deliberately rule-based (śabdālaṅkāra needs minimal semantics). Viśvanātha's
  (*Sāhityadarpaṇa*) 5-way taxonomy — chekānuprāsa, vṛttyanuprāsa, śrutyanuprāsa (5
  place-of-articulation classes), antyānuprāsa (pādānta/padānta rhyme), lāṭānuprāsa (word
  repetition). Core algorithm: n-grams with/without vowels over WX-transliterated surface text,
  subsumption-collapse, then a strict-to-loose cascade (lāṭa → cheka → vṛtti) so each match gets
  only its most stringent type; śruti/antya checked independently. Proximity window
  `8 + 2×length` syllables. No segmenter/meter dependency; anusvāra variants normalized;
  operates on sandhied text.
- **Evaluation:** 70 ślokas + 10 prose passages (Raghuvaṃśa, Kādambarī) — qualitative, no P/R.
- **Code: NOT published.** Web-tool only at [sanskrit.uohyd.ac.in/scl/](https://sanskrit.uohyd.ac.in/scl/)
  ("Yamaka-Anupraasa Identifier"); no repo, no license, single-input interactive. The paper's
  algorithm spec (Table 1 + §5) is complete enough for a **clean-room reimplementation at
  low-moderate cost**; our [sanskrit-util](https://github.com/gasyoun/sanskrit-util) covers the
  transliteration side (WX would need adding — it exports IAST⇄SLP1⇄Devanāgarī today).
- **Reuse plan (per M.G. 02-07-2026):** reimplement as a small SLP1-native library (skip WX;
  SLP1 is losslessly equivalent for this purpose) → (a) batch anuprāsa/type annotation over
  verse corpora (GRETIL/DCS/SamudraManthanam) as a FAIR layer; (b) SanskritKaraoke display
  enrichment (highlight sound-figure spans); (c) a computational-alaṅkāra study (anuprāsa
  density by author/genre/era) — registered as a paper idea in Uprava
  [ARTICLES.md](https://github.com/gasyoun/Uprava/blob/main/ARTICLES.md). Cite Barbadikar &
  Kulkarni; contact them when the UoHyd code channel opens (same channel as the chandas
  student code below).

## 2. Batch chandas validation — tool landscape

Goal: **meter-validate whole verse corpora; a pāda that breaks its identified meter is a
suspect-text signal** feeding the SpellCheck tier pipeline. Two independent survey agents
converged on the same ranking:

| Tool | Author | Code / license | Batch | Error localization | State |
|---|---|---|---|---|---|
| **[skrutable](https://github.com/tylergneill/skrutable)** | Tyler Neill | PyPI `skrutable`; ⚠️ custom share-alike license (not OSI) | **yes — has a "Scan GRETIL" whole-corpus mode already** (~15 verses/s; BG in ~1 s; Rāmāyaṇa demonstrated) | per-pāda diagnostics: `problem_syllables` (0-based positions per pāda), hypermetric/hypometric vs gaṇa-mismatch labels ([diagnostic_label_overview.md](https://github.com/tylergneill/skrutable/blob/main/diagnostic_label_overview.md)) | most active (pushed 06-2026); author presents HANSEL e-text library at ISCLS 2026 |
| **[chanda](https://github.com/hrishikeshrt/chanda)** (Chandojñānam) | Hrishikesh Terdalkar (IIT-K) | PyPI `chanda`; ⚠️ license "Other" — clarify before embedding | yes — CLI `chanda -f file --verse --summary`; 15+ input schemes | **fuzzy Levenshtein with per-syllable edit-op markers** (`i(L)`, `r(भु)[G]{भू}`, `d(...)` at exact syllable positions); 98.2 % correct-meter on OCR-corrupted verses ([arXiv:2209.14924](https://arxiv.org/abs/2209.14924)) | active (pushed 04-2026) |
| [vidyut-chandas](https://github.com/ambuda-org/vidyut/tree/main/vidyut-chandas) | Arun Prasad | Rust + py bindings | yes (library) | none documented; README defers to skrutable/sanskritmetres | experimental |
| [shreevatsa/sanskrit](https://github.com/shreevatsa/sanskrit) | S. Rajagopalan | GPL-2.0 | library-loopable | coarse (hierarchical whole→half→quarter match) | author calls it "broken in major ways"; 96 open issues |
| Melnad/Goyal/Scharf MIT | Sanskrit Library | **no public code** (paper + dead web demo; 98.7 % on 1,031 verses) | — | conservative non-recognition only | dormant (2013) |
| UoHyd / Saṃsādhanī | Amba Kulkarni's group | **no distinct public chandas tool found** on [scl](https://github.com/samsaadhanii/scl) or the portal | — | — | the "student non-batch code" M.G. knows of is presumably unpublished — acquire via direct contact |

**Recommendation (converged, both surveys):** **skrutable primary + `chanda` as
cross-validator.** skrutable is the shortest path (batch mode literally named "Scan GRETIL",
structured per-pāda anomaly output, auto scheme-detection); `chanda`'s per-syllable edit-ops
are the sharper *correction-suggestion* signal — running both and flagging disagreement is the
cheap ensemble. Glue needed: a GRETIL walker (TEI/plain-text pāda extraction — the main cost;
GRETIL markup varies by text family), a flat per-verse anomaly record (file + locus + pāda +
positions), a policy for skrutable's silent `None` cases (both-pādas-wrong is exactly the
highest-value corruption signal and is dropped today — upstream issue/PR candidate), and
license clarification for both tools before any redistribution.

**Pilot (M.G.: now, tiny scope):** one session — `pip install skrutable chanda`, one clean
GRETIL text (e.g. Raghuvaṃśa or Meghadūta, whose GRETIL version Chandojñānam already used),
run both, diff verdicts, hand-check 20 disagreements/anomalies against the edition; decide the
detector's output format. Then park until Q1 2027.

## 3. ISCLS program items worth tracking

From [iscls.github.io/iscls2024/program.html](https://iscls.github.io/iscls2024/program.html)
and [iscls.github.io/program.html](https://iscls.github.io/program.html) (2026):

- **"Contextual Spellchecking for Sanskrit" (demo, Prasanna Venkatesh T S, 2024)** — direct
  overlap with this repo's mission; no paper PDF in the proceedings volume (demo track) —
  track down the tool/author.
- **"Word Sense Alignment of Sanskrit Lexica" (Dhaval K Patel & Amba Kulkarni, 2024,
  [2024.iscls-1.1](https://aclanthology.org/2024.iscls-1.1.pdf))** — Dr. Patel is this repo's
  author; sense alignment across lexica speaks directly to the union-headword/crosswalk assets
  (SHARED_CODE §8/§10) and csl-atlas. Deep-read candidate.
- **"Preserving What Is Written, Not What Is Expected: The Proof-Reader Effect of LLMs in
  Sanskrit OCR" (Jain/Bhatt/Choudhary, 2026)** — names the exact failure mode our body-grounded
  triage guards against (LLMs "correcting" faithful text); relevant to both A44 and the OCR
  pipeline. Read when published.
- **CHANDOMITRA (2026)** — meter-gated verse *generation* (Goyal group); the gating logic is
  adjacent to validation.
- **Varṇacitra detection (Dilip H R, 2024 demo + 2026 paper)** — figure-of-sound family,
  complements anuprāsa for the annotation layer.
- **HANSEL (Tyler Neill, 2026)** — NLP-ready Sanskrit e-text library; potential cleaner corpus
  substrate than raw GRETIL for the meter validator.
- ISCLS 2024 also carries M.G.'s own demo ("Future of Cologne Digital Lexicons").

<p align="right"><sub>Dr. Mārcis Gasūns</sub></p>
