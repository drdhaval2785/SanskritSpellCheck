mkdir Allvs$1
echo "Step 1. Generate AllvsDict.txt and AllvsDict_sf.txt"
php faultfinder3a.php $1 sanhw1.txt Allvs$1/Allvs$1.txt Allvs$1/Allvs$1_sf.txt
echo "Step 2. Generate HTML file having unique entries."
php faultfinder3a-html.php Allvs$1/Allvs$1.txt Allvs$1/Allvs$1-norepeat.html
echo "Step 3. Sort the entries according to dictionarywise and present in table form."
php dictwisesorter-v3.php Allvs$1/Allvs$1-norepeat.html Allvs$1/dictwiseerrors3-table.html
