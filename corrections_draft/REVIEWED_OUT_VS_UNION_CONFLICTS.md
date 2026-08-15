# Reviewed-out vs union: 17 rows two passes disagree about

_Created: 04-08-2026 · Last updated: 04-08-2026_

Run-1's Opus false-positive review ruled each of these **not fileable**, so it sits COMMENTED OUT in `<DICT>_file_first_sf.txt`. The union-across-runs passes re-found it and the H2274 verification pass ruled it fileable against the entry's own text. Both judgements are recorded; neither has been silently overridden.

**Nothing here is activated.** The rows stay reviewed-out, they appear in the scan-verification sheet carrying the newer verdict, and a human's scan vote is the arbiter. Approving one has no effect until the row is uncommented — `apply_scanverify_decisions.py` reports it as missing, which is deliberate: a prior review decision should not be reversed by a silent flip.

Concentrated in **YAT**, whose b/v class was explicitly "held for scan" — exactly the population where the scan, not either pass, is the arbiter.

| dict | headword | proposed | H2274 verdict | run-1 | evidence |
|---|---|---|---|---|---|
| SKD | `mahotka` | `mahotkA` | **PASS** | reviewed-out | L26941 k1>mahotka: 'mahotka¦, strI, (mahAn utkaH darSanotsuko loko yasyAH .) vidyut . iti kecit ..' Fem bahuvrihi (strI + yasyAH) requires stem ending -A; short -a contradicts gend |
| YAT | `AkASabartman` | `AkASavartman` | **SCAN-FIRST** | reviewed-out | L4332 '{#AkASa-bartman#} (rtma) 5. n. Firmament.' Bare gloss, no etymology/xref bearing on b/v; entry itself silent on spelling. |
| YAT | `BImabikrama` | `BImavikrama` | **SCAN-FIRST** | reviewed-out | L28117 '{#BIma-bikrama#} (maH-mA-maM) a. Gigantic.' Bare adjective def, no internal evidence besides declension pattern; no xref to disambiguate b/v. |
| YAT | `BawwArakabAra` | `BawwArakavAra` | **SCAN-FIRST** | reviewed-out | L27690 '{#BawwAraka-bAra#} (raM) 1. n. Sunday.' Bare gloss, no etymology/xref in entry; correction rests on external knowledge that vAra=day. |
| YAT | `aDyabasAyin` | `aDyavasAyin` | **PASS** | reviewed-out | L933 '{#aDya_basAyin#} (yI-yinI-yi) a. Persevering, resolute, determined' directly follows L932 '{#aDya_vasAya#} m. Perseverance' (v-spelled) - the adjectival form of the same head |
| YAT | `araRyabAsa` | `araRyavAsa` | **PASS** | reviewed-out | L2598 '{#araRya-bAsa#} (saH) 1. m. Hermitage' sits directly before L2599 '{#araRya-vAsin#} m. A hermit' (v-spelled, same root vas 'dwell') - the dweller/dwelling-place pair confirm |
| YAT | `avedabid` | `avedavid` | **PASS** | reviewed-out | L3515 '{#a-vedabid#} 5. m. Brahman not knowing the vedas.' Gloss itself paraphrases a-veda-vid ('not knowing'=vid); 'bid' unattested root; no collision for avedavid. |
| YAT | `dibodBava` | `divodBava` | **SCAN-FIRST** | reviewed-out | L18493 '{#dibodBava#} a. Born or produced in heaven.' Silent on spelling; immediately precedes divOkas (v-section), decisive sort placement for divo- not dibo-. No collision. |
| YAT | `garhyabAdin` | `garhyavAdin` | **PASS** | reviewed-out | L12822 '{#garhya-bAdin#} a. Speaking ill, vilely or inaccurately.' Gloss 'Speaking' directly matches vAdin (vad, to speak); 'bAdin' unattested root. No collision for garhyavAdin. |
| YAT | `iBayubati` | `iBayuvati` | **PASS** | reviewed-out | L5754 '{#iBa-yubati#} 2. f. Elephant's cub.' Fem. gloss 'cub' (young female) matches yuvati (young woman); 'yubati' unattested. No collision for iBayuvati. |
| YAT | `indrasAbarRi` | `indrasAvarRi` | **SCAN-FIRST** | reviewed-out | L5714 '{#indra-sAbarRi#} 2. m. Last Menu.' Entry silent on spelling; the last of the 14 Manus is the well-documented Sāvarṇi (sAvarRi), 'sAbarRi' unattested. No collision. |
| YAT | `kapawapravanDa` | `kapawaprabanDa` | **SCAN-FIRST** | reviewed-out | L8374 '{#kapawa-pravanDa#} (nDaH) m. Fraud' — entry gives only the gloss, no etymology distinguishing pravanDa/prabanDa; 'prabanDa' is the attested word (composition/series), 'prav |
| YAT | `kawolabIRA` | `kawolavIRA` | **SCAN-FIRST** | reviewed-out | L8077 '{#kawola-bIRA#} (RA) f. A kind of lute, played by common people'; entry itself silent on spelling; parallel entry kaRqolavIRA (L8198, same 'A kind of X' lute gloss) uses vIR |
| YAT | `kzudrabaMSA` | `kzudravaMSA` | **SCAN-FIRST** | reviewed-out | L11899 '{#kzudra-baMSA#} (SA) f. A plant, (Lycopodium imbricatum)' — entry silent on spelling; relies on external match to MW kzudravaMSA and YAT's own ~40x use of vaMSa elsewhere  |
| YAT | `nirAlamva` | `nirAlamba` | **SCAN-FIRST** | reviewed-out | L21384 '{#nirA_lamva#} (mvaH-mvA-mvaM) a. Self-supported, not relying on others' — entry itself silent on spelling; 'Alamba' (support, from lamb-) is the real root, 'Alamva' unatte |
| YAT | `puMbfza` | `puMvfza` | **SCAN-FIRST** | reviewed-out | L24418 '{#puM-bfza#} (zaH) m. The musk rat' — entry silent on spelling; matches MW puMvfza 'the musk rat'; YAT spells vfza in ~30 other entries, bfza is a hapax. |
| YAT | `viqbarAha` | `viqvarAha` | **PASS** | reviewed-out | L34609 '{#viqba_rAha#}¦ (haH) m. A tame hog.' Entry itself is a bare gloss, but YAT's own varAha (L33271) plus AdivarAha/nfvarAha/mahAvarAha/yajYavarAha/varAhakAntA etc. (11 entrie |

_Dr. Mārcis Gasūns_
