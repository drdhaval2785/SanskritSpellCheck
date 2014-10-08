﻿<?php
/* set execution time to an hour */
ini_set('max_execution_time', 36000);
/* set memory limit to 1000 MB */
ini_set("memory_limit","1000M");
include "dev-slp.php";
include "slp-dev.php";
$ac = array("a","A","i","I","u","U","f","F","x","X","e","o","E","O",); // vowels - 'ac' letters
$hl = array("k","K","g","G","N","c","C","j","J","Y","w","W","q","Q","R","t","T","d","D","n","p","P","b","B","m","y","r","l","v","S","z","s","h","M","H"); 
$al = array("a","A","i","I","u","U","f","F","x","X","e","o","E","O","k","K","g","G","N","c","C","j","J","Y","w","W","q","Q","R","t","T","d","D","n","p","P","b","B","m","y","r","l","v","S","z","s","h","M","H");
$file=file_get_contents("meghadhuta.txt");
$file=str_replace("\r","",$file);
$file=str_replace("\n","",$file);
$file=str_replace("'","",$file);
$file=trim($file);
//echo $file;
$split=preg_split('/([aAiIuUfFxXeEoO])/',$file,0,PREG_SPLIT_DELIM_CAPTURE);
echo "Occurrence of vowels - ".((count($split)-1)/2)."<br>";
$split1=preg_split('/([kKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzshMH])/',$file,0,PREG_SPLIT_DELIM_CAPTURE);
echo "Occurrence of consonants - ".((count($split1)-1)/2)."<br>";
$split1=preg_split('/([kKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzshMH])/',$file,0,PREG_SPLIT_DELIM_CAPTURE);
echo "Ratio of consonants per 100 vowels -".(count($split1)*100)/count($split)."<br>";

?>