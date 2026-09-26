# Confusables reference — Cologne MW72 dual-headword batch (2026-09-26)

_Created: 26-09-2026 · Contributor: Dr. Mārcis Gasūns (via the SanskritLexicography birthday-collision baseline)_

Manual-triage reference only — **these are distinct dictionary lemmas, not spelling
errors**. Filed here per MG ruling 26-09-2026 so that faultfinder/ngram triage does not
mistake their phonetic proximity for a defect to "correct".

Source: the 18 dual-headword insertions of Cologne batch 2026-08-04, mw72
(Cologne#178, MW entries joined by 'and'). Phonetic collisions inside the batch were
verified against the Monier-Williams headword Herfindahl baseline
([birthday_collision_baseline.py](https://github.com/gasyoun/SanskritLexicography/blob/master/birthday_collision_baseline.py)):
every field came out background noise (Poisson p 0.19–0.69), i.e. these pairs share
onsets/finals exactly as often as chance predicts.

## The colliding pairs (SLP1)

| Pair | Shared feature |
|---|---|
| `jawAyus` / `janU` | onset `ja` |
| `dattila` / `dattiya` | onset `da`, final-2 `ya` |
| `yOktASvottara` / `yaRvApatyottara` / `karvura` | final-2 `ra` |
| `GolikA` / `JIrukA` | final-2 `kA` |
| `AgniveSyAyana` / `kftena` | final-2 `na` |
| `jAmadagneya` / `dattiya` | final-2 `ya` |
| `karvura` / `kftena` / `keSarin` | first letter `k` |
| `mandAru` / `meluda` | first letter `m` |
| `dattila` / `dattiya` (with `dveSavyaNjanam`-family inserts) | first letter `d` |

Baseline context: in MW (194,083 headwords) the final letter collapses to an effective
2.6 categories, the first letter to 15 — two of ten random entries sharing a first/last
letter is the norm, not a signal. A collision becomes evidence only at P < 5%
(m_eff ≳ 900 for k = 10).

_Dr. Mārcis Gasūns_
