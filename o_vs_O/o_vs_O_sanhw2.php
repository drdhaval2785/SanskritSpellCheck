<?php
//error_reporting(0);
/* set execution time to an hour */
ini_set('max_execution_time', 36000);
/* set memory limit to 1000 MB */
ini_set("memory_limit","1000M");
// giving links to the list of .txt and converting to html
include 'faultfinder3a_utils.php';
$header = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
<!--... Defining UTF-8 as our default character set, so that devanagari is displayed properly. -->
<meta charset="UTF-8">
<!--... Defining CSS -->
<link rel="stylesheet" type="text/css" href="mystyle.css">
<!--... including Ajax jquery. -->
</head> 
<body>
';
$counter=0;

$nochange = file('../nochange/nochange.txt');
$nochange = array_map('trim',$nochange);
/* Executing function prepareliststs */
// This program was run only once. The output was stored as variables.
echo "Started preparing lists of words from sanhw2.txt<br/>\n";
$words = preparelists()[0];
echo "Completed preparing lists of words from sanhw2.txt<br/>\n";
echo "Started preparing lists of dictionaries from sanhw2.txt<br/>\n";
$dicts = preparelists()[1];
echo "Completed preparing lists dictionaries from sanhw2.txt<br/>\n";
/* Putting data in o_vs_O1.txt file after comparing. */
//comparedicts();
/* Opening o_vs_O1.txt and refractoring and putting in o_vs_O2.txt */
refractor();

function preparelists()
{
	$file = file("sanhw2.txt");
	for ($i=0;$i<count($file);$i++)
	{
		$parts[$i] = explode(':',$file[$i]);
		$words[$i] = $parts[$i][0];
		$dicts[$i] = trim($parts[$i][1]);
	}
	$array[0] = $words;
	$array[1] = $dicts;
	return $array;
}
function similar($text,$start,$end)
{
	echo "Starting ".$start." to ".$end."<br/>\n";
	global $dicts, $words, $counter;
	$outfile = fopen("o_vs_O1.txt","a+");
	for($i=$start;$i<$end;$i++)
	{
		for($j=$i+1;$j<$end;$j++)
		{
			if (strcasecmp($text[$i],$text[$j])===0 && $text[$i]!==$text[$j] && strpos($dicts[$i],"PD")===false && strpos($dicts[$j],"PD")===false && removelnum($dicts[$i])!==removelnum($dicts[$j]) && !(in_array(substr($text[$i],-1),array("a","A","m","M")) && substr($text[$i],-1)!==substr($text[$j],-1) ) )
			{
				fputs($outfile,$text[$i].":".$text[$j]."-".$dicts[$i].":".$dicts[$j]."\n");
				$counter++;
			}
		}
	}
	fclose($outfile);
	echo "Total of $counter entries written to o_vs_O1.txt cumulatively<br/>\n";
}
function comparedicts()
{
	echo "Starting to compare dictionaries for similar entries.<br/>\n";
	$outfile=fopen("o_vs_O1.txt","w+");
	global $words, $dicts;
	// comparing in slots of 10000
	for($i=0;$i<count($words);$i++)
	{
		similar($words,$i,$i+10000);
		$i=$i+10000;
	}
	fclose($outfile);	
}
function refractor()
{
	echo "Started refractoring.<br/>\n";
	global $header, $nochange;
	$raw = file('o_vs_O1.txt');
	$outfile = fopen("o_vs_O2.txt","w+");
	$nasal = array("N","Y","R","n","m");
	$anu = array("M","M","M","M","M");
	$counter=1;
	foreach ($raw as $value)
	{
		$val = preg_split('/([-:])/',$value);
		$val = array_map('trim',$val);
		$dict = preg_split('/([:-])/',$value);
		$dict = array_map('trim',$dict);
		$firstdictstring = removelnum($dict[2]);
		$firstdictarray = explode(',',$firstdictstring);
		$seconddictstring = removelnum($dict[3]);
		$seconddictarray = explode(',',$seconddictstring);
		// Adding some more qualifications
		if (count($val)===count(array_unique($val)) && str_replace($nasal,$anu,$val[0])!==str_replace($nasal,$anu,$val[1]) && !in_array(substr($val[1],-3),array("AMs","Ant")) && removelnum($dict[2])!=="BHS" && removelnum($dict[3])!=="BHS" && !in_array(get_diff($val[0],$val[1]),array("y","Y","r","R")) && strlen(get_diff($val[0],$val[1]))===1 && strlen($val[0])>3 && count(array_intersect($firstdictarray,$seconddictarray))===0 && !in_array($val[0],$nochange) &&  !in_array($val[1],$nochange) )
		{
			echo $val[0]."<br/>\n";
			fputs($outfile,$value);
			$counter++;
		}
	}
	echo "Total of $counter entries culled out and saved to o_vs_O2.txt.<br/>\n";
}
?>