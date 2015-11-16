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
include 'faultfinder3a_utils.php';

function decoratehtml($inputfile,$outputfile1,$outputfile2)
{
	global $header;
	$in = file($inputfile);
	$outfile = fopen($outputfile1,"w+");
	$outtxt = fopen($outputfile2,"w+");
	fputs($outfile,$header);
	fputs($outfile,"<h1>Highest probability words found by o_vs_O method.</h1>");
	fputs($outfile,'<table class="fixed">');
	global $count;
	$count = 1;
	foreach($in as $value1)
	{
		$val =givelinktoo_vs_Otext4($value1);
		$count++;
		fputs($outfile,$val);
		fputs($outtxt,suggestwords($value1)."\n");
	}
	fputs($outfile,"</table></body></html>");
	fclose($outfile);
}
echo "Preparing composite1a.html for comparision.\n";
$outfile = fopen('output3/composite1a.html','w');
fputs($outfile,$header);
fputs($outfile,"<h1>Highest probability words found by o_vs_O method.</h1>");
fputs($outfile,'<table class="fixed">');
decoratehtml('output3/composite1a.txt','output3/composite1a.html','output3/composite1b.txt');

echo "Preparing composite2a.html for comparision.\n";
$outfile = fopen('output3/composite2a.html','w');
fputs($outfile,$header);
fputs($outfile,"<h1>Medium probability words found by o_vs_O method.</h1>");
fputs($outfile,'<table class="fixed">');
decoratehtml('output3/composite2a.txt','output3/composite2a.html','output3/composite2b.txt');

echo "Preparing composite3a.html for comparision.\n";
$outfile = fopen('output3/composite3a.html','w');
fputs($outfile,$header);
fputs($outfile,"<h1>Lowest probability words found by o_vs_O method.</h1>");
fputs($outfile,'<table class="fixed">');
decoratehtml('output3/composite3a.txt','output3/composite3a.html','output3/composite3b.txt');
?>