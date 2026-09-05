_Created: 10-08-2026 · Last updated: 05-09-2026_

# Body-level QA — cross-reference integrity (pilot: MW)

The headword tools only check `<k1>`/`<k2>`. This is the first pass at the **words inside** entries.
Pilot conclusion: of the four body-level checks considered, **cross-reference integrity** is the one
that works on a mature dictionary; raw body-form typo-detection and self-mis-citation **hit the
headword wall** (documented below as a negative result).

> Branch `feat/body-xref-integrity` (worktree), to stay clear of the active parallel session on
> `master`. New files only — fold the findings into `docs/HYPOTHESES.md` + a use case at merge time.

## What works — cross-reference integrity (the apparatus-independent signal)

A body is full of cross-references (`See X`, `cf. X`, `= X`, `q.v.`) whose **target asserts "this
form exists."** We can check whether it does. Unlike spelling, this needs no apparatus/markup and no
corpus judgement — the dictionary makes a checkable claim about itself.

[detectors/body_xref_check.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/body_xref_check.py) extracts every `See/cf./=/q.v. <s>TARGET</s>`,
**canonicalizes the reference notation**, and resolves the target against every k1/k2 headword (all
33 dicts, via `sanhw1`) + DCS lemmas. The notation handling is the whole game — without it the
"unresolved" set is 36 % notation artifacts; with it, 6.2 %:

| step | unresolved |
|---|--:|
| naive (exact match) | 36.1 % |
| + canonical key (drop accents `/\^`, ring `˚°`, avagraha, hyphens, spaces) | 24.1 % |
| + `√`-root refs resolve to the root; ring `˚` = intra-entry self-ref (valid by construction) | 20.5 % |
| + split residual into *typo'd-ref* vs *other* | **6.2 %** |

### MW result (`MW_xref.txt`)

**18,602 cross-reference targets → 1,159 unresolved (6.2 %)**, split into:
- **270 TYPO'd cross-references** (the target is **one confusion-edit from a real entry**) →
  **FILE-FIRST**. Same confusion classes as headword typos, but in *reference targets the headword
  detectors never see*: `surya-kAnta → sUryakAnta`, `vEragya → vErAgya` (missing macron),
  `azwaqiS → azwadiS` (ḍ/d), `mimAMsA → mImAMsA`, `DAtavya → dAtavya` (aspirate).
- **889 other-unresolved** — references to *inflected/partial forms* that simply aren't headwords
  (`anyatra → anyasmin` locative; `aty-` prefix fragment; `-vettavyA` suffix). Mostly legitimate;
  low priority.

⚠️ **Still candidates, not fixes.** The 270 share R1's vowel-length ambiguity (`puzwA`/`puzwa`,
`tulyA`/`tulya` are both real) — so each must be **scan-verified** before filing. But 270 of 18,602
(1.5 %) is a tractable, prioritized, *new* class of fileable correction.

## What failed — raw body-form typo & self-mis-citation (the headword wall)

Documented negative result. Applying the spell-checkers directly to body Sanskrit forms does **not**
work on a mature dictionary, for the same reason R1 fails on headwords:

- **Raw body-form typo detection.** MW has **315,088 `<s>` body tokens / 221,631 distinct**, of which
  **79.9 % are not corpus-attested** — overwhelmingly because they are *inflected/compound forms*,
  not typos. Flagging "unattested" yields ~177 k candidates that are almost all real. This is the
  vowel-length / inflection ambiguity (R1) at ~100× the headword scale — no usable precision without
  the body-grounded (LLM) arbiter.
- **Self-mis-citation** (entry cites its own headword with a confusion difference): only **56 hits in
  MW, 1 of them clean** (`cicIkUcI`/`cicIkucI`) — MW headwords are mature (H2), so the
  "headword-typo-revealed-by-its-own-body" signal is nearly empty. It would be denser on a
  poorly-digitised dict, but on MW it's not a viable standalone signal.

**Consequence:** body QA on a mature dictionary should lead with *structural* claims the dictionary
makes (cross-references), not *spelling* judgements (which need the body-grounded triage). This mirrors
H1: the body adjudicates, plain spelling does not.

## Scaled across dictionaries

The check is markup- and language-aware: it handles both span families (`<s>…</s>` MW / `{#…#}`
everyone else), English (`See`/`cf.`/`q.v.`) **and** German (`s.`/`vgl.`) cue words, and validates
`{{Lbody=N}}` redirects by L-number.

| dict | cue targets | unresolved | **FILE-FIRST typo'd-refs** | `{{Lbody}}` redirects | dangling |
|---|--:|--:|--:|--:|--:|
| MW  | 18,605 | 6.2 %  | **270** | 4,352  | 0 |
| PWG | 23,112 | 23.0 % | **215** | 9      | 0 |
| PW  | 10,460 | 14.0 % | **181** | 12,186 | 0 |
| SHS | 2,504  | 7.6 %  | **43**  | 13     | 0 |
| AP  | 2,806  | 9.4 %  | **24**  | 9,621  | 0 |
| VCP | 0      | —      | 0       | 1,765  | 0 |
| SKD | 0      | —      | 0       | 335    | 0 |

**Two findings:**
1. **733 candidate typo'd cross-references** across the cue-using dicts — a new, prioritized,
   fileable corpus (each still scan-verify). German dicts (PWG 23 %, PW 14 %) carry more unresolved
   than English (MW 6 %, SHS/AP 8–9 %): partly real typo'd-refs, partly German notation the resolver
   handles less fully than MW's — worth more notation work before filing PWG/PW.
2. **Redirect integrity is clean** — of **~28,300 `{{Lbody=N}}` redirects** across all dicts (VCP and
   SKD use these *exclusively*), **0 dangle**. The redirect machinery points only to real entries; a
   reassuring negative result (no broken redirects to file).

## Run it

```sh
cd detectors && python body_xref_check.py <DICT> ../body_xref/<DICT>_xref.txt   # MW PW PWG VCP SKD SHS AP …
```

## Status vs the plan (target order)

1. **Sanskrit body-forms** — done: cross-ref integrity ✅ (733 typo'd-refs), raw typo/mis-citation ✗.
2. **Cross-ref targets** — done across 7 dicts (English + German cues, `{{Lbody}}` redirects).
3. **Gloss-language words** — already covered by the ortho-drift study.

**Before filing:** refine German (PW/PWG) notation handling to drive the 14–23 % unresolved down (so
the typo'd-ref set is cleaner), then scan-verify each FILE-FIRST candidate per the standard workflow.

_Dr. Mārcis Gasūns_
