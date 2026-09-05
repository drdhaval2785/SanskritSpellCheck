_Created: 10-08-2026 · Last updated: 05-09-2026_

# MW correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine ([detectors/run_all.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/run_all.py)) flagged
**1,954 tier-A** MW headwords as possible misspellings. This package is the result of
**triaging** those candidates against MW's *own entry text* (from
[csl-orig](https://github.com/sanskrit-lexicon/csl-orig)) — because a spelling-only
detector cannot tell a typo from a real word, an intentional variant, or editorial
apparatus, but the dictionary entry can.

## The finding

> **Of 1,954 engine "tier-A" candidates, only 4 (0.2%) are body-confirmed fileable
> typos.** 1,161 are real distinct words; **630 are spellings MW documents on purpose**
> (`w.r. for…` wrong-reading apparatus, `v.l.`, `in comp. for…` sandhi/compounding
> forms, cross-references) — **filing them would *corrupt* MW**; 11 are not in the
> current source (stale `sanhw1`); 148 need human eyes.

"Tier A" is high *engine* confidence, **not** precision. **Do not bulk-apply it.** A
second observation: the engine's **vowel-length** flags (≈77% of tier-A) are almost all
false — Sanskrit uses vowel length *lexically* — while the rarer **consonant-class**
flags (retroflex, sibilant, aspirate) are far higher-precision (3 of the 4 confirmed).

## The authoritative artifact

- **[MW_triaged.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/MW/MW_triaged.txt)** — the review queue: six ranked buckets
  (FILE-FIRST · TYPO-UNSURE · REVIEW · REAL-WORD · INTENTIONAL · UNLOCATABLE), each row
  with MW's own entry text, the judgment, the source-confirmation, and a scan link.
- **[MW_file_first_sf.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/MW/MW_file_first_sf.txt)** — the 4 FILE-FIRST candidates in
  CORRECTIONS standard format (`MW:wrong:right:n`). Verify each on the scan, flip the
  trailing `n`→`y`, then `python chg_nchg_sep.py …`.
- **[MW_wrong_readings.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/MW/MW_wrong_readings.txt)** — the standing **do-not-file** list:
  630 headwords MW documents on purpose (wrong-reading apparatus `w.r.` 45, `v.l.` 54,
  in-composition/sandhi 105, cross-reference 204, other 222), grouped by sub-type with
  the entry text. Filing a "correction" for any of these *corrupts* MW; use it as a
  suppression list so future runs never re-flag them. (Generated for every dict triaged.)

### The 4 FILE-FIRST candidates (still verify on the scan)

| wrong → right | MW gloss | why it's a likely typo |
|---|---|---|
| `kattfna → kattfRa` | "a fragrant grass" | *kattṛṇa*: after vocalic ṛ, **ṇatva** forces retroflex ṇ; dental n is anomalous |
| `Bawwaraka → BawwAraka` | "venerable" | the word is *bhaṭṭāraka* (long ā) |
| `akzAMsa → akzAMSa` | "a degree of latitude" | morpheme is *aṃśa* "portion" (ś); dental *aṃsa* = "shoulder" |
| `prativoDavya → prativoQavya` | "to be carried home" | gerundive of *prati-vah* is *voḍhavya* (ḍh) |

> These are **candidates**, not confirmed corrections. A digital-text typo and a faithful
> rendering of a print error look identical here; only the scanned page decides. Open the
> scan link, read the printed headword, and file only what the print contradicts.

## Why the raw engine output over-flags (worked examples — *corrected*)

An earlier version of this readme listed `marga → mArga`, `kiriwa → kirIwa`,
`mADu → maDu` as "likely file." **That was wrong**, and the body-grounded triage caught
it by reading the actual entries:

- `marga` — MW reads `<s>marga</s> ¦ <ab>w.r.</ab> for <s>mArga</s>` — an **intentional
  wrong-reading apparatus entry**. "Correcting" it deletes MW's scholarship.
- `kiriwa` — `See <s>ati-kir°</s>` — a **cross-reference** entry.
- `mADu` — `Vṛddhi form of maDu in comp.` — an **intentional vṛddhi-stem** lemma.
- `atrA` / `prAvft` — the `<k2>` (`a/-trA`, `prA-vft`) carries an accent/hyphen marking
  the long vowel as **editorial intent**.
- `vAcas` — the **genitive singular of *vāc*** "speech"; a valid inflected form.
- `muka` — MW glosses it `the smell of cow-dung`; a **real distinct word**, not a typo
  of *mūka* "dumb".

## Method (pipeline)

```sh
cd detectors
python triage_enrich.py            # attach k2 / DCS band / cross-dict / confusion evidence -> MW_evidence.jsonl
python triage_bodies.py            # attach each candidate's MW entry BODY from csl-orig + classify it
python triage_body_batches.py      # split the 'realword' set into body-aware batches
#  -> run the body-aware LLM workflow (classify TYPO/REALWORD/INTENTIONAL/UNSURE; confirm each TYPO vs source)
python triage_synthesize.py        # combine -> MW_triaged.txt + MW_file_first_sf.txt
```

The decisive signals: MW's **entry body** (real gloss vs `w.r.`/`v.l.`/`in comp.`/`See`),
the **`<k2>`** accent/hyphen field, **DCS** frequency of the suggestion, and **ṇatva /
morpheme** reasoning. The LLM layer is a *triage prior*, not a verdict — a human confirms
each kept case against the scanned page before anything is filed.

## Raw engine output (provenance — do NOT apply)

- [MW_candidates.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/MW/MW_candidates.txt) — the engine's 1,954 ranked tier-A candidates.
- [MW_draft.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/MW/MW_draft.txt) — draft updateByLine change-file for all 1,943 located
  candidates. **Superseded:** the triage shows ~99.8% should *not* be filed. Kept only as
  the engine's unfiltered output; use [MW_file_first_sf.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/MW/MW_file_first_sf.txt) instead.

## How to review → file

1. Open a FILE-FIRST case's scan link (`servepdf.php?dict=MW&key=<wrong>`); read the printed headword.
2. Print shows the suggestion's spelling → digitization typo → flip its line to `:y`.
3. Print shows the suspect spelling (or `<k2>`/body documents it) → drop the case.
4. File the kept cases per the [CORRECTIONS](https://github.com/sanskrit-lexicon/CORRECTIONS/issues)
   workflow (one issue per dictionary).

_Dr. Mārcis Gasūns_
