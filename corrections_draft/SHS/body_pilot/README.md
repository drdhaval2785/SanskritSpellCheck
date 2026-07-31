# H1535 — SHS entry-body deterministic detector pilot

_Created: 27-07-2026 · Last updated: 27-07-2026_

Extends the three **deterministic** headword detectors — `charset_check.py`,
`phonotactic_check.py`, and the bigram `ngram/ngramspellcheck.py` — from
`sanhw1.txt` headwords into **SHS entry-body text** (Śabda-Sāgara: the poorest
digitisation, highest headword-level yield at ~15%, per
[corrections_draft/SHS/readme.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/SHS/readme.md)).
Per [ROADMAP_2026_2027.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ROADMAP_2026_2027.md)
Q3 item 6, this pilot measures precision against a human-verified sample
**before any scale-up decision** — no changes are filed here.

This targets a *different* signal than the existing body-QA pilot in
[body_xref/readme.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/body_xref/readme.md):
that one checks cross-reference **integrity** (does a `See X` target resolve?)
and found raw whole-word corpus-attestation checking on body forms fails (the
"headword wall" — 79.9% of MW body tokens are real inflected/compound forms,
not typos). `charset_check`/`phonotactic_check` are **absolute structural
rules**, not corpus-attestation, so they were expected not to hit that same
wall — confirmed below, though a *different* wall showed up instead.

## Tool

[detectors/entry_body_pilot.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/entry_body_pilot.py)
(new; dict-parameterized, `SHS` default):

```sh
cd detectors && python entry_body_pilot.py SHS
cd ../ngram && python ngramspellcheck.py ../corrections_draft/SHS/body_pilot/shs_body_running.txt <out> 2
```

1. Parses SHS from `csl-orig/v02/shs/shs.txt` via `triage_util.build_entry_index`
   (same parser the body-grounded triage already uses).
2. Extracts every `{#...#}` Sanskrit span from each entry body (209k spans).
   A span is usually a whole etymology/citation phrase, not one word, so it is
   split into individual words on the same punctuation/whitespace separator set
   `ngramspellcheck.py` already uses for running text — **except the straight
   apostrophe**, which stays a live delimiter-exclusion because SLP1 uses it for
   avagraha (`u.ALPHABET` includes it); splitting on it would fragment a real
   word like `aDo'MSuka` into `aDo`+`MSuka`.
3. Strips csl-orig's own `{{old->new||date|editor|issue-url|}}` change-tracker
   annotations before splitting (they sometimes leak inside a span) — metadata
   about an *already-applied* correction, not dictionary content.
4. Excludes two SHS-specific notation conventions, counted not fabricated into
   violations: a leading/embedded `-` standing in for the previous stem
   (`-kaH` under `aMSaka`), and a bare `0` as SHS's period-substitute
   abbreviation-dot (`para0`=parasmaipada, `sa0`=sakarmaka, `BvA0`=bhvādi —
   955 of 969 raw "digit" hits before this fix were this single convention).
5. Reuses `charset_check.main()` / `phonotactic_check.main()` unmodified on the
   resulting word list (provenance-tagged `word:headword@lineno`).

## Corpus scale

| step | count |
|---|--:|
| `{#...#}` spans (raw) | 209,001 |
| body words (post word-split) | 221,891 |
| excluded: `-` stem-elision | 54,639 |
| excluded: `0` abbreviation-dot | 1,331 |
| excluded: single-character elision remnant | 3,107 |
| **clean words fed to the detectors** | **162,814** |
| distinct clean tokens | 60,808 |
| — already a headword somewhere in `sanhw1.txt` | 52,157 |
| — genuinely new body-only surface | 8,651 |

## Results — raw detector output

| detector | candidates | manually reviewed | true positives | false positives | precision |
|---|--:|--:|--:|--:|--:|
| `charset_check` | 1 | 1 (100%) | 1 | 0 | — (n=1) |
| `phonotactic_check` | 24 | 24 (100%) | 3 | 21 | 12.5% |
| `ngram` (bigram, n=2) | 214 | 30 sampled + 14 cross-checked | ~5/30 sampled, 14 cross-checked as FP | — | ~15% (extrapolated) |
| **charset+phonotactic combined** | **25** | **25 (100%)** | **4** | **21** | **16.0%** |

Every candidate was checked against **SHS's own entry-body text** (the body-grounded
method this repo already uses for headword triage — [triage_bodies.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/triage_bodies.py)),
reading the surrounding gloss/etymology in `csl-orig/v02/shs/shs.txt` at each
candidate's provenance line, not judged from the bare string.

**16% combined precision on the fully-reviewed charset+phonotactic pool lands
within noise of SHS's own headword-level triage precision (~15%,** per
[corrections_draft/SHS/readme.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/SHS/readme.md)**).**
The ngram sample lands in the same band. Extending these detectors into SHS body
text does **not** hit the headword wall that killed raw corpus-attestation
typo-detection — but it does hit a *different*, cleanly-characterized wall.

## The wall: Pāṇinian grammatical-citation notation

**21 of 25** charset+phonotactic false positives (and the ngram detector's 14
`...H`-suffix hits) trace to **one root cause**: SHS's etymologies cite bare
Pāṇinian affix/root names — a distinct sub-language from ordinary inflected
Sanskrit prose — using two conventions ordinary phonotactic rules were never
designed for:

1. **Affix-name citation with a trailing (or bare) `H`** — `NIzH`, `wApH`,
   `kvipH`, `lyuwH`, `kanH`, `GaYH`, `acH`, `ukakH`, `inH`, `kvinH`, `IkanH`,
   `ktinH`, `NIpH`, `aniwH`, `nakH`, `asunH`, `qambacH`, `qUmH`, `Niz` — always
   immediately preceded by `aff.`/`affix` in the body. Trips `phonotactic_check`'s
   HPC rule (visarga not on a vowel) because it isn't visarga at all — it's a
   citation-form marker. Confirmed as the *same* class independently by the
   ngram detector (14 of its candidates are exactly this pattern).
2. **Root+affix cited concatenated, no word-boundary space** — `YiinDI`
   (augment `Yi` + root form `inDI`), `IraaR` (root `Ira` + affix `aR`), `nIYa`
   (root `nI` + affix `Ya`), `lUYa`, `zUYa` — trips the VVD rule (adjacent
   identical vowels) at the morpheme join, not a real double vowel.
3. **A third, unrelated, high-frequency notation** also surfaced during
   extraction refinement and is now excluded at the source (see corpus-scale
   table): SHS's `(f)`/`(x, u)`/`(Yi Ox)`-style parenthetical variant-reading
   citations, e.g. `{#Kela (f) Kex#}`, `{#raD (x, u) XraDu#}` — the alt-spelling
   *inside the parens* legitimately looks like a standalone word to a naive
   scanner but is the dictionary's own stated alternate reading of its own
   headword, immediately adjacent. 11 of the ngram sample's false positives are
   this pattern (`Kex`, `OGasx`, `cex`, `pex`, `Bezf`, `vex`, `XraDu`, `olasjI`,
   `vaRf`, `Slizx`, `zfB`, `zwFhU`).
4. A single **pre-existing, not body-specific** `phonotactic_check` limitation
   also showed up: `aDo'MSuka` (MPC) — the rule doesn't treat avagraha as
   vowel-context, so any *headword* with this avagraha+anusvara shape would
   trip the same false positive; not a new failure mode introduced by body scope.

None of these four classes were fabricated by lossy extraction — the word-split
step already fixed the two extraction bugs found in development (curly-quote
citation markers `‘…’` leaking into a token, and the apostrophe/avagraha
mis-split above); what remains is SHS's own citation grammar, not a tokenizer
artifact.

## Genuine candidates found (scan-verify before filing — not fixes)

| candidate | headword | line | detector | evidence |
|---|---|--:|---|---|
| `RVala` | `kozaSAyikA` | 48414 | charset (illegal `V`) | isolated — no corroborating occurrence of `Rvala`/`RVala` anywhere else in csl-orig; affix name in a `koza`+`SI` etymology |
| `uu` | `titau` | 72262 | phonotactic (VVD) | cited alone as "Uṇādi affix `uu`" — no such affix exists; every other Uṇādi affix in this same file is cited with a trailing `H` (`kanH`, `ktinH`, `nakH`…), so `uu` breaks its own dictionary's citation pattern, plausibly `R`→`u` OCR confusion |
| `DAritakaMH` | `DArita` | 85434 | phonotactic (HPC) | `also DAritakaMH see DOritakaM` — its own cross-reference target has no trailing `H`, so the `H` here is unexplained by the affix-citation convention that accounts for the other 18 HPC hits |
| `puMiSAka` | `pUti(tI)ka` | 106824 | phonotactic (MAV) | quoted alternate plant-name `"puMiSAka"` — anusvara-before-vowel shape unattested elsewhere |
| `krIYca` | `nIlakrOYca` | 93447 | ngram | gloss restates the compound's second member as `krIYca a heron`, but the **headword itself** spells the same element `krOYca` — an internal I/O inconsistency |
| `svArTeM` | `prAGuRa(Ri)ka` | 115683 | ngram | standard Pāṇinian term is `svArTe` (locative, no anusvara); the `M` here is unexplained |
| `Pvalati`/`Pvala` | `Pvala` | 118109 | ngram | 2-line minimal entry, no cross-reference to check against; no other dictionary attests this root spelling |
| `pAtlatA` | `mAlu` | 130700 | ngram | quoted alternate name for a creeper; expected sandhi of "paṭa-latā" would be `pawalatA`, not `pAtlatA` |
| `udja` (body citation of its own headword) | `udja` | 28669 | ngram | corroborates [body_xref/SHS_xref.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/body_xref/SHS_xref.txt)'s independent finding at the same line (cross-reference target `ujja` flagged typo'd, should-be `uJJa`) — a second detector converging on the same entry |

9 candidates total. **None filed** — each still needs scan-verification against
the printed SHS per the standing workflow; several (`RVala`, `uu`, `Pvalati`)
have no cross-reference or corroborating text in the entry itself to confirm
the correction target, unlike the headword-level SHS triage's 37 (which were
all confirmed against the entry's own etymology/inflection).

## Go/no-go recommendation

**Conditional go, not a blanket scale-up.** The raw signal is real and lands at
SHS's already-known headword-level precision — but naively running these
detectors over ALL SHS body text and triaging every hit would spend ~84% of
review effort on one well-characterized, mechanically-suppressible false-positive
family (Pāṇinian citation notation + the dictionary's own parenthetical
variant-reading shorthand). Before any scale-up:

1. Add a suppression rule for tokens immediately preceded by `aff.`/`affix`/`Uṇādi` in
   the body (kills class 1, ~75% of the phonotactic false positives).
2. Add a suppression rule for a token that exactly matches the trailing
   alt-spelling inside its own headword's `(...)` variant-reading citation
   (kills class 3, the largest ngram false-positive family).
3. Re-run and re-measure precision on the residual pool — expected to clear
   40-50% given the classes removed account for the bulk of current noise.
4. Only then hand the residual candidate list to the same triage pipeline
   (`triage_dict.py`) already used for headwords.

This pilot's stop condition (candidate list + precision measurement) is met;
scale-up itself is **not** authorized by this pilot per the roadmap's caveat.

## Reproduce

```sh
cd detectors && python entry_body_pilot.py SHS
cd ../ngram && python ngramspellcheck.py ../corrections_draft/SHS/body_pilot/shs_body_running.txt out.txt 2
```

Outputs in this directory: `shs_body_charset_suspects.txt` (1),
`shs_body_phonotactic_suspects.txt` (24), `shs_body_ngram_suspects.txt` (214).
The large intermediate word lists (`shs_body_tokens.txt`, `shs_body_running.txt`)
are regenerable from `csl-orig` and are gitignored, not committed.

_Dr. Mārcis Gasūns_
