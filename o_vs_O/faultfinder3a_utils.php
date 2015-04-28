<?php
/* ejf Nov 28, 2014
 faultfinder3a_utils.php
 Contains two utility functions:
  faultfinder_patterns() and Cologne_hrefyear()

 The faultfinder_patterns() function
 returns a list (array) of pattern structures.
 Each pattern structure is an array of 3 elements:
  PATTERN-NAME - a name for printing. A '-' delimited string
  PATTERN - regex string, the pattern
  PATTERN-ABBREV - constructed from the first characters of the '-' parts.
    e.g., if PATTERN-NAME =  Start-Consonant-Consonant, then
             PATTERN-ABBREV = SCC

 The Cologne_hrefyear(dict) function returns
   the 'year' part associated on Cologne site with the dictionary code 'dict'.
  e.g., Cologne_hrefyear('MW') returns the string '2014'.
  Returns '?' if the 'dict' code is not known.

*/

include 'slp-dev.php';
function faultfinder_patterns() {
// Set up $pattern_data, an array for 
// running a for loop for 10 different type of Consonant, Vowel patterns.
$cpat='[kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSsh]';
$vpat='[aAiIuUfFxXeEoO]';
$spat = '^'; // start pattern
$epat = '$'; // end pattern

$pattern_data_raw = array(
 // array(<PATTTERN-NAME>,<PATTERN>)
 array("Vowel-Vowel","/($vpat$vpat)/"),
 array("Vowel-Consonant-Vowel","/($vpat$cpat$vpat)/"),
 array("Vowel-Consonant-Consonant-Vowel","/($vpat$cpat$cpat$vpat)/"),
 array("Vowel-Consonant-Consonant-Consonant-Vowel","/($vpat$cpat$cpat$cpat$vpat)/"),
 array("Vowel-Consonant-Consonant-Consonant-Consonant-Vowel","/($vpat$cpat$cpat$cpat$cpat$vpat)/"),
 array("Vowel-Consonant-Consonant-Consonant-Consonant-Consonant-Vowel","/($vpat$cpat$cpat$cpat$cpat$cpat$vpat)/"),
 array("Start-Consonant-Consonant","/($spat$cpat$cpat)/"),
 array("Consonant-Consonant-End","/($cpat$cpat$epat)/"),
 array("Consonant-Consonant-Consonant-End","/($cpat$cpat$cpat$epat)/"),
 array("Consonant-Consonant-Consonant-Consonant-End","/($cpat$cpat$cpat$cpat$epat)/")
);


// compute a pattern abbreviation from pattern-name
$pattern_data = array();
foreach($pattern_data_raw as $p){
 list($pattern_name,$pattern) = $p;
 // Get pattern abbreviation from pattern_name
 $patternAbbrev = pattern_abbreviation($pattern_name);
 $pattern_data[] = array($pattern_name,$pattern,$patternAbbrev);
}
return $pattern_data;

}

function pattern_abbreviation($pattern_name){
 $parts = preg_split('/-/',$pattern_name);
 $chars = array();
 foreach($parts as $part) {
  $chars[] = $part[0];
 }
 $c=join('',$chars);
 //echo "pattern_abbreviation: $pattern_name => $c\n";
 return $c;
}

function Cologne_hrefyear($dict) {
// This could be written using an associative array
$dictionaryname=array("ACC","CAE","AE","AP90","AP","BEN","BHS","BOP","BOR","BUR","CCS","GRA","GST","IEG","INM","KRM","MCI","MD","MW72","MW","MWE","PD","PE","PGN","PUI","PWG","PW","SCH","SHS","SKD","SNP","STC","VCP","VEI","WIL","YAT");
$hrefyear = array("2014","2014","2014","2014","2014","2014","2014","2014","2014","2013","2014","2014","2014","2014","2013","2014","2014","2014","2014","2014","2013","2014","2014","2014","2014","2013","2014","2014","2014","2013","2014","2013","2013","2014","2014","2014");
 $ans = '?';
 for($i=0;$i<count($dictionaryname);$i++) {
  if ($dict == $dictionaryname[$i]){
   $ans = $hrefyear[$i];
   break;
  }
 }
 return $ans;
}
//echo "faultfinder3a_utils is printing\n";

function givelinktoo_vs_Otext($text)
{
    $x = explode('-',$text);
	$x = array_map('trim',$x);
	$dicts = explode(':',$x[1]);
	$words = explode(':',$x[0]);
	
	for ($j=0;$j<count($dicts);$j++)
	{
		$culpritdict=explode(',',$dicts[$j]);
		for ($i=0;$i<count($culpritdict);$i++){
		$d[$i]=$culpritdict[$i];
		$y[$i] = Cologne_hrefyear($d[$i]); 
		$rep[$i] = '<a href="'."http://www.sanskrit-lexicon.uni-koeln.de/scans/".$d[$i]."Scan/".$y[$i]."/web/webtc/indexcaller.php".'?key='.$words[$j].'&input=slp1&output=SktDevaUnicode" target="_blank">'.$d[$i]."</a>"; // Keeping direct href because buttons fail to open in multiple tabs. They refresh the page.
		$culpritdict[$i] = str_replace($d[$i],$rep[$i],$culpritdict[$i]);
		}
		$dicts[$j]=implode(',',$culpritdict);
	}
//	echo convert($words[0])." : ".convert($words[1])." - ".$words[0]." : ".$words[1]." - ".$dicts[0]." : ".$dicts[1]."<br/>";
	return convert($words[0])." : ".convert($words[1])." - ".$words[0]." : ".$words[1]." - ".$dicts[0]." : ".$dicts[1]."<br/>";
//	echo $words[0].":".$words[1]."-".$dicts[0].":".$dicts[1]."<br/>";
}
function givelinktoo_vs_Otext1($text)
{
	global $count;
    $x = explode('-',$text);
	$x = array_map('trim',$x);
	$dicts = explode(':',$x[1]);
	$words = explode(':',$x[0]);
	
	for ($j=0;$j<count($dicts);$j++)
	{
		$culpritdict=explode(',',$dicts[$j]);
		for ($i=0;$i<count($culpritdict);$i++){
		$d[$i]=$culpritdict[$i];
		$y[$i] = Cologne_hrefyear($d[$i]); 
		$rep[$i] = '<a href="'."http://www.sanskrit-lexicon.uni-koeln.de/scans/".$d[$i]."Scan/".$y[$i]."/web/webtc/indexcaller.php".'?key='.$words[$j].'&input=slp1&output=SktDevaUnicode" target="_blank">'.$d[$i]."</a>"; // Keeping direct href because buttons fail to open in multiple tabs. They refresh the page.
		$culpritdict[$i] = str_replace($d[$i],$rep[$i],$culpritdict[$i]);
		}
		$dicts[$j]=implode(',',$culpritdict);
	}
//	echo convert($words[0])." : ".convert($words[1])." - ".$words[0]." : ".$words[1]." - ".$dicts[0]." : ".$dicts[1]."<br/>";
	return '<tr><td class="zero">'.$count.'</td><td class="one">'.$words[0].'</td><td class="one">'.$words[1].'</td><td class="two">'.convert($words[0]).'</td><td class="two">'.convert($words[1]).'</td><td class="three">'.$dicts[0].'</td><td class="four">'.$dicts[1].'</td></tr>';
//	echo $words[0].":".$words[1]."-".$dicts[0].":".$dicts[1]."<br/>";
}

?>
