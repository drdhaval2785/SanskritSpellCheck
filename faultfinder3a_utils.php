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
function faultfinder_patterns() {
// Set up $pattern_data, an array for 
// running a for loop for 10 different type of Consonant, Vowel patterns.
$cpat='[kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs]';
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

?>
