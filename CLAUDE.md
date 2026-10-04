_Created: 10-08-2026 · Last updated: 04-10-2026_

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> Org-level conventions (issue taxonomy, `.ai_state.md` session protocol, the
> `csl-orig` correction workflow, Windows/encoding rules) live in the parent
> [Uprava/CLAUDE.md](https://github.com/gasyoun/Uprava/blob/main/CLAUDE.md) and are **not** repeated here. This file covers
> only what is specific to SanskritSpellCheck.

## What this repo is

SanskritSpellCheck is a **QA / error-detection toolset** for the
[Cologne Digital Sanskrit Dictionaries](http://www.sanskrit-lexicon.uni-koeln.de/),
authored by Dr. Dhaval Patel. It is **not a dictionary** — it produces lists of
*suspected misspelled headwords* by comparing spelling/pattern statistics across
~36 Cologne dictionaries. Confirmed errors are then reported as issues in the
separate [sanskrit-lexicon/CORRECTIONS](https://github.com/sanskrit-lexicon/CORRECTIONS/issues)
repo (this repo never edits dictionary source itself).

All Sanskrit text in this repo is in **SLP1** transliteration.

**Runtime** (modernized June 2026): the toolset now runs on **Python 3 + PHP 8**.
All scripts were ported from the original Python 2 / PHP 5–7 (see "Runtime &
porting status" below for exactly what changed and how it was verified). New code
should stay Python 3 / PHP 8 native.

## Core methodology

The central idea (see [README.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/README.md) "Logic" section): treat one
dictionary as a **base/reference** (presumed-correct), build an inventory of the
vowel/consonant patterns its headwords use, then flag any headword in the *other*
dictionaries that contains a pattern the base never uses. A pattern the base
lacks is a spelling-anomaly candidate.

Patterns are defined once in [faultfinder3a_utils.php](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/faultfinder3a_utils.php)
(`faultfinder_patterns()`): `VV`, `VCV`, `VCCV` … up to `VCCCCCV`, plus
`Start-CC`, `CC-End`, `CCC-End`, `CCCC-End`. `V` = `[aAiIuUfFxXeEoO]`,
`C` = the SLP1 consonant class. Pattern names abbreviate to the `P` codes that
appear in output (e.g. `Start-Consonant-Consonant` → `SCC`).

## Three independent detector families

| Detector | Entry point | Finds |
|---|---|---|
| **faultfinder** (primary) | top-level `faultfinder3a.php` + `faultfinder_regen.sh` | headwords with vowel/consonant patterns absent from a base dict |
| **o_vs_O** | [o_vs_O/](o_vs_O/) | minimal-pair / near-spelling confusions across dicts (e.g. `o` vs `O`, single-letter differences) |
| **ngram** | [ngram/ngramspellcheck.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/ngram/ngramspellcheck.py) | suspect words in *running text* whose bigrams/trigrams are absent from MW∩PW |

`faultfinder.php`, `faultfinder1.php`, `faultfinder2.php`, `faultfinder3.php` are
**superseded predecessors** of `faultfinder3a.php`; do not extend them.

## Data spine

- **[sanhw1.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/sanhw1.txt)** — merged headword list, one line `hw:DICT1,DICT2,…`
  (which dictionaries contain that headword). The primary input to faultfinder.
- **[sanhw2.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/sanhw2.txt)** — same, but with per-dict L-IDs: `hw:DICT;Lid,…`.
  Enables deep-links to specific dictionary entries (used by the o_vs_O sanhw2 path).
- Both are sorted in **Sanskrit alphabetical order with `M`→homorganic-nasal
  normalization** (so `aMga` sorts as `aNga`). This sort logic lives in
  [sanhw1/sanhw1.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/sanhw1/sanhw1.py) / [sanhw2/sanhw2.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/sanhw2/sanhw2.py).
- **[nochange/nochange.txt](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/nochange/nochange.txt)** — whitelist of
  human-confirmed-correct words; `faultfinder3a.php` subtracts these from output.
- `MWslp.txt`, `PWslp.txt`, `VCPslp.txt` — single-dictionary SLP1 headword dumps.
  [HeadwordLists/](HeadwordLists/) holds per-dict unique-key lists.

**Specialized dictionaries** `ACC BHS BUR IEG KRM VEI PD` are treated as
"less fruitful" and excluded in places (e.g. [chg_nchg_sep.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/chg_nchg_sep.py)
line 18) because they are domain-specific, not general Sanskrit lexica.

**External dictionary sources (not in `csl-orig`).** A few dicts have headwords in
`sanhw1.txt` but no `csl-orig/v02/<dict>/<dict>.txt` entry text — notably **PD** (Deccan
College *Encyclopaedic Dictionary*, CC BY-NC-SA, ~55 MB). The body-grounded triage resolves a
dict's entry text through `triage_util.source_file(dict_code)`, which prefers a gitignored
`external_src/<dict>/<dict>.txt` staging file and otherwise falls back to `csl-orig`. Stage these
with [detectors/get_external_source.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/get_external_source.py) (re-run on a fresh
clone); they are **never committed here** (license + size). PD expects a **second source** —
register its URL in that script.

## Shared transliteration library

[function.php](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/function.php) (≈436 KB), [slp-dev.php](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/slp-dev.php) (SLP1→Devanagari)
and [dev-slp.php](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/dev-slp.php) (Devanagari→SLP1) are vendored from Dr. Patel's
`sanskrit` sandhi project. They are used only to render Devanagari and Cologne
deep-links in the generated HTML reports — treat them as a third-party dependency:
don't refactor them. They use no PHP-8-removed constructs (`each()`,
`create_function()`, `$str{i}` offsets), so they already run on PHP 8 as-is.

## Output formats (conventions other tools depend on)

- **`AllvsXX.txt`** — `X:P=Y:D` where `X`=headword, `P`=pattern abbrev,
  `Y`=offending substring, `D`=comma-list of dicts containing `X` (never the base).
- **`AllvsXX_sf.txt`** — "standard format" `DICT:word:word:n`, the correction-submission
  format from [CORRECTIONS#154](https://github.com/sanskrit-lexicon/CORRECTIONS/issues/154).
  After a human edits the middle field, [chg_nchg_sep.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/chg_nchg_sep.py) splits it
  into `chg.txt` (real corrections) and `nchg.txt` (false positives → feed back to whitelist).
- The `o_vs_O` composite outputs rank candidate pairs by likelihood
  (composite1 = highest … composite3 = near-nil); see [o_vs_O/readme.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/o_vs_O/readme.md).
- **HTML reports** ([faultfinder3a-html.php](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/faultfinder3a-html.php)) take a 3rd
  `repeat` arg: `0` (default) keeps only single-dictionary words *and* excludes
  post-repha words via `rcc()` (`r` + doubled consonant); `1` allows multi-dict; `2`
  renders every input row (including rcc). The default rcc exclusion encodes a real
  editorial judgment — post-repha doublings (sūryya, varṇṇa, ūrmma) are usually the
  faithful printed form, *not* errors. (`repeat=2` was dead code until fixed June 2026.)
- **[triage_suspects.py](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/triage_suspects.py)** post-processes an `AllvsXX.txt` into
  `noise` (specialized-dict-only), `priority` (non-rcc anomalies — review first), and
  `gemination` (the rcc/post-repha subset — low priority). The 2026 re-run packages
  live in [Allvs_2026/](Allvs_2026); the historical `AllvsXX/` dirs are the 2017 runs.
- **[detectors/](detectors)** — eight newer algorithms on a shared `slp1util.py`
  confusion model, several grounded in the **DCS corpus** (vendored
  `dcs_lemma_summary.json`, 83k SLP1 lemmas + frequency bands, DCS-2021 CC-BY, used
  to suppress real-word headwords and rank suggestions): correctors `spell_correct`
  (DCS-ranked), `consensus`, `intra_dup`, `dict_vs_corpus` (collective errors) emit
  `DICT:wrong:right:n`; flaggers `phonotactic_check`, `charset_check`, `order_check`,
  `meter_check` emit `X:CODE=Y:D`. They target the skeleton-preserving substitutions
  faultfinder is blind to. Task-oriented recipes: **[USE_CASES.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/USE_CASES.md)**.
- **`meter_check`** (H251, 06-07-2026) — batch chandas (meter) validator: a headword
  co-occurring with a metrically broken GRETIL kavya verse is a corpus-corroboration
  signal. Three-way vote (skrutable + `chanda` + `vidyut-chandas`) over GRETIL's Kavya
  section (57 texts, ~26k verses), bridged from free verse text to dictionary headwords
  via `vidyut.cheda`'s segmenter/lemmatizer. Design, corpus-fetch step, verdict scheme,
  and guards (not a tier promoter — same cross-agreement mechanism as the other
  detectors): **[detectors/meter/README.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/detectors/meter/README.md)**.
- **Body-grounded triage** (`detectors/triage_*.py` + `bodyaware_workflow.js`) — turns a
  dictionary's tier-A candidates into a verified FILE-FIRST queue + a do-not-file list by
  judging each against the dictionary's *own entry text* (not spelling alone). Run it with the
  **`/dict-triage <DICT>`** skill ([.claude/commands/dict-triage.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/.claude/commands/dict-triage.md));
  hybrid models (Sonnet classify / Opus confirm). Output: `corrections_draft/<DICT>/`. **Done for
  all 33 dicts** (index: [corrections_draft/README.md](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/README.md)) — 122 fileable
  typos across 11 dicts, ~2,549 do-not-file spellings; the high-yield outliers are poorly-digitised
  sources (SHS 37, YAT 27, ACC 22). ⚠️ Tier-A precision is near-zero on mature dicts; the LLM TYPO pass is
  stochastic (don't blindly re-run a verified package) — the do-not-file list is the real value.
  All steps share `detectors/triage_util.py`, the stdlib-only triage core: paths
  (`csl_root()`/`csl_dict_file()`, `package_dir()`/`work_dir()`), CLI helpers
  (`reconfigure_stdio()`, `dict_arg()`), the tunables every step must agree on (`BATCH_SIZE`,
  `INTENTIONAL_KINDS`, `NEEDS_JUDGMENT`, `SCAN_URL`), the JSON-verdict loaders, and the csl-orig
  `EntryIndex`. Per-dictionary language markers live in `detectors/triage_lang.py` (`_LANG`
  maps the dict code to en/de/sa and defaults unknown codes to English).

## Commands

PHP scripts are **CLI-only**, run from the **repo root** (e.g. `faultfinder3a.php`
hardcodes a relative read of `nochange/nochange.txt`).

```sh
# Full faultfinder pipeline for one base dictionary (e.g. MW), end-to-end:
sh faultfinder_regen.sh MW        # → AllvsMW/{AllvsMW.txt, _sf.txt, -norepeat.html, dictwiseerrors3-table.html}

# …which is equivalently the three manual steps:
php faultfinder3a.php      MW sanhw1.txt AllvsMW/AllvsMW.txt AllvsMW/AllvsMW_sf.txt
php faultfinder3a-html.php AllvsMW/AllvsMW.txt AllvsMW/AllvsMW-norepeat.html
php dictwisesorter-v3.php  AllvsMW/AllvsMW-norepeat.html AllvsMW/dictwiseerrors3-table.html

# Split a human-corrected _sf file into corrections vs whitelist:
python chg_nchg_sep.py AllvsMW/AllvsMW_sf_corrected.txt AllvsMW/chg.txt AllvsMW/nchg.txt

# o_vs_O minimal-pair detector (slow; only rerun if sanhw*.txt changed):
cd o_vs_O && php o_vs_O.php          # → o_vs_O1.txt (raw), o_vs_O2.txt (refined)
cd o_vs_O && sh composite.sh         # best path: composite report from o_vs_O2.txt

# ngram running-text checker (bigrams recommended; n=2 minimizes false positives):
cd ngram && python ngramspellcheck.py data/test.txt data/error.txt 2
```

There is no build, no test suite, and no package manifest — the "tests" are the
generated suspect lists, verified by human reviewers against the scanned dictionaries.
All PHP pipelines and Python helpers run under PHP 8 / Python 3 (see below).

## Runtime (PHP 8.2 / Python 3.14)

Local runtimes: **PHP 8.2** (`C:\xampp\php\php.exe`, *not* on PATH) and **Python
3.14** (`python`, `lxml` installed). The code was ported from Python 2 / PHP 5–7
in June 2026 and verified end-to-end — the full porting log (the `foreach`
faultfinder fix and the 555 alphabet-tail suspects it added, per-file Python
diffs) is in the **git history of this file** (revisions before 04-10-2026; it
was cut for the 4 000 approx-tok agent-docs budget, MG ruling 04-10-2026
«I trust you, cut»). New code stays Python 3 / PHP 8 native.

**Heads-up — re-running an *old* base dict now yields far fewer hits than its
committed file, and that is expected, not a regression.** Fixed errors go
upstream to CORRECTIONS and fold back into a regenerated `sanhw1.txt`, so the
alphabet head is now largely clean: fresh `MW`=110 / `PW`=183 / `PWG`=256 vs the
committed 2017 files (1705 / 1853 / 1984), and most fresh hits are alphabet-tail
(`s…`/`h…`) suspects genuinely worth a review pass. A small result means "mostly
corrected," **not** "pipeline broken." A *small* base flags more (narrow pattern
inventory): SKD (17 k entries) → 31 959 flags — prefer a large clean base for
high-precision lists. `sanhw1.py` / `sanhw2.py` regenerate only on the Cologne
server (they read sibling `<CODE>Scan/<year>/pywork/` trees that exist nowhere
else) — treat `sanhw1.txt` / `sanhw2.txt` as fixed local inputs.

**Tooling:** [.pre-commit-config.yaml](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/.pre-commit-config.yaml) (ruff `E9,F63,F7,F8` —
syntax/undefined-name only, won't catch Py2 `print`)
+ [.github/dependabot.yml](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/.github/dependabot.yml). Default branch `master`.

_Dr. Mārcis Gasūns_
