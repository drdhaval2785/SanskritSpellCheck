<?php  
/* modifications of Dec 8, 2014  so output is a table.
  ref https://github.com/sanskrit-lexicon/CORRECTIONS/issues/42
  Usage:
php faultfinder3a.php MW sanhw1.txt AllvsMW.txt
php faultfinder3a-html.php AllvsMW.txt AllvsMW-norepeat.html
php dictwisesorter-v3.php AllvsMW-norepeat.html dictwiseerrors3-table.html
 
*/
/*
error_reporting(E_ALL);
ini_set('display_errors', '1');
*/
/* faultfinder1.php  modification by ejf of faultfinder.php
  1. Read parameters from $argv
    dicta  ( a code for first dictionary)
    dictb  ( a code for second dictionary)
    dictref ( a code for href )
    output ( name of output file)
    Usage from commandline only:
     php faultfinder1.php <dict1> <dict2> <dictref> <output>
*/
/* This code is written by Dr. Dhaval Patel of www.sanskritworld.in.
 * Video tutorial for its use is available at http://youtu.be/qLqYUZUGM6M
 * Code is available at https://github.com/drdhaval2785/SanskritSpellCheck.
 * https://www.youtube.com/watch?v=rKZ_OsSHwsY&feature=youtu.be is the method of finding and noting wrong entries at https://github.com/sanskrit-lexicon/CORRECTIONS/issues
 * Google doc for understanding the logic behind the machine is https://docs.google.com/document/d/1G4HoDz9nuj2GPeHQopNVSnDEGrnXtoAuXFugj4sQHZg/edit?usp=sharing
 */
 
/* set execution time to an hour */
ini_set('max_execution_time', 36000);
/* set memory limit to 1000 MB */
ini_set("memory_limit","1000M");
// include these two files for conversion
include "dev-slp.php";
include "slp-dev.php";

$dictionaryname=array("ACC","CAE","AE","AP90","AP","BEN","BHS","BOP","BOR","BUR","CCS","GRA","GST","IEG","INM","KRM","MCI","MD","MW72","MW","MWE","PD","PE","PGN","PUI","PWG","PW","SCH","SHS","SKD","SNP","STC","VCP","VEI","WIL","YAT");
$hrefyear = array("2014","2014","2014","2014","2014","2014","2014","2014","2014","2013","2014","2014","2014","2014","2013","2014","2014","2014","2014","2014","2013","2014","2014","2014","2014","2013","2014","2014","2014","2013","2014","2013","2013","2014","2014","2014");

//$dat = file_get_contents('AllvsMW-new.html');
$argument1 = $argv[1];
$dat = file_get_contents($argument1);
//$outfile2=fopen("dictionarywiseerrors2.html","w");
$argument2 = $argv[2];
$outfile2 = fopen($argument2,"w");
fputs($outfile2,"<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n<html xmlns=\"http://www.w3.org/1999/xhtml\">\n
<head>\n
  <META HTTP-EQUIV=\"Content-Language\" CONTENT=\"HI\">\n
  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\n
  </meta>\n
</head>\n
<body>\n");

$data = explode("</br>",$dat);
echo "\n".count($data)."records \n";
foreach ($dictionaryname as $value)
{
    fputs($outfile2,"<H1>$value</H1>\n");
    fputs($outfile2,"<table border='1' style='width:600px'>\n");
    foreach ($data as $val1)
    {
        if (strpos($val1,">".$value."<")!==false)
        {   // scrape html for this line into 4 parts
            $parts = explode(" - ",$val1);
	    $nparts = count($parts);
            if ($nparts != 4) { // check there are expected # of parts
             echo "WARNING: $val1\n";
            }
            $outarr = array("\n<tr>"); // start table row
            foreach($parts as $part) {
	     $outarr[] = "<td>$part</td>";
	    }
	    $outarr[] = "</tr>\n";  // end table row
	    $out = join("",$outarr);
            fputs($outfile2,"$out");
            //fputs($outfile2,$val1."</br>");            
        }
        
    }
    //fputs($outfile2,"</br>");
    fputs($outfile2,"</table>\n");  // close table
}
fclose($outfile2);

?>
