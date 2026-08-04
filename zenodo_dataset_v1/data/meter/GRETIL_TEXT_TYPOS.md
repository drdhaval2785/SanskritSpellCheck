# GRETIL in-corpus typo candidates — bigram checker on running text

_Created: 07-07-2026 · Last updated: 10-07-2026_

> **Superseded for upstream use (10-07-2026, H456):** every locus below has been
> hand-verified against the raw e-texts; the curated, reportable result is
> [GRETIL_UPSTREAM_REPORT.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/meter/GRETIL_UPSTREAM_REPORT.md)
> (60 verified loci / 11 anomalous / 53 classified false positives). This file stays as
> the raw candidates record. Note two verification reversals: `hbizekzyati` is a genuine
> e-text transposition (*'hbiṣekṣyati* in the raw), not a walker artifact as guessed
> below; and `skmsauka`/`pvpadyA` are the editor's apparatus citation sigla, not
> corruption.

Handoff [H289](https://github.com/gasyoun/Uprava/blob/main/handoffs/H289-Opus_SanskritSpellCheck_gretil_other_sections_pilot_07.07.26.md)
Phase 3, **stream 2**: errors *inside the GRETIL e-text itself* (OCR / encoding /
transcription slips), as distinct from the dictionary-headword corrections of
[stream 1](MULTISECTION_ERROR_CANDIDATES.md). These are **GRETIL / e-text defects,
reported upstream to GRETIL** (gretil@sub.uni-goettingen.de) — NOT to the Cologne
[CORRECTIONS](https://github.com/sanskrit-lexicon/CORRECTIONS/issues) queue (a
different consumer: CORRECTIONS is for dictionary text, this is for corpus text).

## Method

[`ngram_corpus_check.py`](detectors/meter/ngram_corpus_check.py) walks each sampled section's verses
([`gretil_walker.py`](detectors/meter/gretil_walker.py)), transliterates every verse IAST→SLP1 with the
canonical [`sanskrit_util.to_slp1`](../sanskrit_util.py), and flags words containing a
bigram **absent from the MW∩PW headword bigram model** (the same
[`ngram/data/2grams.txt`](../../ngram/data/2grams.txt) + whitelist/whiteends suppression
assets as [`ngram/ngramspellcheck.py`](../../ngram/ngramspellcheck.py)), keeping the
locus of each hit. The method is deliberately **high-recall / low-precision** on running
text — inflected, sandhi'd, and compounded words legitimately contain bigrams no headword
has — so every row is a **human-review candidate, never an auto-fix**. Per-section full
lists: `ngram_typos_<section>.tsv` (committed).

## Per-section yield

| Section | Verses | Tokens | Flagged words |
|---|---:|---:|---:|
| Purāṇa (Mārkaṇḍeya 1–93) | 1289 | 12,135 | 21 |
| Epic (Vālmīki Rām., southern 2) | 1500 | 17,868 | 8 |
| Subhāṣita anthology (Vidyākara) | 844 | 21,011 | 17 |
| Verse-śāstra (Manusmṛti) | 1495 | 18,087 | 4 |
| Subhāṣita + Stotra (Phase-1 pilot) | 2597 | 31,860 | 68 |

Flag density is very low on the clean narrative/śāstra e-texts (Epic 8, Manu 4) and
higher on the ornate anthology (Vidyākara) and the pilot's devotional collection — the
same ordering as the meter non-clean rates, i.e. lexical density, not corruption, drives
most of it.

## Confirmed real e-text errors (spot-verified against the GRETIL raw)

- **Vocalic ṝ mis-encoded as visarga ḥ** — the headline finding, a *systematic* GRETIL
  encoding corruption in the **Vālmīki Rāmāyaṇa (southern rec. 2)** e-text. The ṝ-stem
  gen./acc. plurals are written with `ḥ` where `ṝ` belongs: raw `mātḥṇāṃ` for *mātṝṇām*,
  `bhartḥn` for *bhartṝn*, `bhrātḥn` for *bhrātṝn*, `kartḥṇām` for *kartṝṇām*. Surfaced as
  `mAtHRAM` (**3 loci**: rams_2,16.13 · 2,19.6 · 2,38.16), `BartHn` (2,42.15), `BrAtHn`
  (2,8.8), `kartHRAM` (2,20.34), `mAtHMS` (2,1.4), `mAtHn` (2,34.33). One class of fix,
  many loci — worth a single GRETIL report.
- **`dsyu` for *dasyu*** (dropped *a*) — Mārkaṇḍeya-purāṇa markp_19.25, raw
  `dsyu-vyālāgri-śastrādi-…`.
- **`skmsauka`** — a garbled fragment recurring in Vidyākara VidSrk 6.41 and 14.10
  (**2 loci**), bigrams `sk`/`km`/`ms` no headword carries; needs an eyeball against the
  print.

The remaining rows include further plausible slips (`durotdara`, `pAtrANkuratvAtd`,
`paSyedty`, `grahasH`, `mudrAtmaBisH` with stray visarga; `htvAnnantu`) — all left in the
per-section TSVs for a human pass.

## Known false-positive classes (documented, not filed)

- **Legitimate rare clusters** — `dn` in *mṛdnanti / mṛdnīyāt* (√mṛd class-9 present),
  `Yg`/`Jg` in ṅ-clusters. Real words the headword-bigram model simply never saw.
- **Vowel hiatus written out** — `Aa` in Manu `mahāayajñān` (mahā-ayajñān), `AlambhāaV`;
  a GRETIL orthographic choice, not a typo.
- **ñ-sandhi** — the `YE` family (`yajñair…` = *yajñaiḥ* sandhi), very common in the
  Purāṇa list; benign.
- **Walker word-join / avagraha artifacts** — a few tokens fused across a sandhi/avagraha
  boundary by the space-tokenizer (e.g. `hbizekzyati` ← *’bhiṣekṣyati*).

These are catalogued so the next reviewer does not re-litigate them.

_Dr. Mārcis Gasūns_
