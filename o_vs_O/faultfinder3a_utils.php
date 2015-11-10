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
		$dicts[$j]=strip_tags($dicts[$j]);
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
function givelinktoo_vs_Otext2($text)
{
	global $count, $value;
    $x = explode('-',$text);
	$x = array_map('trim',$x);
	$dicts = explode(':',$x[1]);
	$words = explode(':',$x[0]);
	
	for ($j=0;$j<count($dicts);$j++)
	{
		$dicts[$j]=strip_tags($dicts[$j]);
		$culpritdict=explode(',',$dicts[$j]);
		$wordslinked[$j]=webpagelink($words[0],$words[1],$dicts[0],$dicts[1],$culpritdict,$j+1);
		for ($i=0;$i<count($culpritdict);$i++)
		{
			$d[$i]=$culpritdict[$i];
			$y[$i] = Cologne_hrefyear($d[$i]); 
			$rep[$i] = pdflink($d[$i],$words[$j]);
			//'<a href="http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict='.$d[$i].'&key='.$words[$j].'" target="_blank">'.$d[$i]."</a>";
			$culpritdict[$i] = str_replace($d[$i],$rep[$i],$culpritdict[$i]);
		}
		$dicts[$j]=implode(',',$culpritdict);
	}
	//return '<tr><td class="zero">'.$count.'</td><td class="one">'.get_decorated_diff($words[0],$words[1],1).'</td><td class="one">'.get_decorated_diff($words[0],$words[1],2).'</td><td class="two">'.convert($words[0]).'</td><td class="two">'.convert($words[1]).'</td><td class="three">'.$dicts[0].'</td><td class="four">'.$dicts[1].'</td></tr>';
	return '<tr><td class="zero">'.$count.'</td><td class="one">'.$wordslinked[0].'</td><td class="one">'.$wordslinked[1].'</td><td class="two">'.convert($words[0]).'</td><td class="two">'.convert($words[1]).'</td><td class="three">'.$dicts[0].'</td><td class="four">'.$dicts[1].'</td></tr>';
}

// Whether the given dictionary e.g. MW is in the dict string with lnumber 'MW;82,PW:150' 
function indict_with_lnum($needle,$haystack)
{
	// $haystack = "MW;82,PW:150";
	// $needle = "MW"
	//$members = explode(',',$haystack);
	$members = $haystack;
	for($i=0;$i<count($members);$i++)
	{
		$haydict[] = explode(';',$members[$i])[0];
	}
	if (in_array($needle,$haydict))
	{
		return true;
	}
	else 
	{
		return false;
	}
}
function lnum($text,$dict)
{
    $x = explode('-',$text);
	$x = array_map('trim',$x);
	$dicts = explode(':',$x[1]);
	foreach($dicts as $member)
	{
		$alldicts = explode(',',$member);
		foreach ($alldicts as $onedict)
		{
			list($dictchecked,$lnum) = explode(';',$onedict);
			if ($dictchecked === $dict)
			{
				return $lnum;
				break;
			}			
		}
	}
}
function removelnum($dictstring)
{
	$dicts = explode(',',$dictstring);
	$keep = array();
	foreach($dicts as $member)
	{
		$keep[] = explode(';',$member)[0];
	}
	return implode(',',$keep);
}
function givelinktoo_vs_Otext3($text)
{
	global $count, $value;
	$lnum = lnum($text,$value);
    $x = explode('-',$text);
	$x = array_map('trim',$x);
	$dicts = explode(':',$x[1]);
	$words = explode(':',$x[0]);
	
	for ($j=0;$j<count($dicts);$j++)
	{
		$dicts[$j]=removelnum($dicts[$j]);
		$dicts[$j]=strip_tags($dicts[$j]);
		$culpritdict=explode(',',$dicts[$j]);
		$wordslinked[$j]=webpagelink($words[0],$words[1],$dicts[0],$dicts[1],$culpritdict,$j+1);
		for ($i=0;$i<count($culpritdict);$i++)
		{
			$d[$i]=$culpritdict[$i];
			$y[$i] = Cologne_hrefyear($d[$i]); 
			$rep[$i] = pdflink($d[$i],$words[$j]);
			//'<a href="http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict='.$d[$i].'&key='.$words[$j].'" target="_blank">'.$d[$i]."</a>";
			$culpritdict[$i] = str_replace($d[$i],$rep[$i],$culpritdict[$i]);
		}
		$dicts[$j]=implode(',',$culpritdict);
	}
	//return '<tr><td class="zero">'.$count.'</td><td class="four">'.$lnum.'</td><td class="one">'.$wordslinked[0].'</td><td class="one">'.$wordslinked[1].'</td><td class="two">'.convert($words[0]).'</td><td class="two">'.convert($words[1]).'</td><td class="three">'.$dicts[0].'</td><td class="four">'.$dicts[1].'</td></tr>';
	return '<tr><td class="zero">'.$count.'</td><td class="zero">'.$lnum.'</td><td class="one">'.$wordslinked[0].'</td><td class="one">'.$wordslinked[1].'</td><td class="three">'.convert($words[0]).'</td><td class="three">'.convert($words[1]).'</td><td class="two">'.$dicts[0].'</td><td class="two">'.$dicts[1].'</td></tr>';
}

function pdflink($dict,$word)
{
	return '<a href="http://www.sanskrit-lexicon.uni-koeln.de/scans/awork/apidev/servepdf.php?dict='.$dict.'&key='.$word.'" target="_blank">'.$dict."</a>";
}
function webpagelink($oneword,$twoword,$onedict,$twodict,$culpritdict,$var)
{
	global $value;
	if ($var===1) 
	{
		$dictionary=$value; $inputword=$oneword;
	}
	if ($var===2) 
	{
		$preferredorder=array("PWG","PW","MW72","GRA");
		$dictionary=$culpritdict[0];
		for($x=0;$x<count($preferredorder);$x++)
		{
			if(in_array($preferredorder[$x],$culpritdict))
			{
				$dictionary=$preferredorder[$x];
				break;
			}
		}
		$inputword=$twoword;
	}
	$y=Cologne_hrefyear($dictionary);
	return '<a href="'."http://www.sanskrit-lexicon.uni-koeln.de/scans/".$dictionary."Scan/".$y."/web/webtc/indexcaller.php".'?key='.$inputword.'&input=slp1&output=SktDevaUnicode" target="_blank">'.get_decorated_diff($oneword,$twoword,$var)."</a>"; 
}
# See https://coderwall.com/p/3j2hxq/find-and-format-difference-between-two-strings-in-php for the origin of code.
function get_decorated_diff($old, $new, $var){
    $from_start = strspn($old ^ $new, "\0");        
    $from_end = strspn(strrev($old) ^ strrev($new), "\0");

    $old_end = strlen($old) - $from_end;
    $new_end = strlen($new) - $from_end;

    $start = substr($new, 0, $from_start);
    $end = substr($new, $new_end);
    $new_diff = substr($new, $from_start, $new_end - $from_start);  
    $old_diff = substr($old, $from_start, $old_end - $from_start);

    $new = "$start<b style='background-color:#ccffcc'>$new_diff</b>$end";
    $old = "$start<b style='background-color:#ffcccc'>$old_diff</b>$end";
	if ($var===1) { return $old; }
	if ($var===2) { return $new; }
	if ($var===0) { return array("old"=>$old, "new"=>$new); }
}
?>
