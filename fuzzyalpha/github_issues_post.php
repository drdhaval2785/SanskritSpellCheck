<?php
// A PHP code to prepare copy paste material for Github from the corrected fuzzyalpha files.
/* Typical fuzzyalpha file looks like this.
069 tretAyuga
069 triBuvanaSfezWa -> triBuvanaSrezWa
069 triBuvanaviBu
069 headword <a target='_INMword' href='http://www.sanskrit-lexicon.uni-koeln.de/scans/INMScan/2013/web/webtc/indexcaller.php?input=slp1&output=deva&key=triBuvanaSfezWa'>triBuvanaSfezWa</a> ---  page <a target='_INMpage' href='http://www.sanskrit-lexicon.uni-koeln.de/scans/INMScan/2013/web/webtc/servepdf.php?page=679'>679-2</a>
*/
// The first and third line are the words above and below the disputed word.
// Second line is the actual correction line. If there is no correction it would have -> NO CHANGE
// Fourth line is for copy pasting the links to Github.
$dict = "pui"; // Dictionary short name.
$input = file_get_contents($dict."-fuzzybeta.txt");
$out1 = fopen($dict."_change.txt","w+");
$out2 = fopen($dict."_nochange.txt","w+");

$data = explode('------------------------------------------------------------------------',$input);
//print_r($data);

foreach ($data as $value)
{
	if (strpos($value,"NO CHANGE")!==false)
	{
		fputs($out2,$value."<hr>");
	}
	else
	{
		fputs($out1,$value."<hr>");
	}
}

?>