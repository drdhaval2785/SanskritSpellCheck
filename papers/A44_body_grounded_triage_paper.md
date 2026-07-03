---
paper_id: A44
title: "The Dictionary Body as Ground Truth: Body-Grounded LLM Triage and the Precision-Collapse Result"
status: revision executed (referee fixes applied 2026-07-03), pending IRR human gate + author pass
readiness: 3/5
venue: "International Journal of Lexicography (IJL) — per the locked venue split"
author: "**Mārcis Gasūns**, independent scholar ([ORCID 0000-0003-4513-884X](https://orcid.org/0000-0003-4513-884X)), gasyoun@ya.ru"
data_source: "corrections_draft/README.md (33-dict triage complete) + nochange/do_not_file_suppress.txt (2297 deduped) + .claude/commands/dict-triage.md (pipeline)"
---

# The Dictionary Body as Ground Truth: Body-Grounded LLM Triage and the Precision-Collapse Result

> **Draft status (2026-06-26; referee fixes applied 2026-07-03, Fable 5
> `claude-fable-5`, per [A44_review_fable5.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A44_review_fable5.md)).**
> Manuscript built directly on the
> completed 33-dictionary triage indexed in
> [`corrections_draft/README.md`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/README.md). All numerical
> claims below are transcribed from, and recompute against, the committed per-dict
> packages in [`corrections_draft/`](https://github.com/drdhaval2785/SanskritSpellCheck/tree/master/corrections_draft) and the deduped
> suppression file [`nochange/do_not_file_suppress.txt`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/nochange/do_not_file_suppress.txt),
> with the 2026-07-02 source re-verification folded in (§4.5).
> **Open before submission:** (1) obtain an inter-coder
> reliability number (a second annotator — *human gate*, tracked in GTD); (2) finalise
> byline; (3) MG read-through for the IJL register.

## Abstract

On the Monier-Williams Sanskrit–English dictionary, a spelling-anomaly detector's
top tier yields **4 filable corrections out of 1,954 candidates — a precision of
0.20 %** — because a detector cannot, on its own, tell a typo from a real but rare
word, an intentional orthographic variant, or editorial apparatus; run against
mature, much-corrected dictionaries, such detectors produce lists that are almost
all false positives. We
report a three-stage *agentic* triage pipeline that recovers the signal by changing
the arbiter. Rather than judging a candidate against spelling statistics or corpus
attestation, the pipeline judges it against the dictionary's **own entry text**: a
first model classifies each candidate, a second confirms the suspected typos against
the entry body, an adversarial review pass gates false positives, and a human
verifies the survivors against the entry (ultimately the scanned page). Applied
across the **33 dictionaries of the Cologne Digital Sanskrit Dictionaries merge that
carry top-tier anomaly candidates** (the collection itself is larger), the pipeline
converts a near-useless flag list into two
durable assets: a small, evidence-backed **FILE-FIRST** queue (**122 triage-confirmed
candidates across 11 dictionaries, of which 97 survive full source re-verification
as unqualified correction proposals**, as of 2026-07-02) and — the principal
deliverable — a standing **do-not-file
suppression layer** of spellings each dictionary documents on purpose (**2,549 gross
across the dictionaries; 2,297 unique after deduplication**), which prevents
damaging bulk "corrections." Re-verification also surfaced a fifth candidate class
only entry-reading can catch: the **collision**, where the "correct" spelling already
exists as its own entry and a silent respell would clobber apparatus (§4.5). The genuine typos are not uniformly distributed: they
concentrate in **poorly-digitised sources** whose entries nonetheless carry strong
internal checks — *Śabda-Sāgara* (SHS) at **37/246 ≈ 15 %** and Yates (YAT) at
**27/247 ≈ 10.9 %** — where the entry's own etymology or inflectional paradigm
contradicts the headword. The contribution is methodological: the entry body, not
spelling or corpus frequency, is the reliable arbiter of typo-vs-variant, and a
staged classify→confirm→verify pipeline operationalises it at corpus scale.

## 1. Introduction

Automated spell-checking of digitised dictionaries is an attractive idea and a
treacherous one. A pattern-based anomaly detector — of the kind that flags any
headword containing a vowel/consonant sequence absent from a trusted reference
dictionary — is cheap to run and surfaces real OCR and keying errors. But it has no
model of *why* a string might be unusual. In a scholarly lexicon, an unusual string
is far more often a rare-but-real word, an intentional variant the editor recorded,
or a piece of editorial apparatus (a *variae lectiones*, a wrong-reading note, a
sandhi/in-composition form, a cross-reference) than it is a typographic error. The
result, on a mature dictionary that has already been corrected for over a century, is
an anomaly list that is overwhelmingly noise.

We quantify this **precision collapse** and then resolve it. On Monier-Williams (MW,
1899), the engine's top tier produces 1,954 candidates of which only 4 are genuine
filable corrections — **0.20 % precision**. The same pattern holds on the other large,
mature dictionaries: Böhtlingk–Roth (PW) 2 of 657, the *Vācaspatyam* (VCP) 1 of 563.
A list at this precision is worse than useless to a corrections workflow: acting on it
naïvely would *introduce* errors by "correcting" forms the editor put there
deliberately.

The thesis of this paper is that the fix is not a better spelling model but a
**different arbiter**. The information needed to decide typo-vs-variant is already
present — in the dictionary's *own entry text*. An entry that glosses a headword,
gives its etymology, or quotes it in a citation tells us whether the unusual spelling
is meant. A three-stage agentic pipeline reads that text for each candidate, and in
doing so converts the noise list into two stable products.

Our claims:

1. **Precision collapse is real and severe on mature dictionaries** (MW 0.20 %), and
   spelling statistics alone cannot escape it.
2. **The entry body is the reliable arbiter.** A classify→confirm→verify pipeline that
   reads the entry recovers the genuine typos and, more importantly, produces a
   durable **do-not-file** suppression layer (2,549 gross / 2,297 deduped) that
   prevents bad bulk edits.
3. **Genuine errors concentrate in poorly-digitised sources** (SHS 15 %, YAT 10.9 %)
   whose entries carry strong internal checks (explicit etymology + inflection), so
   the body-grounded method is at its most powerful exactly where the errors are.

A note on what this paper is *not*: it does not propose a new spell-checker, and it
never edits a dictionary's source. The host toolset already contains spelling-anomaly
detectors; the contribution here is the body-grounded triage layer above them and the
empirical result about where the signal actually lives.

## 2. Related work

**(a) Spelling-anomaly detection in digitised Sanskrit lexica.** The host
SanskritSpellCheck toolset's own pattern detectors — faultfinder, n-gram, o_vs_O —
are the immediate prior art and this paper's §4.1 input; the nearest external tool
is the ISCLS contextual-spellchecking demo for Sanskrit (Prasanna Venkatesh 2024).
Cross-lexicon comparison of the same corpus has been used for *sense* alignment
(Patel and Kulkarni 2024). The shared gap is that all of these operate on the
headword string or cross-dictionary statistics — not on the entry body that states
whether an unusual spelling is meant.

**(b) LLM verification and its characteristic failure.** Using language models as
classifiers and verifiers imports a known failure mode that is fatal in exactly this
domain: the *proof-reader effect*, in which an LLM "corrects" faithful text toward
its expectation — documented for Sanskrit OCR by Jain, Bhatt and Choudhary (2026),
whose title ("Preserving What Is Written, Not What Is Expected") is this pipeline's
design constraint stated as a slogan. The deterministic-marker backbone (§3.3 step
1), the adversarial review gate (step 4), and the never-edit guardrail (§3.5) are
the architecture that failure mode dictates.

**(c) Variation versus error is a lexicographic distinction, not a string
property.** Scholarly lexica deliberately record *variae lectiones*, wrong-reading
apparatus, in-composition forms, and cross-references — apparatus in the classical
sense of dictionary microstructure (Zgusta 1971; Hausmann and Wiegand 1989; on
editorial practice, Atkins and Rundell 2008). "Correcting" apparatus corrupts the
edition. This is why the arbiter must be the entry: the apparatus labels itself
there, and nowhere else.

The novelty claim, against all three axes: *the entry body as the arbiter,
operationalised as a staged classify→confirm→verify pipeline over a uniformly
marked-up multi-dictionary corpus*, yielding a reusable suppression layer — not a
new spelling model.

## 3. Data and method

### 3.1 Corpus
The testbed is the Cologne Digital Sanskrit Dictionaries as merged in the host
toolset's headword spine [`sanhw1.txt`](../sanhw1.txt). Of the dictionaries in that
merge, **33** carry top-tier anomaly candidates and are triaged here; they span English
(MW, Yates, *Śabda-Sāgara*, Apte, Wilson, Goldstücker, …), German (PW, the Großes
Petersburger Wörterbuch PWG, Schmidt's *Nachträge*, Cappeller, Grassmann), Sanskrit
(*Śabdakalpadruma* SKD, *Vācaspatyam* VCP), French (Burnouf, Stchoupak–Nitti–Renou),
Latin (Bopp), and several name/index works. Entry text is read from the canonical
[`csl-orig`](https://github.com/sanskrit-lexicon/csl-orig) source, `v02/<dict>/<dict>.txt`.
One dictionary, the Deccan College *Encyclopaedic Dictionary* (PD), is not in
`csl-orig` and is read from a staged external source
([`detectors/get_external_source.py`](../detectors/get_external_source.py)); it was
triaged on its first source (see §6). All Sanskrit text is in SLP1 transliteration.

### 3.2 The candidates and the problem
The engine's tier-A candidates (per dict, from
[`detectors/combined_candidates.txt`](../detectors/combined_candidates.txt)) are
headwords whose vowel/consonant pattern is absent from a trusted reference. As §1
showed, on a mature dictionary almost none of these are real errors. The triage's job
is to decide, per candidate, which of five things it is — a genuine typo, a rare real
word, an intentional variant, editorial apparatus, or (a class the 2026-07
re-verification forced into the taxonomy, §4.5) a **collision**, where the would-be
"correct" spelling already exists as its own entry — and that decision requires the
entry, not the headword.

### 3.3 The three-stage pipeline
The pipeline is run per dictionary via the
[`/dict-triage <DICT>`](../.claude/commands/dict-triage.md) skill, which drives
[`detectors/triage_*.py`](../detectors/) and
[`detectors/bodyaware_workflow.js`](../detectors/bodyaware_workflow.js):

1. **Deterministic pre-settlement.** Before any model runs, language-specific markers
   in [`detectors/triage_lang.py`](../detectors/triage_lang.py) settle the obvious
   non-errors: wrong-reading apparatus (`w.r.`, German *fehlerhaft für*, *Richtig*),
   *variae lectiones* (`v.l.`), in-composition/sandhi forms, and cross-references
   (`See`, `s.`, `= X`). This marker layer is model-independent and is the precision
   backbone.
2. **Classify — Sonnet 4.6 (`claude-sonnet-4-6`), June 2026 runs.** The remaining
   real-word candidates are classified in bulk —
   the cheaper model on the high-volume pass.
3. **Source-confirm — Opus 4.8 (`claude-opus-4-8`), June 2026 runs.** The
   suspected-typo pile is confirmed against the entry
   body by a stronger model, which must point to the entry's own evidence.
4. **Adversarial review — Opus 4.8 (`claude-opus-4-8`).** A second pass acts as a false-positive gate over the
   confirmed pile, applying an explicit keep/drop rubric: **keep** only when the
   entry's *own* derivation or citation confirms the suggestion (b/v and vowel-length
   are the highest-yield classes); **drop** for wrong-reading, redirect, *vṛddhi*
   forms, attested variants, or real distinct words.
5. **Human verification.** A human verifies each FILE-FIRST survivor against the entry,
   and — the irreducible final arbiter — against the scanned page (for b/v cases,
   checking व vs ब on the scan). A machine pre-verification of this stage was run
   2026-07-02: four Sonnet 5 (`claude-sonnet-5`) checker agents
   (locate → evidence-quote → direction → collision), with all flags adjudicated by
   Fable 5 (`claude-fable-5`) — see §4.5.

The pipeline emits, per dictionary, a `<DICT>_file_first_sf.txt` (the FILE-FIRST queue
in the CORRECTIONS standard format) and a `<DICT>_wrong_readings.txt` (the do-not-file
list); see [`corrections_draft/<DICT>/`](../corrections_draft/).

### 3.4 The two outputs and which one is stable
The FILE-FIRST/typo pass is a **stochastic** prior: re-runs surface a slightly
different small handful and can even *lose* a previously verified typo (an MW re-run
once refuted 4 confirmed typos), so a committed verified package is never blindly
overwritten. The **do-not-file** list, by contrast, rests on the deterministic marker
layer and is the durable, reproducible artifact. The deduplicated union of all 33
do-not-file lists is regenerated by
[`detectors/gen_do_not_file_suppress.py`](../detectors/gen_do_not_file_suppress.py)
into [`nochange/do_not_file_suppress.txt`](../nochange/do_not_file_suppress.txt), which
[`detectors/slp1util.py`](../detectors/slp1util.py) `load_whitelist()` unions with the
human-curated `nochange.txt` so the detectors never re-surface a documented-intentional
spelling.

### 3.5 Guardrail
The triage never edits a dictionary's source. The LLM/human layer is a *triage prior*;
the entry — and ultimately the scan — is the truth. Confirmed corrections are reported
to the separate CORRECTIONS workflow, not applied here.

## 4. Results

### 4.1 The precision collapse
On the mature, much-corrected dictionaries, tier-A precision is near zero:

| dictionary | tier-A candidates | filable typos | precision |
|---|--:|--:|--:|
| MW (1899) | 1,954 | 4 | **0.20 %** |
| PW (Böhtlingk–Roth) | 657 | 2 | 0.30 % |
| VCP (*Vācaspatyam*) | 563 | 1 | 0.18 % |
| PWG (Großes PW) | 497 | 12 | 2.4 % |

A spelling-only anomaly list on MW is, in effect, 99.8 % false positive. This is the
core negative result the body-grounded method exists to address.

### 4.2 The do-not-file suppression layer (the principal deliverable)
Across all 33 triaged dictionaries, the body-grounded pass catalogues the spellings
each dictionary records on purpose. These fall into a small apparatus taxonomy —
the lexicographically native heart of the result (Table 2a):

**Table 2a. The apparatus taxonomy of documented-intentional spellings.**

| class | what the entry says | example marker |
|---|---|---|
| wrong reading (*w.r.*) | the editor records a reading he judges erroneous in his sources | `w.r.`, German *fehlerhaft für*, *Richtig* |
| *varia lectio* (*v.l.*) | an attested alternative reading, deliberately preserved | `v.l.` |
| in-composition / sandhi form | a form valid only inside compounds or in sandhi | *in comp. for …* |
| cross-reference | the headword exists to point elsewhere | `See`, `s.`, `= X q.v.` |
| grammatical / Vedic note | ṇopadeśa root notation, Vedic stems, and similar tradition-internal marking | e.g. Dhātupāṭha `RiS` for *niś* |

*(Per-dictionary counts per class are a queued mechanical extraction from the
committed `<DICT>_wrong_readings.txt` files, whose rows carry the entry evidence but
not yet a structured class tag.)* The
**per-dictionary counts sum to 2,549** documented-intentional spellings (the gross
figure recorded in the suppress-file header); the **deduplicated union is 2,297 unique
headwords** ([`nochange/do_not_file_suppress.txt`](../nochange/do_not_file_suppress.txt)
header: "2297 unique headwords from 33 dictionaries"). Both numbers are reported
deliberately: the gross 2,549 measures the work per source; the deduped 2,297 is the
artifact actually wired into the detectors. The largest contributors are MW (630), VCP
(408), BHS (294), PW (255), PWG (248), PD (116), SCH (109), and SKD (103). This list — not the
handful of typos — is the durable value: it prevents a future bulk edit from
"correcting" forms the editors put there on purpose.

### 4.3 The filable typos and where they live
The pipeline yields **122 filable typos across 11 dictionaries**. They are highly
concentrated:

| dictionary | filable | tier-A | rate |
|---|--:|--:|--:|
| SHS (*Śabda-Sāgara*, 1900) | **37** | 246 | ~15 % |
| YAT (Yates, 1846) | **27** | 247 | ~10.9 % |
| ACC (Aufrecht, *Cat. Cat.*) | **22** | 174 | ~12.6 % |
| PWG (Großes PW) | 12 | 497 | 2.4 % |
| MCI (*Mahābhārata Cultural Index*) | 10 | 41 | ~24 % |
| MW (1899) | 4 | 1,954 | 0.20 % |
| SKD (*Śabdakalpadruma*) | 3 | 412 | 0.7 % |
| WIL (Wilson, 1832) | 3 | 108 | 2.8 % |
| PW (Böhtlingk–Roth) | 2 | 657 | 0.30 % |
| VCP (*Vācaspatyam*) | 1 | 563 | 0.18 % |
| GST (Goldstücker, 1856) | 1 | 48 | 2.1 % |

The remaining 22 dictionaries yield **0** filable typos. The signal lives in the
**poorly-digitised, less-corrected sources** (SHS, YAT, ACC), not in the large mature
ones. (The counts in this table are the *triage outputs*; §4.5 reports what survives
the downstream source re-verification — for MW, the celebrated "4 of 1,954" resolves
into 2 solid-but-scan-first proposals and 2 editorial duplicate-pair decisions, which
deepens rather than weakens the precision-collapse story.)

### 4.4 The recovery case — entries that contradict their own headwords
SHS is the body-grounded method's ideal case: a smaller, far less-corrected
digitisation in which many OCR/keying errors survive, *and* nearly every entry carries
an explicit etymology (`E. <components>`) and an inflectional paradigm — the strongest
possible internal check. Every one of the 37 SHS typos is contradicted by the entry's
own text. The errors fall into a small set of entry-decidable classes
([`corrections_draft/SHS/readme.md`](../corrections_draft/SHS/readme.md)):

- **b/v (व/ब)** — e.g. `kzIraballI → kzIravallI`, `jAmbabat → jAmbavat`; the etymology
  spells the element with **v** (`E. … vallI a creeper`).
- **retroflex w→W (ट/ठ↔ष्ट)** — e.g. `kARqapfzwa → kARqapfzWa`; the inflections are
  `-zWaH -zWA -zWaM`.
- **vowel length** — e.g. `murali → muralI`; the entry's gender/affix fixes the length
  (`f.(-lI)`).
- **sibilant / nasal / other** — e.g. `hastisuRqA → hastiSuRqA`; the gloss requires the
  corrected consonant.

YAT shows the same profile (27 typos, mostly non-b/v digitisation errors each fixed by
the entry's own citation/gloss; a b/v cluster of ~32 is held back pending scan
confirmation — deliberately, because the Bengali printing of Yates does not
typographically distinguish व from ब, so for this cluster the entry text cannot
outrank the scan). Per-row worked evidence lines for every proposed correction are
published in the live umbrella issue
[sanskrit-lexicon/CORRECTIONS#447](https://github.com/sanskrit-lexicon/CORRECTIONS/issues/447)
— the method's real-world deployment, which doubles as the paper's worked-example
appendix.

### 4.5 The source re-verification pass — and the fifth class
Before filing, all 122 FILE-FIRST rows were re-verified against the live `csl-orig`
entry text (2026-07-02; four Sonnet 5 `claude-sonnet-5` checker agents —
locate → evidence-quote → direction → collision — with all 28 flags adjudicated by
Fable 5 `claude-fable-5`; per-row verdicts in
[`corrections_draft/file_first_verified.tsv`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/file_first_verified.tsv),
synthesis in
[`corrections_draft/VERIFICATION_2026_07.md`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/VERIFICATION_2026_07.md)):

| verdict | n | meaning |
|---|--:|---|
| PASS | **97** | unqualified correction proposals (human scan-check still applies) |
| SCAN-FIRST | 12 | grammar-certain but entry-internally silent — the scan is decisive |
| EDITORIAL (collision) | 11 | the "correct" spelling **already exists as its own entry** |
| DNF | 1 | ṇopadeśa notation → moved to the do-not-file class |
| DROP | 1 | already fixed upstream between triage and verification |

The 11 collisions — YAT dual-listings cross-referenced "Idem", MW `kattfRa`, PWG's
errata-note `duzWu`, Böhtlingk's constructed `*hemana` — are the pass's conceptual
yield: a **fifth candidate class that only entry-reading can catch**, because the
evidence is the *existence of another entry*, not any property of the flagged string.
A silent headword respell here would create duplicate headwords or clobber apparatus.
That the verification pass *strengthened* the taxonomy is itself evidence for the
body-as-arbiter thesis.

## 5. Discussion

**Why the body beats spelling and corpus.** A spelling-only arbiter has no access to
intent; a corpus-attestation arbiter conflates "rare" with "wrong" and is blind to the
editorial apparatus that makes a scholarly lexicon what it is. The entry body resolves
both: it states the etymology, gives the inflection, quotes the citation, and labels
its own apparatus. The precision jump — from 0.20 % on a spelling-only MW list to a
clean, evidence-backed FILE-FIRST queue plus a 2,297-entry suppression layer — is
attributable to the change of arbiter, not to model size (the deterministic marker
layer, which is model-independent, settles most apparatus before any model runs).

**The do-not-file list is the real product.** On mature dictionaries the absolute
number of recoverable typos is tiny and not worth a campaign; the catalogue of
documented-intentional spellings is the lasting asset, because it actively *prevents
harm* — a guard rail against well-meaning bulk "corrections" that would corrupt a
century-corrected edition.

**Filable rate as a digitisation-quality signal.** The strong concentration of typos
in SHS/YAT/ACC, and their near-absence in MW/PW/VCP, means the filable rate doubles as
a proxy for how well-corrected a source already is — a cheap triage signal for which
digitisations still need attention.

## 6. Limitations

- **The FILE-FIRST/TYPO pass is stochastic.** Re-runs surface a different small handful
  and can lose a verified typo; the 122 count is therefore a *floor*, not a point
  estimate, and verified packages are unioned across runs rather than overwritten. The
  do-not-file list does not share this instability (deterministic marker backbone).
- **The queue decays against the living corpus.** One of 122 candidates (~0.8 %) was
  fixed upstream in `csl-orig` in the single week between triage and re-verification;
  any queue must be re-checked against live source immediately before filing.
- **No inter-coder reliability number yet.** The pipeline's third stage is human
  verification, but agreement has not been quantified. A second annotator independently
  re-verifying a sample (FILE-FIRST survivors and a sample of do-not-file/reviewed-out
  lines) against the entry text, reporting κ / percent agreement, is required before
  submission. *(Human gate — see handoff.)*
- **PD external source.** PD is read from a staged external source, not `csl-orig`, and
  was triaged on its first source only (0 filable, 116 do-not-file); a second source is
  expected and would only refine the do-not-file list.
- **The scan is the final, irreducible arbiter.** The LLM/human entry-reading layer is
  a prior; b/v and similar cases must ultimately be confirmed on the scanned page
  before filing. As of the 2026-07-02 re-verification, **12 of 122** rows are
  explicitly scan-first (grammar-certain, entry-internally silent), plus the ~32-row
  YAT b/v cluster held back wholesale (§4.4).

## 7. Conclusion

On mature digitised dictionaries, spelling-anomaly detection collapses to near-zero
precision (MW 0.20 %), and no amount of better spelling statistics escapes it, because
the information that distinguishes a typo from an intentional variant is not in the
headword. It is in the entry. A three-stage agentic pipeline — classify, confirm
against the entry body, human-verify — recovers the genuine errors where they
concentrate (poorly-digitised sources such as SHS at 15 % and YAT at 10.9 %) and, more
durably, produces a 2,297-entry do-not-file suppression layer (2,549 gross) that
prevents damaging bulk corrections across the Cologne corpus. The reusable result is
methodological: the dictionary body, not spelling or corpus frequency, is the reliable
ground truth for typo-vs-variant.

## Data and reproducibility

The 33-dictionary triage index and per-dictionary status table live in
[`corrections_draft/README.md`](../corrections_draft/README.md); each dictionary's
package (`readme.md`, `<DICT>_file_first_sf.txt`, `<DICT>_wrong_readings.txt`,
`<DICT>_triaged.txt`) is in [`corrections_draft/<DICT>/`](../corrections_draft/). The
deduplicated suppression artifact is
[`nochange/do_not_file_suppress.txt`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/nochange/do_not_file_suppress.txt),
regenerated with `cd detectors && python gen_do_not_file_suppress.py` (re-prints the
count and the per-dict header). The pipeline is the
[`/dict-triage <DICT>`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/.claude/commands/dict-triage.md) skill over
[`detectors/triage_*.py`](https://github.com/drdhaval2785/SanskritSpellCheck/tree/master/detectors) and
[`detectors/bodyaware_workflow.js`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/bodyaware_workflow.js).

**What reproduces how.** The claims split by layer, deliberately. The
**deterministic** layers reproduce exactly: the marker backbone, the suppress-list
generation, and every count above — the gross do-not-file total is the sum of the
per-dict header counts in the suppress file (**2,549**); the deduped union is its
data-row count (**2,297**); the filable totals are the data rows of each
`*_file_first_sf.txt` (**122** across 11 dicts); MW precision is
**4 / 1,954 = 0.20 %**. The **LLM typo pass** reproduces only as a *floor under
union-across-runs* (§3.4, §6). The suppression layer's safety is itself tested by the
committed evaluation harness
[`detectors/eval.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/eval.py):
**zero false positives** against the ~31k human-confirmed known-good words of
`nochange.txt`, and recall measured against the 3,884 human-curated historical
o_vs_O pairs — the quantitative backing for §3.4's claim that the layer does not
over-suppress. The work never edits
`csl-orig`; confirmed corrections are reported to the separate CORRECTIONS workflow
(live umbrella issue: [CORRECTIONS#447](https://github.com/sanskrit-lexicon/CORRECTIONS/issues/447)).

## References (draft — author to finalise)

Atkins, B. T. Sue, and Michael Rundell. 2008. *The Oxford Guide to Practical
Lexicography.* Oxford: Oxford University Press.

Hausmann, Franz Josef, and Herbert Ernst Wiegand. 1989. "Component Parts and
Structures of General Monolingual Dictionaries: A Survey." In Hausmann, Reichmann,
Wiegand and Zgusta (eds.), *Wörterbücher / Dictionaries / Dictionnaires,* vol. 1
(HSK 5.1), 328–360. Berlin and New York: Walter de Gruyter.

Jain, ..., Bhatt, ..., and Choudhary, ... 2026. "Preserving What Is Written, Not What
Is Expected: The Proof-Reader Effect of LLMs in Sanskrit OCR." In *Proceedings of the
International Sanskrit Computational Linguistics Symposium (ISCLS 2026).* *[author to
complete first names/pages when the proceedings volume is published]*

Patel, Dhaval, and Amba Kulkarni. 2024. "Word Sense Alignment of Sanskrit Lexica."
In *Proceedings of the 6th International Sanskrit Computational Linguistics Symposium
(ISCLS 2024).* [aclanthology.org/2024.iscls-1.1](https://aclanthology.org/2024.iscls-1.1.pdf).

Prasanna Venkatesh, T. S. 2024. "Contextual Spellchecking for Sanskrit." Demo
presented at the 6th International Sanskrit Computational Linguistics Symposium
(ISCLS 2024). *[demo track — no proceedings PDF; author to confirm citation form]*

Zgusta, Ladislav. 1971. *Manual of Lexicography.* (Janua Linguarum, Series Maior 39.)
Prague: Academia; The Hague and Paris: Mouton.

**Primary digital source.** Cologne Digital Sanskrit Dictionaries (CDSL). Institute
of Indology and Tamil Studies, University of Cologne.
[`sanskrit-lexicon.uni-koeln.de`](https://www.sanskrit-lexicon.uni-koeln.de/).

