<?php  
/*
error_reporting(E_ALL);
ini_set('display_errors', '1');
*/
error_reporting(0);
/* faultfinder3a-html.php 
   ejf.  Nov 28, 2014
   Reads a file in format of that output by faultfinder3a,
   and generates an html report, similar to that output by faultfinder3.
  1. Read parameters from $argv
    infile  = input file name (e.g. AllvsMW.txt)
    outfile = output file name (should end in html; e.g. AllvsMW.html)
  
    Usage from commandline only:
     php faultfinder3a-html.php <input> <output>
    Note 1:  The input file format is that of a file composed of
      a sequence of lines, and each line has format
      X:D1,D2...     
      where X is a headword and D1,D2...  is a comma-separated list of
        dictionary codes.  X is a suspect headword (in that it has
        a pattern which does not occur among the patterns of dictref),
        and D1,D2,   are the dictionaries where X occurs as a headword.
    Note 2: It would be possible to add an <option> input parameter,
        to make other output formats available.
*/
/* This code is written by Dr. Dhaval Patel of www.sanskritworld.in.
 * Video tutorial for its use is available at http://youtu.be/qLqYUZUGM6M
 * Code is available at https://github.com/drdhaval2785/SanskritSpellCheck.
 * https://www.youtube.com/watch?v=rKZ_OsSHwsY&feature=youtu.be is the method of finding and noting wrong entries at https://github.com/sanskrit-lexicon/CORRECTIONS/issues
 * Google doc for understanding the logic behind the machine is https://docs.google.com/document/d/1G4HoDz9nuj2GPeHQopNVSnDEGrnXtoAuXFugj4sQHZg/edit?usp=sharing
 */
 
// include these two files for conversion
if(True){echo "check0\n";}
/*
include "dev-slp.php";
*/
include "slp-dev.php";
// get pattern data
if(True){echo "check1a\n";}
include "faultfinder3a_utils.php";
if(True){echo "check1b\n";}
$pattern_data = faultfinder_patterns();
if(True){echo "check1\n";}
// Read input parameters
$input = $argv[1]; // AllvsMW.txt";
$output = $argv[2];  //AllvsMW.html";
$repeat = $argv[3]; // 1 for allowing more than one dictionary words. 0 for allowing only one dictionary words. Default is 0.
if (!$repeat){
    $repeat='0'; // setting default value of $repeat
}
// read and parse input file 
$fin = fopen($input,"r");
$inrecs = array();
while(! feof($fin)) {
 $line = fgets($fin);
 $line = trim($line);
 if ($line == ''){
   continue;
 }
 list($key,$pat0,$dicts) = explode(':',$line);
 list($patabbrev,$patvalue) = explode('=',$pat0);
 $dictnumbers = count(explode(',',$dicts)); // added by Dr. Dhaval Patel for removing words occurring in more than one dicts. 6 Dec 2014
    if ($repeat==='1')
    {
        $inrecs[] = array($key,$patabbrev,$patvalue,$dicts); // original by ejf.        
    }
    if ($repeat ==='0')
    {
        $inrecs[] = array($key,$patabbrev,$patvalue,$dicts,$dictnumbers); // amendment by Dr. Dhaval Patel.         
    }
}
fclose($fin);
echo count($inrecs) . " records read from $input\n";
faultfinder3a_html_option1($inrecs,$output,$pattern_data);
exit(0);
/*
  option 1 output function
*/
function faultfinder3a_html_option1($inrecs,$output,$pattern_data){
 $outfile=fopen($output,"w");  // completely overwrite
 global $repeat;
echo "repeat is $repeat";
 // add HTML header
fputs($outfile,"<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n<html xmlns=\"http://www.w3.org/1999/xhtml\">\n
<head>\n
  <META HTTP-EQUIV=\"Content-Language\" CONTENT=\"HI\">\n
  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\n
  </meta>\n
<!-- javascript function for making links.  -->
<script type=\"text/javascript\">
 function linkto(key,dictcode,dictyear) {
  var href = \"http://www.sanskrit-lexicon.uni-koeln.de/scans/\" +
    dictcode + \"Scan/\" + dictyear + \"/web/webtc/indexcaller.php?key=\" + key 
    + \"&input=slp1&output=SktDevaUnicode\";
  window.open(href,\"dictionary\");
  return false;
 }
</script>
</head>\n
<body>\n");

foreach($pattern_data as $pattern_datum) {
 list($pattern_name,$pattern,$pattern_abbrev) = $pattern_datum;
 fputs($outfile,"<b style=\"color:red\">This is $pattern_name pattern.</b><br>\n");
 // filter the inrecs for those with this pattern_abbrev
 foreach($inrecs as $inrec) {
     if ($repeat==='1')
     {
        list($key,$patabbrev,$patvalue,$dicts) = $inrec; // original by ejf.         
     }
     if ($repeat === '0')
     {
        list($key,$patabbrev,$patvalue,$dicts,$dictnumbers) = $inrec; // Alteration by Dr. Dhaval Patel.         
     }
  if($patabbrev != $pattern_abbrev) {
   continue; // skip
  }
    if ($repeat === '1')
    {
        fputs($outfile,givelink($dicts,$key)."</br>\n"); // original by ejf.        
    }
    if ($repeat == '0')
    {
    // Keeping only the words occurring in only one dictionary.
        if ($dictnumbers===1)
        {
        fputs($outfile,givelink($dicts,$key)."</br>\n");      
        } // This if portion is amendment by Dr. Dhaval Patel.        
    }
 }
}
fputs($outfile,'</body></html>');
fclose($outfile);
}

function givelink($dictstring,$input)
{
    $culpritdict = explode(',',$dictstring);
    $linkarr = array();
    foreach ($culpritdict as $d){
     $y = Cologne_hrefyear($d); 
     $text = "<button onclick='linkto(\"$input\",\"$d\",\"$y\");return false;'>$d</button>";
     $linkarr[] = $text;
    }        
    $linktext = join(" ",$linkarr);
    $output = $input." - ".convert($input)." - ".$linktext;
    return $output;
}
    
?>
