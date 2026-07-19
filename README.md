SanskritSpellCheck
==================

from faultfinder3a.php - the machine is commandline tool now.

> **Runtime:** modernized June 2026 to run on **Python 3 + PHP 8** — see
> [CLAUDE.md](CLAUDE.md). For task-oriented recipes see **[USE_CASES.md](USE_CASES.md)**;
> for the newer algorithms see **[detectors/readme.md](detectors/readme.md)**; for the project's
> confirmed/refuted/open hypotheses see **[docs/HYPOTHESES.md](docs/HYPOTHESES.md)**.
>
> **Body-grounded triage:** per-dictionary status + results for **all 33 dictionaries (complete)**
> are indexed in **[corrections_draft/README.md](corrections_draft/README.md)** — 122 fileable typos
> across 11 dicts, ~2,549 do-not-file spellings (folded into the detector suppression layer). The
> high-yield outliers are poorly-digitised sources (SHS 37, YAT 27, ACC 22). To re-triage a
> dictionary, type **`/dict-triage <DICT>`** in Claude Code (the link opens the index; the
> slash-command is run by typing it, not by clicking).

## Detection methods

| method | finds | output |
|---|---|---|
| **faultfinder** (`faultfinder3a.php`) | headwords with a vowel/consonant cluster absent from a base dictionary | `X:P=Y:D` |
| **o_vs_O** (`o_vs_O/`) | single-letter near-spelling confusions across dictionaries | pair list |
| **ngram** (`ngram/`) | running-text words whose bigrams are absent from MW∩PW | error list |
| **spell_correct** (`detectors/`) | misspelling whose neighbour is a trusted MW/PW/VCP headword (DCS-frequency-ranked) | `DICT:wrong:right:n` |
| **consensus** (`detectors/`) | minority spelling vs the N-way cross-dictionary majority | `DICT:wrong:right:n` |
| **intra_dup** (`detectors/`) | a dictionary holding a word and a rare variant of it | `DICT:wrong:right:n` |
| **dict_vs_corpus** (`detectors/`) | a form all dictionaries agree on but the DCS corpus contradicts (collective error) | `DICT:wrong:right:n` |
| **phonotactic** (`detectors/`) | impossible anusvara/visarga/double-vowel forms | `X:PH-…=…:D` |
| **charset** (`detectors/`) | non-SLP1 characters (encoding errors) | `X:CHS=…:D` |
| **order** (`detectors/`) | headwords out of Sanskrit collation order | `X:ORD=…` |

## Real error distribution (what the corrections actually are)

Measured from the [o_vs_O](o_vs_O/o_vs_O2.txt) confusion pairs (single-letter class):

| class | share | example |
|---|---|---|
| vowel length (a/A, i/I, u/U) | **75%** | `vira` → `vIra` |
| aspiration (k/K, t/T) | 13% | `kaPila` → `kapila` |
| sibilant (s/S/z) | 8% | `Amfz` → `AmfS` |
| diphthong (o/O, e/E) | 4% | `koSika` → `kOSika` |

The CORRECTIONS history adds v↔b, ṛ↔ri, encoding, duplicates, misordering, and
anti-sandhi. Note **faultfinder is blind to the top three classes** (they preserve
the V/C skeleton) — that is what the `detectors/` package addresses.

## Documentation

- **[USE_CASES.md](USE_CASES.md)** — pick a goal, get the commands and the verify→submit path.
- **[detectors/readme.md](detectors/readme.md)** — the seven newer algorithms (DCS-grounded).
- **[ROADMAP.md](ROADMAP.md)** — phased plan for what's next.
- **[CLAUDE.md](CLAUDE.md)** — architecture, runtime/porting status, conventions.
- **[CHANGELOG.md](CHANGELOG.md)** — dated change history.

## faultfinder pipeline (detail)

The program sequence is 
```
php faultfinder3a.php MW sanhw1.txt AllvsMW/AllvsMW.txt AllvsMW/AllvsMW_sf.txt
php faultfinder3a-html.php AllvsMW/AllvsMW.txt AllvsMW/AllvsMW-norepeat.html
php dictwisesorter-v3.php AllvsMW/AllvsMW-norepeat.html AllvsMW/dictwiseerrors3-table.html
```

Their details are as follow:

```
php faultfinder3a.php MW sanhw1.txt AllvsMW.txt AllvsMW_sf.txt
```

faultfinder3a.php modification by ejf of faultfinder3.php
Nov 28, 2014
This is a command-line php program.
1. Read parameters from $argv
dictref ( a code for 'reference' dictionary)
wholedatafile (filename of a file in format as sanhw1.txt)
output (name of report output file)
sf-output (name of standard-format output file)
Usage from commandline only:
php faultfinder3a.php <dictref> <wholedatafile> <output> <sf-output>
Usage exampple:
php faultfinder3a.php MW sanhw1.txt AllvsMW.txt AllvsMW_sf.txt
Note 1: the headwords for dictref are derived from wholedata.
Thus, wholedata is the only input data source.
Note 2: output is written as a text file. The file is composed of
a sequence of lines, and each line has format
X:P=Y:D where
X is a headword
P is an abbreviated pattern name; for instance,
for pattern named Start-Consonant-Consonant, P=SCC
Y is the (first) instance of P which occurs in X
D is the comma-delimited list of dictionaries containing the word.
Note: It is an implication of the program logic that D does not contain
'dictref' as one of its components.
Note 2a: A separate program (faultfinder3a-html.php) may be used to
construct html output from a txt file in the format described in
Note 2.
Note 3. AllvsMW_sf.txt is the data in standard format as mentioned in https://github.com/sanskrit-lexicon/CORRECTIONS/issues/154. This format helps easy correction submission.

```
php faultfinder3a-html.php AllvsMW.txt AllvsMW-norepeat.html
```

faultfinder3a-html.php
ejf. Nov 28, 2014
Reads a file in format of that output by faultfinder3a,
and generates an html report, similar to that output by faultfinder3.
1. Read parameters from $argv
infile = input file name (e.g. AllvsMW.txt)
outfile = output file name (should end in html; e.g. AllvsMW.html)
Usage from commandline only:
php faultfinder3a-html.php <input> <output>
Note 1: The input file format is that of a file composed of
a sequence of lines, and each line has format
X:D1,D2...
where X is a headword and D1,D2... is a comma-separated list of
dictionary codes. X is a suspect headword (in that it has
a pattern which does not occur among the patterns of dictref),
and D1,D2, are the dictionaries where X occurs as a headword.
Note 2: It would be possible to add an <option> input parameter,
to make other output formats available.

```
php dictwisesorter-v3.php AllvsMW-norepeat.html dictwiseerrors3-table.html
```
modifications of Dec 8, 2014 so output is a table.
ref https://github.com/sanskrit-lexicon/CORRECTIONS/issues/42


# Current status
Issues #363 to #394 have handled all dicts versus MW, PW and PWG in that order.
Now it is getting less fruitful.
VCP is next on board.

# Less fruitful dictionaries.

It is not worthwhile to look into ACC, BHS, BUR, IEG, KRM, VEI because they are specialized dictionaries.
It is not worthwhile to look into PD, because it is relatively clean and it is peculiar that it handles only 'a' headwords.


# Logic

Let me document the method I have adopted to find the suspected wrong entries in #2. 
Code for checking is attached <a href="https://github.com/drdhaval2785/SanskritSpellCheck">here</a>. 
<a href="https://docs.google.com/document/d/1G4HoDz9nuj2GPeHQopNVSnDEGrnXtoAuXFugj4sQHZg/edit?usp=sharing">Google doc</a> for logic behind approach and instructions for dictionary /testers.
Video tutorial for code running - http://youtu.be/qLqYUZUGM6M
Video tutorial for noting issues on this correction forum - https://www.youtube.com/watch?v=rKZ_OsSHwsY

In short - the logic is as follows
1. We check the base dictionary for different Vowel and consonant patterns like VV, VCV, VCCV, VCCCV etc. (We presume that the base dictionary has correct entries - which need not be true).
2. We check the dictionary to be tested for different vowel and consonant patterns like 1 above.
3. If the pattern is not found in 1, but found in 2 - we note that in suspectfalse.html.
4. We check those entries from dictionary scans and verify.
5. If wrong word is detected, it is intimated to the webmaster <a href="https://github.com/sanskrit-lexicon/CORRECTIONS/issues">here</a>.

The latest version of the code is faultfinder3a.php (specific for finding errors from a headword list sanhw1.txt (https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/sanhw1.txt) of dictionaries hosted at http://www.sanskrit-lexicon.uni-koeln.de/).
It is a commandline code which can be executed as shown below.
Step 1 - CD to the directory containing faultfinder3a.php
Step 2 - type php faultfinder3a.php MW sanhw1.txt AllvsMW.txt AllvsMW_sf.txt. (This creates both the suspect report and CORRECTIONS standard-format output.)
Step 3 - type php faultfinder3a-html.php AllvsMW.txt AllvsMW-new.html (This will render AllvsMW.txt in an HTML file with links to individual entries for checking online)
Step 4 - type php dictwisesorter.php AllvsMW-new.html dictwiseerrors1.html (This will sort AllvsMW-new.html dictionarywise.)


# o_vs_O method

The steps are shown in [this readme](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/o_vs_O/backup/readme.txt)
