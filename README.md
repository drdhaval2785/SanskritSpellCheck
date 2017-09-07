SanskritSpellCheck
==================

from faultfinder3a.php - the machine is commandline tool now.

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
output ( name of output file)
Usage from commandline only:
php faultfinder3a.php <dictref> <wholedatafile> <output>
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
Step 2 - type php faultfinder3a.php MW sanhw1.txt AllvsMW.txt. (This will create a file having suspect wrong entries from sanhw1.php when compared to MW as base.) 
Step 3 - type php faultfinder3a-html.php AllvsMW.txt AllvsMW-new.html (This will render AllvsMW.txt in an HTML file with links to individual entries for checking online)
Step 4 - type php dictwisesorter.php AllvsMW-new.html dictwiseerrors1.html (This will sort AllvsMW-new.html dictionarywise.)


# o_vs_O method

The steps are shown in [this readme](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/o_vs_O/readme.txt)