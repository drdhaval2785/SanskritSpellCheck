_Created: 10-08-2026 · Last updated: 05-09-2026_

# BUR correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **162 tier-A** BUR headwords as possible misspellings. BUR is
Burnouf's *Dictionnaire classique sanscrit-français* (1866) — Sanskrit headwords (SLP1 in `{#...#}`)
glossed in **French**, each headword echoed in IAST in the gloss `{%...%}`. This package triages the
candidates against BUR's *own entry text* (from
[csl-orig](https://github.com/sanskrit-lexicon/csl-orig/tree/main/v02/bur)).

## The finding

> **Of 147 located engine "tier-A" candidates, 0 are body-confirmed fileable typos.** 123 are real,
> distinct words, 20 are spellings BUR documents on purpose, 4 are typo-unsure (reviewed out).

This is the expected outcome for a mature 19th-century scholarly dictionary. BUR's most distinctive
pattern is a dense web of **root cross-references**: it lists a root variant and points to the
related root with `cf.` — `*Bad` ... cf. `bhand`, `*jiv` ... cf. `jinv`, `*tub` ... cf. `tumb`,
`baṅga` "le Bengale" cf. `vaṅga`, `kṛṣānu` cf. `kṛśānu`, `vāhu` cf. `bāhu`. These are deliberate
(17 of the 20 do-not-file rows), not errors. The 4 typo-unsure cases were all **reviewed out** by
the Opus false-positive gate: two because the entry's *own gloss* spells the suspect form
(`aśunya` 'sans vide, plein' = priv. of śūnya; `kamaṭa` derived `(kam=eau aṭ=tortue)`) and two as
**vṛddhi derivatives** from a cited base (`smāśānika` ← śmaśāna 'qui fréquente les cimetières';
`viṣṭala` ← sthala). None survived to FILE-FIRST.

Cross-dict fileable precision: SHS 37/246 · YAT 27/247 · ACC 22/174 · … · BHS 0/713 · PUI 0/518 ·
IEG 0/162 · BOP 0/39 · STC 0/111 · **BUR 0/162**.

## The authoritative artifacts

- **[BUR_wrong_readings.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/BUR/BUR_wrong_readings.txt)** — the **do-not-file** list: 20 deliberate
  spellings (cross-reference 17, other 3). Folded into
  [nochange/do_not_file_suppress.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/nochange/do_not_file_suppress.txt).
- **[BUR_triaged.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/BUR/BUR_triaged.txt)** — full queue: 123 REAL-WORD + 20 INTENTIONAL + 4 TYPO-UNSURE.
- **[BUR_file_first_sf.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/BUR/BUR_file_first_sf.txt)** — **empty** (0 fileable); the 4 reviewed-out
  candidates (`aSunya`, `kamawa`, `smASAnika`, `vizwala`) are commented there with the reasons.

## Method

`detectors/triage_dict.py BUR` (package) → body-aware HYBRID classification (BUR registered as
**French** in `triage_lang.py`: `faute pour`/`lisez` = wrong-reading, `voyez`/`voy.`/`cf.` =
cross-reference) → source-confirm the TYPO pile on Opus → **Opus false-positive review** →
`triage_dict.py BUR --finish`. **DRAFT for human review; never edits `csl-orig`.**

_Dr. Mārcis Gasūns_
