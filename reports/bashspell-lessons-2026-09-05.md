# What SanskritSpellCheck can learn from bashspell — and the DH-stack program it minted

_Created: 05-09-2026 · Last updated: 05-09-2026_

Study of [AigizK/bashspell](https://github.com/AigizK/bashspell) (Bashkir Hunspell
spellchecker; 72 commits, actively developed — its morphology tab landed the same day this
was written) for what transfers to a Sanskrit spellchecker and morphological analysis.
Provenance: analysis session 05-09-2026, GLM 5.3 Flash (OxAlpha lane); scope ruled by MG
in chat the same day — deeper research first, then **full DH stack** adoption as a
4-lane program.

## What bashspell is

Two halves:

1. A classic Hunspell CLI wrapper (`bash.aff`/`bash.dic`, dated dictionary versions,
   [`test --valid/--invalid` regression files](https://github.com/AigizK/bashspell/blob/main/README.md),
   exit codes 0/1/2, `--json`).
2. The interesting half — a
   [custom Python rule-chain walker](https://github.com/AigizK/bashspell/blob/main/bashspell_morphology.py)
   that reads the same aff/dic but ignores Hunspell's two-suffix-stage limit, returning
   **all** full parses: stem + POS + morph-by-morph parts + grammar tags + sound changes,
   with unlimited rule-chain depth.

## The transferable lessons

## 1. Full-parse walker replaces a weak analyzer gate

Our vidyut morphological-analyzer gate (ROADMAP Phase 3.2) found only ~6.6% of dictionary
headwords are pratipadikas, and an inflected suspect (`rAjA`) looks non-stem — an
informational ranking signal, not a gate. bashspell's walker answers exactly this shape of
problem: walk inflected surface → stem + tags + parts, no stage limit. A Sanskrit analog
walker over vidyut stems + csl-inflect endings + internal-sandhi rules would turn `morph✓`
from a nudge into a real parse.

## 2. Anti-hallucination discipline (the best part)

1. Split bundled morphemes **only at boundaries proven by independent rules of the same
   class**; ambiguous boundaries stay grouped — *never invent morphemes*. Directly the
   right stance for samāsa segmentation.
2. Alternations are attributed to the boundary with an explicit `changes[]` field
   (`китап+ы → китаб+ы` shown next to the split) — Sanskrit analog: every internal-sandhi
   edit (guṇa/vṛddhi, n→ṇ, s→ṣ) explained at its juncture, never hidden.
3. Work budgets (30k search states / 5k paths / 256-char input) end in an explicit error —
   never a truncated parse list presented as complete. Sanskrit compounds explode
   combinatorially; this is the guard.

## 3. The grammar-audit methodology (most transferable asset)

[`tools/audit_grammar_reference.py`](https://github.com/AigizK/bashspell/blob/main/tools/audit_grammar_reference.py)
crawls **all** archived grammar pages (452), extracts italicized example words, checks each
against the dictionary, and emits: per-page `pages.tsv` (examples/accepted/rejected/sha256),
`scan.json` (every verdict + SHA-256 of pages *and* dictionaries), and
`review-candidates.tsv` of rejects with source-page links. Results from their audit
([report](https://github.com/AigizK/bashspell/blob/main/reports/grammar-audit-2026-09-05.md)):
14,239 unique examples, 82 rejected→accepted flips, 12 accepted→rejected flips, each flip
individually context-checked and logged in `changed-examples.tsv`.

The epistemic framing is the point: *"candidates for linguistic review, NOT automatically
valid test cases"* — the reference also italicizes translations, transcriptions, historical
forms, and deliberately wrong spellings, so 1,461 rejects ≠ 1,461 defects. This is our
"candidates, never silent auto-fixes" principle operationalized at grammar-book scale.

Sanskrit analog: crawl csl-kale / Whitney / Elizarenkova / Kochergina grammar material,
extract examples, check against sanhw1 + MW/PW/VCP + a vidyut parse vote, emit the same
triple of artifacts, human-context-check the rejects, promote confirmed ones into `+`/`−`
regression files. **This is Lane A of the program below** — minted same-day as
[H4154](https://github.com/gasyoun/Uprava/blob/main/handoffs/H4154-OxAlpha_SanskritSpellCheck_grammar-example-audit-prototype_05.09.26.md).

## 4. Derived-data discipline

[`tools/complete_hunspell_paradigms.py`](https://github.com/AigizK/bashspell/blob/main/tools/complete_hunspell_paradigms.py):

1. Hand-written rows stay the source; generated blocks carry BEGIN/END markers + a
   generated-count comment placed **after** the block (a comment inside a block silently
   truncates it — Hunspell counts physical lines; hard-won lesson worth stealing whole).
2. `--write`/`--check` idempotence gate returning 1 on staleness: CI-ready; `--check`
   verified in every audit run.
3. **Inverse paradigms computed from forward classes** (V25–V29 rebuilt from V09+),
   never hand-maintained — one source of truth; conditions apply to *dictionary* spelling
   before stripping; rules differing only in the final stem letter merged into `[class]`
   conditions without broadening. Same pattern guards any regenerated Sanskrit form
   dictionary (sanhw2/MWinflect-style).
4. Same-flag ambiguity resolved at generation time: `+Prc` disambiguated per formative
   (`+Prc/ған|асаҡ|ыр`) so distinct categories stop competing as allomorphs — the same
   conflation plagues coarse Sanskrit participle tags.
5. Strictness: any unfamiliar directive raises — the analyzer refuses partial loads.

## 5. Presentation layer

A web `/analyze` tab (FastAPI, LRU-256 cache, stale-response guard) with a legend of
grammatical labels **in the vernacular**. Estate analog: Russian tag explanations, serving
the SanskritRussian lane and kosha pedagogy morphology drills.

## What NOT to adopt

1. **Hunspell itself.** bashspell's own escape hatch proves the two-stage limit breaks for
   rich morphotactics; Sanskrit compounding + boundary sandhi exceed it far more. Keep the
   DCS-grounded `detectors/` approach; import only the walker pattern over Sanskrit
   lexicon data.
2. Complementarity note: our real error taxonomy (75% vowel length, aspiration, sibilant —
   classes that preserve the V/C skeleton) is an *orthography* problem the affix walker
   does not address. The walker adds morphology; it does not replace the detectors.

## The DH-stack program (MG ruling: full stack, 05-09-2026)

The DH dimensions settled alongside, sequenced so the scope lands as lanes, not one
mega-handoff:

| Lane | Content | Owner / effort | Status |
|---|---|---|---|
| A | Grammar-example audit prototype (§3): crawl → extract → check → pages.tsv/scan.json/review-candidates.tsv(.csv), register/period tags, SHA-256 manifests, IAA-ready two-pass review design | OxAlpha, ~3–5 h | [H4154](https://github.com/gasyoun/Uprava/blob/main/handoffs/H4154-OxAlpha_SanskritSpellCheck_grammar-example-audit-prototype_05.09.26.md) minted 05-09-2026 |
| B | This lessons doc + program map | OxAlpha, ~20 min | this file |
| C | OntoLex canonical-lemma groundwork: sanhw1 → canonical-lemma crosswalk (Patel-convention variants resolve once; ROADMAP 3.3, csl-atlas tie-in), OntoLex-Lemon JSON-LD + TEI Lex-0 dual serialization; rider: translation-alignment attestation via Parallel-Sanskrit-Corpora for `dict_vs_corpus` | Sonnet 5, judgment-heavy, ~6–10 h | mint pending — per-lane mint fence requires a Claude lane (GTD Agent-Ready row 05-09-2026) |
| D | IIIF image–text deep-links: IIIF Image API manifest builder from servepdf scans + region deep-links from review rows; blocker-tolerant (no local tesseract, server 429 → OCR optional, small batches) | OxAlpha, ~4–6 h | queued after Lane A (GTD Agent-Ready row 05-09-2026) |

Decisions owed / bookkeeping:

1. **License `@DECIDE` (MG)**: SanskritSpellCheck declares no license — a publication
   blocker for the citable-dataset goal only (proposal: data CC BY-SA 4.0, code per house
   pattern). GTD Waiting-on-Me row 05-09-2026. The audits themselves are not blocked.
2. With inter-annotator agreement (Cohen's κ) reported on the two-pass verified subset,
   Lane A's output becomes a **citable gold standard** (ROADMAP 3.4's released evaluation
   set) — Zenodo DOI release rides the license ruling; CITATION.cff update per release.
3. Deferred-by-design pointers (mentioned, not built here): CoNLL-U alignment with
   dcs-conllu for analyzer votes; IIIF (Lane D covers the link layer); full OntoLex layer
   beyond groundwork (Lane C boundary).

_Dr. Mārcis Gasūns_
