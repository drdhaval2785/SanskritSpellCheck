<?php
//error_reporting(0);
$header = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
      <style>
         table.fixed {table-layout:fixed; width:100%; border:1px solid black;}/*Setting the table width is important!*/
         td.zero {width:50px; border:1px solid black; text-overflow:ellipsis; }
         td.one {width:200px; border:1px solid black; text-overflow:ellipsis; padding: 10px;}
         td.two {width:200px; border:1px solid black;text-overflow:ellipsis; padding: 10px;}
         td.three {width:100px; border:1px solid black;text-overflow:ellipsis; padding: 10px;}
         td.four {width:100px; border:1px solid black;text-overflow:ellipsis; padding: 10px;}
		 td {overflow:scroll;}
      </style>
<!--... Defining UTF-8 as our default character set, so that devanagari is displayed properly. -->
<meta charset="UTF-8">
</head> 
<body>
';
//echo $header;
include 'faultfinder3a_utils.php';
// Code to arrange the ovsOalpha.txt according to dictionaries rather than only Alphabetical.
$input = file('o_vs_O2.txt');
$dictionaryname=array("ACC","CAE","AE","AP90","AP","BEN","BHS","BOP","BOR","BUR","CCS","GRA","GST","IEG","INM","KRM","MCI","MD","MW72","MW","MWE","PD","PE","PGN","PUI","PWG","PW","SCH","SHS","SKD","SNP","STC","VCP","VEI","WIL","YAT");
$hrefyear = array("2014","2014","2014","2014","2014","2014","2014","2014","2014","2013","2014","2014","2014","2014","2013","2014","2014","2014","2014","2014","2013","2014","2014","2014","2014","2013","2014","2014","2014","2013","2014","2013","2013","2014","2014","2014");
//$dictionaryname=array("ACC");
//$hrefyear = array("2014");

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
	$dict1sepwithoutlnum[$i]=array_map('removelnum1',$dict1separate[$i]);
	$dict2separate[$i] = explode(",",$dict2[$i]);
	$dict2separate[$i]=array_map('trim',$dict2separate[$i]);
	$dict2sepwithoutlnum[$i]=array_map('removelnum1',$dict2separate[$i]);
}
array_map('trim',$word1);
array_map('trim',$word2);
array_map('trim',$dict1);
array_map('trim',$dict2);
$outtext1 = fopen("output3/composite1.txt","w+");
$outtext2 = fopen("output3/composite2.txt","w+");
$outtext3 = fopen("output3/composite3.txt","w+");
$outhtml1 = fopen("output3/composite1.html","w+");
$outhtml2 = fopen("output3/composite2.html","w+");
$outhtml3 = fopen("output3/composite3.html","w+");
fputs($outhtml1,"<h2>Highest probability (One dictionary in first word and more dictionaries in second word)</h2>\n");	
fputs($outhtml2,"<h2>Medium probability (One dictionary in first word and one dictionary in second word)</h2>\n");
fputs($outhtml3,"<h2>Lowest probability (More than one dictionary in first word and it has dictionary under consideration)</h2>\n");

$counter = count($input);
$counter1 = 0;
$counter2 = 0;
$counter3 = 0;
$counter4 = 0;
$counter5 = 0;
$counter6 = 0;
for($j=0;$j<count($input);$j++)
{
	//echo $word1[$j], count($dict1separate[$j]), count($dict2separate[$j]), arrinter($dict1sepwithoutlnum[$j],$dict2sepwithoutlnum[$j])."\n";
	if (count($dict1separate[$j])===1 && count($dict2separate[$j])>1 && arrinter($dict1sepwithoutlnum[$j],$dict2sepwithoutlnum[$j])===0)
	{
		fputs($outtext1,convert($word1[$j])."->".convert($word2[$j])."\n"); 
		fputs($outhtml1,$word1[$j].":".$word2[$j]."-".$dict1[$j].":".$dict2[$j]."<br>\n"); 
		$counter1++;
	}
	elseif (count($dict2separate[$j])===1 && count($dict1separate[$j])>1 && arrinter($dict1sepwithoutlnum[$j],$dict2sepwithoutlnum[$j])===0)
	{
		fputs($outtext1,convert($word2[$j])."->".convert($word1[$j])."\n"); 
		fputs($outhtml1,$word2[$j].":".$word1[$j]."-".$dict2[$j].":".$dict1[$j]."<br>\n"); 
		$counter2++;
	}
	elseif (count($dict1separate[$j])===1 && count($dict2separate[$j])===1 && arrinter($dict1sepwithoutlnum[$j],$dict2sepwithoutlnum[$j])===0)
	{
		fputs($outtext2,convert($word1[$j])."->".convert($word2[$j])."\n"); 
		fputs($outhtml2,$word1[$j].":".$word2[$j]."-".$dict1[$j].":".$dict2[$j]."<br>\n"); 
		$counter3++;
	}
	elseif ( count($dict1separate[$j])>1 && count($dict2separate[$j])>1 && arrinter($dict1sepwithoutlnum[$j],$dict2sepwithoutlnum[$j])===0)
	{
		fputs($outtext3,convert($word1[$j])."->".convert($word2[$j])."\n"); 
		fputs($outhtml3,$word1[$j].":".$word2[$j]."-".$dict1[$j].":".$dict2[$j]."<br>\n"); 
		$counter4++;
	}
	elseif (arrinter($dict1sepwithoutlnum[$j],$dict2sepwithoutlnum[$j])>0)
	{
		fputs($outtext3,convert($word1[$j])."->".convert($word2[$j])."\n"); 
		fputs($outhtml3,$word1[$j].":".$word2[$j]."-".$dict1[$j].":".$dict2[$j]."<br>\n"); 
		$counter5++;
	}
	else
	{
		echo $word1[$j]."\n";
	}
}
echo $counter1."+".$counter2."+".$counter3."+".$counter4."+".$counter5." / ".$counter." occurrences are handled.<br/>\n";
echo $counter1+$counter2+$counter3+$counter4+$counter5." / ".$counter." occurrences are handled.<br/>\n";
fclose($outtext1);
fclose($outhtml1);
fclose($outtext2);
fclose($outhtml2);
fclose($outtext3);
fclose($outhtml3);

# MW;1254 -> MW
function removelnum1($dictwithlnum)
{
	return explode(';',$dictwithlnum)[0];
}
function arrinter($one,$two)
{
	return count(array_intersect($one,$two));
}
/*
foreach ($dictionaryname as $value)
{
	echo "$value dictionary is being treated<br/>\n";
	$counter1=0;
	$counter2=0;
	$counter3=0;
	$counter4=0;
	$counter5=0;
	$counter6=0;
	$counter7=0;
	$countervalue=0;
		//$value = "MW";
			for ($j=0;$j<count($input);$j++)
			{
				if ( (indict_with_lnum($value,$dict1separate[$j]) || indict_with_lnum($value,$dict2separate[$j])) && !(indict_with_lnum($value,$dict1separate[$j]) && indict_with_lnum($value,$dict2separate[$j])) )
				{
					$countervalue++;
				} 			
			}
		$outtext = fopen("output2/$value.txt","w+");
		$outhtml = fopen("output2/$value.html","w+");			
			fputs($outhtml,"<h2>Highest probability (One dictionary in first word and more dictionaries in second word)</h2>\n");
			for ($j=0;$j<count($input);$j++)
			{
				if (count($dict1separate[$j])===1 && count($dict2separate[$j])>1 && indict_with_lnum($value,$dict1separate[$j]) && !indict_with_lnum($value,$dict2separate[$j]))
				{
					fputs($outtext,convert($word1[$j])."->".convert($word2[$j])."\n"); 
					fputs($outhtml,$word1[$j].":".$word2[$j]."-".$dict1[$j].":".$dict2[$j]."<br>\n"); 
					$counter1++;
				}
			}
			//fputs($outhtml,"<h2>One dictionary in second word and more dictionaries in first word</h2>\n");
			for ($j=0;$j<count($input);$j++)
			{	
				if (count($dict2separate[$j])===1 && count($dict1separate[$j])>1 && indict_with_lnum($value,$dict2separate[$j]) && !indict_with_lnum($value,$dict1separate[$j]))
				{
					fputs($outtext,convert($word2[$j])."->".convert($word1[$j])."\n"); 
					fputs($outhtml,$word2[$j].":".$word1[$j]."-".$dict2[$j].":".$dict1[$j]."<br>\n"); 
					$counter2++;
				}
			}
			fputs($outhtml,"<h2>Medium probability (One dictionary in first word and one dictionary in second word)</h2>\n");
			for ($j=0;$j<count($input);$j++)
			{	
				if (count($dict1separate[$j])===1 && count($dict2separate[$j])===1 && indict_with_lnum($value,$dict1separate[$j]) && !indict_with_lnum($value,$dict2separate[$j]))
				{
					fputs($outtext,convert($word1[$j])."->".convert($word2[$j])."\n"); 
					fputs($outhtml,$word1[$j].":".$word2[$j]."-".$dict1[$j].":".$dict2[$j]."<br>\n"); 
					$counter3++;
				}
			}
			//fputs($outhtml,"<h2>One dictionary in second word and one dictionary in first word</h2>\n");
			for ($j=0;$j<count($input);$j++)
			{	
				if (count($dict1separate[$j])===1 && count($dict2separate[$j])===1 && indict_with_lnum($value,$dict2separate[$j]) && !indict_with_lnum($value,$dict1separate[$j]))
				{
					fputs($outtext,convert($word2[$j])."->".convert($word1[$j])."\n"); 
					fputs($outhtml,$word2[$j].":".$word1[$j]."-".$dict2[$j].":".$dict1[$j]."<br>\n"); 
					$counter4++;
				}
			}
			fputs($outhtml,"<h2>Lowest probability (More than one dictionary in first word and it has dictionary under consideration)</h2>\n");
			for ($j=0;$j<count($input);$j++)
			{	
				if ( count($dict1separate[$j])>1 && indict_with_lnum($value,$dict1separate[$j]) && !indict_with_lnum($value,$dict2separate[$j]) )
				{
					fputs($outtext,convert($word1[$j])."->".convert($word2[$j])."\n"); 
					fputs($outhtml,$word1[$j].":".$word2[$j]."-".$dict1[$j].":".$dict2[$j]."<br>\n"); 
					$counter5++;
				}
			}
			//fputs($outhtml,"<h2>More than one dictionary in second word and it has dictionary under consideration</h2>\n");
			for ($j=0;$j<count($input);$j++)
			{	
				if (count($dict2separate[$j])>1 && indict_with_lnum($value,$dict2separate[$j]) && !indict_with_lnum($value,$dict1separate[$j]) )
				{
					fputs($outtext,convert($word2[$j])."->".convert($word1[$j])."\n"); 
					fputs($outhtml,$word2[$j].":".$word1[$j]."-".$dict2[$j].":".$dict1[$j]."<br>\n"); 
					$counter6++;
				}
			}
	//This testing shows that all the cases are covered.
	echo $counter1."+".$counter2."+".$counter3."+".$counter4."+".$counter5."+".$counter6." / ".$countervalue." occurrences are handled.<br/>\n";
	echo $counter1+$counter2+$counter3+$counter4+$counter5+$counter6." / ".$countervalue." occurrences are handled.<br/>\n";
	fclose($outtext);
	fclose($outhtml);
}

foreach ($dictionaryname as $value)
{
	echo "$value is printing.<br/>\n";
	$in = file("output2/".$value.".html");
	$outfile = fopen("output2/$value.html","w+");
	fputs($outfile,$header);
	fputs($outfile,"<h1>$value - list of possible errors found by o_vs_O method</h1>");
	fputs($outfile,'<table class="fixed">');
	$count=1;
	foreach($in as $value1)
	{
		if (strpos($value1,"<h2>")===false)
		{
			$val =givelinktoo_vs_Otext3($value1);
			$count++;
		}
		else
		{
			$val = "</table>".$value1.'<table class="fixed">';
		}
		fputs($outfile,$val);
	}
	fputs($outfile,"</table>");
	fclose($outfile);
}
*/
?>