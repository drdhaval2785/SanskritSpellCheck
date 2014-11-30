﻿<?php
/* set execution time to an hour */
ini_set('max_execution_time', 36000);
/* set memory limit to 1000 MB */
ini_set("memory_limit","1000M");
//include "dev-slp.php";
//include "slp-dev.php";
$az=array("a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",);
$digit=array("1","2","3","4","5","6","7","8","9","0",);
$ac = array("a","A","i","I","u","U","f","F","x","X","e","o","E","O",); // vowels - 'ac' letters
$hl = array("k","K","g","G","N","c","C","j","J","Y","w","W","q","Q","R","t","T","d","D","n","p","P","b","B","m","y","r","l","v","S","z","s","h","M","H"); 
$al = array("a","A","i","I","u","U","f","F","x","X","e","o","E","O","k","K","g","G","N","c","C","j","J","Y","w","W","q","Q","R","t","T","d","D","n","p","P","b","B","m","y","r","l","v","S","z","s","h","M","H");
$file=file_get_contents("meghadhuta-CVC-SLP1.txt");
$file=str_replace(array("1","2","3","4","5","6","7","8","9","0",".","'","?",",","[","]"," ","/","_","*"),array("","","","","","","","","","","","","","","","","","","",""),$file);
foreach($az as $val1)
{
    foreach  ($digit as $val2)
    {
        $file=str_replace($val2."ab",$val2,$file);
        $file=str_replace($val2."cd",$val2,$file);
        $file=str_replace($val2.$val1." ",$val2,$file);
    }
}
$file=str_replace("\r","",$file);
$file=str_replace("<br>","",$file);
$file=str_replace("\n","",$file);
$file=trim($file);
//echo $file."<br>";
$split=preg_split('/([aAiIuUfFxXeEoO])/',$file,0,PREG_SPLIT_DELIM_CAPTURE);
echo "Occurrence of vowels - ".((count($split)-1)/2)."<br>";
$split1=preg_split('/([kKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzshMH])/',$file,0,PREG_SPLIT_DELIM_CAPTURE);
echo "Occurrence of consonants - ".((count($split1)-1)/2)."<br>";
$split1=preg_split('/([kKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzshMH])/',$file,0,PREG_SPLIT_DELIM_CAPTURE);
$figure = (count($split1)*100)/count($split);
$roundedfigure = round($figure,2);
echo "Ratio of consonants per 100 vowels -".$roundedfigure."<br>";

?>