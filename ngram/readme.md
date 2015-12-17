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
