<?php
error_reporting(0);
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
echo $header;
include 'faultfinder3a_utils.php';
// Code to arrange the ovsOalpha.txt according to dictionaries rather than only Alphabetical.
$input = file('ovsOalpha.txt');
$dictionaryname=array("ACC","CAE","AE","AP90","AP","BEN","BHS","BOP","BOR","BUR","CCS","GRA","GST","IEG","INM","KRM","MCI","MD","MW72","MW","MWE","PD","PE","PGN","PUI","PWG","PW","SCH","SHS","SKD","SNP","STC","VCP","VEI","WIL","YAT");
$hrefyear = array("2014","2014","2014","2014","2014","2014","2014","2014","2014","2013","2014","2014","2014","2014","2013","2014","2014","2014","2014","2014","2013","2014","2014","2014","2014","2013","2014","2014","2014","2013","2014","2013","2013","2014","2014","2014");

for ($i=0;$i<count($input);$i++)
{
	list($words[$i],$dicts[$i]) = explode("-",$input[$i]);
	$words[$i]=trim($words[$i]); $dicts[$i]=trim($dicts[$i]);
	list($word1[$i],$word2[$i]) = explode(":",$words[$i]);
	$word1[$i]=trim($word1[$i]); $word2[$i]=trim($word2[$i]);
	list($dict1[$i],$dict2[$i]) = explode(":",$dicts[$i]);
	$dict1[$i]=trim($dict1[$i]); $dict2[$i]=trim($dict2[$i]);
	$dict1separate[$i] = explode(",",$dict1[$i]);
	$dict1separate[$i]=array_map('trim',$dict1separate[$i]);
	$dict2separate[$i] = explode(",",$dict2[$i]);
	$dict2separate[$i]=array_map('trim',$dict2separate[$i]);
}
array_map('trim',$word1);
array_map('trim',$word2);
array_map('trim',$dict1);
array_map('trim',$dict2);

foreach ($dictionaryname as $value)
{
	$counter1=0;
	$counter2=0;
	$counter3=0;
	$counter4=0;
	$counter5=0;
	$counter6=0;
	$counter7=0;
	$counter8=0;
	$countervalue=0;
		//$value = "MW";
		$outtext = fopen("output/$value.txt","w+");
		$outhtml = fopen("output/$value.html","w+");
			fputs($outhtml,"<h2>One dictionary in first word and more dictionaries in second word</h2>\n");
			for ($j=0;$j<count($input);$j++)
			{
				if (count($dict1separate[$j])===1 && count($dict2separate[$j])>1 && in_array($value,$dict1separate[$j]))
				{
					fputs($outtext,$word1[$j].":".$word2[$j]."-".$dict1[$j].":".$dict2[$j]."\n"); 
					fputs($outhtml,$word1[$j].":".$word2[$j]."-".$dict1[$j].":".$dict2[$j]."<br>\n"); 
					$counter1++;
				}
			}
			fputs($outhtml,"<h2>One dictionary in second word and more dictionaries in first word</h2>\n");
			for ($j=0;$j<count($input);$j++)
			{	
				if (count($dict2separate[$j])===1 && count($dict1separate[$j])>1 && in_array($value,$dict2separate[$j]))
				{
					fputs($outtext,$word2[$j].":".$word1[$j]."-".$dict2[$j].":".$dict1[$j]."\n"); 
					fputs($outhtml,$word2[$j].":".$word1[$j]."-".$dict2[$j].":".$dict1[$j]."<br>\n"); 
					$counter2++;
				}
			}
			fputs($outhtml,"<h2>One dictionary in first word and one dictionary in second word</h2>\n");
			for ($j=0;$j<count($input);$j++)
			{	
				if (count($dict1separate[$j])===1 && count($dict2separate[$j])===1 && in_array($value,$dict1separate[$j]))
				{
					fputs($outtext,$word1[$j].":".$word2[$j]."-".$dict1[$j].":".$dict2[$j]."\n"); 
					fputs($outhtml,$word1[$j].":".$word2[$j]."-".$dict1[$j].":".$dict2[$j]."<br>\n"); 
					$counter3++;
				}
			}
			fputs($outhtml,"<h2>One dictionary in second word and one dictionary in first word</h2>\n");
			for ($j=0;$j<count($input);$j++)
			{	
				if (count($dict1separate[$j])===1 && count($dict2separate[$j])===1 && in_array($value,$dict2separate[$j]))
				{
					fputs($outtext,$word2[$j].":".$word1[$j]."-".$dict2[$j].":".$dict1[$j]."\n"); 
					fputs($outhtml,$word2[$j].":".$word1[$j]."-".$dict2[$j].":".$dict1[$j]."<br>\n"); 
					$counter4++;
				}
			}
			fputs($outhtml,"<h2>More than one dictionary in first word and even more dictionaries in second word</h2>\n");
			for ($j=0;$j<count($input);$j++)
			{		
				if (count($dict1separate[$j])<count($dict2separate[$j]) && count($dict2separate[$j])>1 && count($dict1separate[$j])>1 && in_array($value,$dict1separate[$j]) )
				{
					fputs($outtext,$word1[$j].":".$word2[$j]."-".$dict1[$j].":".$dict2[$j]."\n"); 
					fputs($outhtml,$word1[$j].":".$word2[$j]."-".$dict1[$j].":".$dict2[$j]."<br>\n"); 
					$counter5++;
				}
			}
			fputs($outhtml,"<h2>More than one dictionary in second word and even more dictionaries in first word</h2>\n");
			for ($j=0;$j<count($input);$j++)
			{	
				if (count($dict2separate[$j])<count($dict1separate[$j]) && count($dict1separate[$j])>1 && count($dict2separate[$j])>1 && in_array($value,$dict2separate[$j]) )
				{
					fputs($outtext,$word2[$j].":".$word1[$j]."-".$dict2[$j].":".$dict1[$j]."\n"); 
					fputs($outhtml,$word2[$j].":".$word1[$j]."-".$dict2[$j].":".$dict1[$j]."<br>\n"); 
					$counter6++;
				}
			}
			fputs($outhtml,"<h2>More than one dictionary in first word and equal dictionaries in second word</h2>\n");
			for ($j=0;$j<count($input);$j++)
			{	
				if (count($dict1separate[$j])===count($dict2separate[$j])  && count($dict1separate[$j])>1 && count($dict2separate[$j])>1 && in_array($value,$dict1separate[$j]))
				{
					fputs($outtext,$word1[$j].":".$word2[$j]."-".$dict1[$j].":".$dict2[$j]."\n"); 
					fputs($outhtml,$word1[$j].":".$word2[$j]."-".$dict1[$j].":".$dict2[$j]."<br>\n"); 
					$counter7++;
				}
			}
			fputs($outhtml,"<h2>More than one dictionary in second word and equal dictionaries in the first word</h2>\n");
			for ($j=0;$j<count($input);$j++)
			{	
				if (count($dict1separate[$j])===count($dict2separate[$j])  && count($dict1separate[$j])>1 && count($dict2separate[$j])>1 && in_array($value,$dict2separate[$j]))
				{
					fputs($outtext,$word1[$j].":".$word2[$j]."-".$dict1[$j].":".$dict2[$j]."\n"); 
					fputs($outhtml,$word1[$j].":".$word2[$j]."-".$dict1[$j].":".$dict2[$j]."<br>\n"); 
					$counter8++;
				}
			}
	//This testing shows that all the cases are covered.
/*	echo count($input)."<br>";
	echo $counter1."<br>";
	echo $counter2."<br>";
	echo $counter3."<br>";
	echo $counter4."<br>";
	echo $counter5."<br>";
	echo $counter6."<br>";
	echo $counter7."<br>";
	echo $counter8."<br>";
	echo $counter1+$counter2+$counter3+$counter4+$counter5+$counter6+$counter7+$counter8."<br>";
	fclose($outtext);
	fclose($outhtml);*/
}

foreach ($dictionaryname as $value)
{
	echo "$value is printing.<br>";
	$in = file("output/".$value.".html");
	$out = array_map("givelinktoo_vs_Otext",$in);
	$outfile = fopen("output/$value.html","w+");
	$outputdata = implode("<br>\n",$out);
	fputs($outfile,$header);
	fputs($outfile,$outputdata);
	fclose($outfile);
}
	
?>