# Generate error list without L IDs

Inputs: sanhw1.txt

Dependencies: dev-slp.php, faultfinder3a-utils.php, function.php, slp-dev.php.

Step1 - From commandline run `php o_vs_O.php`.

Step2 - This gives two outputs. `o_vs_O1.txt` is the raw form. `o_vs_O2.txt` is form with refractoring (i.e. after removal of unnecessary words).

Step3 - Create a folder named `output1` in the same directory.

Step4 - From commandline run `php dictsorting.php`.

Step5 - This creates two files for each dictionary - one .txt file (word1:word2-dict1:dict2 format) and one .html file (Tabular presentation with links to the Cologne dictionaries and Devanagari display also).

Step6 - Click links from these HTML files and verify the errors.

# Generate error list with L IDs (Better alternative)

Inputs: sanhw2.txt

Dependencies: dev-slp.php, faultfinder3a-utils.php, function.php, slp-dev.php.

Step1 - From commandline run `php o_vs_O_sanhw2.php`.

Step2 - This gives two outputs. `o_vs_O1.txt` is the raw form. `o_vs_O2.txt` is form with refractoring (i.e. after removal of unnecessary words).

Step3 - Create a folder named `output2` in the same directory.

Step4 - From commandline run `php dictsorting_sanhw2.php`.

Step5 - This creates two files for each dictionary - one .txt file (word1:word2-dict1:dict2 format) and one .html file (Tabular presentation with links to the Cologne dictionaries and Devanagari display also).

Step6 - Click links from these HTML files and verify the errors.

Major addition in this version is the L IDs.

# Generate a composite HTML for all dictionaries simultaneously. (Best alternative)

Inputs: o_vs_O2.txt

Dependencies: dev-slp.php, faultfinder3a-utils.php, function.php, slp-dev.php.

Step1 - run `composite.sh`.

Outputs - 

1. Output3/composite1.txt - first word in one dictionary and second word in many dictionaries.

2. Output3/composite2.txt - first word in one dictionary and second word in one dictionary.

3. Output3/composite3.txt - first word in many dictionary and second word in many dictionaries.

4. Output3/composite1a.txt - composite1.txt sorted in descending order of length of word (Highest probability).

5. Output3/composite2a.txt - composite2.txt sorted in descending order of length of word (Medium probability).

6. Output3/composite3a.txt - composite3.txt sorted in descending order of length of word (Almost next to nil probability).

7. Output3/composite1a.html - composite1a.txt displayed with links for comparision (Highest probability).

8. Output3/composite2a.html - composite2a.txt displayed with links for comparision (Medium probability).

9. Output3/composite3a.html - composite3a.txt displayed with links for comparision (Almost next to nil probability).

10. Output3/composite1b.txt - composite1a.txt displayed with alternative for machine processing. See [issue 154](https://github.com/sanskrit-lexicon/CORRECTIONS/issues/154).

11. Output3/composite2b.txt - composite2a.txt displayed with alternative for machine processing. See [issue 154](https://github.com/sanskrit-lexicon/CORRECTIONS/issues/154).

12. Output3/composite3b.txt - composite3a.txt displayed with alternative for machine processing. See [issue 154](https://github.com/sanskrit-lexicon/CORRECTIONS/issues/154).

# Statistics of o_vs_O1.txt v/s o_vs_O2.txt
1. On 15 Nov 2015 - 21989 : 19140 (Started keeping track)
2. On 16 Nov 2015 - 21989 : 14662 (Removed entries which had more than one letter difference and which had difference in y/Y/r/R only)
3. On 16 Nov 2015 - 21989 : 14103 (Removed entries which had less than 4 letters length.)
4. On 16 Nov 3015 - 21989 : 4253 (Removed entries where both sided had the same dictionary e.g. Both words appear in the same dictionary)
