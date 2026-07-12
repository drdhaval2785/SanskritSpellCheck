# GRETIL e-text corrections — verified upstream report

_Created: 10-07-2026 · Last updated: 10-07-2026_

The hand-verified curation of [GRETIL_TEXT_TYPOS.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/meter/GRETIL_TEXT_TYPOS.md)'s
candidate list, prepared for upstream report to GRETIL (gretil@sub.uni-goettingen.de) per
ruling D8 in [ROADMAP_2026_2027.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ROADMAP_2026_2027.md)
and [H456](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H456-Sonnet_SanskritSpellCheck_gretil-typo-report-upstream_10.07.26.md).
**Every row below was re-checked against the raw GRETIL e-text line by a human-review pass**
(Fable 5 `claude-fable-5`, 10-07-2026; raw corpus fetched 06/07-07-2026): all 124 flagged loci
from the five `ngram_typos_*.tsv` files were pulled with their full verse context and
adjudicated one by one. Where the correct reading is not certain, the line is listed as
*anomalous* without a proposed fix — the editors know their sources better than we do.
Detection method: MW∩PW headword-bigram screening over ~101k tokens of five corpus sections
(see the candidates doc); everything the screen flagged that is *not* below is classified in
§9 with the reason it is not GRETIL's error.

**Summary: 60 verified error loci across 7 e-texts, of which 29 fall into three systematic
classes** (ḥ-for-vowel encoding corruption, *agrya*→*agyra* transposition, intrusive vowel);
11 further loci are anomalous with an uncertain correct reading; 53 flags are false positives
of documented kinds (§9), including every mantra/bīja syllable, BHS orthography, editorial
apparatus, and lacuna marker the screen tripped on.

## 1. `sa_vAlmIki-rAmAyaNa-southern-2.txt` — systematic ṝ → ḥ corruption (9 loci)

The ṝ-stem genitive/accusative plurals are written with visarga `ḥ` where vocalic `ṝ`
belongs — one encoding-conversion slip, eight loci; plus one consonant transposition.

| Locus | E-text reads | Should read | Evidence |
|---|---|---|---|
| 2,1.4 | mātḥṃś cāpi | mātṝṃś cāpi | ṝ-stem acc. pl. |
| 2,8.8 | bhrātḥn bhṛtyāṃś ca | bhrātṝn | ṝ-stem acc. pl. |
| 2,16.13 | mātḥṇāṃ vā mamāśubham | mātṝṇāṃ | ṝ-stem gen. pl. |
| 2,19.6 | mātḥṇāṃ vā pitur vāhaṃ | mātṝṇāṃ | ṝ-stem gen. pl. |
| 2,20.34 | kartḥṇāṃ te nivāraṇe | kartṝṇāṃ | ṝ-stem gen. pl. |
| 2,34.33 | mātḥn daśarathātmajaḥ | mātṝn | ṝ-stem acc. pl. |
| 2,38.16 | mātḥṇāṃ śātitāḥ stanāḥ | mātṝṇāṃ | ṝ-stem gen. pl. |
| 2,42.15 | paurastriyo bhartḥn | bhartṝn | ṝ-stem acc. pl. |
| 2,6.21 | rājye 'hbiṣekṣyati | 'bhiṣekṣyati | *bh* keyed as *hb* (transposition) |

## 2. `sa_mArkaNDeyapurANa1-93.txt` — 6 verified + 7 anomalous

Verified:

| Locus | E-text reads | Should read | Evidence |
|---|---|---|---|
| 2.47 | samyaguktaṃ dvijāgyreṇa | dvijāgryeṇa | *agrya* → *agyra* transposition (see §8) |
| 9.2 | viśvāmitraviceṣcitam | viśvāmitraviceṣṭitam | *ṣṭ* keyed as *ṣc*; √ceṣṭ |
| 11.3 | syādahkuras tadvad | syādaṅkuras | *aṅkura* "sprout" (bīja context); *h* for *ṅ* |
| 14.75 | kaṇṭakairderghairāyasaiḥ | kaṇṭakairdīrghairāyasaiḥ | *dīrgha*; *e* for *ī* |
| 19.25 | dsyu-vyālāgri-śastrādi | dasyu- | dropped *a* |
| 19.29 | saṃgrāme cāticeṣcitaiḥ | cāticeṣṭitaiḥ | same *ṣc*-for-*ṣṭ* slip as 9.2 |

Anomalous (line certainly corrupt or unmetrical; correct reading left to the editors):

| Locus | E-text reads | Note |
|---|---|---|
| 8.63 | prasādaṃ kuru meṃ nātha | *meṃ* — stray anusvāra? *me* expected |
| 8.124 | -mukhabāhūdarāṅighrakaḥ | *aṅighraka* garbled; *-āṅghrikaḥ* (aṅghri "foot") likely |
| 8.205 | mṛtanirmālyasūtrāntargūgkeśe | *-gūgkeśe* garbled; unclear |
| 14.60 | nigaḍailauhairagnipratāpitaiḥ | sandhi *r* absent (*nigaḍair lauhair* expected) — or a solid-print artifact |
| 15.20 | htvānnantu sa mārjāro | vowel lost in *ht-*; *hṛtvānnaṃ tu* plausible (cat steals food) |
| 16.25 | gāgṃ parikaraṃ baddhvā | *gāgṃ* — *gāṃ* expected? |
| 16.81 | vāṅmādhurṃyyādibhūṣaṇaiḥ | stray *ṃ* inside *mādhury(y)ādi* |

## 3. `sa_vidyAkara-subhASitaratnakoza.txt` — 12 verified + 1 anomalous

| Locus | E-text reads | Should read | Evidence |
|---|---|---|---|
| 4.18 | yaṃ paśyedty avatu | paśyed ity | dropped *i* in *iti* |
| 9.16 | agre tapta-jalāḥn nitānta- | tapta-jalān | intrusive *ḥ*; acc. pl. |
| 13.12 | asarala-janāśelṣa-krūras | janāśleṣa- | *śleṣa* keyed as *śelṣa* (metathesis) |
| 16.67 | manmathaḥ saṃdndhattāṃ dhanur | saṃdhattāṃ | intrusive *dn* in √dhā form |
| 17.58 | vaidagdhya-mudrātmabhisḥ | mudrātmabhiḥ | *sḥ* impossible; instr. pl. |
| 18.1 | saṃdndhāryate jīvitaṃ | saṃdhāryate | intrusive *dn* (same class as 16.67) |
| 19.5 | manda-manyu-grahasḥ | -grahaḥ | *sḥ* impossible (same verse also carries *atyullasat-d pakṣma-*, a stray *d*) |
| 19.32 | lupta-pātrāṅkuratvātd prakaṭa- | -tvāt | stray *d* after *t* (cf. 19.5) |
| 19.45 | dṛṣṭvaikāsana-saṃshtite | saṃsthite | *th* keyed as *ht* |
| 19.48 | krīḍā durotdara-paṇaḥ | durodara- | *durodara* "gambling, stake" (the verse is about wagers); intrusive *t* |
| 21.5 | rabhasāśelṣo 'pi | rabhasāśleṣo | same *śleṣa* metathesis as 13.12 |
| 21.25 | sva-hastenāñgārās | -hastenāṅgārās | *ṅ* mis-keyed as *ñ* before *g* |

Anomalous: 13.12 *galita-vibhavasyājhevādya dyutir* — intrusive *jh*; *vibhavasyevādya*
(*vibhavasya iva adya*) plausible.

## 4. `sa_manusmRti.txt` — 1 verified

| Locus | E-text reads | Should read | Evidence |
|---|---|---|---|
| 4.61 | nopasṣṛṭe 'ntyajair | nopasṛṣṭe | *sṛṣṭ* keyed as *sṣṛṭ* |

## 5. `sa_bhatRhari-zatakatraya.txt` — 9 verified + 1 anomalous

A notably clean classical text whose few slips are all simple keying errors:

| Locus | E-text reads | Should read | Evidence |
|---|---|---|---|
| 1.4 | pratiniviṣṭa-mūṛkha-jana- | -mūrkha- | *ūṛ* for *ūr* |
| 1.7 | viśeṣāataḥ sarva-vidāṃ | viśeṣataḥ | doubled vowel |
| 1.10 | kṣitidharaṃ mhīdhrād | mahīdhrād | dropped *a* |
| 1.11 | nāgendro niśitāgkuśena | niśitāṅkuśena | *ṅ* keyed as plain *g* |
| 1.77 | samasta-saṃvartakaiṛ | -saṃvartakair | *ṛ* for *r* |
| 1.93 | nolūko 'py avaokate | avalokate | dropped *l* |
| 1.96 | phalati naivaa kulaṃ | naiva | doubled *a* |
| 2.3 | bhrū-cāturyāt kuṣcitākṣāḥ | kuñcitākṣāḥ | *ñc* keyed as *ṣc*; √kuñc |
| 2.48 | viṣam iva bhaviṣyty asukhadam | bhaviṣyaty | dropped *a* |

Anomalous: 1.74 *camdrp volāsayati kairava-cakravālam* — badly garbled; *candra
ullāsayati* (the moon opens the night-lotus bed) is the evident sense.

## 6. `sa_abhinavagupta-kramastotra.txt` — 1 verified

| Locus | E-text reads | Should read | Evidence |
|---|---|---|---|
| AgKs 23 | iyaṃ mārta.ṅdasya | mārtaṇḍasya | stray period inside the word (conversion artifact) |

## 7. `sa_108-buddhist-stotras.txt` — 22 verified + 2 anomalous

Three slips recur systematically in this file; grouped by class.

**(a) ḥ-for-vowel / ḥ-for-consonant corruption** (the same conversion failure as the
Rāmāyaṇa's §1):

| Locus | E-text reads | Should read |
|---|---|---|
| 14.7 | tiryaḥnārakapretagatīnām | tiryaṅnāraka- |
| 20.4 | kharaśaranikaraiśchādayantoḥntarīkṣaṃ | chādayanto 'ntarīkṣaṃ |
| 24.8 | vāmahaste kapḥlaṃ | kapālaṃ |
| 57.5 | yathāvādī tathākārḥ | tathākāraḥ |
| 59.5 | vidyāṃ suvidyḥṃ | suvidyāṃ |

**(b) *agrya* → *agyra* transposition** (same class as Mārkaṇḍeya 2.47):

| Locus | E-text reads | Should read |
|---|---|---|
| 108.29 | sarvābhilāpahetvgryaḥ | -hetvagryaḥ (dropped *a*, same word family) |
| 108.116 | sarvabhāvasvabhāvāgyraḥ | -svabhāvāgryaḥ |
| 108.142 | anaṅgakāyaḥ kāyāgyraḥ | kāyāgryaḥ |
| 108.146 | samādhikāyaḥ kāyāgyraḥ | kāyāgryaḥ |
| 108.147 | nirmāṇakāyaḥ kāyāgyro | kāyāgryo |
| 108.158 | varadavajrāgyra | -vajrāgrya |

**(c) intrusive/duplicated vowel:**

| Locus | E-text reads | Should read |
|---|---|---|
| 1.15 | jihmāanāṃ nityavikṣepād | jihmānāṃ |
| 1.32 | tvayātmanyāhitā guaṇāḥ | guṇāḥ |
| 18.2 | laṅkeśapramukhāściaraṃ | -ściraṃ (*ciram*) |
| 18.39 | alamahamiaha no sukhī | alamahamiha |
| 18.78 | ciaramidamabhyasanena | ciramidam- |
| 18.84 | iadamapi yadi vedmi | idamapi |
| 25.25 | namao mahiṣasaṃvara | namo |
| 39.5 | -caraṇabhuvāmunmayūukhā | -unmayūkhā |
| 55.6 | jīrṇanauikāsamārūḍho | jīrṇanaukā- |

**(d) single slips:**

| Locus | E-text reads | Should read |
|---|---|---|
| 6.2 | durlaṅdhye duḥkhavahnau | durlaṅghye |
| 108.130 | sarvasattvetdriyārthajñaḥ | sarvasattvendriyārtha- |

Anomalous: 6.11 *gadgadodgītayācṣāḥ* (*yācñāḥ* "entreaties" plausible; *cṣ* impossible);
59.5 *sukhapḥcitḥmiti* (multiple ḥ-corruptions in one word; exact reading unclear).

## 8. The two systematic classes worth flagging as classes

1. **ḥ substituted for a vowel or nasal** — 8 loci in the Vālmīki-Rāmāyaṇa southern
   recension 2 (always for *ṝ*) + 5 loci in the 108-buddhist-stotras (for *ā, a,* avagraha,
   *ṅ*). This looks like one conversion step, not typist noise — a search for `ḥ` adjacent
   to a consonant cluster in these two files would likely find further instances beyond our
   sampled sections.
2. ***agrya* keyed as *agyra*** — 7 loci across two unrelated files (Mārkaṇḍeya-purāṇa,
   108-buddhist-stotras). Also likely findable globally by grepping `gyr`.

## 9. What we did NOT report, and why

The bigram screen flagged 124 loci; 53 are not GRETIL errors. Documented so the reader can
see the false-positive discipline:

- **Mantra / bīja / dhāraṇī material** (108-buddhist-stotras): *jhrīṃ, pheṃ, huṃphaṭ,
  jhaṃjhamānā, ṛṛmpaṃ…, mīyakaṇṭhair ḍimaḍima…* — deliberate sound-play and seed
  syllables, not lexical text (11 loci).
- **Buddhist Hybrid Sanskrit orthography**: *ratnaalaṃkṛtu* (BuSto 17.47 — the whole verse
  is BHS), *śrīindrāṇi*, *mahāayajñān* (Manu 3.71), *ālambhā-* hiatus — vowel hiatus
  written out is the edition's convention, not a typo (4).
- **Editorial apparatus swallowed by our tokenizer**: parenthetical variant readings —
  *caṇḍārī(lī)amṛtā, hārdhayuk(hārārdhayuga), viṃśatiḥ(ti), tāyaṇīḥ(ṇīm), vastrāḥ(rṣāḥ)*,
  Manu's *(m: ālambhāav*; and the Vidyākara apparatus sigla *skmsa.u.ka. / pvpadyā.*
  (source citations, initially suspected as corruption — they are not) (8).
- **Lacuna markers** `[…]` inside tokens (5 loci in BuSto 29/34).
- **Valid rare forms and sandhi** our headword-bigram model never saw: *mṛdnantī/mṛdnīyān*
  (√mṛd cl. 9), *yajñair-/jñair-* (7), *saṃghair/oghair/duḥkhaugha*, *-ḍaiḥ/-ṣṭhai-*
  inflected instrumentals, *idānīñ ca / purīñ c-* (regular *ṃ*→*ñ* sandhi), *jhaṅkāra*,
  *asaṃphalat*, *kuraṅgī* etc. (20+).
- **Orthographic choices**: *omkāra* for *oṃkāra*, unsandhied *strīṣaṭdanto*,
  *pīṭhanairṝtye* (ṝ/ṛ variation) (4).
- **Not re-locatable**: *bramty* (bharst 2.47) — flagged by the screen but absent from the
  re-parsed verse; dropped rather than reported unverified (1).

## Provenance

Candidates: bigram screen ([ngram_corpus_check.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/meter/ngram_corpus_check.py),
H289, Opus 4.8 `claude-opus-4-8`, 07-07-2026) over 5 GRETIL sections (~7,725 verses /
~101k tokens). Verification: every locus re-pulled from the raw e-text with full verse
context and hand-adjudicated, Fable 5 (`claude-fable-5`), 10-07-2026, per ruling D8 and the
H277 lesson (the meter run's 39% flag rate was mostly valid poetry — hence precision-first).
GRETIL raw files (CC BY-NC-SA, gitignored locally): fetched 06/07-07-2026 from
[gretil.sub.uni-goettingen.de](https://gretil.sub.uni-goettingen.de/).

_Dr. Mārcis Gasūns_
