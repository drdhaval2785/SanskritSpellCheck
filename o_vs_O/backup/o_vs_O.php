<?php
//error_reporting(0);
/* set execution time to an hour */
ini_set('max_execution_time', 36000);
/* set memory limit to 1000 MB */
ini_set("memory_limit","1000M");
include "dev-slp.php";
include "function.php";
include "slp-dev.php";
// giving links to the list of .txt and converting to html
include 'faultfinder3a_utils.php';

/* Executing function prepareliststs */
// This program was run only once. The output was stored as variables
preparelists();
/* Putting data in o_vs_O1.txt file after comparing. */
comparedicts();
/* Opening o_vs_O1.txt and refractoring and putting in o_vs_O1.html */
refractor();

function preparelists()
{
	$file = file("sanhw1.txt");
	for ($i=0;$i<count($file);$i++)
	{
		$parts[$i] = explode(':',$file[$i]);
		$words[$i] = $parts[$i][0];
		$dicts[$i] = trim($parts[$i][1]);
	}
//	echo '$words=array("'.implode('","',$words).'");';
//	echo '$dicts=array("'.implode('","',$dicts).'");';	
	global $words, $dicts;
}
// comparing the dictionaries
function similar($text,$start,$end)
{
	echo "Starting ".$start." to ".$end."<br/>";
	global $outfile, $dicts;
	$counter=0;
	for($i=$start;$i<$end;$i++)
	{
		for($j=$i+1;$j<$end;$j++)
		{
			if (strcasecmp($text[$i],$text[$j])===0 && $text[$i]!==$text[$j] && strpos($dicts[$i],"PD")===false && strpos($dicts[$j],"PD")===false && $dicts[$i]!==$dicts[$j] && !(in_array(substr($text[$i],-1),array("a","A","m","M")) && substr($text[$i],-1)!==substr($text[$j],-1) ))
			{
				fputs($outfile,$text[$i].":".$text[$j]." - ".$dicts[$i].":".$dicts[$j]."\n");
				$counter++;
			}
		}
	}
	echo $counter."<br/>";
}
function comparedicts()
{
	global $words;
	$outfile=fopen("o_vs_O1.txt","w+");
	// comparing in slots of 10000
	for($i=0;$i<410000;$i++)
	{
		similar($words,$i,$i+10000);
		$i=$i+10000;
	}
	fclose($outfile);	
}
function refractor()
{
	$raw = file('o_vs_O1.txt');
	$outfile = fopen("o_vs_O1.html","w+");
	$nasal = array("N","Y","R","n","m");
	$anu = array("M","M","M","M","M");
	$counter=1;
	foreach ($raw as $value)
	{
		$val = preg_split('/([-:,])/',$value);
		$val = array_map('trim',$val);
		$dict = preg_split('/([:-])/',$value);
		$dict = array_map('trim',$dict);
		// Adding some more qualifications
		if (count($val)===count(array_unique($val)) && str_replace($nasal,$anu,$val[0])!==str_replace($nasal,$anu,$val[1]) && !in_array(substr($val[1],-3),array("AMs","Ant")) && $dict[2]!=="BHS" && $dict[3]!=="BHS" )
		{
			fputs($outfile,givelinktoo_vs_Otext($value)."<br>\n");	
			$counter++;
		}
	}
	echo $counter;	
}
// 7148 entries with no adjustments for nasals
// 5392 entries with adjustments for nasals
// 5351 entries with adjustments for 'Ant' and 'AMs'
// 4733 entries after removing BHS only entries.
?>