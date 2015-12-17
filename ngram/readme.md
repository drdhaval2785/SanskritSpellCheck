# Spellcheck by bigrams and trigrams

To compare n-grams of a given text against the possible ngrams extracted and put in 'data' folder as 2grams.txt and 3grams.txt

# Usage 1:
Put your test file in data/test.txt and click on ngramspellcheck.sh.
Your suspect errors are stored in data/error.txt.

# Usage 2:
`python ngramspellcheck.py inputfile filetostoreerrors n`
e.g.
`python ngramspellcheck.py data/test.txt data/error.txt 2`

It is advisable to try for bigrams only (n=2) to minimize false positives.
It can be extended to trigrams and higher ngrams, but it would increase false positives too much.

# Dictionaries used
MW PW PWG PD MW72 VCP SHS YAT WIL SKD CAE AP ACC AP90 CCS SCH STC MD BUR BHS BEN

# What are the file in data folder

1. 2grams.txt - 1078 bigrams which are common to both MW and PW.
2. 3grams.txt - 11931 trigrams which are common to both MW and PW.
3. test.txt - The file where you should put your test data in SLP1 format.
4. error.txt - The file where you would get your potentially erraneous words after execution of script ngramspellcheck.sh
5. stripgretil.txt - Stores the abbreviations used by GRETIL. Tries to filter out issues of direct copy pasting from GRETIL.
6. whiteends.txt - `declinedend:undeclinedend` format.
7. whitelist.txt - 2grams which are found OK on testing with data. You can also add your OK bigrams here. It would not be shown as error on subsequent run of the code.
