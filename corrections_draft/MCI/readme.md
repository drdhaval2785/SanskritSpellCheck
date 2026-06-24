# MCI correction candidates — BODY-GROUNDED triage (DRAFT for human review)

The unified detector engine flagged **41 tier-A** MCI headwords as possible misspellings. MCI is a
mythological-name index (deities, serpents, kings, tīrthas, peoples, rivers), glossed in English
with Mahābhārata references. Triaged against MCI's *own entry text* (from
[csl-orig](https://github.com/sanskrit-lexicon/csl-orig)).

## The finding

> **Of 41 engine "tier-A" candidates, 10 are body-confirmed fileable typos** — an unusually clean
> set: in each, the **bold headword lemma contradicts the entry's own repeated running citations**
> of the same name. 11 are real distinct names, 3 are documented-intentional.

The confirmation here is strong because MCI's entries quote the name many times in prose. E.g. the
headword is keyed `Mahānadi` (short i) but the body repeats *mahānadī* ("puṇyā caiva mahānadī");
`Dakṣināpatha` (dental n) but the prose has *dakṣiṇāpathavāsin* (retroflex ṇ); `Brahmopanisad`
(dental s) but *brahmopaniṣadaṃ* (retroflex ṣ); `Asvaśiras` but *cāśvaśiro / aśvaśiro* (aśva =
"horse"). These are headword keying errors, not the dictionary's intended spelling.

Cross-dict fileable precision: SHS 37/246 · YAT 27/247 · ACC 22/174 · PWG 12/497 · **MCI 10/41** ·
MW 4/1954 · … — MCI's small-but-rich entries make it proportionally high-yield.

## The FILE-FIRST queue (10 — verify on scan, then file)

[MCI_file_first_sf.txt](MCI_file_first_sf.txt) (`MCI:wrong:right:n`):
`mahAnadi→mahAnadI`, `supratika→supratIka`, `mAkandi→mAkandI`, `kikawa→kIkawa`, `baliha→balIha`
(vowel-length, ī); `dakzinApaTa→dakziRApaTa` (ṇatva); `asvaSiras→aSvaSiras`, `vEsAKa→vESAKa`,
`brahmopanisad→brahmopanizad` (sibilant s→ś/ṣ); `arunDatIvAwa→arunDatIvawa` (vaṭa "banyan", short a).
Each confirmed by the entry's own citations and source-reviewed (no apparatus, correct direction);
still **DRAFT** — verify the Devanāgarī scan before flipping `n`→`y`.

## The authoritative artifacts

- **[MCI_file_first_sf.txt](MCI_file_first_sf.txt)** — 10 FILE-FIRST candidates.
- **[MCI_wrong_readings.txt](MCI_wrong_readings.txt)** — do-not-file: 3 (cross-reference 2, other 1).
  Folded into [nochange/do_not_file_suppress.txt](../../nochange/do_not_file_suppress.txt).
- **[MCI_triaged.txt](MCI_triaged.txt)** — full queue: 10 FILE-FIRST, 11 REAL-WORD, 3 INTENTIONAL.

## Method

`detectors/triage_dict.py MCI` → body-aware classification (English) → **source-confirm + review**
of every TYPO against its full MCI entry (citations confirmed the headword/lemma mismatch) →
`--finish`. **DRAFT for human review; never edits `csl-orig`.**
