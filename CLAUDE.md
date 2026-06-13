# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> Org-level conventions (issue taxonomy, `.ai_state.md` session protocol, the
> `csl-orig` correction workflow, Windows/encoding rules) live in the parent
> [GitHub/CLAUDE.md](../CLAUDE.md) and are **not** repeated here. This file covers
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

**Active work** (as of this writing): the repo is being modernized to run on
**Python 3 + PHP 8** (see "Runtime & porting status" below), while continuing to
(a) generate suspect lists for more base dictionaries and (b) refine the detection
methods. New code should be Python 3 / PHP 8 native, not written to match the
legacy style.

## Core methodology

The central idea (see [README.md](README.md) "Logic" section): treat one
dictionary as a **base/reference** (presumed-correct), build an inventory of the
vowel/consonant patterns its headwords use, then flag any headword in the *other*
dictionaries that contains a pattern the base never uses. A pattern the base
lacks is a spelling-anomaly candidate.

Patterns are defined once in [faultfinder3a_utils.php](faultfinder3a_utils.php)
(`faultfinder_patterns()`): `VV`, `VCV`, `VCCV` … up to `VCCCCCV`, plus
`Start-CC`, `CC-End`, `CCC-End`, `CCCC-End`. `V` = `[aAiIuUfFxXeEoO]`,
`C` = the SLP1 consonant class. Pattern names abbreviate to the `P` codes that
appear in output (e.g. `Start-Consonant-Consonant` → `SCC`).

## Three independent detector families

| Detector | Entry point | Finds |
|---|---|---|
| **faultfinder** (primary) | top-level `faultfinder3a.php` + `faultfinder_regen.sh` | headwords with vowel/consonant patterns absent from a base dict |
| **o_vs_O** | [o_vs_O/](o_vs_O/) | minimal-pair / near-spelling confusions across dicts (e.g. `o` vs `O`, single-letter differences) |
| **ngram** | [ngram/ngramspellcheck.py](ngram/ngramspellcheck.py) | suspect words in *running text* whose bigrams/trigrams are absent from MW∩PW |

`faultfinder.php`, `faultfinder1.php`, `faultfinder2.php`, `faultfinder3.php` are
**superseded predecessors** of `faultfinder3a.php`; do not extend them.

## Data spine

- **[sanhw1.txt](sanhw1.txt)** — merged headword list, one line `hw:DICT1,DICT2,…`
  (which dictionaries contain that headword). The primary input to faultfinder.
- **[sanhw2.txt](sanhw2.txt)** — same, but with per-dict L-IDs: `hw:DICT;Lid,…`.
  Enables deep-links to specific dictionary entries (used by the o_vs_O sanhw2 path).
- Both are sorted in **Sanskrit alphabetical order with `M`→homorganic-nasal
  normalization** (so `aMga` sorts as `aNga`). This sort logic lives in
  [sanhw1/sanhw1.py](sanhw1/sanhw1.py) / [sanhw2/sanhw2.py](sanhw2/sanhw2.py).
- **[nochange/nochange.txt](nochange/nochange.txt)** — whitelist of
  human-confirmed-correct words; `faultfinder3a.php` subtracts these from output.
- `MWslp.txt`, `PWslp.txt`, `VCPslp.txt` — single-dictionary SLP1 headword dumps.
  [HeadwordLists/](HeadwordLists/) holds per-dict unique-key lists.

**Specialized dictionaries** `ACC BHS BUR IEG KRM VEI PD` are treated as
"less fruitful" and excluded in places (e.g. [chg_nchg_sep.py](chg_nchg_sep.py)
line 18) because they are domain-specific, not general Sanskrit lexica.

## Shared transliteration library

[function.php](function.php) (≈436 KB), [slp-dev.php](slp-dev.php) (SLP1→Devanagari)
and [dev-slp.php](dev-slp.php) (Devanagari→SLP1) are vendored from Dr. Patel's
`sanskrit` sandhi project. They are used only to render Devanagari and Cologne
deep-links in the generated HTML reports — treat them as a third-party dependency:
don't refactor them. They use no PHP-8-removed constructs (`each()`,
`create_function()`, `$str{i}` offsets), so they already run on PHP 8 as-is.

## Output formats (conventions other tools depend on)

- **`AllvsXX.txt`** — `X:P=Y:D` where `X`=headword, `P`=pattern abbrev,
  `Y`=offending substring, `D`=comma-list of dicts containing `X` (never the base).
- **`AllvsXX_sf.txt`** — "standard format" `DICT:word:word:n`, the correction-submission
  format from [CORRECTIONS#154](https://github.com/sanskrit-lexicon/CORRECTIONS/issues/154).
  After a human edits the middle field, [chg_nchg_sep.py](chg_nchg_sep.py) splits it
  into `chg.txt` (real corrections) and `nchg.txt` (false positives → feed back to whitelist).
- The `o_vs_O` composite outputs rank candidate pairs by likelihood
  (composite1 = highest … composite3 = near-nil); see [o_vs_O/readme.md](o_vs_O/readme.md).

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
The **PHP pipelines run on PHP 8 today**; the **Python helpers** (`chg_nchg_sep.py`,
`ngram/`, `o_vs_O/sortlen.py`) **must be ported to Python 3 first** — see below.

## Runtime & porting status — **Python 3 + PHP 8 only**

The only available runtimes are Python 3 and PHP 8, but the committed code was
written for Python 2 / PHP 5–7. The two languages are in very different shape.

**PHP side — runs today, one deprecation to clean up.** The faultfinder and o_vs_O
pipelines work on PHP 8. The single rough edge is
`preg_split($pattern, $value, null, PREG_SPLIT_DELIM_CAPTURE)` in
[faultfinder3a.php](faultfinder3a.php) (lines 129 and 150): passing `null` for the
`$limit` argument is deprecated on PHP 8.1+ — change it to `-1`. Scripts set
`memory_limit=1000M` and read all of `sanhw1.txt` (~9 MB) into memory.

**Python side — every script is Python 2 and won't even parse under Python 3.**
All `.py` files use `print` statements (a hard `SyntaxError` in Python 3), so none
run as-is. Concrete porting checklist:

- All files: `print "x"` → `print("x")`.
- [sanhw1/sanhw1.py](sanhw1/sanhw1.py), [sanhw2/sanhw2.py](sanhw2/sanhw2.py):
  - `string.maketrans` → `str.maketrans`; `string.translate(a, t)` → `a.translate(t)`.
  - builtin `cmp(a, b)` was removed → `(a > b) - (a < b)`.
  - `sorted(…, cmp=fn)` was removed → `sorted(…, key=functools.cmp_to_key(fn))`.
  - `hw0.encode('ascii','replace')` returns **bytes** in Py3, so dict keys become
    `b'…'` — these were Py2 unicode→str shims; drop the encode or decode back to `str`.
- [ngram/ngramspellcheck.py](ngram/ngramspellcheck.py): `from HTMLParser import HTMLParser`
  → `from html.parser import HTMLParser` (line 22); `is not 0` → `!= 0` (line 155);
  have `MLStripper.__init__` call `super().__init__()`.
- [o_vs_O/sortlen.py](o_vs_O/sortlen.py): `print` statements; also needs `lxml`.

**`sanhw1.txt` / `sanhw2.txt` are regenerated on the Cologne server, not here.**
`sanhw*.py`'s `addhw()` reads sibling `<CODE>Scan/<year>/pywork/<code>hw2.txt` trees
that aren't on this machine, so porting them is not on the critical path for local
work — treat the two `.txt` files as fixed inputs and let the refresh happen
server-side (the org's standard server-side artefact-refresh model).

**Tooling already wired up:** [.pre-commit-config.yaml](.pre-commit-config.yaml)
(ruff `E9,F63,F7,F8` + yaml/whitespace hooks) and
[.github/dependabot.yml](.github/dependabot.yml) (github-actions). Default branch is
`master`. Note the ruff rule set is syntax/undefined-name only — it will **not** flag
Py2 `print` statements, so it won't catch un-ported files for you.
