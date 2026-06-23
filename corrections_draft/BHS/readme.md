# BHS correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **713 tier-A** BHS headwords as possible misspellings.
BHS is Edgerton's *Buddhist Hybrid Sanskrit Grammar and Dictionary, Vol. II* (1953) — a
specialized lexicon of the hybrid Sanskrit of Buddhist texts, glossed in English. This
package triages the candidates against BHS's *own entry text* (from
[csl-orig](https://github.com/sanskrit-lexicon/csl-orig)): a spelling-only detector cannot
tell a typo from a deliberately-recorded hybrid form, a proper name, or editorial apparatus,
but the entry can.

## The finding

> **Of 713 engine "tier-A" candidates, 0 are body-confirmed fileable typos.** 415 are real,
> distinct BHS words (Edgerton's own glossed lexemes, derivations, and — above all — proper
> names); **294 are spellings BHS records on purpose**; 4 are too terse to judge.

This is the entirely expected result for a *specialized hybrid-Sanskrit* dictionary. The whole
point of Edgerton's work is to document the spellings of Buddhist Hybrid Sanskrit that *diverge*
from standard Sanskrit — so a one-letter "anomaly" against a normal-Sanskrit baseline is almost
always exactly the form Edgerton means to record. The two recurring families:

- **Deliberate hybrid / Middle-Indic / metrical forms** — Edgerton flags these with his standard
  apparatus: `(m.c. for …)` (metri causa), `(= Pali …)`, `semi-MIndic`, `hyper-Skt.`, `also
  written …`, `(graphic) corruption`, `misprint for …`, `read X`, `v.l.`, `q.v.`. (294 do-not-file.)
- **Proper names** — goddesses, yoginīs, rākṣasīs, apsarases, nāga kings, rivers, cities,
  lokadhātus (`Dīpā`, `Kusumā`, `Locanā`, `Nīlotpalā`, `Sundarā`, `Vimokṣā`, `Dṛḍhā`, …), where
  the "extra" letter is the feminine ending or simply the name itself. (the bulk of the 415.)

Across the dictionaries triaged, fileable-typo precision on tier A is tiny — **MW 4/1954 ·
PW 2/657 · VCP 1/563 · PWG 12/497 · SHS 37/~250 · BHS 0/713**. Do **not** bulk-apply tier A; the
durable deliverable is the do-not-file list, which feeds the detector suppression layer.

## The authoritative artifacts

- **[BHS_wrong_readings.txt](BHS_wrong_readings.txt)** — the standing **do-not-file** list: 294
  deliberate spellings, grouped by sub-type (cross-reference **138**, varia-lectio **81**,
  other-intentional **67**, wrong-reading **6**, in-composition **2**). Use it as a suppression
  list so future runs never re-flag them; it is folded into
  [nochange/do_not_file_suppress.txt](../../nochange/do_not_file_suppress.txt) by
  [detectors/gen_do_not_file_suppress.py](../../detectors/gen_do_not_file_suppress.py).
- **[BHS_triaged.txt](BHS_triaged.txt)** — the full review queue: the 415 REAL-WORD entries (with
  Edgerton's own gloss/derivation showing why each is a distinct word) and the 294 INTENTIONAL ones.
- **[BHS_file_first_sf.txt](BHS_file_first_sf.txt)** — **empty** (0 fileable). Nothing to file.

## Why every candidate is safe (worked examples)

- **Proper names** — `{@Kusumā@}` "n. of a legendary queen", `{@Locanā@}` "n. of a goddess",
  `{@Nīlotpalā@}` "n. of an apsaras": the name *is* the headword; "correcting" it to the common
  noun would be wrong.
- **Metri-causa forms** — `{@atīśaya@}` "(m.c. for Skt. ati˚)", `{@uṣṇiṣa@}` "(m.c. for uṣṇīṣa)",
  `{@a-parājīta@}` "(m.c. for ˚jita)": Edgerton explicitly marks the metrical vowel.
- **Documented corruptions / readings** — `{@kṣaṇā@}` "prob. … a mere corruption", `{@prākṛti@}`
  "perhaps only misprint", `[{@śardūla@} … read … {@gardūla@}, q.v.]`: filing these would
  contradict Edgerton's own note.
- **Hybrid lexemes with their own gloss** — `{@antrā@}` "intestines" (contrasted with "Skt. and
  Pali only nt. antra"), `{@sona@}` "(= Pali sona … to Skt. śvan), dog", `{@adhipatya@}`
  "(= Pali adhipacca), overlordship": distinct words, not slips.

## Method

1. **Engine → tier-A package** — `detectors/triage_dict.py BHS` (make_dict_package → enrich →
   bodies → batches). The deterministic marker pass settled 162 candidates as intentional
   (apparatus/redirect/xref) before any LLM call.
2. **Body-aware classification** of the 551 remaining `realword` candidates against BHS's own
   entry text — TYPO / REALWORD / INTENTIONAL / UNSURE. (BHS registered as English in
   `detectors/triage_lang.py`.)
3. **Synthesize** — `detectors/triage_dict.py BHS --finish` → the three artifacts above. With 0
   TYPO classifications there was no source-confirm / review pile.

> **DRAFT for human review.** This package never edits `csl-orig`. The do-not-file list is the
> deliverable; there are no corrections to file from BHS tier A.
