<?php  
/*
error_reporting(E_ALL);
ini_set('display_errors', '1');
*/
/* faultfinder3a.php  modification by ejf of faultfinder3.php
   Nov 28, 2014
  This is a command-line php program.
  1. Read parameters from $argv
    dictref  ( a code for 'reference' dictionary)
    wholedatafile (filename of a file in format as sanhw1.txt)
    output ( name of output file)
    Usage from commandline only:
     php faultfinder3a.php <dictref> <wholedatafile> <output>
    Usage exampple:
     php faultfinder3a.php MW sanhw1.txt AllvsMW.txt
    Note 1: the headwords for dictref are derived from wholedata.
      Thus, wholedata is the only input data source.
    Note 2:  output is written as a text file. The file is composed of
      a sequence of lines, and each line has format
      X:P=Y:D    where
      X is a headword 
      P is an abbreviated pattern name; for instance,
        for pattern named Start-Consonant-Consonant, P=SCC
      Y is the (first) instance of P which occurs in X
      D is the comma-delimited list of dictionaries containing the word.
        Note: It is an implication of the program logic that D does not contain
	'dictref' as one of its components.
    Note 2a:  A separate program  (faultfinder3a-html.php) may be  used to
      construct html output from a txt file in the format described in
      Note 2.
*/
/* This code is written by Dr. Dhaval Patel of www.sanskritworld.in.
 * Video tutorial for its use is available at http://youtu.be/qLqYUZUGM6M
 * Code is available at https://github.com/drdhaval2785/SanskritSpellCheck.
 * https://www.youtube.com/watch?v=rKZ_OsSHwsY&feature=youtu.be is the method of finding and noting wrong entries at https://github.com/sanskrit-lexicon/CORRECTIONS/issues
 * Google doc for understanding the logic behind the machine is https://docs.google.com/document/d/1G4HoDz9nuj2GPeHQopNVSnDEGrnXtoAuXFugj4sQHZg/edit?usp=sharing
 */
 /* set memory limit to 1000 MB */
ini_set("memory_limit","1000M");
error_reporting(E_ALL ^ E_NOTICE);
/* get command-line arguments */
 $dictref = $argv[1]; // 'MW';
 $wholedatafile = $argv[2]; // sanhw1.txt
 $output = $argv[3];  //AllvsMW.txt";
// get pattern data
include "faultfinder3a_utils.php";
$pattern_data = faultfinder_patterns();
// open file where we store the suspect wrong entries.
$outfile=fopen($output,"w");  // completely overwrite

// read wholedatafile into array of trimmed lines
$wholedata = file($wholedatafile);
$wholedata = array_map('trim',$wholedata);
$nwholedata = count($wholedata);
echo "$wholedatafile has $nwholedata lines\n";

// read whitelisted words
$whitelistwords = file('nochange/nochange.txt');
$whitelistwords = array_map('trim',$whitelistwords);

/* parse lines of wholedata into parallel arrays worddata, dictdata
  For instance, if element $i of wholedata is
  aMSaH:AP,AP90,SKD
  then
  $worddata[$i] == 'amSaH'  and
  $dictdata[$i] == array('AP','AP90','SKD')
*/
$worddata=array();
$dictdata=array();
if(False) { // dbg
 echo "Check a\n";
 $nwholedata = 1000; // for debug
}
for ($i=0;$i<$nwholedata;$i++)
{
  list($worddata[$i],$dictdatastring) = explode(':',$wholedata[$i]);
  $dictdata[$i] = explode(',',$dictdatastring);
}

// $filea contains $worddata[$i] provided $dictref is in array $dictdata[$i]
$filea = array();
for ($i=0;$i<$nwholedata;$i++) {
 if (in_array($dictref,$dictdata[$i])) {
  $filea[]=$worddata[$i];
 }
}
if (count($filea) == 0) {
 echo "dictref error: no matches: $dictref\n";
 exit(1);
}
echo count($filea) . " keys in $wholedatafile match $dictref\n";

// 03 September 2017. Started removing whitelisted words from generation of txt file.
#$fileb = $worddata;
$fileb = array_diff($worddata,$whitelistwords);

$unused_dictionaryname=array("ACC","CAE","AE","AP90","AP","BEN","BHS","BOP","BOR","BUR","CCS","GRA","GST","IEG","INM","KRM","MCI","MD","MW72","MW","MWE","PD","PE","PGN","PUI","PWG","PW","SCH","SHS","SKD","SNP","STC","VCP","VEI","WIL","YAT");
$unused_hrefyear = array("2014","2014","2014","2014","2014","2014","2014","2014","2014","2013","2014","2014","2014","2014","2013","2014","2014","2014","2014","2014","2013","2014","2014","2014","2014","2013","2014","2014","2014","2013","2014","2013","2013","2014","2014","2014");

foreach($pattern_data as $pattern_datum) {
 comparepatterns($filea,$pattern_datum,$fileb,$outfile); 
}

/* function comparepatterns 
 * $filea is the file contents of dictionary whose pattern we want to take as input (Base).
 * $pattern_datum refers to the pattern we want to check. 
    It is a list of thre elements:
    $pattern_name = a '-' separated list of names
    $pattern  = the pattern (a regex in string form)
    $pattern_abbrev
 * $filec is the contents of dictionary file to be checked.
 $outfile - File handle for output
 */

function comparepatterns($filea,$pattern_datum,$filec,$outfile)
{
	global $dictdata, $worddata;
	list($pattern_name,$pattern,$patternAbbrev) = $pattern_datum;
	$file = $filea;
	$vccccv=array();
	foreach ($file as $value)
	{
		if(preg_match($pattern,$value))
		{
			$vccccvraw = preg_split($pattern,$value,null,PREG_SPLIT_DELIM_CAPTURE);
			$i=2;
			while($i<count($vccccvraw))
			{
				if(!in_array($vccccvraw[$i-1],$vccccv))
				{$vccccv[]=$vccccvraw[$i-1];
				}
				$i=$i+2;
			}
		}
	}
	$vccccv = array_unique($vccccv);
	$vccccv = array_values($vccccv);
		// checking the second file.
		$file1 = $filec;
		for ($j=0;$j<count($file1);$j++)
		{
			$value=$file1[$j];
			$wpats=array(); // Patterns flagged for this word
			if(preg_match($pattern,$value))
			{
				$vccccvex = preg_split($pattern,$value,null,PREG_SPLIT_DELIM_CAPTURE);        
				$i=2;
				while ($i<count($vccccvex))
				{
				 // if not found in the patterns already noted -
			 // flag it as suspect pattern and enter in output
					if ( !in_array($vccccvex[$i-1],$vccccv ))
					{$wpats[]=$vccccvex[$i-1];
					}
					$i=$i+2;
				}
			}
			if (count($wpats) > 0) {
		  // generate output
			  //$dictmatch = givelink($dictdata[$j]);
		  $dictmatch = join(',',$dictdata[$j]);
			  $w = $worddata[$j];
			  // just use the first pattern. There are a handful of multiple patts
		  $wpat = $wpats[0];
			  // Put in pattern abbrev, for later 
			  $wpat1 = "$patternAbbrev=$wpat";
			  fwrite($outfile,"$w:$wpat1:$dictmatch\n");
			  if(count($wpats) > 1) { // curious about this
			   //echo "DUP pattern: $w:$wpat:$dictmatch\n";
			 }
		}
		}
}
    fclose($outfile);


function unused_givelink($culpritdict)
{
    global $dictionaryname, $hrefyear;
    $linkarr = array();
    for($j=0;$j<count($dictionaryname);$j++)
    {    
        foreach ($culpritdict as $culvalue)
        {
        if ($culvalue===$dictionaryname[$j])
        {
         $linkarr[] = $dictionaryname[$j];
        }
        }
    }        
    $linktext = join(",",$linkarr);
    return $linktext;
}

?>
