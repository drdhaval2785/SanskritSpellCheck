<?php  
/*
error_reporting(E_ALL);
ini_set('display_errors', '1');
*/
/* faultfinder1.php  modification by ejf of faultfinder.php
  1. Read parameters from $argv
    dicta  ( a code for first dictionary)
    dictb  ( a code for second dictionary)
    dictref ( a code for href )
    output ( name of output file)
    Usage from commandline only:
     php faultfinder1.php <dict1> <dict2> <dictref> <output>
*/
/* This code is written by Dr. Dhaval Patel of www.sanskritworld.in.
 * Video tutorial for its use is available at http://youtu.be/qLqYUZUGM6M
 * Code is available at https://github.com/drdhaval2785/SanskritSpellCheck.
 * https://www.youtube.com/watch?v=rKZ_OsSHwsY&feature=youtu.be is the method of finding and noting wrong entries at https://github.com/sanskrit-lexicon/CORRECTIONS/issues
 * Google doc for understanding the logic behind the machine is https://docs.google.com/document/d/1G4HoDz9nuj2GPeHQopNVSnDEGrnXtoAuXFugj4sQHZg/edit?usp=sharing
 */
 
/* set execution time to an hour */
//ini_set('max_execution_time', 36000);
/* set memory limit to 1000 MB */
//ini_set("memory_limit","1000M");
// include these two files for conversion
include "dev-slp.php";
include "slp-dev.php";

$dicta = $argv[1];
$dictb = $argv[2];
$dictref = $argv[3];
$output = $argv[4];
if  (!$output) { 
 // If there are NOT 4 arguments, compute 
 // default values for dictref and output from dicta and dictb
 $dictref = $dictb;
 $output = $dictb . "vs" . $dicta . ".html";
}echo "$dicta, $dictb, $output\n";
// open file where we store the suspect wrong entries.
//$outfile=fopen("suspectfalse.html","w+");
$outfile=fopen($output,"w");  // completely overwrite
// adding HTML head for utf-8
fputs($outfile,'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <META HTTP-EQUIV="Content-Language" CONTENT="HI">
  <!--<meta name="language" content="hi"> -->
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  </meta>
</head>
    <body>');


// Assume dictfiles are in same directory as program
$dictfilea = $dicta . "slp.txt" ; 
$dictfileb = $dictb . "slp.txt" ;
/* Slurp the dictionaries into arrays BEFORE the loop, for efficiency 
  Assume dictionary file contains headwords, one per line
*/

$filea = file($dictfilea);
if (! $filea) {
 echo "ERROR $dicta: file $filea not found\n";
 exit(1);
}
echo "$dictfilea has " . count($filea) . " lines\n";
$fileb = file($dictfileb);
if (! $fileb) {
 echo "ERROR $dictb: file $fileb not found\n";
 exit(1);
}
echo "$dictfileb has " . count($fileb) . " lines\n";
/* from $dictref, construct base of href ($hrefbase).
for example (if $dicta == 'MW'):
 $hrefbase = "http://www.sanskrit-lexicon.uni-koeln.de/scans/MWScan/2014/web/webtc/indexcaller.php"
 The only question is what is the year (like 2014 for MW).
 Note, for instance, that PW  is needed rather than PWK for this href.  And,
     dictfilea also PWslp.txt (not PWKslp.txt)
 These need to be expanded to include all dictionaries that are 2013.
*/
$hrefyeardict=array("ACC" => "2014","AE" => "2014","AP" => "2014","AP90" => "2014",
       "BEN" => "2014","BHS" => "2014","BOP" => "2014","BOR" => "2014",
       "BUR" => "2013","CAE" => "2014","CCS" => "2014","GRA" => "2014",
       "GST" => "2014","IEG" => "2014","INM" => "2013","KRM" => "2014",
       "MCI" => "2014","MD" => "2014","MW" => "2014","MW72" => "2014",
       "MWE" => "2013","PD" => "2014","PE" => "2014","PGN" => "2014",
       "PUI" => "2014","PWG" => "2013","PW" => "2014","SCH" => "2014",
       "SHS" => "2014","SKD" => "2013","SNP" => "2014","STC" => "2013",
       "VCP" => "2013","VEI" => "2014","WIL" => "2014","YAT" => "2014");
$hrefyear = $hrefyeardict[$dictref];
if (! $hrefyear) {
 echo "ERROR: Unknown dictref = $dictref\n";
 exit(1);
}
$hrefbase = "http://www.sanskrit-lexicon.uni-koeln.de/scans/".$dictref."Scan/".$hrefyear."/web/webtc/indexcaller.php";
echo "hrefbase = $hrefbase\n";
// running a for loop for 10 different type of Consonant, Vowel patterns.
for($b=0;$b<10;$b++)
{
if ($b===0)
{
    fputs($outfile,'<b style="color:red">This is Vowel-Vowel pattern.</b><br>');
}
if ($b===1)
{
    fputs($outfile,'<b style="color:red">This is Vowel-Consonant-Vowel pattern.</b><br>');
}
if ($b===2)
{
    fputs($outfile,'<b style="color:red">This is Vowel-Consonant-Consonant-Vowel pattern.</b><br>');
}
if ($b===3)
{
    fputs($outfile,'<b style="color:red">This is Vowel-Consonant-Consonant-Consonant-Vowel pattern.</b><br>');
}
if ($b===4)
{
    fputs($outfile,'<b style="color:red">This is Vowel-Consonant-Consonant-Consonant-Consonant-Vowel pattern.</b><br>');
}
if ($b===5)
{
    fputs($outfile,'<b style="color:red">This is Vowel-Consonant-Consonant-Consonant-Consonant-Consonant-Vowel pattern.</b><br>');
}
if ($b===6)
{
    fputs($outfile,'<b style="color:red">This is Start-Consonant-Consonant pattern.</b><br>');
}
if ($b===7)
{
    fputs($outfile,'<b style="color:red">This is Consonant-Consonant-End pattern.</b><br>');
}
if ($b===8)
{
    fputs($outfile,'<b style="color:red">This is Consonant-Consonant-Consonant-End pattern.</b><br>');
}
if ($b===9)
{
    fputs($outfile,'<b style="color:red">This is Consonant-Consonant-Consonant-Consonant-End pattern.</b><br>');
}

// Regular expression for finding out these 10 patterns. New can be added if needed.
if ($b===0)
{
    $pattern  = '/([aAiIuUfFxXeEoO][aAiIuUfFxXeEoO])/';
}
if ($b===1)
{
    $pattern  = '/([aAiIuUfFxXeEoO][kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs][aAiIuUfFxXeEoO])/';
}
if ($b===2)
{
    $pattern  = '/([aAiIuUfFxXeEoO][kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs][kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs][aAiIuUfFxXeEoO])/';
}
if ($b===3)
{
    $pattern  = '/([aAiIuUfFxXeEoO][kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs][kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs][kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs][aAiIuUfFxXeEoO])/';
}
if ($b===4)
{
    $pattern  = '/([aAiIuUfFxXeEoO][kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs][kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs][kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs][kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs][aAiIuUfFxXeEoO])/';
}
if ($b===5)
{
    $pattern  = '/([aAiIuUfFxXeEoO][kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs][kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs][kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs][kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs][kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs][aAiIuUfFxXeEoO])/';
}
if ($b===6)
{
    $pattern  = '/^([kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs][kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs])/';
}
if ($b===7)
{
    $pattern  = '/([kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs][kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs])$/';
}
if ($b===8)
{
    $pattern  = '/([kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs][kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs][kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs])$/';
}
if ($b===9)
{
    $pattern  = '/([kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs][kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs][kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs][kKgGNcCjJYwWqQRtTdDnpPbBmyrlvzSs])$/';
}

// This is the place we will have to change for different dictionaries. first parameter is the base dictionary. second is fixed. Third is the dictionary we want to check.
//comparepatterns($filea,$b,$fileb); 
comparepatterns($filea,$pattern,$fileb,$outfile,$hrefbase); 
}

/* function comparepatterns 
 * $a is the file contents of dictionary whose pattern we want to take as input (Base).
 * $b refers to the pattern we want to check. $pattern is that pattern ( a regex string)
 * 0 - Vowel-Vowel (VV)
 * 1 - Vowel-Consonant-Vowel (VCV)
 * 2 - Vowel-Consonant-Consonant-Vowel (VCCV)
 * 3 - Vowel-Consonant-Consonant-Consonant-Vowel (VCCCV)
 * 4 - Vowel-Consonant-Consonant-Consonant-Consonant-Vowel (VCCCCV)
 * 5 - Vowel-Consonant-Consonant-Consonant-Consonant-Consonant-Vowel (VCCCCCV)
 * 6 - Start-Consonant-Consonant (^CC)
 * 7 - Consonant-Consonant-End (CC$)
 * 8 - Consonant-Consonant-Consonant-End (CCC$)
 * 9 - Consonant-Consonant-Consonant-Consonant-End (CCCC$)
 * $c is the contents of dictionary file to be checked.
 $outfile - File handle for output
 $hrefbase = Base of href to be written
 */
function comparepatterns($filea,$pattern,$filec,$outfile,$hrefbase)
{
    // global $outfile; global $b; global $pattern;  Don't need globals. All passed as args
//$file= file($a);
$file = $filea;
$vccccv=array();
foreach ($file as $value)
{
    if(preg_match($pattern,$value))
    {
        $vccccvraw = preg_split($pattern,$value,null,PREG_SPLIT_DELIM_CAPTURE);
        $i=2;
        while($i<count($vccccvraw))
        {
            if(!in_array($vccccvraw[$i-1],$vccccv))
            {
            $vccccv=array_merge($vccccv,array($vccccvraw[$i-1]));
            }
            $i=$i+2;
        }
    }
}
$vccccv = array_unique($vccccv);
$vccccv = array_values($vccccv);
    // checking the second file.
    //$file1=file($c);
    $file1 = $filec;
    foreach ($file1 as $value)
    {
        if(preg_match($pattern,$value))
        {
            $vccccvex = preg_split($pattern,$value,null,PREG_SPLIT_DELIM_CAPTURE);        
            $i=2;
            while ($i<count($vccccvex))
            {
// if not found in the patterns already noted - flag it as suspect pattern and enter in suspectfalse.html
                if ( !in_array($vccccvex[$i-1],$vccccv ))
                {
                      fputs($outfile,'  <a href="'.$hrefbase.'?key='.$value.'&input=slp1&output=SktDevaUnicode" target="_blank">'.$value."</a> - ".convert($value)." - ".$vccccvex[$i-1]."<br>");
                }
                $i=$i+2;
            }
        }
    }
}
fputs($outfile,'</body></html>');
    fclose($outfile);

    
    
?>