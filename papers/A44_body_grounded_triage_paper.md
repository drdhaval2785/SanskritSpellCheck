_Created: 10-08-2026 · Last updated: 06-09-2026_

---
paper_id: A44
title: "The Dictionary Body as Ground Truth: Body-Grounded LLM Triage and the Precision-Collapse Result"
status: full draft (4/5) — author-voice pass 2 2026-09-06 (SIGNOFF_A44_author_pass.md); GED/confusion-set reframe + harm metric (§4.7) + References fixes 2026-07-12; author-voice pass 2026-07-10; blind second-annotator study (§4.6) folded in 2026-07-10; revised 2026-07-03 per A44_review_fable5.md (IJL reframe, verification pass folded in)
readiness: 4/5
venue: "International Journal of Lexicography (IJL)"
author: "**Mārcis Gasūns**, independent scholar ([ORCID 0000-0003-4513-884X](https://orcid.org/0000-0003-4513-884X)), gasyoun@ya.ru"
data_source: "corrections_draft/README.md (33-dict triage) + corrections_draft/VERIFICATION_2026_07.md (per-row re-verification) + nochange/do_not_file_suppress.txt (2297 deduped) + .claude/commands/dict-triage.md (pipeline)"
---

# The Dictionary Body as Ground Truth: Body-Grounded LLM Triage and the Precision-Collapse Result

> **Draft status (2026-07-10).** Revised per the pre-submission review
> ([A44_review_fable5.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/A44_review_fable5.md)): reframed for IJL, the 2026-07-02
> source re-verification folded in (fifth candidate class: *collision*), apparatus
> taxonomy promoted to a named table with per-dictionary counts, §2 related work
> drafted, per-phase model attribution added, reproducibility claims split. The
> blind second-annotator study of §4.6 was added on 2026-07-10; it discharges the
> former reliability gate under ruling D2, and the human recruit stays deferred and
> acknowledged as future work in §6.
>
> **This pass (12-07-2026, Fable 5, `claude-fable-5`, per H825 ruling D10).** The
> task is now positioned explicitly on the GED / confusion-set (real-word error)
> lineage — additive framing in the Abstract, §1 and a new §2(d); the related work
> gains verified confusion-set, anomaly-detection and CDSL-adjacent citations; a
> detection-level **harm metric** against the held-out gold verdicts is reported
> (new §4.7); and the two known References defects are fixed — Artstein & Poesio
> (2008) now has a full entry, and the unverifiable "ISCLS 2026 proof-reader"
> entry is **removed** (the over-correction claim now rests on verified citations
> plus this project's own observation). Every References URL was resolved and
> title/author-checked against its landing page on 12-07-2026.
>
> **Second author-voice pass (06-09-2026, Fable 5.1, `claude-fable-5-1`, H3857).**
> Register only — no number, claim or citation altered; the calls made and the
> flags carried are in [SIGNOFF_A44_author_pass.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/papers/SIGNOFF_A44_author_pass.md).
>
> **Open before submission:** (1) an author read-through for register; (2) the
> cross-family blind annotation run (§4.6) — tooled, pending an API credential;
> (3) the human-anchor gap of §6 remains tracked, not resolved.

## Abstract

A spelling-anomaly detector cannot, on its own, tell a typo from a real but rare
word, an intentional orthographic variant, or editorial apparatus. In
error-detection terms the task is **grammatical error detection (GED)** posed at
the headword level over a confusion set of near-spellings — a real-word-error
problem, since the flagged string is (or resembles) a possible word and the
question is whether *this* occurrence is an error; the system detects and
triages but does not auto-correct. Run against
mature, much-corrected dictionaries, such detectors produce lists that are almost
all false positives: on the Monier-Williams Sanskrit–English dictionary, only **4 of
1,954** top-tier candidates survive triage — a precision of **0.20 %**. We report a
staged *body-grounded* triage that recovers the signal by changing the arbiter: a
candidate is judged not against spelling statistics or corpus attestation but
against the dictionary's **own entry text** — the gloss, etymology, inflection, and
the editorial apparatus the entry itself declares. Applied across the **33
dictionaries of the merged Cologne Digital Sanskrit collection that carry top-tier
anomaly candidates**, the triage converts a near-useless flag list into two durable
lexicographic assets: a small, evidence-backed correction queue (**122
triage-confirmed candidates, of which 92 survive a subsequent per-row source
re-verification as unqualified proposals**, as of 2026-07-02) and — the principal
deliverable — a standing **do-not-file catalogue** of spellings each dictionary
documents on purpose (**2,549 across the dictionaries; 2,297 unique after
deduplication**), which prevents damaging bulk "corrections" of *variae lectiones*,
wrong-reading apparatus, and cross-references. Re-verification also surfaced a
class invisible to headword-level checking: **collisions**, where the "correct"
spelling already exists as its own entry and a silent respell would create
duplicates or clobber apparatus. The genuine typos concentrate in
**poorly-digitised sources** whose entries carry strong internal checks —
*Śabda-Sāgara* (SHS) ≈ 15 % and Yates (YAT) ≈ 11 % — where the entry's own
etymology or paradigm contradicts its headword. The contribution is
methodological: the entry body, not spelling or corpus frequency, is the reliable
arbiter of typo-vs-variant.

## 1. Introduction

Every scholarly dictionary contains spellings its editor knew to be wrong. The
wrong-reading note (*w.r.*), the *varia lectio*, the cross-referenced by-form, the
sandhi-bound compound member — these are not defects but **apparatus**: the
lexicographer's record of what the tradition transmits, deliberately including
forms the editor judged erroneous *in the sources*. This is the oldest boundary
problem of practical lexicography — variation versus error — and it has a hard
consequence for digital curation: any automated "correction" campaign that cannot
tell apparatus from typo will corrupt precisely the entries where the lexicographer
was most careful. A *v.l.* silently "fixed" is a witness destroyed.

Automated spell-checking of digitised dictionaries is therefore an attractive idea
and a treacherous one. A pattern-based anomaly detector — of the kind that flags any
headword containing a vowel/consonant sequence absent from a trusted reference
dictionary — is cheap to run and surfaces real OCR and keying errors. But it has no
model of *why* a string might be unusual. In a scholarly lexicon, an unusual string
is far more often a rare-but-real word, an intentional variant, or apparatus than a
typographic error. The result, on a mature dictionary corrected for over a century,
is an anomaly list that is overwhelmingly noise.

This task has a name and a twenty-five-year lineage. In the vocabulary of the
error-detection literature it is **grammatical error detection (GED)** at the
headword level, over a **confusion set**: each candidate is a real-word-like
string to be arbitrated against a small set of near-spellings (b/v, vowel length,
retroflexion) — the *real-word error* setting studied since Golding and Roth's
(1999) context-sensitive spelling correction and institutionalised as a benchmark
by the Chinese Spelling Check bake-offs (Tseng et al. 2015), where most errors are
likewise visually or phonologically confusable real characters. The system
reported here sits on the *detection* side of the detection/correction
distinction drawn by Rei and Yannakoudakis (2016): it flags, classifies, and
triages single headwords; it performs no full-sentence correction and applies
nothing automatically. Section 4.7 evaluates it accordingly, with the
detection-standard precision-weighted F0.5.

We quantify this **precision collapse** and then resolve it. On Monier-Williams (MW,
1899), the engine's top tier produces 1,954 candidates of which only 4 survive
triage — **0.20 % precision**. The same pattern holds on the other large, mature
dictionaries: Böhtlingk–Roth (PW) 2 of 657, the *Vācaspatyam* (VCP) 1 of 563. A list
at this precision is worse than useless to a corrections workflow: acting on it
naively would *introduce* errors by "correcting" forms the editor put there
deliberately.

The thesis of this paper is that the fix is not a better spelling model but a
**different arbiter**. The information needed to decide typo-vs-variant is already
present — in the dictionary's *own entry text*. An entry that glosses a headword,
gives its etymology, or quotes it in a citation tells us whether the unusual
spelling is meant. A staged triage reads that text for each candidate, and in doing
so converts the noise list into two stable products.

Our claims:

1. **Precision collapse is real and severe on mature dictionaries** (MW 0.20 %), and
   spelling statistics alone cannot escape it.
2. **The entry body is the reliable arbiter.** A classify→confirm→verify pipeline that
   reads the entry recovers the genuine typos and, more importantly, produces a
   durable **do-not-file** catalogue (2,549 across dictionaries / 2,297 deduped) that
   prevents bad bulk edits.
3. **Genuine errors concentrate in poorly-digitised sources** (SHS ≈ 15 %, YAT ≈ 11 %)
   whose entries carry strong internal checks (explicit etymology + inflection), so
   the body-grounded method is at its most powerful exactly where the errors are.

A note on what this paper is *not*: it does not propose a new spell-checker, and it
never edits a dictionary's source. The host toolset already contains spelling-anomaly
detectors; the contribution here is the body-grounded triage layer above them and the
empirical result about where the signal actually lives.

## 2. Related work

Four literatures border the method. **(a) Dictionary-digitisation quality assurance
and OCR post-correction.** Error detection in digitised reference works generally
operates on the string level — pattern anomalies, n-gram plausibility, dictionary
lookups (Piotrowski 2012 surveys the OCR-era pipeline). The direct methodological
ancestor of the host toolset's detectors is Bloodgood and Strauss (2016), who run a
battery of statistical anomaly detectors (character rarity, length, language-model
signals) over an XML electronic dictionary to flag likely errors; the pattern,
n-gram and confusion-pair detectors here are the same move on Sanskrit headwords,
and §4.1 measures exactly how far that string-level family carries on a mature
lexicon: to 0.20 % precision. Discrepancy- and entropy-based anomaly ranking has
likewise been used to surface inconsistencies in annotated lexical resources
(Hollenstein et al. 2016). On this paper's own corpus, Mondaca and Rau (2020)
transform the Cologne Digital Sanskrit Dictionaries into OntoLex-Lemon — a
modelling effort, not a correcting one — and Patel and Kulkarni (2024), by the
host toolset's author, align word senses *across* the Sanskrit lexica; that
cross-dictionary correspondence is the same signal this toolset's consensus and
collation detectors exploit, turned from sense alignment to error detection, which
makes the two lines direct companions. The nearest prior tool is the
Hunspell-based spellchecker for Sanskrit
presented at ICON 2022 (Prasanna 2022 — Sanskrit-language object text; 100 %
precision on the words it accepts, but heavy over-flagging from its 37,058-entry
paradigm-generated lexicon — the mirror image of the precision collapse measured
here); the present work differs in target (the *dictionary as edition*, headwords
plus apparatus) and in output (a suppression catalogue, not corrections). No tool
in the survey models the variant-versus-typo distinction — Hunspell
wordlists, up to the 543,758-entry `sa_IN` pack bundled with LibreOffice since
2025, hard-code one spelling as correct (full survey:
[docs/PRIOR_ART.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/PRIOR_ART.md)).

**(b) LLM-assisted correction
and its characteristic failure.** Recent evaluations of LLM and vision-language
reading of historical text document an over-correction failure mode: the model
produces fluent, plausible output with little grounding in what the witness
actually reads — "plausible but visually unsupported" substitutions on ancient
Greek editions (Karamolegkou et al. 2026), and no-free-lunch results for
LLM post-correction of historical documents generally (Kanerva et al. 2025). We
have observed the same tendency in this pipeline's own model passes — the model
"fixes" what is written toward what it expects; call it the *proof-reader
effect*. That failure mode is precisely what a dictionary's apparatus maximally
provokes, and it motivates this pipeline's two design choices: a deterministic
marker backbone that settles declared apparatus *before* any model runs, and an
adversarial review stage gating the model's confirmations.

**(c) Variation versus
error in historical lexicography.** The editorial theory of *variae lectiones* and
wrong-reading apparatus long predates digitisation; what the digital setting adds
is scale and the new risk of *bulk* corruption. We are not aware of prior work
that operationalises the entry body as the arbiter for typo-vs-variant at corpus
scale, or that treats the resulting **do-not-file catalogue as the primary
deliverable** of a spell-checking campaign — the inversion this paper argues for.

**(d) Grammatical error detection and the confusion-set tradition.** The
typo-vs-variant decision is a real-word error problem — the flagged string is (or
resembles) a possible word, and the judgment is whether *this* occurrence is an
error. That is the setting of context-sensitive spelling correction since Golding
and Roth (1999), whose WinSpell arbitrates within fixed confusion sets, and of the
SIGHAN Chinese Spelling Check bake-offs (Tseng et al. 2015), whose errors are
predominantly visually or phonologically confusable real characters — the closest
large-scale analogue to the b/v, vowel-length and retroflex confusions here. Two
of that tradition's instruments transfer directly. First, the
detection/correction distinction (Rei and Yannakoudakis 2016): this system is GED
— it flags and triages but never auto-corrects — and is evaluated with the
tradition's precision-weighted F0.5 (§4.7; on GEC/GED evaluation practice see
Grundkiewicz et al. 2015). Second, typed error annotation with per-type counts as
the backbone of evaluation (Bryant et al. 2017's ERRANT); Table 2's apparatus
taxonomy with per-class and per-dictionary counts is the lexicographic analogue.
What the dictionary setting adds to this lineage is the apparatus problem — a
confusion set that *deliberately contains* "wrong" forms — and an arbiter the
sentence-level tradition does not have: the entry body. On annotator disagreement
as signal rather than noise, §4.6 follows Plank (2022).

*(Every References URL was resolved and title/author-checked on 12-07-2026; the
project's human citation-verification gate remains a final spot-check before
submission.)*

## 3. Data and method

### 3.1 Corpus
The testbed is the Cologne Digital Sanskrit Dictionaries as merged in the host
toolset's headword spine [`sanhw1.txt`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/sanhw1.txt). Of the dictionaries in that
merge, **33** carry top-tier anomaly candidates and are triaged here; they span English
(MW, Yates, *Śabda-Sāgara*, Apte, Wilson, Goldstücker, …), German (PW, the Großes
Petersburger Wörterbuch PWG, Schmidt's *Nachträge*, Cappeller, Grassmann), Sanskrit
(*Śabdakalpadruma* SKD, *Vācaspatyam* VCP), French (Burnouf, Stchoupak–Nitti–Renou),
Latin (Bopp), and several name/index works. Entry text is read from the canonical
[`csl-orig`](https://github.com/sanskrit-lexicon/csl-orig) source, `v02/<dict>/<dict>.txt`.
One dictionary, the Deccan College *Encyclopaedic Dictionary* (PD), is not in
`csl-orig` and is read from a staged external source
([`detectors/get_external_source.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/get_external_source.py)); it was
triaged on its first source (see §6). All Sanskrit text is in SLP1 transliteration.

### 3.2 The candidates and the five-way decision
The engine's tier-A candidates (per dict, from
[`detectors/combined_candidates.txt`](../detectors/combined_candidates.txt)) are
headwords whose vowel/consonant pattern is absent from a trusted reference. As §1
showed, on a mature dictionary almost none of these are real errors. The triage's job
is to decide, per candidate, which of **five** things it is:

1. a **genuine typo** (the entry's own evidence contradicts the headword);
2. a **rare real word**;
3. an **intentional variant** the editor recorded;
4. **editorial apparatus** (*w.r.*, *v.l.*, in-composition form, cross-reference);
5. a **collision** — the "corrected" spelling already exists as its own entry, so the
   right action is an editorial decision (merge / respell / leave), never a silent
   respell.

The fifth class was forced by the 2026-07 re-verification (§4.5): eleven candidates
that looked like plain corrections turned out to be duplicate-pair or apparatus
collisions — a category only *entry-reading* can catch (the colliding entry must be
looked up), which independently strengthens the body-as-arbiter thesis. Each decision
requires the entry, not the headword.

### 3.3 The staged pipeline
The pipeline is run per dictionary via the
[`/dict-triage <DICT>`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/.claude/commands/dict-triage.md) skill (operational detail
in Appendix A). Model attribution follows the project standard — tier plus exact
version per phase; the June 2026 triage runs used Sonnet 4.6 (`claude-sonnet-4-6`)
for bulk classification and Opus 4.8 (`claude-opus-4-8`) for source-confirmation and
adversarial review; the 2026-07-02 re-verification used four Sonnet 5
(`claude-sonnet-5`) checkers with Fable 5 (`claude-fable-5`) adjudication:

1. **Deterministic pre-settlement** (no model). Language-specific markers
   ([`detectors/triage_lang.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/triage_lang.py)) settle the declared
   apparatus: wrong-reading (`w.r.`, German *fehlerhaft für*, *Richtig*), *variae
   lectiones* (`v.l.`), in-composition/sandhi forms, cross-references (`See`, `s.`,
   `= X`). This marker layer is model-independent and is the precision backbone.
2. **Classify** — Sonnet 4.6 (`claude-sonnet-4-6`), June 2026. The remaining
   candidates are classified in bulk (the cheaper model on the high-volume pass).
3. **Source-confirm** — Opus 4.8 (`claude-opus-4-8`), June 2026. The suspected-typo
   pile is confirmed against the entry body; the model must point to the entry's own
   evidence.
4. **Adversarial review** — Opus 4.8 (`claude-opus-4-8`), June 2026. A second pass
   acts as a false-positive gate with an explicit keep/drop rubric: **keep** only when
   the entry's *own* derivation or citation confirms the suggestion (b/v and
   vowel-length are the highest-yield classes); **drop** for wrong-reading, redirect,
   *vṛddhi* forms, attested variants, or real distinct words.
5. **Source re-verification** — Sonnet 5 (`claude-sonnet-5`) checkers + Fable 5
   (`claude-fable-5`) adjudication, 2026-07-02. Every surviving candidate re-verified
   per row against live `csl-orig` (locate → evidence-quote → direction → collision
   checks); results in §4.5.
6. **Human verification.** A human verifies each survivor against the entry, and —
   the irreducible final arbiter — against the scanned page (for b/v cases, checking
   व vs ब on the scan).

### 3.4 The two outputs, and exactly what reproduces
The two output layers have different epistemic status, and we state them separately.
**Deterministic and exactly reproducible:** the marker backbone, the do-not-file
catalogue built on it, and every count in this paper recompute bit-identically from
the committed files. **Stochastic, reproducible as a floor:** the LLM typo pass —
re-runs surface a slightly different small handful and can even *lose* a previously
verified typo (an MW re-run once refuted 4 confirmed typos), so verified packages are
unioned across runs and never blindly overwritten; the 122 figure is a floor under
union-across-runs, not a point estimate. The suppression layer's safety has its own
harness: [`detectors/eval.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/eval.py) checks that the suppress list
raises **zero false positives against ~31,000 known-good headwords** and measures
recall against the 3,884 historically corrected pairs — the evidence that the
do-not-file layer does not over-suppress. The deduplicated union of all 33
do-not-file lists is regenerated by
[`detectors/gen_do_not_file_suppress.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/gen_do_not_file_suppress.py)
into [`nochange/do_not_file_suppress.txt`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/nochange/do_not_file_suppress.txt), which
[`detectors/slp1util.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/slp1util.py) `load_whitelist()` unions with the
human-curated `nochange.txt` so the detectors never re-surface a documented-intentional
spelling.

### 3.5 Guardrail
The triage never edits a dictionary's source. The LLM/human layer is a *triage prior*;
the entry — and ultimately the scan — is the truth. Confirmed corrections are reported
to the separate CORRECTIONS workflow (deployed live as umbrella issue
[CORRECTIONS #447](https://github.com/sanskrit-lexicon/CORRECTIONS/issues/447)), not
applied here.

## 4. Results

### 4.1 The precision collapse
On the mature, much-corrected dictionaries, tier-A precision is near zero:

| dictionary | tier-A candidates | triage-confirmed | precision |
|---|--:|--:|--:|
| MW (1899) | 1,954 | 4 | **0.20 %** |
| PW (Böhtlingk–Roth) | 657 | 2 | 0.30 % |
| VCP (*Vācaspatyam*) | 563 | 1 | 0.18 % |
| PWG (Großes PW) | 497 | 12 | 2.4 % |

A spelling-only anomaly list on MW is, in effect, 99.8 % false positive. This is the
core negative result the body-grounded method exists to address. (Re-verification
sharpened MW's four survivors further — see §4.5.)

### 4.2 The do-not-file catalogue (the principal deliverable)
Across all 33 triaged dictionaries, the body-grounded pass catalogues the spellings
each dictionary records on purpose. **Table 2** gives the apparatus taxonomy with its
counts:

*Table 2a. Documented-intentional spellings by apparatus class (all 33 dictionaries,
gross = 2,549).*

| apparatus class | marker examples | count |
|---|---|--:|
| cross-reference | `See X`, `s. X`, `= X q.v.` | 1,048 |
| other documented-intentional | grammatical/Vedic notes, ṇopadeśa root notation, entry-declared oddities | 845 |
| *varia lectio* | `v.l.` | 260 |
| wrong-reading apparatus | `w.r.`, *fehlerhaft für*, *Richtig:* | 259 |
| in-composition / sandhi form | *in comp. for X*, ibc./ifc. | 137 |

*Table 2b. Largest per-dictionary contributions (class breakdown).*

| dictionary | total | dominant classes |
|---|--:|---|
| MW | 630 | other 222 · cross-ref 204 · in-comp 105 · v.l. 54 · w.r. 45 |
| VCP | 408 | cross-ref 362 · other 43 |
| BHS (Edgerton) | 294 | cross-ref 138 · v.l. 81 · other 67 |
| PW | 255 | w.r. 95 · other 88 · v.l. 38 |
| PWG | 248 | cross-ref 137 · w.r. 71 · other 28 |
| PD | 116 | v.l. 66 · cross-ref 22 · w.r. 16 |
| SCH | 109 | other 75 · w.r. 18 |
| SKD | 103 | other 86 · cross-ref 14 |

The **per-dictionary counts sum to 2,549**; the **deduplicated union is 2,297 unique
headwords** ([`nochange/do_not_file_suppress.txt`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/nochange/do_not_file_suppress.txt)).
Both numbers are reported because they answer different questions: the gross 2,549
measures the work per source; the deduped 2,297 is the artefact wired into the
detectors. The class profile repays attention — the indigenous VCP suppresses almost entirely via
cross-references (its kośa structure), while Böhtlingk's PW is the corpus's densest
carrier of explicit wrong-reading apparatus (95), and Edgerton's BHS of *variae
lectiones* (81). This catalogue — not the handful of typos — is the durable value: it
prevents a future bulk edit from "correcting" forms the editors put there on purpose.

### 4.3 The fileable typos and where they live
The triage yields **122 confirmed candidates across 11 dictionaries**. They are highly
concentrated:

| dictionary | confirmed | tier-A | rate |
|---|--:|--:|--:|
| SHS (*Śabda-Sāgara*, 1900) | **37** | 246 | ~15 % |
| YAT (Yates, 1846) | **27** | 219 | 12.3 % |
| ACC (Aufrecht, *Catalogus Catalogorum*) | **22** | 144 | 15.3 % |
| PWG (Großes PW) | 12 | 497 | 2.4 % |
| MCI (*Mahābhārata Cultural Index*) | 10 | 24 | 41.7 % |
| MW (1899) | 4 | 1,954 | 0.20 % |
| SKD (*Śabdakalpadruma*) | 3 | 412 | 0.7 % |
| WIL (Wilson, 1832) | 3 | 108 | 2.8 % |
| PW (Böhtlingk–Roth) | 2 | 657 | 0.30 % |
| VCP (*Vācaspatyam*) | 1 | 563 | 0.18 % |
| GST (Goldstücker, 1856) | 1 | 48 | 2.1 % |

The remaining 22 dictionaries yield **0** fileable typos. The signal lives in the
**poorly-digitised, less-corrected sources** (SHS, YAT, ACC), not in the large mature
ones. Tier-A denominators are counted from the committed per-dictionary
candidate files (2026-07-02 pin: YAT 219, ACC 144, MCI 24); the earlier print's
YAT 247 / ACC 174 / MCI 41 came from the gitignored `combined_candidates.txt` and is
not reproducible from anything committed — regenerate with `cd detectors && python
run_all.py ../sanhw1.txt` only for live work, never as the paper's denominators.

### 4.4 The recovery case — entries that contradict their own headwords
SHS is the body-grounded method's ideal case: a smaller, far less-corrected
digitisation in which many OCR/keying errors survive, *and* nearly every entry carries
an explicit etymology (`E. <components>`) and an inflectional paradigm — the strongest
possible internal check. Every one of the 37 SHS typos is contradicted by the entry's
own text. The errors fall into a small set of entry-decidable classes
([`corrections_draft/SHS/readme.md`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/SHS/readme.md); each class
is deployed with full in-entry evidence lines in the live umbrella issue
[CORRECTIONS #447](https://github.com/sanskrit-lexicon/CORRECTIONS/issues/447)):

- **b/v (व/ब)** — e.g. `kzIraballI → kzIravallI`, `jAmbabat → jAmbavat`; the etymology
  spells the element with **v** (`E. … vallI a creeper`).
- **retroflex w→W (ट/ठ↔ष्ट)** — e.g. `kARqapfzwa → kARqapfzWa`; the inflections are
  `-zWaH -zWA -zWaM`. *(This very row also illustrates queue decay: it was corrected
  upstream between triage and re-verification — §4.5.)*
- **vowel length** — e.g. `murali → muralI`; the entry's gender/affix fixes the length
  (`f.(-lI)`).
- **sibilant / nasal / other** — e.g. `hastisuRqA → hastiSuRqA`; the gloss requires the
  corrected consonant.

YAT shows the same profile (27 typos, mostly non-b/v digitisation errors each fixed by
the entry's own citation/gloss). One YAT cluster of ~32 b/v candidates is held back
for the scan deliberately: **Bengali print does not distinguish व and ब** — Yates was
typeset in Calcutta from Bengali-script founts — so for YAT the entry text *cannot*
arbitrate b/v and only the scanned page can. The held-back cluster is the method
correctly recognising the limit of its own arbiter.

### 4.5 The re-verification pass — and the collision class
Before any filing, all 122 confirmed candidates were re-verified per row against live
`csl-orig` (2026-07-02; per-row verdicts in
[`corrections_draft/file_first_verified.tsv`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/file_first_verified.tsv),
narrative in [`corrections_draft/VERIFICATION_2026_07.md`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/VERIFICATION_2026_07.md)):

| verdict | n | meaning |
|---|--:|---|
| **PASS** | 92 | unqualified proposals (still scan-checked by the human, as always) |
| **SCAN-FIRST** | 17 | grammar-certain but entry-internal evidence silent — the scan is decisive |
| **EDITORIAL (collision)** | 11 | the correct spelling already exists as its own entry — merge/respell/leave is an editorial decision |
| **DNF** | 1 | ṇopadeśa root notation — moved to the do-not-file class |
| **DROP** | 1 | already corrected upstream between triage and verification |

Three consequences. First, the **collision class** (§3.2, class 5): eleven candidates
— YAT dual-listings cross-referenced "Idem", MW's `kattfRa`, PWG's `duzWu` errata
note, PW's constructed `*hemana` — would, under a naive respell, have created
duplicate headwords or clobbered apparatus. Only entry-reading catches these, which
strengthens the body-as-arbiter thesis: even the *confirmed-typo* pile still contains
decisions that belong to the editor, not the pipeline. Second, **MW's headline
restated**: the triage's "4 fileable of 1,954" resolves after
re-verification into 2 scan-first plus 2 editorial-collision rows — the
precision-collapse story deepens (on the most-corrected dictionary, even the
survivors are not simple fixes). Third, **queues decay**: one row (~0.8 %) was fixed
upstream in the five weeks between triage and verification; correction queues must be
re-verified against the live source immediately before filing. (The verdict counts
above reflect the editor's same-day audit of the verification pass, which downgraded
five SHS rows resting on class-pattern rationale alone from PASS to SCAN-FIRST —
"no in-entry etymology → the scan decides". §4.6 returns to those five rows.)

### 4.6 A blind LLM second annotator: the method's reproducibility, measured

The five-way verdict taxonomy of §4.5 was re-applied to all 122 rows by a **blind
second annotator**: an independent model tier (Opus 4.8, `claude-opus-4-8`; the
original pass was Sonnet 5, `claude-sonnet-5`, mechanical verification with Fable 5,
`claude-fable-5`, adjudication of flags), a prompt written fresh from the taxonomy
definitions, and an evidence file containing *only* the candidate pair and the
dictionary's own entry bodies under both spellings — no access to the original
verdicts, notes, prompts, or detector tier labels
([`corrections_draft/irr/`](../corrections_draft/irr/); inputs built by
[`irr_build_inputs.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/irr_build_inputs.py), agreement computed with
exact rational arithmetic by [`irr_agreement.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/irr_agreement.py)).

Agreement on the five-way taxonomy is **κ = 0.336** (Cohen; observed agreement
59.0 %, chance 38.3 %; approximate 95 % CI ≈ 0.34 ± 0.14 — spanning "poor" to
"moderate"; full confusion matrix and per-class κ in
[`agreement_stats.md`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/irr/agreement_stats.md)). On the
binary collapse — *does this row describe a genuine defect needing
action* ({PASS, SCAN-FIRST, EDITORIAL}) versus not ({DNF, DROP}) — raw agreement is
**121/122 (99.2 %)**; we print the raw count rather than a κ for the binary
collapse: with marginals this skewed (the blind annotator produced zero DNF, a
2×1 marginal), κ is a one-cell statistic and misleads. The
blind annotator never rejected a proposed correction as substantively wrong
(zero DNF), and reproduced the original EDITORIAL class with perfect recall (all 11
rows).

The 50 five-way disagreements are not noise but signal — the position Plank (2022) argues for
annotator label variation generally; they decompose almost
exhaustively into two *policy* differences, with **no case of misread evidence**:

1. **Collision threshold (33 rows).** The blind annotator labels EDITORIAL whenever
   the corrected spelling has *any* entry of its own; the original pass reserved
   EDITORIAL for genuine rival readings, filing catalogue-structure repeats (ACC's
   multi-supplement *Catalogus Catalogorum* lists the same work several times, so a
   misspelled repeat is a plain typo, not a merge question) as PASS. Twenty-one of
   the thirty-three rows are ACC.
2. **Evidence threshold (16 rows).** The blind annotator demands that the entry body
   *spell* the corrected form, refusing philological inference the original pass
   accepted (that a month-name is *Phālguna*, that *mahāmāyā* underlies "Durgā;
   illusion", that ruki requires *-ṣu* in a desiderative). Two of these
   (YAT `duzwu`, `cInapizWa`) flag a real subtlety: the entry's inflectional
   parenthesis repeats the headword's own error, so body-internal consistency can
   *support* a typo — the one configuration where the body misleads as arbiter.
3. **One decisiveness reversal**: on SHS `saptAtitama` the blind annotator was *more*
   confident than the editor (morphological impossibility read as decisive; the
   editor's audit had ruled the scan decisive).

Two findings follow. First, the disagreement is
**about filing policy, not about facts** — both annotators recognise the same
defects on the same evidence (the 99.2 % binary figure), and κ = 0.336 measures how
much of the five-way taxonomy is decision rule rather than observation; this is the
category-definition effect the agreement literature warns about (Artstein and
Poesio 2008), here isolated experimentally because the evidence channel was held
fixed. Second, the blind annotator **independently reproduced the human editor's
audit**: of the five weak SHS rows the editor downgraded PASS → SCAN-FIRST on
02-07-2026 (§4.5), the blind pass — with no knowledge that an audit had occurred —
assigned SCAN-FIRST to four and PASS to one. The method's cautious layer, in other
words, is recoverable from the evidence alone.

One caveat of design, not execution: both annotators are Anthropic models — a
same-family pairing the self-enhancement-bias literature cautions against. A
cross-family replication is now tooled
([`detectors/irr_cross_family.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/irr_cross_family.py) re-runs the
identical blind protocol with a non-Anthropic judge) and pending an API
credential; its κ will be reported as obtained, like the first.

### 4.7 The harm metric: what a naive auto-apply would corrupt

The GED framing of §1 licenses a detection-level evaluation of the underlying
spelling-anomaly detectors themselves, and that evaluation directly measures the
stakes of this paper's central claim. The verified verdicts of §4.5 double as a
held-out gold set ([`detectors/gold_corrections.tsv`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/gold_corrections.tsv),
derived from [`file_first_verified.tsv`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/file_first_verified.tsv)):
**109 POSITIVE rows — 108 unique (one duplicate pair, jAmbabat, filed for both SHS and
WIL)** (genuine corrections a detector *should* find) and **13
HARM rows** — the EDITORIAL-collision, DNF and DROP verdicts, i.e. exactly the
rows that must **not** be silently "corrected". [`detectors/eval.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/eval.py)
scores each corrector against this gold set with the tradition's
precision-weighted F0.5 (β = 0.5; on GEC/GED evaluation practice see Grundkiewicz
et al. 2015), plus a **harm rate**: the share of the 13 protected rows the
detector flags as if they were plain corrections.

*Table 4. Detection-level metrics against the verified gold set (109 rows / 108 unique
POSITIVE / 13 HARM; false-positive rate measured against the ~31,843-word known-good
whitelist).*

| detector | P | R | F0.5 | FPR (whitelist) | harm rate |
|---|--:|--:|--:|--:|--:|
| `spell_correct` | 91.2 % | 95.4 % | 0.920 | 0.0 | **76.9 %** (10/13) |
| `consensus` | 88.5 % | 85.2 % | 0.878 | 0.0 | **92.3 %** (12/13) |
| `intra_dup` | 75.0 % | 33.3 % | 0.600 | 0.0 | **92.3 %** (12/13) |
| `dict_vs_corpus` | 0.0 % | 0.0 % | 0.000 | 0.0 | 0.0 % (0/13) |
| **union of all** | 89.2 % | 99.1 % | 0.910 | 0.0 | **100 %** (13/13) |

Read as ordinary GED systems, the detectors are good: F0.5 of 0.88–0.92, 99.1 %
recall in union, and zero false positives against the known-good whitelist — the
existing filing gate holds. One scope caveat on that 99.1 %: the gold frame is by
construction the union's own surviving verdicts, so this is **recall of the triage
frame**, not dictionary-wide recall; precision, FPR and the harm rate are not affected
by the circularity. But the harm column is the finding: the same
detectors, on their own, flag **77–100 % of the exact collision, apparatus and
stale rows** (range across the seven flag-raising detectors; the degenerate
`dict_vs_corpus` — which flags nothing at all, 0/13 — is excluded from the range)
that the triage's EDITORIAL/DNF/DROP verdicts exist to protect. A
naive auto-apply pipeline reporting 99 % recall would, in the same run,
corrupt all 13 protected rows — merging rival readings, respelling apparatus,
re-introducing an upstream-fixed form. This is not a separate result from the
paper's thesis; it is that thesis measured. The do-not-file layer (§4.2, §5) is
what stands between a strong detector and the harm column, and nothing in the
detector's own scores — precision, recall, F0.5, whitelist FPR — reveals the
danger: only entry-level triage does.

## 5. Discussion

**Why the body beats spelling and corpus.** A spelling-only arbiter has no access to
intent; a corpus-attestation arbiter conflates "rare" with "wrong" and is blind to the
editorial apparatus that makes a scholarly lexicon what it is. The entry body resolves
both: it states the etymology, gives the inflection, quotes the citation, and labels
its own apparatus. The precision jump — from 0.20 % on a spelling-only MW list to a
clean, evidence-backed proposal queue plus a 2,297-entry suppression catalogue — is
attributable to the change of arbiter, not to model size (the deterministic marker
layer, which is model-independent, settles most apparatus before any model runs; and
the collision class shows entry-reading catching what even confirmed-typo lists miss).

**The do-not-file catalogue is the real product.** On mature dictionaries the absolute
number of recoverable typos is tiny and not worth a campaign; the catalogue of
documented-intentional spellings is the lasting asset, because it actively *prevents
harm* — a guard rail against well-meaning bulk "corrections" that would corrupt a
century-corrected edition. Section 4.7 puts a number on that harm: the union of
the underlying detectors recovers 99 % of the genuine corrections *and* all 13
protected rows, so precision and harm rise together, and it is the protection
layer, not the detector, that makes the queue safe to act on. This is the paper's
inversion: the spell-checking campaign's most valuable output is the list of
things it must never touch.

**Fileable rate as a digitisation-quality signal.** The strong concentration of typos
in SHS/YAT/ACC, and their near-absence in MW/PW/VCP, means the fileable rate doubles as
a proxy for how well-corrected a source already is — a cheap triage signal for which
digitisations still need attention.

## 6. Limitations

- **The LLM typo pass is stochastic** (§3.4): the 122 figure is a floor under
  union-across-runs, not a point estimate. The do-not-file catalogue does not share
  this instability (deterministic marker backbone; `eval.py` harness).
- **The reliability number is model-vs-model, not human IRR.** §4.6 reports a blind
  second-annotator study (κ = 0.336 five-way; 99.2 % binary defect recognition), but
  both annotators are language models of different tiers under different prompts.
  What it measures is the **reproducibility of the method from the evidence alone** —
  whether the taxonomy can be re-derived blind from the entry bodies — plus an
  incidental convergence with the human editor's audit on the five weak SHS rows. It
  does not measure agreement with an independent human expert, which remains future
  work (the recruit is deferred; tracked in the project GTD). The κ was computed once,
  on the first blind run, and reported as obtained — the second annotator's prompt was
  not iterated toward agreement. Both figures (κ = 0.336 five-way; 121/122 raw binary
  agreement — the binary κ is not printed, see §4.6) are
  LLM-only inter-rater comparisons — soon two model *families*, once the pending
  cross-family run of §4.6 completes — and are not yet licensed against an
  independent human-labelled seed set; that outstanding gap is tracked explicitly in
  [`corrections_draft/irr/HUMAN_ANCHOR_NEEDED.md`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/irr/HUMAN_ANCHOR_NEEDED.md).
- **Queues decay.** ~0.8 %/week against the live, actively corrected `csl-orig`
  (measured over the triage→verification interval); all counts carry their as-of
  dates, and filing must re-verify against the live source.
- **PD external source.** PD is read from a staged external source, not `csl-orig`,
  and was triaged on its first source only (0 fileable, 116 do-not-file); a second
  source is expected and would only refine the do-not-file list.
- **The scan is the final, irreducible arbiter.** The LLM/human entry-reading layer
  is a prior; b/v and similar cases must be confirmed on the scanned page before
  filing — seventeen rows are explicitly held at SCAN-FIRST, plus YAT's ~32-row b/v
  cluster (§4.4).

## 7. Conclusion

On mature digitised dictionaries, spelling-anomaly detection collapses to near-zero
precision (MW 0.20 %), and no amount of better spelling statistics escapes it, because
the information that distinguishes a typo from an intentional variant is not in the
headword. It is in the entry. A staged pipeline — classify, confirm against the entry
body, re-verify, human-verify — recovers the genuine errors where they concentrate
(poorly-digitised sources such as SHS at ≈15 % and YAT at ≈11 %), exposes the
collision class no headword-level check can see, and, more durably, produces a
2,297-entry do-not-file catalogue (2,549 gross) that prevents damaging bulk
corrections across the Cologne corpus. The reusable result is methodological: the
dictionary body, not spelling or corpus frequency, is the reliable ground truth for
typo-vs-variant.

## Appendix A — pipeline operational detail

The per-dictionary run is driven by the
[`/dict-triage <DICT>`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/.claude/commands/dict-triage.md) skill over
[`detectors/triage_*.py`](../detectors/) and
[`detectors/bodyaware_workflow.js`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/bodyaware_workflow.js). Each run
emits `<DICT>_file_first_sf.txt` (the proposal queue in the CORRECTIONS standard
format) and `<DICT>_wrong_readings.txt` (the do-not-file list with per-class
sections); see [`corrections_draft/<DICT>/`](../corrections_draft/). The 2026-07-02
re-verification reused `triage_util.EntryIndex` for entry location and emitted
[`corrections_draft/file_first_verified.tsv`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/file_first_verified.tsv).

## Data and reproducibility

The 33-dictionary triage index and per-dictionary status table live in
[`corrections_draft/README.md`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/README.md); the re-verification
record in [`corrections_draft/VERIFICATION_2026_07.md`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/VERIFICATION_2026_07.md)
and [`file_first_verified.tsv`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/file_first_verified.tsv). The
deduplicated suppression artefact is
[`nochange/do_not_file_suppress.txt`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/nochange/do_not_file_suppress.txt),
regenerated with `cd detectors && python gen_do_not_file_suppress.py`; its safety
harness is [`detectors/eval.py`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/eval.py) (0 false positives vs ~31k
known-good headwords; recall vs the 3,884 historical pairs); the same script
reproduces the §4.7 detection-level table (F0.5 + harm rate) against
[`detectors/gold_corrections.tsv`](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/gold_corrections.tsv). To re-verify the
headline figures: the gross do-not-file total is the sum of the per-dict section
counts in the wrong-readings files (**2,549**); the deduped union is the suppress
file's data-row count (**2,297**); the confirmed totals are the data rows of each
`*_file_first_sf.txt` (**122** across 11 dicts, as of triage — the queue files are
living artefacts and held **178** data rows as of 04-09-2026; the frozen triage-era
frame is the `file_first_verified.tsv` verdict rows, not the live queues) and the verdict rows of
`file_first_verified.tsv` (92/17/11/1/1, as of 2026-07-02, including the editor's
same-day PASS→SCAN-FIRST audit of five SHS rows); the agreement study's artefacts are
`corrections_draft/irr/` (blind second annotations, exact-arithmetic κ, disagreement
taxonomy) with `detectors/irr_build_inputs.py` + `detectors/irr_agreement.py` as the
reproducing scripts; MW precision is
**4 / 1,954 = 0.20 %**. The work never edits `csl-orig`; confirmed corrections are
reported to the separate CORRECTIONS workflow
([umbrella issue #447](https://github.com/sanskrit-lexicon/CORRECTIONS/issues/447)).

## References *(every URL resolved and title/author-checked 12-07-2026; final human spot-check before submission)*

- Artstein, R., & Poesio, M. (2008). Survey Article: Inter-Coder Agreement for
  Computational Linguistics. *Computational Linguistics*, 34(4), 555–596.
  [https://aclanthology.org/J08-4004/](https://aclanthology.org/J08-4004/).
- Bloodgood, M., & Strauss, B. (2016). Data Cleaning for XML Electronic
  Dictionaries via Statistical Anomaly Detection. *Proceedings of the 2016 IEEE
  Tenth International Conference on Semantic Computing (ICSC)*.
  [https://arxiv.org/abs/1602.07807](https://arxiv.org/abs/1602.07807).
- Bryant, C., Felice, M., & Briscoe, T. (2017). Automatic Annotation and
  Evaluation of Error Types for Grammatical Error Correction. *Proceedings of the
  55th Annual Meeting of the Association for Computational Linguistics (Volume 1:
  Long Papers)*. [https://aclanthology.org/P17-1074/](https://aclanthology.org/P17-1074/).
- Golding, A. R., & Roth, D. (1999). A Winnow-Based Approach to Context-Sensitive
  Spelling Correction. *Machine Learning*, 34(1–3).
  [https://arxiv.org/abs/cs/9811003](https://arxiv.org/abs/cs/9811003).
- Grundkiewicz, R., Junczys-Dowmunt, M., & Gillian, E. (2015). Human Evaluation of
  Grammatical Error Correction Systems. *Proceedings of the 2015 Conference on
  Empirical Methods in Natural Language Processing (EMNLP)*.
  [https://aclanthology.org/D15-1052/](https://aclanthology.org/D15-1052/).
- Hollenstein, N., Schneider, N., & Webber, B. (2016). Inconsistency Detection in
  Semantic Annotation. *Proceedings of the Tenth International Conference on
  Language Resources and Evaluation (LREC 2016)*.
  [https://aclanthology.org/L16-1629/](https://aclanthology.org/L16-1629/).
- Kanerva, J., Ledins, C., Käpyaho, S., & Ginter, F. (2025). OCR Error
  Post-Correction with LLMs in Historical Documents: No Free Lunches. *Proceedings
  of the RESOURCEFUL 2025 Workshop*.
  [https://arxiv.org/abs/2502.01205](https://arxiv.org/abs/2502.01205).
- Karamolegkou, A., Angleraud, N., Sagot, B., & Clérice, T. (2026). Reading or
  Guessing? Visual Grounding Failures of Vision-Language Models for OCR in Ancient
  Greek Editions. arXiv:2605.27750.
  [https://arxiv.org/abs/2605.27750](https://arxiv.org/abs/2605.27750).
- Mondaca, F., & Rau, F. (2020). Transforming the Cologne Digital Sanskrit
  Dictionaries into OntoLex-Lemon. *Proceedings of the 7th Workshop on Linked Data
  in Linguistics (LDL-2020)*.
  [https://aclanthology.org/2020.ldl-1.2/](https://aclanthology.org/2020.ldl-1.2/).
- Patel, D. K., & Kulkarni, A. (2024). Word Sense Alignment of Sanskrit Lexica.
  *Proceedings of the 7th International Sanskrit Computational Linguistics
  Symposium (ISCLS 2024)*.
  [https://aclanthology.org/2024.iscls-1.1/](https://aclanthology.org/2024.iscls-1.1/).
- Piotrowski, M. (2012). *Natural Language Processing for Historical Texts*. Morgan &
  Claypool.
- Plank, B. (2022). The "Problem" of Human Label Variation: On Ground Truth in
  Data, Modeling and Evaluation. *Proceedings of the 2022 Conference on Empirical
  Methods in Natural Language Processing (EMNLP)*.
  [https://aclanthology.org/2022.emnlp-main.731/](https://aclanthology.org/2022.emnlp-main.731/).
- Prasanna, S. (2022). Spellchecker for Sanskrit: The Road Less Taken. *Proceedings
  of the 19th International Conference on Natural Language Processing (ICON 2022)*,
  290–299. [https://aclanthology.org/2022.icon-main.35/](https://aclanthology.org/2022.icon-main.35/).
  *(Verified 10-07-2026 by the H452 prior-art scan; replaces the earlier "ISCLS 2024
  contextual spellchecker" placeholder — that volume contains no spellchecking paper.
  See [docs/PRIOR_ART.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/PRIOR_ART.md).)*
- Rei, M., & Yannakoudakis, H. (2016). Compositional Sequence Labeling Models for
  Error Detection in Learner Writing. *Proceedings of the 54th Annual Meeting of
  the Association for Computational Linguistics (Volume 1: Long Papers)*.
  [https://aclanthology.org/P16-1112/](https://aclanthology.org/P16-1112/).
- Tseng, Y.-H., Lee, L.-H., Chang, L.-P., & Chen, H.-H. (2015). Introduction to
  SIGHAN 2015 Bake-off for Chinese Spelling Check. *Proceedings of the Eighth
  SIGHAN Workshop on Chinese Language Processing*.
  [https://aclanthology.org/W15-3106/](https://aclanthology.org/W15-3106/).

*(Removed 12-07-2026: the draft's former entry "ISCLS (2026). Preserving what is
written, not what is expected…" could not be verified — the published ISCLS 2026
proceedings ([https://aclanthology.org/volumes/2026.iscls-1/](https://aclanthology.org/volumes/2026.iscls-1/))
contain no such paper. The over-correction claim it supported is now grounded in
Karamolegkou et al. (2026) and Kanerva et al. (2025) plus this project's own
observation; see §2(b).)*

_Dr. Mārcis Gasūns_
