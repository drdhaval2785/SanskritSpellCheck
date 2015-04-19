<?php
/* set execution time to an hour */
ini_set('max_execution_time', 36000);
/* set memory limit to 1000 MB */
ini_set("memory_limit","1000M");
include "dev-slp.php";
include "function.php";
include "slp-dev.php";

$outfile1 = fopen('nochange_ovsO.txt','w+');
$outfile2 = fopen('change_ovsO.txt','w+');

// giving links to the list of .txt and converting to html
include 'faultfinder3a_utils.php';
function givelinktoo_vs_Otext($text)
{
	global $outfile;
    $x = explode('=',$text);
	$x = array_map('trim',$x);
	$dicts = explode(':',$x[1]);
	$dicts = array_map('trim',$dicts);
	$words = explode('->',$x[0]);
	$words = array_map('trim',$words);
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
	fputs($outfile,$words[0]." -> ".$words[1]."<br/>".$dicts[0]."<hr/>\n");
}


$file = file('ovsOalpha.txt');
foreach ($file as $value)
{
	$couter=1;
	if (strpos($value,'->')!==false)
	{
		$outfile = $outfile2;
		givelinktoo_vs_Otext($value);	
	}
	else
	{
		$outfile = $outfile1;
		fputs($outfile,$value);
	}
}

fclose($outfile);


?>