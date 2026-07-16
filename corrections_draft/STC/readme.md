# STC correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **111 tier-A** STC headwords as possible misspellings. STC is
Stchoupak–Nitti–Renou's *Dictionnaire Sanscrit-Français* (1932) — Sanskrit headwords glossed in
**French**, with the Sanskrit set in `{@...@}` (IAST) and the French gloss in `{%...%}`. This
package triages the candidates against STC's *own entry text* (from
[csl-orig](https://github.com/sanskrit-lexicon/csl-orig/tree/main/v02/stc)).

## The finding

> **Of 93 located engine "tier-A" candidates, 0 are body-confirmed fileable typos.** 75 are real,
> distinct words, 9 are spellings STC documents on purpose, 5 are typo-unsure (source-confirm
> refuted or reviewed out), 1 needs the printed page, 3 are unlocatable.

This is the expected outcome for a mature 20th-century scholarly dictionary. STC's own apparatus is
dense: it routinely records a variant headword and points to the canonical entry with `v.` (=
*voyez*), `v. s.` (*voyez sous*), `lire` (*read*) or `pour` — e.g. `caṭura-` *pour* `caṭula-`,
`valmi-` *lire* `vallī-`, `vi-nivarhaṇa-` *lire* `˚barhaṇa-`, `Atas` = `atas`. These are deliberate
cross-references, not errors. The 5 typo-unsure cases are instructive: the Opus review gate **held
back** three the classifier had flagged as real distinct words — `praś-` (the genuine root
*pṛcchati* 'demander'), `bibhīṣaṇa-` (a **b/v** variant STC defines in its own right as "frère de
Rāvaṇa" = Vibhīṣaṇa), `pra-dīna-` (a **d/ḍ** form glossed 'envolé', i.e. praḍīna) — and source-
confirm refuted two others (`pra-dhāraṇā-`, `ā-patanā-`, both feminine `-ā` entries matching their
own headword). The b/v and d/ḍ pairs are exactly the high-yield classes, but each is **held for the
scan** rather than filed, since STC may print the variant on purpose.

Cross-dict fileable precision: SHS 37/246 · YAT 27/247 · ACC 22/174 · … · BHS 0/713 · PUI 0/518 ·
IEG 0/162 · BOP 0/39 · **STC 0/111**.

## The authoritative artifacts

- **[STC_wrong_readings.txt](STC_wrong_readings.txt)** — the **do-not-file** list: 9 deliberate
  spellings (cross-reference / *lire* apparatus). Folded into
  [nochange/do_not_file_suppress.txt](../../nochange/do_not_file_suppress.txt).
- **[STC_triaged.txt](STC_triaged.txt)** — full queue: 75 REAL-WORD + 9 INTENTIONAL + 5 TYPO-UNSURE
  (incl. the b/v `bibhīṣaṇa` and d/ḍ `pradīna` cases, **held for scan**) + 1 REVIEW + 3 UNLOCATABLE.
- **[STC_file_first_sf.txt](STC_file_first_sf.txt)** — **empty** (0 fileable); the 3 reviewed-out
  candidates (`praS`, `biBIzaRa`, `pradIna`) are commented there with the reviewer's reasons.

## Method

`detectors/triage_dict.py STC` (package) → body-aware HYBRID classification (STC registered as
**French** in `triage_lang.py`: `faute pour`/`lisez` = wrong-reading, `voyez`/`voy.`/`cf.` =
cross-reference) → source-confirm the TYPO pile on Opus → **Opus false-positive review** →
`triage_dict.py STC --finish`. **DRAFT for human review; never edits `csl-orig`.**
