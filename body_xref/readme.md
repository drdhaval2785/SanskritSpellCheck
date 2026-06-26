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

[detectors/body_xref_check.py](../detectors/body_xref_check.py) extracts every `See/cf./=/q.v. <s>TARGET</s>`,
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

## Run it

```sh
cd detectors && python body_xref_check.py MW ../body_xref/MW_xref.txt
```

## Next (target order, per the plan)

1. **Sanskrit body-forms** — done (this pilot): cross-ref integrity ✅, raw typo/mis-citation ✗.
2. **Cross-ref targets across more dicts** — run on PW/PWG/VCP (German/Sanskrit cue words differ:
   `s.`/`vgl.`/`{{Lbody=N}}`), and on a poorly-digitised dict (SHS) where the typo'd-ref density
   should be higher.
3. **Gloss-language words** — already covered by the ortho-drift study.
