# Orthographic-Drift Roadmap

_Created: 17-06-2026 · Last updated: 04-07-2026_

**Status: ✅ COMPLETE across all 5 gloss languages** (changelog `[1.20.0]`–`[1.30.0]`). This
document is the original **design**; the implementation (`detectors/ortho_drift.py`, profile-driven
de/en/fr/la/ru), the per-language outputs in `ortho_drift/`, and the synthesis are all done — read
the results in **[docs/ORTHO_DRIFT_FINDINGS.md](docs/ORTHO_DRIFT_FINDINGS.md)**. Nothing here edits
`csl-orig`. *Optional, externally-gated extensions remain* (within-EN recency control over the
modern dicts incl. PD; German DTA/RIDGES long-tail merge) — see Task C in
[H008-Opus_SanskritSpellCheck_NEXT_23.06.26.md](H008-Opus_SanskritSpellCheck_NEXT_23.06.26.md).
**Scope:** a new dimension for the body-grounded triage — check the **gloss-language tokens
inside dictionary entries** against a **2026 standard**, and document, at meta level, how
19th-/early-20th-century European-language spelling has drifted.

> Companion to the headword triage ([corrections_draft/README.md](corrections_draft/README.md),
> recipes in [USE_CASES.md](USE_CASES.md)). Same pipeline, new axis.

---

## 1. What & why

The headword triage (`detectors/triage_*.py`) judges a flagged **Sanskrit headword** against a
dictionary's own entry text. This study turns the lens on the **gloss language** — the German,
English, French, Latin or Russian prose in which each dictionary defines its headwords.

Each Cologne dictionary was written in its author's *contemporary* orthography: Wilson's 1832
English, Böhtlingk–Roth's 1850s–70s German, Burnouf's 1866 French. Orthographic standards have
since moved — in some languages by **legislated reform**, in others by **convention drift**. So
the gloss text is a dated artifact, and the gap between it and a 2026 standard is:

1. a **search-normalization** problem (a user searching modern German "Tier" misses Böhtlingk's
   "Thier"); and
2. a **historical-linguistics dataset** — a measurable record of orthographic change across ~13
   decades and 5 languages, in a single uniformly-marked-up corpus.

The decisive insight: **the period orthography lives in the gloss language, not in the Sanskrit**,
and Cologne markup already separates the two — Sanskrit is wrapped in `{#…#}` (SLP1) / `{@…@}`
(other transliteration), so the gloss-language running text is what falls *outside* those spans.

---

## 2. The corpus (what we actually have)

From the 18 dictionaries already triaged for headwords, the gloss-language × era map:

| gloss language | dictionaries (era) | reform regime |
|---|---|---|
| **German** | PW · PWG (1855–75) · GRA (1873) · CCS (1887) — all **pre-1901**; SCH (1928) — **post-1901, pre-1996** | legislated, twice |
| **English** | WIL (1832) · GST (1856) · BEN (1866) · MW72 (1872) · CAE (1891) · MD (1893) · MW (1899) · SHS (1900) · AP90 (1890) · AP (mod.) | convention drift |
| **French** | BUR (Burnouf, 1866) · STC (Stchoupak–Nitti–Renou, 1932) | minor |
| **Latin** | BOP (Bopp, *Glossarium*, 1847) | ~stable |
| **Russian** | **external** — Kossovich (KOW, pre-1918) · Kochergina (mod.), in [SamudraManthanam](https://github.com/sanskrit-lexicon) (not the Cologne 33) | legislated (1918) |

The German and Russian sets are the scientifically cleanest, because their reforms are
**dated and rule-defined** — we can predict the expected drift and validate against it.

---

## 3. What changed, per language

> These are well-established facts to be **encoded as rule-sets in Phase 0** (and validated
> against the published reform documents during build — see Open decisions).

### German — legislated, twice
- **1901** (II. Orthographische Konferenz): dropped etymological `th` in German-origin words
  (`Thür→Tür`, `Theil→Teil`, `Thal→Tal`), `c→k/z` in many loans (`Capitel→Kapitel`),
  `giebt→gibt`, `-iren→-ieren`, `Litteratur→Literatur`.
- **1996/2004/2006**: `ß→ss` after a short vowel (`daß→dass`, `Fluß→Fluss`), some `ph→f`,
  compound/hyphen/comma rules.
- ⇒ **PW/PWG/GRA/CCS (pre-1901) should show heavy drift; SCH (1928) should show only the
  1996-era drift** — a built-in internal control.

### English — convention drift (no central authority)
- `connexion/inflexion/reflexion → -ction`; `shew→show`; `mediæval/æon → medieval/eon`
  (`æ/œ→e`); dropped diaeresis (`coördinate→coordinate`); Victorian `-ise/-ize` variation;
  archaic past forms. No single reform date — a *gradient*, which makes English the **hardest**
  (drift vs. genuine error vs. valid British variant all overlap).

### French — minor
- pre-1935 Académie (8th ed.) spellings; the 1990 *rectifications orthographiques* (accents,
  some hyphens/plurals). BUR (1866) and STC (1932) differ only lightly from 2026.

### Latin — ~stable
- Bopp's *Glossarium* (1847) Latin is orthographically close to modern Latin convention.
  **Low priority** — likely a near-null result; useful mainly as a negative control.

### Russian — legislated (1918), the most dramatic
- The 1918 reform dropped word-final ъ (hard sign), and the letters і→и, ѣ (yat)→е,
  ѳ (fita)→ф, ѵ (izhitsa)→и. ⇒ a **pre-1918 dictionary (Kossovich) will differ massively** from
  a modern one (Kochergina). The richest drift signal in the corpus — but the sources live in
  SamudraManthanam, not Cologne.

---

## 4. Method — one new axis on the existing pipeline

Reuse the headword architecture; add a gloss dimension.

1. **Extract gloss tokens.** Reuse `triage_util.build_entry_index` for entry bodies; add a
   gloss tokenizer that strips the Sanskrit spans (`{#…#}`, `{@…@}`) and source/italic markup
   (`{%…%}` — used for italics, headword echoes, and source sigla, so handle with care) and
   emits the remaining European-language word tokens.
2. **Check vs a 2026 reference.** A token absent from a pinned modern **Hunspell** dictionary
   (+ SCOWL for English) is a *candidate*.
3. **Classify each candidate** (Sonnet, body-aware — mirrors the headword `classify` phase):
   - **reform-drift** — correct for its era, spelled differently in 2026 (apply the per-language
     reform rule-set to recognise these, e.g. `Thier`→`Tier`);
   - **OCR / digitization error** — wrong in *both* the historical and modern standard;
   - **proper noun** — names (German nouns are capitalised, so capitalisation alone won't do —
     needs a gazetteer/NER pass; proper nouns will dominate the raw candidate set);
   - **abbreviation / source siglum** — `Mahābh.`, `ŚKDR.`, `s. u.`, etc.;
   - **archaic-but-still-valid** — attested historical variant not changed by any reform.
4. **(Optional, only if a correction list is ever sanctioned)** Opus confirm + Opus review of
   the OCR-error subset, exactly as the headword pipeline does today.

Models: hybrid as now — **Sonnet classify / Opus confirm-review** (`bodyaware_workflow.js`
gains an `ortho` mode, or a sibling `ortho_workflow.js`). Language config lives in a module
parallel to [`detectors/triage_lang.py`](detectors/triage_lang.py) (per-language reference +
reform rule-set), registered the same single-line way `_LANG` is.

---

## 5. Output — a drift report, not corrections

Per dictionary, an **orthographic-drift report**:

```
historical_form    2026_form        count   category            example_entry
Thier              Tier             214     reform:1901-th        {#mfga#} das wilde Thier
giebt              gibt              88      reform:1901-ie        ... giebt es ...
connexion          connection       31      drift:xion            in connexion with ...
<ocr-garble>       —                12       ocr-error             ...
```

…plus a per-dictionary **meta summary** ("PW: pre-1901 German throughout; N% of gloss tokens
differ from 2026 Duden; dominant patterns Th→T, c→k, -iren→-ieren") and, across dictionaries, a
**timeline of indological-lexicography orthography** (drift-rate by publication year × language)
— the citable historical-linguistics artifact.

Outputs live beside the triage packages (e.g. `corrections_draft/<DICT>/<DICT>_ortho_drift.txt`)
or a dedicated `ortho_drift/` tree.

---

## 6. Guardrail (non-negotiable)

This is a **documentation / search-normalization layer, NOT a correction list.** Modernising a
historical gloss would corrupt the scholarly edition — the same principle as the headword
[do-not-file lists](corrections_draft/README.md). It produces a *report* + a *normalization map*
(for search), and **never edits `csl-orig`**.

It **could** graduate into a correction layer one day — but only for genuine OCR errors (never
reform-drift), and only behind an **explicit human sign-off gate**, exactly like the FILE-FIRST
queue. Until then: read-only documentation.

---

## 7. Phases & milestones

| phase | scope | why this order |
|---|---|---|
| **0 — scaffold** | gloss tokenizer; pin the 2026 Hunspell/SCOWL snapshots; encode the **German 1901 + 1996 rule-sets**; proper-noun handling | German is the cleanest validation target |
| **1 — German pilot** | **PW vs 2026 Duden/Hunspell** first, then PWG/GRA/CCS/SCH | legislated reform ⇒ predict-and-validate; SCH (1928) is the internal control (should show *less* drift than PW) |
| **2 — English** | the 10 English dicts (WIL→MW) with VARD2 + a Victorian-variant lexicon | hardest (gradient, no rules); do after the German method is proven |
| **3 — French / Latin / Russian** | BUR+STC (French), BOP (Latin, control), **Kossovich vs Kochergina (Russian, 1918)** from SamudraManthanam | rounds out the corpus; Russian is the dramatic finale |
| **4 — synthesis** | cross-dict timeline + the meta-level artifact / write-up | the publishable output |

Start small: **Phase 0 + the PW-vs-Duden pilot** is the minimum viable slice and validates the
whole approach against the one language whose reform is fully rule-defined.

---

## 8. Open decisions (need a human)

1. **What pins "2026"?** A specific Hunspell `de_DE`/`en_GB`/`en_US`/`fr_FR` release + Duden
   edition + SCOWL version, recorded for reproducibility.
2. **Proper-noun strategy** — gazetteer, NER, or accept them as a labelled bucket? They will be
   the largest candidate class and the main false-positive source.
3. **Russian source access** — wire Kossovich/Kochergina from SamudraManthanam (`build_src.py`
   already emits `kow.jsonl`/`koch.jsonl`); confirm the path and licence.
4. **Correction-list graduation** — do we ever want the OCR-error subset to become a sign-off-
   gated correction queue, or stay purely documentary?
5. **Coverage** — all body tokens, or a sampled / frequency-thresholded subset (full bodies are
   far more tokens than the one-headword-per-entry the current pipeline handles).

---

## 9. Prior art — reuse, don't reinvent

| need | reuse |
|---|---|
| 2026 word-lists | **Hunspell** `de_DE`/`en_GB`/`en_US`/`fr_FR` (LibreOffice/Mozilla) + **SCOWL** (English) |
| German reform rules | published **1901** + **1996/2004/2006** rule-sets; [Deutsches Textarchiv (DTA)](https://www.deutschestextarchiv.de/) / **RIDGES** historical-normalization resources |
| German historical normalization | **Norma** / **CAB** (cascaded analysis broker) |
| English historical normalization | **VARD2** (Lancaster — EModE/Victorian variant spelling) |
| Russian pre-1918 | the 1918-reform letter map (ъ/і/ѣ/ѳ/ѵ); Kossovich text from SamudraManthanam |

Historical-spelling normalization is a mature DH subfield — the contribution here is **applying
it to a uniformly-marked-up, multilingual indological-lexicography corpus** and producing the
cross-decade drift dataset, not building new normalizers.

_Dr. Mārcis Gasūns_
