<?php
/* set execution time to an hour */
ini_set('max_execution_time', 36000);
/* set memory limit to 1000 MB */
ini_set("memory_limit","1000M");
include "dev-slp.php";
include "function.php";
include "slp-dev.php";

$outfile = fopen('tobepasted.txt','w+');
// giving links to the list of .txt and converting to html
include 'faultfinder3a_utils.php';
function givelinktoo_vs_Otext($text)
{
	global $outfile;
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
	fputs($outfile,convert($words[0])."_:_".convert($words[1])." - ".$words[0].":".$words[1]."<br/>".$dicts[0]."<hr/>\n");
}


$file = file('ovsOalpha.txt');
foreach ($file as $value)
{
	$couter=1;
	if (strpos($value,'1')===0||strpos($value,'2')===0||strpos($value,'3')===0||strpos($value,'4')===0||strpos($value,'5')===0||strpos($value,'6')===0||strpos($value,'7')===0||strpos($value,'8')===0||strpos($value,'9')===0||strpos($value,'0')===0)
	{
	
	}
	else
	{
		$parts=preg_split('/([:-])/',$value);
		givelinktoo_vs_Otext($value);
//		echo "$counter $parts[0] -> $parts[2] headword <a target='_INMword' href='http://www.sanskrit-lexicon.uni-koeln.de/scans/INMScan/2013/web/webtc/indexcaller.php?input=slp1&output=deva&key=asaYjYa'>asaYjYa</a> ---  page <a target='_INMpage' href='http://www.sanskrit-lexicon.uni-koeln.de/scans/INMScan/2013/web/webtc/servepdf.php?page=092'>092-2</a> <hr/>";
	}
}

fclose($outfile);


?>