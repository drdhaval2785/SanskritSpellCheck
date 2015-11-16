# php o_vs_O_sanhw2.php takes a lot of time. 
# Therefore, use only o_vs_O2.txt preferrably. 
# You would want to regenerate o_vs_O2.txt only if sanhw2.txt is altered.
echo "Running o_vs_O_sanhw2.php and storing in o_vs_O2.txt."
echo 
#php o_vs_O_sanhw2.php
echo "Running dictsorting_single.php."
echo 
php dictsorting_single.php
echo "Running sortlen.py."
echo 
python sortlen.py
echo "Running decoratehtml.php."
echo 
php decoratehtml.php
