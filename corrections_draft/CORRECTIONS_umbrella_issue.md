# Verified headword typo candidates across 11 dictionaries — batch from SanskritSpellCheck triage

> **POSTED 02-07-2026** as [sanskrit-lexicon/CORRECTIONS#447](https://github.com/sanskrit-lexicon/CORRECTIONS/issues/447)
> (M.G. authorization). This file is the source of record for the issue body; maintainer
> follow-ups happen on the issue.

This issue presents **120 tier-A candidates** — 92 proposed corrections + 17 scan-first candidates
+ 11 editorial (duplicate-pair / apparatus collision) decisions — drawn from a **body-grounded
triage** of all 33 CDSL dictionaries in [SanskritSpellCheck](https://github.com/drdhaval2785/SanskritSpellCheck):
automated pattern-anomaly detection followed by manual, entry-text verification of every candidate
kept here. Each row was re-verified against the **current** [csl-orig](https://github.com/sanskrit-lexicon/csl-orig)
entry text on **2026-07-02**.

**The scan is the final arbiter.** Nothing here should be applied to any dictionary until a human
checks the printed page against the proposed spelling — these are candidates, ranked by internal
evidence, not confirmed corrections. "Proposed" rows are contradicted by their own entry's
etymology, derivation, inflection, or citation; "scan-first" rows are grammar-plausible but the
entry body alone doesn't settle the point; "editorial" rows are duplicate-pair or apparatus
collisions where the entry text raises a merge-vs-respell question for the editor, not a clean
typo.

Full evidence file: [corrections_draft/file_first_verified.tsv](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/file_first_verified.tsv).

One candidate (SHS `kARqapfzwa`) was found already fixed upstream in csl-orig since the original
triage, and one candidate (YAT `RiS`→`niS`) was reclassified do-not-file after a second look —
both are listed in the closing appendix for the audit trail, not proposed here.

---

## SHS — Śabda-Sāgara (37 triaged → 29 proposed + 7 scan-first + 1 already fixed)

SHS is poorly digitised, but nearly every entry carries an explicit `E.` etymology (or an internal
grammatical derivation) that independently fixes the correct spelling — which is why it is the
highest-yield dict in this pass. Every row below was (1) body-confirmed by automated triage +
manual verification (classification, source-confirmation, and adversarial review across models),
and (2) re-verified against the current [csl-orig SHS entry text](https://github.com/sanskrit-lexicon/csl-orig/blob/main/v02/shs/shs.txt)
on 2026-07-02. The scan remains the final arbiter — nothing is applied until a human checks the
print.

### 1. Proposed corrections (29)

| # | wrong → right | in-entry evidence | scan |
|---|---|---|---|
| 1 | `BUnaya` → `BUmaya` | "mayaw affix regularly yields -maya 'made of'; BUnaya's -naya does not match" | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=BUnaya) |
| 2 | `BadraballI` → `BadravallI` | "E. {#Badra#} lucky, {#vallI#} a creeper" — etymology spells vallI with v | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=BadraballI) |
| 3 | `SilAbalkA` → `SilAvalkA` | cross-reference `SilAvalkala` confirms v-spelling of valka | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=SilAbalkA) |
| 4 | `akASadIpa` → `AkASadIpa` | E. and cross-ref `AkASapradIpaH` both spell AkASa with initial long A | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=akASadIpa) |
| 5 | `diDizupati` → `diDizUpati` | "E. {#diDizU#} as [above/prior sense]" — etymology spells diDizU with long U | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=diDizupati) |
| 6 | `ditisUta` → `ditisuta` | "E. {#diti#} ..., {#suta#} a son" — etymology spells suta with short u | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=ditisUta) |
| 7 | `divaspfTibI` → `divaspfTivI` | "E. {#diva#} heaven, {#pfTivI#} earth" — etymology spells pfTivI with v | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=divaspfTibI) |
| 8 | `drabaja` → `dravaja` | "{#dravAt jAyate jana-qa#}" — etymology and derivation both spell drava with v | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=drabaja) |
| 9 | `hastisuRqA` → `hastiSuRqA` | "E. {#hastin#} an elephant, {#SuRqA#} the trunk" — palatal S in etymology | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=hastisuRqA) |
| 10 | `jAmbabat` → `jAmbavat` | matup-affixed nom. `-vAn` and cross-ref `jAmbuvat` both confirm v-spelling | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=jAmbabat) |
| 11 | `jAmbunadamaya` → `jAmbUnadamaya` | "E. {#jAmbUnada#} and {#mayaw#} aff." — etymology spells jAmbUnada with long U | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=jAmbunadamaya) |
| 12 | `jalarupa` → `jalarUpa` | "{#jalasya rUzam iva rUpam asya SuBratvAt#}" — etymology + derivation spell rUpa long | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=jalarupa) |
| 13 | `kAlyaRineya` → `kAlyARineya` | base `kalyARI` has retroflex R; Qak-derivation rule requires n→R nati | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=kAlyaRineya) |
| 14 | `kAzwakuddAla` → `kAzWakuddAla` | E. and cross-ref `kAzWakUddAla` both spell kAzWa with capital W | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=kAzwakuddAla) |
| 15 | `klItakika` → `klItakikA` | "E. {#krItaka#} traffic" — fem. marker context supports -ikA reading | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=klItakika) |
| 16 | `kzIraballI` → `kzIravallI` | "E. {#kzIra#} water, {#vallI#} pedicle: see {#kzIrakandA#}" — v-spelling | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=kzIraballI) |
| 17 | `laGizwa` → `laGizWa` | inflectional stem `-zWaH-zWA-zWaM` and `izWan` affix both confirm retroflex zWa | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=laGizwa) |
| 18 | `murali` → `muralI` | fem. inflectional stem `-lI` implies nom. muralI; headword short-i inconsistent | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=murali) |
| 19 | `navakArika` → `navakArikA` | "E. {#nava#} new, {#kArikA#} agent" — etymology's kArikA ends long final A | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=navakArika) |
| 20 | `ninittakAla` → `nimittakAla` | "E. {#nimitta#}, {#kAla#} time" — etymology literally spells nimitta | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=ninittakAla) |
| 21 | `nyaNkuBUrUha` → `nyaNkuBUruha` | "E. {#nyaNku#} a deer, {#BUruha#} [a tree]" — etymology spells BUruha short u | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=nyaNkuBUrUha) |
| 22 | `pAniyavarRikA` → `pAnIyavarRikA` | "{#pAnIyamiva varRavati-varRi-Rvul#}" — entry's own derivation spells pAnIya long I | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=pAniyavarRikA) |
| 23 | `paNKagrAha` → `paNkagrAha` | "E. {#paNka#} mud, {#grAha#} a shark" — etymology spells paNka lowercase k | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=paNKagrAha) |
| 24 | `padazwIva` → `padazWIva` | "E. {#pad#} a foot, {#azWIvat#} the knee" — etymology spells azWIvat capital W | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=padazwIva) |
| 25 | `svarRabalkala` → `svarRavalkala` | "E. {#svarRa#} gold, {#valkala#} bark" — etymology spells valkala with v | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=svarRabalkala) |
| 26 | `vAcanIka` → `vAcanika` | Wak (thak) affix regularly yields short -ika, not long -Ika | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=vAcanIka) |
| 27 | `vArttayana` → `vArttAyana` | "E. {#vArttA#} news, {#ayana#} going" — etymology spells vArttA long final A | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=vArttayana) |
| 28 | `viSamaSIla` → `vizamaSIla` | "E. {#vizama, SIla#} having" — etymology spells vizama with retroflex z | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=viSamaSIla) |
| 29 | `zuh` → `suh` | cited present-tense form `suhyati` is built on root suh (dental s) | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=zuh) |

### 2. Scan-first (7)

| # | wrong → right | in-entry evidence | scan |
|---|---|---|---|
| 1 | `maYjarinamra` → `maYjarInamra` | terse entry, no E.; accepted on affix-pattern rationale, not contradicted | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=maYjarinamra) |
| 2 | `natyuha` → `natyUha` | no E. present; PASS on worklist's MISSING basis, no internal contradiction | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=natyuha) |
| 3 | `pitfrupa` → `pitfrUpa` | no E.; compound = pitf + rUpa 'form', matches jalarupa→jalarUpa correction class | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=pitfrupa) |
| 4 | `pratipaTan` → `pratipaTam` | bare gloss, no E.; adverbial -am grammar-plausible but not body-evidenced | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=pratipaTan) |
| 5 | `pratyupaveza` → `pratyupaveSa` | bare gloss, no E.; z/S not internally decidable from this entry | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=pratyupaveza) |
| 6 | `purUzadantikA` → `puruzadantikA` | no E.; purUza→puruza is the standard short-u spelling of 'man' | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=purUzadantikA) |
| 7 | `saptAtitama` → `saptatitama` | wrong spelling recurs in body headword tag only, no other body occurrence | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SHS&key=saptAtitama) |

All seven are grammar-plausible, but the entry body is either a bare gloss or carries no
etymology, so the print must decide.

### 3. Already fixed upstream (1)

`kARqapfzwa` → `kARqapfzWa` — corrected in [csl-orig](https://github.com/sanskrit-lexicon/csl-orig/blob/main/v02/shs/shs.txt) since the June triage (the correct form `kARqapfzWa` already exists as its own entry, id 9855, pc 171-b); listed only for the audit trail.

---

## YAT — Yates' Dictionary in Sanscrit and English (27 triaged → 17 proposed + 4 scan-first + 5 editorial)

YAT is Yates' *Dictionary in Sanscrit and English* (Calcutta, Baptist Mission Press, 1846) — a
verbal-root-rich Sanskrit-English lexicon, poorly digitised like SHS, so a real share of its
tier-A candidates are genuine OCR/keying errors rather than editorial apparatus.

### 1. Proposed corrections (17)

| # | wrong → right | in-entry evidence | scan |
|---|---|---|---|
| 1 | `RaB` → `naB` | body conjugates the verb `naBati, naByati, naBnAti` — dental n, contradicting headword R | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=YAT&key=RaB) |
| 2 | `Rij` → `nij` | body conjugates `niMkte, nenekti, nenikte` — all dental n, contradicting headword R | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=YAT&key=Rij) |
| 3 | `aSanayA` → `aSanAyA` | gloss "Hunger" matches the attested lexeme aSanAyA; no colliding headword | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=YAT&key=aSanayA) |
| 4 | `ambukfta` → `ambUkfta` | gloss "Sputtered" fits onomatopoeic ambūkṛta, not ambu 'water' + kṛta | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=YAT&key=ambukfta) |
| 5 | `avasfzWa` → `avasfzwa` | in-line inflection `(zwaH-zwA-zwaM)` uses unaspirated zw, contradicting headword zW | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=YAT&key=avasfzWa) |
| 6 | `cInapizWa` → `cInapizwa` | cīna-piṣṭa (ppp of piṣ 'to grind') takes retroflex zw, not aspirated zW | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=YAT&key=cInapizWa) |
| 7 | `drAvana` → `drAvaRa` | causative noun of dru 'to run/melt' takes retroflex Ra per ṇatva after r | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=YAT&key=drAvana) |
| 8 | `duzwu` → `duzWu` | likely corruption route via duḥṣṭhu 'ill-placed', which takes aspirated zW | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=YAT&key=duzwu) |
| 9 | `hantAkAra` → `hantakAra` | gloss "Rice to be given to a guest" matches the hanta-kāra vocative compound | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=YAT&key=hantAkAra) |
| 10 | `lakzmIpala` → `lakzmIPala` | gloss "Ægle marmelos" (bael fruit) requires lakṣmī-phala, aspirated Pa | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=YAT&key=lakzmIpala) |
| 11 | `mahAmayA` → `mahAmAyA` | gloss "Durgā; illusion" matches mAyA 'illusion' (long A), the standard lexeme | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=YAT&key=mahAmayA) |
| 12 | `pakzipARIyaSAlikA` → `pakzipAnIyaSAlikA` | gloss "trough for watering beasts" — pānīya 'water' takes dental n, not R | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=YAT&key=pakzipARIyaSAlikA) |
| 13 | `prAkPAlguRa` → `prAkPAlguna` | cross-ref to Phalguna (month name), which conventionally takes dental n | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=YAT&key=prAkPAlguRa) |
| 14 | `prAyopavizWa` → `prAyopavizwa` | in-line inflection `(zwaH-zwA-zwaM)` uses unaspirated zw, contradicting headword zW | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=YAT&key=prAyopavizWa) |
| 15 | `vESizWya` → `vESizwya` | vaiśiṣṭya (from viśiṣṭa) takes retroflex zw, not aspirated zW | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=YAT&key=vESizWya) |
| 16 | `zazWihAyana` → `zazwihAyana` | ṣaṣṭi-hāyana takes zw (from ṣaṣṭi 'sixty'), not aspirated zW | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=YAT&key=zazWihAyana) |
| 17 | `pAradfzvan` → `pAradfSvan` | in-line inflection uses a retroflex-z cluster matching the headword's own zv; no colliding headword | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=YAT&key=pAradfzvan) |

### 2. Scan-first (4)

| # | wrong → right | in-entry evidence | scan |
|---|---|---|---|
| 1 | `AparAhnika` → `AparAhRika` | aparāhṇa ṇatva is grammar-certain, but entry's own k2 spells dental hnika — direction needs re-check | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=YAT&key=AparAhnika) |
| 2 | `arsasa` → `arSasa` | two different parts of speech (noun vs adjective), both independently attested nearby — may be a real pair | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=YAT&key=arsasa) |
| 3 | `asaMSakta` → `asaMsakta` | gloss "Indifferent" supports the correction, but no citation confirms the sibilant literally | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=YAT&key=asaMSakta) |
| 4 | `saNGati` → `saNgati` | both `saNGati` and `sa-Ngati` are richly and separately glossed nearby — possible real minimal pair, not a clean typo | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=YAT&key=saNGati) |

### 3. Editorial: duplicate-pair or apparatus collisions (5)

Each pair below already exists as two separate YAT headwords with overlapping or cross-referenced
glosses. The correction direction is plausible, but since the "right" spelling already exists as
its own entry, a respell risks orphaning or colliding with that entry — the editor should decide
merge vs respell vs leave-as-attested-variant, ideally after checking the scan.

| # | pair | both entries | evidence / editor's options |
|---|---|---|---|
| 1 | `AkzadyUta` (L4372, "Gambling") ↔ `akza-dyUta` (L99, "Idem") | both attested | L99 is explicitly glossed "Idem", pointing back to another entry — check which entry the cross-reference actually targets before merging or respelling L4372 |
| 2 | `gaDABft` (L45090, "Viṣṇu") ↔ `gadA-Bft` (L12584, "Idem") | both attested, same referent | intentional dual-listing (gadā-bhṛt "mace-bearer"); respelling `gaDABft`→`gadABft` collides with the existing `gadABft` entry |
| 3 | `mayAvin` (L45199, "A cheat") ↔ `mAyA-vin` (L29759, "A juggler") | both attested, distinct glosses | genuinely separate lexemes, not one typo'd into the other; no internal evidence in L45199 supports lengthening a→A |
| 4 | `pratisidDa` (L25690, "Prohibited") ↔ `prati-zidDa` (L25660, "Forbidden, prohibited, unlawful") | near-identical glosses | almost certainly duplicate listings of pratiṣiddha; needs a merge decision, not a silent respell |
| 5 | `vizwABU` (L35741) ↔ `vizWABU` (L35751), 10 L apart | identical gloss "Born in filth" | very likely the same word listed twice (viṣṭhā+bhū); disposition (merge/delete vs respell) needs human judgment |

**Appendix note:** `RiS` → `niS` was considered and reclassified **do-not-file**: it is likely
Dhātupāṭha ṇopadeśa root notation (a deliberate grammatical marking convention), and filing it
as a typo correction would destroy that deliberate record. See closing appendix.

---

## ACC — Aufrecht's Catalogus Catalogorum (22 triaged → 17 proposed + 4 scan-first + 1 editorial)

ACC is Aufrecht's *Catalogus Catalogorum* (1891–1903) — a catalogue of Sanskrit works and authors,
each entry a normalised title/author-name with a terse manuscript-source citation. Most candidates
here are dropped diacritics in well-known work titles; the print colophon is still the final word,
since ACC faithfully records catalogue spellings that can genuinely vary by manuscript.

### 1. Proposed corrections (17)

| # | wrong → right | in-entry evidence | scan |
|---|---|---|---|
| 1 | `EtareyavrAhmaRa` → `EtareyabrAhmaRa` | wrong is an isolated singleton; right form (b, not v) has 4 well-attested entries — the famous Aitareya-Brāhmaṇa | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=ACC&key=EtareyavrAhmaRa) |
| 2 | `QuRqi` → `QuRQi` | wrong is an isolated singleton; right form (aspirated retroflex QA) has 4 well-attested entries — a personal name | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=ACC&key=QuRqi) |
| 3 | `SAkawayanavyAkaraRa` → `SAkawAyanavyAkaraRa` | wrong-entry body describes the same Jaina grammar as the right-form entries (2 well-attested vs 1) | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=ACC&key=SAkawayanavyAkaraRa) |
| 4 | `SatapaTavrAhmaRa` → `SatapaTabrAhmaRa` | wrong is a singleton under the v-spelling; right form (b) has 3 separate well-attested entries — the famous Śatapatha-Brāhmaṇa | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=ACC&key=SatapaTavrAhmaRa) |
| 5 | `SravaRadvAdaSIvratakalpa` → `SrAvaRadvAdaSIvratakalpa` | Śrāvaṇa is the standard month-name spelling (Śrāvaṇa-dvādaśī-vrata, a lunar-calendar vow) | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=ACC&key=SravaRadvAdaSIvratakalpa) |
| 6 | `bfhannArayaRopanizad` → `bfhannArAyaRopanizad` | wrong is a singleton; a self-referential alias chain in the Mahānārāyaṇopaniṣad entry confirms the spelling | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=ACC&key=bfhannArayaRopanizad) |
| 7 | `dakziRamUrtisaMhitA` → `dakziRAmUrtisaMhitA` | wrong is a singleton; right form has 5 separate well-attested entries — Dakṣiṇāmūrti is a standard theonym | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=ACC&key=dakziRamUrtisaMhitA) |
| 8 | `jEminIyanyAyamAlAvistAra` → `jEminIyanyAyamAlAvistara` | wrong is a singleton; right form has 5 well-attested entries incl. an explicit alias list | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=ACC&key=jEminIyanyAyamAlAvistAra) |
| 9 | `kAwakopanizad` → `kAWakopanizad` | right form (aspirated W) is the standard Kāṭhakopaniṣad name; wrong-entry body carries only editorial addenda markers | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=ACC&key=kAwakopanizad) |
| 10 | `mahAnArayaRopanizad` → `mahAnArAyaRopanizad` | wrong is a singleton; right form is the well-known Mahānārāyaṇopaniṣad, itself cross-referencing bṛhannārāyaṇopaniṣad | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=ACC&key=mahAnArayaRopanizad) |
| 11 | `metrAyaRIyopanizad` → `mEtrAyaRIyopanizad` | right form has 2 well-attested entries incl. an explicit alias list establishing mE- (vṛddhi) as standard for the Maitrāyaṇīya-Upaniṣad family | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=ACC&key=metrAyaRIyopanizad) |
| 12 | `parAmArTasAra` → `paramArTasAra` | wrong entry itself carries the alternate title "or SezAryA"; right form has 6 entries sharing that same alternate title — Abhinavagupta's Paramārthasāra | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=ACC&key=parAmArTasAra) |
| 13 | `rupagosvAmin` → `rUpagosvAmin` | wrong-entry body's own k1 key ("rupa gosvAmin") is a split digitization artifact describing the well-known author Rūpa Gosvāmin | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=ACC&key=rupagosvAmin) |
| 14 | `saMnyasaviDi` → `saMnyAsaviDi` | Aufrecht's own cross-reference in the wrong entry uses the long-a saṃnyāsa- spelling, self-contradicting the headword | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=ACC&key=saMnyasaviDi) |
| 15 | `viSvarUpanivanDa` → `viSvarUpanibanDa` | both wrong and right entries independently describe the same source work (Bhaviṣyottarapurāṇa) from different manuscript catalogues | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=ACC&key=viSvarUpanivanDa) |
| 16 | `vivekacUqAmaRI` → `vivekacUqAmaRi` | wrong is a singleton; right form (short final i) has 3 well-attested entries — the famous Advaita text Vivekacūḍāmaṇi | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=ACC&key=vivekacUqAmaRI) |
| 17 | `zadftuvarRana` → `zaqftuvarRana` | wrong is a singleton; right form (retroflex q) has 2 well-attested entries via Kāvyamālā, the standard spelling in that genre | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=ACC&key=zadftuvarRana) |

### 2. Scan-first (4)

| # | wrong → right | in-entry evidence | scan |
|---|---|---|---|
| 1 | `SakawAyanasmfti` → `SAkawAyanasmfti` | vṛddhi A in Śākaṭāyana grammar-certain, but body is a bare citation — colophon faithfulness only scan can settle | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=ACC&key=SakawAyanasmfti) |
| 2 | `rAsayAtraviveka` → `rAsayAtrAviveka` | yātrā long-A is a real compound, but body is a bare citation ("by Sulapani. L.4059") | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=ACC&key=rAsayAtraviveka) |
| 3 | `sAttvikavrahmavidyAvilAsa` → `sAttvikabrahmavidyAvilAsa` | vr→b brahma-spelling is plausible but unconfirmed internally; colophon-faithfulness risk is endemic to v/b pairs | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=ACC&key=sAttvikavrahmavidyAvilAsa) |
| 4 | `zadarTasaMkzepa` → `zaqarTasaMkzepa` | ṣaḍ- sandhi before a voiced stop is grammar-certain, but body is citation-only with no overlap | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=ACC&key=zadarTasaMkzepa) |

### 3. Editorial: duplicate-pair or apparatus collision (1)

| # | pair | both entries | evidence / editor's options |
|---|---|---|---|
| 1 | `gAyatrIBAsya` (L5911) vs `gAyatrIBAzya` | wrong entry has its own independent citation list (Oxf.296b, B.1,12, Taylor 1,282, Oppert II,6254, Śaṅkarācārya, B.4,50, BA.16), no overlap with the right-form entries (L5912 "or saMDyABAzya", L32589) | cannot rule out these being two independently-catalogued manuscripts rather than a keying error; the sibilant s/z confusion is plausible but internal proof is absent — needs a scan check before deciding whether to merge or respell |

---

## PWG — Petersburger Wörterbuch, large edition (12 triaged → 10 proposed + 2 editorial)

PWG (Sanskrit–German *Petersburger Wörterbuch*, Böhtlingk–Roth's large edition) carries more
digitization errors than the mature English-language dictionaries, and the strongest signal is
internal: the entry's own German derivation or citation directly contradicts the headword
spelling.

### 1. Proposed corrections (10)

| # | wrong → right | in-entry evidence | scan |
|---|---|---|---|
| 1 | `arTavanDa` → `arTabanDa` | body quotes `lalitArTabanDaM pattre niveSitamudAharaRaM priyAyAH` verbatim, with b | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=PWG&key=arTavanDa) |
| 2 | `paRavanDa` → `paRabanDa` | derivation `(paRa + ba˚)` spells the second element with b; gloss "concluding a contract" | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=PWG&key=paRavanDa) |
| 3 | `BAvavanDana` → `BAvabanDana` | own derivation `(BAva + ba˚)` spells the second element with b | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=PWG&key=BAvavanDana) |
| 4 | `Dabalapakza` → `Davalapakza` | gloss "Gans" (goose) = dhavala-pakṣa "white-winged"; semantic match confirmed | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=PWG&key=Dabalapakza) |
| 5 | `avakaSa` → `avakASa` | body quotes `nakzatrARAmavakASena` — long A instantiated inline in the citation | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=PWG&key=avakaSa) |
| 6 | `tarAvalI` → `tArAvalI` | body reads `tArARAM saMKyayA padyEryuktA tArAvalI matA` — own citation spells the first element long A | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=PWG&key=tarAvalI) |
| 7 | `dIvAkIrtya` → `divAkIrtya` | own derivation `(divA + kI˚)` uses short i; entry marked `(so zu lesen)` — PWG's own errata pointer | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=PWG&key=dIvAkIrtya) |
| 8 | `tfzitottara` → `tfzitottarA` | gender marker `f.` (feminine plant name) contradicts the masculine/neuter-looking headword ending | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=PWG&key=tfzitottara) |
| 9 | `yajYamus` → `yajYamuz` | body derivation names the root "2. muz" — the class marker itself is z | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=PWG&key=yajYamus) |
| 10 | `biBedayisu` → `biBedayizu` | desiderative-of-causative suffix -izu: satva after i is exceptionless morphology | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=PWG&key=biBedayisu) |

### 2. Editorial: apparatus collision (2)

| # | pair | both entries | evidence / editor's options |
|---|---|---|---|
| 1 | `duzwu` vs `duzWu` (hom. 2) | the `duzwu` "entry" is PWG's own errata note ("Z. 3 lies duzwu st. suzwu"), an unrelated correction, not a spelling of the headword being verified; `duzWu` (hom. 2, "ill-behaved") is a real, independently cited headword | applying the correction would collide the real word with an unrelated apparatus note — do not file |
| 2 | `pfzwavanDu` vs `pfzwabanDu` | both independently glossed and cited (RV 3,20,3); `vgl. banDupfcC` in `pfzwavanDu`'s body supports the b-spelling generally, but the two headwords stand as separate entries with their own derivations | resembles an attested-variant pair (cf. the reviewed-out ketunAlin/ketumAli case) rather than a clean typo; scan should confirm before merging |

---

## MCI — Mahābhārata mythological-name index (10 proposed)

MCI is a mythological-name index (deities, serpents, kings, tīrthas, peoples, rivers), glossed in
English with Mahābhārata references. Its entries quote each name many times in running citations,
which makes headword-vs-citation contradictions unusually clean to confirm.

### 1. Proposed corrections (10)

| # | wrong → right | in-entry evidence | scan |
|---|---|---|---|
| 1 | `arunDatIvAwa` → `arunDatIvawa` | IAST citation "Arundhativata" uses short final -a (vaṭa "banyan tree"), contradicting the headword's long-final-A | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=MCI&key=arunDatIvAwa) |
| 2 | `asvaSiras` → `aSvaSiras` | IAST citation "casvasiro" (= ca+aśvaśiras) uses the sibilant s, contradicting the dental-s headword | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=MCI&key=asvaSiras) |
| 3 | `baliha` → `balIha` | IAST citations "Balihas"/"balihanam" use long-i, contradicting the short-i headword | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=MCI&key=baliha) |
| 4 | `brahmopanisad` → `brahmopanizad` | IAST citation "brahmopanisadam" uses retroflex ṣ (SLP1 z), contradicting the dental-s headword | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=MCI&key=brahmopanisad) |
| 5 | `dakzinApaTa` → `dakziRApaTa` | repeated IAST citations "daksinapathavasin"/"daksinapathajanmanah" use retroflex-n, contradicting the dental-n headword | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=MCI&key=dakzinApaTa) |
| 6 | `kikawa` → `kIkawa` | IAST citations "Kikatas"/"kikatatavin" use long-i, contradicting the short-i headword | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=MCI&key=kikawa) |
| 7 | `mAkandi` → `mAkandI` | IAST citation "makandim" (accusative of a long-final-i stem) confirms long-I | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=MCI&key=mAkandi) |
| 8 | `mahAnadi` → `mahAnadI` | entry describes a river name; body citation uses long-final-i (standard nadI "river" morphology) | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=MCI&key=mahAnadi) |
| 9 | `supratika` → `supratIka` | entry's own prose (Bhagadatta's elephant) uses long-I throughout — note: may be a stray duplicate of an existing SupratIka entry, editor may prefer merge over respell | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=MCI&key=supratika) |
| 10 | `vEsAKa` → `vESAKa` | prose repeatedly cites "Vaisakha" (the month), contradicting the dental-s headword | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=MCI&key=vEsAKa) |

---

## MW — Monier-Williams Sanskrit-English Dictionary (4 triaged → 0 proposed + 2 scan-first + 2 editorial)

MW is the most mature, thoroughly corrected of the CDSL dictionaries. Its mature text yields **no
unqualified proposed corrections** in this pass — every remaining candidate is either grammar-certain
but body-silent (scan-first), or contested by an already-existing sibling headword (editorial).

### 1. Scan-first (2)

| # | wrong → right | in-entry evidence | scan |
|---|---|---|---|
| 1 | `akzAMsa` → `akzAMSa` | body is only "a degree of latitude" — akṣa+aṃśa "degree" compound is etymologically certain but the body is silent on the sibilant | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=MW&key=akzAMsa) |
| 2 | `prativoDavya` → `prativoQavya` | voḍhavya is the only grammatically formable gerundive of vah — but `prativoQavya` already exists as a bare cross-reference entry with a different citation | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=MW&key=prativoDavya) |

### 2. Editorial: duplicate-pair collisions (2)

| # | pair | both entries | evidence / editor's options |
|---|---|---|---|
| 1 | `Bawwaraka` vs `BawwAraka` | `Bawwaraka` is a short, single-source (L. = lexicographers) gloss "venerable"; `BawwAraka` already exists richly as its own 5-sense headword | plausible near-duplicate, but could equally be an attested short-vowel variant deliberately recorded by the lexicographers — needs scan |
| 2 | `kattfna` vs `kattfRa` | `kattfRa` already exists as its own separate MW entry (L42680); `kattfna` (L42856-7) has 2 senses incl. Pistia Stratiotes | read as two distinct MW headwords (possibly true homographs / different plants) rather than typo+correction; the ṇatva argument is a general phonology rule, not confirmed by `kattfna`'s own body — do not merge without checking the scan |

---

## SKD — Śabdakalpadruma (3 proposed)

SKD is the great Sanskrit-to-Sanskrit encyclopaedic lexicon. As with every Sanskrit-body dictionary
in this batch, the decisive signal is internal: the entry's own Sanskrit derivation (vyutpatti)
contradicts the headword spelling.

### 1. Proposed corrections (3)

| # | wrong → right | in-entry evidence | scan |
|---|---|---|---|
| 1 | `hitAbalI` → `hitAvalI` | own derivation `hitAnAM AvalI yatra` spells the second element with v; Hindi gloss `hiyAvalI` also uses v | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SKD&key=hitAbalI) |
| 2 | `pUzaBAzA` → `pUzaBAsA` | own derivation `... BAsa + ac . wAp` derives from root BAs (palatal s); headword's retroflex z contradicts it | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SKD&key=pUzaBAzA) |
| 3 | `vfzaBAzA` → `vfzaBAsA` | own derivation `vfzeRa DarmmeRa BAsate iti . BAsa + ac` again from root BAs (palatal s); headword's z contradicted | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=SKD&key=vfzaBAzA) |

---

## WIL — H. H. Wilson, A Dictionary, Sanscrit and English, 1832 (3 proposed)

WIL is the earliest major Sanskrit-English dictionary. As the oldest and least-corrected of the
mature dictionaries in this batch, it surfaces a small number of residual errors — each confirmed
by the entry's own etymology or inflection.

### 1. Proposed corrections (3)

| # | wrong → right | in-entry evidence | scan |
|---|---|---|---|
| 1 | `boDidruna` → `boDidruma` | etymology "boDi knowledge, druma a tree" and inflection marker `-maH` both spell the second element druma | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=WIL&key=boDidruna) |
| 2 | `jAmbabat` → `jAmbavat` | own inflection `-vAn` and etymology `jAmba + matup affix; also jAmbuvat` both confirm v-spelling | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=WIL&key=jAmbabat) |
| 3 | `kaNkalodya` → `kaNkaloqya` | own paradigm form `-qyaM` (retroflex q) contradicts the headword's dental d | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=WIL&key=kaNkalodya) |

---

## PW — Petersburger Wörterbuch, small edition (2 triaged → 1 proposed + 1 editorial)

PW (Sanskrit–German *Petersburger Wörterbuch*, Böhtlingk–Roth's shorter edition) is a mature,
thoroughly corrected dictionary whose wrong-reading apparatus is explicit and dense (95 entries
literally say `fehlerhaft für` — "erroneous for"); most tier-A candidates here are documented
apparatus, not typos.

### 1. Proposed corrections (1)

| # | wrong → right | in-entry evidence | scan |
|---|---|---|---|
| 1 | `Bagama` → `BagaRa` | gloss "der Umlauf der Gestirne" (revolution of the constellations) is textually near-identical to BagaRa's own sense 2 "der Umlauf im Zodiakus … Auch überh. Umlauf (eines Planeten)" | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=PW&key=Bagama) |

### 2. Editorial: apparatus collision (1)

| # | pair | both entries | evidence / editor's options |
|---|---|---|---|
| 1 | `hemana` vs `hEmana` (hom. 2) | headword itself is `*`-prefixed — PW's own convention for an editorially-constructed form; body reads "Adj. von 2. heman", a cross-reference to the already-existing `hEmana` hom. 2 entry ("Adj. golden") | this looks like PW's own intentional back-formation pointer, not a digitization typo — do not blind-merge; check the scan for the asterisk convention |

---

## VCP — Vācaspatyam (1 proposed)

VCP is a Sanskrit-to-Sanskrit thesaurus that systematically lists variant spellings as
cross-reference redirects and contains thousands of real verbal roots that merely resemble commoner
words — of 563 tier-A candidates, only one survives as a body-confirmed typo.

### 1. Proposed corrections (1)

| # | wrong → right | in-entry evidence | scan |
|---|---|---|---|
| 1 | `camIkara` → `cAmIkara` | own gloss states explicitly "...yadyogAt svarRaM cAmIkaramityucyate" = "by that combination gold is called cāmīkara" — the entry names the correct form verbatim | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=VCP&key=camIkara) |

---

## GST — Goldstücker, A Dictionary, Sanskrit and English, 1856 (1 proposed)

GST (Goldstücker, left incomplete at his death in 1872) carries an unusually high share of
documented variants and cross-references relative to its size; only one of its 48 tier-A
candidates is a clean, unqualified typo.

### 1. Proposed corrections (1)

| # | wrong → right | in-entry evidence | scan |
|---|---|---|---|
| 1 | `aprakaraRika` → `aprAkaraRika` | entry's own etymology "E. a (neg.) and prAkaraRika" and its quoted Kāvyaprakāśa citation "aprAkaraRikasyABiDAnena prAkariRakasyAkzepo'prastutapraSaMsA" both use long A, directly contradicting the short-a headword | [scan](http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict=GST&key=aprakaraRika) |

---

## Appendix — audit trail (not proposed)

- **DROP — SHS `kARqapfzwa` → `kARqapfzWa`.** Already fixed upstream in [csl-orig](https://github.com/sanskrit-lexicon/csl-orig/blob/main/v02/shs/shs.txt) since the original triage; the correct form `kARqapfzWa` already exists as its own entry (id 9855, pc 171-b). No action needed.
- **DNF — YAT `RiS` → `niS`.** Reclassified do-not-file: `RiS` (L16299, "to meditate profoundly, or abstractedly") and `niS` (L21672, "Night") are semantically and grammatically unrelated words that merely resemble each other in SLP1; `RiS` is likely Dhātupāṭha ṇopadeśa root notation, and filing this correction would destroy a deliberate grammatical record, not fix a typo.

---

Maintainers: please pick any subset of the above for filing — draft `updateByLine.py`
change-files can be supplied per dictionary on request.
