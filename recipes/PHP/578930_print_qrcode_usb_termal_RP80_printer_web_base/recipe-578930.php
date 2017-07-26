<?php

//printer setup
$printer="/dev/usb/lp0";

//formating qrcode
$text="hello i am printed from web at ".date("d/m/Y H:i:s");

function mystrtohex($str) {
  $ret="";for($i=0;$i< strlen($str); $i++){$ret.="\\x".bin2hex($str[$i]);}
  //need to use eval for "push" real hex values
  eval("\$ret=\"".$ret."\";");
  return $ret;
}


//https://code.google.com/p/python-escpos/wiki/Usage
//1.Set the Module Function 167  n between 1 and 16 (decimal) in hex
//1D 28 6B 03 00 31 43 n  
$string= "\x1D\x28\x6B\x03\x00\x31\x43\x04";


//2.Set correction error level Function 169 n \x30 -> 7% L \x31 -> 15% M \x32 -> 25% Q \x33 -> 30% H
//1D 28 6B 03 00 31 45 n 
$string .= "\x1D\x28\x6B\x03\x00\x31\x45\x33";


//3.Store Data Function 180 -> n storage chars (see below) + 3
//1D 28 6B n 00 31 50 30
//Note 0d = 13 chars
//need to use eval for "push" real hex values
eval("\$yy=\"\\x"."1D"."\\x"."28"."\\x"."6B"."\\x".sprintf("%02x",strlen($text)+3)."\\x"."00"."\\x"."31"."\\x"."50"."\\x"."30\";"); 

$string.=$yy;


//3.DATA 10 chars
//56 69 76 61 20 43 68 69 6c 65
//$data="\x56\x69\x76\x61\x20\x43\x68\x69\x6c\x65"; // 10 chars
$string .=mystrtohex($text);


//4.PRINT Function 181
//1D 28 6B 03 00 31 51 30
$string .= "\x1D\x28\x6B\x03\x00\x31\x51\x30";


//5.cut paper at end
//          line feed         ,  cut paper
$string .= "\x00\x1B\x33\x00"."\x1D\x56\x42\x00"; //."\x00\x1B\x32"; //line feed, and cut paper...

//end.formating qrcode

//send data to USB printer
$fp=fopen($printer, 'w');
fwrite($fp,$string);
fclose($fp);
			
?>
