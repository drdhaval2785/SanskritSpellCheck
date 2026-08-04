# Web spellchecker suggester — design spec

_Created: 12-07-2026 · Last updated: 12-07-2026_

Design spec for the **suggestion-generation engine** behind the Q1-2027 web spellchecker
app ([ROADMAP_2026_2027.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ROADMAP_2026_2027.md)
Q1 item 2; product ruling **D6**). Authored 12-07-2026 by Opus 4.8 (`claude-opus-4-8`) for
[H828](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H828-Fable_SanskritSpellCheck_web-suggester-spec-oflazer-vidyut_12.07.26.md)
— commissioned as a Fable 5 (`claude-fable-5`) design task per ruling **D1** (judgment gates);
executed at M.G.'s direction. **This is a specification, not an implementation** — the build is
deferred to post-30-06-2027 under ruling **D13** so it does not compete with the ≥300-corrections
north-star for effort. A future build session executes from this file.

The engine reuses assets already in this repo (the confusion model, DCS frequency bands, the
33-dictionary union headword list, the vendored vidyut stems, the do-not-file suppression list, and
the shared transcoders); it turns the two ACL-canonical algorithms named below into the missing
candidate-generation and ranking layers. Prior-art landscape:
[docs/PRIOR_ART.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/PRIOR_ART.md).

---

## 0. What this is and is not

- **Scope:** the algorithm + data + interface spec for a *flag-and-suggest* Sanskrit spellchecker —
  input a word (or running text), decide whether it is valid, and if not, return a **ranked list of
  correction suggestions** drawn from validated Sanskrit forms.
- **Not in scope (this handoff):** any code, the app repo, the client bundle, deployment. Those are
  the Q1-2027 build (ruling D13). Where a build decision is genuinely open, it is parked in §12.
- **The one-line thesis:** [PRIOR_ART.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/PRIOR_ART.md)
  found that *suggestion generation against a validated Sanskrit lexicon is essentially unoccupied
  territory* — the only flag-and-suggest tool is a dormant unlicensed demo. The ACL literature hands
  us the exact architecture to occupy it, and every data asset it needs already sits in this repo.

---

## 1. The opportunity, and the two algorithms that fill it

Three findings from the prior-art scan define the gap and how to fill it:

1. **Candidate generation is a solved problem in the FST literature — Oflazer 1996.**
   [Oflazer, "Error-tolerant Finite-State Recognition with Applications to Morphological Analysis
   and Spelling Correction" (Computational Linguistics 22:1, 1996, J96-1003)](https://aclanthology.org/J96-1003.pdf)
   enumerates *all* forms reachable in a lexicon automaton within edit distance `k`, using a
   **cut-off edit distance** to prune branches early so the traversal stays tractable even over a
   very large lexicon. This is precisely how you turn a *validator* (an FST that says yes/no) into a
   *suggestion generator* (an FST that says "no, but here are the nearby yeses"). We have two
   automata to traverse (§2.3): the **union headword trie** and the **Vidyut kosha FST**.

2. **Candidate ranking is a solved problem too — Brill & Moore 2000.**
   [Brill & Moore, "An Improved Error Model for Noisy Channel Spelling Correction" (ACL 2000,
   P00-1037)](https://aclanthology.org/P00-1037/) replaces single-character Levenshtein with
   **generic string→string edits** (α → β over substrings), which is what captures Sanskrit's real
   error modes: transliteration digraphs (`ri` ↔ `f`), retroflex/dental swaps, aspiration, sibilant
   confusion, post-repha gemination, sandhi-boundary noise. The repo already measures the
   single-character version of this channel
   ([detectors/confusion_weights.json](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/confusion_weights.json));
   Brill-Moore is its multi-substring generalization.

3. **The whole cascade has a morphologically-rich precedent.** The winning
   [QALB Arabic shared-task](https://aclanthology.org/W14-3605/) systems
   ([QCMUQ, W15-3217](https://aclanthology.org/W15-3217/)) were hybrid morph-analyzer + character-MT +
   error-tolerant-FST cascades — exactly the shape below. Arabic, like Sanskrit, is morphologically
   rich with a productive derivational system; that these cascades won there is the external evidence
   that the shape transfers.

The result is a **noisy-channel spellchecker**: `argmax_w P(w | x) ∝ P(x | w) · P(w)`, where the
channel `P(x | w)` is Brill-Moore, the prior `P(w)` is DCS corpus frequency, and the candidate set
`{w}` is produced by Oflazer traversal of validated Sanskrit forms.

---

## 2. Architecture

### 2.0 Pipeline overview

```
             ┌────────────────────────────────────────────────────────────────┐
  raw input  │  SLP1 / IAST / Devanāgarī  (single word OR running text)        │
─────────────┼────────────────────────────────────────────────────────────────┤
   §2.1  →   │  NORMALIZE     sanskrit-util  ·  {IAST, Devanāgarī} → SLP1       │
             │                (running text → tokenize; optional sandhi split)  │
   §2.2  →   │  VALIDITY GATE is x ∈ (union HW ∪ vidyut kosha ∪ DCS ∪ accept)?  │
             │                ├─ yes → VALID, emit nothing (green)              │
             │                └─ no  → continue                                 │
   §2.3  →   │  CANDIDATES    Oflazer error-tolerant traversal, edit dist ≤ k   │
             │                over  (a) union-headword trie                     │
             │                      (b) Vidyut kosha FST  (validator→generator) │
   §2.4  →   │  RANK          P(x|w) Brill-Moore channel  ×  P(w) DCS prior     │
             │                       ×  measured confusion weights              │
   §2.5  →   │  SUPPRESS      variant-aware accept-list (do-not-file ∪ nochange)│
             │                drop any suggestion that is itself a known variant │
   §2.6  →   │  OUTPUT        ranked suggestions + confidence + provenance      │
             └────────────────────────────────────────────────────────────────┘
```

### 2.1 Input normalization layer

- **Accept SLP1, IAST, and Devanāgarī**; convert everything to **SLP1** internally (the repo's
  invariant — all Sanskrit text is SLP1). Conversion goes through the shared **sanskrit-util**
  package, already wired into this repo as
  [detectors/sanskrit_util.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/main/detectors/sanskrit_util.py)
  (a thin shim re-exporting `to_slp1`, `deva_to_slp1`, `deva_to_iast`, …). Do **not** vendor a
  transcoder; consume the package (this is also the Q1 PyPI package's rule).
- **Scheme detection:** if the input carries Devanāgarī codepoints → Devanāgarī; else if it carries
  IAST diacritics (`ā ī ū ṛ ṝ ḷ ṃ ḥ ṅ ñ ṭ ḍ ṇ ś ṣ`) → IAST; else assume SLP1. Offer an explicit
  scheme selector in the UI as an override — heuristic detection is ambiguous for ASCII-only input
  (`deva` is valid SLP1 *and* valid Harvard-Kyoto).
- **Known transcoder gotcha (must carry into the build):** Devanāgarī `ळ` (retroflex l-bar) must go
  through the package's **direct** `deva_to_slp1` (→ `L`), never `to_slp1(deva_to_iast(·))`, which
  mis-maps `ळ` onto vocalic ḷ → `x` because both share the IAST glyph ḷ (U+1E37). This bug is
  documented at [detectors/slp1util.py:146](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/slp1util.py)
  (`devanagari_to_slp1`) and in memory as the `sanskrit-util` `devanagari_to_slp1 ळ→x` caveat.
- **Running text** (paste-a-paragraph mode): tokenize on whitespace + daṇḍa (`।` `॥`); each token is
  checked independently. Optional sandhi/compound split via `vidyut-cheda` (already the meter
  pipeline's word→headword bridge) is a **phase-2 enhancement**, not v1 — v1 checks surface tokens
  and lets the user split manually, mirroring Prasanna's design.

### 2.2 Validity gate

A token is **valid** (emit no suggestion) if, after normalization, it is a member of any of:

| Oracle | Asset (in-repo) | Size | What membership means |
|---|---|---|---|
| Attested headword | [sanhw1.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/sanhw1.txt) union | 431,596 | ≥1 of 33 CDSL dictionaries attests this exact spelling |
| Morphological stem | [detectors/vidyut_stems.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/vidyut_stems.txt) | 205,233 | a Vidyut pratipadika (nominal stem) |
| Corpus lemma | [detectors/dcs_lemma_summary.json](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/dcs_lemma_summary.json) | ~83k | attested in the DCS corpus (with a frequency band) |
| Accept-list (variant) | [nochange/nochange.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/nochange/nochange.txt) ∪ [nochange/do_not_file_suppress.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/nochange/do_not_file_suppress.txt) | 30,887 + 2,297 | human-confirmed-correct, or a variant a dictionary documents *on purpose* |

The union of these four is the **acceptance lexicon** `L`. Loaders already exist:
`slp1util.load_lexicon`, `load_vidyut_stems`, `load_dcs_lemmas`, `load_whitelist`
([detectors/slp1util.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/slp1util.py)).
Membership is `O(1)` (hash sets) — no traversal needed for the valid case, which is the common case.

> **Why a full-form set, not stem+morphology, for v1.** `sanhw1.txt` is a headword (stem) list,
> so an *inflected* surface form (e.g. `devasya`) is not in it and would be flagged. v1 accepts this
> limitation and documents it: the DCS lemma set + Vidyut kosha (which is inflection-aware) cover
> much of the gap, and full inflected-form validation is the phase-2 `vidyut-prakriya` / `vidyut-cheda`
> path (§12 open question O3). Prasanna's tool has the same surface-form limitation.

### 2.3 Candidate generation — Oflazer error-tolerant traversal

This is **the core new algorithm** and the main build task. The repo today generates candidates only
by a single-substitution confusion neighbourhood (`slp1util.confusion_candidates`, effectively
edit-distance-1, confusion-pairs-only). Oflazer replaces that with a general edit-distance-`k`
traversal of a lexicon automaton.

**Two automata, unioned:**

- **(a) Union-headword trie/DAWG** built from the 431,596 `sanhw1.txt` headwords. Traversing it
  error-tolerantly yields *attested dictionary spellings* within edit distance `k` of the input —
  the "which real dictionary word did they mean" answer. Build a compact double-array trie or a
  minimized DAWG (see §6 for client packaging).
- **(b) Vidyut kosha FST.** [Vidyut](https://github.com/ambuda-org/vidyut) (`vidyut-kosha`, MIT) is
  itself a finite-state lexicon; error-tolerant traversal of it yields *grammatically generable*
  forms even when they are not headwords. This is the step that **turns Vidyut from a validator into
  a suggestion generator** — the handoff's central idea. The vendored
  [detectors/vidyut_stems.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/vidyut_stems.txt)
  (built by [detectors/gen_vidyut_stems.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/gen_vidyut_stems.py))
  is the stem inventory; a build session either (i) traverses the kosha FST directly via the
  `vidyut` Python/Rust API (server-side), or (ii) traverses a trie built from the vendored stem list
  (client-side, no runtime Vidyut dependency — mirrors how the stems are already vendored). Prefer
  (ii) for the client bundle, (i) for a serverless suggest endpoint.

**Oflazer cut-off edit distance (the pruning that makes it tractable).** Walk the automaton
depth-first. At each node, the path from the root spells a prefix `p` of a candidate word; maintain
the row of the Levenshtein matrix between the input `x` and `p`. The **cut-off distance** at that
node is the minimum value in the current matrix row restricted to a diagonal band of width `2k+1`
(the "H" of Oflazer §4). If that minimum exceeds the threshold `t`, **no descendant can finish
within edit distance `t`**, so prune the entire subtree. On reaching a final (word-accepting) state
with row-final value ≤ `t`, emit the word with its exact edit distance. Sketch:

```
traverse(node, prefix_row):
    for (edge_char, child) in node.edges:
        new_row = levenshtein_advance(prev=prefix_row, input=x, added_char=edge_char)
        if min(banded(new_row)) > t:        # cut-off: whole subtree is too far
            continue
        if child.is_final and new_row[-1] <= t:
            emit(word=child.word, dist=new_row[-1])
        traverse(child, new_row)
```

- **Threshold `t = k`** (a small integer). **Default `k = 2`**; degrade to `k = 1` for long inputs
  (`len > 12`) to bound the candidate set, and allow `k = 1` "fast mode" in the UI. `k` is a tunable
  in a config block, not hard-coded.
- **Weighted variant (preferred).** Plain Levenshtein `t` treats all edits as cost 1. Because we
  have a *measured* channel (§2.4), the traversal should prune on **channel cost**, not raw edit
  count: an edit-distance-2 candidate reachable by two high-probability confusion edits (e.g. two
  vowel-length swaps) should survive where an edit-distance-1 candidate reachable only by an
  improbable edit is cut. This is the natural marriage of Oflazer (traversal + pruning) and
  Brill-Moore (edit weights): the cut-off compares the *accumulated channel cost* against a
  probability floor. v1 may ship the unweighted form first and add channel-weighted pruning as a
  fast follow — record which was shipped.
- **Seed the traversal with the existing confusion neighbourhood.** `confusion_candidates(x)` (incl.
  the `f ↔ ri/ru` vocalic-r expansion) is a cheap, high-precision edit-distance-1 generator already
  in the repo; run it first and intersect with `L` for instant high-confidence hits, then fall
  through to full Oflazer traversal for the rest. This keeps the common single-typo case fast.

### 2.4 Candidate ranking — Brill-Moore channel × DCS prior × confusion weights

Rank each candidate `w` by the noisy-channel posterior `P(x | w) · P(w)`:

- **Channel `P(x | w)` — Brill & Moore string-edit model.** Partition `x` and `w` into aligned
  substrings and score `∏ P(β → α)` over the partition that maximizes the product (equivalently, sum
  of log-probabilities). The edit-probability table `P(β → α)` is **trained from aligned (wrong,
  right) pairs**, of which the repo already holds two sources:
  - the **3,884** human-curated single-letter confusion pairs in
    [o_vs_O/o_vs_O2.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/o_vs_O/o_vs_O2.txt)
    (already distilled to the 20-pair single-char table in
    [detectors/confusion_weights.json](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/confusion_weights.json)
    by [detectors/gen_confusion_weights.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/gen_confusion_weights.py));
  - the verified FILE-FIRST corrections
    ([corrections_draft/file_first_verified.tsv](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/file_first_verified.tsv))
    — real `wrong → right` pairs, which include multi-character edits the single-char table cannot
    express.

  The single-char `confusion_weights.json` is the **degenerate case** of the Brill-Moore table (all
  α, β length 1). The build extends it to substrings: it *must* cover at least the digraph/length
  edits Sanskrit needs — `ri↔f`, `rI↔F`, `ru↔f`, aspiration (`K↔k`), sibilant (`S↔s`, `z↔s`),
  retroflex↔dental (`w↔t`, `q↔d`, `R↔n`), `v↔b`, anusvāra/nasal (`M↔m`+homorganic), and post-repha
  gemination (`rgg↔rg`). `slp1util.confusion_weight(a, b, weights)` already scores a single-char
  edit; generalize it to a substring alignment.
- **Prior `P(w)` — DCS frequency band.** Reuse the exact mechanism in
  [detectors/spell_correct.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/spell_correct.py):
  `dcs.get(normalize_lemma(w))` gives a band `1..5` (1 = hapax … 5 = 1000+ occurrences); a
  band-5 correction outranks a band-1 correction. For headwords absent from DCS, fall back to a small
  floor prior scaled by **cross-dictionary attestation count** (how many of the 33 dicts carry `w`,
  read straight from the `sanhw1.txt` line) — a word in 20 dictionaries is a better guess than one in
  1. Never let a zero-frequency candidate outrank an attested one.
- **The combined score** is `log P(x|w) + λ · log P(w)`, `λ` a tunable blend weight. Return the
  top-N (default N = 5) by descending score, with the exact edit distance and the DCS band exposed
  as provenance (§2.6).

`detectors/spell_correct.py` is the **working prototype of this ranker** at edit-distance-1 scope:
it already suppresses DCS-attested inputs as real words, generates confusion neighbours, filters to
the trusted lexicon, and ranks by DCS band. The web suggester is `spell_correct.py` with (a) Oflazer
traversal replacing the single-substitution generator and (b) the Brill-Moore channel replacing the
binary confusion filter. **Start from that file.**

### 2.5 Suppression / accept-list layer — the variant-aware differentiator

Two distinct roles for the accept-list (`nochange.txt` ∪ `do_not_file_suppress.txt`):

1. **On the input side** (already in §2.2): if `x` is on the accept-list, it is a *documented
   variant, not a typo* — mark it valid, suggest nothing. This is the layer **no other tool has**:
   Hunspell packs hard-code one spelling as correct and flag every variant; the do-not-file catalogue
   (2,297 spellings a dictionary documents on purpose — `w.r.` apparatus, `v.l.`, in-composition and
   sandhi forms, cross-references, Vedic notes) encodes *variant ≠ error* as first-class data.
2. **On the suggestion side:** when ranking candidates for a genuinely-invalid `x`, do **not** offer
   a suggestion that is itself only an accept-list variant of another candidate — collapse
   variant-clusters so the user sees one canonical suggestion, not five spellings of the same word.

The list is regenerated by
[detectors/gen_do_not_file_suppress.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/gen_do_not_file_suppress.py)
from the per-dict `*_wrong_readings.txt` files as more dictionaries are triaged, so the accept-list
grows automatically with the correction work — the web app inherits every triage pass for free.

### 2.6 Output surface (UI contract)

For each flagged token, return a JSON record the UI renders:

```json
{
  "input": "SriNga",
  "scheme": "SLP1",
  "valid": false,
  "suggestions": [
    {"slp1": "SfNga", "iast": "śṛṅga", "devanagari": "शृङ्ग",
     "edit_distance": 1, "channel": "ri→f", "dcs_band": 4,
     "attested_in": ["MW","PW","VCP","AP90"], "score": -2.13}
  ]
}
```

- **Render suggestions in the user's input scheme** (SLP1 in → SLP1 out; Devanāgarī in → Devanāgarī
  out) via `slp-dev.php`/`dev-slp.php` equivalents or the sanskrit-util package, but always keep SLP1
  in the payload for copy/debug.
- **Show provenance** — which dictionaries attest the suggestion, its DCS band, and the edit that
  produced it. This provenance *is* the product's differentiator (evidence-based, not generative);
  surface it, do not hide it behind a bare list.
- **Interaction model** (from the proven Prasanna design, credited per §8): a paste box / editor,
  red-underline on flagged tokens, click or keyboard (Ctrl-Space) to reveal ranked suggestions.
  [OpenOCRCorrect](https://github.com/rohitsaluja22/OpenOCRCorrect) (BSD-3) is the reusable
  interactive-correction UI prior art to study before building the review surface from scratch.

---

## 3. Reuse map — what exists vs what to build

The design principle: **consume the repo's assets, build only the two ACL algorithms and the app.**

### 3.1 Already in-repo (reuse, do not rebuild)

| Need | Existing asset | Notes |
|---|---|---|
| SLP1/IAST/Devanāgarī → SLP1 | [detectors/sanskrit_util.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/main/detectors/sanskrit_util.py) → `sanskrit-util` pkg | shared package; `ळ→x` gotcha noted §2.1 |
| Attested-headword oracle | [sanhw1.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/sanhw1.txt) (431,596) + `slp1util.parse_sanhw1`/`load_lexicon` | also gives per-word dict-attestation count for the prior |
| Morphological-stem oracle | [detectors/vidyut_stems.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/vidyut_stems.txt) (205,233) + `slp1util.load_vidyut_stems` | vendored from Vidyut (MIT); the FST to traverse in §2.3(b) |
| Corpus-frequency prior | [detectors/dcs_lemma_summary.json](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/dcs_lemma_summary.json) + `slp1util.load_dcs_lemmas` | freq bands 1..5; DCS-2021 CC-BY |
| Single-char channel weights | [detectors/confusion_weights.json](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/confusion_weights.json) (20 pairs) + `slp1util.confusion_weight` | the degenerate case of the Brill-Moore table |
| Edit-distance-1 candidate seed | `slp1util.confusion_candidates` (incl. `f↔ri/ru`) | fast path before full traversal |
| Variant-aware accept-list | [nochange/nochange.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/nochange/nochange.txt) (30,887) + [nochange/do_not_file_suppress.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/nochange/do_not_file_suppress.txt) (2,297) + `slp1util.load_whitelist` | grows automatically as dicts are triaged |
| Ranker prototype | [detectors/spell_correct.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/spell_correct.py) | DCS-suppress + confusion-gen + band-rank at k=1; the starting point |
| Capped Levenshtein | `slp1util.edit_distance` (cap=3) | baseline distance; Oflazer supersedes for generation |
| Evaluation harness | [detectors/eval.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/eval.py) | recall vs 3,884 pairs; FP vs nochange — reuse for suggester eval (§7) |
| Aligned training pairs | [o_vs_O/o_vs_O2.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/o_vs_O/o_vs_O2.txt) (3,884) + [corrections_draft/file_first_verified.tsv](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/file_first_verified.tsv) | to train the Brill-Moore table |
| Interactive-correction UI prior art | [OpenOCRCorrect](https://github.com/rohitsaluja22/OpenOCRCorrect) (BSD-3) | study before building the review surface |

### 3.2 Must be built (the actual gap)

| # | Build item | Basis | Effort |
|---|---|---|---|
| B1 | **Lexicon automaton** — compact trie/DAWG over the 431,596 union headwords (+ a stem trie over vidyut_stems) | §2.3(a); double-array trie or minimized DAWG | medium |
| B2 | **Oflazer error-tolerant traversal** with cut-off (banded) edit distance, threshold `k`, weighted-cost variant | §2.3; [Oflazer 1996](https://aclanthology.org/J96-1003.pdf) | **hard (core)** |
| B3 | **Brill-Moore substring error model** — train `P(β→α)` from the aligned pairs; substring-alignment scorer generalizing `confusion_weight` | §2.4; [Brill-Moore 2000](https://aclanthology.org/P00-1037/) | **hard (core)** |
| B4 | **Ranking function** `log P(x\|w) + λ·log P(w)` with DCS-band + attestation-count prior; top-N | §2.4; extends `spell_correct.py` | medium |
| B5 | **Vidyut-as-generator path** — error-tolerant traversal of the kosha FST (server) or vendored-stem trie (client) | §2.3(b) | medium |
| B6 | **Web app** — new repo + GitHub Pages (ruling D6): input box, scheme detect/override, red-underline, click/Ctrl-Space suggestions, provenance panel, prior-art "about" note | §2.6; Prasanna UI pattern + OpenOCRCorrect | medium |
| B7 | **Client packaging** — compact automaton + channel table shipped to the browser, or a serverless suggest endpoint | §6 | medium |
| B8 | **Evaluation** — precision@k / recall@k / MRR on a held-out set; baseline vs LibreOffice `sa_IN` | §7; extends `eval.py` | medium |

---

## 4. Differentiators (all grounded in in-repo assets)

Straight from [PRIOR_ART.md §7a](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/PRIOR_ART.md):

1. **Tri-scheme input** — SLP1 **and** IAST **and** Devanāgarī, interactively. Nothing in the
   landscape supports IAST interactively (only one dormant 2019 research repo touches romanized
   input at all). Free from the shared transcoder (§2.1).
2. **Evidence-based validity, not generative.** Our oracle is 33-dictionary attestation + DCS corpus
   + Vidyut, not a few-hundred-paradigm expansion. Prasanna's generative dictionary *over-flags*
   (100% precision on accepted words but heavy OOV noise, paper Table 4); an attestation oracle does
   not.
3. **Measured-confusion ranking, not edit distance.** Suggestions rank by an empirically-measured
   channel (`confusion_weights.json` → Brill-Moore) × DCS corpus frequency — not Hunspell's uniform
   edit distance. `ri↔f` and vowel-length swaps are weighted by how often they actually occur.
4. **Variant-aware suppression** (§2.5) — the do-not-file catalogue distinguishes *variant* from
   *typo*, which **no other tool models at all**. This is confirmed-novel in the landscape.

---

## 5. Algorithms in detail

### 5.1 Oflazer cut-off edit distance — why it is tractable

Naïvely, "all lexicon words within edit distance `k`" is `O(|L| · |x| · k)` if you compare `x`
against every word — 431,596 comparisons per query, too slow interactively. Oflazer's insight: share
work across words with a common prefix by walking the **automaton** and computing the edit-distance
matrix **incrementally per edge**, then prune. The banded cut-off (only the `2k+1` diagonal of the
matrix can matter for a distance-`k` match) bounds each row to constant width, and pruning discards
whole subtrees the moment their best-possible completion exceeds `t`. In practice this visits a tiny
fraction of the automaton. Implementation notes for the build:

- Keep only the previous matrix **row** per stack frame (not the full matrix).
- Precompute the banded min so the cut-off test is `O(k)`.
- Cap emitted candidates (e.g. 200) before ranking to bound the ranker's cost.
- Reference implementations to consult (do not reinvent — per the check-prior-art rule): SymSpell,
  `liblevenshtein`, and Lucene's `LevenshteinAutomaton` all implement Oflazer-family Levenshtein-
  automaton traversal. Adapt one; the SLP1-specific part is only the alphabet and the weighted-cost
  channel.

### 5.2 Brill-Moore error model — training and scoring

- **Training data:** align each `(wrong, right)` pair (o_vs_O2.txt + file_first_verified.tsv) at the
  character level; extract all substring-edit operations `α → β` up to a window (Brill-Moore use up
  to length 2–3 on each side, plus position); count and normalize to `P(β → α)` (probability the
  intended substring `β` was written as `α`). Store as a compact JSON table, the sibling of
  `confusion_weights.json` — call it `brillmoore_edits.json`, regenerated by a
  `gen_brillmoore_edits.py` next to `gen_confusion_weights.py`.
- **Scoring** `P(x | w)`: find the partition of `(x, w)` into aligned substring pairs maximizing
  `∏ P(β_i → α_i)`; a small dynamic program over the two strings (Brill-Moore §3). Smooth unseen
  edits with a floor probability so a novel edit is penalized, not fatal.
- **Back-compat:** if the table has no multi-char entry for a span, fall back to the single-char
  `confusion_weights.json` value — so the model degrades gracefully to the already-shipped channel.

### 5.3 The ranking function (reference form)

```
score(x, w) = log P(x | w)            # Brill-Moore channel, §5.2
            + λ * log P(w)            # prior: DCS band (1..5) else attestation-count floor
where P(w) ∝ dcs_band(w)              if w ∈ DCS
           ∝ ε * dict_attestation(w)  otherwise   (ε « smallest DCS mass)
return top-N w by score, N default 5, λ tunable (start λ = 1.0)
```

Return nothing (word is valid) if `x ∈ L` (§2.2). Suppress any `w` that is only an accept-list
variant of a higher-ranked `w'` (§2.5).

---

## 6. Data assets and client packaging

The app is planned client-side on GitHub Pages (ruling D6). The data must ship to the browser or a
serverless function:

- **Automaton (B1):** 431,596 headwords compress well as a minimized DAWG / double-array trie
  (typically a few MB; comparable to how Prasanna's tool shipped a 37k-entry dictionary and how
  LibreOffice ships a 15.5 MB flat list). If the union trie is too large for a comfortable client
  bundle, ship a **serverless suggest endpoint** (Prasanna used a Netlify function running Hunspell
  via `nodehun`; the same shape works — a small function traversing the automaton). Decide at build
  time by measuring the minimized bundle (§12 open question O1).
- **Channel + prior tables:** `confusion_weights.json` (704 B) and `brillmoore_edits.json` (small),
  plus a pruned DCS-band map (drop the JSON body, keep `{lemma: band}`) — all small enough to inline.
- **Accept-list:** 33k entries; ship as a compact set (bloom filter is acceptable for the input-side
  membership test since a false "valid" only means one missed flag, never a wrong correction).
- **Vidyut path:** ship the vendored `vidyut_stems.txt` trie for the client, or call the kosha FST in
  the serverless function. Do **not** require a WASM Vidyut build for v1 (heavy); the vendored stem
  list is the client-safe form.

---

## 7. Evaluation plan

Reuse and extend [detectors/eval.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/eval.py):

- **Recall@k / MRR** on a held-out split of the aligned pairs (o_vs_O2 + file_first_verified): for
  each `(wrong, right)`, is `right` in the top-k suggestions, and at what rank? (Train/test split so
  the channel is not evaluated on its own training pairs.)
- **False-positive rate:** run the validity gate over `nochange.txt` (30,887 known-good) — it must
  flag ≈ 0 (the accept-list guarantees this; the test catches regressions).
- **Baseline comparison:** measure the LibreOffice `sa_IN` Hunspell pack (543,758 entries) on the
  same held-out set — the prior-art scan's stated purpose for it ("a baseline to evaluate against,"
  [PRIOR_ART.md §2a](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/PRIOR_ART.md)).
  Evaluating against it is fine; **ingesting its wordlist is not** (§9).
- **Over-flagging check** on real running text (a GRETIL passage already in-repo under
  `detectors/gretil_*_raw/`): what fraction of valid tokens get flagged? This is the axis on which
  Prasanna's generative dictionary failed; report ours.
- Success is reported as a table in the app repo's README / a metrics doc and mirrored to the paper
  data statements — the web app is also evidence for A44's contrast (§8).

---

## 8. Prior-art credit (M.G.'s standing instruction)

- **In the app UI:** an "about / prior art" note crediting **Prasanna Venkatesh T S, "Spellchecker
  for Sanskrit: The Road Less Taken", ICON 2022** ([2022.icon-main.35](https://aclanthology.org/2022.icon-main.35/))
  — the only prior interactive flag-and-suggest Sanskrit tool, whose UI pattern (CodeMirror editor,
  red-underline, click/Ctrl-Space) this app follows. Also acknowledge the project's own Hunspell
  lineage ([samskrtam.ru/sanskrit-hunspell](https://samskrtam.ru/sanskrit-hunspell/), Gasuns 2013).
- **In the review-UI build:** reuse/study [OpenOCRCorrect](https://github.com/rohitsaluja22/OpenOCRCorrect)
  (BSD-3), the only permissively-licensed interactive correction UI found.
- **In the papers:** both A37 and A44 already cite Prasanna as the state of object-language
  spellchecking; the web app becomes a concrete instance of A44's contrast — generative dictionaries
  over-flag, string-level detectors over-accept, and the evidence-based + variant-aware layer is what
  neither has ([PRIOR_ART.md §7c](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/PRIOR_ART.md)).

---

## 9. Licensing guards (hard constraints)

From [PRIOR_ART.md §7a.4](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/PRIOR_ART.md)
and the roadmap's standing constraints:

- ✅ **Vidyut (MIT)** is the one safely embeddable external oracle — vendor the stems, embed the
  kosha, no attribution beyond the MIT notice already carried in
  [gen_vidyut_stems.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/gen_vidyut_stems.py).
- ⛔ **Do NOT ingest the LibreOffice `sa_IN.dic`** (license unsettled — GPL-2 `COPYING` was added then
  reverted; wikipedia/wikisource derivation adds CC-BY-SA share-alike questions). Evaluate against it
  (§7); never merge it into our data or ship it.
- ⛔ **Do NOT ingest any GPL Hunspell wordlist** (Shreeshrii GPL-3, Firefox add-on GPL-2).
- **Heritage (LGPLLR):** cross-validate against its inflected-forms databank as a *sidecar* oracle
  (LGPLLR permits use with attribution), never a merged ingest.
- **SCL / Samsaadhanii (GPL-2):** call **remotely** as a second-opinion analyzer, never vendor. A
  combined-license question is already in the pending Kulkarni outreach.
- **ashtadhyayi.com data:** needs a license ask before any use.
- **DCS-2021 (CC-BY):** already vendored with attribution; keep the attribution.
- **CDSL headwords:** a Hunspell `.aff/.dic` *export* of our validated union (a packaging option the
  scan surfaced) needs a CDSL-headword licensing check first — out of scope for the web app, flagged
  for the PyPI/packaging track.

---

## 10. ISCLS demo hook (ruling D12)

The web app is a natural **ISCLS demo-track** submission: an interactive, evidence-grounded,
tri-scheme Sanskrit spellchecker occupying a decade-open niche
([COLOGNE #91](https://github.com/sanskrit-lexicon/COLOGNE/issues/91), "Hunspell for Sanskrit?", open
since 2016). It pairs naturally with A44 (the method paper behind the validity oracle) and cites
Prasanna (also an ISCLS-community author) as the immediate predecessor. When the build lands
(Q1 2027), the demo submission is a low-marginal-cost deliverable off the same artifact — note it in
the app repo's README and in [ARTICLES.md](https://github.com/gasyoun/Uprava/blob/main/ARTICLES.md)
at build time.

---

## 11. Non-goals and guards

- **No build in this handoff** (ruling D13). Build deferred to post-30-06-2027 so it does not compete
  with the ≥300-corrections north-star.
- **Candidate generation via Vidyut here is a SUGGESTER function** — enumerate nearby *valid* forms
  for a user's typo. This is **distinct from and not in conflict with refuted paths R2/R6** (Vidyut as
  a *detector-side tier promoter*, refuted per the roadmap's "do not re-attempt" list). The suggester
  never promotes a detector candidate's tier; it answers a different question (what did the user
  mean), on the user-facing side, not the QA side. Keep the two uses firewalled.
- **v1 checks surface tokens, not full inflection** (§2.2 note) — inflected-form validation via
  `vidyut-prakriya`/`vidyut-cheda` is phase-2, not a v1 requirement. Document the limitation in the UI.
- **The app is a NEW repo + GitHub Pages** (ruling D6) — this spec can live in
  `SanskritSpellCheck/docs` and be carried over to the new repo at build time.
- **Publish-safety:** before the app goes public, run
  [/publish-safety-check](https://github.com/gasyoun/claude-config/blob/main/commands/publish-safety-check.md)
  — verify no gitignored bulk (`external_src/`, `review/`) or unsettled-license data leaks into the
  client bundle.

---

## 12. Open questions / build prerequisites

Genuine forks a build session (or M.G.) must resolve — parked here, not guessed:

- **O1 — Client bundle vs serverless.** Measure the minimized union-headword automaton. If it fits a
  comfortable client bundle (target ≲ 5–8 MB gzipped), ship fully client-side (Pages, no backend); if
  not, ship a serverless suggest endpoint (Prasanna's Netlify-function shape). Decision waits on the
  measured size.
- **O2 — Edit-distance threshold policy.** Confirm `k = 2` default with length-based degrade to
  `k = 1`, and whether to ship channel-weighted pruning in v1 or as a fast follow. Needs the
  precision@k / latency numbers from a prototype (§7).
- **O3 — Inflected-form coverage in v1.** Surface-form-only (accept the limitation, ship faster) vs
  `vidyut-cheda` sandhi/inflection split in v1 (better coverage, heavier). Recommend surface-only for
  v1, matching Prasanna.
- **O4 — Vidyut client form.** Vendored stem-trie (client-safe, no WASM) vs WASM kosha build (fuller
  generation, heavy). Recommend the vendored stem-trie for v1.
- **O5 — Repo location.** New standalone repo now vs incubate in `SanskritSpellCheck/webapp/` and
  split later. Ruling D6 says new repo; confirm the name at build time (working name
  `sanskrit-spellcheck-web`).

---

## 13. Build task breakdown (for the future session)

Ordered, each item cross-referenced to §3.2. A build session executes roughly in this order:

1. **B3 + Brill-Moore table** — `gen_brillmoore_edits.py` (train from the aligned pairs) +
   substring-alignment scorer generalizing `slp1util.confusion_weight`. Testable standalone against
   `eval.py`.
2. **B1** — build the union-headword automaton (minimized DAWG / double-array trie) + a stem trie.
   Measure the bundle size → resolves O1/O4.
3. **B2** — Oflazer cut-off traversal over B1 (adapt a reference Levenshtein-automaton library).
   Unweighted first, then channel-weighted pruning.
4. **B4** — the ranker: fork `spell_correct.py`, swap in B2 (generation) + B3 (channel), keep its
   DCS-band prior; add the attestation-count floor.
5. **B5** — the Vidyut generator path (vendored-stem trie for the client).
6. **B8** — evaluation harness extension (precision@k / recall@k / MRR + LibreOffice baseline +
   over-flag rate on GRETIL text). Gate the build on these numbers.
7. **B6 + B7** — the web app (new repo + Pages) and client packaging: UI, scheme detect, provenance
   panel, prior-art "about" note; then `/publish-safety-check` before going public.
8. **ISCLS demo note** (§10) + `ARTICLES.md` entry at build time.

Each of the above is a candidate handoff of its own when the Q1-2027 build opens; B2 and B3 are the
two hard, judgment-bearing pieces and should each be their own handoff.

---

## References

- [Oflazer, K. (1996). "Error-tolerant Finite-State Recognition with Applications to Morphological Analysis and Spelling Correction." Computational Linguistics 22(1), J96-1003.](https://aclanthology.org/J96-1003.pdf)
- [Brill, E. & Moore, R. C. (2000). "An Improved Error Model for Noisy Channel Spelling Correction." ACL 2000, P00-1037.](https://aclanthology.org/P00-1037/)
- [Mohit et al. (2014). QALB Arabic spelling-correction shared task, W14-3605.](https://aclanthology.org/W14-3605/) · [QCMUQ, W15-3217.](https://aclanthology.org/W15-3217/)
- [Prasanna S. (2022). "Spellchecker for Sanskrit: The Road Less Taken." ICON 2022, 2022.icon-main.35.](https://aclanthology.org/2022.icon-main.35/)
- [Prasad, A. (2024). Vidyut. ISCLS 2024, 2024.iscls-1.7.](https://aclanthology.org/2024.iscls-1.7/) · [ambuda-org/vidyut](https://github.com/ambuda-org/vidyut) (MIT)
- [docs/PRIOR_ART.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/docs/PRIOR_ART.md) — the full landscape survey (H452)
- [ROADMAP_2026_2027.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ROADMAP_2026_2027.md) — rulings D1, D6, D12, D13

_Dr. Mārcis Gasūns_
