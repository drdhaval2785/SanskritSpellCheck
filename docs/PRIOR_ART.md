# Prior art — Sanskrit spellchecking tools and correction surfaces

_Created: 10-07-2026 · Last updated: 10-07-2026_

Survey run 10-07-2026 for [H452](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H452-Fable_SanskritSpellCheck_prior-art-scan_10.07.26.md)
(roadmap Q3 item 1, ruling D1 in [ROADMAP_2026_2027.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ROADMAP_2026_2027.md)):
three parallel web-research agents (general-purpose, Fable 5 `claude-fable-5` session) + main-session
verification, Fable 5 (`claude-fable-5`) synthesis. Every claim below traces to a fetched page or a
committed file; claims that could not be verified are marked **[inferred]** or listed as
non-findings. Sibling survey for the meter/alliteration track:
[docs/CHANDAS_ANUPRASA_PRIOR_ART.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/CHANDAS_ANUPRASA_PRIOR_ART.md).

## 0. Scope, and what "we" are

Prior art here means anything that flags or corrects Sanskrit spelling: interactive
flag-and-suggest spellcheckers, Hunspell/aspell dictionary packs, morphological analyzers whose
failure is a de-facto validity flag, ML post-OCR correctors, and valid-form data assets usable as
wordlists. For contrast throughout: **this repo** is a *dictionary-QA* machine, not a user-facing
spellchecker — ten detector families (pattern, confusion-pair, n-gram, consensus, intra-duplicate,
dict-vs-corpus, phonotactic, charset, collation-order, meter) over the **33 Cologne CDSL headword
lists** in SLP1, cross-dictionary evidence + DCS corpus adjudication + body-grounded LLM triage,
with the *do-not-file catalogue* (variant ≠ typo) as a first-class deliverable
(see [README.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/README.md),
[detectors/readme.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/readme.md),
[papers/A44_body_grounded_triage_paper.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A44_body_grounded_triage_paper.md)).

**The one-line landscape verdict:** no maintained, published, flag-and-suggest Sanskrit
spellchecker exists. The field splits into (a) one dormant demo with an unpublished source, (b)
Hunspell wordlist packs of wildly varying size and unsettled licensing, (c) analyzer platforms
whose "unrecognized word" behaviour is an accidental spellcheck, and (d) a research line on
post-OCR seq2seq correction. Suggestion generation against a validated Sanskrit lexicon — what the
Q1-2027 web app intends — is essentially unoccupied territory.

## 1. sanskrit-spellchecker.netlify.app — the only true flag-and-suggest tool

Named explicitly by M.G. in the 02-07-2026 interview; **identified**: it is the online interface of
**Prasanna Venkatesh T S, "Spellchecker for Sanskrit: The Road Less Taken", ICON 2022, pp. 290–299**
([aclanthology.org/2022.icon-main.35](https://aclanthology.org/2022.icon-main.35/)) — the paper's
footnote 14 links the site verbatim. Author: PhD scholar, Dept. of Sanskrit, Ramakrishna Mission
Vivekananda College, Chennai (GitHub [vipranarayan14](https://github.com/vipranarayan14));
acknowledges Amba Kulkarni's guidance.

- **Approach:** Hunspell dictionary on the **word-and-paradigm model** with affix rules framed from
  Paninian grammar (a few hundred paradigms; base forms carry paradigm flags, e.g. देव → flag
  `1001`); `TRY` characters ordered by corpus-derived Devanagari character frequency
  ([sanskrit-char-frequency](https://github.com/vipranarayan14/sanskrit-char-frequency)); `REP`
  rules for typical errors (रामह → रामः). The web app (CodeMirror editor, red-underline +
  click/Ctrl-Space suggestions) POSTs word batches to a Netlify serverless function running the
  dictionary via [nodehun](https://www.npmjs.com/package/nodehun).
- **Data:** `sa_IN.dic` with **37,058 entries**, hand-built from paradigms (paper p. 3), Devanagari
  only (IAST named as future work).
- **License:** **unknown — the source was never published.** All 117 public repos of the author
  were enumerated: no spellchecker repo; GitHub code search for the function endpoint returns
  nothing. Only the test corpus ([hunspell-sanskrit-corpus-test](https://github.com/vipranarayan14/hunspell-sanskrit-corpus-test),
  2022) is public.
- **Maintenance:** site live 10-07-2026, still self-labeled "in development … only for demo
  purposes"; the announced Firefox/LibreOffice add-ons never appeared. **[inferred]** dormant since
  ~2022.
- **Evaluation (paper Table 4):** 751-word test corpus (3 OCR'd Rāmāyaṇa pages, sandhi/samāsa
  manually split): 100% precision on accepted words, but heavy over-flagging from OOV — the
  paradigm dictionary is far too small for real text.
- **Reuse / avoid / differ:** *Reuse:* the affix-design playbook (paradigm flags, frequency-ordered
  `TRY`, `REP` confusion pairs) is the best published recipe if we ever ship a Hunspell pack; the
  test-corpus repo is reusable evaluation data; **cite it in the web app UI and both papers — M.G.'s
  explicit instruction.** *Avoid:* depending on it (no source, no license, dormant). *Differ:* our
  validity oracle is evidence-based (33-dictionary consensus + DCS corpus + body-grounded triage),
  not generative (paradigm expansion); our suggestion ranking can use measured confusion weights
  ([detectors/confusion_weights.json](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/confusion_weights.json))
  and DCS frequency instead of Hunspell edit distance; we take SLP1/IAST/Devanagari input, not
  Devanagari only.

## 2. Hunspell / aspell dictionary packs

### 2a. LibreOffice bundled `sa_IN` (Shantanu Oak, 2025) — the big new arrival

**Sanskrit ships with LibreOffice since January 2025**: [`sa_IN/`](https://github.com/LibreOffice/dictionaries/tree/master/sa_IN)
in LibreOffice/dictionaries holds `sa_IN.aff` (7.4 KB), `sa_IN.dic` (**15.5 MB, 543,758 entries**),
and a hyphenation dic (commit "Add Sanskrit" 10-01-2025, contributed by Shantanu Oak). This
postdates and supersedes the ICON 2022 paper's claim that no complete Hunspell Sanskrit dictionary
existed.

- **Approach:** flat wordlist + aggressive `BREAK` rules stripping inflectional endings/prefixes —
  no paradigm morphology; `MAXCPDSUGS 0` (no compound suggestions).
- **Data:** the author's LibreOffice extension ["Sanskrit Spellchecker"](https://extensions.libreoffice.org/en/extensions/show/27509)
  states "based on wikipedia and wikisource" — **[inferred]** the bundled dic shares that origin
  (same author, same aff style; not stated in-tree).
- **License: formally unsettled.** A GPL-2 `COPYING` was added 05-05-2025 and **reverted**
  08-05-2025 by a LibreOffice maintainer ("the copying file contradicts the copyright statements of
  the individual files"); no license file sits in `sa_IN/` today. The author's standalone
  extensions are LGPL (v8.0, 15-03-2024) and his Firefox add-on
  ["Sanskrit Dictionary"](https://addons.mozilla.org/en-US/firefox/addon/sanskrit-dictionary/) is
  GPL-3 (v4.0.0, 31-07-2023).
- **Maintenance:** in-tree, so distribution is alive; the dictionary content's update cadence is
  the author's.
- **Reuse / avoid / differ:** *Reuse:* as a **baseline to evaluate against** (a 543k wordlist with
  `BREAK`-stripping is exactly the "big flat list" design our evidence-based approach claims to
  beat — measure it on the A44 gold sample); the aff `BREAK` inventory is a useful list of
  strippable endings. *Avoid:* **ingesting the wordlist into our data until its license is
  settled** — the in-tree status is contradictory, and wikipedia/wikisource derivation adds CC-BY-SA
  share-alike questions. *Differ:* wordlist provenance — ours is 33 curated dictionaries with
  per-headword provenance, theirs is scraped web text; a scraped list validates misspellings that
  are merely *frequent*.

### 2b. Shreeshrii/hindi-hunspell Sanskrit (ShreeDevi Kumar, 2017)

[`Sanskrit/`](https://github.com/Shreeshrii/hindi-hunspell/tree/master/Sanskrit) holds `sa_IN.aff`
(20.5 KB, machine-generated by Hunspell's `affixcompress`, header "generated by ShreeDevi Kumar,
Released under GPL", `LANG hi_IN`) + `sa_IN.dic` — **3,228 entries**, mostly verb forms; root also
ships `dict-sa-Deva.zip`, `dict-sa-Latn.zip` (an unexamined Latin-script variant), and
`sa_spellchecker_OOo3.oxt`. License **GPLv3** (per `LICENSES-en.txt`); Sanskrit dir last touched
**22-03-2017**. *Reuse:* nothing directly (tiny, stale); the `-Latn` pack is the only sighted
attempt at non-Devanagari Hunspell input, worth one look before we design IAST support. *Avoid:*
GPL wordlist ingestion. *Differ:* scale and provenance.

### 2c. Firefox "Sanskrit Spell Checker" (Quintanilha & Della Líbera, 2018)

[addons.mozilla.org/en-US/firefox/addon/sanskrit-spell-checker](https://addons.mozilla.org/en-US/firefox/addon/sanskrit-spell-checker/)
— Hunspell add-on with only **838 Devanagari words** (the ICON 2022 paper's comparative eval),
GPL-2, v2.0.2 (25-04-2024 re-signing), 52 users. Flags + suggests via Firefox's native spellcheck.
*Verdict:* historical footnote; demonstrates the distribution channel, not the lexicon.

### 2d. Gasuns 2013 — the in-house ancestor

[samskrtam.ru/sanskrit-hunspell](https://samskrtam.ru/sanskrit-hunspell/) — M.G.'s own early
Hunspell dictionary, cited by the ICON 2022 paper as incomplete/unmaintained. Prior art to
acknowledge in the papers' related work: the project's own lineage with Hunspell predates this
repo.

### 2e. Non-findings (verified absences)

- **No `sa` in [wooorm/dictionaries](https://github.com/wooorm/dictionaries)** (all language dirs
  enumerated; Latin exists, Sanskrit does not) — i.e. no npm-ecosystem Sanskrit spellcheck pack.
- **No GNU aspell Sanskrit** ([ftp.gnu.org/gnu/aspell/dict/0index.html](https://ftp.gnu.org/gnu/aspell/dict/0index.html)
  fetched: Hindi present, Sanskrit absent).
- **The sanscript / indic-transliteration ecosystem has no spellcheck component**:
  [sanscript.js](https://github.com/indic-transliteration/sanscript.js) (and siblings) is
  transliteration-only — script conversion between Brahmic and Roman schemes, MIT, no error
  detection or normalization features documented. Relevant to the web app only as the
  input-conversion layer (Devanagari/IAST → SLP1), not as prior art for checking.
- **[sanskrit-coders](https://github.com/sanskrit-coders) spellcheck page 404s** (link rot).
- **[sanskrit-lexicon/COLOGNE issue #91](https://github.com/sanskrit-lexicon/COLOGNE/issues/91)
  "Hunspell for Sanskrit?" — open since 2016**, 31 comments, never resolved: the Cologne ecosystem
  itself has wanted this for a decade. Our planned Cologne integration is the direct answer.

## 3. Analyzer platforms — validity flags without suggestions

### 3a. Sanskrit Heritage Platform (Gérard Huet, INRIA)

The Reader displays an unrecognized input chunk as a **grey rectangle with undefined morphology**
(per the [manual](https://sanskrit.uohyd.ac.in/SKT/manual.html), UoH mirror; INRIA hosts block
fetchers) — the strongest de-facto spellcheck surface among the platforms, but explicitly **no
correction/suggestion feature** (manual: garbage in, garbage out). "Sanskrit made easy" search
tolerates missing diacritics (fuzzy lookup, not correction). Morphology is generated **always from
the Heritage Sanskrit–French dictionary**, not MW. License: lexicon + morphological databanks under
**LGPLLR**, Zen toolkit LGPL. Actively maintained (v3.77, 15-03-2026); local install possible
(three INRIA GitLab repos), UoH runs a public mirror. *Reuse:* the LGPLLR inflected-forms databank
is a legally clean candidate validity oracle / wordlist to **cross-validate** our detector output
against (LGPLLR permits use with attribution; keep it a sidecar, not a merged ingest). *Differ:*
Heritage answers "is this form derivable from *its* lexicon"; we answer "which of 33 dictionaries
attests this headword, and does the corpus agree".

### 3b. Samsaadhanii / SCL (Amba Kulkarni, Univ. of Hyderabad)

[sanskrit.uohyd.ac.in/scl](https://sanskrit.uohyd.ac.in/scl/) ·
[github.com/samsaadhanii/scl](https://github.com/samsaadhanii/scl) — morphological
analyser/generator, sandhi splitter/joiner, segmenter, compound tools, Aṣṭādhyāyī simulator,
annotated e-readers (the "Reading Aid" family, which consumes Cologne exports). **No documented
spell-check, invalid-word flagging, or suggestion surface** anywhere on the site, README, or FAQ;
analyser failure on unrecognized words is undocumented (**[inferred]**: silent no-analysis). The
lab *did* run a web spellchecker built on the analyser — **defunct** per the ICON 2022 paper
(fn. 2, "no longer maintained", Kulkarni personal communication). Lexicon: Amarakosha Knowledge-Net
+ Dhātupāṭha concordance (MW not named). License **GPL-2.0**; active (pushed 24-04-2026); site
advertises APIs for all tools; Docker exists. *Reuse:* **call or cross-validate, never vendor** —
the GPL boundary is a standing guard, and a combined license question is already in the pending
Kulkarni outreach ([H057 draft](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H057-Opus_Uprava_OUTREACH_2026-07-02_amba_kulkarni_scl_02.07.26.md)).
Its analyser-as-oracle is the natural *second opinion* on any form our consensus detector calls
wrong. *Differ:* generative analysis vs attested-evidence QA, as with Heritage.

### 3c. SanskritShala (IIT Kharagpur, ACL 2023 demo)

[cnerg.iitkgp.ac.in/sanskritshala](https://cnerg.iitkgp.ac.in/sanskritshala) ·
[arXiv 2302.09527](https://arxiv.org/abs/2302.09527) — segmentation / morph tagging / parsing /
compound ID with an annotation UI where **humans correct the model**, not the reverse. No
spellcheck. *Verdict:* adjacent platform, not prior art for correction.

## 4. The ML correction line — post-OCR, not spellcheck

- **ByT5-Sanskrit / DharmaMitra** (Nehrdich, Hellwig, Keutzer; EMNLP Findings 2024,
  [arXiv 2409.13920](https://arxiv.org/abs/2409.13920); models on HuggingFace, PyPI client
  [dharmamitra-sanskrit-grammar](https://pypi.org/project/dharmamitra-sanskrit-grammar/)) — one
  multitask byte-level model for segmentation, lemmatization, tagging, and **OCR post-correction**
  (SOTA claim), trained on DCS. The only ML *correction* model in the field — but its domain is
  scan noise in running text, seq2seq, no interactive surface. Code org self-describes permissive
  licensing, yet the [byt5-sanskrit-analyzers](https://github.com/dharmamitra/byt5-sanskrit-analyzers)
  repo has **no license file** (GitHub API `license: null`) — exact model licenses unverified.
  *Reuse:* candidate re-ranker/second annotator for running-text detectors (ngram, meter) — via the
  API or HF models once licensing is confirmed; **avoid** treating it as a headword-QA tool: A44's
  proof-reader-effect concern (models "fix" toward expectation) is exactly the failure mode
  body-grounded triage exists to prevent. *Differ:* they correct the text toward a language model;
  we adjudicate the lexicon against its own body evidence.
- **pe-ocr-sanskrit** (Maheshwari et al., EMNLP 2022,
  [github.com/ayushbits/pe-ocr-sanskrit](https://github.com/ayushbits/pe-ocr-sanskrit)) — post-OCR
  benchmark, ~218k sentences / 1.5M words from 30 books; no license file; last push 2023-10.
  *Reuse:* the benchmark framing (and data, license permitting) if the OCR-triage phase-2 work
  resumes.
- **majumderb/sanskrit-ocr** (CoNLL 2018, [github.com/majumderb/sanskrit-ocr](https://github.com/majumderb/sanskrit-ocr))
  — post-OCR correction of **romanised (IAST)** Sanskrit; the only sighted IAST-input correction
  work; no license; dormant since 2019.
- **OpenOCRCorrect** (IIT-B, [github.com/rohitsaluja22/OpenOCRCorrect](https://github.com/rohitsaluja22/OpenOCRCorrect))
  — interactive OCR-error correction UI for Indian languages incl. Sanskrit, C++, **BSD-3-Clause**,
  last push 2024-07. *Reuse:* the only permissively-licensed interactive correction UI found;
  worth a look before building the web app's review surface from scratch.
- **saarthak5/bigram-spellchecker** — student-scale contextual (bigram LM + edit likelihood)
  Devanagari spellchecker, Python, no license, pushed 2025-04. Noted for completeness.

## 5. Valid-form data assets (wordlist candidates)

| Asset | Size / nature | License | Verdict |
|---|---|---|---|
| **Vidyut** ([ambuda-org/vidyut](https://github.com/ambuda-org/vidyut), Prasad 2024 ISCLS, [2024.iscls-1.7](https://aclanthology.org/2024.iscls-1.7/)) | `vidyut-kosha` compact FST lexicon; `vidyut-prakriya` generates forms **with sūtra provenance**; `vidyut-cheda` segmenter; `vidyut-chandas` meter | **MIT** | **Already consumed here**: kosha pratipadika stems vendored as a validity oracle via [detectors/gen_vidyut_stems.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/gen_vidyut_stems.py); `vidyut.cheda` is the meter pipeline's word→headword bridge; vidyut-chandas is the third meter vote ([detectors/meter/README.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/meter/README.md)). **Not a spellchecker** — no flag/suggest API; it is the best-licensed generative oracle, complementary to our attested-evidence approach. |
| **ashtadhyayi.com data** ([ashtadhyayi-com/data](https://github.com/ashtadhyayi-com/data)) | precomputed dhātu forms, śabda forms, kośa data; very active (last push 03-07-2026) | **no license file** (open-intent inferred) | Valid-form tables usable as a cross-check *after* a license ask; raw GitHub JSON is the de-facto API. No flag-and-suggest surface. |
| **Heritage inflected-forms databanks** (INRIA) | full morphology XML from the Heritage lexicon | **LGPLLR** | Legally cleanest external wordlist; cross-validate, don't merge (see §3a). |
| **LibreOffice sa_IN.dic** | 543,758 scraped-text entries | unsettled | Baseline only until licensing clears (§2a). |

## 6. Summary table

| Tool | Approach | Data | License | Maintained? | Flag/suggest? |
|---|---|---|---|---|---|
| [netlify spellchecker](https://sanskrit-spellchecker.netlify.app/) (Prasanna, ICON 2022) | Hunspell, Paninian word-and-paradigm | 37,058 entries, hand-built | source unpublished | dormant ~2022, site live | **both** |
| [LibreOffice sa_IN](https://github.com/LibreOffice/dictionaries/tree/master/sa_IN) (Oak) | Hunspell, flat list + BREAK | 543,758, web-scraped | **unsettled** | in-tree since 01-2025 | both (via LO) |
| [Shreeshrii Sanskrit](https://github.com/Shreeshrii/hindi-hunspell/tree/master/Sanskrit) | Hunspell, affixcompress | 3,228 | GPL-3 | stale (2017) | both (via host app) |
| [Firefox add-on](https://addons.mozilla.org/en-US/firefox/addon/sanskrit-spell-checker/) (Líbera) | Hunspell | 838 | GPL-2 | re-signed 2024 | both (via FF) |
| [Heritage Platform](https://sanskrit.uohyd.ac.in/SKT/) (Huet) | morphological analysis | Heritage lexicon | LGPLLR/LGPL | active (v3.77, 03-2026) | flag only (grey box) |
| [SCL/Samsaadhanii](https://github.com/samsaadhanii/scl) (Kulkarni) | morphological analysis | Amarakosha KN + Dhātupāṭha | GPL-2.0 | active (04-2026) | none (spellchecker defunct) |
| [ByT5-Sanskrit](https://arxiv.org/abs/2409.13920) (DharmaMitra) | seq2seq multitask | DCS | permissive-intent, unconfirmed | active | none (batch OCR fix) |
| [Vidyut](https://github.com/ambuda-org/vidyut) | generative (prakriya/kosha) | Paninian derivation + DCS | MIT | active | none (oracle only) |
| **this repo** | cross-dict consensus + corpus + body triage | 33 CDSL headword lists, SLP1 | — | active | QA lists, not UI (yet) |

## 7. Implications

### 7a. For the Q1-2027 web app design

1. **The niche is real and open**: the only flag-and-suggest tool is a dormant unlicensed demo;
   the only big wordlist is license-unsettled scraped text. A validated-provenance spellchecker
   with suggestion ranking has no occupant. The decade-open
   [COLOGNE #91](https://github.com/sanskrit-lexicon/COLOGNE/issues/91) is the demand signal.
2. **Cite the netlify tool in the UI** (M.G.'s instruction) — an "about / prior art" note crediting
   Prasanna (ICON 2022), and both papers cite it (§7b/§7c).
3. **Differentiators to build on, all already in-repo:** SLP1/IAST/Devanagari input (nothing
   supports IAST interactively; only a 2019 research repo touches it); suggestion ranking by
   measured confusion weights + DCS frequency (vs Hunspell edit distance); the do-not-file
   suppression layer as a *variant-aware* accept list — no other tool distinguishes variant from
   typo at all.
4. **Licensing guards:** do not ingest the LibreOffice or GPL wordlists; cross-validate against
   Heritage (LGPLLR) and call SCL remotely (GPL); Vidyut (MIT) remains the one safely embeddable
   external oracle. ashtadhyayi.com data needs a license ask before use.
5. **Packaging option surfaced by the scan:** a Hunspell `.aff/.dic` export of our validated
   headword union would ride every platform Hunspell supports (LibreOffice/Firefox distribution
   channel proven by Oak's extensions) — Prasanna's affix design is the recipe to follow; needs a
   CDSL-headword licensing check first.
6. **Reusable UI prior art:** OpenOCRCorrect (BSD-3) for the correction-review surface.

### 7b. For A37's related work (ortho-drift dater)

A37 measures the **gloss metalanguage** of dictionaries; the scanned tools all target the Sanskrit
*object language*. One delimiting citation suffices: Prasanna (ICON 2022) as the state of Sanskrit
object-language spellchecking, contrasted with A37's channel (the gloss). The Hunspell de_DE /
en_GB dictionaries A37 already uses as runtime deps are the same technology family — worth a
sentence noting the tooling continuity. Added to
[papers/A37_ortho_drift_paper.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A37_ortho_drift_paper.md) §2.

### 7c. For A44's related work (body-grounded triage)

1. **Citation correction (found by this scan):** A44 §2 credited "the contextual spell-checker for
   Sanskrit demonstrated at ISCLS 2024" — the ISCLS 2024 proceedings
   ([2024.iscls-1](https://aclanthology.org/volumes/2024.iscls-1/)) contain **no** spellcheck paper.
   The intended reference is **Prasanna S., ICON 2022** ([2022.icon-main.35](https://aclanthology.org/2022.icon-main.35/)).
   Corrected in the paper.
2. **A sharpened contrast for §4.1:** Prasanna's evaluation reports 100% precision *on words
   accepted* with heavy over-flagging — the mirror image of A44's precision-collapse result on
   string-level detectors over a mature lexicon. Generative dictionaries over-flag; string-level
   detectors over-accept trivial noise; the body-grounded layer is what neither approach has.
3. **The suppression-catalogue framing is confirmed novel:** no scanned tool models
   variant-vs-typo; Hunspell packs hard-code one spelling as correct. The do-not-file catalogue has
   no counterpart in the landscape.

_Dr. Mārcis Gasūns_
