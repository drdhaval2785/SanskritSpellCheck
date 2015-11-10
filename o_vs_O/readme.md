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

# Generate a composite HTML for all dictionaries simultaneously.


Inputs: sanhw2.txt

Dependencies: dev-slp.php, faultfinder3a-utils.php, function.php, slp-dev.php.




# Note: 
Please focus only on the corrections in the dictionary under consideration.
If you see any errors in the dictionary other than the one you are dealing with, leave it.
You will encounter it in the dictionary concerned. We will treat it there.

